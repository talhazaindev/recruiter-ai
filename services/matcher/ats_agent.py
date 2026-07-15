"""Real ats-agent matcher — must-have verify + relevant experience scoring."""

from __future__ import annotations

import contextlib
import io
import logging
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def _ensure_ats_agent_on_path() -> Path:
    """Add ats-agent dir to sys.path so must_req / relevant_exp / tech_aliases_db import."""
    # services/matcher/ats_agent.py → parents[2] = repo root
    root = Path(__file__).resolve().parents[2]
    ats = root / "ats-agent"
    for p in (str(ats), str(root)):
        if p not in sys.path:
            sys.path.insert(0, p)
    return ats


def _to_dict(obj: Any) -> dict[str, Any]:
    """Normalize pydantic model or dict to plain dict."""
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    return dict(obj)


def match_jd_resume(jd: Any, resume: Any) -> dict[str, Any]:
    """Run ats-agent verification and rank by relevant experience."""
    _ensure_ats_agent_on_path()

    from must_req.verify import verify_candidate
    from relevant_exp.find_project_exp import find_relevant_project_experience
    from relevant_exp.find_work_exp import find_relevant_experience

    jd_data = _to_dict(jd)
    resume_data = _to_dict(resume)

    # Ensure raw text is present for skill scanning
    if not resume_data.get("raw_resume_text"):
        parts = [
            resume_data.get("professional_summary") or "",
            " ".join(resume_data.get("skills") or []),
        ]
        for exp in resume_data.get("experience") or []:
            if isinstance(exp, dict):
                parts.append(str(exp.get("description") or ""))
                parts.append(str(exp.get("company") or ""))
                parts.append(str(exp.get("designation") or ""))
        resume_data["raw_resume_text"] = "\n".join(p for p in parts if p)

    passed, details = verify_candidate(resume_data, jd_data, return_details=True)
    details = details or {}
    failed_rules: list[str] = list(details.get("failed_checks") or [])
    if details.get("failure_reason"):
        failed_rules = failed_rules or [str(details["failure_reason"])]

    work_years = 0.0
    gap_found = False
    gaps: list[Any] = []
    project_result: dict[str, Any] = {}

    # ats-agent modules print emoji diagnostics; redirect to avoid Windows charmap errors
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            work_years, gap_found, gaps = find_relevant_experience(jd_data, resume_data)
    except Exception as exc:
        logger.warning("find_relevant_experience failed: %s", exc)

    try:
        with contextlib.redirect_stdout(io.StringIO()):
            project_result = find_relevant_project_experience(jd_data, resume_data) or {}
    except Exception as exc:
        logger.warning("find_relevant_project_experience failed: %s", exc)

    project_years = float(project_result.get("total_project_years") or 0.0)
    if "total_project_years" not in project_result:
        # Fall back to count of relevant projects as a weak signal
        relevant_projects = project_result.get("relevant_projects") or []
        project_years = float(len(relevant_projects)) * 0.25

    skills_details = (details.get("skills") or {}).get("details") or {}
    found_skills = list(skills_details.get("found_skills") or [])
    missing_skills = list(skills_details.get("missing_skills") or [])

    # Score: hard-filter pass bonus + relevant years + project signal + skill coverage
    required = list(skills_details.get("required_skills") or [])
    skill_ratio = (len(found_skills) / max(len(required), 1)) if required else 0.5
    base = skill_ratio * 50.0
    year_signal = min(30.0, float(work_years) * 4.0)
    project_signal = min(10.0, project_years * 5.0)
    pass_bonus = 20.0 if passed else 0.0
    score = round(min(100.0, base + year_signal + project_signal + pass_bonus), 1)
    if not passed:
        score = min(score, 45.0)

    summary = (
        "Passed must-have filters; ranked by relevant work/project experience."
        if passed
        else (details.get("failure_reason") or "Failed one or more must-have filters.")
    )

    return {
        "hard_filters": {"passed": bool(passed), "failed_rules": failed_rules},
        "score": score,
        "rank_signals": {
            "relevant_work_years": work_years,
            "relevant_project_years": project_years,
            "gap_found": gap_found,
            "gaps": gaps[:5] if isinstance(gaps, list) else [],
            "found_skills": found_skills,
            "missing_skills": missing_skills,
            "relevant_projects": len(project_result.get("relevant_projects") or []),
        },
        "explanation": {
            "summary": summary,
            "matched_skills": found_skills,
            "failed_rules": failed_rules,
            "verification": {
                "education": (details.get("education") or {}).get("message"),
                "skills": (details.get("skills") or {}).get("message"),
                "experience": (details.get("experience") or {}).get("message"),
            },
        },
        "matcher_version": "ats-agent.v1",
    }
