"""
verify.py - Master verification module that orchestrates education, skills, and experience validation
"""

import json
import logging
from typing import Dict, Any, Tuple, Optional, List
from pathlib import Path


from .verify_education import verify_education_criteria
from .verify_skills import verify_skills
from .verify_totalexp import verify_total_experience

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VerificationResult:
    """
    Container class for verification results.
    """
    def __init__(self):
        self.overall_pass = False
        self.education = {
            'passed': False,
            'message': '',
            'details': {}
        }
        self.skills = {
            'passed': False,
            'message': '',
            'details': {}
        }
        self.experience = {
            'passed': False,
            'message': '',
            'details': {}
        }
        self.failed_checks = []
        self.failure_reason = ''
        self.summary = []
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert result to dictionary.
        """
        return {
            'overall_pass': self.overall_pass,
            'education': self.education,
            'skills': self.skills,
            'experience': self.experience,
            'failed_checks': self.failed_checks,
            'failure_reason': self.failure_reason,
            'summary': self.summary
        }
    
    def to_json(self) -> str:
        """
        Convert result to JSON string.
        """
        return json.dumps(self.to_dict(), indent=2)


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


def verify_candidate(
    resume: Dict[str, Any],
    jd: Dict[str, Any],
    return_details: bool = False,
    skip_checks: Optional[List[str]] = None,
    use_fuzzy_matching: bool = True,
    fuzzy_threshold: float = 0.85
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Master verification function that checks education, skills, and experience.
    
    Args:
        resume: Resume dictionary with all required fields
        jd: Job description dictionary with all requirements
        return_details: If True, return detailed information
        skip_checks: List of checks to skip ('education', 'skills', 'experience')
        use_fuzzy_matching: If True, use fuzzy matching for skills
        fuzzy_threshold: Similarity threshold for fuzzy matching (0-1)
        
    Returns:
        If return_details is False: Tuple of (all_checks_passed, None)
        If return_details is True: Tuple of (all_checks_passed, details_dict)
        
        details_dict contains:
            - overall_pass: Boolean indicating if all checks passed
            - education: Dict with education verification results
            - skills: Dict with skills verification results
            - experience: Dict with experience verification results
            - failed_checks: List of failed check names
            - failure_reason: Detailed failure reason
            - summary: List of summary messages
    """
    result = VerificationResult()
    
    # Initialize skip_checks if None
    if skip_checks is None:
        skip_checks = []
    
    # Track failed checks
    failed_checks = []
    
    try:
        # =========================
        # 1. Verify Education
        # =========================
        if 'education' not in skip_checks:
            logger.info("Verifying education...")
            edu_passed, edu_details = verify_education_criteria(
                resume, 
                jd, 
                return_details=True
            )
            
            result.education['passed'] = edu_passed
            result.education['message'] = edu_details.get('message', '')
            result.education['details'] = edu_details
            
            if edu_passed:
                result.summary.append(f"✅ Education: {edu_details.get('message', 'Passed')}")
            else:
                failed_checks.append('education')
                result.summary.append(f"❌ Education: {edu_details.get('message', 'Failed')}")
                result.failure_reason = edu_details.get('failure_reason', 'Education requirement not met')
        else:
            result.education['passed'] = True
            result.education['message'] = 'Skipped (education check disabled)'
            result.summary.append("⏭️ Education: Skipped")
        
        # =========================
        # 2. Verify Skills
        # =========================
        if 'skills' not in skip_checks:
            logger.info("Verifying skills...")
            skills_passed, skills_details = verify_skills(
                resume, 
                jd, 
                return_details=True,
                use_fuzzy_matching=use_fuzzy_matching,
                fuzzy_threshold=fuzzy_threshold
            )
            
            result.skills['passed'] = skills_passed
            result.skills['message'] = skills_details.get('message', '')
            result.skills['details'] = skills_details
            
            if skills_passed:
                result.summary.append(f"✅ Skills: {skills_details.get('message', 'Passed')}")
            else:
                failed_checks.append('skills')
                result.summary.append(f"❌ Skills: {skills_details.get('message', 'Failed')}")
                # Only set failure reason if education didn't fail (first failure takes precedence)
                if not result.failure_reason:
                    result.failure_reason = skills_details.get('failure_reason', 'Skills requirement not met')
        else:
            result.skills['passed'] = True
            result.skills['message'] = 'Skipped (skills check disabled)'
            result.summary.append("⏭️ Skills: Skipped")
        
        # =========================
        # 3. Verify Experience
        # =========================
        if 'experience' not in skip_checks:
            logger.info("Verifying experience...")
            exp_passed, exp_details = verify_total_experience(
                resume, 
                jd, 
                return_details=True
            )
            
            result.experience['passed'] = exp_passed
            result.experience['message'] = exp_details.get('message', '')
            result.experience['details'] = exp_details
            
            if exp_passed:
                result.summary.append(f"✅ Experience: {exp_details.get('message', 'Passed')}")
            else:
                failed_checks.append('experience')
                result.summary.append(f"❌ Experience: {exp_details.get('message', 'Failed')}")
                # Only set failure reason if no previous failure
                if not result.failure_reason:
                    result.failure_reason = exp_details.get('failure_reason', 'Experience requirement not met')
        else:
            result.experience['passed'] = True
            result.experience['message'] = 'Skipped (experience check disabled)'
            result.summary.append("⏭️ Experience: Skipped")
        
        # =========================
        # Determine Overall Result
        # =========================
        result.failed_checks = failed_checks
        result.overall_pass = len(failed_checks) == 0
        
        if result.overall_pass:
            result.summary.append("✅ OVERALL: All checks passed!")
        else:
            result.summary.append(f"❌ OVERALL: Failed checks: {', '.join(failed_checks)}")
            if not result.failure_reason:
                result.failure_reason = f"Failed checks: {', '.join(failed_checks)}"
        
        # Log summary
        for line in result.summary:
            logger.info(line)
        
        if return_details:
            return result.overall_pass, result.to_dict()
        return result.overall_pass, None
        
    except Exception as e:
        error_msg = f"Error during verification: {str(e)}"
        logger.error(error_msg)
        
        result.overall_pass = False
        result.failure_reason = error_msg
        result.failed_checks.append('verification_error')
        result.summary.append(f"❌ Error: {error_msg}")
        
        if return_details:
            return False, result.to_dict()
        return False, None


def verify_candidate_from_files(
    jd_file_path: str,
    resume_file_path: str,
    return_details: bool = False,
    skip_checks: Optional[List[str]] = None,
    use_fuzzy_matching: bool = True,
    fuzzy_threshold: float = 0.85
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Verify candidate by loading JSON files.
    
    Args:
        jd_file_path: Path to JD JSON file
        resume_file_path: Path to Resume JSON file
        return_details: If True, return detailed information
        skip_checks: List of checks to skip ('education', 'skills', 'experience')
        use_fuzzy_matching: If True, use fuzzy matching for skills
        fuzzy_threshold: Similarity threshold for fuzzy matching (0-1)
        
    Returns:
        Tuple of (all_checks_passed, details_dict or None)
    """
    try:
        # Load JSON files
        with open(jd_file_path, 'r', encoding='utf-8') as f:
            jd_data = json.load(f)
        
        with open(resume_file_path, 'r', encoding='utf-8') as f:
            resume_data = json.load(f)
        
        # Verify candidate
        return verify_candidate(
            resume_data,
            jd_data,
            return_details=return_details,
            skip_checks=skip_checks,
            use_fuzzy_matching=use_fuzzy_matching,
            fuzzy_threshold=fuzzy_threshold
        )
        
    except FileNotFoundError as e:
        error_msg = f"File not found: {e}"
        logger.error(error_msg)
        if return_details:
            details = {
                'overall_pass': False,
                'failure_reason': error_msg,
                'failed_checks': ['file_not_found'],
                'summary': [f"❌ {error_msg}"]
            }
            return False, details
        return False, None
        
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON format: {e}"
        logger.error(error_msg)
        if return_details:
            details = {
                'overall_pass': False,
                'failure_reason': error_msg,
                'failed_checks': ['invalid_json'],
                'summary': [f"❌ {error_msg}"]
            }
            return False, details
        return False, None
        
    except Exception as e:
        error_msg = f"Error reading files: {e}"
        logger.error(error_msg)
        if return_details:
            details = {
                'overall_pass': False,
                'failure_reason': error_msg,
                'failed_checks': ['file_error'],
                'summary': [f"❌ {error_msg}"]
            }
            return False, details
        return False, None


def quick_verify(
    resume: Dict[str, Any],
    jd: Dict[str, Any]
) -> bool:
    """
    Quick verification without details.
    
    Args:
        resume: Resume dictionary
        jd: Job description dictionary
        
    Returns:
        Boolean indicating if all checks passed
    """
    passed, _ = verify_candidate(resume, jd, return_details=False)
    return passed


if __name__ == "__main__":
    # Example usage
    repo_root = Path(__file__).resolve().parent.parent.parent
    jd_folder = repo_root / "JD-jsons"
    resume_folder = repo_root / "Resumes-jsons"
    
    jd_files = list(jd_folder.glob("*.json"))
    resume_files = list(resume_folder.glob("*.json"))
    
    if not jd_files:
        raise SystemExit(f"No JD JSON files found in {jd_folder}")
    
    if not resume_files:
        raise SystemExit(f"No Resume JSON files found in {resume_folder}")
    
    jd = load_json(jd_files[0])
    print(f"Using JD: {jd_files[0].name}")
    print("=" * 60)
    
    for resume_file in resume_files:
        resume = load_json(resume_file)
        print(f"\nProcessing: {resume_file.name}")
        print("-" * 40)
        
        # Full verification with details
        passed, details = verify_candidate(resume, jd, return_details=True)
        
        if passed:
            print(f"✅ PASSED: {resume_file.name}")
            for summary in details['summary']:
                if '✅' in summary:
                    print(f"  {summary}")
        else:
            print(f"❌ FAILED: {resume_file.name}")
            for summary in details['summary']:
                if '❌' in summary:
                    print(f"  {summary}")
            print(f"  Failure reason: {details['failure_reason']}")
            print(f"  Failed checks: {details['failed_checks']}")
        
        print("-" * 40)