"""Job description CRUD routes."""

from __future__ import annotations

from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import get_current_user
from app.db import get_db
from app.models.schemas import JobCreate, JobPublic, JobUpdate, UserPublic
from app.services.audit import write_audit

router = APIRouter(prefix="/v1/jobs", tags=["jobs"])


def _job_public(doc: dict, counts: dict | None = None) -> JobPublic:
    """Map a Mongo job document to the public schema."""
    counts = counts or {}
    return JobPublic(
        id=str(doc["_id"]),
        org_id=doc["org_id"],
        status=doc["status"],
        jd=doc["jd"],
        jd_schema_version=doc.get("jd_schema_version", "jd.v1"),
        created_by=doc.get("created_by"),
        created_at=doc["created_at"],
        updated_at=doc["updated_at"],
        candidate_count=counts.get("candidate_count", 0),
        needs_review_count=counts.get("needs_review_count", 0),
        shortlisted_count=counts.get("shortlisted_count", 0),
    )


async def _counts_for_job(org_id: str, job_id: str) -> dict:
    """Aggregate dashboard counts for a job."""
    db = get_db()
    candidate_count = await db.match_results.count_documents({"org_id": org_id, "job_id": job_id})
    needs_review_count = await db.match_results.count_documents(
        {"org_id": org_id, "job_id": job_id, "review_status": "needs_review"}
    )
    shortlisted_count = await db.match_results.count_documents(
        {"org_id": org_id, "job_id": job_id, "shortlisted": True}
    )
    return {
        "candidate_count": candidate_count,
        "needs_review_count": needs_review_count,
        "shortlisted_count": shortlisted_count,
    }


@router.get("", response_model=list[JobPublic])
async def list_jobs(user: UserPublic = Depends(get_current_user)) -> list[JobPublic]:
    """List jobs for the current org."""
    db = get_db()
    cursor = db.jobs.find({"org_id": user.org_id}).sort("updated_at", -1)
    jobs: list[JobPublic] = []
    async for doc in cursor:
        counts = await _counts_for_job(user.org_id, str(doc["_id"]))
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
        "created_by": user.id,
        "created_at": now,
        "updated_at": now,
    }
    result = await db.jobs.insert_one(doc)
    doc["_id"] = result.inserted_id
    await write_audit(user.org_id, user.id, "job.create", "job", str(result.inserted_id))
    return _job_public(doc)


@router.get("/{job_id}", response_model=JobPublic)
async def get_job(job_id: str, user: UserPublic = Depends(get_current_user)) -> JobPublic:
    """Fetch a single job."""
    db = get_db()
    doc = await db.jobs.find_one({"_id": ObjectId(job_id), "org_id": user.org_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Job not found")
    counts = await _counts_for_job(user.org_id, job_id)
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
        updates["jd"] = body.jd.model_dump()
    if body.status is not None:
        updates["status"] = body.status
    await db.jobs.update_one({"_id": ObjectId(job_id)}, {"$set": updates})
    doc.update(updates)
    await write_audit(user.org_id, user.id, "job.update", "job", job_id)
    counts = await _counts_for_job(user.org_id, job_id)
    return _job_public(doc, counts)
