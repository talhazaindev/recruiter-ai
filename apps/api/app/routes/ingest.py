"""CV ingest: multipart upload and Drive folder enqueue."""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.auth import get_current_user
from app.db import get_db
from app.models.schemas import DriveIngestRequest, UserPublic
from app.queue import QUEUE_INGEST, enqueue
from app.services.audit import write_audit
from app.services.pipeline import enqueue_parse_for_batch_files
from app.services.storage import upload_bytes

router = APIRouter(tags=["ingest"])

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc"}
MAX_FILE_BYTES = 15 * 1024 * 1024


def _ext(name: str) -> str:
    """Lowercase file extension including dot."""
    idx = name.rfind(".")
    return name[idx:].lower() if idx >= 0 else ""


async def _create_batch(
    org_id: str,
    job_id: str,
    source: str,
    created_by: str,
    meta: dict[str, Any] | None = None,
) -> str:
    """Insert an ingest_batches document and return its id."""
    db = get_db()
    now = datetime.now(timezone.utc)
    doc = {
        "org_id": org_id,
        "job_id": job_id,
        "source": source,
        "status": "queued",
        "meta": meta or {},
        "counters": {
            "total": 0,
            "parsing": 0,
            "parsed": 0,
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


import logging
from time import perf_counter

logger = logging.getLogger(__name__)


@router.post("/v1/jobs/{job_id}/ingest/upload")
async def ingest_upload(
    job_id: str,
    files: list[UploadFile] = File(...),
    user: UserPublic = Depends(get_current_user),
) -> dict[str, Any]:
    """Upload one or more CVs and enqueue parse/match pipeline."""
    overall_start = perf_counter()

    logger.info("========== INGEST API START ==========")
    db = get_db()
    t = perf_counter()

    job = await db.jobs.find_one({"_id": ObjectId(job_id), "org_id": user.org_id})
    logger.info("=======Mongo jobs.find_one: %.3fs", perf_counter() - t)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    t = perf_counter()

    batch_id = await _create_batch(user.org_id, job_id, "upload", user.id)
    logger.info("======Create batch: %.3fs", perf_counter() - t)
    resume_ids: list[str] = []
    now = datetime.now(timezone.utc)

    for f in files:
        name = f.filename or "resume.pdf"
        ext = _ext(name)
        if ext not in ALLOWED_EXTENSIONS:
            continue
        data = await f.read()
        if len(data) > MAX_FILE_BYTES:
            raise HTTPException(status_code=400, detail=f"{name} exceeds size limit")
        content_type = f.content_type or "application/octet-stream"
        key = f"{user.org_id}/{job_id}/{batch_id}/{uuid.uuid4().hex}{ext}"
        t = perf_counter()

        upload_bytes(key, data, content_type)
        logger.info("======MinIO upload (%s): %.3fs", name, perf_counter() - t)
        resume_doc = {
            "org_id": user.org_id,
            "candidate_id": None,
            "job_id": job_id,
            "batch_id": batch_id,
            "source": "upload",
            "source_ref": {
                "original_filename": name,
                "content_type": content_type,
                "storage_key": key,
            },
            "parse": {
                "status": "queued",
                "schema_version": "matching.v1",
                "resume": None,
                "confidence": 0.0,
                "field_confidence": {},
                "needs_review": False,
                "warnings": [],
                "provenance": {},
            },
            "created_at": now,
            "updated_at": now,
        }
        t = perf_counter()

        ins = await db.resumes.insert_one(resume_doc)
        logger.info("======Mongo resumes.insert_one: %.3fs", perf_counter() - t)
        resume_ids.append(str(ins.inserted_id))

    if not resume_ids:
        raise HTTPException(status_code=400, detail="No valid PDF/DOCX files")
    t = perf_counter()

    await db.ingest_batches.update_one(
        {"_id": ObjectId(batch_id)},
        {
            "$set": {
                "status": "processing",
                "counters.total": len(resume_ids),
                "updated_at": datetime.now(timezone.utc),
            }
        },
    )
    logger.info("======Mongo ingest_batches.update_one: %.3fs", perf_counter() - t)
    # Activate job when ingest starts
    if job.get("status") == "draft":
        t = perf_counter()

        await db.jobs.update_one(
            {"_id": ObjectId(job_id)},
            {"$set": {"status": "active", "updated_at": datetime.now(timezone.utc)}},
        )
        logger.info("======Mongo jobs.update_one: %.3fs", perf_counter() - t)

    try:
        t = perf_counter()

        enqueue_parse_for_batch_files(batch_id, user.org_id, job_id, resume_ids)
        logger.info("======Redis enqueue: %.3fs", perf_counter() - t)
    except Exception:
        # Fallback: process inline if Redis is down (dev resilience)
        from app.services.pipeline import process_parse_task

        for rid in resume_ids:
            await process_parse_task(
                {"resume_id": rid, "org_id": user.org_id, "job_id": job_id, "batch_id": batch_id}
            )

    t = perf_counter()

    await write_audit(
        user.org_id,
        user.id,
        "ingest.upload",
        "batch",
        batch_id,
        {"file_count": len(resume_ids)},
    )
    logger.info("======Audit write: %.3fs", perf_counter() - t)
    logger.info(
    "========== INGEST API END (%.3fs) ==========",
    perf_counter() - overall_start,
)
    return {"batch_id": batch_id, "file_count": len(resume_ids), "status": "processing"}


@router.post("/v1/jobs/{job_id}/ingest/drive")
async def ingest_drive(
    job_id: str,
    body: DriveIngestRequest,
    user: UserPublic = Depends(get_current_user),
) -> dict[str, Any]:
    """Enqueue Google Drive folder ingest for a job."""
    db = get_db()
    job = await db.jobs.find_one({"_id": ObjectId(job_id), "org_id": user.org_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if not body.folder_url.strip():
        raise HTTPException(status_code=400, detail="folder_url required")

    folder_id = _extract_drive_folder_id(body.folder_url)
    batch_id = await _create_batch(
        user.org_id,
        job_id,
        "gdrive",
        user.id,
        meta={"folder_url": body.folder_url, "folder_id": folder_id},
    )
    enqueue(
        QUEUE_INGEST,
        {
            "batch_id": batch_id,
            "job_id": job_id,
            "org_id": user.org_id,
            "folder_id": folder_id,
            "folder_url": body.folder_url,
            "user_id": user.id,
        },
    )
    await db.ingest_batches.update_one(
        {"_id": ObjectId(batch_id)},
        {"$set": {"status": "processing", "updated_at": datetime.now(timezone.utc)}},
    )
    await write_audit(user.org_id, user.id, "ingest.drive", "batch", batch_id, {"folder_id": folder_id})
    return {"batch_id": batch_id, "folder_id": folder_id, "status": "processing"}


@router.get("/v1/batches/{batch_id}")
async def get_batch(batch_id: str, user: UserPublic = Depends(get_current_user)) -> dict[str, Any]:
    """Return ingest batch progress counters."""
    db = get_db()
    doc = await db.ingest_batches.find_one({"_id": ObjectId(batch_id), "org_id": user.org_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Batch not found")
    return {
        "id": str(doc["_id"]),
        "job_id": doc["job_id"],
        "source": doc["source"],
        "status": doc["status"],
        "counters": doc.get("counters", {}),
        "meta": doc.get("meta", {}),
        "last_error": doc.get("last_error"),
        "created_at": doc["created_at"],
        "updated_at": doc["updated_at"],
    }


def _extract_drive_folder_id(url: str) -> str:
    """Parse a Google Drive folder id from common URL shapes."""
    patterns = [
        r"/folders/([a-zA-Z0-9_-]+)",
        r"[?&]id=([a-zA-Z0-9_-]+)",
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    # Allow raw folder id
    if re.fullmatch(r"[a-zA-Z0-9_-]{10,}", url.strip()):
        return url.strip()
    raise HTTPException(status_code=400, detail="Could not parse Drive folder id from URL")
