#!/usr/bin/env bash
# Upgrade devlab to the latest available version
set -euo pipefail

# Automatically handle externally managed Python installations
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
        echo "Detected externally managed Python installation." >&2
        echo "Creating a local virtual environment via ./devlab_venv.sh upgrade" >&2
        exec "$(dirname "$0")/devlab_venv.sh" upgrade "$@"
    fi
fi

# Upgrade the package via pip
python3 -m pip install --upgrade devlab

echo "devlab upgraded successfully"
