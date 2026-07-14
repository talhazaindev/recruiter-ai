"""Teammate hybrid matcher package — stable `match_jd_resume` contract."""

from __future__ import annotations

from typing import Any

from services.matcher.stub import stub_match


def match_jd_resume(jd: Any, resume: Any) -> Any:
    """Public matcher entrypoint used by API workers.

    Replace `stub_match` with the real hybrid pipeline when ready.
    """
    return stub_match(jd, resume)
