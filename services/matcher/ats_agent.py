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
    from must_req.verify_totalexp import calculate_experience_months
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
    must_have_failed_rules = list(failed_rules)

    work_years = 0.0
    gap_found = False
    gaps: list[Any] = []
    experience_evaluations: list[dict[str, Any]] = []
    project_result: dict[str, Any] = {}

    # ats-agent modules print emoji diagnostics; redirect to avoid Windows charmap errors
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            work_years, gap_found, gaps, experience_evaluations = find_relevant_experience(
                jd_data, resume_data
            )
    except Exception as exc:
        logger.warning("find_relevant_experience failed: %s", exc)

    try:
        with contextlib.redirect_stdout(io.StringIO()):
            project_result = find_relevant_project_experience(jd_data, resume_data) or {}
    except Exception as exc:
        logger.warning("find_relevant_project_experience failed: %s", exc)

    relevant_projects = list(project_result.get("relevant_projects") or [])
    relevant_certifications = list(project_result.get("relevant_certifications") or [])
    project_matches = project_result.get("project_matches") or {}
    certification_matches = project_result.get("certification_matches") or {}
    projects_certificates_count = int(
        project_result.get("relevant_count")
        or len(relevant_projects) + len(relevant_certifications)
    )
    project_years = float(project_result.get("total_project_years") or 0.0)
    if "total_project_years" not in project_result:
        # Fall back to count of relevant projects as a weak scoring signal.
        project_years = float(len(relevant_projects)) * 0.25

    experience_details = (details.get("experience") or {}).get("details") or {}
    total_experience = experience_details.get("total_years")
    if not isinstance(total_experience, (int, float)):
        total_months, _, _, _, _ = calculate_experience_months(
            resume_data.get("experience") or []
        )
        total_experience = total_months / 12
    total_experience = round(float(total_experience or 0.0), 2)
    work_years = round(float(work_years or 0.0), 2)

    minimum_total = (
        (jd_data.get("requirements_must_have") or {})
        .get("experience", {})
        .get("minimum_total_years")
    )
    minimum_relevant = float(jd_data.get("minimum_relevant_years") or 0.0)
    relevant_passed = work_years >= minimum_relevant
    final_passed = bool(passed and relevant_passed)

    if not passed:
        comment = "Failed Requirements"
    elif not relevant_passed:
        comment = "Insufficient Relevant Exp"
        failed_rules.append(
            f"Relevant experience {work_years:.1f}y is below required "
            f"{minimum_relevant:.1f}y"
        )
    elif gap_found:
        comment = "Gap Found"
    elif work_years >= minimum_relevant + 1:
        comment = "Overqualified"
    elif minimum_relevant > 0:
        comment = "Good Candidate"
    else:
        comment = "Qualified"

    skills_details = (details.get("skills") or {}).get("details") or {}
    found_skills = list(skills_details.get("found_skills") or [])
    missing_skills = list(skills_details.get("missing_skills") or [])

    # Score: hard-filter pass bonus + relevant years + project signal + skill coverage
    required = list(skills_details.get("required_skills") or [])
    skill_ratio = (len(found_skills) / max(len(required), 1)) if required else 0.5
    base = skill_ratio * 45.0
    year_signal = min(30.0, float(work_years) * 4.0)
    project_signal = min(10.0, project_years * 5.0)
    has_relevance_evidence = work_years > 0 or bool(relevant_projects)
    pass_bonus = 15.0 if final_passed and has_relevance_evidence else 0.0
    score = round(min(100.0, base + year_signal + project_signal + pass_bonus), 1)
    if not final_passed:
        score = min(score, 45.0)
    elif not has_relevance_evidence:
        score = min(score, 55.0)

    summary = (
        "Passed all requirements; ranked by relevant work/project experience."
        if final_passed
        else (
            details.get("failure_reason")
            or (failed_rules[-1] if failed_rules else "Failed one or more requirements.")
        )
    )

    failed_requirements = [
        {"requirement": rule, "status": "Failed", "reason": rule}
        for rule in failed_rules
    ]
    assessment_details = {
        "passed": final_passed,
        "final_status": "Pass" if final_passed else "Fail",
        "final_comment": comment,
        "failed_requirements": failed_requirements,
        "steps": [
            {
                "step": 1,
                "title": "Must-Have Requirements Verification",
                "status": "passed" if passed else "failed",
                "summary": details.get("summary") or [],
                "failed_requirements": [
                    {"requirement": rule, "status": "Failed", "reason": rule}
                    for rule in must_have_failed_rules
                ],
            },
            {
                "step": 2,
                "title": "Total Experience Check",
                "status": "passed" if (details.get("experience") or {}).get("passed") else "failed",
                "total_experience": total_experience,
                "minimum_required": minimum_total,
                "message": (details.get("experience") or {}).get("message") or "",
            },
            {
                "step": 3,
                "title": "Relevant Work Experience Analysis",
                "status": "passed" if relevant_passed else "failed",
                "relevant_experience": work_years,
                "minimum_required": minimum_relevant,
                "gap_found": gap_found,
                "gaps": gaps if isinstance(gaps, list) else [],
                "experience_evaluations": experience_evaluations,
            },
            {
                "step": 4,
                "title": "Projects & Certifications Analysis",
                "status": "completed",
                "projects_certificates_count": projects_certificates_count,
                "relevant_projects": relevant_projects,
                "relevant_certifications": relevant_certifications,
                "project_matches": project_matches,
                "certification_matches": certification_matches,
                "total_projects_checked": project_result.get("total_projects_checked"),
                "total_certifications_checked": project_result.get(
                    "total_certifications_checked"
                ),
                "invalid_projects": project_result.get("invalid_projects") or [],
                "invalid_certifications": project_result.get("invalid_certifications")
                or [],
            },
            {
                "step": 5,
                "title": "Final Assessment",
                "status": "completed",
                "comment": comment,
                "overall_status": "Pass" if final_passed else "Fail",
                "failed_requirements": failed_requirements,
            },
        ],
    }

    return {
        "hard_filters": {"passed": final_passed, "failed_rules": failed_rules},
        "score": score,
        "rank_signals": {
            "relevant_work_years": work_years,
            "total_experience_years": total_experience,
            "relevant_project_years": project_years,
            "projects_certificates_count": projects_certificates_count,
            "gap_found": gap_found,
            "gaps": gaps[:5] if isinstance(gaps, list) else [],
            "found_skills": found_skills,
            "missing_skills": missing_skills,
            "relevant_projects": len(relevant_projects),
            "relevant_certifications": len(relevant_certifications),
            "experience_evaluations": experience_evaluations,
            "project_matches": project_matches,
            "certification_matches": certification_matches,
            "status": "Pass" if final_passed else "Fail",
            "comment": comment,
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
            "details": assessment_details,
            
        },
        "matcher_version": "ats-agent.v3",
    }
