"""Tests for manual JD rematch behavior."""

from __future__ import annotations

from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from bson import ObjectId
from fastapi import HTTPException

from app.models.schemas import JobDescriptionSchema, JobUpdate, UserPublic
from app.routes import jobs as jobs_route


@pytest.fixture
def user() -> UserPublic:
    """Authenticated recruiter user."""
    return UserPublic(id="user-1", email="recruiter@example.com", role="admin", org_id="org-1")


@pytest.fixture
def job_doc() -> dict:
    """Stored job with one JD revision."""
    return {
        "_id": ObjectId("674c00000000000000000001"),
        "org_id": "org-1",
        "status": "active",
        "jd": JobDescriptionSchema(job_title="Engineer").model_dump(),
        "jd_schema_version": "jd.v1",
        "jd_revision": 2,
        "created_by": "user-1",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }


def _mock_db(
    *,
    job: dict | None,
    stale_count: int = 1,
    rematch_in_progress: bool = False,
    resumes: list[dict] | None = None,
) -> MagicMock:
    """Build a minimal async Mongo mock for job routes."""
    db = MagicMock()
    db.jobs = MagicMock()
    db.jobs.find_one = AsyncMock(return_value=job)
    db.jobs.update_one = AsyncMock()
    db.jobs.insert_one = AsyncMock(return_value=SimpleNamespace(inserted_id=ObjectId()))

    db.match_results = MagicMock()
    db.match_results.update_many = AsyncMock()
    db.match_results.distinct = AsyncMock(return_value=["candidate-1"])

    async def _aggregate(_pipeline):
        if stale_count > 0:
            yield {"candidate_id": "candidate-1", "jd_revision": 1, "stale": True}

    db.match_results.aggregate = MagicMock(return_value=_aggregate([]))

    active_batch = {"_id": ObjectId()} if rematch_in_progress else None
    db.ingest_batches = MagicMock()
    db.ingest_batches.find_one = AsyncMock(return_value=active_batch)
    db.ingest_batches.insert_one = AsyncMock(
        return_value=SimpleNamespace(inserted_id=ObjectId("674c00000000000000000099"))
    )

    async def _resume_aggregate(_pipeline):
        for resume in resumes or []:
            yield {"resume": resume}

    db.resumes = MagicMock()
    db.resumes.aggregate = MagicMock(return_value=_resume_aggregate([]))
    return db


@pytest.mark.asyncio
async def test_update_job_marks_stale_without_enqueue(user: UserPublic, job_doc: dict) -> None:
    """Saving a changed JD marks results stale but does not auto-rematch."""
    db = _mock_db(job=job_doc)
    with (
        patch.object(jobs_route, "get_db", return_value=db),
        patch.object(jobs_route, "write_audit", new=AsyncMock()),
        patch.object(jobs_route, "enqueue_rematch_for_job", new=AsyncMock()) as enqueue_rematch,
    ):
        body = JobUpdate(jd=JobDescriptionSchema(job_title="Senior Engineer"))
        result = await jobs_route.update_job(str(job_doc["_id"]), body, user)

    db.match_results.update_many.assert_awaited_once()
    enqueue_rematch.assert_not_called()
    assert result.jd_revision == 3


@pytest.mark.asyncio
async def test_rematch_job_resets_decisions_and_enqueues(user: UserPublic, job_doc: dict) -> None:
    """Manual rematch resets shortlist/review and enqueues match-only tasks."""
    resume = {
        "_id": ObjectId("674c00000000000000000002"),
        "candidate_id": "candidate-1",
        "batch_id": "batch-old",
        "parse": {"needs_review": False, "resume": {"skills": []}, "status": "ok"},
    }
    db = _mock_db(job=job_doc, stale_count=1, resumes=[resume])
    with (
        patch.object(jobs_route, "get_db", return_value=db),
        patch.object(jobs_route, "write_audit", new=AsyncMock()),
        patch.object(jobs_route, "iter_latest_parsed_resumes", new=AsyncMock(return_value=[resume])),
        patch.object(jobs_route, "enqueue_rematch_for_job", new=AsyncMock(return_value=1)) as enqueue_rematch,
    ):
        response = await jobs_route.rematch_job(str(job_doc["_id"]), user)

    db.match_results.update_many.assert_awaited()
    enqueue_rematch.assert_awaited_once()
    assert response.candidate_count == 1
    assert response.status == "processing"


@pytest.mark.asyncio
async def test_rematch_job_rejects_when_not_stale(user: UserPublic, job_doc: dict) -> None:
    """Manual rematch is blocked when results are already current."""
    db = _mock_db(job=job_doc, stale_count=0)
    with (
        patch.object(jobs_route, "get_db", return_value=db),
        pytest.raises(HTTPException) as exc,
    ):
        await jobs_route.rematch_job(str(job_doc["_id"]), user)

    assert exc.value.status_code == 400
    assert "stale" in str(exc.value.detail).lower()


@pytest.mark.asyncio
async def test_rematch_job_rejects_when_already_running(user: UserPublic, job_doc: dict) -> None:
    """Manual rematch is blocked while another rematch batch is active."""
    db = _mock_db(job=job_doc, stale_count=1, rematch_in_progress=True)
    with (
        patch.object(jobs_route, "get_db", return_value=db),
        pytest.raises(HTTPException) as exc,
    ):
        await jobs_route.rematch_job(str(job_doc["_id"]), user)

    assert exc.value.status_code == 409


@pytest.mark.asyncio
async def test_is_result_stale_helper() -> None:
    """Stale detection covers explicit stale flags and revision drift."""
    assert jobs_route._is_result_stale({"stale": True, "jd_revision": 2}, 2) is True
    assert jobs_route._is_result_stale({"stale": False, "jd_revision": 1}, 2) is True
    assert jobs_route._is_result_stale({"stale": False, "jd_revision": 2}, 2) is False
