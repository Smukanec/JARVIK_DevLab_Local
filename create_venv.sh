#!/usr/bin/env bash
# Create and activate a local Python virtual environment
set -euo pipefail

VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR"
    python3 -m venv "$VENV_DIR"
    if [ ! -f "$VENV_DIR/bin/activate" ]; then
        echo "Failed to create virtual environment – install python3-venv or run 'python3 -m ensurepip --upgrade'" >&2
        exit 1
    fi
fi

# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

# Ensure pip is available and up to date
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip

echo "Virtual environment activated."
echo "Install dependencies with 'pip install -r requirements.txt'"
