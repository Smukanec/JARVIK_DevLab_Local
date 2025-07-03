#!/usr/bin/env bash
# Upgrade jarvik-devlab to the latest available version
set -euo pipefail

# Upgrade the package via pip
python3 -m pip install --upgrade jarvik-devlab

echo "jarvik-devlab upgraded successfully"
