"""Detect single- vs multi-column PDF layouts for parser routing."""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


def detect_columns(pdf_path: str, *, footer_margin: int = 50, header_margin: int = 50) -> dict[str, Any]:
    """Return column layout stats for a PDF.

    Uses PyMuPDF ``column_boxes`` (same algorithm as ``parser.multi_column``).
    ``is_multicolumn`` is True when any page has more than one column box.
    """
    import fitz

    from parser.multi_column import column_boxes

    doc = fitz.open(pdf_path)
    pages: list[dict[str, Any]] = []
    max_columns = 0

    try:
        for page_index, page in enumerate(doc):
            try:
                boxes = column_boxes(
                    page,
                    footer_margin=footer_margin,
                    header_margin=header_margin,
                    no_image_text=True,
                )
                count = len(boxes)
            except Exception as exc:
                logger.warning("column_boxes failed on page %s: %s", page_index, exc)
                count = 1
            pages.append({"page": page_index, "columns": count})
            if count > max_columns:
                max_columns = count
    finally:
        doc.close()

    if max_columns < 1:
        max_columns = 1

    return {
        "is_multicolumn": max_columns > 1,
        "max_columns": max_columns,
        "pages": pages,
    }
