"""Tests for skip-on-recover behavior in parse / match / Drive ingest."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from bson import ObjectId

from app.queue import QUEUE_PARSE, recover_claimed
from app.routes import drive as drive_route
from app.services import pipeline


def _payload(*, resume_id: str | None = None) -> dict:
    """Minimal worker payload."""
    return {
        "resume_id": resume_id or str(ObjectId()),
        "org_id": "org-1",
        "job_id": str(ObjectId()),
        "batch_id": str(ObjectId()),
        "candidate_id": "cand-1",
        "needs_review": False,
    }


@pytest.mark.asyncio
async def test_process_parse_skips_when_already_parsed_and_matched(monkeypatch) -> None:
    """Recovered parse task must not re-run Docling or re-enqueue match."""
    resume_id = str(ObjectId())
    resume_doc = {
        "_id": ObjectId(resume_id),
        "org_id": "org-1",
        "candidate_id": "cand-1",
        "parse": {
            "status": "parsed",
            "resume": {"basics": {"name": "A"}},
            "needs_review": False,
        },
    }
    db = MagicMock()
    db.resumes = MagicMock()
    db.resumes.find_one = AsyncMock(return_value=resume_doc)
    db.resumes.update_one = AsyncMock()
    db.match_results = MagicMock()
    db.match_results.find_one = AsyncMock(return_value={"_id": ObjectId()})
    db.ingest_batches = MagicMock()
    db.ingest_batches.find_one = AsyncMock(return_value=None)
    db.ingest_batches.update_one = AsyncMock()

    parse_bytes = MagicMock()
    enqueue = MagicMock()
    monkeypatch.setattr(pipeline, "get_db", lambda: db)
    monkeypatch.setattr(pipeline, "parse_resume_bytes", parse_bytes)
    monkeypatch.setattr(pipeline, "enqueue", enqueue)
    monkeypatch.setattr(pipeline, "_maybe_finish_batch", AsyncMock())

    await pipeline.process_parse_task(_payload(resume_id=resume_id), converter=object())

    parse_bytes.assert_not_called()
    enqueue.assert_not_called()
    db.resumes.update_one.assert_not_awaited()
    db.ingest_batches.update_one.assert_not_awaited()


@pytest.mark.asyncio
async def test_process_parse_enqueues_match_when_parsed_but_unmatched(monkeypatch) -> None:
    """Already-parsed resume without a match should only enqueue match."""
    resume_id = str(ObjectId())
    payload = _payload(resume_id=resume_id)
    resume_doc = {
        "_id": ObjectId(resume_id),
        "org_id": "org-1",
        "candidate_id": "cand-1",
        "parse": {
            "status": "parsed",
            "resume": {"basics": {"name": "A"}},
            "needs_review": True,
        },
    }
    db = MagicMock()
    db.resumes = MagicMock()
    db.resumes.find_one = AsyncMock(return_value=resume_doc)
    db.match_results = MagicMock()
    db.match_results.find_one = AsyncMock(return_value=None)

    enqueue = MagicMock()
    monkeypatch.setattr(pipeline, "get_db", lambda: db)
    monkeypatch.setattr(pipeline, "parse_resume_bytes", MagicMock())
    monkeypatch.setattr(pipeline, "enqueue", enqueue)

    await pipeline.process_parse_task(payload, converter=object())

    pipeline.parse_resume_bytes.assert_not_called()
    enqueue.assert_called_once()
    args, _kwargs = enqueue.call_args
    assert args[1]["resume_id"] == resume_id
    assert args[1]["needs_review"] is True
    assert args[1]["candidate_id"] == "cand-1"


@pytest.mark.asyncio
async def test_process_match_skips_when_current_result_exists(monkeypatch) -> None:
    """Recovered match task must not re-run matcher when a current result exists."""
    resume_id = str(ObjectId())
    job_id = str(ObjectId())
    batch_id = str(ObjectId())
    payload = {
        "resume_id": resume_id,
        "org_id": "org-1",
        "job_id": job_id,
        "batch_id": batch_id,
        "candidate_id": "cand-1",
        "needs_review": False,
    }
    db = MagicMock()
    db.jobs = MagicMock()
    db.jobs.find_one = AsyncMock(
        return_value={"_id": ObjectId(job_id), "org_id": "org-1", "jd": {"job_title": "Eng"}}
    )
    db.resumes = MagicMock()
    db.resumes.find_one = AsyncMock(
        return_value={
            "_id": ObjectId(resume_id),
            "org_id": "org-1",
            "parse": {"resume": {"basics": {"name": "A"}}},
        }
    )
    db.match_results = MagicMock()
    db.match_results.find_one = AsyncMock(return_value={"_id": ObjectId()})
    db.ingest_batches = MagicMock()
    db.ingest_batches.update_one = AsyncMock()

    match_fn = MagicMock()
    monkeypatch.setattr(pipeline, "get_db", lambda: db)
    monkeypatch.setattr(pipeline, "match_jd_resume", match_fn)
    monkeypatch.setattr(pipeline, "_maybe_finish_batch", AsyncMock())

    await pipeline.process_match_task(payload)

    match_fn.assert_not_called()
    db.ingest_batches.update_one.assert_not_awaited()
    pipeline._maybe_finish_batch.assert_awaited_once_with(batch_id)


@pytest.mark.asyncio
async def test_ingest_drive_skips_completed_batch(monkeypatch) -> None:
    """Completed Drive ingest batches must not re-list the folder."""
    batch_id = str(ObjectId())
    db = MagicMock()
    db.ingest_batches = MagicMock()
    db.ingest_batches.find_one = AsyncMock(
        return_value={"_id": ObjectId(batch_id), "status": "completed", "counters": {"total": 5}}
    )
    get_token = AsyncMock(return_value="token")
    monkeypatch.setattr(drive_route, "get_db", lambda: db)
    monkeypatch.setattr(drive_route, "get_access_token", get_token)

    count = await drive_route.ingest_drive_folder(
        org_id="org-1",
        user_id="user-1",
        job_id=str(ObjectId()),
        batch_id=batch_id,
        folder_id="folder-1",
    )

    assert count == 0
    get_token.assert_not_awaited()


@pytest.mark.asyncio
async def test_ingest_drive_skips_when_discovery_already_finished(monkeypatch) -> None:
    """Processing batches with counters.total > 0 must not re-discover files."""
    batch_id = str(ObjectId())
    db = MagicMock()
    db.ingest_batches = MagicMock()
    db.ingest_batches.find_one = AsyncMock(
        return_value={"_id": ObjectId(batch_id), "status": "processing", "counters": {"total": 3}}
    )
    get_token = AsyncMock(return_value="token")
    monkeypatch.setattr(drive_route, "get_db", lambda: db)
    monkeypatch.setattr(drive_route, "get_access_token", get_token)

    count = await drive_route.ingest_drive_folder(
        org_id="org-1",
        user_id="user-1",
        job_id=str(ObjectId()),
        batch_id=batch_id,
        folder_id="folder-1",
    )

    assert count == 0
    get_token.assert_not_awaited()


def test_recover_claimed_moves_processing_to_ready() -> None:
    """Startup recovery moves claimed tasks back onto the ready queue."""
    client = MagicMock()
    client.rpoplpush = MagicMock(side_effect=["task-a", "task-b", None])

    with patch("app.queue.get_redis", return_value=client):
        recovered = recover_claimed(QUEUE_PARSE)

    assert recovered == 2
    assert client.rpoplpush.call_count == 3
    client.rpoplpush.assert_any_call(f"{QUEUE_PARSE}:processing", QUEUE_PARSE)
