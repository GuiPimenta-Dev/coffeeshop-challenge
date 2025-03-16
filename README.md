# Trio CoffeeShop Challenge


## Evaluation Results

*Last updated: 2025-03-16 18:51:42*

### Summary Statistics
- **Total candidates evaluated:** 1
- **Average score:** 27.00 points
- **Pass rate:** 0/1 (0.0%)
- **Failed candidates:** 1 (100.0%)




## Overview

This repository contains scripts to set up, clone, and evaluate candidate repositories for the Trio CoffeeShop coding challenge.

### Clone Script

The `clone.sh` script will:
1. Clone a GitHub repository
2. Create a folder with the candidate's name (formatted to lowercase with underscores)
3. Copy the evaluation.md file as README.md into the cloned repository

## Usage Instructions

### For Unix/Linux/macOS

1. Make the script executable (only needed once):
   ```bash
   chmod +x clone.sh
   ```

2. Run the script:
   ```bash
   ./clone.sh --repo https://github.com/username/repo --name "Candidate Name"
   ```
   
### For Windows

Windows users have multiple options to run the script:

#### Option 1: Using Git Bash (recommended)
If you have Git for Windows installed, it comes with Git Bash:

1. Open Git Bash
2. Navigate to the repository directory
3. Make the script executable (only needed once):
   ```bash
   chmod +x clone.sh
   ```
4. Run the script:
   ```bash
   ./clone.sh --repo https://github.com/username/repo --name "Candidate Name"
   ```

#### Option 2: Using Windows Subsystem for Linux (WSL)
If you have WSL installed:

1. Open WSL terminal
2. Navigate to the repository directory
3. Make the script executable (only needed once):
   ```bash
   chmod +x clone.sh
   ```
4. Run the script:
   ```bash
   ./clone.sh --repo https://github.com/username/repo --name "Candidate Name"
   ```

#### Option 3: Manual Steps (if you can't run bash scripts)
If you're unable to run bash scripts on your Windows system:

1. Create a folder with the candidate's name (replacing spaces with underscores and lowercase)
2. Clone the repository into that folder:
   ```
   git clone https://github.com/username/repo ${CANDIDATE_NAME}/challenge
   ```
3. Delete `.git` from `${CANDIDATE_NAME}/challenge` folder
4. Copy the evaluation.md file as README.md into the cloned repository

## Parameters

* `--repo` - The GitHub repository URL to clone
* `--name` - The candidate's name (will be converted to lowercase with underscores)

## Example

```bash
./clone.sh --repo https://github.com/GuiPimenta-Dev/got --name "John Smith"
```

This will:
1. Create a directory called "john_smith"
2. Clone the specified repository into it
3. Copy evaluation.md as README.md to the repository

## Automated Evaluation

This repository includes scripts and workflows for automated evaluation:

### Summarizing Evaluations

The `.github/scripts/summarize_grades.py` script:
- Scans all candidate directories for README.md files
- Extracts the total points from each evaluation
- Updates the main README.md with summary statistics
- Runs automatically via GitHub Actions when evaluations change

### AI Feedback Generation

The `.github/scripts/generate_feedback.py` script:
- Analyzes completed evaluations using Groq's AI API
- Generates personalized feedback for each candidate
- Appends feedback directly to each candidate's README.md file
- Can be triggered manually through GitHub Actions workflow

### GitHub Actions

The repository includes a GitHub Actions workflow that:
- Automatically updates statistics when evaluations change
- Can be manually triggered to generate AI feedback
- Commits changes back to the repository automatically

See `.github/workflows/evaluation.yml` for implementation details.