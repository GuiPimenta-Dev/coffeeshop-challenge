#!/usr/bin/env python3
"""
Script to extract final grades from candidate evaluation README files.
It scans all directories in the current path, looks for README.md files,
and extracts the total points assigned to each candidate.

The script also updates the main README.md with evaluation statistics.

If any folder is missing a grade, the script will exit with an error message.
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

# Constants
PASSING_THRESHOLD = 28  # Minimum points required to pass
README_PATH = Path("./README.md")
RESULTS_SECTION_START = "## Evaluation Results"
RESULTS_SECTION_END = "## Overview"

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


def update_readme_with_results(results):
    """Update the main README.md with evaluation results."""
    if not results:
        return
        
    # Calculate summary statistics
    total_candidates = len(results)
    total_points = sum(r['points'] for r in results)
    average_points = total_points / total_candidates if total_candidates > 0 else 0
    passed_candidates = sum(1 for r in results if r['passed'])
    failed_candidates = total_candidates - passed_candidates
    
    # Sort results by points (highest first)
    results.sort(key=lambda x: (-x['points'], x['candidate'].lower()))
    
    # Create the results section
    timestamp = datetime.now().strftime("%Y-%m-%d")
    results_section = f"""## Evaluation Results

*Last updated: {timestamp}*

### Summary Statistics
- **Total candidates evaluated:** {total_candidates}
- **Average score:** {average_points:.2f} points
- **Pass rate:** {passed_candidates}/{total_candidates} ({passed_candidates/total_candidates*100:.1f}%)
- **Failed candidates:** {failed_candidates} ({failed_candidates/total_candidates*100:.1f}%)

"""
    
    results_section += "\n"
    
    try:
        # Read the current README
        with open(README_PATH, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Check if the results section already exists
        if RESULTS_SECTION_START in content:
            # Replace the existing results section
            pattern = f"{RESULTS_SECTION_START}.*?{RESULTS_SECTION_END}"
            updated_content = re.sub(pattern, f"{results_section}{RESULTS_SECTION_END}", content, flags=re.DOTALL)
        else:
            # Add the results section at the top, after the title
            title_end = content.find('\n', content.find('#'))
            updated_content = content[:title_end + 1] + "\n\n" + results_section + "\n" + content[title_end + 1:]
        
        # Write the updated content back to the README
        with open(README_PATH, 'w', encoding='utf-8') as file:
            file.write(updated_content)
            
        print(f"README.md updated with evaluation results.")
        
    except Exception as e:
        print(f"WARNING: Failed to update README.md: {str(e)}")


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
        
        # Update the README with the evaluation results
        update_readme_with_results(results)
        
    except GradingError as e:
        print(f"\nERROR: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()