"""Detect single- vs multi-column PDF layouts for parser routing."""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


def detect_columns(pdf_path: str, *, footer_margin: int = 50, header_margin: int = 50) -> dict[str, Any]:
    """Classify a PDF as single-column, multi-column, or unknown.

    Uses PyMuPDF ``column_boxes`` (same algorithm as ``parser.multi_column``).
    A page is substantive multi-column only when at least two detected boxes
    contain enough text to avoid routing sidebars and decorative fragments to
    Docling.
    """
    import fitz

    from parser.multi_column import column_boxes

    doc = fitz.open(pdf_path)
    pages: list[dict[str, Any]] = []
    max_columns = 0
    failures: list[str] = []
    useful_pages = 0
    multi_pages = 0

    try:
        for page_index, page in enumerate(doc):
            try:
                boxes = column_boxes(
                    page,
                    footer_margin=footer_margin,
                    header_margin=header_margin,
                    no_image_text=True,
                )
                text_lengths = [
                    len(page.get_text("text", clip=box).strip())
                    for box in boxes
                ]
                substantive = [length for length in text_lengths if length >= 80]
                page_text_length = len(page.get_text("text").strip())
                count = len(boxes)
                if page_text_length >= 80:
                    useful_pages += 1
                if len(substantive) >= 2:
                    multi_pages += 1
            except Exception as exc:
                logger.warning("column_boxes failed on page %s: %s", page_index, exc)
                failures.append(f"page_{page_index}: {exc}")
                count = 0
                text_lengths = []
                page_text_length = 0
            pages.append(
                {
                    "page": page_index,
                    "columns": count,
                    "column_text_lengths": text_lengths,
                    "text_length": page_text_length,
                    "substantive_multicolumn": len(
                        [length for length in text_lengths if length >= 80]
                    )
                    >= 2,
                }
            )
            if count > max_columns:
                max_columns = count
    finally:
        doc.close()

    if multi_pages:
        classification = "multi"
    elif failures or useful_pages == 0:
        classification = "unknown"
    else:
        classification = "single"

    return {
        "classification": classification,
        "is_multicolumn": classification == "multi",
        "max_columns": max_columns,
        "pages": pages,
        "failures": failures,
        "useful_pages": useful_pages,
        "multi_pages": multi_pages,
    }
