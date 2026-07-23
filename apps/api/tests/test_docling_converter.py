"""Unit tests for Docling converter factory and eager warm (no real model load)."""

from __future__ import annotations

import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest
from bson import ObjectId


@pytest.fixture(autouse=True)
def _isolate_docling(monkeypatch):
    """Reset singleton and keep settings/env from forcing a missing Docker path."""
    import parser.docling_parser as dp

    monkeypatch.delenv("DOCLING_ARTIFACTS_PATH", raising=False)
    monkeypatch.setenv("DOCLING_DO_OCR", "false")
    monkeypatch.setenv("DOCLING_DO_TABLE_STRUCTURE", "false")
    monkeypatch.setattr(dp, "_settings_docling", lambda: None)
    dp.reset_docling_converter()
    yield
    dp.reset_docling_converter()


def test_build_pdf_pipeline_options_defaults() -> None:
    """Born-digital defaults: OCR and table structure off, no artifacts path."""
    import parser.docling_parser as dp

    opts = dp.build_pdf_pipeline_options()
    assert opts.do_ocr is False
    assert opts.do_table_structure is False
    assert opts.artifacts_path is None


def test_build_pdf_pipeline_options_honors_artifacts_dir(monkeypatch, tmp_path) -> None:
    """Configured artifacts path must exist and be absolute."""
    import parser.docling_parser as dp

    models = tmp_path / "models"
    models.mkdir()
    monkeypatch.setenv("DOCLING_ARTIFACTS_PATH", str(models))
    monkeypatch.setenv("DOCLING_DO_OCR", "true")
    monkeypatch.setenv("DOCLING_DO_TABLE_STRUCTURE", "true")

    opts = dp.build_pdf_pipeline_options()
    assert Path(opts.artifacts_path) == models.resolve()
    assert opts.do_ocr is True
    assert opts.do_table_structure is True


def test_missing_artifacts_path_raises(monkeypatch, tmp_path) -> None:
    """Fail closed when DOCLING_ARTIFACTS_PATH points at a missing directory."""
    import parser.docling_parser as dp

    missing = tmp_path / "does-not-exist"
    monkeypatch.setenv("DOCLING_ARTIFACTS_PATH", str(missing))
    with pytest.raises(FileNotFoundError, match="DOCLING_ARTIFACTS_PATH"):
        dp.build_pdf_pipeline_options()


def test_get_docling_converter_is_singleton(monkeypatch) -> None:
    """One converter instance per process."""
    import parser.docling_parser as dp

    fake = object()
    monkeypatch.setattr(dp, "create_docling_converter", lambda: fake)
    assert dp.get_docling_converter() is fake
    assert dp.get_docling_converter() is fake


def test_initialize_docling_pipeline_warms_once(monkeypatch) -> None:
    """Eager warm calls initialize_pipeline once, then reuses the converter."""
    import parser.docling_parser as dp
    from docling.datamodel.base_models import InputFormat

    calls: list[object] = []

    class FakeConverter:
        def initialize_pipeline(self, fmt: object) -> None:
            calls.append(fmt)

    fake = FakeConverter()
    monkeypatch.setattr(dp, "create_docling_converter", lambda: fake)

    first = dp.initialize_docling_pipeline(warm=True)
    second = dp.initialize_docling_pipeline(warm=True)

    assert first is fake
    assert second is fake
    assert calls == [InputFormat.PDF]


def test_process_parse_task_resolves_converter_when_missing(monkeypatch) -> None:
    """Inline API fallback resolves the shared Docling singleton when converter is None."""
    import parser.docling_parser as dp
    from app.services import pipeline

    calls: list[object] = []
    sentinel = object()

    def fake_get() -> object:
        calls.append(sentinel)
        return sentinel

    monkeypatch.setattr(dp, "get_docling_converter", fake_get)

    resume_id = ObjectId()
    resumes = MagicMock()
    resumes.find_one = AsyncMock(
        return_value={
            "_id": resume_id,
            "org_id": "org",
            "source_ref": {
                "storage_key": "k",
                "original_filename": "r.pdf",
                "content_type": "application/pdf",
            },
            "parse": {"status": "queued", "resume": None},
        }
    )
    resumes.update_one = AsyncMock()
    jobs = MagicMock()
    jobs.find_one = AsyncMock(return_value={"minimum_relevant_years": 0})
    batches = MagicMock()
    batches.find_one = AsyncMock(return_value=None)
    batches.update_one = AsyncMock()
    db = MagicMock()
    db.resumes = resumes
    db.jobs = jobs
    db.ingest_batches = batches
    monkeypatch.setattr(pipeline, "get_db", lambda: db)
    monkeypatch.setattr(pipeline, "get_settings", lambda: MagicMock(parse_confidence_review_threshold=0.5))
    monkeypatch.setattr(pipeline, "download_bytes", MagicMock(side_effect=RuntimeError("stop-before-parse")))
    monkeypatch.setattr(pipeline, "_maybe_finish_batch", AsyncMock())

    asyncio.run(
        pipeline.process_parse_task(
            {
                "resume_id": str(resume_id),
                "org_id": "org",
                "job_id": str(ObjectId()),
                "batch_id": str(ObjectId()),
            },
            converter=None,
        )
    )

    assert calls == [sentinel]
    resumes.find_one.assert_awaited()
