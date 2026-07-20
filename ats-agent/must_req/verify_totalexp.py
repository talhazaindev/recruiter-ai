"""
verify_totalexp.py - Module to verify if candidate meets minimum total experience requirement
Handles overlapping date ranges, year-only dates, and gap detection.
"""

import json
from datetime import datetime
from typing import Dict, Any, Tuple, List, Optional
from pathlib import Path
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
GAP_THRESHOLD_MONTHS = 3  # Maximum allowed gap in months before flagging


def load_json(file_path: Path) -> Dict[str, Any]:
    """
    Load JSON file and return dictionary.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Dictionary containing JSON data
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_date(date_str: Optional[str]) -> Optional[Tuple[datetime, bool]]:
    """
    Parse date string into datetime object with support for multiple formats.
    Returns (datetime_object, is_year_only) or None if parsing fails.
    """
    if not date_str or not isinstance(date_str, str):
        return None
    
    # Clean the string
    date_str = date_str.strip()
    
    # Handle "Present" as current date
    if date_str.lower() in ['present', 'current', 'now']:
        return datetime.now(), False
    
    # Check if it's year-only format
    year_match = re.search(r'^\s*(19|20)\d{2}\s*$', date_str)
    if year_match:
        year = int(year_match.group())
        return datetime(year, 1, 1), True
    
    # Supported date formats (add more as needed)
    date_formats = [
        '%Y-%m-%d',        # 2023-01-15
        '%Y/%m/%d',        # 2023/01/15
        '%m/%d/%Y',        # 01/15/2023
        '%d/%m/%Y',        # 15/01/2023
        '%d-%m-%Y',        # 15-01-2023
        '%B %Y',           # January 2023
        '%b %Y',           # Jan 2023
        '%Y-%m',           # 2023-01
        '%m/%Y',           # 01/2023
        '%B %d, %Y',       # January 15, 2023
        '%b %d, %Y',       # Jan 15, 2023
        '%d %B %Y',        # 15 January 2023
        '%d %b %Y',        # 15 Jan 2023
    ]
    
    for date_format in date_formats:
        try:
            dt = datetime.strptime(date_str, date_format)
            return dt, False
        except (ValueError, TypeError):
            continue
    
    # Try to extract year and month from string
    year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
    if not year_match:
        logger.warning(f"Could not parse date: '{date_str}'")
        return None
    
    year = int(year_match.group())
    month = 1
    day = 1
    
    # Try to extract month
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
    
    # Try to extract day
    day_match = re.search(r'\b(0?[1-9]|[12][0-9]|3[01])\b', date_str)
    if day_match:
        day = int(day_match.group())
        if day > 31:
            day = 1
    
    try:
        return datetime(year, month, day), False
    except ValueError:
        logger.warning(f"Could not parse date: '{date_str}'")
        return None


def get_date_as_float(date_str: Optional[str], is_end_date: bool = False) -> Optional[float]:
    """
    Convert date string to float (year.month_fraction).
    If is_end_date is True and date is year-only, use Dec 31.
    """
    if not date_str:
        return None
    
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


def calculate_experience_months(
    experiences: List[Dict[str, Any]]
) -> Tuple[float, int, int, bool, List[Dict[str, Any]]]:
    """
    Calculate total experience in months from list of experience entries.
    Handles overlapping dates, year-only dates, and gap detection.
    
    Returns:
        Tuple of (total_months, valid_entries, skipped_entries, gap_found, gaps)
    """
    if not experiences or not isinstance(experiences, list):
        return 0.0, 0, 0, False, []
    
    # Parse all experiences into date ranges
    parsed_experiences = []
    skipped_entries = 0
    
    for exp in experiences:
        if not isinstance(exp, dict):
            skipped_entries += 1
            continue
        
        start_date = exp.get('start_date', '')
        end_date = exp.get('end_date', '')
        
        # If start date is missing, skip this experience
        if not start_date or not isinstance(start_date, str) or start_date.strip() == '':
            skipped_entries += 1
            logger.debug(f"Skipping experience: Missing start date - {exp.get('company', 'Unknown')}")
            continue
        
        start_float = get_date_as_float(start_date, is_end_date=False)
        end_float = get_date_as_float(end_date, is_end_date=True)
        
        # A genuinely omitted end date means current employment. An invalid
        # non-empty date is uncertain and must not inflate experience.
        if end_float is None:
            if not str(end_date or "").strip():
                now = datetime.now()
                end_float = now.year + (now.month - 1) / 12 + (now.day - 1) / 365
            else:
                skipped_entries += 1
                continue
        
        if start_float is not None and end_float is not None:
            if end_float < start_float:
                skipped_entries += 1
                logger.warning(
                    "Skipping reversed experience range for %s",
                    exp.get("company", "Unknown"),
                )
                continue
            parsed_experiences.append({
                'company': exp.get('company', ''),
                'designation': exp.get('designation', ''),
                'start': start_float,
                'end': end_float,
                'start_date': start_date,
                'end_date': end_date
            })
        else:
            skipped_entries += 1
            logger.debug(f"Skipping experience: Could not parse dates - {exp.get('company', 'Unknown')}")
    
    # Sort by start date
    parsed_experiences.sort(key=lambda x: x['start'])
    
    # Detect gaps
    gap_found, gaps = detect_gaps(experiences)
    
    if not parsed_experiences:
        return 0.0, 0, skipped_entries, gap_found, gaps
    
    # Merge overlapping ranges
    merged_ranges = []
    current_start = parsed_experiences[0]['start']
    current_end = parsed_experiences[0]['end']
    
    for i in range(1, len(parsed_experiences)):
        exp = parsed_experiences[i]
        
        if exp['start'] <= current_end:
            # Overlap - extend the end if needed
            if exp['end'] > current_end:
                current_end = exp['end']
        else:
            # No overlap - save current range and start new
            merged_ranges.append({
                'start': current_start,
                'end': current_end
            })
            current_start = exp['start']
            current_end = exp['end']
    
    # Add the last range
    merged_ranges.append({
        'start': current_start,
        'end': current_end
    })
    
    # Calculate total months from merged ranges
    total_months = 0.0
    for range_data in merged_ranges:
        months = (range_data['end'] - range_data['start']) * 12
        if months > 0:
            total_months += months
    
    return total_months, len(parsed_experiences), skipped_entries, gap_found, gaps


def verify_total_experience(
    resume: Dict[str, Any],
    jd: Dict[str, Any],
    return_details: bool = False
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Verify if candidate meets minimum total experience requirement.
    
    Args:
        resume: Resume dictionary
        jd: Job description dictionary
        return_details: If True, return detailed information
        
    Returns:
        If return_details is False: Tuple of (is_qualified, None)
        If return_details is True: Tuple of (is_qualified, details_dict)
        
        details_dict contains:
            - message: Success/error message
            - required_years: Minimum required years from JD
            - total_years: Calculated total years of experience
            - valid_entries: Number of valid experience entries counted
            - total_entries: Total number of experience entries in resume
            - skipped_entries: Number of skipped entries
            - gap_found: True if gap > threshold detected
            - gaps: List of gap details
            - failed_checks: List of failed validation checks
            - failure_reason: Detailed failure reason if not qualified
    """
    details = {
        'message': '',
        'required_years': None,
        'total_years': None,
        'valid_entries': 0,
        'total_entries': 0,
        'skipped_entries': 0,
        'gap_found': False,
        'gaps': [],
        'failed_checks': [],
        'failure_reason': ''
    }
    
    try:
        # Extract required experience from JD
        requirements = jd.get('requirements_must_have', {})
        experience_req = requirements.get('experience', {})
        required_years = experience_req.get('minimum_total_years')
        
        if required_years is None or required_years == 0:
            details['message'] = "No minimum experience requirement specified in JD"
            if return_details:
                return True, details
            return True, None
        
        # Ensure required_years is a number
        try:
            required_years = float(required_years)
            details['required_years'] = required_years
        except (ValueError, TypeError):
            error_msg = f"Invalid required experience value: {required_years}"
            details['message'] = error_msg
            details['failed_checks'].append('invalid_requirement')
            details['failure_reason'] = error_msg
            if return_details:
                return False, details
            return False, None
        
        # Extract experiences from resume
        experiences = resume.get('experience', [])
        details['total_entries'] = len(experiences) if isinstance(experiences, list) else 0
        
        if not experiences or not isinstance(experiences, list):
            error_msg = "No experience found in resume"
            details['message'] = error_msg
            details['failed_checks'].append('no_experience')
            details['failure_reason'] = error_msg
            if return_details:
                return False, details
            return False, None
        
        # Calculate total experience with overlap handling
        total_months, valid_entries, skipped_entries, gap_found, gaps = calculate_experience_months(experiences)
        total_years = total_months / 12
        
        details['total_years'] = total_years
        details['valid_entries'] = valid_entries
        details['skipped_entries'] = skipped_entries
        details['gap_found'] = gap_found
        details['gaps'] = gaps
        
        # If no valid experience entries found
        if valid_entries == 0:
            error_msg = "No valid experience entries found (all entries missing start dates)"
            details['message'] = error_msg
            details['failed_checks'].append('no_valid_experience')
            details['failure_reason'] = error_msg
            if return_details:
                return False, details
            return False, None
        
        # Check if meets requirement
        if total_years >= required_years:
            gap_msg = f" | Gaps found: {len(gaps)}" if gap_found else " | No gaps detected"
            details['message'] = (f"Qualified: {total_years:.2f} years experience "
                                 f"(Required: {required_years:.2f} years) "
                                 f"[{valid_entries} valid entries, {skipped_entries} skipped]{gap_msg}")
            if return_details:
                return True, details
            return True, None
        else:
            gap_msg = f" | Gaps found: {len(gaps)}" if gap_found else " | No gaps detected"
            error_msg = (f"Not qualified: {total_years:.2f} years experience "
                        f"(Required: {required_years:.2f} years)"
                        f"[{valid_entries} valid entries, {skipped_entries} skipped]{gap_msg}")
            details['message'] = error_msg
            details['failed_checks'].append('insufficient_experience')
            details['failure_reason'] = f"Experience {total_years:.2f} < Required {required_years:.2f}"
            if return_details:
                return False, details
            return False, None
            
    except Exception as e:
        error_msg = f"Error verifying experience: {str(e)}"
        logger.error(error_msg)
        details['message'] = error_msg
        details['failed_checks'].append('verification_error')
        details['failure_reason'] = error_msg
        if return_details:
            return False, details
        return False, None


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    jd_folder = repo_root / "JD-jsons"
    resume_folder = repo_root / "Resumes-jsons"

    jd_files = list(jd_folder.glob("*.json"))
    resume_files = list(resume_folder.glob("*.json"))

    if not jd_files:
        raise SystemExit(f"No JD JSON files found in {jd_folder}")

    jd = load_json(jd_files[0])
    print(f"Using JD: {jd_files[0].name}")
    print(f"Gap threshold: {GAP_THRESHOLD_MONTHS} months")
    print("=" * 80)

    for resume_file in resume_files:
        resume = load_json(resume_file)
        passed, details = verify_total_experience(resume, jd, return_details=True)
        
        print(f"\n📄 {resume_file.name}")
        print(f"   Passed: {passed}")
        print(f"   Total Experience: {details.get('total_years', 0):.2f} years")
        print(f"   Required: {details.get('required_years', 0):.2f} years")
        print(f"   Valid Entries: {details.get('valid_entries', 0)}")
        print(f"   Skipped Entries: {details.get('skipped_entries', 0)}")
        print(f"   Gap Found: {details.get('gap_found', False)}")
        
        if details.get('gap_found', False):
            gaps = details.get('gaps', [])
            print(f"   Number of Gaps: {len(gaps)}")
            for i, gap in enumerate(gaps, 1):
                print(f"      Gap {i}: {gap['gap_months']:.1f} months ({gap['gap_years']:.1f} years)")
                print(f"         Between: {gap['from_designation']} at {gap['from_company']} (ended {gap['from_end']})")
                print(f"         And: {gap['to_designation']} at {gap['to_company']} (started {gap['to_start']})")
        
        print(f"   Message: {details.get('message', 'N/A')}")