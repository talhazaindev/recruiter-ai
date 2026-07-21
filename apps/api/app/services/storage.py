"""CV file storage backed by MongoDB GridFS.

CV binaries are stored in GridFS inside the same shared Atlas database as the
resume metadata, so every developer/instance pointed at the same MONGODB_URI
sees the same files. The public interface (upload_bytes / download_bytes /
ensure_bucket) is kept stable so callers do not need to change.

Files are addressed by the same ``storage_key`` string used previously as the
S3 object key (e.g. ``{org_id}/{job_id}/sha256/{sha}{ext}``), stored as the
GridFS filename.
"""

from __future__ import annotations

from functools import lru_cache

import gridfs
from pymongo import MongoClient

from app.config import get_settings

GRIDFS_BUCKET = "resume_files"


@lru_cache
def _get_sync_db():
    """Return a synchronous pymongo database handle for GridFS access."""
    settings = get_settings()
    client: MongoClient = MongoClient(settings.mongodb_uri)
    return client[settings.mongodb_db]


@lru_cache
def _get_fs() -> gridfs.GridFS:
    """Return the GridFS handle for the resume file bucket."""
    return gridfs.GridFS(_get_sync_db(), collection=GRIDFS_BUCKET)


def ensure_bucket() -> None:
    """Ensure GridFS indexes exist (idempotent).

    GridFS creates its own indexes on first write; this touches the files
    collection to make lookups by ``filename`` fast and to surface any
    connection problem early during startup.
    """
    db = _get_sync_db()
    db[f"{GRIDFS_BUCKET}.files"].create_index("filename")


def upload_bytes(key: str, data: bytes, content_type: str) -> str:
    """Store raw bytes in GridFS under ``key`` and return the key.

    Any existing file with the same key is removed first so a re-upload
    replaces the previous copy instead of accumulating versions.
    """
    fs = _get_fs()
    for existing in fs.find({"filename": key}):
        fs.delete(existing._id)
    fs.put(data, filename=key, contentType=content_type)
    return key


def download_bytes(key: str) -> bytes:
    """Download stored bytes by ``key``.

    Raises FileNotFoundError if the key is not present so callers can map it
    to a 404.
    """
    fs = _get_fs()
    grid_out = fs.find_one({"filename": key})
    if grid_out is None:
        raise FileNotFoundError(f"No stored file for key: {key}")
    return grid_out.read()


def delete_bytes(key: str) -> None:
    """Delete any stored file(s) for ``key`` (idempotent)."""
    fs = _get_fs()
    for existing in fs.find({"filename": key}):
        fs.delete(existing._id)
