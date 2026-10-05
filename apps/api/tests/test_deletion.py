"""Tests for CV and candidate cascade deletion."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from bson import ObjectId

from app.services import deletion


def _delete_result(count: int = 1) -> SimpleNamespace:
    """Build a Mongo-like deletion result."""
    return SimpleNamespace(deleted_count=count)


@pytest.mark.asyncio
async def test_delete_resume_removes_orphaned_candidate() -> None:
    """Deleting a candidate's final CV also removes their orphaned identity."""
    candidate_id = "674c00000000000000000010"
    resume = {
        "_id": ObjectId("674c00000000000000000011"),
        "org_id": "org-1",
        "job_id": "674c00000000000000000012",
        "candidate_id": candidate_id,
        "source_ref": {"storage_key": "org-1/job-1/cv.pdf"},
    }
    db = MagicMock()
    db.match_results.delete_many = AsyncMock(return_value=_delete_result())
    db.match_results.find_one = AsyncMock(side_effect=[None, None])
    db.resumes.delete_one = AsyncMock(return_value=_delete_result())
    db.resumes.find_one = AsyncMock(side_effect=[None, None])
    db.candidates.update_one = AsyncMock()
    db.candidates.delete_one = AsyncMock(return_value=_delete_result())
    db.screening_calls.delete_many = AsyncMock(return_value=_delete_result())

    with patch.object(deletion, "_delete_stored_file", new=AsyncMock()) as remove_file:
        counts = await deletion.delete_resume(db, "org-1", resume)

    remove_file.assert_awaited_once_with("org-1/job-1/cv.pdf")
    db.candidates.delete_one.assert_awaited_once()
    assert counts == {"resumes": 1, "match_results": 1}


@pytest.mark.asyncio
async def test_delete_candidate_from_job_preserves_other_job_identity() -> None:
    """Deleting from one job keeps a candidate referenced by another job."""
    candidate_id = "674c00000000000000000020"
    resume = {
        "_id": ObjectId("674c00000000000000000021"),
        "candidate_id": candidate_id,
        "source_ref": {"storage_key": "org-1/job-1/cv.pdf"},
    }
    cursor = MagicMock()
    cursor.to_list = AsyncMock(return_value=[resume])
    db = MagicMock()
    db.resumes.find = MagicMock(return_value=cursor)
    db.resumes.delete_many = AsyncMock(return_value=_delete_result())
    db.resumes.find_one = AsyncMock(return_value={"_id": ObjectId()})
    db.match_results.delete_many = AsyncMock(return_value=_delete_result(2))
    db.match_results.find_one = AsyncMock()
    db.candidates.update_one = AsyncMock()
    db.candidates.delete_one = AsyncMock()
    db.screening_calls.delete_many = AsyncMock()

    with patch.object(deletion, "_delete_stored_file", new=AsyncMock()):
        counts = await deletion.delete_candidate_from_job(
            db,
            "org-1",
            "674c00000000000000000022",
            candidate_id,
        )

    db.candidates.update_one.assert_awaited_once()
    db.candidates.delete_one.assert_not_awaited()
    assert counts == {"resumes": 1, "match_results": 2}
