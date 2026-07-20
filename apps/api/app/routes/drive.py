"""Google Drive OAuth + folder listing helpers."""

from __future__ import annotations

import logging
import hashlib
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlencode

import httpx
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from pymongo.errors import DuplicateKeyError

from app.auth import get_current_user
from app.config import get_settings
from app.db import get_db
from app.models.schemas import UserPublic
from app.services.storage import upload_bytes
from app.services.pipeline import enqueue_parse_for_batch_files

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/integrations/drive", tags=["drive"])

DRIVE_AUTH = "https://accounts.google.com/o/oauth2/v2/auth"
DRIVE_TOKEN = "https://oauth2.googleapis.com/token"
DRIVE_FILES = "https://www.googleapis.com/drive/v3/files"
SCOPES = "https://www.googleapis.com/auth/drive.readonly"


@router.get("/auth-url")
async def drive_auth_url(user: UserPublic = Depends(get_current_user)) -> dict[str, str]:
    """Return Google OAuth URL for connecting Drive."""
    settings = get_settings()
    if not settings.google_client_id:
        raise HTTPException(
            status_code=501,
            detail="Google Drive not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.",
        )
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": settings.google_redirect_uri,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent",
        "state": f"{user.org_id}:{user.id}",
    }
    return {"url": f"{DRIVE_AUTH}?{urlencode(params)}"}


@router.get("/callback")
async def drive_callback(code: str = Query(...), state: str = Query(...)) -> RedirectResponse:
    """OAuth callback — store refresh token and redirect to web app."""
    settings = get_settings()
    try:
        org_id, user_id = state.split(":", 1)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid state") from exc

    async with httpx.AsyncClient(timeout=30) as client:
        token_res = await client.post(
            DRIVE_TOKEN,
            data={
                "code": code,
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uri": settings.google_redirect_uri,
                "grant_type": "authorization_code",
            },
        )
    if token_res.status_code >= 400:
        raise HTTPException(status_code=400, detail="Failed to exchange Drive code")
    tokens = token_res.json()
    db = get_db()
    await db.drive_tokens.update_one(
        {"org_id": org_id, "user_id": user_id},
        {
            "$set": {
                "org_id": org_id,
                "user_id": user_id,
                "access_token": tokens.get("access_token"),
                "refresh_token": tokens.get("refresh_token"),
                "expires_in": tokens.get("expires_in"),
                "token_type": tokens.get("token_type"),
                "updated_at": datetime.now(timezone.utc),
            }
        },
        upsert=True,
    )
    web = settings.cors_origin_list[0] if settings.cors_origin_list else "http://localhost:5173"
    return RedirectResponse(f"{web}/settings/drive?connected=1")


@router.get("/status")
async def drive_status(user: UserPublic = Depends(get_current_user)) -> dict[str, Any]:
    """Whether Drive is connected for this user."""
    db = get_db()
    doc = await db.drive_tokens.find_one({"org_id": user.org_id, "user_id": user.id})
    configured = bool(get_settings().google_client_id)
    return {"configured": configured, "connected": bool(doc), "updated_at": (doc or {}).get("updated_at")}


async def get_access_token(org_id: str, user_id: str) -> str | None:
    """Return a usable Drive access token, refreshing if possible."""
    settings = get_settings()
    db = get_db()
    doc = await db.drive_tokens.find_one({"org_id": org_id, "user_id": user_id})
    if not doc:
        return None
    if doc.get("access_token"):
        return doc["access_token"]
    if not doc.get("refresh_token"):
        return None
    async with httpx.AsyncClient(timeout=30) as client:
        res = await client.post(
            DRIVE_TOKEN,
            data={
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "refresh_token": doc["refresh_token"],
                "grant_type": "refresh_token",
            },
        )
    if res.status_code >= 400:
        return None
    data = res.json()
    await db.drive_tokens.update_one(
        {"_id": doc["_id"]},
        {"$set": {"access_token": data.get("access_token"), "updated_at": datetime.now(timezone.utc)}},
    )
    return data.get("access_token")


async def ingest_drive_folder(
    *,
    org_id: str,
    user_id: str,
    job_id: str,
    batch_id: str,
    folder_id: str,
) -> int:
    """List PDF/DOCX in a Drive folder, store files, enqueue parse. Returns file count."""
    token = await get_access_token(org_id, user_id)
    db = get_db()
    if not token:
        # Stub mode: mark batch with instructional error so UI stays useful in demos
        await db.ingest_batches.update_one(
            {"_id": ObjectId(batch_id)},
            {
                "$set": {
                    "status": "failed",
                    "last_error": (
                        "Google Drive not connected. Connect via /v1/integrations/drive/auth-url "
                        "or upload files manually."
                    ),
                    "updated_at": datetime.now(timezone.utc),
                }
            },
        )
        return 0

    q = f"'{folder_id}' in parents and trashed=false"
    files: list[dict[str, Any]] = []
    page_token = None
    async with httpx.AsyncClient(timeout=60) as client:
        while True:
            params: dict[str, Any] = {
                "q": q,
                "fields": "nextPageToken, files(id, name, mimeType)",
                "pageSize": 100,
            }
            if page_token:
                params["pageToken"] = page_token
            res = await client.get(
                DRIVE_FILES,
                params=params,
                headers={"Authorization": f"Bearer {token}"},
            )
            if res.status_code >= 400:
                await db.ingest_batches.update_one(
                    {"_id": ObjectId(batch_id)},
                    {
                        "$set": {
                            "status": "failed",
                            "last_error": res.text,
                            "updated_at": datetime.now(timezone.utc),
                        }
                    },
                )
                return 0
            payload = res.json()
            for f in payload.get("files", []):
                name = f.get("name", "")
                lower = name.lower()
                if lower.endswith((".pdf", ".docx", ".doc")):
                    files.append(f)
            page_token = payload.get("nextPageToken")
            if not page_token:
                break

        resume_ids: list[str] = []
        skipped_count = 0
        now = datetime.now(timezone.utc)
        for f in files:
            file_id = f["id"]
            name = f["name"]
            dl = await client.get(
                f"{DRIVE_FILES}/{file_id}?alt=media",
                headers={"Authorization": f"Bearer {token}"},
            )
            if dl.status_code >= 400:
                logger.warning("Skip Drive file %s: %s", name, dl.status_code)
                continue
            source_sha256 = hashlib.sha256(dl.content).hexdigest()
            if await db.resumes.find_one(
                {
                    "org_id": org_id,
                    "job_id": job_id,
                    "$or": [
                        {"source_ref.drive_file_id": file_id},
                        {"source_ref.source_sha256": source_sha256},
                    ],
                },
                {"_id": 1},
            ):
                skipped_count += 1
                continue
            ext = "." + name.rsplit(".", 1)[-1].lower() if "." in name else ".pdf"
            key = f"{org_id}/{job_id}/sha256/{source_sha256}{ext}"
            content_type = f.get("mimeType") or "application/octet-stream"
            upload_bytes(key, dl.content, content_type)
            try:
                ins = await db.resumes.insert_one(
                    {
                        "org_id": org_id,
                        "candidate_id": None,
                        "job_id": job_id,
                        "batch_id": batch_id,
                        "source": "gdrive",
                        "source_ref": {
                            "drive_file_id": file_id,
                            "original_filename": name,
                            "content_type": content_type,
                            "storage_key": key,
                            "source_sha256": source_sha256,
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
                )
            except DuplicateKeyError:
                skipped_count += 1
                continue
            resume_ids.append(str(ins.inserted_id))

    await db.ingest_batches.update_one(
        {"_id": ObjectId(batch_id)},
        {
            "$set": {
                "status": "processing" if resume_ids else "completed",
                "counters.total": len(resume_ids),
                "meta.skipped_duplicates": skipped_count,
                "updated_at": datetime.now(timezone.utc),
            }
        },
    )
    if resume_ids:
        enqueue_parse_for_batch_files(batch_id, org_id, job_id, resume_ids)
    return len(resume_ids)
