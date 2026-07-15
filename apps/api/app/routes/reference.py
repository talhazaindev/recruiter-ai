"""Reference data for JD curation (skills / education dropdowns)."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.models.schemas import UserPublic

router = APIRouter(tags=["reference"])


def _ensure_ats_agent_on_path() -> None:
    """Import skills_db / education_db from ats-agent."""
    root = Path(__file__).resolve().parents[4]
    ats = root / "ats-agent"
    for p in (str(ats), str(root)):
        if p not in sys.path:
            sys.path.insert(0, p)


@router.get("/v1/reference/skills")
async def list_skills(_user: UserPublic = Depends(get_current_user)) -> dict[str, Any]:
    """Canonical skill keys from ats-agent skills_db."""
    _ensure_ats_agent_on_path()
    from must_req.skills_db import get_all_skills

    skills = sorted(get_all_skills(), key=str.lower)
    return {"skills": skills}


@router.get("/v1/reference/degrees")
async def list_degrees(_user: UserPublic = Depends(get_current_user)) -> dict[str, Any]:
    """Degree level keys from education_db."""
    _ensure_ats_agent_on_path()
    from must_req.education_db import DEGREE_ALIASES, DEGREE_LEVELS

    degrees = sorted(DEGREE_LEVELS.keys(), key=lambda d: DEGREE_LEVELS[d])
    aliases = {k: DEGREE_ALIASES.get(k, []) for k in degrees}
    return {"degrees": degrees, "aliases": aliases}


@router.get("/v1/reference/disciplines")
async def list_disciplines(_user: UserPublic = Depends(get_current_user)) -> dict[str, Any]:
    """Discipline keys from education_db."""
    _ensure_ats_agent_on_path()
    from must_req.education_db import ALL_DISCIPLINES, DISCIPLINE_ALIASES

    disciplines = sorted(ALL_DISCIPLINES, key=str.lower)
    aliases = {k: DISCIPLINE_ALIASES.get(k, []) for k in disciplines}
    return {"disciplines": disciplines, "aliases": aliases}
