from pathlib import Path
import sys
from typing import Dict, Any, List, Tuple

# Add the parent directory to path to import from subfolders
sys.path.append(str(Path(__file__).resolve().parent))

# Import functions from the required folders

from must_req.verify import verify_candidate
from relevant_exp.find_work_exp import find_relevant_experience
from relevant_exp.find_project_exp import find_relevant_project_experience

def load_json(file_path: Path) -> Dict[str, Any]:
    """Load JSON file and return as dictionary"""
    import json
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def process_resumes() -> None:
    """Main function to process resumes against JD"""
    
    # Define paths
    repo_root = Path(__file__).resolve().parent.parent
    jd_folder = repo_root / "JD-jsons"
    resume_folder = repo_root / "Resumes-jsons"
    
    # Get all JSON files
    jd_files = list(jd_folder.glob("*.json"))
    resume_files = list(resume_folder.glob("*.json"))
    
    # Check if files exist
    if not jd_files:
        raise SystemExit(f"No JD JSON files found in {jd_folder}")
    
    if not resume_files:
        raise SystemExit(f"No Resume JSON files found in {resume_folder}")
    
    # Load JD
    jd = load_json(jd_files[0])
    print(f"Using JD: {jd_files[0].name}")
    print("=" * 60)
    
    # List to store results for ranking
    ranked_results = []
    
    # Process each resume
    for resume_file in resume_files:
        resume = load_json(resume_file)
        print(f"\nProcessing: {resume_file.name}")
        print("-" * 40)
        
        # Step 1: Full verification with details (must-have requirements)
        passed, details = verify_candidate(resume, jd, return_details=True)
        
        if passed:
            print(f"✅ PASSED: {resume_file.name}")
            for summary in details['summary']:
                if '✅' in summary:
                    print(f"  {summary}")
            
            # Step 2: After passing must-have requirements, find relevant work experience
            years, gap_found, gaps = find_relevant_experience(jd, resume)
            # Convert years to dictionary format
            result = {'total_relevant_years': float(years)}
            
            # Step 3: Find relevant project experience
            project_result = find_relevant_project_experience(jd, resume)
            
            # Store results for ranking
            ranked_results.append({
                'resume_file': resume_file,
                'resume_name': resume_file.name,
                'work_experience_years': result.get('total_relevant_years', 0),
                'project_experience_years': project_result.get('total_project_years', 0) if isinstance(project_result, dict) else float(project_result) if project_result is not None else 0,
                'gap_found': gap_found,
                'gaps': gaps,
                'work_details': result,
                'project_details': project_result if isinstance(project_result, dict) else {'total_project_years': float(project_result) if project_result is not None else 0}
            })
            
            print(f"  Relevant Work Experience: {result.get('total_relevant_years', 0):.2f} years")
            if isinstance(project_result, dict):
                print(f"  Relevant Project Experience: {project_result.get('total_project_years', 0):.2f} years")
            else:
                print(f"  Relevant Project Experience: {float(project_result) if project_result is not None else 0:.2f} years")
            
            if gap_found:
                print(f"  ⚠️ Experience gaps found: {gaps}")
            
        else:
            print(f"❌ FAILED: {resume_file.name}")
            for summary in details['summary']:
                if '❌' in summary:
                    print(f"  {summary}")
            print(f"  Failure reason: {details['failure_reason']}")
            print(f"  Failed checks: {details['failed_checks']}")
            
            # Still add failed candidates but with 0 experience
            ranked_results.append({
                'resume_file': resume_file,
                'resume_name': resume_file.name,
                'work_experience_years': 0,
                'project_experience_years': 0,
                'gap_found': True,
                'gaps': ['Failed must-have requirements'],
                'work_details': {},
                'project_details': {},
                'failed': True
            })
        
        print("-" * 40)
    
    # Step 4: Rank resumes based on total relevant experience
    print("\n" + "=" * 60)
    print("📊 RANKING RESUMES BY RELEVANT EXPERIENCE")
    print("=" * 60)
    
    # Check if JD has minimum_relevant_years requirement
    min_relevant_years = jd.get('minimum_relevant_years', 0)
    is_fresh_graduate = False
    
    if isinstance(min_relevant_years, str) and "0-6 months" in min_relevant_years.lower():
        is_fresh_graduate = True
        print("ℹ️  JD indicates 0-6 months experience - considering project experience as secondary criteria")
    
    # Sort results
    if is_fresh_graduate:
        # Sort by work experience first, then project experience
        sorted_results = sorted(
            [r for r in ranked_results if not r.get('failed', False)],
            key=lambda x: (x['work_experience_years'], x['project_experience_years']),
            reverse=True
        )
    else:
        # Sort by work experience only (descending)
        sorted_results = sorted(
            [r for r in ranked_results if not r.get('failed', False)],
            key=lambda x: x['work_experience_years'],
            reverse=True
        )
    
    # Display ranking
    print(f"\n🏆 Top Candidates:")
    print("-" * 60)
    
    for rank, result in enumerate(sorted_results, 1):
        print(f"{rank}. {result['resume_name']}")
        print(f"   Relevant Work Experience: {result['work_experience_years']:.2f} years")
        
        if is_fresh_graduate:
            print(f"   Relevant Project Experience: {result['project_experience_years']:.2f} years")
        
        if result.get('gap_found', False) and not result.get('failed', False):
            print(f"   ⚠️ Experience gaps: {result.get('gaps', [])}")
        print()
    
    # Show failed candidates
    failed_candidates = [r for r in ranked_results if r.get('failed', False)]
    if failed_candidates:
        print("\n❌ Failed Candidates (Did not meet must-have requirements):")
        print("-" * 60)
        for result in failed_candidates:
            print(f"  • {result['resume_name']}")
    
    print("\n" + "=" * 60)
    print("✅ Processing complete!")

if __name__ == "__main__":
    process_resumes()