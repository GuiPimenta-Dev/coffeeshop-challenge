#!/usr/bin/env python3
"""
Script to generate AI feedback for each candidate using Groq's LLM API.
It reads the evaluation.md file from each candidate's folder and uses AI
to generate a summary of strengths and suggestions for improvement.
"""

import os
import sys
import json
import re
import argparse
import time
from pathlib import Path
import requests

# Groq API configuration
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"  # Using Llama 3 70B model

class FeedbackError(Exception):
    """Custom exception for feedback generation errors"""
    pass

def generate_ai_feedback(evaluation_text, candidate_name):
    """
    Generates feedback using Groq's AI based on evaluation.md content
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a senior technical interviewer providing feedback on a candidate's technical assessment.
Review the following evaluation for {candidate_name} and provide:

1. A summary of their strengths (2-3 bullet points)
2. Areas for improvement (2-3 bullet points)
3. Overall assessment (2-3 sentences)

IMPORTANT EVALUATION FORMAT INFORMATION:
- Each criterion has a checkbox: [x] means the candidate met this criterion, [ ] means they did not
- After each checkbox, there is a point value in parentheses (e.g., *(2.0)*) - this is the maximum possible points
- When a checkbox is marked [x], the candidate received those points (the exact amount shown in parentheses)
- When a checkbox is NOT marked [ ], the candidate received 0 points for that criterion 
- The "Total of Points" field shows the candidate's overall score
- The "PASS" or "FAIL" checkbox indicates their final result (PASS is 28+ points)

EXTREMELY IMPORTANT: You MUST base your feedback ONLY on what is actually checked in the evaluation. 
DO NOT make assumptions about what the candidate did well if it's not explicitly checked with [x].
If no boxes are checked in a section, the candidate did not demonstrate any strengths in that area.

For example:
- [x] Feature implemented correctly *(1.0)* = Candidate earned 1.0 point, mention as a strength
- [ ] Documentation complete *(2.0)* = Candidate earned 0 points, mention as area for improvement

Focus your feedback on:
1. ONLY the areas where the candidate excelled (marked with [x])
2. Critical areas that were missing (unmarked checkboxes with high point values)
3. Patterns of strengths and weaknesses across categories
4. Focus more on the topics 2 (Code Quality & Maintainability), 4 (Solution) and 5 (Tests) from the evaluation criteria

Be specific, constructive, and actionable in your feedback. Highlight both what they did well (ONLY if marked with [x]) and what they could improve.

Here is the evaluation to analyze:

{evaluation_text}

IMPORTANT: Before writing feedback, carefully count how many [x] marks are in the evaluation.
If there are no [x] marks or very few, acknowledge this in your feedback and focus primarily on areas for improvement.

Format your response as:

## Strengths
- (Only include strengths that correspond to items marked with [x] in the evaluation)
- (If very few or no items are marked with [x], state that the submission had limited strengths based on the evaluation criteria)

## Areas for Improvement
- (Include the most important items not marked with [x], especially those with high point values)
- (Be specific about what was missing and how it could be improved)

## Overall Assessment
(2-3 sentences summarizing the performance based on what was actually checked in the evaluation. Be honest but constructive about areas for growth.)

Make your feedback specific, actionable, and focused on helping the candidate grow as a developer.
"""

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            feedback = result["choices"][0]["message"]["content"]
            return feedback
        else:
            raise FeedbackError("No feedback content in the API response")
            
    except requests.exceptions.RequestException as e:
        raise FeedbackError(f"API request failed: {str(e)}")


def process_candidate_folder(folder_path):
    """Process a candidate folder and generate feedback"""
    
    # Format candidate name from folder name
    candidate_name = folder_path.name.replace('_', ' ').title()
    
    # Path to the README.md (evaluation) file
    readme_path = folder_path / "README.md"
    if not readme_path.exists():
        raise FeedbackError(f"Candidate {candidate_name} is missing a README.md file")
    
    # Read the evaluation file
    try:
        with open(readme_path, 'r', encoding='utf-8') as file:
            evaluation_text = file.read()
    except Exception as e:
        raise FeedbackError(f"Error reading evaluation file: {str(e)}")
    
    # Check if feedback already exists in README
    feedback_section = "# Feedback"
    if feedback_section in evaluation_text:
        print(f"Feedback for {candidate_name} already exists in README.md. Skipping...")
        return readme_path
    
    # Generate AI feedback
    print(f"Generating feedback for {candidate_name}...")
    feedback = generate_ai_feedback(evaluation_text, candidate_name)
    
    # Append feedback to README.md
    try:
        # Format the feedback with a clear separator
        formatted_feedback = f"\n\n---\n\n#  Feedback\n\n{feedback}"
        
        # Append to the README
        with open(readme_path, 'a', encoding='utf-8') as file:
            file.write(formatted_feedback)
            
        print(f"Feedback appended to README.md for {candidate_name}")
        return readme_path
    except Exception as e:
        raise FeedbackError(f"Error updating README.md with feedback: {str(e)}")
    


def main():
    """Main function to process all candidate folders"""
    
    parser = argparse.ArgumentParser(description="Generate AI feedback for candidate evaluations")
    parser.add_argument("--candidate", help="Process only the specified candidate folder")
    args = parser.parse_args()
    
    try:
        current_dir = Path('.')
        processed_count = 0
        
        # If a specific candidate is specified
        if args.candidate:
            folder_path = current_dir / args.candidate
            if not folder_path.exists() or not folder_path.is_dir():
                raise FeedbackError(f"Candidate folder '{args.candidate}' not found")
            
            feedback_path = process_candidate_folder(folder_path)
            print(f"\nFeedback generated for {args.candidate}!")
            print(f"Feedback saved to: {feedback_path}")
            processed_count = 1
        
        # Process all folders
        else:
            print("\n=== Generating AI Feedback for All Candidates ===\n")
            
            skipped_count = 0
            for item in current_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    try:
                        # Check README.md for existing feedback
                        readme_path = item / "README.md"
                        if not readme_path.exists():
                            print(f"✗ Skipping {item.name}: No README.md file found")
                            continue
                            
                        # Check if feedback already exists in README
                        try:
                            with open(readme_path, 'r', encoding='utf-8') as file:
                                if "#  Feedback" in file.read():
                                    print(f"✓ Skipping {item.name}: Feedback already exists in README.md")
                                    skipped_count += 1
                                    continue
                        except Exception:
                            print(f"✗ Error reading README.md for {item.name}")
                            continue
                            
                        feedback_path = process_candidate_folder(item)
                        print(f"✓ Feedback saved to: {feedback_path}")
                        processed_count += 1
                        # Add a small delay to avoid API rate limits
                        time.sleep(0.5)
                    except FeedbackError as e:
                        print(f"✗ Error for {item.name}: {str(e)}")
        
        print(f"\nProcess complete! Generated feedback for {processed_count} candidate(s).")
        if skipped_count > 0:
            print(f"Skipped {skipped_count} candidate(s) with existing feedback.")
        
    except FeedbackError as e:
        print(f"\nERROR: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()