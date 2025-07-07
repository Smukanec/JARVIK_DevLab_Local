import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from devlab.generator import CodeGenerator
from devlab.validator import CodeValidator


def test_generator_echoes_prompt():
    gen = CodeGenerator()
    prompt = "print('hi')"
    output = gen.generate(prompt)
    assert prompt in output
    assert output.startswith("#")


def test_validator_checks_non_empty():
    val = CodeValidator()
    assert val.validate("code") is True
    assert val.validate("") is False
    assert val.validate("   ") is False
