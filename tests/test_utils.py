import pathlib
import sys
import sysconfig
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from devlab.utils import detect_language, detect_externally_managed_python

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


def test_detect_externally_managed_python(monkeypatch, tmp_path):
    monkeypatch.delenv("VIRTUAL_ENV", raising=False)
    pure = tmp_path / "lib"
    pure.mkdir()
    monkeypatch.setattr(
        sysconfig, "get_paths", lambda: {"purelib": str(pure)}
    )
    (pure / "EXTERNALLY-MANAGED").touch()
    assert detect_externally_managed_python() is True


def test_detect_externally_managed_python_virtualenv(monkeypatch, tmp_path):
    monkeypatch.setenv("VIRTUAL_ENV", "1")
    pure = tmp_path / "lib"
    pure.mkdir()
    monkeypatch.setattr(
        sysconfig, "get_paths", lambda: {"purelib": str(pure)}
    )
    (pure / "EXTERNALLY-MANAGED").touch()
    assert detect_externally_managed_python() is False



