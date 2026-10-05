"""Regression tests for title, education, and experience integrity."""

from __future__ import annotations

from must_req.verify_education import education_entry_matches
from must_req.verify_totalexp import calculate_experience_months
from relevant_exp.find_work_exp import is_tech_match, is_title_match, normalize_title


def test_ai_ml_title_preserves_both_role_tokens() -> None:
    """Slash normalization must not reduce the target title to ``ai``."""
    normalized = normalize_title("Associate AI/ML Engineer")
    assert normalized == "ai ml engineer"
    assert is_title_match("Machine Learning Engineer", "Associate AI/ML Engineer")
    assert not is_title_match("Management Trainee", "Associate AI/ML Engineer")


def test_short_technology_aliases_use_boundaries() -> None:
    """Short aliases must not match inside unrelated words."""
    assert is_tech_match("Built production AI systems", "AI")
    assert not is_tech_match("Maintained retail applications", "AI")


def test_education_uses_institution_context_and_optional_completion() -> None:
    """Discipline can be read from the complete education entry."""
    matched, details = education_entry_matches(
        {
            "degree": "Bachelor of Science",
            "institution": "School of Computer Science",
            "graduation_date": "2026",
            "cgpa": "3.5",
        },
        {
            "degree": "bachelor",
            "discipline": "computer science",
            "minimum_cgpa": None,
            "must_be_completed": False,
        },
    )
    assert matched, details


def test_invalid_and_reversed_experience_ranges_are_skipped() -> None:
    """Invalid end dates cannot be interpreted as current employment."""
    months, valid, skipped, _, _ = calculate_experience_months(
        [
            {
                "company": "A",
                "start_date": "2020-01",
                "end_date": "not-a-date",
            },
            {
                "company": "B",
                "start_date": "2024-01",
                "end_date": "2023-01",
            },
        ]
    )
    assert months == 0
    assert valid == 0
    assert skipped == 2
