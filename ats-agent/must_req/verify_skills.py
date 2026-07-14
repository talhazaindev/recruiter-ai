# verify_skills.py
"""
Module to verify if candidate possesses all required skills.
Supports comprehensive skill matching including HR, Business Development,
and other professional skills.
"""

import json
import re
from typing import Dict, Any, Tuple, List, Optional, Set
from pathlib import Path
import logging
from difflib import SequenceMatcher

# Import skill database
from .skills_db import (
    COMMON_VARIATIONS,
    SKILL_CATEGORIES,
    get_skill_variations,
    get_skills_by_category,
    is_hr_skill,
    is_business_skill,
    is_management_skill,
    is_technical_skill
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


def normalize_text(text: str) -> str:
    """
    Normalize text by converting to lowercase and removing extra spaces.
    
    Args:
        text: Input text string
        
    Returns:
        Normalized text
    """
    if not text:
        return ""
    return ' '.join(text.lower().split())


def get_synonyms(skill: str) -> List[str]:
    """
    Get all synonyms/variations for a skill from the common variations dictionary.
    
    Args:
        skill: Skill to look up
        
    Returns:
        List of synonyms for the skill
    """
    skill_lower = skill.lower().strip()
    
    # Direct match in common variations
    if skill_lower in COMMON_VARIATIONS:
        return COMMON_VARIATIONS[skill_lower]
    
    # Check if any key is a substring of the skill (e.g., "react native" contains "react")
    matching_synonyms = []
    for key, variants in COMMON_VARIATIONS.items():
        if key in skill_lower or skill_lower in key:
            matching_synonyms.extend(variants)
    
    return list(set(matching_synonyms))  # Remove duplicates


def generate_skill_variations(skill: str) -> Set[str]:
    """
    Generate various forms of a skill for flexible matching.
    
    Args:
        skill: Original skill string
        
    Returns:
        Set of skill variations
    """
    variations = set()
    
    if not skill:
        return variations
    
    # Clean and normalize the skill
    skill_clean = skill.strip().lower()
    variations.add(skill_clean)
    
    # Add synonyms from common variations
    synonyms = get_synonyms(skill_clean)
    variations.update(synonyms)
    
    # Remove common punctuation
    skill_no_punct = re.sub(r'[^\w\s]', '', skill_clean)
    variations.add(skill_no_punct)
    
    # Remove extra spaces
    skill_single_space = ' '.join(skill_clean.split())
    variations.add(skill_single_space)
    
    # Handle compound words (e.g., "machine learning" -> "machinelearning")
    skill_compound = skill_single_space.replace(' ', '')
    if skill_compound != skill_single_space:
        variations.add(skill_compound)
    
    # Handle hyphenated versions (e.g., "machine-learning")
    skill_hyphen = skill_single_space.replace(' ', '-')
    if skill_hyphen != skill_single_space:
        variations.add(skill_hyphen)
    
    # Handle underscore versions (e.g., "machine_learning")
    skill_underscore = skill_single_space.replace(' ', '_')
    if skill_underscore != skill_single_space:
        variations.add(skill_underscore)
    
    # Handle camel case variations
    if ' ' in skill_single_space:
        # e.g., "machine learning" -> "MachineLearning"
        camel = ''.join(word.capitalize() for word in skill_single_space.split())
        variations.add(camel.lower())
        
        # e.g., "machine learning" -> "Machine Learning"
        title_case = ' '.join(word.capitalize() for word in skill_single_space.split())
        variations.add(title_case.lower())
    
    # Handle common abbreviations (if skill has multiple words, take first letters)
    words = skill_single_space.split()
    if len(words) > 1:
        # e.g., "machine learning" -> "ml"
        acronym = ''.join(word[0] for word in words if word)
        if len(acronym) > 1:
            variations.add(acronym)
    
    # Handle plurals
    if skill_clean.endswith('s'):
        singular = skill_clean[:-1]
        variations.add(singular)
    else:
        # Add plural form
        if skill_clean.endswith('y'):
            plural = skill_clean[:-1] + 'ies'
            variations.add(plural)
        elif skill_clean.endswith('s') or skill_clean.endswith('x') or skill_clean.endswith('z'):
            plural = skill_clean + 'es'
            variations.add(plural)
        elif skill_clean.endswith('ch') or skill_clean.endswith('sh'):
            plural = skill_clean + 'es'
            variations.add(plural)
        else:
            plural = skill_clean + 's'
            variations.add(plural)
    
    # Add variations with "ing" suffix
    if not skill_clean.endswith('ing'):
        variations.add(skill_clean + 'ing')
    
    # Add variations with "er" suffix
    if not skill_clean.endswith('er'):
        variations.add(skill_clean + 'er')
    
    # Add variations with "ed" suffix
    if not skill_clean.endswith('ed'):
        if skill_clean.endswith('e'):
            variations.add(skill_clean + 'd')
        else:
            variations.add(skill_clean + 'ed')
    
    # Remove empty strings and duplicates
    return {v for v in variations if v}


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity ratio between two strings using SequenceMatcher.
    
    Args:
        text1: First string
        text2: Second string
        
    Returns:
        Similarity ratio between 0 and 1
    """
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def check_skill_in_text(
    skill: str, 
    text: str, 
    use_word_boundaries: bool = True,
    use_fuzzy_matching: bool = True,
    fuzzy_threshold: float = 0.85
) -> Tuple[bool, Set[str], Set[str], str]:
    """
    Check if a skill (or its variations) appears in the text with fuzzy matching.
    
    Args:
        skill: Skill to check
        text: Resume text to search in
        use_word_boundaries: If True, use word boundaries for exact matching
        use_fuzzy_matching: If True, use fuzzy matching for typos
        fuzzy_threshold: Similarity threshold for fuzzy matching (0-1)
        
    Returns:
        Tuple of (found, variations_found, variations_checked, match_type)
        match_type: 'exact', 'word_boundary', 'substring', 'fuzzy', 'none'
    """
    if not skill or not text:
        return False, set(), set(), 'none'
    
    # Normalize text
    normalized_text = normalize_text(text)
    
    # Generate variations
    variations = generate_skill_variations(skill)
    
    # Check each variation with different strategies
    found_variations = set()
    match_type = 'none'
    
    # Strategy 1: Word boundary matching (most accurate)
    if use_word_boundaries:
        for variation in variations:
            if variation:
                pattern = r'\b' + re.escape(variation) + r'\b'
                if re.search(pattern, normalized_text):
                    found_variations.add(variation)
                    match_type = 'word_boundary'
        
        if found_variations:
            return True, found_variations, variations, match_type
    
    # Strategy 2: Substring matching (for compound words)
    for variation in variations:
        if variation and variation in normalized_text:
            found_variations.add(variation)
            if match_type != 'word_boundary':
                match_type = 'substring'
    
    if found_variations:
        return True, found_variations, variations, match_type
    
    # Strategy 3: Fuzzy matching (for typos)
    if use_fuzzy_matching:
        # Clean text by removing special characters and splitting into words
        cleaned_text = re.sub(r'[^\w\s]', '', normalized_text)
        words = cleaned_text.split()
        
        # Check each variation against each word
        for variation in variations:
            if not variation:
                continue
            
            # Check if variation is similar to any word
            for word in words:
                similarity = calculate_similarity(variation, word)
                if similarity >= fuzzy_threshold:
                    found_variations.add(variation)
                    match_type = 'fuzzy'
                    break
            
            # Also check against the entire text (for multi-word skills)
            if not found_variations and len(variation.split()) > 1:
                # Clean the variation
                cleaned_variation = re.sub(r'[^\w\s]', '', variation)
                # Check similarity with cleaned text
                similarity = calculate_similarity(cleaned_variation, cleaned_text)
                if similarity >= fuzzy_threshold:
                    found_variations.add(variation)
                    match_type = 'fuzzy'
                    break
    
    found = len(found_variations) > 0
    return found, found_variations, variations, match_type


def extract_required_skills(jd_data: Dict[str, Any]) -> List[str]:
    """
    Extract required skills from JD data.
    
    This function handles various cases:
    - skills field missing → returns empty list
    - skills field is null/None → returns empty list  
    - skills field is empty array → returns empty list
    - skills field has values → returns filtered list of non-empty skills
    
    Args:
        jd_data: Job description dictionary
        
    Returns:
        List of required skills (empty list if none specified)
    """
    try:
        requirements = jd_data.get('requirements_must_have', {})
        
        # Handle case where requirements_must_have doesn't exist
        if not requirements:
            logger.debug("No 'requirements_must_have' field found in JD")
            return []
        
        skills = requirements.get('skills')
        
        # Case: skills field is missing
        if 'skills' not in requirements:
            logger.debug("'skills' field missing from requirements")
            return []
        
        # Case: skills field is null/None
        if skills is None:
            logger.debug("'skills' field is null/None")
            return []
        
        # Case: skills is not a list
        if not isinstance(skills, list):
            logger.warning(f"'skills' field is not a list, got: {type(skills)}")
            return []
        
        # Case: empty list
        if not skills:
            logger.debug("'skills' field is an empty list")
            return []
        
        # Filter out empty strings, None, and whitespace-only strings
        filtered_skills = []
        for skill in skills:
            if skill is None:
                continue
            if isinstance(skill, str) and skill.strip():
                filtered_skills.append(skill.strip())
        
        logger.debug(f"Extracted {len(filtered_skills)} skills from JD")
        return filtered_skills
        
    except (AttributeError, KeyError, TypeError) as e:
        logger.error(f"Error extracting required skills: {e}")
        return []


def get_raw_resume_text(resume_data: Dict[str, Any]) -> str:
    """
    Extract raw resume text from resume data.
    
    Args:
        resume_data: Resume dictionary
        
    Returns:
        Raw resume text
    """
    try:
        raw_text = resume_data.get('raw_resume_text', '')
        if raw_text is None:
            return ''
        return str(raw_text).strip()
    except (AttributeError, KeyError, TypeError) as e:
        logger.error(f"Error extracting resume text: {e}")
        return ''


def verify_skills(
    resume: Dict[str, Any],
    jd: Dict[str, Any],
    return_details: bool = False,
    use_fuzzy_matching: bool = True,
    fuzzy_threshold: float = 0.85
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Verify if candidate possesses all required skills.
    
    Args:
        resume: Resume dictionary with 'raw_resume_text' field
        jd: Job description dictionary with 'requirements_must_have.skills' field
        return_details: If True, return detailed information
        use_fuzzy_matching: If True, use fuzzy matching for typos
        fuzzy_threshold: Similarity threshold for fuzzy matching (0-1)
        
    Returns:
        If return_details is False: Tuple of (all_skills_found, None)
        If return_details is True: Tuple of (all_skills_found, details_dict)
        
        details_dict contains:
            - message: Success/error message
            - required_skills: List of all required skills
            - found_skills: List of skills found in resume
            - missing_skills: List of skills not found in resume
            - skill_variations: Dict of skill -> variations checked
            - found_variations: Dict of skill -> variations found
            - match_types: Dict of skill -> match type used
            - synonym_matches: Dict of skill -> synonyms used for matching
            - skill_categories: Dict of skill -> category information
            - failed_checks: List of failed validation checks
            - failure_reason: Detailed failure reason if not qualified
    """
    details = {
        'message': '',
        'required_skills': [],
        'found_skills': [],
        'missing_skills': [],
        'skill_variations': {},
        'found_variations': {},
        'match_types': {},
        'synonym_matches': {},
        'skill_categories': {},
        'failed_checks': [],
        'failure_reason': ''
    }
    
    try:
        # Extract required skills from JD
        required_skills = extract_required_skills(jd)
        details['required_skills'] = required_skills
        
        # If no skills required, automatically pass
        if not required_skills:
            details['message'] = "No skills requirement specified in JD (skills field missing, null, or empty)"
            if return_details:
                return True, details
            return True, None
        
        # Get resume raw text
        resume_text = get_raw_resume_text(resume)
        
        if not resume_text:
            error_msg = "No raw resume text found in resume data"
            details['message'] = error_msg
            details['failed_checks'].append('no_resume_text')
            details['failure_reason'] = error_msg
            if return_details:
                return False, details
            return False, None
        
        # Check each required skill
        found_skills = []
        missing_skills = []
        skill_variations = {}
        found_variations = {}
        match_types = {}
        synonym_matches = {}
        skill_categories = {}
        
        for skill in required_skills:
            found, found_vars, checked_vars, match_type = check_skill_in_text(
                skill, 
                resume_text,
                use_fuzzy_matching=use_fuzzy_matching,
                fuzzy_threshold=fuzzy_threshold
            )
            
            skill_variations[skill] = list(checked_vars) if checked_vars else []
            found_variations[skill] = list(found_vars) if found_vars else []
            match_types[skill] = match_type
            
            # Get skill category information
            categories = []
            if is_technical_skill(skill):
                categories.append('technical')
            if is_hr_skill(skill):
                categories.append('hr')
            if is_business_skill(skill):
                categories.append('business')
            if is_management_skill(skill):
                categories.append('management')
            skill_categories[skill] = categories if categories else ['general']
            
            # Check which synonyms were used
            synonyms = get_synonyms(skill)
            used_synonyms = [syn for syn in synonyms if syn in found_vars]
            synonym_matches[skill] = used_synonyms if used_synonyms else []
            
            if found:
                found_skills.append(skill)
                logger.debug(f"Found skill '{skill}' in resume (match: {match_type}, variation: {found_vars})")
            else:
                missing_skills.append(skill)
                logger.debug(f"Missing skill '{skill}' in resume (checked: {checked_vars})")
        
        details['found_skills'] = found_skills
        details['missing_skills'] = missing_skills
        details['skill_variations'] = skill_variations
        details['found_variations'] = found_variations
        details['match_types'] = match_types
        details['synonym_matches'] = synonym_matches
        details['skill_categories'] = skill_categories
        
        # Check if all skills are found
        if not missing_skills:
            details['message'] = f"All required skills found ({len(found_skills)} skills)"
            if return_details:
                return True, details
            return True, None
        else:
            missing_count = len(missing_skills)
            found_count = len(found_skills)
            error_msg = (f"Missing skills: {', '.join(missing_skills)} "
                        f"({found_count} found, {missing_count} missing)")
            details['message'] = error_msg
            details['failed_checks'].append('missing_skills')
            details['failure_reason'] = f"Required skills not found: {', '.join(missing_skills)}"
            if return_details:
                return False, details
            return False, None
            
    except Exception as e:
        error_msg = f"Error verifying skills: {str(e)}"
        logger.error(error_msg)
        details['message'] = error_msg
        details['failed_checks'].append('verification_error')
        details['failure_reason'] = error_msg
        if return_details:
            return False, details
        return False, None


def verify_skills_from_files(
    jd_file_path: str,
    resume_file_path: str,
    return_details: bool = False,
    use_fuzzy_matching: bool = True,
    fuzzy_threshold: float = 0.85
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Verify skills by loading JSON files.
    
    Args:
        jd_file_path: Path to JD JSON file
        resume_file_path: Path to Resume JSON file
        return_details: If True, return detailed information
        use_fuzzy_matching: If True, use fuzzy matching for typos
        fuzzy_threshold: Similarity threshold for fuzzy matching (0-1)
        
    Returns:
        Tuple of (all_skills_found, details_dict or None)
    """
    try:
        with open(jd_file_path, 'r', encoding='utf-8') as f:
            jd_data = json.load(f)
        
        with open(resume_file_path, 'r', encoding='utf-8') as f:
            resume_data = json.load(f)
        
        return verify_skills(resume_data, jd_data, return_details, use_fuzzy_matching, fuzzy_threshold)
        
    except FileNotFoundError as e:
        details = {
            'message': f"File not found: {e}",
            'failed_checks': ['file_not_found'],
            'failure_reason': str(e)
        }
        if return_details:
            return False, details
        return False, None
    except json.JSONDecodeError as e:
        details = {
            'message': f"Invalid JSON format: {e}",
            'failed_checks': ['invalid_json'],
            'failure_reason': str(e)
        }
        if return_details:
            return False, details
        return False, None
    except Exception as e:
        details = {
            'message': f"Error reading files: {e}",
            'failed_checks': ['file_error'],
            'failure_reason': str(e)
        }
        if return_details:
            return False, details
        return False, None


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent.parent
    jd_folder = repo_root / "JD-jsons"
    resume_folder = repo_root / "Resumes-jsons"

    jd_files = list(jd_folder.glob("*.json"))
    resume_files = list(resume_folder.glob("*.json"))

    if not jd_files:
        raise SystemExit(f"No JD JSON files found in {jd_folder}")

    jd = load_json(jd_files[0])
    print(f"Using JD: {jd_files[0].name}")

    for resume_file in resume_files:
        resume = load_json(resume_file)
        passed, details = verify_skills(resume, jd, return_details=True)
        if passed:
            print(f"{resume_file.name}: True - {details.get('message')}")
        else:
            print(
                f"{resume_file.name}: False - {details.get('message')} | "
                f"failed_checks={details.get('failed_checks')} | "
                f"reason={details.get('failure_reason')}"
            )