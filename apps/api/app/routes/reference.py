"""Reference data for JD curation (skills / tech / education dropdowns)."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, Query

from app.auth import get_current_user
from app.models.schemas import UserPublic
from app.services.catalog_search import search_catalog

router = APIRouter(tags=["reference"])


def _ensure_ats_agent_on_path() -> None:
    """Import skills_db / education_db / tech_aliases_db from ats-agent."""
    root = Path(__file__).resolve().parents[4]
    ats = root / "ats-agent"
    for p in (str(ats), str(root)):
        if p not in sys.path:
            sys.path.insert(0, p)


@router.get("/v1/reference/skills")
async def list_skills(
    _user: UserPublic = Depends(get_current_user),
    q: str | None = Query(default=None, description="Optional search over keys and aliases"),
    limit: int = Query(default=40, ge=1, le=100),
) -> dict[str, Any]:
    """Canonical skill keys from ats-agent skills_db, with optional alias search."""
    _ensure_ats_agent_on_path()
    from must_req.skills_db import COMMON_VARIATIONS

    result = search_catalog(COMMON_VARIATIONS, q=q, limit=limit)
    return {
        "skills": result["keys"],
        "aliases": result["aliases"],
        "items": result["items"],
    }


@router.get("/v1/reference/tech-stack")
async def list_tech_stack(
    _user: UserPublic = Depends(get_current_user),
    q: str | None = Query(default=None, description="Optional search over keys and aliases"),
    limit: int = Query(default=40, ge=1, le=100),
) -> dict[str, Any]:
    """Tech stack keys from tech_aliases_db, including compound stacks."""
    _ensure_ats_agent_on_path()
    from tech_aliases_db import COMPOUND_TECH_ALIASES, TECH_STACK_ALIASES

    catalog: dict[str, list[str]] = {
        **{k: list(v) for k, v in TECH_STACK_ALIASES.items()},
        **{k: list(v) for k, v in COMPOUND_TECH_ALIASES.items()},
    }
    kind_by_id = {k: "tech" for k in TECH_STACK_ALIASES}
    kind_by_id.update({k: "compound" for k in COMPOUND_TECH_ALIASES})

    result = search_catalog(catalog, q=q, limit=limit, kind_by_id=kind_by_id)
    return {
        "tech": result["keys"],
        "aliases": result["aliases"],
        "items": result["items"],
    }


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
