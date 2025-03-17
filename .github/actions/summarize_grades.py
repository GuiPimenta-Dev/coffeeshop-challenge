#!/usr/bin/env python3
"""
Script to extract final grades from candidate evaluation README files.
It scans all directories in the current path, looks for README.md files,
and extracts the total points assigned to each candidate.

The script creates a candidates.md file with evaluation statistics and 
a table of all candidates sorted by their grades.

If any folder is missing a grade, the script will exit with an error message.
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime
import statistics

# Constants
PASSING_THRESHOLD = 28  # Minimum points required to pass
CANDIDATES_PATH = Path("./candidates.md")

class GradingError(Exception):
    """Custom exception for grading errors"""
    pass

def extract_grade(readme_path):
    """Extract the total points from a README.md file."""
    try:
        with open(readme_path, 'r', encoding='utf-8') as file:
            content = file.read()

            # Look for "Total of Points: X" or similar pattern
            points_match = re.search(r'Total\s+of\s+Points:\s*(\d+)', content, re.IGNORECASE)
            
            if points_match:
                points_str = points_match.group(1)
                if not points_str or not points_str.strip():
                    raise GradingError("Total points field is empty")
                return int(points_str)
            else:
                raise GradingError("Total points field not found")
                
    except GradingError:
        raise
    except Exception as e:
        raise GradingError(f"Error reading README file: {str(e)}")


def get_all_grades():
    """Scan all directories and get grades from README files."""
    results = []
    current_dir = Path('.')
    
    for item in current_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.') and not item.name == "venv":
            # Format candidate name for better readability - replace underscores with spaces and capitalize
            candidate_name = item.name.replace('_', ' ').title()
            
            # Check for README.md in the directory
            readme_path = item / "README.md"
            if not readme_path.exists():
                raise GradingError(f"Candidate '{candidate_name}' (folder: {item.name}) is missing a README.md file")
            
            try:
                points = extract_grade(readme_path)
                results.append({
                    'candidate': candidate_name,
                    'folder': item.name,
                    'points': points,
                    'passed': points >= PASSING_THRESHOLD
                })
            except GradingError as e:
                raise GradingError(f"Error grading candidate '{candidate_name}' (folder: {item.name}): {str(e)}")
    
    return results


def create_candidates_md(results):
    """Create a candidates.md file with statistics and grades table."""
    if not results:
        return
        
    # Sort results by points (highest first)
    results.sort(key=lambda x: (-x['points'], x['candidate'].lower()))
    
    # Calculate summary statistics
    total_candidates = len(results)
    all_points = [r['points'] for r in results]
    total_points = sum(all_points)
    average_points = total_points / total_candidates if total_candidates > 0 else 0
    passed_candidates = sum(1 for r in results if r['passed'])
    failed_candidates = total_candidates - passed_candidates
    
    # Additional statistics
    top_grade = max(all_points) if all_points else 0
    min_grade = min(all_points) if all_points else 0
    median_grade = statistics.median(all_points) if all_points else 0
    
    # Create the document
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    content = f"""# Candidate Evaluation Results

*Last updated: {timestamp}*

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total candidates | {total_candidates} |
| Top grade | {top_grade} |
| Minimum grade | {min_grade} |
| Average grade | {average_points:.2f} |
| Median grade | {median_grade} |
| Approved candidates | {passed_candidates} ({passed_candidates/total_candidates*100:.1f}%) |
| Failed candidates | {failed_candidates} ({failed_candidates/total_candidates*100:.1f}%) |

## All Candidates

| Candidate | Grade | Status |
|-----------|-------|--------|
"""
    
    # Add each candidate to the table
    for r in results:
        status = "PASS" if r['passed'] else "FAIL"
        content += f"| {r['candidate']} | {r['points']} | {status} |\n"
    
    try:
        # Write the content to candidates.md
        with open(CANDIDATES_PATH, 'w', encoding='utf-8') as file:
            file.write(content)
            
        print(f"candidates.md created with evaluation results.")
        
    except Exception as e:
        print(f"WARNING: Failed to create candidates.md: {str(e)}")


def main():
    """Main function to run the script."""
    try:
        results = get_all_grades()
        
        if not results:
            print("No candidate directories found.")
            return
        
        # Sort results by points (highest first)
        results.sort(key=lambda x: (-x['points'], x['candidate'].lower()))
        
        # Calculate summary statistics
        total_candidates = len(results)
        total_points = sum(r['points'] for r in results)
        average_points = total_points / total_candidates if total_candidates > 0 else 0
        passed_candidates = sum(1 for r in results if r['passed'])
        failed_candidates = total_candidates - passed_candidates
        
        print("\n=== Summary ===")
        print(f"Total candidates evaluated: {total_candidates}")
        print(f"Total points awarded: {total_points}")
        print(f"Average points per candidate: {average_points:.2f}")
        print(f"Passed candidates: {passed_candidates} ({passed_candidates/total_candidates*100:.1f}%)")
        print(f"Failed candidates: {failed_candidates} ({failed_candidates/total_candidates*100:.1f}%)")
        
        # Create candidates.md with the evaluation results
        create_candidates_md(results)
        
    except GradingError as e:
        print(f"\nERROR: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()