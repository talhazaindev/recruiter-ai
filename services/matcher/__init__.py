"""Hybrid matcher package — ats-agent verification + ranking."""

from __future__ import annotations

from typing import Any

from services.matcher.ats_agent import match_jd_resume as ats_match


def match_jd_resume(jd: Any, resume: Any) -> Any:
    """Public matcher entrypoint used by API workers."""
    payload = ats_match(jd, resume)
    try:
        from app.models.schemas import MatchOutput

        return MatchOutput.model_validate(payload)
    except Exception:
        return payload
