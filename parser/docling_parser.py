"""Docling-based resume parser for multi-column CVs."""

from __future__ import annotations

import logging
import os
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

from parser.parser import _is_person_name, extract_basic_info, normalize_heading

logger = logging.getLogger(__name__)

_converter: DocumentConverter | None = None
_pipeline_initialized: bool = False


def _env_bool(name: str, default: bool) -> bool:
    """Parse a boolean environment variable."""
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _settings_docling() -> dict[str, Any] | None:
    """Load Docling knobs from app Settings when the API package is importable."""
    try:
        from app.config import get_settings

        s = get_settings()
        return {
            "artifacts_path": (s.docling_artifacts_path or "").strip() or None,
            "do_ocr": bool(s.docling_do_ocr),
            "do_table_structure": bool(s.docling_do_table_structure),
        }
    except Exception:
        return None


def _resolve_artifacts_path(configured: str | None = None) -> str | None:
    """Return absolute artifacts path, or None for Docling HF default cache."""
    raw = (configured if configured is not None else os.getenv("DOCLING_ARTIFACTS_PATH") or "").strip()
    if not raw:
        return None
    path = Path(raw).expanduser().resolve()
    if not path.is_dir():
        raise FileNotFoundError(
            f"DOCLING_ARTIFACTS_PATH={path} does not exist or is not a directory. "
            "Bake models into the image (see infra/Dockerfile.api) or unset the variable."
        )
    return str(path)


def build_pdf_pipeline_options() -> PdfPipelineOptions:
    """Build PDF pipeline options (OCR/tables off by default for born-digital resumes)."""
    from_settings = _settings_docling()
    if from_settings is not None:
        do_ocr = from_settings["do_ocr"]
        do_table = from_settings["do_table_structure"]
        artifacts = _resolve_artifacts_path(from_settings["artifacts_path"])
    else:
        do_ocr = _env_bool("DOCLING_DO_OCR", False)
        do_table = _env_bool("DOCLING_DO_TABLE_STRUCTURE", False)
        artifacts = _resolve_artifacts_path()

    opts = PdfPipelineOptions()
    opts.do_ocr = do_ocr
    opts.do_table_structure = do_table
    if artifacts:
        opts.artifacts_path = artifacts
    return opts


def create_docling_converter() -> DocumentConverter:
    """Create a DocumentConverter configured for born-digital resume PDFs."""
    opts = build_pdf_pipeline_options()
    return DocumentConverter(
        allowed_formats=[InputFormat.PDF],
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opts)},
    )


def get_docling_converter() -> DocumentConverter:
    """Return one lazy converter per process."""
    global _converter
    if _converter is None:
        _converter = create_docling_converter()
    return _converter


def initialize_docling_pipeline(*, warm: bool = True) -> DocumentConverter:
    """Create (or reuse) the converter and optionally load the PDF pipeline eagerly.

    Call at parse-worker startup so model load cost is paid before the first task.
    """
    global _pipeline_initialized
    converter = get_docling_converter()
    if warm and not _pipeline_initialized:
        opts = build_pdf_pipeline_options()
        t0 = time.perf_counter()
        logger.info(
            "Initializing Docling PDF pipeline (artifacts=%s, ocr=%s, tables=%s)",
            opts.artifacts_path or "(huggingface default)",
            opts.do_ocr,
            opts.do_table_structure,
        )
        converter.initialize_pipeline(InputFormat.PDF)
        _pipeline_initialized = True
        logger.info("Docling PDF pipeline ready in %.3fs", time.perf_counter() - t0)
    return converter


def reset_docling_converter() -> None:
    """Clear the process-local converter (tests only)."""
    global _converter, _pipeline_initialized
    _converter = None
    _pipeline_initialized = False

HEADING_MAP = {
    # =========================
    # EDUCATION
    # =========================

    "education": "education",
    "educational background": "education",
    "academic background": "education",
    "academic qualification": "education",
    "academic qualifications": "education",
    "educational qualifications": "education",
    "qualifications": "education",
    "education & training": "education",
    "education and training": "education",
    "education:": "education",

    # =========================
    # EXPERIENCE
    # =========================
    "experience": "experience",
    "work experience": "experience",
    "professional experience": "experience",
    "employment history": "experience",
    "career history": "experience",
    "work history": "experience",
    "employment": "experience",
    "professional background": "experience",
    "industry experience": "experience",
    "career experience": "experience",
    "experience:": "experience",

    # =========================
    # SKILLS
    # =========================
    "skill": "skills",
    "skills": "skills",
    "technical skills": "skills",
    "core skills": "skills",
    "key skills": "skills",
    "professional skills": "skills",
    "hard skills": "skills",
    "soft skills": "skills",
    "competencies": "skills",
    "technical competencies": "skills",
    "technical expertise": "skills",
    "expertise": "skills",
    "areas of expertise": "skills",
    "technology stack": "skills",
    "tools & technologies": "skills",
    "tools and technologies": "skills",
    "technologies": "skills",
    "programming languages": "skills",
    "technical proficiencies": "skills",
    "tech stack": "skills",
    "techstack": "skills",
    "strength": "skills",
"strengths": "skills",
"core competencies": "skills",
"technical strengths": "skills",
"technicalskills":"skills",
"coreskills":"skills",


    # =========================
    # PROJECTS
    # =========================
    "projects": "projects",
    "project": "projects",
    "personal projects": "projects",
    "academic projects": "projects",
    "professional projects": "projects",
    "key projects": "projects",
    "major projects": "projects",
    "selected projects": "projects",
    "relevant projects": "projects",
    "project experience": "projects",

    # =========================
    # CERTIFICATIONS
    # =========================
    "certification": "certifications",
    "certifications": "certifications",
    "certificates": "certifications",
    "licenses & certifications": "certifications",
    "licenses and certifications": "certifications",
    "professional certifications": "certifications",
    "training & certifications": "certifications",
    "training and certifications": "certifications",
    "credentials": "certifications",
    "licenses": "certifications",

    # =========================
    # PROFESSIONAL SUMMARY
    # =========================
    "summary": "summary",
    "professional summary": "summary",
    "professionalsummary":"summary",
    "aboutme":"summary",
    "career summary": "summary",
    "profile": "summary",
    "professional profile": "summary",
    "career profile": "summary",
    "executive summary": "summary",
    "overview": "summary",
    "about me": "summary",
    "about": "summary",
    "objective": "summary",
    "career objective": "summary",
    "professional objective": "summary",
    "personal statement": "summary",
    "career overview": "summary",
    "career highlights": "summary",
    "career highlight": "summary",


    #==============================
    #certificates
    #==============================
    # =========================
# CERTIFICATIONS
# =========================
"certification": "certifications",
"certifications": "certifications",
"certificate": "certifications",
"certificates": "certifications",
"certified courses": "certifications",
"professional certification": "certifications",
"professional certifications": "certifications",
"industry certifications": "certifications",
"technical certifications": "certifications",
"licenses": "certifications",
"license": "certifications",
"licences": "certifications",          # British spelling
"licence": "certifications",
"licenses and certifications": "certifications",
"licences and certifications": "certifications",
"credentials": "certifications",
"professional credentials": "certifications",
"certifications & awards": "certification",

"trainings": "certifications",
"training and certifications": "certifications",
"courses": "certifications",
"online courses": "certifications",
"completed courses": "certifications",
"professional development": "certifications",
"continuing education": "certifications",
"certification and training": "certifications",



    # =========================
# RESEARCH
# =========================
"research": "research",
"research experience": "research",
"research work": "research",
"research projects": "research",
"research interests": "research",
"academic research": "research",
"scientific research": "research",
"publications": "research",
"publication": "research",
"published work": "research",
"research publications": "research",
"journal publications": "research",
"conference publications": "research",
"conference papers": "research",
"journal papers": "research",
"research papers": "research",
"research paper": "research",
"papers": "research",
"peer-reviewed publications": "research",
"peer reviewed publications": "research",
"selected publications": "research",
"articles": "research",
"technical papers": "research",
"thesis": "research",
"dissertation": "research",


# =========================
# ACHIEVEMENTS
# =========================
"achievement": "achievements",
"achievements": "achievements",

"accomplishment": "achievements",
"accomplishments": "achievements",
"key accomplishments": "achievements",
"major accomplishments": "achievements",
"professional accomplishments": "achievements",
"career accomplishments": "achievements",
"academic accomplishments": "achievements",
"personal accomplishments": "achievements",
"notable accomplishments": "achievements",

"award": "achievements",
"awards": "achievements",
"honor": "achievements",
"honors": "achievements",
"honour": "achievements",
"honours": "achievements",

"honors and awards": "achievements",
"honours and awards": "achievements",
"awards and honors": "achievements",
"awards and honours": "achievements",
"honors achievements": "achievements",
"honours achievements": "achievements",
"achievements and awards": "achievements",
"awards and achievements": "achievements",
"honors and recognition": "achievements",
"honours and recognition": "achievements",
"awards and recognition": "achievements",
"recognition and awards": "achievements",

"recognitions": "achievements",
"professional recognition": "achievements",
"academic recognition": "achievements",

"distinction": "achievements",
"distinctions": "achievements",
"academic distinctions": "achievements",

"merit": "achievements",
"merits": "achievements",
"academic merit": "achievements",

"commendation": "achievements",
"commendations": "achievements",

"career highlights": "achievements",
"professional highlights": "achievements",
"achievement highlights": "achievements",
"key highlights": "achievements",
"highlights": "achievements",

"milestone": "achievements",
"milestones": "achievements",

"success": "achievements",
"successes": "achievements",
"success stories": "achievements",

"scholarship": "achievements",
"scholarships": "achievements",
"fellowship": "achievements",
"fellowships": "achievements",

"competitive achievements": "achievements",
"professional achievements": "achievements",
"academic achievements": "achievements",
"technical achievements": "achievements",
"research achievements": "achievements",
"personal achievements": "achievements",
"key achievements": "achievements",
"major achievements": "achievements",
"career achievements": "achievements",

"activities": "achievements",

"extra curricular activities": "achievements",
"extracurricular activities": "achievements",
"co curricular activities": "achievements",
"cocurricular activities": "achievements",

"positions of responsibility": "achievements",
"leadership achievements": "achievements",
"leadership awards": "achievements",

# Three-word / Four-word achievement headings
"activities honors and awards": "achievements",
"activities honours and awards": "achievements",

"honors awards and achievements": "achievements",
"honours awards and achievements": "achievements",

"awards honors and achievements": "achievements",
"awards honours and achievements": "achievements",

"awards achievements and honors": "achievements",
"awards achievements and honours": "achievements",

"honors achievements and awards": "achievements",
"honours achievements and awards": "achievements",

"academic honors and awards": "achievements",
"academic honours and awards": "achievements",

"professional honors and awards": "achievements",
"professional honours and awards": "achievements",

"awards and recognitions": "achievements",
"honors and recognitions": "achievements",
"honours and recognitions": "achievements",

"recognition awards and honors": "achievements",
"recognition awards and honours": "achievements",

"key awards and achievements": "achievements",
"major awards and achievements": "achievements",

"achievements honors and awards": "achievements",
"achievements honours and awards": "achievements",

"scholarships honors and awards": "achievements",
"scholarships honours and awards": "achievements",
}

def extract_name_docling(docling_json):

    candidates = []

    for text in docling_json.get("texts", []):

        if text.get("label") != "section_header":
            continue

        if text.get("content_layer") == "furniture":
            continue

        prov = text.get("prov", [])

        if not prov:
            continue

        if prov[0]["page_no"] != 1:
            continue

        value = text["text"].strip()

        if not _is_person_name(value):
            continue

        candidates.append((prov[0]["bbox"]["t"], value))

    if not candidates:
        return None

    # top-most heading
    candidates.sort(reverse=True)

    return candidates[0][1]

def build_docling_sections(doc, HEADER_MAP):
    """
    Converts Docling JSON into

    {
        "experience":{
            "content":"...",
            "company":"...",
            ...
        },
        "education":{
            "Superior University":{
                "content":"..."
            }
        }
    }

    Rules

    1. Header in HEADER_MAP
            -> new section

    2. Header NOT in HEADER_MAP
            -> subsection

    3. Normal text
            -> append to current subsection

    4. If subsection doesn't exist
            -> create 'content'
    """
    #print(doc)
    texts = {
        t["self_ref"]: t
        for t in doc.get("texts", [])
    }

    groups = {
        g["self_ref"]: g
        for g in doc.get("groups", [])
    }

    sections = defaultdict(dict)

    current_section = "miscellaneous"
    current_subsection = "content"

    sections[current_section]["content"] = []

    def ensure(section, subsection):

        if section not in sections:
            sections[section] = {}

        if subsection not in sections[section]:
            sections[section][subsection] = []

    def visit(ref):

        nonlocal current_section
        nonlocal current_subsection

        ############################
        # TEXT NODE
        ############################

        if ref.startswith("#/texts/"):

            node = texts[ref]

            label = node.get("label", "")
            text = node.get("text", "").strip()

            if not text:
                return

            if label == "section_header":

                key = normalize_heading(text)

                if key in HEADER_MAP:

                    current_section = HEADER_MAP[key]
                    current_subsection = "content"

                    ensure(current_section, current_subsection)

                else:

                    current_subsection = text

                    ensure(current_section, current_subsection)

            else:

                ensure(current_section, current_subsection)

                sections[current_section][current_subsection].append(text)

        ############################
        # GROUP NODE
        ############################

        elif ref.startswith("#/groups/"):

            group = groups[ref]

            for child in group.get("children", []):

                visit(child["$ref"])

    #############################################
    # Traverse BODY in original reading order
    #############################################

    for child in doc["body"]["children"]:

        ref = child["$ref"]

        if ref.startswith("#/pictures/"):
            continue

        visit(ref)

    #############################################
    # Join accumulated text
    #############################################

    final = {}

    for sec, subs in sections.items():

        final[sec] = {}

        for sub, values in subs.items():

            final[sec][sub] = "\n".join(values).strip()

    return final

def convert_to_resume_schema(doc, HEADER_MAP):

    sections = build_docling_sections(doc, HEADER_MAP)

    return {

        
        "summary":
            sections.get("summary", {})
                    .get("content", ""),

        "skills":
            sections.get("skills", {}),

        "experience":
            sections.get("experience", {}),

        "projects":
            sections.get("projects", {}),

        "education":
            sections.get("education", {}),

        "certifications":
            sections.get("certifications", {})
    }


def parse_cv_docling(
    path: str,
    converter: DocumentConverter | None = None,
) -> dict[str, Any]:
    """Parse a CV with Docling and return nested section dicts (same shape as custom parse_cv)."""
    converter = converter or get_docling_converter()
    result = converter.convert(path)
    doc_dict = result.document.export_to_dict()
    raw_text = result.document.export_to_text()
    name = extract_name_docling(doc_dict)
    email, phone = extract_basic_info(raw_text)

    final_sections = convert_to_resume_schema(doc_dict, HEADING_MAP)
    final_sections["name"] = name
    final_sections["email"] = email
    final_sections["phone"] = phone
    final_sections["raw_text"] = raw_text
    return final_sections


# Backwards-compatible alias
cv_parse_docling = parse_cv_docling
