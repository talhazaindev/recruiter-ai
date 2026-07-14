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

def extract_spans_from_json(doc_json):
    """
    Returns spans in the reading order determined by pymupdf4llm.
    """
    #with open(json_path, "r", encoding="utf-8") as f:
     #   doc_json = json.load(f)
    spans = []
    #print(doc_json)
    for page in doc_json["pages"]:
        page_num = page["page_number"]

        for box in page["boxes"]:

            # Skip pictures / drawings
            if box["boxclass"] != "text" and box["boxclass"]!= "section-header":
                continue

            for line in box["textlines"]:

                for span in line["spans"]:
                    if span["text"]=="SUMMARY":
                        print("xd")
                    spans.append({
                        "text": span["text"],
                        "font": span["font"],
                        "size": span["size"],
                        "flags": span["flags"],
                        "bbox": span["bbox"],
                        "page": page_num,
                        "bold": bool(span["flags"] & 16),
                    })
    #print(spans)
    return spans

def extract_spans_pymupdf4llm(pdf_path):
    json_data = pymupdf4llm.to_json(pdf_path)
    #json_path = pathlib.Path("temp.json")
    #json_path.write_text(
    #    json.dumps(json_data, indent=2),
    #    encoding="utf-8"
    #)
    Path("temp.json").write_text(json_data, encoding="utf-8")
    doc_json = json.loads(json_data)
    #print(doc_json)
    # Extract spans from JSON
    return extract_spans_from_json(doc_json)

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
            page_spans = extract_page_spans(page, page_num)
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
    #print(all_spans)
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

def extract_page_spans(page, page_num):


    spans = []


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

    #print(spans)
    return spans

#v2
""" def is_heading(span, current_font_size=None):
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
 """

#isheading v1
def is_heading(span, next_span, current_font_size=None):
    #print(span)
    text = span["text"].strip()
    font = span["font"]
    bold_flag = span["bold"]
    bold = ("Bold" in font) or (bold_flag)
    
    normalized = normalize_heading(text)
    #print("Checking heading:", text, "Normalized:", normalized, "Bold:", bold, "Current font size:", current_font_size)
    # Primary check: must be in HEADING_MAP and bold
    if normalized in HEADING_MAP and bold:
        
        if abs(span["bbox"][1] - next_span["bbox"][1]) <= 1 and next_span["text"] !=" ":  # Allow a small size difference
            return False
        else:
            return True
    
    # Secondary check: only if it's in HEADING_MAP but not bold,
    # and matches the current font size (might be a heading without bold formatting)
    if normalized in HEADING_MAP and current_font_size is not None and span["size"] >= current_font_size:
        if abs(span["bbox"][1] - next_span["bbox"][1]) <= 1:
            pass
        else:   
            return True
    
    return False

#isheading v3
""" def is_heading(span, next_span, current_font_size=None):
    text = span["text"].strip()
    font = span["font"]
    bold = ("Bold" in font) or span["bold"]

    score = 0

    # Empty text cannot be a heading
    if not text:
        return False

    # Reject if next span is on the same line
    SAME_LINE_TOLERANCE = 1.0
    if abs(span["bbox"][1] - next_span["bbox"][1]) <= SAME_LINE_TOLERANCE:
        return False
    else: 
        score+=1

    normalized = normalize_heading(text)


    # Strong signal: known heading
    if normalized in HEADING_MAP:
        score += 3

    # Bold text
    if bold:
        score += 1

    # Font size comparable to current section heading
    if current_font_size is None or span["size"] >= current_font_size:
        score += 1

    # Headings are usually short
    if len(text.split()) <= 5:
        score += 1

    # Accept if score is high enough
    return score >= 3
 """

def normalize_heading(text: str) -> str:
    #xd=text
    #if text=="T E C H N I C A L S K I L L S":
        
     #   print("Normalizing heading:", text)
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
    #if xd=="T E C H N I C A L S K I L L S":
     #   print("Normalized heading:", text)
    return text

#v2
def build_sections(spans, current_font_size=None):
    sections = {}
    current_heading = None
    current_content = []

    total_spans = len(spans)

    for i,span in enumerate(spans):
        if i<total_spans-1:
            next_span=spans[i+1]
        else:
            next_span=span


        text = span["text"].strip()
        font = span["font"]
        if not text:
            continue

        span["text"] = text
        
        if is_heading(span,next_span, current_font_size):
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
                    "flags": span["flags"],
                    "size": span["size"],
                })

    # Save last section if it has content
    if current_heading is not None and current_content:
        if current_heading not in sections:
            sections[current_heading] = []
        sections[current_heading].extend(current_content)
    #print(sections)
    return sections

#v1
""" def build_sections(spans, current_font_size=None):

    sections = {}

    current_heading = None
    current_content = []

    for span in spans:

        text = span["text"].strip()
        font = span["font"]
        #flags = span["flags"]
        if not text:
            continue

        span["text"] = text
        if is_heading(span,current_font_size):
            
            # Save previous section
            if current_heading is not None:
                if current_heading == "miscellaneous" and current_heading in sections:
                    sections[current_heading].extend(current_content)
                else:
                    sections[current_heading] = current_content
        

            normalized = normalize_heading(text)

            if normalized in HEADING_MAP:
                current_heading = HEADING_MAP[normalized]
                current_font_size = span["size"]
                
            else:
                #########
                current_heading="miscellaneous"
                #print(current_content)
                current_font_size = span["size"]
            current_content = []
                
                
        else:
            if current_heading=="miscellaneous":
                print(current_content)
            if current_heading is not None:
                current_content.append({"text": text,"bold":("Bold" in span["font"]),"flags": span["flags"]})

    # Save last section
    if current_heading is not None:
        if current_heading == "miscellaneous" and current_heading in sections:
            sections[current_heading].extend(current_content)
        else:
            sections[current_heading] = current_content
        #sections[current_heading] = current_content
    #print(sections)
    return sections
 """

def find_headers(path):
    #spans = extract_spans(path)
    spans=extract_spans(path)
    #spans=extract_spans_pymupdf4llm(path)
   # print(spans[:100])
    font_sizes = []

    # Find all unique font sizes
    for span in spans:
        font_sizes.append(span["size"])

    font_sizes = list(set(font_sizes))
    font_sizes.sort(reverse=True)
    #print("xd2")
    print(font_sizes)
    name=extract_name(spans,font_sizes[0])
    sections = build_sections(spans,font_sizes[1])
    #print(sections)
    return sections,font_sizes[-1],name
   
    """ print("Sections found:")
    for heading, content in sections.items():
        print(f"Heading: {heading}")
        for line in content:
            print(f"  {line}")
        print("-" * 40)
     """

def group_section(items,min_font):
    grouped = {}

    current_key = None

    for item in items:
        text = item["text"].strip()

        #print(item)
        if (item["bold"]or item["flags"] >= 16) and item["size"] > min_font:  # Assuming bold text or flagged text indicates a new key
            current_key = text

            if current_key in grouped:
                i = 2
                while f"{current_key}_{i}" in grouped:
                    i += 1
                current_key = f"{current_key}_{i}"


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

""" def form_json(sections):
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=4, ensure_ascii=False)
 """
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

                # Make key unique if it already exists
                base_key = new_key
                i = 2
                while new_key in merged:
                    new_key = f"{base_key}_{i}"
                    i += 1

                merged[new_key] = value

        # Handle trailing empty keys
        if pending:
            if merged:
                last_key = next(reversed(merged))
                value = merged.pop(last_key)

                new_last_key = last_key + " " + " ".join(pending)

                # Make key unique if it already exists
                base_key = new_last_key
                i = 2
                while new_last_key in merged:
                    new_last_key = f"{base_key}_{i}"
                    i += 1

                merged[new_last_key] = value
            else:
                new_key = " ".join(pending)

                # Make key unique if it already exists
                base_key = new_key
                i = 2
                while new_key in merged:
                    new_key = f"{base_key}_{i}"
                    i += 1

                merged[new_key] = [""]

        new_data[section] = merged

    return new_data

def extract_name(spans,max_size):

    name_parts = []

    for span in spans:
        text = span["text"].strip()

        if span["size"] == max_size:
            name_parts.append(text)


       
    if not name_parts:
        return None

    return " ".join(name_parts)

def extract_basic_info(raw_text):
    

    # -----------------------------
    # Name (largest font on first page)
    # -----------------------------
    # -----------------------------
    # Email
    # -----------------------------
    email_pattern = re.compile(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    )

    email_match = email_pattern.search(raw_text)
    email = email_match.group(0) if email_match else None

    # -----------------------------
    # Phone
    # -----------------------------
    phone_pattern = re.compile(
        r"((?:\+92|0092|92|0)?[-\s]?3\d{2}[-\s]?\d{7})"
    )


    match = phone_pattern.search(raw_text)

    phone = match.group(1) if match else None
    return email,phone
    

def parse_cv(path):
    print("Parsing CV from path:", path)
    raw_text = extract_raw_text(path)
    email,phone=extract_basic_info(raw_text)
    
    sections,min_font,name = find_headers(path)
    #print(sections)
    for section_name, items in sections.items():
        sections[section_name] = group_section(items,min_font)
    sections["email"]=email
    sections["phone"]=phone
    sections["name"]=name
    sections["raw_text"] = raw_text

    #print(sections)
    merged_sections = merge_lists(sections)
    #print(merged_sections)
    merged_sections = merge_empty_keys(merged_sections)
    #print(type(merged_sections))
    #form_json(merged_sections,path)
    #form_json(merged_sections)

    return merged_sections

    