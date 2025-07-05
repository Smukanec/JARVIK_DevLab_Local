import pathlib
import sys
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from devlab.utils import detect_language

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

