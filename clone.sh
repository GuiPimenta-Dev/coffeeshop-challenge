#!/bin/bash
set -e

# Script to clone a GitHub repository and create a candidate folder
# Usage: ./setup.sh --repo=https://github.com/username/repo --name="John Doe"

# Default values
GITHUB_REPO=""
CANDIDATE_NAME=""

# Parse named parameters
while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo=*)
      GITHUB_REPO="${1#*=}"
      shift
      ;;
    --repo)
      GITHUB_REPO="$2"
      shift 2
      ;;
    --name=*)
      CANDIDATE_NAME="${1#*=}"
      shift
      ;;
    --name)
      CANDIDATE_NAME="$2"
      shift 2
      ;;
    *)
      # Unknown option
      echo "Warning: Unknown option $1"
      shift
      ;;
  esac
done

# Check if required parameters are provided
if [ -z "$GITHUB_REPO" ] || [ -z "$CANDIDATE_NAME" ]; then
  echo "Error: Missing required parameters"
  echo "Usage: ./setup.sh --repo=https://github.com/username/repo --name=\"John Doe\""
  echo "   or: ./setup.sh --repo https://github.com/username/repo --name \"John Doe\""
  echo ""
  echo "Parameters:"
  echo "  --repo    GitHub repository URL"
  echo "  --name    Candidate name (will be converted to lowercase with underscores)"
  exit 1
fi

echo "GitHub Repository: $GITHUB_REPO"
echo "Candidate Name: $CANDIDATE_NAME"

# Format candidate name: lowercase and replace spaces with underscores
FORMATTED_NAME=$(echo "$CANDIDATE_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '_')
echo "Formatted candidate name: $FORMATTED_NAME"

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Script directory: $SCRIPT_DIR"

# Create candidate folder
echo "Creating directory structure..."
mkdir -p "$FORMATTED_NAME"

# Clone the repo directly to the candidate's folder
echo "Cloning repository $GITHUB_REPO..."
git clone "$GITHUB_REPO" "$FORMATTED_NAME/challenge"

echo "Removing .git folder..."
rm -rf "$FORMATTED_NAME/challenge/.git"

# Check if clone was successful
if [ $? -ne 0 ]; then
  echo "Error: Failed to clone repository"
  exit 1
fi

# Copy evaluation.md to candidate folder as README.md
cp "$SCRIPT_DIR/evaluation.md" "$FORMATTED_NAME/README.md"

# Check if file copy was successful
if [ $? -ne 0 ]; then
  echo "Error: Failed to copy evaluation.md"
  exit 1
fi