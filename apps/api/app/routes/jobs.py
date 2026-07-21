"""Job description CRUD routes."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import get_current_user
from app.db import get_db
from app.models.schemas import JobCreate, JobPublic, JobRematchResponse, JobUpdate, UserPublic
from app.services.audit import write_audit
from app.services.rematch import enqueue_rematch_for_job, iter_latest_parsed_resumes

router = APIRouter(prefix="/v1/jobs", tags=["jobs"])


def _jd_hash(jd: dict) -> str:
    """Return a stable hash for a canonical JD payload."""
    return hashlib.sha256(
        json.dumps(jd, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()


def _is_result_stale(result: dict[str, Any], jd_revision: int) -> bool:
    """Return True when a match row is out of date for the current JD revision."""
    if result.get("stale") is True:
        return True
    return int(result.get("jd_revision") or 0) != jd_revision


async def _stale_match_count(org_id: str, job_id: str, jd_revision: int) -> int:
    """Count current candidates whose latest match is stale for the job JD."""
    db = get_db()
    pipeline: list[dict[str, Any]] = [
        {"$match": {"org_id": org_id, "job_id": job_id}},
        {
            "$sort": {
                "is_current": -1,
                "updated_at": -1,
                "created_at": -1,
            }
        },
        {"$group": {"_id": "$candidate_id", "result": {"$first": "$$ROOT"}}},
        {"$replaceRoot": {"newRoot": "$result"}},
    ]
    count = 0
    async for row in db.match_results.aggregate(pipeline):
        if _is_result_stale(row, jd_revision):
            count += 1
    return count


async def _rematch_status_for_job(org_id: str, job_id: str) -> dict[str, Any]:
    """Return whether a manual rematch batch is currently running."""
    db = get_db()
    batch = await db.ingest_batches.find_one(
        {
            "org_id": org_id,
            "job_id": job_id,
            "source": "rematch",
            "status": {"$in": ["queued", "processing"]},
        },
        sort=[("created_at", -1)],
    )
    if batch:
        return {
            "rematch_in_progress": True,
            "active_rematch_batch_id": str(batch["_id"]),
        }
    return {"rematch_in_progress": False, "active_rematch_batch_id": None}


def _job_public(doc: dict, counts: dict | None = None) -> JobPublic:
    """Map a Mongo job document to the public schema."""
    counts = counts or {}
    return JobPublic(
        id=str(doc["_id"]),
        org_id=doc["org_id"],
        status=doc["status"],
        jd=doc["jd"],
        jd_schema_version=doc.get("jd_schema_version", "jd.v1"),
        jd_revision=int(doc.get("jd_revision") or 1),
        created_by=doc.get("created_by"),
        created_at=doc["created_at"],
        updated_at=doc["updated_at"],
        candidate_count=counts.get("candidate_count", 0),
        needs_review_count=counts.get("needs_review_count", 0),
        shortlisted_count=counts.get("shortlisted_count", 0),
        stale_match_count=counts.get("stale_match_count", 0),
        rematch_in_progress=counts.get("rematch_in_progress", False),
        active_rematch_batch_id=counts.get("active_rematch_batch_id"),
    )


async def _counts_for_job(org_id: str, job_id: str, jd_revision: int) -> dict:
    """Aggregate dashboard counts for a job."""
    db = get_db()
    base = {"org_id": org_id, "job_id": job_id}
    candidate_count = len(await db.match_results.distinct("candidate_id", base))
    needs_review_count = len(
        await db.match_results.distinct(
            "candidate_id", {**base, "review_status": "needs_review"}
        )
    )
    shortlisted_count = len(
        await db.match_results.distinct(
            "candidate_id", {**base, "shortlisted": True}
        )
    )
    rematch_status = await _rematch_status_for_job(org_id, job_id)
    stale_match_count = await _stale_match_count(org_id, job_id, jd_revision)
    return {
        "candidate_count": candidate_count,
        "needs_review_count": needs_review_count,
        "shortlisted_count": shortlisted_count,
        "stale_match_count": stale_match_count,
        **rematch_status,
    }


async def _create_rematch_batch(
    org_id: str,
    job_id: str,
    created_by: str,
    candidate_count: int,
) -> str:
    """Insert a rematch-only ingest batch used for progress tracking."""
    db = get_db()
    now = datetime.now(timezone.utc)
    doc = {
        "org_id": org_id,
        "job_id": job_id,
        "source": "rematch",
        "status": "processing",
        "meta": {"trigger": "manual"},
        "counters": {
            "total": candidate_count,
            "parsing": 0,
            "parsed": candidate_count,
            "matching": 0,
            "matched": 0,
            "failed": 0,
            "needs_review": 0,
        },
        "created_by": created_by,
        "created_at": now,
        "updated_at": now,
    }
    result = await db.ingest_batches.insert_one(doc)
    return str(result.inserted_id)


@router.get("", response_model=list[JobPublic])
async def list_jobs(user: UserPublic = Depends(get_current_user)) -> list[JobPublic]:
    """List jobs for the current org."""
    db = get_db()
    cursor = db.jobs.find({"org_id": user.org_id}).sort("updated_at", -1)
    jobs: list[JobPublic] = []
    async for doc in cursor:
        counts = await _counts_for_job(
            user.org_id,
            str(doc["_id"]),
            int(doc.get("jd_revision") or 1),
        )
        jobs.append(_job_public(doc, counts))
    return jobs


@router.post("", response_model=JobPublic, status_code=status.HTTP_201_CREATED)
async def create_job(body: JobCreate, user: UserPublic = Depends(get_current_user)) -> JobPublic:
    """Create a new job with JD schema."""
    db = get_db()
    now = datetime.now(timezone.utc)
    doc = {
        "org_id": user.org_id,
        "status": body.status,
        "jd": body.jd.model_dump(),
        "jd_schema_version": "jd.v1",
        "jd_revision": 1,
        "jd_hash": _jd_hash(body.jd.model_dump()),
        "created_by": user.id,
        "created_at": now,
        "updated_at": now,
    }
    result = await db.jobs.insert_one(doc)
    doc["_id"] = result.inserted_id
    await write_audit(user.org_id, user.id, "job.create", "job", str(result.inserted_id))
    counts = await _counts_for_job(user.org_id, str(result.inserted_id), 1)
    return _job_public(doc, counts)


@router.get("/{job_id}", response_model=JobPublic)
async def get_job(job_id: str, user: UserPublic = Depends(get_current_user)) -> JobPublic:
    """Fetch a single job."""
    db = get_db()
    doc = await db.jobs.find_one({"_id": ObjectId(job_id), "org_id": user.org_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Job not found")
    counts = await _counts_for_job(
        user.org_id,
        job_id,
        int(doc.get("jd_revision") or 1),
    )
    return _job_public(doc, counts)


@router.patch("/{job_id}", response_model=JobPublic)
async def update_job(
    job_id: str,
    body: JobUpdate,
    user: UserPublic = Depends(get_current_user),
) -> JobPublic:
    """Update JD and/or status."""
    db = get_db()
    doc = await db.jobs.find_one({"_id": ObjectId(job_id), "org_id": user.org_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Job not found")
    updates: dict = {"updated_at": datetime.now(timezone.utc)}
    if body.jd is not None:
        new_jd = body.jd.model_dump()
        if new_jd != doc.get("jd"):
            updates["jd"] = new_jd
            updates["jd_revision"] = int(doc.get("jd_revision") or 1) + 1
            updates["jd_hash"] = _jd_hash(new_jd)
    if body.status is not None:
        updates["status"] = body.status
    await db.jobs.update_one({"_id": ObjectId(job_id)}, {"$set": updates})
    doc.update(updates)
    await write_audit(user.org_id, user.id, "job.update", "job", job_id)
    if "jd_revision" in updates:
        await db.match_results.update_many(
            {"org_id": user.org_id, "job_id": job_id},
            {"$set": {"stale": True, "updated_at": datetime.now(timezone.utc)}},
        )
    counts = await _counts_for_job(
        user.org_id,
        job_id,
        int(doc.get("jd_revision") or 1),
    )
    return _job_public(doc, counts)


@router.post("/{job_id}/rematch", response_model=JobRematchResponse)
async def rematch_job(
    job_id: str,
    user: UserPublic = Depends(get_current_user),
) -> JobRematchResponse:
    """Manually rematch all parsed CVs against the current JD."""
    db = get_db()
    doc = await db.jobs.find_one({"_id": ObjectId(job_id), "org_id": user.org_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Job not found")

    rematch_status = await _rematch_status_for_job(user.org_id, job_id)
    if rematch_status["rematch_in_progress"]:
        raise HTTPException(status_code=409, detail="A rematch is already in progress for this job")

    jd_revision = int(doc.get("jd_revision") or 1)
    stale_match_count = await _stale_match_count(user.org_id, job_id, jd_revision)
    if stale_match_count <= 0:
        raise HTTPException(status_code=400, detail="No stale match results to rematch")

    resumes = await iter_latest_parsed_resumes(user.org_id, job_id)
    if not resumes:
        raise HTTPException(status_code=400, detail="No parsed CVs available to rematch")

    now = datetime.now(timezone.utc)
    await db.match_results.update_many(
        {"org_id": user.org_id, "job_id": job_id},
        {
            "$set": {
                "shortlisted": False,
                "shortlisted_at": None,
                "shortlisted_by": None,
                "review_status": "none",
                "review_notes": "",
                "reviewed_by": None,
                "reviewed_at": None,
                "updated_at": now,
            }
        },
    )

    batch_id = await _create_rematch_batch(
        user.org_id,
        job_id,
        user.id,
        len(resumes),
    )
    candidate_count = await enqueue_rematch_for_job(
        user.org_id,
        job_id,
        batch_id,
        user.id,
    )
    await write_audit(
        user.org_id,
        user.id,
        "job.rematch",
        "job",
        job_id,
        {"batch_id": batch_id, "candidate_count": candidate_count},
    )
    return JobRematchResponse(
        batch_id=batch_id,
        candidate_count=candidate_count,
        status="processing",
    )
