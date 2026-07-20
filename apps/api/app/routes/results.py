"""Results, shortlist, review, and candidate detail routes."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth import get_current_user
from app.db import get_db
from app.models.schemas import ReviewUpdate, ShortlistRequest, UserPublic
from app.services.audit import write_audit

router = APIRouter(tags=["results"])


def _mask_email(email: str) -> str:
    """Mask email for non-shortlisted views."""
    if "@" not in email:
        return "***"
    local, domain = email.split("@", 1)
    return (local[:1] + "***@" + domain) if local else "***@" + domain


def _mask_phone(phone: str) -> str:
    """Mask phone keeping last 3 digits."""
    digits = "".join(c for c in phone if c.isdigit())
    if len(digits) < 4:
        return "***"
    return "***" + digits[-3:]


async def _hydrate_row(db, org_id: str, mr: dict, reveal_contact: bool) -> dict[str, Any]:
    """Join match_result with candidate + resume summary fields."""
    cand = await db.candidates.find_one({"_id": ObjectId(mr["candidate_id"]), "org_id": org_id})
    resume = await db.resumes.find_one({"_id": ObjectId(mr["resume_id"]), "org_id": org_id})
    snapshot = (
        mr.get("identity_snapshot")
        or (resume or {}).get("parse", {}).get("identity")
        or cand
        or {}
    )
    emails = snapshot.get("emails", [])
    phones = snapshot.get("phones", [])
    shortlisted = bool(mr.get("shortlisted"))
    show = reveal_contact or shortlisted
    return {
        "id": str(mr["_id"]),
        "job_id": mr["job_id"],
        "resume_id": mr["resume_id"],
        "candidate_id": mr["candidate_id"],
        "batch_id": mr.get("batch_id"),
        "score": mr.get("score", 0),
        "hard_filters": mr.get("hard_filters", {}),
        "rank_signals": mr.get("rank_signals", {}),
        "explanation": mr.get("explanation", {}),
        "shortlisted": shortlisted,
        "review_status": mr.get("review_status", "none"),
        "matcher_version": mr.get("matcher_version"),
        "jd_revision": mr.get("jd_revision"),
        "parse_attempt_id": mr.get("parse_attempt_id"),
        "stale": bool(mr.get("stale")),
        "candidate": {
            "name": snapshot.get("name", ""),
            "emails": emails if show else [_mask_email(e) for e in emails],
            "phones": phones if show else [_mask_phone(p) for p in phones],
            "links": snapshot.get("links", []) if show else [],
            "contact_revealed": show,
        },
        "parse": {
            "status": (resume or {}).get("parse", {}).get("status"),
            "confidence": (resume or {}).get("parse", {}).get("confidence"),
            "needs_review": (resume or {}).get("parse", {}).get("needs_review"),
            "warnings": (resume or {}).get("parse", {}).get("warnings", []),
        },
        "skills": (
            (((resume or {}).get("parse") or {}).get("resume") or {}).get("skills") or []
        ),
        "created_at": mr.get("created_at"),
        "updated_at": mr.get("updated_at"),
    }


@router.get("/v1/jobs/{job_id}/results")
async def list_results(
    job_id: str,
    user: UserPublic = Depends(get_current_user),
    view: str = Query("best_fit", pattern="^(best_fit|shortlisted|needs_review|failed_filters|all)$"),
    min_score: float | None = None,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
) -> dict[str, Any]:
    """Ranked match results for the dashboard."""
    db = get_db()
    job = await db.jobs.find_one({"_id": ObjectId(job_id), "org_id": user.org_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    view_query: dict[str, Any] = {}
    if view == "shortlisted":
        view_query["shortlisted"] = True
    elif view == "needs_review":
        view_query["review_status"] = "needs_review"
    elif view == "failed_filters":
        view_query["hard_filters.passed"] = False
        view_query["hard_filters.unknown"] = {"$ne": True}
    elif view == "best_fit":
        view_query["hard_filters.passed"] = True

    if min_score is not None:
        view_query["score"] = {"$gte": min_score}

    base_pipeline: list[dict[str, Any]] = [
        {"$match": {"org_id": user.org_id, "job_id": job_id}},
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
    if view_query:
        base_pipeline.append({"$match": view_query})
    total_rows = await db.match_results.aggregate(
        [*base_pipeline, {"$count": "total"}]
    ).to_list(length=1)
    total = int(total_rows[0]["total"]) if total_rows else 0
    pipeline = [
        *base_pipeline,
        {"$sort": {"score": -1, "updated_at": -1, "_id": 1}},
        {"$skip": offset},
        {"$limit": limit},
    ]
    rows: list[dict[str, Any]] = []
    async for mr in db.match_results.aggregate(pipeline):
        mr["stale"] = int(mr.get("jd_revision") or 0) != int(job.get("jd_revision") or 1)
        rows.append(await _hydrate_row(db, user.org_id, mr, reveal_contact=False))
    return {"items": rows, "total": total, "limit": limit, "offset": offset}


async def _get_result_detail(result_id: str, user: UserPublic, job_id: str | None = None) -> dict[str, Any]:
    """Build candidate/match detail with optional job binding."""
    db = get_db()
    query: dict[str, Any] = {"_id": ObjectId(result_id), "org_id": user.org_id}
    if job_id is not None:
        query["job_id"] = job_id
    mr = await db.match_results.find_one(query)
    if not mr:
        raise HTTPException(status_code=404, detail="Result not found")
    row = await _hydrate_row(db, user.org_id, mr, reveal_contact=bool(mr.get("shortlisted")))
    resume = await db.resumes.find_one(
        {"_id": ObjectId(mr["resume_id"]), "org_id": user.org_id}
    )
    row["resume"] = (resume or {}).get("parse", {}).get("resume")
    row["raw_resume_text"] = ((resume or {}).get("parse", {}).get("resume") or {}).get("raw_resume_text", "")
    row["source_ref"] = (resume or {}).get("source_ref") or {}
    row["parse_meta"] = {
        "status": (resume or {}).get("parse", {}).get("status"),
        "confidence": (resume or {}).get("parse", {}).get("confidence"),
        "warnings": (resume or {}).get("parse", {}).get("warnings", []),
        "provenance": (resume or {}).get("parse", {}).get("provenance", {}),
    }
    return row


@router.get("/v1/jobs/{job_id}/match-results/{result_id}")
async def get_job_result(
    job_id: str,
    result_id: str,
    user: UserPublic = Depends(get_current_user),
) -> dict[str, Any]:
    """Return a result only when it belongs to the requested job."""
    return await _get_result_detail(result_id, user, job_id)


@router.get("/v1/match-results/{result_id}")
async def get_result(result_id: str, user: UserPublic = Depends(get_current_user)) -> dict[str, Any]:
    """Backwards-compatible organization-scoped result detail."""
    return await _get_result_detail(result_id, user)


@router.get("/v1/resumes/{resume_id}/file")
async def download_resume_file(resume_id: str, user: UserPublic = Depends(get_current_user)):
    """Stream original CV bytes for in-app preview / download."""
    from fastapi.responses import Response

    from app.services.storage import download_bytes

    db = get_db()
    resume = await db.resumes.find_one({"_id": ObjectId(resume_id), "org_id": user.org_id})
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    ref = resume.get("source_ref") or {}
    key = ref.get("storage_key")
    if not key:
        raise HTTPException(status_code=404, detail="File not stored")
    try:
        data = download_bytes(key)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=f"File missing in storage: {exc}") from exc
    filename = ref.get("original_filename") or "resume.pdf"
    content_type = ref.get("content_type") or "application/pdf"
    # Force PDF content-type for browser iframe preview when extension is pdf
    if filename.lower().endswith(".pdf"):
        content_type = "application/pdf"
    return Response(
        content=data,
        media_type=content_type,
        headers={
            "Content-Disposition": f'inline; filename="{filename}"',
            "Cache-Control": "private, max-age=60",
        },
    )


@router.post("/v1/match-results/{result_id}/shortlist")
async def toggle_shortlist(
    result_id: str,
    body: ShortlistRequest,
    user: UserPublic = Depends(get_current_user),
) -> dict[str, Any]:
    """Shortlist or unshortlist a match result."""
    db = get_db()
    mr = await db.match_results.find_one({"_id": ObjectId(result_id), "org_id": user.org_id})
    if not mr:
        raise HTTPException(status_code=404, detail="Result not found")
    now = datetime.now(timezone.utc)
    updates = {
        "shortlisted": body.shortlisted,
        "shortlisted_at": now if body.shortlisted else None,
        "shortlisted_by": user.id if body.shortlisted else None,
        "updated_at": now,
    }
    await db.match_results.update_one({"_id": ObjectId(result_id)}, {"$set": updates})
    await write_audit(
        user.org_id,
        user.id,
        "shortlist.set",
        "match_result",
        result_id,
        {"shortlisted": body.shortlisted},
    )
    mr.update(updates)
    return await _hydrate_row(db, user.org_id, mr, reveal_contact=body.shortlisted)


@router.get("/v1/jobs/{job_id}/shortlist")
async def shortlist_contacts(job_id: str, user: UserPublic = Depends(get_current_user)) -> list[dict[str, Any]]:
    """Full contact roster for shortlisted candidates."""
    db = get_db()
    cursor = db.match_results.find(
        {"org_id": user.org_id, "job_id": job_id, "shortlisted": True}
    ).sort("score", -1)
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    async for mr in cursor:
        candidate_id = str(mr.get("candidate_id") or "")
        if candidate_id in seen:
            continue
        seen.add(candidate_id)
        rows.append(await _hydrate_row(db, user.org_id, mr, reveal_contact=True))
    return rows


@router.get("/v1/jobs/{job_id}/review-queue")
async def review_queue(job_id: str, user: UserPublic = Depends(get_current_user)) -> list[dict[str, Any]]:
    """Low-confidence / needs-review candidates."""
    db = get_db()
    cursor = db.match_results.find(
        {"org_id": user.org_id, "job_id": job_id, "review_status": "needs_review"}
    ).sort("score", -1)
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    async for mr in cursor:
        candidate_id = str(mr.get("candidate_id") or "")
        if candidate_id in seen:
            continue
        seen.add(candidate_id)
        rows.append(await _hydrate_row(db, user.org_id, mr, reveal_contact=False))
    return rows


@router.patch("/v1/match-results/{result_id}/review")
async def update_review(
    result_id: str,
    body: ReviewUpdate,
    user: UserPublic = Depends(get_current_user),
) -> dict[str, Any]:
    """Approve or reject after manual review."""
    db = get_db()
    mr = await db.match_results.find_one({"_id": ObjectId(result_id), "org_id": user.org_id})
    if not mr:
        raise HTTPException(status_code=404, detail="Result not found")
    now = datetime.now(timezone.utc)
    await db.match_results.update_one(
        {"_id": ObjectId(result_id)},
        {
            "$set": {
                "review_status": body.review_status,
                "review_notes": body.notes,
                "reviewed_by": user.id,
                "reviewed_at": now,
                "updated_at": now,
            }
        },
    )
    await write_audit(
        user.org_id,
        user.id,
        "review.update",
        "match_result",
        result_id,
        {"review_status": body.review_status},
    )
    mr["review_status"] = body.review_status
    return await _hydrate_row(db, user.org_id, mr, reveal_contact=bool(mr.get("shortlisted")))
