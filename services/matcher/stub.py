"""Deterministic hybrid stub matcher (replaced by teammate pipeline later)."""

from __future__ import annotations

import re
from typing import Any

# Common tech tokens extracted from long JD prose pasted into "skills"
_TECH_TOKEN_RE = re.compile(
    r"\b(python|fastapi|django|flask|langchain|langgraph|llm|llms|rag|"
    r"postgres|postgresql|pgvector|mongodb|redis|docker|kubernetes|ci/?cd|"
    r"react|typescript|javascript|aws|azure|gcp|pytorch|tensorflow|"
    r"vector|agent(?:ic)?|api|devops|sql|nosql|ml|nlp)\b",
    re.IGNORECASE,
)


def _normalize_skill_requirements(raw_skills: list[str]) -> list[str]:
    """Turn JD skill entries into matchable tokens.

    Short entries (e.g. \"Python\") stay as-is. Long prose bullets are reduced
    to known tech tokens so stub hard-filters stay usable before real matching lands.
    """
    out: list[str] = []
    seen: set[str] = set()
    for skill in raw_skills:
        text = (skill or "").strip()
        if not text:
            continue
        if len(text) <= 40:
            key = text.lower()
            if key not in seen:
                seen.add(key)
                out.append(key)
            continue
        for match in _TECH_TOKEN_RE.findall(text):
            key = match.lower().replace("ci/cd", "ci/cd")
            if key not in seen:
                seen.add(key)
                out.append(key)
    return out


def _skill_present(required: str, resume_skills: set[str], haystack: str) -> bool:
    """True if required skill appears in structured skills or raw resume text."""
    req = required.lower()
    if req in resume_skills:
        return True
    if any(req in s or s in req for s in resume_skills):
        return True
    return bool(req) and req in haystack


def stub_match(jd: Any, resume: Any) -> Any:
    """Score JD vs resume with hard filters + skill overlap.

    Accepts Pydantic models or dicts; returns a MatchOutput-like pydantic model
    when `app.models.schemas` is importable, else a plain dict.
    """
    jd_data = jd.model_dump() if hasattr(jd, "model_dump") else dict(jd)
    resume_data = resume.model_dump() if hasattr(resume, "model_dump") else dict(resume)

    must_have = jd_data.get("requirements_must_have") or {}
    must_skills = _normalize_skill_requirements(must_have.get("skills") or [])
    resume_skills = {s.lower() for s in (resume_data.get("skills") or [])}
    haystack = " ".join(
        [
            (resume_data.get("raw_resume_text") or "").lower(),
            (resume_data.get("professional_summary") or "").lower(),
            " ".join(resume_skills),
        ]
    )
    failed: list[str] = []

    missing_skills = [s for s in must_skills if not _skill_present(s, resume_skills, haystack)]
    # Soften: fail only if majority of must tokens missing (stub UX until real matcher)
    if must_skills and len(missing_skills) == len(must_skills):
        failed.append(f"missing_must_skills:{','.join(missing_skills[:8])}")
    elif must_skills and len(missing_skills) > max(2, len(must_skills) // 2):
        failed.append(f"missing_must_skills:{','.join(missing_skills[:8])}")

    exp = must_have.get("experience") or {}
    min_years = exp.get("minimum_total_years")
    experience_rows = resume_data.get("experience") or []
    if min_years is not None and min_years > 0:
        estimated = max(len(experience_rows) * 1.5, 1.0 if experience_rows else 0.0)
        # Stub only hard-fails extreme gaps; real matcher will enforce precisely
        if estimated < min_years and (min_years - estimated) >= 5:
            failed.append(f"insufficient_years:have_{estimated}_need_{min_years}")

    edu_req = ((must_have.get("education") or {}).get("degree") or "").lower()
    education = resume_data.get("education") or []
    if edu_req and not education:
        failed.append(f"missing_education:{edu_req}")

    passed = len(failed) == 0
    preferred = _normalize_skill_requirements(
        list(jd_data.get("preferred_skills") or [])
        + list(jd_data.get("tech_stack") or [])
        + list(jd_data.get("keywords") or [])
    )
    nice = _normalize_skill_requirements(list((jd_data.get("nice_to_have") or {}).get("skills") or []))
    all_wanted = set(preferred) | set(nice) | set(must_skills)
    overlap = {s for s in all_wanted if _skill_present(s, resume_skills, haystack)} if all_wanted else resume_skills
    base = (len(overlap) / max(len(all_wanted), 1)) * 70 if all_wanted else 40.0
    bonus = 20.0 if passed else 0.0
    year_signal = min(10.0, len(experience_rows) * 3.0)
    score = round(min(100.0, base + bonus + year_signal), 1)
    if not passed:
        score = min(score, 45.0)

    payload = {
        "hard_filters": {"passed": passed, "failed_rules": failed},
        "score": score,
        "rank_signals": {
            "skill_overlap": sorted(overlap),
            "must_skills_matched": sorted(set(must_skills) - set(missing_skills)),
            "experience_rows": len(experience_rows),
        },
        "explanation": {
            "summary": (
                "Passed must-have filters and ranked by skill/tech overlap."
                if passed
                else "Failed one or more must-have filters; ranked below best-fit."
            ),
            "matched_skills": sorted(overlap),
            "failed_rules": failed,
        },
        "matcher_version": "hybrid.v1-stub",
    }

    try:
        from app.models.schemas import MatchOutput

        return MatchOutput.model_validate(payload)
    except Exception:
        return payload
