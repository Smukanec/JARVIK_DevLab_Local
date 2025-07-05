#!/usr/bin/env bash
# Upgrade jarvik-devlab to the latest available version
set -euo pipefail

# Exit if running under an externally managed Python without virtualenv
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

# Upgrade the package via pip
python3 -m pip install --upgrade jarvik-devlab

echo "jarvik-devlab upgraded successfully"
