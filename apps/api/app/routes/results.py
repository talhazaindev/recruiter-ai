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
    emails = (cand or {}).get("emails", [])
    phones = (cand or {}).get("phones", [])
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
        "candidate": {
            "name": (cand or {}).get("name", ""),
            "emails": emails if show else [_mask_email(e) for e in emails],
            "phones": phones if show else [_mask_phone(p) for p in phones],
            "links": (cand or {}).get("links", []) if show else [],
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
) -> list[dict[str, Any]]:
    """Ranked match results for the dashboard."""
    db = get_db()
    job = await db.jobs.find_one({"_id": ObjectId(job_id), "org_id": user.org_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    query: dict[str, Any] = {"org_id": user.org_id, "job_id": job_id}
    if view == "shortlisted":
        query["shortlisted"] = True
    elif view == "needs_review":
        query["review_status"] = "needs_review"
    elif view == "failed_filters":
        query["hard_filters.passed"] = False
    elif view == "best_fit":
        query["hard_filters.passed"] = True

    if min_score is not None:
        query["score"] = {"$gte": min_score}

    cursor = db.match_results.find(query).sort("score", -1).limit(limit)
    rows: list[dict[str, Any]] = []
    async for mr in cursor:
        rows.append(await _hydrate_row(db, user.org_id, mr, reveal_contact=False))
    return rows


@router.get("/v1/match-results/{result_id}")
async def get_result(result_id: str, user: UserPublic = Depends(get_current_user)) -> dict[str, Any]:
    """Candidate/match detail including structured resume when available."""
    db = get_db()
    mr = await db.match_results.find_one({"_id": ObjectId(result_id), "org_id": user.org_id})
    if not mr:
        raise HTTPException(status_code=404, detail="Result not found")
    row = await _hydrate_row(db, user.org_id, mr, reveal_contact=bool(mr.get("shortlisted")))
    resume = await db.resumes.find_one({"_id": ObjectId(mr["resume_id"])})
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
    async for mr in cursor:
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
    async for mr in cursor:
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
