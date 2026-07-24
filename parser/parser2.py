from pydoc import doc
import re
import fitz
import json
import os
from docx import Document
import pymupdf.layout  # activate PyMuPDF-Layout in pymupdf
import pymupdf4llm
import pathlib
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

from parser.parser import _is_person_name, extract_basic_info,column_boxes
from parser.parser import HEADING_MAP,merge_empty_keys
from parser.parser import extract_basic_info,extract_raw_text,merge_lists
from parser.parser import normalize_heading,extract_name,group_section


def extract_lines(pdf_path):
    """
    Extract spans from PDF with multi-column support.
    Returns spans in correct reading order (left-to-right, top-to-bottom).
    """
    doc = fitz.open(pdf_path)
    all_lines = []
    
    for page_num, page in enumerate(doc, start=1):
        # Detect columns on this page
        columns = column_boxes(page, footer_margin=50, header_margin=50)
        
        if len(columns) <= 1:
            # Single column - extract normally
            page_lines = extract_page_lines(page, page_num)
            all_lines.extend(page_lines)
        else:
            # Multi-column - extract per column in reading order
            for col_rect in columns:
                # Extract text from this column's bounding box
                col_lines = extract_lines_from_bbox(page, col_rect, page_num)
                all_lines.extend(col_lines)
    
    doc.close()
    #for i in all_spans:
     #   print(i["text"])
    #print(all_spans)
    return all_lines

def extract_lines_from_bbox(page, bbox, page_num):
    """
    Extract lines from a specific bounding box.
    Useful for extracting text from a single column.
    """

    lines = []

    text_dict = page.get_text("dict", clip=bbox, sort=True)

    for block in text_dict["blocks"]:

        if block["type"] != 0:
            continue

        for line in block["lines"]:

            if not line["spans"]:
                continue

            line_text = merge_spans_text(line["spans"])

            if not line_text:
                continue

            spans = line["spans"]

            max_font_size = max(span["size"] for span in spans)
            avg_font_size = sum(span["size"] for span in spans) / len(spans)

            bold_ratio = (
                sum(bool(span["flags"] & (1 << 4)) for span in spans)
                / len(spans)
            )

            dominant_font = max(
                set(span["font"] for span in spans),
                key=lambda f: sum(s["font"] == f for s in spans)
            )

            lines.append({
                "text": line_text,
                "font": dominant_font,
                "size": max_font_size,
                "avg_size": avg_font_size,
                "flags": max(span["flags"] for span in spans),
                "bbox": line["bbox"],
                "page": page_num,
                "bold": bold_ratio >= 0.5,
                "bold_ratio": bold_ratio,
                "spans": spans,
            })

    return lines

def merge_spans_text(spans, gap_threshold=1.5):
    """
    Merge span texts into a single line while preserving spaces between words.

    gap_threshold:
        Minimum horizontal gap (in PDF points) that indicates a space
        should be inserted between consecutive spans.
    """

    if not spans:
        return ""

    text = spans[0]["text"]

    for prev_span, curr_span in zip(spans[:-1], spans[1:]):

        prev_right = prev_span["bbox"][2]
        curr_left = curr_span["bbox"][0]

        gap = curr_left - prev_right

        # Insert a space only if the spans are visually separated
        if gap > gap_threshold:
            text += " "

        text += curr_span["text"]

    return " ".join(text.split())

def extract_page_lines(page, page_num):

    lines = []

    text_dict = page.get_text("dict", sort=True)

    for block in text_dict["blocks"]:

        if block["type"] != 0:
            continue

        for line in block["lines"]:
            #logger.info(line)
            if not line["spans"]:
                continue

            line_text = merge_spans_text(line["spans"])
            
            if not line_text:
                continue

            spans = line["spans"]

            max_font_size = max(span["size"] for span in spans)
            avg_font_size = sum(span["size"] for span in spans) / len(spans)

            bold_ratio = (
                sum(span["flags"] >= 16 for span in spans)
                / len(spans)
            )

            dominant_font = max(
                set(span["font"] for span in spans),
                key=lambda f: sum(s["font"] == f for s in spans)
            )

            lines.append({
                "text": line_text,
                "font": dominant_font,
                "size": max_font_size,
                "avg_size": avg_font_size,
                "flags": max(span["flags"] for span in spans),
                "bbox": line["bbox"],
                "page": page_num,
                "bold": bold_ratio >= 0.5,
                "bold_ratio": bold_ratio,
                "spans": spans,
            })

    return lines

def is_heading(line, current_font_size=None):
    """
    Determines whether a line is a section heading.
    """

    text = line["text"].strip()

    if not text:
        return False

    normalized = normalize_heading(text)

    bold = ("Bold" in line["font"]) or line["bold"]

    # Primary check: known heading + bold
    if normalized in HEADING_MAP and bold:
        return True

    # Secondary check: known heading + large font
    if (
        normalized in HEADING_MAP
        and current_font_size is not None
        and line["size"] >= current_font_size
    ):
        return True

    return False

def build_sections(lines, current_font_size=None):
    sections = {}
    current_heading = None
    current_content = []

    for line in lines:

        text = line["text"].strip()

        if not text:
            continue

        if is_heading(line, current_font_size):

            # Save previous section
            if current_heading is not None and current_content:
                sections.setdefault(current_heading, []).extend(current_content)

            # Start new section
            normalized = normalize_heading(text)

            if normalized in HEADING_MAP:
                current_heading = HEADING_MAP[normalized]
            else:
                current_heading = "miscellaneous"

            current_font_size = line["size"]
            current_content = []

        else:

            if current_heading is not None:
                current_content.append({
                    "text": text,
                    "bold": line["bold"],
                    "flags": line["flags"],
                    "size": line["size"],
                })

    # Save last section
    if current_heading is not None and current_content:
        sections.setdefault(current_heading, []).extend(current_content)

    return sections

def find_headers(path):
    lines = extract_lines(path)
    # lines = extract_lines_pymupdf4llm(path)
    #logger.info(lines)
    font_sizes = sorted(
        {line["size"] for line in lines},
        reverse=True
    )

    if not font_sizes:
        font_sizes = [12.0]

    # Largest font is assumed to be the candidate name
    name = extract_name(lines, font_sizes[0])

    # Section headings tend to be the 2nd or 3rd largest font
    heading_size = font_sizes[min(2, len(font_sizes) - 1)]

    sections = build_sections(lines, heading_size)

    return sections, font_sizes[-1], name

def form_json(sections, filename,folder="result5"):
    # Create result folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)
    
    # Extract just the base filename from the path
    base_name = os.path.basename(filename)
    base_name = os.path.splitext(base_name)[0] + '.json'

    
    # Save in result folder
    filepath = os.path.join(folder, base_name)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=4, ensure_ascii=False)
 

def parse_cv2(path):
    #logger.info("*************************************xd23")
    print("Parsing CV from path:", path)
    raw_text = extract_raw_text(path)
    #logger.info(raw_text)
    email,phone=extract_basic_info(raw_text)
    #logger.info(raw_text)
    sections,min_font,name = find_headers(path)
    logger.info("***************************************************************")
    #logger.info(sections)
    for section_name, items in sections.items():
        sections[section_name] = group_section(items,min_font)
    logger.info("****************************************************************")
    #logger.info(sections)
    sections["email"]=email
    sections["phone"]=phone
    sections["name"]=name
    sections["raw_text"] = raw_text

    #print(sections)
    merged_sections = merge_lists(sections)
    #logger.info(merged_sections)
    #print(merged_sections)
    merged_sections = merge_empty_keys(merged_sections)
    #print(type(merged_sections))
    #form_json(merged_sections,path)
    #form_json(merged_sections)
    
    return merged_sections

