"""Screening calls — not available until a real voice agent is configured."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.auth import get_current_user
from app.models.schemas import UserPublic

router = APIRouter(tags=["calls"])


@router.get("/v1/candidates/{candidate_id}/calls")
async def list_calls(candidate_id: str, user: UserPublic = Depends(get_current_user)) -> list:
    """Voice screening is not enabled."""
    _ = (candidate_id, user)
    return []


@router.post("/v1/candidates/{candidate_id}/calls", status_code=501)
async def create_call(candidate_id: str, user: UserPublic = Depends(get_current_user)) -> None:
    """Reject stub call creation — voice agent not wired."""
    _ = (candidate_id, user)
    raise HTTPException(
        status_code=501,
        detail="AI voice screening is not available yet.",
    )


@router.get("/v1/jobs/{job_id}/calls")
async def list_job_calls(job_id: str, user: UserPublic = Depends(get_current_user)) -> list:
    """Voice screening is not enabled."""
    _ = (job_id, user)
    return []
