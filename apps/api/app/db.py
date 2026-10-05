"""MongoDB connection, indexes, and collection helpers."""

from __future__ import annotations

from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import get_settings

_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None


COLLECTIONS = (
    "users",
    "jobs",
    "candidates",
    "resumes",
    "ingest_batches",
    "match_results",
    "screening_calls",
    "audit_events",
    "drive_tokens",
)


async def connect_db() -> AsyncIOMotorDatabase:
    """Connect to MongoDB and ensure indexes."""
    global _client, _db
    settings = get_settings()
    _client = AsyncIOMotorClient(settings.mongodb_uri)
    _db = _client[settings.mongodb_db]
    await ensure_indexes(_db)
    return _db


async def close_db() -> None:
    """Close MongoDB client."""
    global _client, _db
    if _client is not None:
        _client.close()
    _client = None
    _db = None


def get_db() -> AsyncIOMotorDatabase:
    """Return the active database handle."""
    if _db is None:
        raise RuntimeError("Database not connected")
    return _db


async def ensure_indexes(db: AsyncIOMotorDatabase) -> None:
    """Create production indexes for scale and org isolation."""
    await db.users.create_index("email", unique=True)
    await db.users.create_index([("org_id", 1), ("email", 1)])

    await db.jobs.create_index([("org_id", 1), ("status", 1), ("updated_at", -1)])

    await db.resumes.create_index([("org_id", 1), ("batch_id", 1)])
    await db.resumes.create_index([("org_id", 1), ("job_id", 1)])
    await db.resumes.create_index([("org_id", 1), ("parse.needs_review", 1)])
    await db.resumes.create_index(
        [("org_id", 1), ("job_id", 1), ("source_ref.source_sha256", 1)],
        unique=True,
        partialFilterExpression={"source_ref.source_sha256": {"$type": "string"}},
        name="unique_job_resume_sha256",
    )
    await db.resumes.create_index(
        [("org_id", 1), ("job_id", 1), ("source_ref.drive_file_id", 1)],
        unique=True,
        partialFilterExpression={"source_ref.drive_file_id": {"$type": "string"}},
        name="unique_job_drive_file",
    )

    await db.match_results.create_index([("org_id", 1), ("job_id", 1), ("score", -1)])
    await db.match_results.create_index([("org_id", 1), ("job_id", 1), ("shortlisted", 1)])
    await db.match_results.create_index([("org_id", 1), ("job_id", 1), ("review_status", 1)])
    legacy_match_index = "org_id_1_job_id_1_resume_id_1"
    if legacy_match_index in await db.match_results.index_information():
        await db.match_results.drop_index(legacy_match_index)
    await db.match_results.create_index(
        [("org_id", 1), ("job_id", 1), ("candidate_id", 1)],
        unique=True,
        partialFilterExpression={"is_current": True},
        name="unique_current_job_candidate",
    )

    await db.candidates.create_index([("org_id", 1), ("emails", 1)])
    await db.candidates.create_index([("org_id", 1), ("phones", 1)])
    await db.candidates.create_index(
        [("org_id", 1), ("primary_email_normalized", 1)],
        unique=True,
        partialFilterExpression={"primary_email_normalized": {"$type": "string"}},
        name="unique_org_primary_email",
    )

    await db.ingest_batches.create_index([("org_id", 1), ("job_id", 1), ("created_at", -1)])
    await db.screening_calls.create_index([("org_id", 1), ("candidate_id", 1), ("created_at", -1)])
    await db.audit_events.create_index([("org_id", 1), ("created_at", -1)])
    await db.drive_tokens.create_index([("org_id", 1), ("user_id", 1)], unique=True)


def oid_str(doc: dict[str, Any] | None, field: str = "_id") -> str | None:
    """Convert ObjectId field to string if present."""
    if not doc or field not in doc:
        return None
    return str(doc[field])
