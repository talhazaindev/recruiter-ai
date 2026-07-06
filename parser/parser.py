import re
import fitz
import json
import os
from docx import Document

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
"training": "certifications",
"trainings": "certifications",
"training and certifications": "certifications",
"courses": "certifications",
"online courses": "certifications",
"completed courses": "certifications",
"professional development": "certifications",
"continuing education": "certifications",
"certification and training": "certifications",
}

def column_boxes(page, footer_margin=50, header_margin=50, no_image_text=True):
    """Determine bboxes which wrap a column."""
    paths = page.get_drawings()
    bboxes = []

    # path rectangles
    path_rects = []

    # image bboxes
    img_bboxes = []

    # bboxes of non-horizontal text
    # avoid when expanding horizontal text boxes
    vert_bboxes = []

    # compute relevant page area
    clip = +page.rect
    clip.y1 -= footer_margin  # Remove footer area
    clip.y0 += header_margin  # Remove header area

    def can_extend(temp, bb, bboxlist):
        """Determines whether rectangle 'temp' can be extended by 'bb'
        without intersecting any of the rectangles contained in 'bboxlist'.

        Items of bboxlist may be None if they have been removed.

        Returns:
            True if 'temp' has no intersections with items of 'bboxlist'.
        """
        for b in bboxlist:
            if not intersects_bboxes(temp, vert_bboxes) and (
                b == None or b == bb or (temp & b).is_empty
            ):
                continue
            return False

        return True

    def in_bbox(bb, bboxes):
        """Return 1-based number if a bbox contains bb, else return 0."""
        for i, bbox in enumerate(bboxes):
            if bb in bbox:
                return i + 1
        return 0

    def intersects_bboxes(bb, bboxes):
        """Return True if a bbox intersects bb, else return False."""
        for bbox in bboxes:
            if not (bb & bbox).is_empty:
                return True
        return False

    def extend_right(bboxes, width, path_bboxes, vert_bboxes, img_bboxes):
        """Extend a bbox to the right page border.

        Whenever there is no text to the right of a bbox, enlarge it up
        to the right page border.

        Args:
            bboxes: (list[IRect]) bboxes to check
            width: (int) page width
            path_bboxes: (list[IRect]) bboxes with a background color
            vert_bboxes: (list[IRect]) bboxes with vertical text
            img_bboxes: (list[IRect]) bboxes of images
        Returns:
            Potentially modified bboxes.
        """
        for i, bb in enumerate(bboxes):
            # do not extend text with background color
            if in_bbox(bb, path_bboxes):
                continue

            # do not extend text in images
            if in_bbox(bb, img_bboxes):
                continue

            # temp extends bb to the right page border
            temp = +bb
            temp.x1 = width

            # do not cut through colored background or images
            if intersects_bboxes(temp, path_bboxes + vert_bboxes + img_bboxes):
                continue

            # also, do not intersect other text bboxes
            check = can_extend(temp, bb, bboxes)
            if check:
                bboxes[i] = temp  # replace with enlarged bbox

        return [b for b in bboxes if b != None]

    def clean_nblocks(nblocks):
        """Do some elementary cleaning."""

        # 1. remove any duplicate blocks.
        blen = len(nblocks)
        if blen < 2:
            return nblocks
        start = blen - 1
        for i in range(start, -1, -1):
            bb1 = nblocks[i]
            bb0 = nblocks[i - 1]
            if bb0 == bb1:
                del nblocks[i]

        # 2. repair sequence in special cases:
        # consecutive bboxes with almost same bottom value are sorted ascending
        # by x-coordinate.
        y1 = nblocks[0].y1  # first bottom coordinate
        i0 = 0  # its index
        i1 = -1  # index of last bbox with same bottom

        # Iterate over bboxes, identifying segments with approx. same bottom value.
        # Replace every segment by its sorted version.
        for i in range(1, len(nblocks)):
            b1 = nblocks[i]
            if abs(b1.y1 - y1) > 10:  # different bottom
                if i1 > i0:  # segment length > 1? Sort it!
                    nblocks[i0 : i1 + 1] = sorted(
                        nblocks[i0 : i1 + 1], key=lambda b: b.x0
                    )
                y1 = b1.y1  # store new bottom value
                i0 = i  # store its start index
            i1 = i  # store current index
        if i1 > i0:  # segment waiting to be sorted
            nblocks[i0 : i1 + 1] = sorted(nblocks[i0 : i1 + 1], key=lambda b: b.x0)
        return nblocks

    # extract vector graphics
    for p in paths:
        path_rects.append(p["rect"].irect)
    path_bboxes = path_rects

    # sort path bboxes by ascending top, then left coordinates
    path_bboxes.sort(key=lambda b: (b.y0, b.x0))

    # bboxes of images on page, no need to sort them
    for item in page.get_images():
        img_bboxes.extend(page.get_image_rects(item[0]))

    # blocks of text on page
    blocks = page.get_text(
        "dict",
        flags=fitz.TEXTFLAGS_TEXT,
        clip=clip,
    )["blocks"]

    # Make block rectangles, ignoring non-horizontal text
    for b in blocks:
        bbox = fitz.IRect(b["bbox"])  # bbox of the block

        # ignore text written upon images
        if no_image_text and in_bbox(bbox, img_bboxes):
            continue

        # confirm first line to be horizontal
        line0 = b["lines"][0]  # get first line
        if line0["dir"] != (1, 0):  # only accept horizontal text
            vert_bboxes.append(bbox)
            continue

        srect = fitz.EMPTY_IRECT()
        for line in b["lines"]:
            lbbox = fitz.IRect(line["bbox"])
            text = "".join([s["text"].strip() for s in line["spans"]])
            if len(text) > 1:
                srect |= lbbox
        bbox = +srect

        if not bbox.is_empty:
            bboxes.append(bbox)

    # Sort text bboxes by ascending background, top, then left coordinates
    bboxes.sort(key=lambda k: (in_bbox(k, path_bboxes), k.y0, k.x0))

    # Extend bboxes to the right where possible
    bboxes = extend_right(
        bboxes, int(page.rect.width), path_bboxes, vert_bboxes, img_bboxes
    )

    # immediately return of no text found
    if bboxes == []:
        return []

    # --------------------------------------------------------------------
    # Join bboxes to establish some column structure
    # --------------------------------------------------------------------
    # the final block bboxes on page
    nblocks = [bboxes[0]]  # pre-fill with first bbox
    bboxes = bboxes[1:]  # remaining old bboxes

    for i, bb in enumerate(bboxes):  # iterate old bboxes
        check = False  # indicates unwanted joins

        # check if bb can extend one of the new blocks
        for j in range(len(nblocks)):
            nbb = nblocks[j]  # a new block

            # never join across columns
            if bb == None or nbb.x1 < bb.x0 or bb.x1 < nbb.x0:
                continue

            # never join across different background colors
            if in_bbox(nbb, path_bboxes) != in_bbox(bb, path_bboxes):
                continue

            temp = bb | nbb  # temporary extension of new block
            check = can_extend(temp, nbb, nblocks)
            if check == True:
                break

        if not check:  # bb cannot be used to extend any of the new bboxes
            nblocks.append(bb)  # so add it to the list
            j = len(nblocks) - 1  # index of it
            temp = nblocks[j]  # new bbox added

        # check if some remaining bbox is contained in temp
        check = can_extend(temp, bb, bboxes)
        if check == False:
            nblocks.append(bb)
        else:
            nblocks[j] = temp
        bboxes[i] = None

    # do some elementary cleaning
    nblocks = clean_nblocks(nblocks)

    # return identified text bboxes
    return nblocks

def extract_raw_text(pdf_path):
    """
    Extract raw text from a PDF file without any formatting.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Raw text content
    """
    doc = fitz.open(pdf_path)
    all_text = ""
    
    for page in doc:
        all_text += page.get_text()
    
    doc.close()
    #print(all_text)
    return all_text

def extract_raw_text_docx(docx_path):
    """
    Extract raw text from a DOCX file, including tables.

    Args:
        docx_path (str): Path to the DOCX file

    Returns:
        str: Raw text content
    """
    doc = Document(docx_path)

    all_text = []

    # Normal paragraphs
    for para in doc.paragraphs:
        if para.text.strip():
            all_text.append(para.text)

    # Text inside tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip():
                    all_text.append(cell.text)

    return "\n".join(all_text)

def extract_spans(pdf_path):
    """
    Extract spans from PDF with multi-column support.
    Returns spans in correct reading order (left-to-right, top-to-bottom).
    """
    doc = fitz.open(pdf_path)
    all_spans = []
    
    for page_num, page in enumerate(doc, start=1):
        # Detect columns on this page
        columns = column_boxes(page, footer_margin=50, header_margin=50)
        
        if len(columns) <= 1:
            # Single column - extract normally
            page_spans = extract_page_spans(pdf_path)
            all_spans.extend(page_spans)
        else:
            # Multi-column - extract per column in reading order
            for col_rect in columns:
                # Extract text from this column's bounding box
                col_spans = extract_spans_from_bbox(page, col_rect, page_num)
                all_spans.extend(col_spans)
    
    doc.close()
    #for i in all_spans:
     #   print(i["text"])
    return all_spans

def extract_spans_from_bbox(page, bbox, page_num):
    """
    Extract spans from a specific bounding box.
    Useful for extracting text from a column.
    """
    spans = []
    # Get text dictionary within the bounding box
    text_dict = page.get_text("dict", clip=bbox, sort=True)
    
    for block in text_dict["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                spans.append({
                    "text": span["text"],
                    "font": span["font"],
                    "size": span["size"],
                    "flags": span["flags"],
                    "bbox": span["bbox"],
                    "page": page_num,
                    "bold": bool(span["flags"] & 2**4),
                })
    return spans

def extract_page_spans(pdf_path):

    doc = fitz.open(pdf_path)

    spans = []

    for page_num, page in enumerate(doc, start=1):

        text_dict = page.get_text("dict",sort=True)

        for block in text_dict["blocks"]:

            if block["type"] != 0:
                continue

            for line in block["lines"]:
                #print(len(line["spans"]))
                
                for span in line["spans"]:

                    spans.append({
                        "text": span["text"],
                        "font": span["font"],
                        "size": span["size"],
                        "flags": span["flags"],
                        "bbox": span["bbox"],
                        "page": page_num,
                        "bold": span["flags"] >= 16,

                    })

    doc.close()
    #print(spans)
    return spans

def is_heading(span, current_font_size=None):
    text = span["text"].strip()
    font = span["font"]
    #flags = span["flags"]
    bold_flag=span["bold"]
    bold = ("Bold" in font) or (bold_flag) 


    normalized = normalize_heading(text)
    if normalized in HEADING_MAP and bold:
        return True
    

    #if not bold:
    #    return False

    if current_font_size is not None and span["size"] == current_font_size:# and normalized in HEADING_MAP:
        return True
     
    return False

def normalize_heading(text: str) -> str:

    #print("Normalizing heading:", text)
    text=text.lower().strip()
    text = text.replace("&", "and")
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    words = text.split()
    
    if len(words) >= 3 and all(len(word) == 1 for word in words):
        text = "".join(words)
    
    text = re.sub(r"\s+", " ", text)
    #print("Normalized heading:", text)
    return text

def build_sections(spans, current_font_size=None):
    sections = {}
    current_heading = None
    current_content = []

    for span in spans:
        text = span["text"].strip()
        font = span["font"]
        if not text:
            continue

        span["text"] = text
        
        if is_heading(span, current_font_size):
            # Save previous section if it has content
            if current_heading is not None and current_content:
                if current_heading not in sections:
                    sections[current_heading] = []
                sections[current_heading].extend(current_content)
            
            # Start new section
            normalized = normalize_heading(text)
            
            if normalized in HEADING_MAP:
                current_heading = HEADING_MAP[normalized]
            else:
                current_heading = "miscellaneous"
            
            current_font_size = span["size"]
            current_content = []
            
        else:
            # Add content to current section
            if current_heading is not None:
                current_content.append({
                    "text": text,
                    "bold": "Bold" in span["font"],
                    "flags": span["flags"]
                })

    # Save last section if it has content
    if current_heading is not None and current_content:
        if current_heading not in sections:
            sections[current_heading] = []
        sections[current_heading].extend(current_content)

    return sections

# def build_sections(spans, current_font_size=None):

#     sections = {}

#     current_heading = None
#     current_content = []

#     for span in spans:

#         text = span["text"].strip()
#         font = span["font"]
#         #flags = span["flags"]
#         if not text:
#             continue

#         span["text"] = text
#         if is_heading(span,current_font_size):
            
#             # Save previous section
#             if current_heading is not None:
#                 if current_heading == "miscellaneous" and current_heading in sections:
#                     sections[current_heading].extend(current_content)
#                 else:
#                     sections[current_heading] = current_content
        

#             normalized = normalize_heading(text)

#             if normalized in HEADING_MAP:
#                 current_heading = HEADING_MAP[normalized]
#                 current_font_size = span["size"]
                
#             else:
#                 #########
#                 current_heading="miscellaneous"
#                 #print(current_content)
#                 current_font_size = span["size"]
#             current_content = []
                
                
#         else:
#             if current_heading=="miscellaneous":
#                 print(current_content)
#             if current_heading is not None:
#                 current_content.append({"text": text,"bold":("Bold" in span["font"]),"flags": span["flags"]})

#     # Save last section
#     if current_heading is not None:
#         if current_heading == "miscellaneous" and current_heading in sections:
#             sections[current_heading].extend(current_content)
#         else:
#             sections[current_heading] = current_content
#         #sections[current_heading] = current_content
#     #print(sections)
#     return sections

def find_headers(path):
    #spans = extract_spans(path)
    spans=extract_spans(path)
    font_sizes = []

    # Find all unique font sizes
    for span in spans:
        font_sizes.append(span["size"])

    font_sizes = list(set(font_sizes))
    font_sizes.sort(reverse=True)

    sections = build_sections(spans,font_sizes[1])

    return sections
   
    """ print("Sections found:")
    for heading, content in sections.items():
        print(f"Heading: {heading}")
        for line in content:
            print(f"  {line}")
        print("-" * 40)
     """

def group_section(items):
    grouped = {}

    current_key = None

    for item in items:
        text = item["text"].strip()

        #print(item)
        if item["bold"]or item["flags"] >= 16:  # Assuming bold text or flagged text indicates a new key
            current_key = text
            grouped[current_key] = []

        elif current_key is not None:
            grouped[current_key].append(text)
        else:
            # No title encountered yet
            grouped.setdefault("content", []).append(text)

    return grouped

def merge_lists(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = merge_lists(value)
        return data

    elif isinstance(data, list):
        # If it's a list of strings, merge into one string inside a list
        if all(isinstance(item, str) for item in data):
            merged = " ".join(item.strip() for item in data)
            return [merged]

        # Otherwise recurse
        return [merge_lists(item) for item in data]

    return data

def form_json(sections):
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=4, ensure_ascii=False)

def merge_empty_keys(data):
    """
    Merges consecutive keys with empty values into the next key
    that contains non-empty content.

    Returns a new JSON object.
    """

    new_data = {}

    for section, entries in data.items():

        # Skip sections that are not dictionaries
        if not isinstance(entries, dict):
            new_data[section] = entries
            continue

        merged = {}
        pending = []

        keys = list(entries.keys())

        for key in keys:
            value = entries[key]

            is_empty = (
                isinstance(value, list)
                and (len(value) == 0 or all(str(v).strip() == "" for v in value))
            )

            if is_empty:
                pending.append(key)
            else:
                if pending:
                    new_key = " ".join(pending + [key])
                    pending.clear()
                else:
                    new_key = key

                merged[new_key] = value

        # Handle trailing empty keys
        if pending:
            if merged:
                last_key = next(reversed(merged))
                new_last_key = last_key + " " + " ".join(pending)
                merged[new_last_key] = merged.pop(last_key)
            else:
                merged[" ".join(pending)] = [""]

        new_data[section] = merged

    return new_data

def parse_cv(path):
    print("Parsing CV from path:", path)
    raw_text = extract_raw_text(path)
    sections = find_headers(path)
    #print(sections)
    for section_name, items in sections.items():
        sections[section_name] = group_section(items)
    sections["raw_text"] = raw_text
    merged_sections = merge_lists(sections)
    merged_sections = merge_empty_keys(merged_sections)
    form_json(merged_sections)
    #return raw_text
    