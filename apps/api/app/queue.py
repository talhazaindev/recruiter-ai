"""Redis-backed job queue for ingest / parse / match workers."""

from __future__ import annotations

import json
from typing import Any

import redis

from app.config import get_settings

QUEUE_PARSE = "queue:parse"
QUEUE_MATCH = "queue:match"
QUEUE_INGEST = "queue:ingest"


def get_redis() -> redis.Redis:
    """Sync Redis client for enqueue from API and workers."""
    return redis.from_url(get_settings().redis_url, decode_responses=True)


def enqueue(queue: str, payload: dict[str, Any]) -> None:
    """Push a JSON task onto a named queue."""
    client = get_redis()
    client.rpush(queue, json.dumps(payload))


def dequeue(queue: str, timeout: int = 5) -> dict[str, Any] | None:
    """Blocking pop from a queue; returns None on timeout."""
    client = get_redis()
    item = client.blpop(queue, timeout=timeout)
    if not item:
        return None
    _, raw = item
    return json.loads(raw)
