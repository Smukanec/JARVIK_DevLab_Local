"""Main orchestrator for DevLab.

This module provides the :class:`DevEngine` which ties together the
pipeline and simple persistent storage of prompts and results.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from .pipeline import Pipeline
from .knowledge_db import KnowledgeDB

_CONFIG_PATH = Path(__file__).with_name("devlab_config.json")


def _load_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {path}. "
            "Run install.sh or pass --config to devlab-cli."
        )
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


class DevEngine:
    """Orchestrates prompts through the pipeline and stores context."""

    def __init__(self, config_path: Path | None = None) -> None:
        cfg_path = config_path or _CONFIG_PATH
        self.config = _load_config(cfg_path)

        mem_path = self.config.get("memory_path", "dev_memory")
        self.memory_dir = Path(mem_path)
        if not self.memory_dir.is_absolute():
            self.memory_dir = Path(__file__).with_name(mem_path)

        know_path = self.config.get("knowledge_path", "knowledge_db")
        self.knowledge_dir = Path(know_path)
        if not self.knowledge_dir.is_absolute():
            self.knowledge_dir = Path(__file__).with_name(know_path)

        self.log_dir = Path(__file__).with_name("logs")

        self.memory_dir.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)
        self.knowledge_dir.mkdir(exist_ok=True)

        self.knowledge_db = KnowledgeDB(self.knowledge_dir)

        self.pipeline = Pipeline(self.config.get("url", ""), self.log_dir)

    def _store_context(self, prompt: str, result: str) -> None:
        """Persist prompt and result into the memory directory."""
        # use microsecond precision to avoid collisions when called quickly
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
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
        self.knowledge_db.add_entry(
            prompt, result, ["programování", "technologie"]
        )
        if log:
            self._log_output(result)
        return result

    def export_memory(self, path: str | Path | None = None) -> Path:
        """Export memory directory as a zip archive.

        Parameters
        ----------
        path:
            Optional output file path. Defaults to ``memory_export.zip`` in the
            current working directory.
        """
        out_path = Path(path or "memory_export.zip")
        if not out_path.is_absolute():
            out_path = Path.cwd() / out_path

        import zipfile

        with zipfile.ZipFile(out_path, "w") as zf:
            for file in sorted(self.memory_dir.glob("*.json")):
                zf.write(file, arcname=file.name)
        return out_path

    def export_knowledge(self, path: str | Path | None = None) -> Path:
        """Export the knowledge database as a single JSON file."""
        out_path = Path(path or "knowledge_export.json")
        if not out_path.is_absolute():
            out_path = Path.cwd() / out_path
        return self.knowledge_db.export(out_path)
