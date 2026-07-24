"""
find_relevant_exp.py

This module calculates the total relevant experience in years from a resume
based on a job description. It uses fuzzy matching for title comparison and
handles combined/compound job titles effectively.
"""

import re
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from difflib import SequenceMatcher
from dateutil.parser import parse as parse_date_util
from dateutil.parser import ParserError

import sys
from pathlib import Path

# Configuration
GAP_THRESHOLD_MONTHS = 3  # Maximum allowed gap in months before flagging
MIN_TECH_STACK_MATCH_PERCENTAGE = 10  # Minimum percentage of tech stack matches (0-100)
FUZZY_MATCH_THRESHOLD = 0.85  # Threshold for fuzzy matching (0.0 to 1.0)
JOB_TITLE_TOKEN_WEIGHT = 0.7  # Minimum token overlap ratio for partial matches

# Find tech_aliases_db.py by going up the directory tree
current = Path(__file__).parent.absolute()
for _ in range(5):
    if (current / "tech_aliases_db.py").exists():
        sys.path.insert(0, str(current))
        break
    current = current.parent

# Import from shared database
from tech_aliases_db import (
    JOB_TITLE_PREFIXES,
    TECH_STACK_ALIASES,
    COMPOUND_TECH_ALIASES,
    JOB_TITLE_MAPPINGS
)

def fuzzy_match(str1: str, str2: str, threshold: float = FUZZY_MATCH_THRESHOLD) -> bool:
    """
    Perform fuzzy matching between two strings using SequenceMatcher.
    
    Returns True if the similarity ratio exceeds the threshold.
    """
    if not str1 or not str2:
        return False
    
    # Clean strings for better matching
    str1 = str1.lower().strip()
    str2 = str2.lower().strip()
    
    # Direct match check
    if str1 == str2:
        return True
    
    # Containment is useful for full role phrases, but unsafe for short tokens
    # such as "ai" (which otherwise matches "trainee").
    shorter = min(len(str1), len(str2))
    if shorter >= 5 and (
        re.search(r"(?<!\w)" + re.escape(str1) + r"(?!\w)", str2)
        or re.search(r"(?<!\w)" + re.escape(str2) + r"(?!\w)", str1)
    ):
        return True
    
    # Use SequenceMatcher for fuzzy matching
    similarity = SequenceMatcher(None, str1, str2).ratio()
    return similarity >= threshold

def get_compound_tech_components(tech: str) -> List[str]:
    """
    Get all component technologies for a compound tech stack alias.
    Returns expanded list of technologies.
    """
    if not tech:
        return []
    
    tech_lower = tech.lower().strip()
    
    # Check if it's a compound alias
    for alias, components in COMPOUND_TECH_ALIASES.items():
        if tech_lower == alias or tech_lower in components:
            return components
    
    return [tech]

def get_tech_aliases(tech: str) -> List[str]:
    """
    Get all aliases for a given technology.
    Returns the tech itself plus all its aliases from the mapping.
    """
    if not tech:
        return []
    
    tech_lower = tech.lower().strip()
    
    # Check if it's a compound alias first
    compound_components = get_compound_tech_components(tech_lower)
    if len(compound_components) > 1 or compound_components != [tech_lower]:
        return compound_components
    
    # Direct match in aliases dictionary
    for key, aliases in TECH_STACK_ALIASES.items():
        if tech_lower == key or tech_lower in aliases:
            # Return all aliases including the key itself
            return [key] + aliases
    
    # If tech not found, return just the normalized tech
    return [tech_lower]

def is_tech_match(description: str, tech: str) -> bool:
    """
    Check if a technology appears in the description using aliases, compound matches, and fuzzy matching.
    """
    if not description or not tech:
        return False
    
    description_lower = description.lower()
    
    # Get all aliases for this tech (including compound expansions)
    aliases = get_tech_aliases(tech)
    
    # Check each alias
    for alias in aliases:
        normalized_alias = alias.strip().lower()
        if len(normalized_alias) < 3 and normalized_alias not in {"ai", "ml", "r"}:
            continue
        # Require token boundaries; raw substring checks made aliases such as
        # "ai", "py", and "it" match unrelated words.
        pattern = r'(?<!\w)' + re.escape(normalized_alias) + r'(?!\w)'
        if re.search(pattern, description_lower):
            return True
    
    # For compound tech, check if multiple components appear
    if len(aliases) > 3:  # Likely a compound alias
        matching_components = 0
        for alias in aliases:
            if len(alias) > 2 and re.search(
                r"(?<!\w)" + re.escape(alias) + r"(?!\w)", description_lower
            ):
                matching_components += 1
        
        # If at least 60% of components match, consider it a match
        if matching_components / len(aliases) >= 0.6:
            return True
    
    # Try fuzzy matching for longer tech names
    description_words = description_lower.split()
    tech_words = tech.lower().split()
    
    # If tech is a multi-word phrase, check if all words appear
    if len(tech_words) > 1:
        matching_words = sum(1 for word in tech_words if word in description_lower)
        if matching_words / len(tech_words) >= 0.6:
            return True
    
    # Try fuzzy matching on the full description (for approximate matches)
    if len(description) > 50:  # Only for substantial descriptions
        # Split into sentences and check fuzzy match
        for word in description_words:
            if len(tech) >= 5 and len(word) > 4 and fuzzy_match(tech.lower(), word, 0.88):
                return True
    
    return False

def normalize_title(title: str) -> str:
    """
    Normalize a job title by:
    1. Converting to lowercase
    2. Removing common prefixes (senior, junior, lead, etc.)
    3. Removing special characters
    4. Stripping extra whitespace
    """
    if not title:
        return ""
    
    # Convert to lowercase
    title = title.lower().strip()
    
    # Remove common prefixes using imported list
    for prefix in JOB_TITLE_PREFIXES:
        if title.startswith(prefix):
            title = title[len(prefix):]
    
    # Preserve both sides of compound titles. "AI/ML Engineer" becomes
    # "ai ml engineer", not the dangerously broad title "ai".
    title = title.replace("/", " ")

    # Remove special characters except spaces and hyphens
    title = re.sub(r'[^\w\s\-]', '', title)
    
    # Remove extra spaces
    title = ' '.join(title.split())
    
    return title

def extract_compound_titles(title: str) -> List[str]:
    """
    Extract all possible interpretations of a compound job title.
    Handles cases like "AI/ML Engineer" -> ["AI Engineer", "ML Engineer", "AI/ML Engineer"]
    """
    if not title:
        return [title]
    
    variations = [title]
    
    # Handle slash-separated compound titles
    if '/' in title:
        parts = [p.strip() for p in title.split('/') if p.strip()]
        
        if len(parts) >= 2:
            base_title = title.split('/')[-1].strip()
            role_parts = base_title.split()
            role = role_parts[-1] if role_parts else ''
            
            for part in parts:
                if part != base_title:
                    if role:
                        variations.append(f"{part} {role}")
                    else:
                        variations.append(part)
            
            combined = ' '.join(parts)
            if role and not combined.endswith(role):
                variations.append(f"{combined} {role}")
            else:
                variations.append(combined)
    
    return list(set(variations))

def is_title_match(experience_title: str, job_title: str) -> bool:
    """
    Check if an experience designation matches the job title using fuzzy matching.
    """
    if not experience_title or not job_title:
        return False
    
    normalized_exp = normalize_title(experience_title)
    normalized_job = normalize_title(job_title)
    
    if fuzzy_match(normalized_exp, normalized_job):
        return True
    
    job_variations = extract_compound_titles(job_title)
    exp_variations = extract_compound_titles(experience_title)
    
    for job_var in job_variations:
        norm_job_var = normalize_title(job_var)
        for exp_var in exp_variations:
            norm_exp_var = normalize_title(exp_var)
            if fuzzy_match(norm_exp_var, norm_job_var):
                return True
    
    canonical_keys = []
    for key, aliases in JOB_TITLE_MAPPINGS.items():
        if fuzzy_match(normalized_job, key) or any(fuzzy_match(normalized_job, alias) for alias in aliases):
            canonical_keys.append(key)
        for job_var in job_variations:
            norm_job_var = normalize_title(job_var)
            if fuzzy_match(norm_job_var, key) or any(fuzzy_match(norm_job_var, alias) for alias in aliases):
                canonical_keys.append(key)
    
    if canonical_keys:
        for key in canonical_keys:
            aliases = JOB_TITLE_MAPPINGS.get(key, [])
            for alias in aliases:
                if fuzzy_match(normalized_exp, alias):
                    return True
            for alias in aliases:
                alias_words = set(normalize_title(alias).split())
                exp_words = set(normalized_exp.split())
                if len(alias_words & exp_words) >= min(2, len(alias_words)):
                    return True
            if fuzzy_match(normalized_exp, key):
                return True
            key_words = set(normalize_title(key).split())
            exp_words = set(normalized_exp.split())
            if len(key_words & exp_words) >= min(2, len(key_words)):
                return True
    
    exp_words = set(normalized_exp.split())
    job_words = set(normalized_job.split())
    
    for job_var in job_variations:
        norm_job_var = normalize_title(job_var)
        job_var_words = set(norm_job_var.split())
        
        if len(job_var_words) > 0 and len(exp_words) > 0:
            common_words = exp_words.intersection(job_var_words)
            overlap_ratio = len(common_words) / max(len(job_var_words), len(exp_words))
            if overlap_ratio >= JOB_TITLE_TOKEN_WEIGHT:
                return True
    
    return False

def extract_tech_stack_from_description(description: str, tech_stack: List[str]) -> int:
    """
    Extract and count how many tech stack items appear in the experience description.
    Uses aliases, compound matching, and fuzzy matching for comprehensive detection.
    """
    if not description or not tech_stack:
        return 0
    
    matches = 0
    for tech in tech_stack:
        if is_tech_match(description, tech):
            matches += 1
    
    return matches

def is_experience_relevant(
    experience: Dict[str, Any], 
    job_title: str, 
    tech_stack: List[str]
) -> Tuple[bool, int]:
    """
    Determine if an experience is relevant based on:
    1. Job title matching (with fuzzy matching)
    2. Tech stack matching (percentage-based with aliases)
    """
    exp_designation = experience.get('designation', '')
    title_match = is_title_match(exp_designation, job_title)
    
    if not title_match:
        return False, 0
    
    
    if not tech_stack:
        print("Warning: No tech stack provided in JD")
        return True, 0
    
    description = experience.get('description', '')
    tech_matches = extract_tech_stack_from_description(description, tech_stack)
    
    if len(tech_stack) == 0:
        return True, 0
    
    match_percentage = (tech_matches / len(tech_stack)) * 100
    is_relevant = match_percentage >= MIN_TECH_STACK_MATCH_PERCENTAGE
    
    return is_relevant, tech_matches

def parse_date(date_str: str) -> Optional[Tuple[datetime, bool]]:
    """
    Parse date strings in various formats.
    Returns (datetime_object, is_year_only) or None if parsing fails.
    """
    if not date_str or date_str.lower() in ['present', 'current', 'now']:
        return None
    
    date_str = date_str.strip()
    is_year_only = False
    
    # Try just year format first
    year_match = re.search(r'^\s*(19|20)\d{2}\s*$', date_str)
    if year_match:
        year = int(year_match.group())
        is_year_only = True
        return datetime(year, 1, 1), is_year_only
    
    # Try common formats
    common_formats = [
        "%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y",
        "%m-%d-%Y", "%m/%d/%Y", "%b %Y", "%B %Y",
        "%b-%Y", "%B-%Y", "%Y-%b", "%Y-%B",
        "%b %d, %Y", "%B %d, %Y", "%d %b %Y", "%d %B %Y",
        "%m/%Y", "%Y/%m", "%Y-%m"
    ]
    
    for fmt in common_formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt, False
        except ValueError:
            continue
    
    # Try with regex extraction for more complex cases
    year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
    if not year_match:
        return None
    
    year = int(year_match.group())
    month = 1
    day = 1
    
    month_names = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
        'january': 1, 'february': 2, 'march': 3, 'april': 4, 'june': 6,
        'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12
    }
    
    date_lower = date_str.lower()
    for name, num in month_names.items():
        if name in date_lower:
            month = num
            break
    
    day_match = re.search(r'\b(0?[1-9]|[12][0-9]|3[01])\b', date_str)
    if day_match:
        day = int(day_match.group())
        if day > 31:
            day = 1
    
    try:
        return datetime(year, month, day), False
    except ValueError:
        return None

def get_date_as_float(date_str: str, is_end_date: bool = False) -> Optional[float]:
    """
    Convert date string to float (year.month_fraction).
    If is_end_date is True and date is year-only, use Dec 31.
    """
    if not date_str:
        return None
    
    # Handle 'present', 'current', 'now'
    if date_str.lower() in ['present', 'current', 'now']:
        now = datetime.now()
        return now.year + (now.month - 1) / 12 + (now.day - 1) / 365
    
    parsed = parse_date(date_str)
    if not parsed:
        return None
    
    dt, is_year_only = parsed
    
    if is_year_only:
        if is_end_date:
            # Year-only end date: use Dec 31
            return dt.year + 11/12  # December
        else:
            # Year-only start date: use Jan 1
            return dt.year
    else:
        # Full date: use exact month/day
        return dt.year + (dt.month - 1) / 12 + (dt.day - 1) / 365

def calculate_overlap_adjusted_months(
    relevant_start: str, 
    relevant_end: str, 
    all_experiences: List[Dict[str, Any]]
) -> float:
    """
    Calculate months for a relevant experience, adjusting for overlaps with irrelevant experiences.
    If there's an overlap with irrelevant experience and months/days aren't specified,
    split the year evenly.
    """
    # Get relevant date range as floats
    start_float = get_date_as_float(relevant_start, is_end_date=False)
    end_float = get_date_as_float(relevant_end, is_end_date=True)
    
    if start_float is None or end_float is None:
        return 0.0
    
    # Check for overlaps with irrelevant experiences
    for exp in all_experiences:
        # Skip if this is the same relevant experience
        if exp.get('start_date') == relevant_start and exp.get('end_date') == relevant_end:
            continue
        
        # Check if this experience is irrelevant (or we're checking all for adjustment)
        exp_start = get_date_as_float(exp.get('start_date', ''), is_end_date=False)
        exp_end = get_date_as_float(exp.get('end_date', ''), is_end_date=True)
        
        if exp_start is None or exp_end is None:
            continue
        
        # Check for overlap
        overlap_start = max(start_float, exp_start)
        overlap_end = min(end_float, exp_end)
        
        if overlap_start < overlap_end:
            # There is an overlap
            # Check if the relevant dates are year-only and irrelevant has year-only
            start_parsed = parse_date(relevant_start)
            end_parsed = parse_date(relevant_end)
            exp_start_parsed = parse_date(exp.get('start_date', ''))
            exp_end_parsed = parse_date(exp.get('end_date', ''))
            
            # If both are year-only and they share the same year, split the year
            if (start_parsed and start_parsed[1] and 
                end_parsed and end_parsed[1] and
                exp_start_parsed and exp_start_parsed[1] and
                exp_end_parsed and exp_end_parsed[1]):
                
                # Check if the overlap is exactly a full year
                if int(overlap_start) == int(overlap_end):
                    # Split the year: half for relevant, half for irrelevant
                    overlap_year = int(overlap_start)
                    # If relevant starts in that year and irrelevant also has that year
                    if int(start_float) == overlap_year and int(exp_start) == overlap_year:
                        # Move relevant start to July 1 of that year (half year)
                        start_float = overlap_year + 0.5  # July
    
    # Calculate months
    months = (end_float - start_float) * 12
    
    return max(0, months)

def detect_gaps(experiences: List[Dict[str, Any]]) -> Tuple[bool, List[Dict[str, Any]]]:
    """
    Detect gaps in work experience that exceed the threshold.
    Returns (gap_found, list_of_gaps)
    """
    if not experiences or len(experiences) < 2:
        return False, []
    
    # Get all experiences with valid dates, sorted by start date
    valid_experiences = []
    for exp in experiences:
        start = exp.get('start_date', '')
        if not start:
            continue
        
        start_float = get_date_as_float(start, is_end_date=False)
        end_float = get_date_as_float(exp.get('end_date', ''), is_end_date=True)
        
        if start_float is not None and end_float is not None:
            valid_experiences.append({
                'company': exp.get('company', ''),
                'designation': exp.get('designation', ''),
                'start': start_float,
                'end': end_float,
                'start_date': start,
                'end_date': exp.get('end_date', '')
            })
    
    if len(valid_experiences) < 2:
        return False, []
    
    # Sort by start date
    valid_experiences.sort(key=lambda x: x['start'])
    
    gaps = []
    for i in range(len(valid_experiences) - 1):
        current_end = valid_experiences[i]['end']
        next_start = valid_experiences[i + 1]['start']
        
        # Calculate gap in months
        gap_months = (next_start - current_end) * 12
        
        # Check if there's a gap (positive gap means gap, negative means overlap)
        if gap_months > GAP_THRESHOLD_MONTHS:
            gaps.append({
                'from_company': valid_experiences[i]['company'],
                'from_designation': valid_experiences[i]['designation'],
                'from_end': valid_experiences[i]['end_date'],
                'to_company': valid_experiences[i + 1]['company'],
                'to_designation': valid_experiences[i + 1]['designation'],
                'to_start': valid_experiences[i + 1]['start_date'],
                'gap_months': gap_months,
                'gap_years': gap_months / 12
            })
    
    return len(gaps) > 0, gaps

def find_relevant_experience(
    job_json: Dict[str, Any], 
    resume_json: Dict[str, Any]
) -> Tuple[float, bool, List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Main function to calculate total relevant experience in years.
    Handles overlapping date ranges properly and detects gaps.
    
    Returns:
        Tuple[float, bool, List[Dict], List[Dict]]:
        - total_relevant_years: Total relevant experience in years
        - gap_found: True if gap > threshold detected
        - gaps: List of gap details
        - experience_evaluations: Per-role relevance breakdown
    """
    job_title = job_json.get('job_title', '')
    tech_stack = job_json.get('tech_stack', [])
    tech_stack_size = len(tech_stack) if isinstance(tech_stack, list) else 0
    
    if not job_title:
        print("Warning: No job title provided in JD")
        return 0.0, False, [], []
    
    experiences = resume_json.get('experience', [])
    
    if not experiences:
        print("No experience entries found in resume")
        return 0.0, False, [], []
    
    # Check for gaps in complete work experience
    gap_found, gaps = detect_gaps(experiences)
    
    # Collect relevant experiences
    relevant_experiences = []
    relevant_count = 0
    experience_evaluations: List[Dict[str, Any]] = []
    
    print(f"\n🔍 Checking experiences for job title: '{job_title}'")
    print(f"Tech stack criteria: {tech_stack}")
    print(f"Tech stack match threshold: {MIN_TECH_STACK_MATCH_PERCENTAGE}%")
    print(f"Gap detection threshold: {GAP_THRESHOLD_MONTHS} months")
    print("-" * 60)
    
    # First, identify all relevant experiences
    for exp in experiences:
        is_relevant, tech_matches = is_experience_relevant(exp, job_title, tech_stack)
        
        exp_designation = exp.get('designation', '')
        exp_company = exp.get('company', '')
        start_date = exp.get('start_date', '')
        end_date = exp.get('end_date', '')
        title_match = is_title_match(exp_designation, job_title)
        match_percentage = (tech_matches / tech_stack_size * 100) if tech_stack_size else 0.0
        reason = "title_mismatch"
        
        if is_relevant:
            # Calculate months for display (simple calculation)
            start_float = get_date_as_float(start_date, is_end_date=False)
            end_float = get_date_as_float(end_date, is_end_date=True)
            
            if start_float is not None and end_float is not None:
                months = (end_float - start_float) * 12
                if months > 0:
                    relevant_experiences.append({
                        'designation': exp_designation,
                        'company': exp_company,
                        'start_date': start_date,
                        'end_date': end_date,
                        'months': months,
                        'tech_matches': tech_matches,
                        'start_float': start_float,
                        'end_float': end_float
                    })
                    relevant_count += 1
                    reason = "relevant"
                    print(f"✅ Relevant #{relevant_count}: {exp_designation} at {exp_company}")
                    print(f"   - Tech matches: {tech_matches}/{len(tech_stack)} ({match_percentage:.1f}%)")
                    print(f"   - Duration: {months/12:.2f} years")
                else:
                    is_relevant = False
                    reason = "invalid_dates"
                    print(f"⚠️  Relevant but invalid dates: {exp_designation} at {exp_company}")
            else:
                is_relevant = False
                reason = "invalid_dates"
                print(f"⚠️  Relevant but invalid dates: {exp_designation} at {exp_company}")
        else:
            if not title_match:
                reason = "title_mismatch"
                print(f"❌ {exp_designation} at {exp_company} - Title mismatch")
            else:
                reason = "tech_below_threshold"
                print(f"❌ {exp_designation} at {exp_company} - Tech mismatch (matches: {tech_matches}/{len(tech_stack)}, {match_percentage:.1f}% < {MIN_TECH_STACK_MATCH_PERCENTAGE}%)")

        experience_evaluations.append({
            "company": exp_company,
            "designation": exp_designation,
            "start_date": start_date,
            "end_date": end_date,
            "is_relevant": bool(is_relevant and reason == "relevant"),
            "title_match": bool(title_match),
            "tech_matches": int(tech_matches or 0),
            "tech_stack_size": tech_stack_size,
            "match_percentage": round(float(match_percentage), 1),
            "reason": reason,
        })
    
    # Calculate relevant experience with overlap handling
    total_months = 0.0
    
    if relevant_experiences:
        # Get all experience ranges (including irrelevant) for overlap adjustment
        all_experiences = resume_json.get('experience', [])
        
        # Sort relevant experiences by start date
        relevant_experiences.sort(key=lambda x: x['start_float'])
        
        # Merge overlapping relevant experiences first
        merged_ranges = []
        current_start = relevant_experiences[0]['start_float']
        current_end = relevant_experiences[0]['end_float']
        current_exp = relevant_experiences[0]
        
        for i in range(1, len(relevant_experiences)):
            exp = relevant_experiences[i]
            
            # Check if this experience overlaps with current range
            if exp['start_float'] <= current_end:
                # Overlap - extend the end if needed
                if exp['end_float'] > current_end:
                    current_end = exp['end_float']
            else:
                # No overlap - save current range and start new
                merged_ranges.append({
                    'start': current_start,
                    'end': current_end,
                    'start_date': current_exp['start_date'],
                    'end_date': current_exp['end_date'] if current_exp['end_date'] else None,
                    'exp': current_exp
                })
                current_start = exp['start_float']
                current_end = exp['end_float']
                current_exp = exp
        
        # Add the last range
        merged_ranges.append({
            'start': current_start,
            'end': current_end,
            'start_date': current_exp['start_date'],
            'end_date': current_exp['end_date'] if current_exp['end_date'] else None,
            'exp': current_exp
        })
        
        # Calculate total months from merged ranges, adjusting for overlaps with irrelevant
        for merged_range in merged_ranges:
            # For each merged range, check overlaps with irrelevant experiences
            start_float = merged_range['start']
            end_float = merged_range['end']
            
            # Check if there are irrelevant experiences overlapping with this range
            for exp in all_experiences:
                # Check if this experience is relevant
                is_rel, _ = is_experience_relevant(exp, job_title, tech_stack)
                if is_rel:
                    continue  # Skip relevant experiences (already handled)
                
                # Check overlap with this irrelevant experience
                exp_start = get_date_as_float(exp.get('start_date', ''), is_end_date=False)
                exp_end = get_date_as_float(exp.get('end_date', ''), is_end_date=True)
                
                if exp_start is None or exp_end is None:
                    continue
                
                # Calculate overlap
                overlap_start = max(start_float, exp_start)
                overlap_end = min(end_float, exp_end)
                
                if overlap_start < overlap_end:
                    # There's an overlap with an irrelevant experience
                    # Check if the relevant range is year-only and irrelevant is year-only
                    start_parsed = parse_date(merged_range['start_date'])
                    exp_start_parsed = parse_date(exp.get('start_date', ''))
                    
                    # If both are year-only, split the year
                    if (start_parsed and start_parsed[1] and 
                        exp_start_parsed and exp_start_parsed[1]):
                        # Both are year-only - split the overlapping year
                        overlap_year = int(overlap_start)
                        if int(start_float) == overlap_year and int(exp_start) == overlap_year:
                            # Split the year: move relevant start to July 1
                            start_float = overlap_year + 0.5  # July
            
            # Calculate months for this range
            months = (end_float - start_float) * 12
            if months > 0:
                total_months += months
    
    # Convert to years
    total_years = total_months / 12
    
    print("-" * 60)
    
    # Show overlap details if there are multiple relevant experiences
    if len(relevant_experiences) > 1:
        print(f"📊 Overlap handling: {len(relevant_experiences)} relevant experiences merged")
        individual_total = sum([exp['months'] for exp in relevant_experiences])
        print(f"   Individual durations would be: {individual_total/12:.2f} years")
        print(f"   Total after overlap handling: {total_years:.2f} years")
    
    # Show gap information
    if gap_found:
        print(f"\n⚠️  GAP FOUND: {len(gaps)} gap(s) exceeding {GAP_THRESHOLD_MONTHS} months:")
        for gap in gaps:
            print(f"   - {gap['gap_months']:.1f} months ({gap['gap_years']:.1f} years) between")
            print(f"     {gap['from_designation']} at {gap['from_company']} (ended {gap['from_end']})")
            print(f"     and {gap['to_designation']} at {gap['to_company']} (started {gap['to_start']})")
    else:
        print(f"\n✅ No gaps detected exceeding {GAP_THRESHOLD_MONTHS} months")
    
    print(f"\n📊 Total relevant experience: {total_years:.2f} years")
    print(f"📊 Number of relevant experiences: {relevant_count}")
    
    return total_years, gap_found, gaps, experience_evaluations


if __name__ == "__main__":
    # Test Case 1: Irrelevant 2023-2024, Relevant 2024-2026 (year-only)
    test_case_1 = {
        "job": {
            "job_title": "Agentic AI Engineer",
            "tech_stack": ["Python", "FastAPI", "PostgreSQL", "Docker","Langchain", "LlamaIndex", "OpenAI API","machine learning"]
        },
        "resume": {
            "experience": [
                {
                    "company": "Irrelevant Corp",
                    "designation": "AI Engineer",
                    "start_date": "2023",
                    "end_date": "2024",
                    "description": "Built voice agents using Flask, Docker , Langgraph, etc"
                }
            ]
        }
    }
    
    
    
    print("🧪 Running Test Cases\n" + "="*80)
    
    test_cases = [test_case_1]
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"📝 Test Case {i}")
        print(f"{'='*80}")
        result, gap_found, gaps, evaluations = find_relevant_experience(test["job"], test["resume"])
        print(f"\n🎯 Final Result: {result:.2f} years of relevant experience")
        print(f"🎯 Gap Found: {gap_found}")
        print(f"🎯 Evaluations: {len(evaluations)}")
        if gaps:
            print(f"🎯 Number of gaps: {len(gaps)}")
    
    print("\n✅ All test cases completed!")