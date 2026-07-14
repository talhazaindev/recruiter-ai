"""
find_relevant_project_exp.py

This module calculates the total relevant project and certification experience
from a resume based on a job description's tech stack. It's designed for
associate/junior positions where candidates may not have extensive work experience.
"""

import re
import json
from typing import List, Dict, Any, Optional, Tuple
from difflib import SequenceMatcher


import sys
from pathlib import Path

# Find tech_aliases_db.py by going up the directory tree
current = Path(__file__).parent.absolute()
for _ in range(5):
    if (current / "tech_aliases_db.py").exists():
        sys.path.insert(0, str(current))
        break
    current = current.parent


from tech_aliases_db import (
        MIN_TECH_STACK_MATCH_PERCENTAGE,
        FUZZY_MATCH_THRESHOLD,
        TECH_STACK_ALIASES,
        COMPOUND_TECH_ALIASES,
    )



def fuzzy_match(str1: str, str2: str, threshold: float = FUZZY_MATCH_THRESHOLD) -> bool:
    """
    Perform fuzzy matching between two strings using SequenceMatcher.
    """
    if not str1 or not str2:
        return False
    
    str1 = str1.lower().strip()
    str2 = str2.lower().strip()
    
    if str1 == str2:
        return True
    
    if str1 in str2 or str2 in str1:
        return True
    
    similarity = SequenceMatcher(None, str1, str2).ratio()
    return similarity >= threshold

def get_compound_tech_components(tech: str) -> List[str]:
    """
    Get all component technologies for a compound tech stack alias.
    """
    if not tech:
        return []
    
    tech_lower = tech.lower().strip()
    
    for alias, components in COMPOUND_TECH_ALIASES.items():
        if tech_lower == alias or tech_lower in components:
            return components
    
    return [tech]

def get_tech_aliases(tech: str) -> List[str]:
    """
    Get all aliases for a given technology.
    """
    if not tech:
        return []
    
    tech_lower = tech.lower().strip()
    
    compound_components = get_compound_tech_components(tech_lower)
    if len(compound_components) > 1 or compound_components != [tech_lower]:
        return compound_components
    
    for key, aliases in TECH_STACK_ALIASES.items():
        if tech_lower == key or tech_lower in aliases:
            return [key] + aliases
    
    return [tech_lower]

def is_tech_match(description: str, tech: str) -> bool:
    """
    Check if a technology appears in the description using aliases, compound matches, and fuzzy matching.
    """
    if not description or not tech:
        return False
    
    description_lower = description.lower()
    aliases = get_tech_aliases(tech)
    
    for alias in aliases:
        if alias in description_lower:
            return True
        
        pattern = r'\b' + re.escape(alias) + r'\b'
        if re.search(pattern, description_lower):
            return True
    
    if len(aliases) > 3:
        matching_components = 0
        for alias in aliases:
            if len(alias) > 2 and alias in description_lower:
                matching_components += 1
        
        if matching_components / len(aliases) >= 0.6:
            return True
    
    description_words = description_lower.split()
    tech_words = tech.lower().split()
    
    if len(tech_words) > 1:
        matching_words = sum(1 for word in tech_words if word in description_lower)
        if matching_words / len(tech_words) >= 0.6:
            return True
    
    if len(description) > 50:
        for word in description_words:
            if len(word) > 3 and fuzzy_match(tech.lower(), word, 0.8):
                return True
    
    return False

def extract_tech_stack_from_description(description: str, tech_stack: List[str]) -> int:
    """
    Extract and count how many tech stack items appear in the description.
    """
    if not description or not tech_stack:
        return 0
    
    matches = 0
    for tech in tech_stack:
        if is_tech_match(description, tech):
            matches += 1
    
    return matches

def calculate_match_percentage(tech_matches: int, total_tech: int) -> float:
    """
    Calculate the percentage of tech stack matches.
    """
    if total_tech == 0:
        return 0.0
    return (tech_matches / total_tech) * 100

def is_valid_project(project: Any) -> Tuple[bool, str]:
    """
    Check if a project is valid (must be a non-empty string).
    Returns: (is_valid, project_text)
    """
    if project is None:
        return False, ""
    
    if not isinstance(project, str):
        return False, ""
    
    project_text = project.strip()
    return bool(project_text), project_text

def is_valid_certification(certification: Any) -> Tuple[bool, str]:
    """
    Check if a certification is valid (must be a non-empty string).
    Returns: (is_valid, cert_text)
    """
    if certification is None:
        return False, ""
    
    if not isinstance(certification, str):
        return False, ""
    
    cert_text = certification.strip()
    return bool(cert_text), cert_text

def is_relevant_certification(certification: str, tech_stack: List[str]) -> Tuple[bool, int]:
    """
    Determine if a certification is relevant based on tech stack matching.
    For certifications: if ANY keyword matches, it's considered relevant.
    """
    is_valid, cert_text = is_valid_certification(certification)
    if not is_valid:
        return False, 0
    
    if not tech_stack:
        return False, 0
    
    tech_matches = 0
    matched_techs = []
    
    # Check each tech in the stack
    for tech in tech_stack:
        if is_tech_match(cert_text, tech):
            tech_matches += 1
            matched_techs.append(tech)
    
    # For certifications: if at least ONE tech matches, it's relevant
    is_relevant = tech_matches >= 1
    
    # Also print which techs matched for debugging
    if is_relevant:
        print(f"   - Matched techs: {', '.join(matched_techs)}")
    
    return is_relevant, tech_matches

def is_relevant_project(project: str, tech_stack: List[str]) -> Tuple[bool, int]:
    """
    Determine if a project is relevant based on tech stack matching.
    For projects: uses the threshold percentage from tech_aliases_db.
    """
    is_valid, project_text = is_valid_project(project)
    if not is_valid:
        return False, 0
    
    if not tech_stack:
        return False, 0
    
    tech_matches = extract_tech_stack_from_description(project_text, tech_stack)
    match_percentage = calculate_match_percentage(tech_matches, len(tech_stack))
    is_relevant = match_percentage >= MIN_TECH_STACK_MATCH_PERCENTAGE
    
    return is_relevant, tech_matches

def find_relevant_project_experience(
    job_json: Dict[str, Any], 
    resume_json: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Main function to calculate total relevant project and certification experience.
    """
    tech_stack = job_json.get('tech_stack', [])
    
    if not tech_stack:
        print("Warning: No tech stack provided in JD")
        return {
            'relevant_count': 0,
            'relevant_projects': [],
            'relevant_certifications': [],
            'project_matches': {},
            'certification_matches': {},
            'total_projects_checked': 0,
            'total_certifications_checked': 0,
            'invalid_projects': [],
            'invalid_certifications': []
        }
    
    projects = resume_json.get('projects', [])
    certifications = resume_json.get('certifications', [])
    
    if not isinstance(projects, list):
        projects = []
    if not isinstance(certifications, list):
        certifications = []
    
    print(f"\n🔍 Checking projects and certifications for tech stack:")
    print(f"Tech stack criteria: {tech_stack}")
    print(f"Project match threshold: {MIN_TECH_STACK_MATCH_PERCENTAGE}%")
    print(f"Certification match threshold: 1 keyword match")
    print("-" * 60)
    
    relevant_projects = []
    project_matches = {}
    invalid_projects = []
    total_relevant = 0
    total_projects_checked = 0
    
    print("\n📁 Checking Projects:")
    
    if not projects:
        print("   No projects found in resume")
    else:
        for idx, project in enumerate(projects, 1):
            is_valid, project_text = is_valid_project(project)
            
            if not is_valid:
                invalid_projects.append(f"Project #{idx}: {project}")
                print(f"⚠️  Project #{idx}: Invalid or empty project entry - skipped")
                continue
            
            total_projects_checked += 1
            
            # Get project name for display (first 50 characters)
            project_name = project_text[:50] + "..." if len(project_text) > 50 else project_text
            
            is_relevant, tech_matches = is_relevant_project(project, tech_stack)
            
            match_percentage = calculate_match_percentage(tech_matches, len(tech_stack))
            project_matches[project_name] = {
                'tech_matches': tech_matches,
                'match_percentage': match_percentage,
                'is_relevant': is_relevant
            }
            
            if is_relevant:
                relevant_projects.append(project_text)
                total_relevant += 1
                print(f"✅ Relevant Project: {project_name}")
                print(f"   - Tech matches: {tech_matches}/{len(tech_stack)} ({match_percentage:.1f}%)")
            else:
                print(f"❌ Project: {project_name}")
                print(f"   - Tech matches: {tech_matches}/{len(tech_stack)} ({match_percentage:.1f}%)")
    
    print("\n📜 Checking Certifications:")
    print("   (Any match = relevant)")
    relevant_certifications = []
    certification_matches = {}
    invalid_certifications = []
    total_certifications_checked = 0
    
    if not certifications:
        print("   No certifications found in resume")
    else:
        for idx, cert in enumerate(certifications, 1):
            is_valid, cert_text = is_valid_certification(cert)
            
            if not is_valid:
                invalid_certifications.append(f"Certification #{idx}: {cert}")
                print(f"⚠️  Certification #{idx}: Invalid or empty certification - skipped")
                continue
            
            total_certifications_checked += 1
            is_relevant, tech_matches = is_relevant_certification(cert, tech_stack)
            
            match_percentage = calculate_match_percentage(tech_matches, len(tech_stack))
            certification_matches[cert_text] = {
                'tech_matches': tech_matches,
                'match_percentage': match_percentage,
                'is_relevant': is_relevant
            }
            
            if is_relevant:
                relevant_certifications.append(cert_text)
                total_relevant += 1
                print(f"✅ Relevant Certification: {cert_text}")
                print(f"   - Tech matches: {tech_matches}/{len(tech_stack)} ({match_percentage:.1f}%)")
            else:
                print(f"❌ Certification: {cert_text}")
                print(f"   - Tech matches: {tech_matches}/{len(tech_stack)} ({match_percentage:.1f}%)")
    
    print("-" * 60)
    print(f"📊 Total relevant projects + certifications: {total_relevant}")
    print(f"📊 Relevant projects: {len(relevant_projects)}")
    print(f"📊 Relevant certifications: {len(relevant_certifications)}")
    print(f"📊 Total projects checked: {total_projects_checked}")
    print(f"📊 Total certifications checked: {total_certifications_checked}")
    
    if invalid_projects:
        print(f"⚠️  Invalid projects skipped: {len(invalid_projects)}")
    if invalid_certifications:
        print(f"⚠️  Invalid certifications skipped: {len(invalid_certifications)}")
    
    return {
        'relevant_count': total_relevant,
        'relevant_projects': relevant_projects,
        'relevant_certifications': relevant_certifications,
        'project_matches': project_matches,
        'certification_matches': certification_matches,
        'total_projects_checked': total_projects_checked,
        'total_certifications_checked': total_certifications_checked,
        'invalid_projects': invalid_projects,
        'invalid_certifications': invalid_certifications
    }


if __name__ == "__main__":
    # Test Case with projects as strings
    test_case = {
        "job": {
            "job_title": "Associate AI/ML Engineer",
            "tech_stack": ["Python", "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "Docker", "AWS"]
        },
        "resume": {
            "projects": [
                "Built a deep learning model using TensorFlow and PyTorch for image classification",
                None,
                "",
                "Built a full-stack MERN application with React, Node.js, and MongoDB",
                "Analyzed datasets using Pandas and NumPy for data science projects",
                12345,
                "Developed an ETL pipeline using Python and AWS services"
            ],
            "certifications": [
                "AWS Certified Machine Learning Specialty",
                "",
                None,
                "  ",
                "TensorFlow Developer Certificate",
                123,
                "Python Programming Certificate"
            ]
        }
    }
    
    print("🧪 Running Test Case\n" + "="*80)
    result = find_relevant_project_experience(test_case["job"], test_case["resume"])
    
    print(f"\n🎯 Final Results:")
    print(f"   - Total relevant count: {result['relevant_count']}")
    print(f"   - Relevant projects: {result['relevant_projects']}")
    print(f"   - Relevant certifications: {result['relevant_certifications']}")
    print(f"   - Total projects checked: {result['total_projects_checked']}")
    print(f"   - Total certifications checked: {result['total_certifications_checked']}")
    
    if result['invalid_projects']:
        print(f"   - Invalid projects skipped: {result['invalid_projects']}")
    if result['invalid_certifications']:
        print(f"   - Invalid certifications skipped: {result['invalid_certifications']}")