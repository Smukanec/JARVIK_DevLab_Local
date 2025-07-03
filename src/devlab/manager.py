"""DevLab manager orchestrating generation and validation."""

from typing import Optional

from .generator import CodeGenerator
from .validator import CodeValidator

class DevLabManager:
    """Coordinates code generation and validation steps."""

    def __init__(self,
                 generator: Optional[CodeGenerator] = None,
                 validator: Optional[CodeValidator] = None) -> None:
        self.generator = generator or CodeGenerator()
        self.validator = validator or CodeValidator()

    def run(self, prompt: str) -> str:
        """Generate code for the prompt and validate it."""
        code = self.generator.generate(prompt)
        if self.validator.validate(code):
            return code
        # Report validation failure with an explicit error
        raise ValueError("Generated code failed validation")
