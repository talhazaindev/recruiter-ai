"""Parser service adapter — bridges repo `parser/` into MatchingResumeSchema."""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import tempfile
from pathlib import Path
from typing import Any

from app.config import get_settings
from app.models.schemas import (
    CandidateExtras,
    EducationEntry,
    ExperienceEntry,
    MatchingResumeSchema,
    ParseResult,
)

logger = logging.getLogger(__name__)

EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_RE = re.compile(r"(?:\+92|0)?3\d{2}[-\s]?\d{7}")
URL_RE = re.compile(r"https?://[^\s|]+|(?:www\.)?(?:linkedin|github)\.com/[^\s|]+", re.I)


def parse_resume_bytes(
    data: bytes,
    filename: str,
    content_type: str = "application/pdf",
) -> ParseResult:
    """Parse a resume file into ParseResult.

    PARSER_MODE=local (default for production path) uses the PyMuPDF parser
    package under repo `parser/`. PARSER_MODE=stub keeps deterministic fakes.
    """
    settings = get_settings()
    if settings.parser_mode == "stub":
        return _parse_stub(data, filename)
    return _parse_local(data, filename)


def settings_parser_is_stub() -> bool:
    """Whether the configured parser mode is stub."""
    return get_settings().parser_mode == "stub"


def _parse_stub(data: bytes, filename: str) -> ParseResult:
    """Deterministic stub parse for demos without PDF deps."""
    digest = hashlib.sha256(data).hexdigest()[:8]
    stem = Path(filename).stem.replace("_", " ").replace("-", " ").title() or "Candidate"
    text = data.decode("utf-8", errors="ignore")
    emails = EMAIL_RE.findall(text)[:3]
    phones = PHONE_RE.findall(text)[:3]
    if not emails:
        emails = [f"{stem.lower().replace(' ', '.')}@example.com"]
    if not phones:
        phones = ["+923001234567"]

    skills = ["Python", "SQL", "React", "FastAPI", "MongoDB"]
    offset = int(digest[:2], 16) % 3
    skills = skills[offset:] + skills[:offset]
    confidence = 0.82 if len(data) > 500 else 0.45
    needs_review = confidence < get_settings().parse_confidence_review_threshold

    resume = MatchingResumeSchema(
        raw_resume_text=text[:5000] or f"Stub resume for {stem}",
        professional_summary=f"Experienced professional ({stem}) with software engineering background.",
        skills=skills,
        experience=[
            ExperienceEntry(
                company="Acme Soft",
                designation="Software Engineer",
                start_date="2021-01",
                end_date="Present",
                description="Built APIs and data pipelines.\nImproved hiring ops tooling.",
            )
        ],
        projects=[f"{stem} Portfolio Project"],
        education=[
            EducationEntry(
                degree="BS Computer Science",
                institution="NUST",
                cgpa="3.5",
                graduation_date="2020",
            )
        ],
        certifications=[],
    )
    return ParseResult(
        schema_version="matching.v1",
        status="partial" if needs_review else "ok",
        resume=resume,
        candidate=CandidateExtras(name=stem, emails=emails, phones=phones, links=[]),
        confidence=confidence,
        field_confidence={"skills": 0.8, "experience": 0.7, "education": 0.75},
        warnings=["stub_parser"],
        needs_review=needs_review,
        provenance={"parser": "stub", "filename": filename, "digest": digest},
    )


def _parse_local(data: bytes, filename: str) -> ParseResult:
    """Run the repo CV parser and normalize into MatchingResumeSchema."""
    import tempfile as _tempfile

    suffix = Path(filename).suffix.lower() or ".pdf"
    tmp_path: str | None = None
    warnings: list[str] = []

    try:
        # Ensure repo root is importable for `parser.parser`
        # .../apps/api/app/services/parser_adapter.py → parents[4] = repo root
        root = Path(__file__).resolve().parents[4]
        import sys

        root_s = str(root)
        if root_s not in sys.path:
            sys.path.insert(0, root_s)

        # Propagate Groq key from Settings/.env into os.environ for groq client
        groq_key = get_settings().groq_api_key or os.getenv("GROQ_API_KEY", "")
        if groq_key:
            os.environ["GROQ_API_KEY"] = groq_key

        with _tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(data)
            tmp_path = tmp.name

        # DOCX → PDF if LibreOffice available (best-effort)
        path_to_parse = tmp_path
        if suffix in {".docx", ".doc"}:
            converted = _try_docx_to_pdf(tmp_path)
            if converted:
                path_to_parse = converted
            else:
                warnings.append("docx_pdf_conversion_unavailable")

        from parser.parser import parse_cv  # type: ignore

        # Avoid clobbering process CWD output.json: patch form_json temporarily
        sections = _run_parse_cv(path_to_parse)
        if not sections:
            raise RuntimeError("parse_cv returned empty")

        structured = _normalize_sections(sections)
        # Optional Groq enrichment for education/experience arrays
        if os.getenv("GROQ_API_KEY"):
            try:
                enriched = _groq_structure_edu_exp(
                    sections.get("education") or {},
                    sections.get("experience") or {},
                )
                if enriched.get("experience"):
                    structured["experience"] = [
                        ExperienceEntry.model_validate(e) for e in enriched["experience"]
                    ]
                if enriched.get("education"):
                    structured["education"] = [
                        EducationEntry.model_validate(e) for e in enriched["education"]
                    ]
            except Exception as exc:
                warnings.append(f"groq_structure_skipped: {exc}")
                logger.warning("Groq structure failed: %s", exc)

        name = str(sections.get("name") or "").strip()
        emails = _as_list(sections.get("email"))
        phones = _as_list(sections.get("phone"))
        raw = str(sections.get("raw_text") or "")
        if not emails:
            emails = EMAIL_RE.findall(raw)[:3]
        if not phones:
            phones = PHONE_RE.findall(raw)[:3]
        links = URL_RE.findall(raw)[:8]

        confidence = _score_confidence(structured, name=name, emails=emails)
        needs_review = confidence < get_settings().parse_confidence_review_threshold
        status = "ok" if confidence >= 0.7 else "partial"

        return ParseResult(
            schema_version="matching.v1",
            status=status,
            resume=MatchingResumeSchema(**structured),
            candidate=CandidateExtras(
                name=name or Path(filename).stem.replace("_", " "),
                emails=emails,
                phones=phones,
                links=links,
            ),
            confidence=confidence,
            field_confidence={
                "skills": 0.85 if structured["skills"] else 0.3,
                "experience": 0.85 if structured["experience"] else 0.3,
                "education": 0.85 if structured["education"] else 0.3,
            },
            warnings=warnings,
            needs_review=needs_review,
            provenance={"parser": "local.pymupdf", "filename": filename},
        )
    except Exception as exc:
        logger.exception("Local parse failed for %s", filename)
        result = _parse_stub(data, filename)
        result.warnings = [f"local_parser_fallback: {exc}", "stub_parser"]
        result.status = "partial"
        result.needs_review = True
        result.provenance = {
            **result.provenance,
            "parser": "stub_fallback",
            "error": str(exc),
        }
        return result
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass


def _run_parse_cv(path: str) -> dict[str, Any]:
    """Call parse_cv and prefer its return value; fall back to reading output.json."""
    from parser import parser as parser_mod  # type: ignore

    # Redirect form_json to a temp file so we don't pollute CWD
    out_file = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
    out_path = out_file.name
    out_file.close()

    original_form = parser_mod.form_json

    def _form_json(sections: dict[str, Any]) -> None:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(sections, f, indent=2, ensure_ascii=False)

    parser_mod.form_json = _form_json
    try:
        result = parser_mod.parse_cv(path)
        if isinstance(result, dict) and result:
            return result
        with open(out_path, encoding="utf-8") as f:
            return json.load(f)
    finally:
        parser_mod.form_json = original_form
        try:
            os.unlink(out_path)
        except OSError:
            pass


def _normalize_sections(sections: dict[str, Any]) -> dict[str, Any]:
    """Map legacy nested section dicts → MatchingResumeSchema fields."""
    raw = str(sections.get("raw_text") or "")
    summary = _flatten_section(sections.get("summary") or sections.get("professional_summary"))
    skills = _flatten_skills(sections.get("skills"))
    projects = _flatten_projects(sections.get("projects"))
    certifications = _flatten_skills(sections.get("certifications"))
    experience = _heuristic_experience(sections.get("experience") or {})
    education = _heuristic_education(sections.get("education") or {})

    return {
        "raw_resume_text": raw,
        "professional_summary": summary,
        "skills": skills,
        "experience": experience,
        "projects": projects,
        "education": education,
        "certifications": certifications,
    }


def _flatten_section(value: Any) -> str:
    """Collapse nested section content into one string."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(_flatten_section(v) for v in value if v).strip()
    if isinstance(value, dict):
        parts: list[str] = []
        for k, v in value.items():
            body = _flatten_section(v)
            if k == "content":
                if body:
                    parts.append(body)
            elif body:
                parts.append(f"{k}: {body}" if body != k else body)
            elif str(k).strip():
                parts.append(str(k).strip())
        return "\n".join(parts).strip()
    return str(value).strip()


def _flatten_skills(value: Any) -> list[str]:
    """Extract a flat unique skill list from nested skills section."""
    text = _flatten_section(value)
    if not text:
        return []
    # Split on commas / newlines / pipes / bullets
    chunks = re.split(r"[\n,|/•·;]+", text)
    skills: list[str] = []
    seen: set[str] = set()
    for chunk in chunks:
        s = chunk.strip(" -:\t")
        # Skip category labels like "Languages" alone if very short category headers
        if not s or len(s) > 80:
            continue
        if s.lower().endswith(":") or s.lower() in {
            "languages",
            "frameworks",
            "frameworks & libraries",
            "tools",
            "tools & platforms",
            "libraries",
            "interests & hobbies",
        }:
            continue
        key = s.lower()
        if key not in seen:
            seen.add(key)
            skills.append(s)
    return skills[:80]


def _flatten_projects(value: Any) -> list[str]:
    """Flatten projects section into title + detail strings."""
    if not value:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, dict):
        out: list[str] = []
        for k, v in value.items():
            body = _flatten_section(v)
            if k == "content":
                if body:
                    out.append(body)
            elif body:
                out.append(f"{k}: {body}")
            elif str(k).strip() and k != "content":
                out.append(str(k).strip())
        return out
    return []


def _heuristic_experience(value: Any) -> list[ExperienceEntry]:
    """Best-effort experience rows without LLM (key ≈ company/title blob)."""
    if isinstance(value, list):
        rows: list[ExperienceEntry] = []
        for item in value:
            if isinstance(item, dict):
                rows.append(ExperienceEntry.model_validate(item))
            elif item:
                rows.append(ExperienceEntry(description=str(item)))
        return rows
    if not isinstance(value, dict):
        text = _flatten_section(value)
        return [ExperienceEntry(description=text)] if text else []

    rows = []
    for key, val in value.items():
        if key == "content" and not _flatten_section(val):
            continue
        desc = _flatten_section(val)
        title = "" if key == "content" else str(key).strip()
        # Try split "Company — Role" patterns loosely into company
        company = title
        designation = ""
        rows.append(
            ExperienceEntry(
                company=company,
                designation=designation,
                start_date="",
                end_date="",
                description=desc,
            )
        )
    return rows


def _heuristic_education(value: Any) -> list[EducationEntry]:
    """Best-effort education entries without LLM."""
    if isinstance(value, list):
        rows: list[EducationEntry] = []
        for item in value:
            if isinstance(item, dict):
                rows.append(EducationEntry.model_validate(item))
            elif item:
                rows.append(EducationEntry(degree=str(item)))
        return rows
    text = _flatten_section(value)
    if not text:
        return []
    chunks = [c.strip() for c in re.split(r"\n\s*\n", text) if c.strip()]
    if not chunks:
        chunks = [text]
    return [
        EducationEntry(degree=chunk, institution="", cgpa="", graduation_date="")
        for chunk in chunks
    ]


def _groq_structure_edu_exp(education: Any, experience: Any) -> dict[str, Any]:
    """Use Groq to structure education/experience like llm_checking.py."""
    from groq import Groq

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    prompt = f"""
You are an expert resume parser.
Reconstruct Education and Experience entries from imperfect nested JSON.
Rules: do not paraphrase; empty string if unknown; return ONLY JSON with keys experience and education.
Experience fields: company, designation, start_date, end_date, description
Education fields: degree, institution, cgpa, graduation_date

Education input:
{json.dumps(education, indent=2, ensure_ascii=False)}

Experience input:
{json.dumps(experience, indent=2, ensure_ascii=False)}
"""
    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "qwen/qwen3-32b"),
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are an expert CV parser."},
            {"role": "user", "content": prompt},
        ],
    )
    content = response.choices[0].message.content or "{}"
    # Strip accidental fences
    content = content.strip()
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)
    return json.loads(content)


def _score_confidence(structured: dict[str, Any], *, name: str, emails: list[str]) -> float:
    """Heuristic confidence from populated matching fields."""
    score = 0.35
    if name:
        score += 0.15
    if emails:
        score += 0.1
    if structured.get("skills"):
        score += 0.15
    if structured.get("experience"):
        score += 0.15
    if structured.get("education"):
        score += 0.1
    if structured.get("raw_resume_text"):
        score += 0.05
    return round(min(score, 0.98), 2)


def _as_list(value: Any) -> list[str]:
    """Normalize scalar/list contact fields to list[str]."""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    s = str(value).strip()
    return [s] if s else []


def _try_docx_to_pdf(docx_path: str) -> str | None:
    """Convert DOCX to PDF via LibreOffice when available."""
    import subprocess

    soffice = os.environ.get(
        "LIBREOFFICE_PATH",
        r"C:\Program Files\LibreOffice\program\soffice.exe",
    )
    if not os.path.exists(soffice):
        return None
    out_dir = os.path.dirname(os.path.abspath(docx_path))
    try:
        subprocess.run(
            [soffice, "--headless", "--convert-to", "pdf", docx_path, "--outdir", out_dir],
            check=True,
            capture_output=True,
            timeout=120,
        )
        pdf_name = os.path.splitext(os.path.basename(docx_path))[0] + ".pdf"
        pdf_path = os.path.join(out_dir, pdf_name)
        return pdf_path if os.path.exists(pdf_path) else None
    except Exception:
        return None
