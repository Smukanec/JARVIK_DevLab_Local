import importlib.util
import pathlib

import pytest

# Load the utils module directly to avoid importing the whole DevLab package
_utils_path = pathlib.Path(__file__).resolve().parents[1] / "DevLab" / "utils.py"
spec = importlib.util.spec_from_file_location("DevLab.utils", _utils_path)
_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_utils)

detect_language = _utils.detect_language

@pytest.mark.parametrize(
    "prompt,expected",
    [
        ("def foo(bar):\n    return bar", "python"),
        ("import os", "python"),
        ("<html><body>Hello</body></html>", "html"),
        ("<?php echo 'Hi'; ?>", "php"),
        ("Some random text", "text"),
        ("", "text"),
    ],
)
def test_detect_language(prompt, expected):
    assert detect_language(prompt) == expected

