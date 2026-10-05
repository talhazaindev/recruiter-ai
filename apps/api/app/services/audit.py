"""Audit event helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.db import get_db


async def write_audit(
    org_id: str,
    actor_id: str,
    action: str,
    entity_type: str,
    entity_id: str,
    meta: dict[str, Any] | None = None,
) -> None:
    """Persist an audit trail row for sensitive HR actions."""
    db = get_db()
    await db.audit_events.insert_one(
        {
            "org_id": org_id,
            "actor_id": actor_id,
            "action": action,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "meta": meta or {},
            "created_at": datetime.now(timezone.utc),
        }
    )
