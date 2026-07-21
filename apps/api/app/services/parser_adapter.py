"""Parser service adapter — auto-routes custom vs Docling by column layout."""

from __future__ import annotations

import json
import logging
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any
from parser.docling_parser import parse_cv_docling
from docling.document_converter import DocumentConverter

from time import perf_counter

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


def _ensure_repo_root_on_path() -> Path:
    """Make repo root importable for ``parser.*`` packages."""
    root = Path(__file__).resolve().parents[4]
    root_s = str(root)
    if root_s not in sys.path:
        sys.path.insert(0, root_s)
    return root


def merge_sections(
    first: dict[str, Any],
    second: dict[str, Any],
) -> dict[str, Any]:
    required_sections = [
        "education",
        "experience",
        "skills",
    ]

    merged = {}

    for section in required_sections:
        if section in first:
            first[section] = first[section]
        elif section in second:
            first[section] = second[section]

    return first

def _should_run_custom_parser(resume: dict) -> bool:
    """
    Returns True if the custom parser should be executed.

    Conditions:
    - A required section is missing.
    - A required section is empty.
    - A required section contains only empty strings / empty values.
    """

    required_sections = [
        "education",
        "experience",
        #"projects",
        "skills",
    ]
    #print(resume)
    def has_meaningful_data(value):
        if value is None:
            return False

        if isinstance(value, str):
            return value.strip() != ""

        if isinstance(value, list):
            if len(value) == 0:
                return False
            return any(has_meaningful_data(item) for item in value)

        if isinstance(value, dict):
            if len(value) == 0:
                return False
            return any(has_meaningful_data(v) for v in value.values())

        return True

    issue=False
    for section in required_sections:
        if section not in resume:
            logger.info(f"{section} not found")
            issue= True

        if not has_meaningful_data(resume[section]):
            logger.info(f"{section} not meaningful data found")

            issue= True

    return issue



def parse_resume_bytes(
    data: bytes,
    filename: str,
    content_type: str = "application/pdf",
    min_experience: float=0,
    converter: DocumentConverter | None = None
    
) -> ParseResult:
    """Parse a resume: single-column → custom PyMuPDF; multi-column → Docling."""
    _ensure_repo_root_on_path()
    groq_key = get_settings().groq_api_key or os.getenv("GROQ_API_KEY", "")
    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key

    suffix = Path(filename).suffix.lower() or ".pdf"
    tmp_path: str | None = None
    converted_path: str | None = None
    warnings: list[str] = []
    
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(data)
            tmp_path = tmp.name

        path_to_parse = tmp_path
        if suffix in {".docx", ".doc"}:
            converted_path = _try_docx_to_pdf(tmp_path)
            if converted_path:
                path_to_parse = converted_path
            else:
                warnings.append("docx_pdf_conversion_unavailable")

        layout: dict[str, Any] = {"is_multicolumn": False, "max_columns": 1, "pages": []}
        use_docling = False
        if path_to_parse.lower().endswith(".pdf"):
            try:
                from parser.layout_detect import detect_columns

                layout = detect_columns(path_to_parse)
                use_docling = bool(layout.get("is_multicolumn"))
            except Exception as exc:
                warnings.append(f"column_detect_failed: {exc}")
                logger.warning("Column detection failed for %s: %s", filename, exc)
                use_docling = False

        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        if use_docling:
            logger.info("========== DOCLING 1START ==========")
            t = perf_counter()
            sections = parse_cv_docling(path_to_parse,converter)
            parser_id = "docling"
            logger.info(
                "========== DOCLING 1END (%.3fs) ==========",
                 perf_counter() - t
            )
        else:
            logger.info("========== CUSTOM PARSER 1START ==========")
            t = perf_counter()


            sections = _run_parse_cv(path_to_parse)
            logger.info(
    "========== CUSTOM PARSER1 END (%.3fs) ==========",
    perf_counter() - t
)

            parser_id = "custom.pymupdf"

        if not sections:
            raise RuntimeError(f"{parser_id} returned empty sections")

        structured = _normalize_sections(sections)
        alternative_flow=_should_run_custom_parser(structured)

        if alternative_flow==True:
            if parser_id=="docling":
                logger.info("========== CUSTOM PARSER 2START ==========")
                t = perf_counter()

                sections2=_run_parse_cv(path_to_parse)
                parser_id = "custom.pymupdf"
                logger.info(
                    "========== CUSTOM PARSER 2END (%.3fs) ==========",
                    perf_counter() - t
                )

                sections=merge_sections(sections,sections2)
                #print("custom2")
            else:
                logger.info("========== DOCLING 1START ==========")
                t = perf_counter()
                sections2 = parse_cv_docling(path_to_parse,converter)
                parser_id = "docling"
                logger.info(
                    "========== DOCLING 1END (%.3fs) ==========",
                    perf_counter() - t
                )
                
                #print("docling2")
                sections=merge_sections(sections,sections2)
                
        if not sections:
            raise RuntimeError(f"{parser_id} returned empty sections")

        structured = _normalize_sections(sections)
        
        if os.getenv("GROQ_API_KEY"):
            logger.info("========== GROQ START ==========")
            t = perf_counter()

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
            logger.info(
                "========== GROQ END (%.3fs) ==========",
                perf_counter() - t
            )
        name = str(sections.get("name") or "").strip()
        emails = _as_list(sections.get("email"))
        phones = _as_list(sections.get("phone"))
        raw = str(sections.get("raw_text") or "")
        if not emails:
            emails = EMAIL_RE.findall(raw)[:3]
        if not phones:
            phones = PHONE_RE.findall(raw)[:3]
        links = URL_RE.findall(raw)[:8]

        confidence = _score_confidence(structured, name=name, emails=emails,min_experience=min_experience)
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
            provenance={
                "parser": parser_id,
                "filename": filename,
                "columns": layout.get("max_columns", 1),
                "is_multicolumn": layout.get("is_multicolumn", False),
            },
        )
    except Exception as exc:
        logger.exception("Parse failed for %s", filename)
        raise RuntimeError(f"Resume parse failed for {filename}: {exc}") from exc
    finally:
        for p in (tmp_path, converted_path):
            if p and os.path.exists(p):
                try:
                    os.unlink(p)
                except OSError:
                    pass


def _run_parse_cv(path: str) -> dict[str, Any]:
    """Call custom parse_cv; redirect form_json to a temp file."""
    from parser import parser as parser_mod  # type: ignore

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
    """Map nested section dicts → MatchingResumeSchema fields."""
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
    chunks = re.split(r"[\n,|/•·;]+", text)
    skills: list[str] = []
    seen: set[str] = set()
    for chunk in chunks:
        s = chunk.strip(" -:\t")
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
    """Best-effort experience rows without LLM."""
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
        rows.append(
            ExperienceEntry(
                company=title,
                designation="",
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
    """Use Groq to structure education/experience."""
    from groq import Groq

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    prompt = f"""
You are an expert resume parser.

You are given ONLY the Education and Experience sections of a resume.

The parser that generated these sections is imperfect.
Some resumes may have:
- Missing subsection boundaries (everything merged into one subsection)
- Too many subsection boundaries
- Incorrect subsection titles
- Broken subsection keys

Your task is to reconstruct the original Education and Experience entries.

IMPORTANT RULES

1. There may be ZERO, ONE, OR MANY education entries.
2. There may be ZERO, ONE, OR MANY experience entries.
3. Extract ALL entries. Never stop after the first one.
4. Never omit an entry.
5. Never merge two different jobs into one.
6. Never merge two different education records into one.

TEXT PRESERVATION

- Do NOT summarize.
- Do NOT rewrite.
- Do NOT paraphrase.
- Do NOT improve grammar.
- Preserve all information from the input.
- Every piece of information must appear exactly once in the output.
- If a value cannot be assigned to a structured field, include it in the description.

FIELD EXTRACTION

For Experience:

- company
- designation
- start_date
- end_date
- description

For Education:

- degree
- institution
- cgpa
- graduation_date

If a field cannot be confidently determined, leave it as an empty string.

The description field should contain ALL remaining text that does not belong to the structured fields.

OUTPUT FORMAT

Return ONLY valid JSON.

Always return BOTH keys.

{{
    "experience": [
        {{
            "company": "",
            "designation": "",
            "start_date": "",
            "end_date": "",
            "description": ""
        }}
    ],
    "education": [
        {{
            "degree": "",
            "institution": "",
            "cgpa": "",
            "graduation_date": ""
        }}
    ]
}}

Education input:

{json.dumps(education, indent=2)}

Experience input:

{json.dumps(experience, indent=2)}
"""
    print("sent to groq")
    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", get_settings().groq_model or "qwen/qwen3-32b"),
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are an expert CV parser."},
            {"role": "user", "content": prompt},
        ],
    )
    #print(response)
    content = response.choices[0].message.content or "{}"
    content = content.strip()
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)
    return json.loads(content)



EXPECTED_EXPERIENCE_FIELDS = [
    "company",
    "designation",
    "start_date",
    "end_date",
    "description",
]

EXPECTED_EDUCATION_FIELDS = [
    "degree",
    "institution",
    "cgpa",
    "graduation_date",
]


def _extract_words(data, include_keys=True):
    words = []

    if data is None:
        return words

    if isinstance(data, str):
        words.extend(re.findall(r"\b\w+\b", data))

    elif isinstance(data, list):
        for item in data:
            words.extend(_extract_words(item, include_keys))

    elif isinstance(data, dict):
        for key, value in data.items():
            if include_keys:
                words.extend(re.findall(r"\b\w+\b", str(key)))
            words.extend(_extract_words(value, include_keys))

    return words


def _score_confidence(
    structured: dict[str, Any],
    *,
    name: str,
    emails: list[str],
    min_experience: float,
) -> float:
    """
    Confidence that the parser extracted the resume correctly.
    Returns a value between 0.0 and 1.0.
    """

    # ---------------- Required Sections ---------------- #

    required_sections = ["skills", "education"]

    if min_experience > 0:
        required_sections.append("experience")

    section_score = 0.0

    for section in required_sections:
        if structured.get(section):
            section_score += 1

    section_score /= len(required_sections)

    # ---------------- Completeness ---------------- #

    total_fields = 0
    filled_fields = 0

    if structured.get("education"):

        for edu in structured["education"]:
            for field in EXPECTED_EDUCATION_FIELDS:
                total_fields += 1
                value = getattr(edu, field, "")
                if str(value).strip():
                    filled_fields += 1
                
    if min_experience > 0 and structured.get("experience"):

        for exp in structured["experience"]:
            for field in EXPECTED_EXPERIENCE_FIELDS:
                total_fields += 1
                value = getattr(exp, field, "")
                if str(value).strip():
                    filled_fields += 1
                
    completeness_score = (
        filled_fields / total_fields if total_fields else 1.0
    )

    # ---------------- Raw Text Coverage ---------------- #

    raw_text = structured.get("raw_resume_text", "")

    raw_words = len(re.findall(r"\b\w+\b", raw_text))

    structured_words = []

    structured_words.extend(
        _extract_words(structured.get("skills", []), include_keys=True)
    )

    structured_words.extend(
        _extract_words(structured.get("education", []), include_keys=False)
    )

    structured_words.extend(
        _extract_words(structured.get("experience", []), include_keys=False)
    )

    coverage = (
        min(len(structured_words) / raw_words, 1.0)
        if raw_words
        else 0.0
    )

    # ---------------- Final Confidence ---------------- #

    confidence = (
        0.40 * section_score
        + 0.40 * completeness_score
        + 0.20 * coverage
    )

    # Small parser bonuses

    if name:
        confidence += 0.02

    if emails:
        confidence += 0.02

    return round(min(confidence, 0.99), 2)

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