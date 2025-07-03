"""Main orchestrator for DevLab.

This module provides the :class:`DevEngine` which ties together the
pipeline and simple persistent storage of prompts and results.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from .pipeline import Pipeline

_CONFIG_PATH = Path(__file__).with_name("devlab_config.json")


def _load_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing configuration file: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


class DevEngine:
    """Orchestrates prompts through the pipeline and stores context."""

    def __init__(self, config_path: Path | None = None) -> None:
        cfg_path = config_path or _CONFIG_PATH
        self.config = _load_config(cfg_path)
        self.memory_dir = Path(__file__).with_name("dev_memory")
        self.log_dir = Path(__file__).with_name("logs")
        self.memory_dir.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)
        self.pipeline = Pipeline(self.config.get("url", ""), self.log_dir)

    def _store_context(self, prompt: str, result: str) -> None:
        """Persist prompt and result into the dev_memory directory."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        entry = {
            "prompt": prompt,
            "result": result,
            "topics": ["programování", "technologie"],
            "timestamp": timestamp,
        }
        path = self.memory_dir / f"{timestamp}.json"
        with path.open("w", encoding="utf-8") as fh:
            json.dump(entry, fh, ensure_ascii=False, indent=2)

    def _log_output(self, text: str) -> None:
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        path = self.log_dir / f"{timestamp}.log"
        with path.open("w", encoding="utf-8") as fh:
            fh.write(text)

    def run(self, prompt: str, log: bool = False) -> str:
        """Process a prompt through the pipeline."""
        result = self.pipeline.run(prompt)
        self._store_context(prompt, result)
        if log:
            self._log_output(result)
        return result
