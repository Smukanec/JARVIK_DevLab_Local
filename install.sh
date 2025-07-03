#!/usr/bin/env bash
# Simple installation script for jarvik-devlab
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Upgrade pip to ensure latest features
python3 -m pip install --upgrade pip

# Install the package from source
python3 -m pip install .

echo "jarvik-devlab installed successfully"
