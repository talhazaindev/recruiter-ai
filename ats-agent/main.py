from pathlib import Path
import sys
from typing import Dict, Any, List, Tuple, Optional

# Add the parent directory to path to import from subfolders
sys.path.append(str(Path(__file__).resolve().parent))

# Import functions from the required folders
from must_req.verify import verify_candidate
from relevant_exp.find_work_exp import find_relevant_experience
from relevant_exp.find_project_exp import find_relevant_project_experience

# Configuration
OVERQUALIFIED_THRESHOLD = 1  # Years above minimum_relevant_years to be considered overqualified

def load_json(file_path: Path) -> Dict[str, Any]:
    """Load JSON file and return as dictionary"""
    import json
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def process_resumes() -> Tuple[List[Tuple[str, float, float, int, str, str]], List[Dict[str, Any]]]:
    """
    Main function to process resumes against JD and return results as tuples with details
    
    Returns:
        Tuple of:
        - List of tuples: (Resume Title, Relevant Experience, Total Experience, 
                          No of Relevant Projects + Certificates, Comment, Status)
        - List of detail dictionaries for each resume with step-by-step breakdown
    """
    
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
    
    # Get JD requirements
    min_relevant_years = jd.get('minimum_relevant_years', 0)
    if isinstance(min_relevant_years, str):
        try:
            min_relevant_years = float(min_relevant_years.split()[0])
        except:
            min_relevant_years = 0
    
    # Get minimum total years from must-have requirements
    must_have = jd.get('requirements_must_have', {})
    experience_req = must_have.get('experience', {})
    min_total_years = experience_req.get('minimum_total_years', None)
    if min_total_years is not None:
        try:
            min_total_years = float(min_total_years)
        except:
            min_total_years = None
    
    # List to store results as tuples
    results = []
    # List to store detailed breakdowns
    details_list = []
    
    # Process each resume
    for resume_file in resume_files:
        resume = load_json(resume_file)
        resume_title = resume_file.name
        print(f"\nProcessing: {resume_file.name}")
        print("-" * 40)
        
        # Initialize variables
        comment = ""
        status = "Fail"  # Default status
        relevant_experience = 0.0
        total_experience = 0.0
        projects_certificates_count = 0
        
        # Initialize detail breakdown
        detail_breakdown = {
            'resume_name': resume_title,
            'steps': [],
            'passed': False,
            'final_comment': "",
            'final_status': "Fail",
            'failed_requirements': []  # Track specific failed requirements
        }
        
        # Step 1: Must-have requirements verification
        step1 = {
            'step': 1,
            'title': 'Must-Have Requirements Verification',
            'description': 'Checking if candidate meets all mandatory requirements',
            'status': 'in_progress',
            'requirements_checked': [],
            'failed_requirements': []
        }
        detail_breakdown['steps'].append(step1)
        
        passed, details = verify_candidate(resume, jd, return_details=True)
        
        if not passed:
            # Failed must-have requirements
            comment = "Failed Requirements"
            status = "Fail"
            detail_breakdown['passed'] = False
            detail_breakdown['final_comment'] = comment
            detail_breakdown['final_status'] = "Fail"
            
            # Get total experience if available
            total_experience = details.get('total_years', 0)
            if isinstance(total_experience, (int, float)):
                total_experience = float(total_experience)
            else:
                total_experience = 0.0
            
            # Parse failed checks to get specific requirements
            failed_checks = details.get('failed_checks', [])
            failed_requirements_list = []
            
            # failed_checks is a list like ['education', 'skills'] or similar
            for check in failed_checks:
                # Map check names to readable requirement names
                requirement_name = check
                if isinstance(check, str):
                    # Capitalize and format the requirement name
                    if check == 'education':
                        requirement_name = 'Education Requirements'
                    elif check == 'skills':
                        requirement_name = 'Skills Requirements'
                    elif check == 'experience':
                        requirement_name = 'Experience Requirements'
                    elif check == 'degree':
                        requirement_name = 'Degree Requirements'
                    elif check == 'discipline':
                        requirement_name = 'Discipline Requirements'
                    elif check == 'cgpa' or check == 'minimum_cgpa':
                        requirement_name = 'CGPA Requirements'
                    else:
                        requirement_name = check.replace('_', ' ').title()
                
                failed_requirements_list.append({
                    'requirement': requirement_name,
                    'status': 'Failed',
                    'reason': f'{requirement_name} not met'
                })
            
            # If there's a detailed failure reason, add it
            failure_reason = details.get('failure_reason', '')
            if failure_reason and isinstance(failure_reason, str) and not failed_requirements_list:
                failed_requirements_list.append({
                    'requirement': 'Must-have requirements',
                    'status': 'Failed',
                    'reason': failure_reason
                })
            
            # Add step details for failure with specific failed requirements
            step1['status'] = 'failed'
            step1['summary'] = details.get('summary', [])
            step1['failure_reason'] = failure_reason
            step1['failed_checks'] = failed_checks
            step1['failed_requirements'] = failed_requirements_list
            step1['total_experience'] = total_experience
            step1['requirements_checked'] = details.get('requirements_checked', [])
            
            detail_breakdown['failed_requirements'] = failed_requirements_list
            
            # Add to results with failure comment and status
            results.append((resume_title, 0.0, total_experience, 0, comment, status))
            details_list.append(detail_breakdown)
            
            print(f"❌ FAILED: {resume_file.name}")
            if failed_requirements_list:
                print(f"  Failed Requirements:")
                for req in failed_requirements_list:
                    print(f"    ❌ {req['requirement']}")
            else:
                for summary in details['summary']:
                    if '❌' in summary:
                        print(f"  {summary}")
            if failure_reason:
                print(f"  Failure reason: {failure_reason}")
            if failed_checks:
                print(f"  Failed checks: {failed_checks}")
            print("-" * 40)
            continue
        
        # Passed must-have requirements
        comment = "Qualified"
        status = "Pass"  # Will be updated if later checks fail
        detail_breakdown['passed'] = True
        
        # Update step 1 with success
        requirements_checked = details.get('requirements_checked', [])
        passed_requirements = []
        
        # Get all requirements that were checked
        for req in requirements_checked:
            req_name = req
            if isinstance(req, str):
                if req == 'education':
                    req_name = 'Education Requirements'
                elif req == 'skills':
                    req_name = 'Skills Requirements'
                elif req == 'experience':
                    req_name = 'Experience Requirements'
                elif req == 'degree':
                    req_name = 'Degree Requirements'
                elif req == 'discipline':
                    req_name = 'Discipline Requirements'
                elif req == 'cgpa' or req == 'minimum_cgpa':
                    req_name = 'CGPA Requirements'
                else:
                    req_name = req.replace('_', ' ').title()
            
            passed_requirements.append({
                'requirement': req_name,
                'status': 'Passed'
            })
        
        step1['status'] = 'passed'
        step1['summary'] = details.get('summary', [])
        step1['total_experience'] = details.get('total_years', 0)
        step1['requirements_checked'] = requirements_checked
        step1['passed_requirements'] = passed_requirements
        step1['failed_requirements'] = []
        
        print(f"✅ PASSED: {resume_file.name}")
        print(f"  All must-have requirements passed:")
        for req in passed_requirements:
            print(f"    ✅ {req['requirement']}")
        for summary in details['summary']:
            if '✅' in summary:
                print(f"  {summary}")
        
        # Step 2: Get total experience
        total_experience = details.get('total_years', 0)
        if isinstance(total_experience, (int, float)):
            total_experience = float(total_experience)
        else:
            total_experience = 0.0
        print(f"  Total Experience: {total_experience:.2f} years")
        
        # Check if total experience meets requirement
        total_exp_passed = True
        total_exp_requirement = None
        if min_total_years is not None:
            total_exp_passed = total_experience >= min_total_years
            total_exp_requirement = {
                'requirement': f'Total experience >= {min_total_years} years',
                'actual': f'{total_experience:.1f} years',
                'status': 'Passed' if total_exp_passed else 'Failed'
            }
        
        step2 = {
            'step': 2,
            'title': 'Total Experience Check',
            'description': f'Total years of experience: {total_experience:.2f} years',
            'status': 'passed' if total_exp_passed else 'failed',
            'total_experience': total_experience,
            'minimum_required': min_total_years,
            'passed': total_exp_passed,
            'requirement': total_exp_requirement
        }
        detail_breakdown['steps'].append(step2)
        
        # Step 3: Find relevant work experience
        years, gap_found, gaps, experience_evaluations = find_relevant_experience(jd, resume)
        relevant_experience = float(years) if years else 0.0
        print(f"  Relevant Work Experience: {relevant_experience:.2f} years")
        
        # Check if relevant experience meets requirement
        relevant_exp_passed = relevant_experience >= min_relevant_years
        relevant_exp_requirement = {
            'requirement': f'Relevant experience >= {min_relevant_years} years',
            'actual': f'{relevant_experience:.1f} years',
            'status': 'Passed' if relevant_exp_passed else 'Failed'
        }
        
        step3 = {
            'step': 3,
            'title': 'Relevant Work Experience Analysis',
            'description': f'Identified {relevant_experience:.2f} years of relevant experience',
            'status': 'passed' if relevant_exp_passed else 'failed',
            'relevant_experience': relevant_experience,
            'minimum_required': min_relevant_years,
            'gap_found': gap_found,
            'gaps': gaps if gap_found else [],
            'experience_evaluations': experience_evaluations,
            'passed': relevant_exp_passed,
            'requirement': relevant_exp_requirement
        }
        detail_breakdown['steps'].append(step3)
        
        # Step 4: Find relevant project experience (count of projects + certificates)
        project_result = find_relevant_project_experience(jd, resume)
        
        # Extract the total count of projects + certificates
        if isinstance(project_result, dict):
            projects_certificates_count = project_result.get('total_project_years', 0)
            
            relevant_projects = project_result.get('relevant_projects', 0)
            relevant_certs = project_result.get('relevant_certifications', 0)
            
            if isinstance(relevant_projects, list):
                relevant_projects = len(relevant_projects)
            elif isinstance(relevant_projects, (int, float)):
                relevant_projects = int(relevant_projects)
            else:
                relevant_projects = 0
                
            if isinstance(relevant_certs, list):
                relevant_certs = len(relevant_certs)
            elif isinstance(relevant_certs, (int, float)):
                relevant_certs = int(relevant_certs)
            else:
                relevant_certs = 0
            
            if projects_certificates_count == 0 and (relevant_projects > 0 or relevant_certs > 0):
                projects_certificates_count = relevant_projects + relevant_certs
                
        elif isinstance(project_result, (int, float)):
            projects_certificates_count = int(project_result)
        else:
            projects_certificates_count = 0
        
        projects_certificates_count = int(projects_certificates_count) if projects_certificates_count else 0
        print(f"  Relevant Projects + Certificates: {projects_certificates_count}")
        
        step4 = {
            'step': 4,
            'title': 'Projects & Certifications Analysis',
            'description': f'Found {projects_certificates_count} relevant projects and certifications',
            'status': 'completed',
            'projects_certificates_count': projects_certificates_count,
            'project_result': project_result if isinstance(project_result, dict) else {'count': projects_certificates_count}
        }
        detail_breakdown['steps'].append(step4)
        
        # Step 5: Determine final comment, status, and overall assessment
        comment_priority = []
        comments_details = []
        is_qualified = True  # Track if candidate meets all requirements
        failed_requirements_final = []
        
        # Check for requirement failures
        if min_total_years is not None and total_experience < min_total_years:
            comment_priority.append("Insufficient Total Exp")
            comments_details.append(f"Total experience ({total_experience:.1f}y) < required ({min_total_years:.1f}y)")
            is_qualified = False
            failed_requirements_final.append({
                'requirement': f'Total experience >= {min_total_years} years',
                'actual': f'{total_experience:.1f} years',
                'reason': f'Candidate has {total_experience:.1f} years but requires {min_total_years} years'
            })
            print(f"  ⚠️ Total experience {total_experience:.1f}y is less than required {min_total_years:.1f}y")
        
        if relevant_experience < min_relevant_years:
            comment_priority.append("Insufficient Relevant Exp")
            comments_details.append(f"Relevant experience ({relevant_experience:.1f}y) < required ({min_relevant_years:.1f}y)")
            is_qualified = False
            failed_requirements_final.append({
                'requirement': f'Relevant experience >= {min_relevant_years} years',
                'actual': f'{relevant_experience:.1f} years',
                'reason': f'Candidate has {relevant_experience:.1f} years of relevant experience but requires {min_relevant_years} years'
            })
            print(f"  ⚠️ Relevant experience {relevant_experience:.1f}y is less than required {min_relevant_years:.1f}y")
        
        # Check for gap (doesn't cause failure, just warning)
        if gap_found:
            if not comment_priority:
                comment_priority.append("Gap Found")
                comments_details.append(f"Experience gaps detected: {', '.join(gaps) if gaps else 'Yes'}")
                print(f"  ⚠️ Experience gaps found: {gaps}")
        
        # Check for overqualified or good candidate (only if qualified)
        if is_qualified:
            if relevant_experience >= (min_relevant_years + OVERQUALIFIED_THRESHOLD):
                if not comment_priority:
                    comment_priority.append("Overqualified")
                    comments_details.append(f"Relevant experience ({relevant_experience:.1f}y) exceeds requirement by {OVERQUALIFIED_THRESHOLD}+ years")
                    print(f"  ℹ️ Candidate is overqualified (relevant exp: {relevant_experience:.1f}y > required: {min_relevant_years:.1f}y)")
            elif relevant_experience >= min_relevant_years:
                if not comment_priority:
                    comment_priority.append("Good Candidate")
                    comments_details.append(f"Relevant experience ({relevant_experience:.1f}y) meets requirement ({min_relevant_years:.1f}y)")
                    print(f"  ✅ Good Candidate (relevant exp: {relevant_experience:.1f}y meets requirement: {min_relevant_years:.1f}y)")
            else:
                if not comment_priority:
                    comment_priority.append("Qualified")
                    comments_details.append("All requirements met satisfactorily")
                    print(f"  ✅ Candidate is qualified")
        
        # Set final status based on qualification
        if is_qualified:
            status = "Pass"
        else:
            status = "Fail"
        
        comment = " | ".join(comment_priority) if comment_priority else "Qualified"
        detail_breakdown['final_comment'] = comment
        detail_breakdown['final_status'] = status
        detail_breakdown['failed_requirements'] = failed_requirements_final
        
        # Add final step with overall assessment
        step5 = {
            'step': 5,
            'title': 'Final Assessment',
            'description': 'Overall evaluation of candidate',
            'status': 'completed',
            'comment': comment,
            'comments_details': comments_details,
            'relevant_experience': relevant_experience,
            'total_experience': total_experience,
            'projects_certificates': projects_certificates_count,
            'min_relevant_required': min_relevant_years,
            'min_total_required': min_total_years,
            'overall_status': status,
            'failed_requirements': failed_requirements_final,
            'all_requirements_passed': is_qualified
        }
        detail_breakdown['steps'].append(step5)
        
        # Add result as tuple with status
        results.append((resume_title, relevant_experience, total_experience, projects_certificates_count, comment, status))
        details_list.append(detail_breakdown)
        
        print("-" * 40)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 RESULTS SUMMARY")
    print("=" * 60)
    print(f"{'Resume Title':<30} {'Relevant Exp':<15} {'Total Exp':<12} {'Projects+Certs':<15} {'Status':<8} {'Comment':<20}")
    print("-" * 100)
    for title, rel_exp, tot_exp, proj_certs, comment, status in results:
        status_display = "✅ Pass" if status == "Pass" else "❌ Fail"
        print(f"{title[:28]:<30} {rel_exp:<15.2f} {tot_exp:<12.2f} {proj_certs:<15} {status_display:<8} {comment[:18]:<20}")
    
    print("\n" + "=" * 60)
    print("✅ Processing complete!")
    
    return results, details_list

if __name__ == "__main__":
    results, details = process_resumes()
    
    print(f"Here are the details {details}")
    
    # The results are returned as tuples and can be sent to frontend
    print(f"\nReturned {len(results)} results as tuples ready for frontend")
    print(f"Returned {len(details)} detail breakdowns ready for popup display")
    
    # Sample output showing how to use both
    print("\n" + "=" * 60)
    print("📋 SAMPLE DATA FOR FRONTEND")
    print("=" * 60)
    
    for i, (title, rel_exp, tot_exp, proj_certs, comment, status) in enumerate(results, 1):
        status_emoji = "✅" if status == "Pass" else "❌"
        print(f"\n{i}. {title}")
        print(f"   Relevant Experience: {rel_exp:.2f} years")
        print(f"   Total Experience: {tot_exp:.2f} years")
        print(f"   Projects + Certificates: {proj_certs}")
        print(f"   Status: {status_emoji} {status}")
        print(f"   Comment: {comment}")
        
        # Show failed requirements if any
        if i <= len(details):
            detail = details[i-1]
            if detail['failed_requirements']:
                print(f"   ❌ Failed Requirements:")
                for req in detail['failed_requirements']:
                    print(f"      - {req['requirement']}")
                    if 'actual' in req:
                        print(f"        Actual: {req['actual']}")
                    if 'reason' in req:
                        print(f"        Reason: {req['reason']}")
            elif not detail['passed']:
                # If passed is False but no failed_requirements, check step 1
                for step in detail['steps']:
                    if step.get('step') == 1 and step.get('failed_requirements'):
                        print(f"   ❌ Failed Requirements:")
                        for req in step['failed_requirements']:
                            print(f"      - {req['requirement']}")
                            if 'reason' in req:
                                print(f"        Reason: {req['reason']}")
    
    print("\n" + "=" * 60)
    print("💡 Frontend Integration:")
    print("  - Use 'results' list for main table display")
    print("  - Each result tuple: (Title, Relevant Exp, Total Exp, Projects+Certs, Comment, Status)")
    print("  - Status is 'Pass' if ALL must-have requirements AND relevant exp >= min relevant experience  are met")
    print("  - Status is 'Fail' otherwise")
    print("  - Use 'details' list for popup/modal when user clicks on view details")
    print("  - Each detail contains:")
    print("    * Step-by-step breakdown of the evaluation process")
    print("    * Specific failed requirements with reasons")
    print("    * Requirements checked and their status")
    print("    * Actual values vs required values")
    print("    * If there is any confusion in main.py you can tke help from must_req folder code files and relevant_exp folder code files")
    