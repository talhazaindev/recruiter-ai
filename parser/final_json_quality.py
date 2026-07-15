import re

EXPECTED_EXPERIENCE_FIELDS = [
    "company",
    "designation",
    "start_date",
    "end_date",
    "description"
]

EXPECTED_EDUCATION_FIELDS = [
    "degree",
    "institution",
    "cgpa",
    "graduation_date"
]

EXPECTED_SECTIONS = [
    "skills",
    "experience",
    "projects",
    "education",
    "certifications"
]

def score_sections(parsed_json: dict):

    score_per_section = 30 / len(EXPECTED_SECTIONS)

    score = 0

    missing = []

    for section in EXPECTED_SECTIONS:

        value = parsed_json.get(section)

        if value:
            score += score_per_section
        else:
            missing.append(section)

    return round(score,2), missing

def extract_words(data, include_keys=True):
    """
    Recursively extracts words from nested dicts/lists.

    Parameters
    ----------
    include_keys : bool
        Whether dictionary keys should also be counted.
    """

    words = []

    if data is None:
        return words

    if isinstance(data, str):
        words.extend(re.findall(r"\b\w+\b", data))

    elif isinstance(data, list):
        for item in data:
            words.extend(extract_words(item, include_keys))

    elif isinstance(data, dict):

        for key, value in data.items():

            if include_keys:
                words.extend(re.findall(r"\b\w+\b", str(key)))

            words.extend(extract_words(value, include_keys))

    else:
        words.extend(re.findall(r"\b\w+\b", str(data)))

    return words

def word_count(text: str) -> int:
    if not text:
        return 0

    return len(re.findall(r"\b\w+\b", str(text)))

def score_raw_text_coverage(parsed_json):

    raw_text = parsed_json.get("raw_text", "")
    raw_words = word_count(raw_text)

    structured_words = []

    # Count subsection names
    structured_words.extend(
        extract_words(parsed_json.get("skills", {}), include_keys=True)
    )

    structured_words.extend(
        extract_words(parsed_json.get("projects", {}), include_keys=True)
    )

    structured_words.extend(
        extract_words(parsed_json.get("certifications", {}), include_keys=True)
    )

    # Ignore schema keys
    structured_words.extend(
        extract_words(parsed_json.get("experience", []), include_keys=False)
    )

    structured_words.extend(
        extract_words(parsed_json.get("education", []), include_keys=False)
    )

    if not raw_words:
        return 0, 0

    coverage = len(structured_words) / len(raw_words)

    score = min(coverage, 1.0) * 40

    return round(score, 2), round(coverage * 100, 2)

def score_subsections(parsed_json):

    total_fields = 0
    filled_fields = 0

    # Experience

    for exp in parsed_json.get("experience", []):

        for field in EXPECTED_EXPERIENCE_FIELDS:

            total_fields += 1

            if str(exp.get(field, "")).strip():
                filled_fields += 1

    # Education

    for edu in parsed_json.get("education", []):

        for field in EXPECTED_EDUCATION_FIELDS:

            total_fields += 1

            if str(edu.get(field, "")).strip():
                filled_fields += 1

    if total_fields == 0:
        return 0, 0

    completeness = filled_fields / total_fields

    score = completeness * 30

    return round(score,2), round(completeness * 100,2)

def calculate_quality_score(parsed_json):

    raw_score, coverage = score_raw_text_coverage(parsed_json)

    section_score, missing = score_sections(parsed_json)

    subsection_score, subsection_completion = score_subsections(parsed_json)

    total_score = raw_score + section_score + subsection_score

    return {

        "quality_score": round(total_score,2),

        "raw_text_coverage": coverage,

        "section_score": round(section_score,2),

        "missing_sections": missing,

        "subsection_score": round(subsection_score,2),

        "subsection_completion": subsection_completion
    }
