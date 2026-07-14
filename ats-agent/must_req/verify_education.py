"""
Simple education checker for JD and resume JSON files.

This file checks whether one education entry in a resume matches the JD
education requirement.

Public API:
- verify_education_criteria(resume, jd) -> bool
- verify_education_criteria(resume, jd, return_details=True) -> (bool, dict)
- check_education(resume, jd) -> backwards-compatible alias
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Import education database
from .education_db import (
    DEGREE_LEVELS,
    DEGREE_ALIASES,
    DISCIPLINE_ALIASES,
    IT_RELATED_DISCIPLINES,
    BUSINESS_RELATED_DISCIPLINES,
)


# ============================================================
# File helpers
# ============================================================

def load_json(file_path: str | Path) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_text(value: Any) -> str:
    """Lowercase text and replace punctuation with spaces."""
    if value is None:
        return ""
    text = str(value).lower().strip()
    text = text.replace("&", " and ")
    text = re.sub(r"[\/_\-.,()\[\]{}:;|\\]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def compact_alnum(value: Any) -> str:
    """Lowercase and keep only letters/numbers (for forms like BSCS)."""
    if value is None:
        return ""
    return re.sub(r"[^a-z0-9]", "", str(value).lower())


def word_match(text: str, phrase: str) -> bool:
    """Return True if phrase appears as a whole word/phrase in text."""
    if not text or not phrase:
        return False
    pattern = r"\b" + re.escape(normalize_text(phrase)) + r"\b"
    return re.search(pattern, text) is not None


# ============================================================
# Degree and discipline matching (using education_db)
# ============================================================

def find_degree_level(text: Any) -> Optional[str]:
    """Return the canonical degree level found in text."""
    normalized = normalize_text(text)
    if not normalized:
        return None

    # Higher degrees first.
    order = ["phd", "professional_degree", "master", "graduate_diploma", 
             "graduate_certificate", "bachelor", "associate", "diploma", "certificate"]
    for level in order:
        for alias in DEGREE_ALIASES.get(level, []):
            if word_match(normalized, alias):
                return level

    # Fallback for compact forms like BSCS, MSCS, BTECHAI
    compact = compact_alnum(text)
    if compact:
        compact_aliases = {}
        for level in order:
            aliases = DEGREE_ALIASES.get(level, [])
            compact_aliases[level] = sorted(
                {compact_alnum(a) for a in aliases if compact_alnum(a)},
                key=len,
                reverse=True,
            )

        for level in order:
            for alias in compact_aliases[level]:
                if compact.startswith(alias):
                    return level
    return None


def find_discipline(text: Any) -> Optional[str]:
    """Return the canonical discipline found in text."""
    normalized = normalize_text(text)
    if not normalized:
        return None

    for discipline, aliases in DISCIPLINE_ALIASES.items():
        for alias in aliases:
            if word_match(normalized, alias):
                return discipline

    # Fallback for compact forms like BSCS / MSCS / BSEE.
    compact = compact_alnum(text)
    if not compact:
        return None

    # Build compact discipline alias map once per call (small dict, simple and clear).
    compact_discipline_aliases: Dict[str, List[str]] = {}
    for discipline, aliases in DISCIPLINE_ALIASES.items():
        compact_discipline_aliases[discipline] = sorted(
            {compact_alnum(a) for a in aliases if compact_alnum(a)},
            key=len,
            reverse=True,
        )

    # 1) Direct compact contains check.
    for discipline, aliases in compact_discipline_aliases.items():
        for alias in aliases:
            if alias and alias in compact:
                return discipline

    # 2) Strip a degree prefix (bs/ms/phd/...) then check remainder.
    degree_prefixes: List[str] = []
    for aliases in DEGREE_ALIASES.values():
        degree_prefixes.extend([compact_alnum(a) for a in aliases if compact_alnum(a)])
    degree_prefixes = sorted(set(degree_prefixes), key=len, reverse=True)

    for prefix in degree_prefixes:
        if compact.startswith(prefix) and len(compact) > len(prefix):
            remainder = compact[len(prefix):]
            for discipline, aliases in compact_discipline_aliases.items():
                for alias in aliases:
                    if alias and (remainder == alias or remainder.startswith(alias) or remainder.endswith(alias)):
                        return discipline

    return None


def parse_cgpa(value: Any) -> Optional[float]:
    """Extract the first number from a CGPA field."""
    if value is None:
        return None
    match = re.search(r"\d+(?:\.\d+)?", str(value))
    return float(match.group(0)) if match else None


def parse_graduation_date(value: Any) -> Optional[datetime]:
    """Parse common graduation date formats."""
    if value is None:
        return None

    text = str(value).strip().lower()
    text = text.replace("graduated", "").replace("graduation", "").strip()

    formats = [
        "%Y-%m",
        "%Y/%m",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%b %Y",
        "%B %Y",
        "%b %d %Y",
        "%B %d %Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    return None


# ============================================================
# Requirement checks
# ============================================================

def degree_meets_requirement(candidate_degree: Optional[str], required_degree: Optional[str]) -> bool:
    if required_degree is None:
        return True
    if candidate_degree is None:
        return False

    candidate_rank = DEGREE_LEVELS.get(candidate_degree)
    required_rank = DEGREE_LEVELS.get(required_degree)
    if candidate_rank is None or required_rank is None:
        return candidate_degree == required_degree
    return candidate_rank >= required_rank


def discipline_meets_requirement(candidate_discipline: Optional[str], required_discipline: Optional[str]) -> bool:
    if required_discipline is None:
        return True
    if candidate_discipline is None:
        return False

    # If JD requires IT, allow any IT-related discipline
    if required_discipline == "information technology":
        return candidate_discipline in IT_RELATED_DISCIPLINES
    
    # If JD requires business/management, allow business-related disciplines
    # This is useful for HR and BD roles
    if required_discipline in ["business administration", "management", "human resources"]:
        return candidate_discipline in BUSINESS_RELATED_DISCIPLINES or candidate_discipline == required_discipline

    return candidate_discipline == required_discipline


def completion_meets_requirement(graduation_date: Any, must_be_completed: Optional[bool]) -> bool:
    if must_be_completed is None:
        return True

    parsed_date = parse_graduation_date(graduation_date)
    if parsed_date is None:
        # If we require completion but cannot parse the date, fail.
        return False if must_be_completed else True

    is_completed = parsed_date <= datetime.today()
    return is_completed == must_be_completed


def education_entry_matches(entry: dict, edu_req: dict) -> Tuple[bool, Dict[str, Any]]:
    """Check one education entry against the JD education requirement."""
    required_degree = find_degree_level(edu_req.get("degree"))
    required_discipline = find_discipline(edu_req.get("discipline"))
    min_cgpa = edu_req.get("minimum_cgpa")
    must_be_completed = edu_req.get("must_be_completed")

    degree_text = entry.get("degree", "")
    candidate_degree = find_degree_level(degree_text)
    candidate_discipline = find_discipline(degree_text)

    degree_ok = degree_meets_requirement(candidate_degree, required_degree)
    discipline_ok = discipline_meets_requirement(candidate_discipline, required_discipline)

    cgpa_ok = True
    if min_cgpa is not None:
        candidate_cgpa = parse_cgpa(entry.get("cgpa"))
        cgpa_ok = candidate_cgpa is not None and candidate_cgpa >= float(min_cgpa)

    completion_ok = completion_meets_requirement(entry.get("graduation_date"), must_be_completed)

    failed_checks = []
    if not degree_ok:
        failed_checks.append("degree")
    if not discipline_ok:
        failed_checks.append("discipline")
    if not cgpa_ok:
        failed_checks.append("minimum_cgpa")
    if not completion_ok:
        failed_checks.append("must_be_completed")

    details = {
        "degree_ok": degree_ok,
        "discipline_ok": discipline_ok,
        "cgpa_ok": cgpa_ok,
        "completion_ok": completion_ok,
        "failed_checks": failed_checks,
        "failure_reason": ", ".join(failed_checks) if failed_checks else "",
        "candidate_degree": candidate_degree,
        "candidate_discipline": candidate_discipline,
        "entry": entry,
    }

    return degree_ok and discipline_ok and cgpa_ok and completion_ok, details


# ============================================================
# Main public function
# ============================================================

def verify_education_criteria(resume: dict, jd: dict, return_details: bool = False):
    """Return True if at least one resume education entry satisfies the JD."""
    edu_req = jd.get("requirements_must_have", {}).get("education", {}) or {}

    # If the JD has no education rules, pass automatically.
    if all(edu_req.get(key) is None for key in ["degree", "discipline", "minimum_cgpa", "must_be_completed"]):
        result = True
        details = {"message": "No education requirements"}
        return (result, details) if return_details else result

    education_list = resume.get("education", []) or []
    if not education_list:
        result = False
        details = {"message": "No education found in resume", "failed_checks": ["education_missing"], "failure_reason": "education_missing"}
        return (result, details) if return_details else result

    last_failure = {"message": "No matching education found", "failed_checks": ["unknown"], "failure_reason": "unknown"}

    for entry in education_list:
        if not isinstance(entry, dict):
            continue

        matched, details = education_entry_matches(entry, edu_req)
        if matched:
            success_details = {
                "message": "Education requirements met",
                "matched_entry": entry,
                "candidate_degree": details["candidate_degree"],
                "candidate_discipline": details["candidate_discipline"],
            }
            return (True, success_details) if return_details else True

        last_failure = {
            "message": "No matching education found",
            "last_checked_entry": entry,
            **details,
        }

    return (False, last_failure) if return_details else False


# Backwards-compatible alias for other scripts.
check_education = verify_education_criteria


# ============================================================
# Simple standalone test
# ============================================================

if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent.parent
    jd_folder = repo_root / "JD-jsons"
    resume_folder = repo_root / "Resumes-jsons"

    jd_files = list(jd_folder.glob("*.json"))
    resume_files = list(resume_folder.glob("*.json"))

    if not jd_files:
        raise SystemExit(f"No JD JSON files found in {jd_folder}")

    jd = load_json(jd_files[0])
    print(f"Using JD: {jd_files[0].name}")

    for resume_file in resume_files:
        resume = load_json(resume_file)
        passed, details = verify_education_criteria(resume, jd, return_details=True)
        if passed:
            print(f"{resume_file.name}: True - {details.get('message')}")
        else:
            print(
                f"{resume_file.name}: False - {details.get('message')} | "
                f"failed_checks={details.get('failed_checks')} | "
                f"reason={details.get('failure_reason')}"
            )