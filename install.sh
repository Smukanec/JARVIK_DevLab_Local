#!/usr/bin/env bash
# Simple installation script for jarvik-devlab
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Warn if run in an externally managed Python environment without an active
# virtual environment.
if [ -z "${VIRTUAL_ENV:-}" ]; then
    if python3 - <<'EOF'
import sysconfig, pathlib, sys
p = pathlib.Path(sysconfig.get_paths()["purelib"])
for parent in [p] + list(p.parents):
    if (parent / "EXTERNALLY-MANAGED").exists():
        sys.exit(0)
sys.exit(1)
EOF
    then
        echo "Error: detected externally managed Python installation." >&2
        echo "Create and activate a virtual environment before running install.sh or upgrade.sh." >&2
        echo "Run ./devlab_venv.sh to create and activate a virtual environment automatically." >&2
        exit 1
    fi
fi

# Upgrade pip to ensure latest features
python3 -m pip install --upgrade pip

# Install the package from source
python3 -m pip install .

echo "jarvik-devlab installed successfully"
