"""Shared pipeline logic used by workers and optional in-process fallback."""

from __future__ import annotations

import logging
import re
import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from app.config import get_settings
from app.db import get_db
from app.models.schemas import JobDescriptionSchema, MatchingResumeSchema
from app.queue import QUEUE_MATCH, QUEUE_PARSE, enqueue
from app.services.matcher_adapter import match_jd_resume
from app.services.parser_adapter import parse_resume_bytes
from app.services.storage import download_bytes
from time import perf_counter


logger = logging.getLogger(__name__)


def _normalize_emails(values: list[str]) -> list[str]:
    """Normalize and deduplicate candidate email addresses."""
    return list(dict.fromkeys(value.strip().lower() for value in values if "@" in value))


def _normalize_phones(values: list[str]) -> list[str]:
    """Normalize and deduplicate candidate phone numbers."""
    normalized: list[str] = []
    for value in values:
        digits = re.sub(r"\D", "", value)
        if len(digits) >= 10:
            normalized.append(digits[-10:])
    return list(dict.fromkeys(normalized))


async def _resolve_candidate(
    org_id: str,
    job_id: str,
    candidate: Any,
    confidence: float,
    warnings: list[str],
) -> tuple[ObjectId, dict[str, Any]]:
    """Atomically resolve a canonical candidate and return its identity snapshot."""
    db = get_db()
    now = datetime.now(timezone.utc)
    emails = _normalize_emails(candidate.emails)
    phones = _normalize_phones(candidate.phones)
    identity_valid = "candidate_name_invalid_or_missing" not in warnings
    snapshot = {
        "name": candidate.name,
        "emails": emails,
        "phones": phones,
        "links": list(dict.fromkeys(candidate.links)),
        "quality": confidence if identity_valid else min(confidence, 0.4),
        "valid_name": identity_valid,
        "warnings": warnings,
    }
    clauses: list[dict[str, Any]] = []
    if emails:
        clauses.extend(
            [
                {"primary_email_normalized": emails[0]},
                {"emails": {"$in": emails}},
            ]
        )
    if phones:
        clauses.append({"phones_normalized": {"$in": phones}})
    existing = (
        await db.candidates.find_one({"org_id": org_id, "$or": clauses})
        if clauses
        else None
    )
    if existing:
        updates: dict[str, Any] = {
            "emails": list(dict.fromkeys([*(existing.get("emails") or []), *emails])),
            "phones_normalized": list(
                dict.fromkeys([*(existing.get("phones_normalized") or []), *phones])
            ),
            "updated_at": now,
        }
        if emails and not existing.get("primary_email_normalized"):
            updates["primary_email_normalized"] = emails[0]
        if snapshot["quality"] > float(existing.get("identity_quality") or 0):
            updates.update(
                {
                    "name": candidate.name if snapshot["valid_name"] else existing.get("name", ""),
                    "phones": candidate.phones if snapshot["valid_name"] else existing.get("phones", []),
                    "links": candidate.links if snapshot["valid_name"] else existing.get("links", []),
                    "identity_quality": snapshot["quality"],
                }
            )
        await db.candidates.update_one(
            {"_id": existing["_id"]},
            {"$addToSet": {"job_ids": job_id}, "$set": updates},
        )
        return existing["_id"], snapshot

    document = {
        "org_id": org_id,
        "name": candidate.name,
        "emails": emails,
        "primary_email_normalized": emails[0] if emails else None,
        "phones": candidate.phones,
        "phones_normalized": phones,
        "links": candidate.links,
        "identity_quality": snapshot["quality"],
        "job_ids": [job_id],
        "created_at": now,
        "updated_at": now,
    }
    try:
        inserted = await db.candidates.insert_one(document)
        return inserted.inserted_id, snapshot
    except DuplicateKeyError:
        existing = await db.candidates.find_one(
            {"org_id": org_id, "primary_email_normalized": emails[0]}
        )
        if not existing:
            raise
        await db.candidates.update_one(
            {"_id": existing["_id"]},
            {"$addToSet": {"job_ids": job_id}, "$set": {"updated_at": now}},
        )
        return existing["_id"], snapshot


async def process_parse_task(payload: dict[str, Any]) -> None:
    """Parse one resume file and enqueue matching."""
    overall_start = perf_counter()
    logger.info("========== PROCESS PARSE TASK START [%s] ==========")

    db = get_db()
    settings = get_settings()
    resume_id = payload["resume_id"]
    org_id = payload["org_id"]
    job_id = payload["job_id"]
    batch_id = payload["batch_id"]
    reparse = bool(payload.get("reparse"))

    t = perf_counter()

    resume_doc = await db.resumes.find_one({"_id": ObjectId(resume_id), "org_id": org_id})
    logger.info("======Mongo resumes.find_one: %.3fs", perf_counter() - t)
    if not resume_doc:
        logger.error("Resume %s not found", resume_id)
        return

    t = perf_counter()

    await db.resumes.update_one(
        {"_id": ObjectId(resume_id)},
        {"$set": {"parse.status": "running", "updated_at": datetime.now(timezone.utc)}},
    )
    logger.info("======Mongo resumes.update_one (running): %.3fs", perf_counter() - t)
    t = perf_counter()

    if not reparse:
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

        result = parse_resume_bytes(data, filename, content_type)
        logger.info("======Resume Parser TOTAL: %.3fs", perf_counter() - t)
        candidate = result.candidate
        t = perf_counter()
        candidate_id, identity_snapshot = await _resolve_candidate(
            org_id,
            job_id,
            candidate,
            result.confidence,
            result.warnings,
        )
        logger.info("======Mongo candidate resolution: %.3fs", perf_counter() - t)

        needs_review = result.needs_review or result.confidence < settings.parse_confidence_review_threshold
        t = perf_counter()

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
                        "identity": identity_snapshot,
                    },
                    "updated_at": datetime.now(timezone.utc),
                }
            },
        )
        logger.info("======Mongo resumes.update_one (parsed): %.3fs", perf_counter() - t)
        t = perf_counter()

        if not reparse:
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

        matching_blocked = (
            result.status == "partial"
            or "hard_filter_fields_uncertain" in result.warnings
        )
        if result.resume and result.status != "failed" and not matching_blocked:
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
                    "rematch": reparse,
                },
            )
            logger.info("======Redis enqueue match: %.3fs", perf_counter() - t)
        else:
            if result.resume and matching_blocked:
                now = datetime.now(timezone.utc)
                provenance = result.provenance or {}
                await db.match_results.update_one(
                    {
                        "org_id": org_id,
                        "job_id": job_id,
                        "candidate_id": str(candidate_id),
                        "is_current": True,
                    },
                    {
                        "$set": {
                            "resume_id": resume_id,
                            "batch_id": batch_id,
                            "hard_filters": {
                                "passed": False,
                                "failed_rules": [],
                                "unknown": True,
                            },
                            "score": 0.0,
                            "rank_signals": {"status": "Needs review"},
                            "explanation": {
                                "summary": "Matching deferred because required fields were not parsed reliably."
                            },
                            "review_status": "needs_review",
                            "matcher_version": "deferred",
                            "parse_attempt_id": provenance.get("parse_attempt_id"),
                            "parse_hash": provenance.get("parse_hash"),
                            "identity_snapshot": identity_snapshot,
                            "is_current": True,
                            "updated_at": now,
                        },
                        "$setOnInsert": {
                            "shortlisted": False,
                            "shortlisted_at": None,
                            "shortlisted_by": None,
                            "created_at": now,
                        },
                    },
                    upsert=True,
                )
            if not reparse:
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
        if not reparse:
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
    rematch = bool(payload.get("rematch"))

    job = await db.jobs.find_one({"_id": ObjectId(job_id), "org_id": org_id})
    resume_doc = await db.resumes.find_one({"_id": ObjectId(resume_id), "org_id": org_id})
    if not job or not resume_doc or not resume_doc.get("parse", {}).get("resume"):
        logger.error("Missing job/resume for match %s", resume_id)
        return

    if not rematch:
        await db.ingest_batches.update_one(
            {"_id": ObjectId(batch_id)},
            {"$inc": {"counters.matching": 1}},
        )

    try:
        jd = JobDescriptionSchema.model_validate(job["jd"])
        resume = MatchingResumeSchema.model_validate(resume_doc["parse"]["resume"])
        output = match_jd_resume(jd, resume)

        existing_result = await db.match_results.find_one(
            {
                "org_id": org_id,
                "job_id": job_id,
                "candidate_id": candidate_id,
                "is_current": True,
            },
            {"review_status": 1},
        )
        previous_review = (existing_result or {}).get("review_status")
        review_status = (
            previous_review
            if previous_review in {"approved", "rejected"}
            else ("needs_review" if needs_review else "none")
        )
        now = datetime.now(timezone.utc)
        jd_hash = hashlib.sha256(
            json.dumps(job["jd"], sort_keys=True, default=str).encode("utf-8")
        ).hexdigest()
        provenance = resume_doc.get("parse", {}).get("provenance", {})
        doc = {
            "resume_id": resume_id,
            "batch_id": batch_id,
            "matcher_version": output.matcher_version,
            "jd_revision": int(job.get("jd_revision") or 1),
            "jd_hash": jd_hash,
            "parse_attempt_id": provenance.get("parse_attempt_id"),
            "parse_hash": provenance.get("parse_hash"),
            "identity_snapshot": resume_doc.get("parse", {}).get("identity") or {},
            "hard_filters": output.hard_filters.model_dump(),
            "score": output.score,
            "rank_signals": output.rank_signals,
            "explanation": output.explanation,
            "review_status": review_status,
            "is_current": True,
            "stale": False,
            "updated_at": now,
        }
        await db.match_results.update_one(
            {
                "org_id": org_id,
                "job_id": job_id,
                "candidate_id": candidate_id,
                "is_current": True,
            },
            {
                "$set": doc,
                "$setOnInsert": {
                    "org_id": org_id,
                    "job_id": job_id,
                    "candidate_id": candidate_id,
                    "shortlisted": False,
                    "shortlisted_at": None,
                    "shortlisted_by": None,
                    "created_at": now,
                },
            },
            upsert=True,
        )
        if not rematch:
            await db.ingest_batches.update_one(
                {"_id": ObjectId(batch_id)},
                {
                    "$inc": {"counters.matching": -1, "counters.matched": 1},
                    "$set": {"updated_at": now},
                },
            )
    except Exception as exc:
        logger.exception("Match failed for %s", resume_id)
        if not rematch:
            await db.ingest_batches.update_one(
                {"_id": ObjectId(batch_id)},
                {
                    "$inc": {"counters.matching": -1, "counters.failed": 1},
                    "$set": {"updated_at": datetime.now(timezone.utc), "last_error": str(exc)},
                },
            )
        else:
            await db.match_results.update_many(
                {"org_id": org_id, "job_id": job_id, "candidate_id": candidate_id},
                {"$set": {"stale": True, "rematch_error": str(exc)}},
            )
    finally:
        if not rematch:
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
