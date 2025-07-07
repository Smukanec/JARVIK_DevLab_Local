from __future__ import annotations

"""Utility helpers for the DevLab package."""

import os
import re
import sysconfig
from pathlib import Path


def detect_language(prompt: str) -> str:
    """Very small heuristic to guess the programming language in *prompt*.

    The function looks for common keywords or code fragments and returns one
    of ``"python"``, ``"html"``, ``"php"`` or ``"text"`` (default).
    """
    if not prompt:
        return "text"
    lowered = prompt.lower()
    if "<?php" in lowered or re.search(r"\bphp\b", lowered):
        return "php"
    if "<html" in lowered or "</html>" in lowered:
        return "html"
    if "python" in lowered or re.search(r"\bdef\b", lowered) or "import " in lowered:
        return "python"
    return "text"


def detect_externally_managed_python() -> bool:
    """Return ``True`` if running under an externally managed Python install.

    The check mimics the logic used by ``install.sh``. It looks for an
    ``EXTERNALLY-MANAGED`` marker file inside ``sysconfig.get_paths()["purelib"]``
    or any of its parent directories when no virtual environment is active.
    """

    if os.environ.get("VIRTUAL_ENV"):
        return False

    purelib = Path(sysconfig.get_paths()["purelib"])
    for parent in [purelib] + list(purelib.parents):
        if (parent / "EXTERNALLY-MANAGED").exists():
            return True
    return False
