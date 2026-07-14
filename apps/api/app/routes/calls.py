"""Future AI voice screening call stubs."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from app.auth import get_current_user
from app.db import get_db
from app.models.schemas import ScreeningCallCreate, UserPublic
from app.services.audit import write_audit

router = APIRouter(tags=["calls"])


@router.get("/v1/candidates/{candidate_id}/calls")
async def list_calls(candidate_id: str, user: UserPublic = Depends(get_current_user)) -> list[dict[str, Any]]:
    """List screening calls for a candidate (future voice agent)."""
    db = get_db()
    cursor = db.screening_calls.find(
        {"org_id": user.org_id, "candidate_id": candidate_id}
    ).sort("created_at", -1)
    rows: list[dict[str, Any]] = []
    async for doc in cursor:
        rows.append(_public_call(doc))
    return rows


@router.post("/v1/candidates/{candidate_id}/calls", status_code=201)
async def create_call(
    candidate_id: str,
    body: ScreeningCallCreate,
    user: UserPublic = Depends(get_current_user),
) -> dict[str, Any]:
    """Stub: queue an AI screening call (not executed in v1)."""
    db = get_db()
    cand = await db.candidates.find_one({"_id": ObjectId(candidate_id), "org_id": user.org_id})
    if not cand:
        raise HTTPException(status_code=404, detail="Candidate not found")

    job_id = None
    if body.match_result_id:
        mr = await db.match_results.find_one(
            {"_id": ObjectId(body.match_result_id), "org_id": user.org_id}
        )
        if mr:
            job_id = mr.get("job_id")

    now = datetime.now(timezone.utc)
    doc = {
        "org_id": user.org_id,
        "job_id": job_id,
        "candidate_id": candidate_id,
        "match_result_id": body.match_result_id,
        "provider": "twilio_ai_agent",
        "status": "queued_stub",
        "started_at": None,
        "ended_at": None,
        "recording_url": None,
        "transcript_text": None,
        "transcript_json": None,
        "agent_summary": None,
        "disposition": None,
        "message": "AI voice screening is not enabled yet. Record is reserved for future workers.",
        "created_by": user.id,
        "created_at": now,
        "updated_at": now,
    }
    ins = await db.screening_calls.insert_one(doc)
    doc["_id"] = ins.inserted_id
    await write_audit(user.org_id, user.id, "call.stub_create", "screening_call", str(ins.inserted_id))
    return _public_call(doc)


@router.get("/v1/jobs/{job_id}/calls")
async def list_job_calls(job_id: str, user: UserPublic = Depends(get_current_user)) -> list[dict[str, Any]]:
    """List all screening calls for a job."""
    db = get_db()
    cursor = db.screening_calls.find({"org_id": user.org_id, "job_id": job_id}).sort("created_at", -1)
    return [_public_call(doc) async for doc in cursor]


def _public_call(doc: dict[str, Any]) -> dict[str, Any]:
    """Serialize a screening_calls document."""
    return {
        "id": str(doc["_id"]),
        "org_id": doc.get("org_id"),
        "job_id": doc.get("job_id"),
        "candidate_id": doc.get("candidate_id"),
        "match_result_id": doc.get("match_result_id"),
        "provider": doc.get("provider"),
        "status": doc.get("status"),
        "started_at": doc.get("started_at"),
        "ended_at": doc.get("ended_at"),
        "recording_url": doc.get("recording_url"),
        "transcript_text": doc.get("transcript_text"),
        "agent_summary": doc.get("agent_summary"),
        "disposition": doc.get("disposition"),
        "message": doc.get("message"),
        "created_at": doc.get("created_at"),
        "updated_at": doc.get("updated_at"),
    }
