"""Shared pipeline logic used by workers and optional in-process fallback."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from bson import ObjectId

from app.config import get_settings
from app.db import get_db
from app.models.schemas import JobDescriptionSchema, MatchingResumeSchema
from app.queue import QUEUE_MATCH, QUEUE_PARSE, enqueue
from app.services.matcher_adapter import match_jd_resume
from app.services.parser_adapter import parse_resume_bytes
from app.services.storage import download_bytes
from time import perf_counter
from docling.document_converter import DocumentConverter


logger = logging.getLogger(__name__)


async def process_parse_task(payload: dict[str, Any],converter: DocumentConverter) -> None:
    """Parse one resume file and enqueue matching."""
    overall_start = perf_counter()
    logger.info("========== PROCESS PARSE TASK START [%s] ==========")

    db = get_db()
    settings = get_settings()
    resume_id = payload["resume_id"]
    org_id = payload["org_id"]
    job_id = payload["job_id"]
    batch_id = payload["batch_id"]

    t = perf_counter()

    resume_doc = await db.resumes.find_one({"_id": ObjectId(resume_id), "org_id": org_id})
    logger.info("======Mongo resumes.find_one: %.3fs", perf_counter() - t)
    if not resume_doc:
        logger.error("Resume %s not found", resume_id)
        return
    temp_job=await db.jobs.find_one({"_id": ObjectId(job_id)},
        {"minimum_relevant_years": 1}
)
    min_experience=temp_job.get("minimum_relevant_years", 0) or 0
    t = perf_counter()

    await db.resumes.update_one(
        {"_id": ObjectId(resume_id)},
        {"$set": {"parse.status": "running", "updated_at": datetime.now(timezone.utc)}},
    )
    logger.info("======Mongo resumes.update_one (running): %.3fs", perf_counter() - t)
    t = perf_counter()

    await db.ingest_batches.update_one(
        {"_id": ObjectId(batch_id)},
        {"$inc": {"counters.parsing": 1}},
    )
    logger.info("======Mongo ingest_batches.update_one (+parsing): %.3fs", perf_counter() - t)
    try:
        storage_key = resume_doc["source_ref"]["storage_key"]
        t = perf_counter()

        data = download_bytes(storage_key)
        logger.info("======MinIO download: %.3fs", perf_counter() - t)
        filename = resume_doc["source_ref"].get("original_filename", "resume.pdf")
        content_type = resume_doc["source_ref"].get("content_type", "application/pdf")
        t = perf_counter()

        result = parse_resume_bytes(data, filename, content_type,min_experience,converter)
        logger.info("======Resume Parser TOTAL: %.3fs", perf_counter() - t)
        candidate = result.candidate
        cand_doc = {
            "org_id": org_id,
            "name": candidate.name,
            "emails": candidate.emails,
            "phones": candidate.phones,
            "links": candidate.links,
            "job_ids": [job_id],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        # Dedupe loosely by first email within org
        existing = None
        if candidate.emails:
            t = perf_counter()

            #existing = await db.candidates.find_one({"org_id": org_id, "emails": candidate.emails[0]},{})
            existing = await db.candidates.find_one({
                        "org_id": org_id,
                        "$or": [
                                {"emails": candidate.emails[0]},
                                {"phones": candidate.phones[0]}
                                ]
                        })
            logger.info("======Mongo candidates.find_one: %.3fs", perf_counter() - t)
        if existing:
            candidate_id = existing["_id"]
            t = perf_counter()

            await db.candidates.update_one(
                {"_id": candidate_id},
                {
                    "$addToSet": {"job_ids": job_id},
                    "$set": {
                        "name": candidate.name or existing.get("name", ""),
                        "phones": candidate.phones or existing.get("phones", []),
                        "links": candidate.links or existing.get("links", []),
                        "updated_at": datetime.now(timezone.utc),
                    },
                },
            )
            logger.info("======Mongo candidates.update_one: %.3fs", perf_counter() - t)
        else:
            t = perf_counter()

            ins = await db.candidates.insert_one(cand_doc)
            logger.info("======Mongo candidates.insert_one: %.3fs", perf_counter() - t)
            candidate_id = ins.inserted_id

        needs_review = result.needs_review or result.confidence < settings.parse_confidence_review_threshold
        t = perf_counter()

        need_to_update=True
        if existing:
            
            existing_resume = await db.resumes.find_one(
                {
                    "candidate_id": str(candidate_id),
                     "job_id": job_id,
                 },
                 {"_id": 1},)
            if existing_resume:
                result.status='failed'
            
                logger.info("cv already exist")
                await db.resumes.delete_one(
                    {"_id": ObjectId(resume_id)})
            else:
                await db.resumes.update_one(
                {"_id": ObjectId(resume_id)},
                {
                    "$set": {
                        "candidate_id": str(candidate_id),
                        "parse": {
                            "status": result.status,
                            "schema_version": result.schema_version,
                            "resume": result.resume.model_dump() if result.resume else None,
                            "confidence": result.confidence,
                            "field_confidence": result.field_confidence,
                            "needs_review": needs_review,
                            "warnings": result.warnings,
                            "provenance": result.provenance,
                        },
                        "updated_at": datetime.now(timezone.utc),
                    }
                },
            )
        else:
            await db.resumes.update_one(
                {"_id": ObjectId(resume_id)},
                {
                    "$set": {
                        "candidate_id": str(candidate_id),
                        "parse": {
                            "status": result.status,
                            "schema_version": result.schema_version,
                            "resume": result.resume.model_dump() if result.resume else None,
                            "confidence": result.confidence,
                            "field_confidence": result.field_confidence,
                            "needs_review": needs_review,
                            "warnings": result.warnings,
                            "provenance": result.provenance,
                        },
                        "updated_at": datetime.now(timezone.utc),
                    }
                },
            )
            logger.info("======Mongo resumes.update_one (parsed): %.3fs", perf_counter() - t)
            t = perf_counter()

        await db.ingest_batches.update_one(
            {"_id": ObjectId(batch_id)},
            {
                "$inc": {
                    "counters.parsing": -1,
                    "counters.parsed": 1,
                    "counters.needs_review": 1 if needs_review else 0,
                    "counters.failed": 1 if result.status == "failed" else 0,
                },
                "$set": {"updated_at": datetime.now(timezone.utc)},
            },
        )
        logger.info("======Mongo ingest_batches.update_one (parsed): %.3fs", perf_counter() - t)

        if result.resume and result.status != "failed":
            t = perf_counter()

            enqueue(
                QUEUE_MATCH,
                {
                    "resume_id": resume_id,
                    "candidate_id": str(candidate_id),
                    "job_id": job_id,
                    "batch_id": batch_id,
                    "org_id": org_id,
                    "needs_review": needs_review,
                },
            )
            logger.info("======Redis enqueue match: %.3fs", perf_counter() - t)
        else:

            await _maybe_finish_batch(batch_id)
    except Exception as exc:
        logger.exception("Parse failed for %s", resume_id)
        await db.resumes.update_one(
            {"_id": ObjectId(resume_id)},
            {
                "$set": {
                    "parse.status": "failed",
                    "parse.warnings": [str(exc)],
                    "parse.needs_review": True,
                    "updated_at": datetime.now(timezone.utc),
                }
            },
        )
        await db.ingest_batches.update_one(
            {"_id": ObjectId(batch_id)},
            {
                "$inc": {"counters.parsing": -1, "counters.failed": 1, "counters.parsed": 1},
                "$set": {"updated_at": datetime.now(timezone.utc)},
            },
        )
        await _maybe_finish_batch(batch_id)
        
    logger.info(
    "========== PROCESS PARSE TASK END [%s] (%.3fs) ==========",
    resume_id,
    perf_counter() - overall_start,
)


async def process_match_task(payload: dict[str, Any]) -> None:
    """Match one parsed resume against its JD."""
    db = get_db()
    resume_id = payload["resume_id"]
    org_id = payload["org_id"]
    job_id = payload["job_id"]
    batch_id = payload["batch_id"]
    candidate_id = payload["candidate_id"]
    needs_review = payload.get("needs_review", False)

    job = await db.jobs.find_one({"_id": ObjectId(job_id), "org_id": org_id})
    resume_doc = await db.resumes.find_one({"_id": ObjectId(resume_id), "org_id": org_id})
    if not job or not resume_doc or not resume_doc.get("parse", {}).get("resume"):
        logger.error("Missing job/resume for match %s", resume_id)
        return

    await db.ingest_batches.update_one(
        {"_id": ObjectId(batch_id)},
        {"$inc": {"counters.matching": 1}},
    )

    try:
        jd = JobDescriptionSchema.model_validate(job["jd"])
        resume = MatchingResumeSchema.model_validate(resume_doc["parse"]["resume"])
        output = match_jd_resume(jd, resume)

        review_status = "needs_review" if needs_review else "none"
        now = datetime.now(timezone.utc)
        doc = {
            "org_id": org_id,
            "job_id": job_id,
            "resume_id": resume_id,
            "candidate_id": candidate_id,
            "batch_id": batch_id,
            "matcher_version": output.matcher_version,
            "hard_filters": output.hard_filters.model_dump(),
            "score": output.score,
            "rank_signals": output.rank_signals,
            "explanation": output.explanation,
            "shortlisted": False,
            "shortlisted_at": None,
            "shortlisted_by": None,
            "review_status": review_status,
            "created_at": now,
            "updated_at": now,
        }
        await db.match_results.update_one(
            {"org_id": org_id, "job_id": job_id, "resume_id": resume_id},
            {"$set": doc},
            upsert=True,
        )
        await db.ingest_batches.update_one(
            {"_id": ObjectId(batch_id)},
            {
                "$inc": {"counters.matching": -1, "counters.matched": 1},
                "$set": {"updated_at": now},
            },
        )
    except Exception as exc:
        logger.exception("Match failed for %s", resume_id)
        await db.ingest_batches.update_one(
            {"_id": ObjectId(batch_id)},
            {
                "$inc": {"counters.matching": -1, "counters.failed": 1},
                "$set": {"updated_at": datetime.now(timezone.utc), "last_error": str(exc)},
            },
        )
    finally:
        await _maybe_finish_batch(batch_id)


async def _maybe_finish_batch(batch_id: str) -> None:
    """Mark batch completed when all files are processed."""
    db = get_db()
    batch = await db.ingest_batches.find_one({"_id": ObjectId(batch_id)})
    if not batch:
        return
    c = batch.get("counters", {})
    total = c.get("total", 0)
    done = c.get("parsed", 0)
    matching = c.get("matching", 0)
    parsing = c.get("parsing", 0)
    matched = c.get("matched", 0)
    if total > 0 and done >= total and parsing <= 0 and matching <= 0 and matched >= (total - c.get("failed", 0)):
        # Soft complete: parsed all and no workers in flight
        status = "completed"
        if c.get("failed", 0) == total:
            status = "failed"
        elif c.get("failed", 0) > 0:
            status = "completed_with_errors"
        await db.ingest_batches.update_one(
            {"_id": ObjectId(batch_id)},
            {"$set": {"status": status, "updated_at": datetime.now(timezone.utc)}},
        )
    elif total > 0 and done >= total and parsing <= 0 and matching <= 0:
        await db.ingest_batches.update_one(
            {"_id": ObjectId(batch_id)},
            {"$set": {"status": "completed", "updated_at": datetime.now(timezone.utc)}},
        )


def enqueue_parse_for_batch_files(batch_id: str, org_id: str, job_id: str, resume_ids: list[str]) -> None:
    """Enqueue parse tasks for newly ingested resumes."""
    for rid in resume_ids:
        enqueue(
            QUEUE_PARSE,
            {"resume_id": rid, "org_id": org_id, "job_id": job_id, "batch_id": batch_id},
        )
