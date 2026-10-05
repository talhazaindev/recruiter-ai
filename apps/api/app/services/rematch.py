"""Manual JD rematch helpers (match-only, no re-parse)."""

from __future__ import annotations

from typing import Any

from app.db import get_db
from app.queue import QUEUE_MATCH, enqueue


async def iter_latest_parsed_resumes(org_id: str, job_id: str) -> list[dict[str, Any]]:
    """Return the newest parsed resume document per candidate for a job."""
    db = get_db()
    cursor = db.resumes.aggregate(
        [
            {
                "$match": {
                    "org_id": org_id,
                    "job_id": job_id,
                    "candidate_id": {"$type": "string"},
                    "parse.resume": {"$ne": None},
                    "parse.status": {"$ne": "failed"},
                }
            },
            {"$sort": {"updated_at": -1}},
            {"$group": {"_id": "$candidate_id", "resume": {"$first": "$$ROOT"}}},
        ]
    )
    return [item["resume"] async for item in cursor]


async def enqueue_rematch_for_job(
    org_id: str,
    job_id: str,
    batch_id: str,
    created_by: str,
) -> int:
    """Enqueue match-only tasks for every parsed CV on a job."""
    resumes = await iter_latest_parsed_resumes(org_id, job_id)
    for resume in resumes:
        enqueue(
            QUEUE_MATCH,
            {
                "resume_id": str(resume["_id"]),
                "candidate_id": resume["candidate_id"],
                "job_id": job_id,
                "batch_id": batch_id,
                "org_id": org_id,
                "needs_review": resume.get("parse", {}).get("needs_review", False),
                "rematch": True,
            },
        )
    return len(resumes)
