"""Cascade deletion helpers for jobs, candidates, and CVs."""

from __future__ import annotations

import asyncio
from typing import Any

from bson import ObjectId

from app.services.storage import delete_bytes


async def _delete_stored_file(storage_key: str | None) -> None:
    """Delete a GridFS file without blocking the FastAPI event loop."""
    if not storage_key:
        return
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, delete_bytes, storage_key)


async def _cleanup_candidate_if_orphaned(db: Any, org_id: str, candidate_id: str) -> None:
    """Delete a candidate only when no resume or match result still references it."""
    has_resume = await db.resumes.find_one(
        {"org_id": org_id, "candidate_id": candidate_id},
        {"_id": 1},
    )
    has_result = await db.match_results.find_one(
        {"org_id": org_id, "candidate_id": candidate_id},
        {"_id": 1},
    )
    if has_resume or has_result:
        return

    candidate_oid = ObjectId(candidate_id)
    await db.screening_calls.delete_many(
        {
            "org_id": org_id,
            "candidate_id": {"$in": [candidate_id, candidate_oid]},
        }
    )
    await db.candidates.delete_one({"_id": candidate_oid, "org_id": org_id})


async def delete_resume(db: Any, org_id: str, resume: dict[str, Any]) -> dict[str, int]:
    """Delete one CV, its match rows, stored file, and an orphaned candidate."""
    resume_id = str(resume["_id"])
    candidate_id = str(resume.get("candidate_id") or "")
    job_id = str(resume.get("job_id") or "")
    source_ref = resume.get("source_ref") or {}
    await _delete_stored_file(source_ref.get("storage_key"))

    result = await db.match_results.delete_many(
        {"org_id": org_id, "resume_id": resume_id}
    )
    deleted = await db.resumes.delete_one({"_id": resume["_id"], "org_id": org_id})

    if candidate_id:
        has_job_resume = await db.resumes.find_one(
            {"org_id": org_id, "job_id": job_id, "candidate_id": candidate_id},
            {"_id": 1},
        )
        has_job_result = await db.match_results.find_one(
            {"org_id": org_id, "job_id": job_id, "candidate_id": candidate_id},
            {"_id": 1},
        )
        if not has_job_resume and not has_job_result:
            await db.candidates.update_one(
                {"_id": ObjectId(candidate_id), "org_id": org_id},
                {"$pull": {"job_ids": job_id}},
            )
        await _cleanup_candidate_if_orphaned(db, org_id, candidate_id)

    return {
        "resumes": int(deleted.deleted_count),
        "match_results": int(result.deleted_count),
    }


async def delete_candidate_from_job(
    db: Any,
    org_id: str,
    job_id: str,
    candidate_id: str,
) -> dict[str, int]:
    """Delete a candidate's CVs and results for one job, preserving other jobs."""
    resumes = await db.resumes.find(
        {"org_id": org_id, "job_id": job_id, "candidate_id": candidate_id}
    ).to_list(length=None)
    for resume in resumes:
        source_ref = resume.get("source_ref") or {}
        await _delete_stored_file(source_ref.get("storage_key"))

    resume_ids = [str(resume["_id"]) for resume in resumes]
    match_query: dict[str, Any] = {
        "org_id": org_id,
        "job_id": job_id,
        "candidate_id": candidate_id,
    }
    if resume_ids:
        match_query = {
            "org_id": org_id,
            "job_id": job_id,
            "$or": [
                {"candidate_id": candidate_id},
                {"resume_id": {"$in": resume_ids}},
            ],
        }
    result = await db.match_results.delete_many(match_query)
    deleted = await db.resumes.delete_many(
        {"org_id": org_id, "job_id": job_id, "candidate_id": candidate_id}
    )
    await db.candidates.update_one(
        {"_id": ObjectId(candidate_id), "org_id": org_id},
        {"$pull": {"job_ids": job_id}},
    )
    await _cleanup_candidate_if_orphaned(db, org_id, candidate_id)
    return {
        "resumes": int(deleted.deleted_count),
        "match_results": int(result.deleted_count),
    }


async def delete_job(db: Any, org_id: str, job_id: str) -> dict[str, int]:
    """Delete a job and all job-scoped CV, result, batch, and file data."""
    resumes = await db.resumes.find(
        {"org_id": org_id, "job_id": job_id}
    ).to_list(length=None)
    for resume in resumes:
        source_ref = resume.get("source_ref") or {}
        await _delete_stored_file(source_ref.get("storage_key"))

    resume_candidate_ids = {
        str(resume["candidate_id"])
        for resume in resumes
        if resume.get("candidate_id")
    }
    result_candidate_ids = {
        str(value)
        for value in await db.match_results.distinct(
            "candidate_id",
            {"org_id": org_id, "job_id": job_id},
        )
        if value
    }
    candidate_ids = resume_candidate_ids | result_candidate_ids

    match_result = await db.match_results.delete_many(
        {"org_id": org_id, "job_id": job_id}
    )
    resume_result = await db.resumes.delete_many(
        {"org_id": org_id, "job_id": job_id}
    )
    batch_result = await db.ingest_batches.delete_many(
        {"org_id": org_id, "job_id": job_id}
    )
    job_result = await db.jobs.delete_one(
        {"_id": ObjectId(job_id), "org_id": org_id}
    )

    for candidate_id in candidate_ids:
        await db.candidates.update_one(
            {"_id": ObjectId(candidate_id), "org_id": org_id},
            {"$pull": {"job_ids": job_id}},
        )
        await _cleanup_candidate_if_orphaned(db, org_id, candidate_id)

    return {
        "jobs": int(job_result.deleted_count),
        "resumes": int(resume_result.deleted_count),
        "match_results": int(match_result.deleted_count),
        "ingest_batches": int(batch_result.deleted_count),
    }
