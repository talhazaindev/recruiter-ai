"""Hybrid matcher adapter — delegates to services.matcher."""

from __future__ import annotations

from app.models.schemas import JobDescriptionSchema, MatchOutput, MatchingResumeSchema


def match_jd_resume(jd: JobDescriptionSchema, resume: MatchingResumeSchema) -> MatchOutput:
    """Score a resume against a JD via the matcher service package."""
    from services.matcher import match_jd_resume as external_match

    result = external_match(jd, resume)
    if isinstance(result, MatchOutput):
        return result
    return MatchOutput.model_validate(result)
