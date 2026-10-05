"""Audit and optionally repair candidate/result integrity in Atlas.

Dry-run is the default. Pass ``--apply`` only after reviewing the JSON report.
Apply mode creates a timestamped backup collection before changing records.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

ROOT = Path(__file__).resolve().parents[3]
API_ROOT = ROOT / "apps" / "api"
sys.path.insert(0, str(API_ROOT))
sys.path.insert(0, str(ROOT))

from app.config import get_settings  # noqa: E402
from app.queue import QUEUE_PARSE, enqueue  # noqa: E402


def _valid_name(value: Any) -> bool:
    """Return whether a stored candidate name is plausible."""
    text = " ".join(str(value or "").split())
    return (
        2 <= len(text.split()) <= 6
        and len(text) <= 80
        and "@" not in text
        and "http" not in text.lower()
        and text.lower()
        not in {"software engineer", "work experience", "professional summary"}
    )


def _timestamp(value: Any) -> float:
    """Convert a stored datetime into a sortable timestamp."""
    return value.timestamp() if isinstance(value, datetime) else 0.0


def _age_seconds(value: Any) -> float:
    """Return record age while tolerating naive MongoDB datetimes."""
    if not isinstance(value, datetime):
        return 0.0
    now = datetime.now(value.tzinfo) if value.tzinfo else datetime.utcnow()
    return (now - value).total_seconds()


async def _audit_job(
    db: Any, job: dict[str, Any], *, load_records: bool
) -> tuple[dict[str, Any], dict[str, list[dict]]]:
    """Return an integrity report and optionally loaded records for one job."""
    job_id = str(job["_id"])
    base_results_query = {"org_id": job["org_id"], "job_id": job_id}
    projection_results = {
        "_id": 1,
        "candidate_id": 1,
        "matcher_version": 1,
        "jd_revision": 1,
        "stale": 1,
    }
    results_cursor = db.match_results.find(base_results_query, projection_results)
    results = await results_cursor.to_list(length=None)

    base_resumes_query = {"org_id": job["org_id"], "job_id": job_id}
    projection_resumes = {
        "_id": 1,
        "batch_id": 1,
        "candidate_id": 1,
        "source_ref.source_sha256": 1,
        "source_ref.drive_file_id": 1,
        "parse.status": 1,
        "parse.identity": 1,
        "parse.confidence": 1,
        "parse.needs_review": 1,
        "parse.warnings": 1,
        "updated_at": 1,
    }
    if load_records:
        resumes = await db.resumes.find(base_resumes_query).to_list(length=None)
    else:
        resumes = await db.resumes.find(base_resumes_query, projection_resumes).to_list(length=None)

    batches = await db.ingest_batches.find(
        {"org_id": job["org_id"], "job_id": job_id},
        {"_id": 1, "status": 1, "updated_at": 1},
    ).to_list(length=None)
    candidate_ids = {str(row.get("candidate_id") or "") for row in results if row.get("candidate_id")}
    candidates = await db.candidates.find(
        {
            "org_id": job["org_id"],
            "_id": {"$in": [ObjectId(cid) for cid in candidate_ids if ObjectId.is_valid(cid)]},
        },
        {"_id": 1, "name": 1},
    ).to_list(length=None)

    result_groups: dict[str, list[dict]] = defaultdict(list)
    for row in results:
        result_groups[str(row.get("candidate_id") or "")].append(row)
    hash_groups: dict[str, list[str]] = defaultdict(list)
    for resume in resumes:
        digest = str((resume.get("source_ref") or {}).get("source_sha256") or "")
        if digest:
            hash_groups[digest].append(str(resume["_id"]))

    malformed = [
        {"candidate_id": str(candidate["_id"]), "name": candidate.get("name", "")}
        for candidate in candidates
        if not _valid_name(candidate.get("name"))
    ]
    current_revision = int(job.get("jd_revision") or 1)
    stale = []
    for row in results:
        if row.get("matcher_version") not in {"ats-agent.v2", "ats-agent.v3"}:
            stale.append(str(row["_id"]))
            continue
        if int(row.get("jd_revision") or 0) != current_revision:
            stale.append(str(row["_id"]))
            continue
        if row.get("stale") is True:
            stale.append(str(row["_id"]))
            continue
    stuck = [
        str(batch["_id"])
        for batch in batches
        if batch.get("status") in {"queued", "processing"}
        and _age_seconds(batch.get("updated_at")) > 3600
    ]
    report = {
        "job_id": job_id,
        "job_title": (job.get("jd") or {}).get("job_title"),
        "result_rows": len(results),
        "unique_candidates": len([key for key in result_groups if key]),
        "duplicate_result_rows": sum(max(0, len(rows) - 1) for rows in result_groups.values()),
        "duplicate_candidate_groups": {
            key: len(rows) for key, rows in result_groups.items() if key and len(rows) > 1
        },
        "duplicate_fingerprint_groups": {
            key: values for key, values in hash_groups.items() if len(values) > 1
        },
        "missing_fingerprints": sum(
            not bool((resume.get("source_ref") or {}).get("source_sha256"))
            for resume in resumes
        ),
        "malformed_candidates": malformed,
        "stale_results": stale,
        "stuck_batches": stuck,
    }
    if not load_records:
        return report, {}

    return report, {"results": results, "resumes": resumes, "batches": batches, "candidates": candidates}


async def _apply_job(db: Any, job: dict[str, Any], records: dict[str, list[dict]], backup: str) -> None:
    """Archive loaded records, choose current results, and enqueue reparses."""
    backup_docs: list[dict[str, Any]] = []
    for collection, documents in records.items():
        for document in documents:
            backup_docs.append({"source_collection": collection, "document": document})
    backup_docs.append({"source_collection": "jobs", "document": job})
    if backup_docs:
        await db[backup].insert_many(backup_docs)

    resumes_by_candidate: dict[str, list[dict]] = defaultdict(list)
    for resume in records["resumes"]:
        if resume.get("candidate_id"):
            resumes_by_candidate[str(resume["candidate_id"])].append(resume)
    results_by_candidate: dict[str, list[dict]] = defaultdict(list)
    for result in records["results"]:
        results_by_candidate[str(result.get("candidate_id") or "")].append(result)

    for candidate_id, resumes in resumes_by_candidate.items():
        resumes.sort(
            key=lambda resume: (
                _valid_name((resume.get("parse") or {}).get("identity", {}).get("name")),
                float((resume.get("parse") or {}).get("confidence") or 0),
                _timestamp(resume.get("updated_at")),
            ),
            reverse=True,
        )
        canonical_resume = resumes[0]
        results = results_by_candidate.get(candidate_id, [])
        if results:
            results.sort(
                key=lambda row: (
                    row.get("resume_id") == str(canonical_resume["_id"]),
                    _timestamp(row.get("updated_at")),
                    float(row.get("score") or 0),
                ),
                reverse=True,
            )
            canonical_result = results[0]
            shortlisted = any(bool(row.get("shortlisted")) for row in results)
            review_values = [row.get("review_status") for row in results]
            review_status = next(
                (
                    status
                    for status in ("approved", "rejected", "needs_review", "none")
                    if status in review_values
                ),
                "none",
            )
            await db.match_results.update_many(
                {"_id": {"$in": [row["_id"] for row in results]}},
                {"$set": {"is_current": False, "integrity_archived": True}},
            )
            await db.match_results.update_one(
                {"_id": canonical_result["_id"]},
                {
                    "$set": {
                        "is_current": True,
                        "integrity_archived": False,
                        "resume_id": str(canonical_resume["_id"]),
                        "shortlisted": shortlisted,
                        "review_status": review_status,
                        "stale": True,
                    }
                },
            )
        enqueue(
            QUEUE_PARSE,
            {
                "resume_id": str(canonical_resume["_id"]),
                "candidate_id": candidate_id,
                "job_id": str(job["_id"]),
                "batch_id": canonical_resume["batch_id"],
                "org_id": job["org_id"],
                "reparse": True,
            },
        )


async def run(job_id: str | None, apply: bool) -> None:
    """Run the audit and optional repair."""
    settings = get_settings()
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.mongodb_db]
    query: dict[str, Any] = {}
    if job_id:
        if not ObjectId.is_valid(job_id):
            raise ValueError("Invalid job id")
        query["_id"] = ObjectId(job_id)
    jobs = await db.jobs.find(query).to_list(length=None)
    backup = "integrity_backup_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    reports: list[dict[str, Any]] = []
    try:
        for job in jobs:
            report, records = await _audit_job(db, job, load_records=apply)
            reports.append(report)
            if apply:
                await _apply_job(db, job, records, backup)
        print(json.dumps({"mode": "apply" if apply else "dry-run", "backup": backup if apply else None, "jobs": reports}, indent=2, default=str))
    finally:
        client.close()


def main() -> None:
    """Parse CLI arguments and execute the audit."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-id")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    asyncio.run(run(args.job_id, args.apply))


if __name__ == "__main__":
    main()
