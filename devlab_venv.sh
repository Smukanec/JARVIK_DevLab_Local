#!/usr/bin/env bash
# Run DevLab under a local virtual environment.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR="$SCRIPT_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR"
    python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
./install.sh

python -m DevLab.cli "$@"
