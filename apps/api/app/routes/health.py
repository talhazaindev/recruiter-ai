"""Health and readiness endpoints."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from app.config import get_settings
from app.db import get_db

router = APIRouter(tags=["health"])


@router.get("/v1/health")
async def health() -> dict[str, Any]:
    """Liveness probe."""
    return {"status": "ok", "service": "recruiter-api"}


@router.get("/v1/ready")
async def ready() -> dict[str, Any]:
    """Readiness: Mongo ping + settings snapshot (no secrets)."""
    settings = get_settings()
    mongo_ok = False
    try:
        db = get_db()
        await db.command("ping")
        mongo_ok = True
    except Exception as exc:
        return {"status": "degraded", "mongo": False, "error": str(exc)}
    return {
        "status": "ready" if mongo_ok else "degraded",
        "mongo": mongo_ok,
        "parser_mode": settings.parser_mode,
        "matcher_mode": settings.matcher_mode,
        "org_id_default": settings.default_org_id,
    }
