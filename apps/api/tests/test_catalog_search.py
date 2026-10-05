"""Unit tests for catalog alias search helpers."""

from __future__ import annotations

from app.services.catalog_search import humanize_key, resolve_to_canonical, search_catalog


SAMPLE = {
    "python": ["python", "py", "python3"],
    "javascript": ["javascript", "js", "ecmascript"],
    "machine_learning": ["machine learning", "ml", "deep learning"],
}


def test_humanize_key() -> None:
    assert humanize_key("machine_learning") == "machine learning"


def test_search_by_alias() -> None:
    result = search_catalog(SAMPLE, q="py", limit=10)
    ids = [item["id"] for item in result["items"]]
    assert "python" in ids
    python = next(item for item in result["items"] if item["id"] == "python")
    assert python.get("matched_via") == "py"


def test_search_empty_returns_keys() -> None:
    result = search_catalog(SAMPLE, q=None, limit=10)
    assert result["keys"] == ["javascript", "machine_learning", "python"]
    assert len(result["items"]) == 3


def test_resolve_alias_to_canonical() -> None:
    assert resolve_to_canonical(SAMPLE, "py") == "python"
    assert resolve_to_canonical(SAMPLE, "ML") == "machine_learning"
    assert resolve_to_canonical(SAMPLE, "custom-thing") == "custom-thing"
