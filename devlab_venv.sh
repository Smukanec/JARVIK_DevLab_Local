#!/usr/bin/env bash
# Run DevLab under a local virtual environment.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Determine whether to run install or upgrade. The first positional argument can
# be "install" (default) or "upgrade". Any additional arguments are passed to
# devlab-cli.
cmd="install"
if [[ "${1:-}" == "upgrade" ]]; then
    cmd="upgrade"
    shift
elif [[ "${1:-}" == "install" ]]; then
    shift
fi

VENV_DIR="$SCRIPT_DIR/.venv"
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

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
if [ "$cmd" = "upgrade" ]; then
    ./upgrade.sh
else
    ./install.sh
fi

python3 -m devlab.cli "$@"
