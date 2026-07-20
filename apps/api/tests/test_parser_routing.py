"""Regression tests for the custom/Docling routing contract."""

from __future__ import annotations

import sys
import types

import pytest

from app.services import parser_adapter


@pytest.fixture(autouse=True)
def _settings(monkeypatch):
    """Keep routing tests deterministic and offline."""
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.setattr(
        parser_adapter,
        "get_settings",
        lambda: types.SimpleNamespace(
            groq_api_key="",
            groq_model="test",
            parse_confidence_review_threshold=0.55,
        ),
    )


def _sections(name: str = "Ada Lovelace") -> dict:
    return {
        "name": name,
        "email": "ada@example.com",
        "phone": "+923001234567",
        "raw_text": "Ada Lovelace " + ("machine learning python " * 100),
        "skills": {"content": "Python, Machine Learning"},
        "experience": {
            "Analytical Engines": {
                "content": "Engineer January 2022 Present Python machine learning"
            }
        },
        "education": {"University": {"content": "Bachelor Computer Science 2021"}},
        "projects": {"Engine": {"content": "Machine learning project"}},
    }


def _layout(monkeypatch, classification: str) -> None:
    import parser.layout_detect

    monkeypatch.setattr(
        parser.layout_detect,
        "detect_columns",
        lambda _path: {
            "classification": classification,
            "is_multicolumn": classification == "multi",
            "max_columns": 2 if classification == "multi" else 1,
            "pages": [],
            "failures": [],
        },
    )


def test_single_column_never_calls_docling(monkeypatch) -> None:
    """Weak or strong single-column output remains custom-only."""
    _layout(monkeypatch, "single")
    monkeypatch.setattr(parser_adapter, "_run_parse_cv", lambda _path: _sections())
    fake_docling = types.ModuleType("parser.docling_parser")

    def forbidden(_path: str) -> dict:
        raise AssertionError("Docling must not run for a single-column resume")

    fake_docling.parse_cv_docling = forbidden  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "parser.docling_parser", fake_docling)

    result = parser_adapter.parse_resume_bytes(b"%PDF fixture", "resume.pdf")

    assert result.provenance["selected_parser"] == "custom.pymupdf"
    assert result.provenance["layout_classification"] == "single"


def test_unknown_layout_is_custom_only_and_reviewed(monkeypatch) -> None:
    """Unknown layout uses custom output and requires review."""
    _layout(monkeypatch, "unknown")
    monkeypatch.setattr(parser_adapter, "_run_parse_cv", lambda _path: _sections())

    result = parser_adapter.parse_resume_bytes(b"%PDF fixture", "resume.pdf")

    assert result.provenance["selected_parser"] == "custom.pymupdf"
    assert result.needs_review is True
    assert "layout_unknown_custom_only" in result.warnings


def test_multi_column_uses_docling(monkeypatch) -> None:
    """Positive multi-column evidence makes Docling eligible."""
    _layout(monkeypatch, "multi")
    fake_docling = types.ModuleType("parser.docling_parser")
    fake_docling.parse_cv_docling = lambda _path: _sections()  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "parser.docling_parser", fake_docling)
    monkeypatch.setattr(
        parser_adapter,
        "_run_parse_cv",
        lambda _path: (_ for _ in ()).throw(AssertionError("unnecessary custom fallback")),
    )

    result = parser_adapter.parse_resume_bytes(b"%PDF fixture", "resume.pdf")

    assert result.provenance["selected_parser"] == "docling"
    assert result.provenance["layout_classification"] == "multi"


def test_malformed_name_requires_review(monkeypatch) -> None:
    """Section headings cannot silently become trusted candidate names."""
    _layout(monkeypatch, "single")
    monkeypatch.setattr(
        parser_adapter, "_run_parse_cv", lambda _path: _sections("WORK EXPERIENCE")
    )

    result = parser_adapter.parse_resume_bytes(b"%PDF fixture", "resume.pdf")

    assert "candidate_name_invalid_or_missing" in result.warnings
    assert result.needs_review is True
