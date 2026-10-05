"""Shared domain Pydantic schemas: JD, resume matching payload, match output."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, EmailStr, Field


# ---------------------------------------------------------------------------
# Job Description schema (exact contract)
# ---------------------------------------------------------------------------


class EducationRequirement(BaseModel):
    """Must-have education constraints on a JD."""

    degree: str | None = None
    discipline: str | None = None
    minimum_cgpa: float | None = None
    must_be_completed: bool | None = None


class ExperienceRequirement(BaseModel):
    """Must-have experience constraints on a JD."""

    minimum_total_years: float | None = None


class RequirementsMustHave(BaseModel):
    """Hard requirements section of a JD."""

    education: EducationRequirement = Field(default_factory=EducationRequirement)
    experience: ExperienceRequirement = Field(default_factory=ExperienceRequirement)
    skills: list[str] = Field(default_factory=list)


class NiceToHave(BaseModel):
    """Preferred / soft-signal section of a JD."""

    skills: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    companies: list[str] = Field(default_factory=list)


class JobDescriptionSchema(BaseModel):
    """Canonical JD schema used by API, matcher, and UI."""

    job_title: str = ""
    job_summary: str = ""
    key_responsibilities: list[str] = Field(default_factory=list)
    requirements_must_have: RequirementsMustHave = Field(default_factory=RequirementsMustHave)
    minimum_relevant_years: float | None = None
    tech_stack: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    nice_to_have: NiceToHave = Field(default_factory=NiceToHave)
    keywords: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Matching resume schema (parser contract / matching.v1)
# ---------------------------------------------------------------------------


class ExperienceEntry(BaseModel):
    """One employment row on a resume."""

    company: str = ""
    designation: str = ""
    start_date: str = ""
    end_date: str = ""
    description: str = ""


class EducationEntry(BaseModel):
    """One education row on a resume."""

    degree: str = ""
    institution: str = ""
    cgpa: str = ""
    graduation_date: str = ""


class MatchingResumeSchema(BaseModel):
    """Stable resume payload consumed by the hybrid matcher."""

    raw_resume_text: str = ""
    professional_summary: str = ""
    skills: list[str] = Field(default_factory=list)
    experience: list[ExperienceEntry] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    education: list[EducationEntry] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)


class CandidateExtras(BaseModel):
    """Contact / identity fields kept outside the matching schema."""

    name: str = ""
    emails: list[str] = Field(default_factory=list)
    phones: list[str] = Field(default_factory=list)
    links: list[str] = Field(default_factory=list)


class ParseResult(BaseModel):
    """Parser envelope returned by the parser service adapter."""

    schema_version: str = "matching.v1"
    status: Literal["ok", "partial", "failed"] = "ok"
    resume: MatchingResumeSchema | None = None
    candidate: CandidateExtras = Field(default_factory=CandidateExtras)
    confidence: float = 0.0
    field_confidence: dict[str, float] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    needs_review: bool = False
    provenance: dict[str, Any] = Field(default_factory=dict)
    job_id: str | None = None


# ---------------------------------------------------------------------------
# Matcher contract
# ---------------------------------------------------------------------------


class HardFilters(BaseModel):
    """Deterministic must-have filter outcome."""

    passed: bool = True
    failed_rules: list[str] = Field(default_factory=list)


class MatchOutput(BaseModel):
    """Hybrid matcher return shape consumed by workers and API."""

    hard_filters: HardFilters = Field(default_factory=HardFilters)
    score: float = 0.0
    rank_signals: dict[str, Any] = Field(default_factory=dict)
    explanation: dict[str, Any] = Field(default_factory=dict)
    matcher_version: str = "hybrid.v1"


# ---------------------------------------------------------------------------
# Auth / API request-response models
# ---------------------------------------------------------------------------


class TokenResponse(BaseModel):
    """JWT login response."""

    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    """Email/password login body."""

    email: EmailStr
    password: str


class UserPublic(BaseModel):
    """Public user representation."""

    id: str
    email: EmailStr
    role: str
    org_id: str


class JobCreate(BaseModel):
    """Create job with JD payload."""

    jd: JobDescriptionSchema = Field(default_factory=JobDescriptionSchema)
    status: Literal["draft", "active", "closed"] = "draft"


class JobUpdate(BaseModel):
    """Partial job update."""

    jd: JobDescriptionSchema | None = None
    status: Literal["draft", "active", "closed"] | None = None


class JobPublic(BaseModel):
    """Job document returned to clients."""

    id: str
    org_id: str
    status: str
    jd: JobDescriptionSchema
    jd_schema_version: str = "jd.v1"
    jd_revision: int = 1
    created_by: str | None = None
    created_at: datetime
    updated_at: datetime
    candidate_count: int = 0
    needs_review_count: int = 0
    shortlisted_count: int = 0
    stale_match_count: int = 0
    rematch_in_progress: bool = False
    active_rematch_batch_id: str | None = None


class JobRematchResponse(BaseModel):
    """Manual JD rematch kickoff response."""

    batch_id: str
    candidate_count: int
    status: str = "processing"


class DriveIngestRequest(BaseModel):
    """Google Drive folder ingest body."""

    folder_url: str


class ShortlistRequest(BaseModel):
    """Toggle shortlist flag."""

    shortlisted: bool = True


class ReviewUpdate(BaseModel):
    """Manual review decision."""

    review_status: Literal["approved", "rejected", "needs_review"]
    notes: str = ""


class ScreeningCallCreate(BaseModel):
    """Future voice-agent trigger (stub)."""

    match_result_id: str | None = None
