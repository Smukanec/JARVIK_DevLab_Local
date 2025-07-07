"""Pipeline module for running models sequentially.

The pipeline inspects an input prompt, guesses the programming language
and chooses appropriate Jarvik models. Information about the detected
language and chosen models is written to ``logs/`` for traceability.
"""

from __future__ import annotations

from typing import Any, Dict, List
from pathlib import Path
from datetime import datetime
import logging
import requests

from .utils import detect_language


class Pipeline:
    """Sequential pipeline for running Jarvik models."""

    def __init__(self, base_url: str, log_dir: Path | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.log_dir = log_dir or Path(__file__).with_name("logs")
        self.log_dir.mkdir(exist_ok=True)

        # initialize a dedicated logger for this pipeline instance
        self.logger = logging.getLogger(f"{__name__}.{id(self)}")
        self.logger.handlers.clear()
        handler = logging.FileHandler(self.log_dir / "errors.log")
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        )
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

    def _run_model(self, model: str, prompt: str) -> str:
        """Call a Jarvik model and return its output.

        Parameters
        ----------
        model:
            Name of the model to invoke.
        prompt:
            Text prompt for the model.
        """
        payload: Dict[str, Any] = {"model": model, "prompt": prompt}
        try:
            resp = requests.post(
                f"{self.base_url}/run", json=payload, timeout=60
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("output", "")
        except requests.HTTPError as exc:
            status = getattr(exc.response, "status_code", "unknown")
            msg = getattr(exc.response, "text", str(exc))
            self.logger.error(
                "HTTP error running model %s (status %s): %s", model, status, msg
            )
        except requests.RequestException:
            # network or timeout related errors
            self.logger.exception("Request failed for model %s", model)
        except Exception:
            # JSON decode or other unexpected errors
            self.logger.exception("Unexpected error running model %s", model)
        return ""

    def _log_selection(self, language: str, models: List[str]) -> None:
        """Write the chosen language and models into the log directory."""
        # use microsecond precision to avoid log filename collisions when
        # multiple pipeline runs happen within the same second
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        path = self.log_dir / f"{timestamp}_pipeline.log"
        with path.open("w", encoding="utf-8") as fh:
            fh.write(f"language: {language}\n")
            fh.write(f"models: {', '.join(models)}\n")

    def run(self, prompt: str) -> str:
        """Run the pipeline with the given prompt."""
        language = detect_language(prompt)
        if language in {"html", "php"}:
            models = ["Code Llama"]
        elif language == "python":
            models = ["Command R+", "StrCoder"]
        else:
            models = ["Command R+"]

        self._log_selection(language, models)

        output = prompt
        for model in models:
            output = self._run_model(model, output)
        return output
