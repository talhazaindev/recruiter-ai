"""Standalone workers that poll Redis queues for parse / match / ingest."""

from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path

# Allow `python workers/parse_worker.py` from repo root
ROOT = Path(__file__).resolve().parents[1]
API_ROOT = ROOT / "apps" / "api"
sys.path.insert(0, str(API_ROOT))
sys.path.insert(0, str(ROOT))

from app.db import close_db, connect_db  # noqa: E402
from app.queue import (  # noqa: E402
    QUEUE_INGEST,
    QUEUE_MATCH,
    QUEUE_PARSE,
    acknowledge,
    dequeue,
    recover_claimed,
    retry_or_dead_letter,
)
from app.routes.drive import ingest_drive_folder  # noqa: E402
from app.services.pipeline import process_match_task, process_parse_task  # noqa: E402
from app.services.storage import ensure_bucket  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("workers")


async def run_parse_loop() -> None:
    """Continuously process parse queue."""
    await connect_db()
    try:
        ensure_bucket()
    except Exception as exc:
        logger.warning("Storage init: %s", exc)
    logger.info("Parse worker listening on %s", QUEUE_PARSE)
    recovered = await asyncio.to_thread(recover_claimed, QUEUE_PARSE)
    if recovered:
        logger.warning("Recovered %s interrupted parse tasks", recovered)
    while True:
        payload = await asyncio.to_thread(dequeue, QUEUE_PARSE, 5)
        if not payload:
            continue
        try:
            await process_parse_task(payload)
            await asyncio.to_thread(acknowledge, payload)
        except Exception as exc:
            logger.exception("parse task failed")
            await asyncio.to_thread(retry_or_dead_letter, payload, str(exc))


async def run_match_loop() -> None:
    """Continuously process match queue."""
    await connect_db()
    logger.info("Match worker listening on %s", QUEUE_MATCH)
    recovered = await asyncio.to_thread(recover_claimed, QUEUE_MATCH)
    if recovered:
        logger.warning("Recovered %s interrupted match tasks", recovered)
    while True:
        payload = await asyncio.to_thread(dequeue, QUEUE_MATCH, 5)
        if not payload:
            continue
        try:
            await process_match_task(payload)
            await asyncio.to_thread(acknowledge, payload)
        except Exception as exc:
            logger.exception("match task failed")
            await asyncio.to_thread(retry_or_dead_letter, payload, str(exc))


async def run_ingest_loop() -> None:
    """Continuously process Drive ingest queue."""
    await connect_db()
    try:
        ensure_bucket()
    except Exception as exc:
        logger.warning("Storage init: %s", exc)
    logger.info("Ingest worker listening on %s", QUEUE_INGEST)
    recovered = await asyncio.to_thread(recover_claimed, QUEUE_INGEST)
    if recovered:
        logger.warning("Recovered %s interrupted ingest tasks", recovered)
    while True:
        payload = await asyncio.to_thread(dequeue, QUEUE_INGEST, 5)
        if not payload:
            continue
        try:
            count = await ingest_drive_folder(
                org_id=payload["org_id"],
                user_id=payload["user_id"],
                job_id=payload["job_id"],
                batch_id=payload["batch_id"],
                folder_id=payload["folder_id"],
            )
            logger.info("Drive ingest batch %s files=%s", payload["batch_id"], count)
            await asyncio.to_thread(acknowledge, payload)
        except Exception as exc:
            logger.exception("ingest task failed")
            await asyncio.to_thread(retry_or_dead_letter, payload, str(exc))


def main() -> None:
    """CLI entry: python -m workers.parse_worker style via argv."""
    role = Path(sys.argv[0]).stem
    if len(sys.argv) > 1:
        role = sys.argv[1]
    loops = {
        "parse_worker": run_parse_loop,
        "parse": run_parse_loop,
        "match_worker": run_match_loop,
        "match": run_match_loop,
        "ingest_worker": run_ingest_loop,
        "ingest": run_ingest_loop,
    }
    fn = loops.get(role)
    if not fn:
        print("Usage: python workers/<parse|match|ingest>_worker.py")
        sys.exit(1)
    asyncio.run(fn())


if __name__ == "__main__":
    main()
