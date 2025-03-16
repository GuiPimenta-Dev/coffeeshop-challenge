# Evaluation Scripts

This directory contains scripts used to process candidate evaluations for the Trio Selective Process.

## Scripts

### summarize_grades.py

This script scans all candidate directories, extracts grades from their README.md files, and updates the main README.md with a summary of results. It calculates statistics like:

- Total number of candidates evaluated
- Average score
- Pass/fail rates

Usage:
```bash
python summarize_grades.py
```

### generate_feedback.py

This script uses the Groq AI API to generate detailed feedback for each candidate based on their evaluation. It creates a FEEDBACK.md file in each candidate's directory with:

- Strengths
- Areas for improvement
- Overall assessment

The script will only generate feedback for candidates who don't already have a FEEDBACK.md file.

Usage:
```bash
python generate_feedback.py
```

Requires environment variable:
- GROQ_API_KEY: API key for accessing Groq's API

### Mock Services

The following mock services simulate external APIs used in the challenge:

- **mock_notification.py**: Simulates an email notification service with a 20% failure rate
- **mock_payment.py**: Simulates a payment processing service with a 0.3% failure rate

These are intended to be deployed as serverless functions but can be used locally for testing.

## GitHub Actions Integration

These scripts are integrated with GitHub Actions to automatically:

1. Update the main README.md with evaluation statistics when candidate evaluations change
2. Generate AI feedback for candidates when manually triggered

See the workflow configuration in `.github/workflows/evaluation.yml`.