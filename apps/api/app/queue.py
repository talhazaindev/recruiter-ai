"""Redis-backed job queue for ingest / parse / match workers."""

from __future__ import annotations

import json
from typing import Any

import redis

from app.config import get_settings

QUEUE_PARSE = "queue:parse"
QUEUE_MATCH = "queue:match"
QUEUE_INGEST = "queue:ingest"
MAX_ATTEMPTS = 3


def get_redis() -> redis.Redis:
    """Sync Redis client for enqueue from API and workers."""
    return redis.from_url(get_settings().redis_url, decode_responses=True)


def enqueue(queue: str, payload: dict[str, Any]) -> None:
    """Push a JSON task onto a named queue."""
    client = get_redis()
    task = dict(payload)
    task.setdefault("_attempt", 0)
    client.rpush(queue, json.dumps(task))


def dequeue(queue: str, timeout: int = 5) -> dict[str, Any] | None:
    """Atomically claim a task; returns None on timeout."""
    client = get_redis()
    processing = f"{queue}:processing"
    raw = client.brpoplpush(queue, processing, timeout=timeout)
    if not raw:
        return None
    payload = json.loads(raw)
    payload["_queue_raw"] = raw
    payload["_queue_name"] = queue
    return payload


def acknowledge(payload: dict[str, Any]) -> None:
    """Remove a successfully processed claimed task."""
    queue = str(payload.get("_queue_name") or "")
    raw = str(payload.get("_queue_raw") or "")
    if queue and raw:
        get_redis().lrem(f"{queue}:processing", 1, raw)


def retry_or_dead_letter(payload: dict[str, Any], error: str) -> None:
    """Retry a claimed task or move it to a dead-letter queue."""
    queue = str(payload.get("_queue_name") or "")
    raw = str(payload.get("_queue_raw") or "")
    if not queue or not raw:
        return
    client = get_redis()
    client.lrem(f"{queue}:processing", 1, raw)
    task = {
        key: value
        for key, value in payload.items()
        if key not in {"_queue_raw", "_queue_name"}
    }
    task["_attempt"] = int(task.get("_attempt", 0)) + 1
    task["_last_error"] = error
    destination = queue if task["_attempt"] < MAX_ATTEMPTS else f"{queue}:dead"
    client.rpush(destination, json.dumps(task))


def recover_claimed(queue: str) -> int:
    """Return tasks left claimed by a stopped worker to the ready queue."""
    client = get_redis()
    processing = f"{queue}:processing"
    recovered = 0
    while client.rpoplpush(processing, queue) is not None:
        recovered += 1
    return recovered
