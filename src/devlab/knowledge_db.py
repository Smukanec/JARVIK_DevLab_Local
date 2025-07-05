from __future__ import annotations

"""Simple JSON based knowledge database."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, List


class KnowledgeDB:
    """Stores prompt/response pairs as JSON files."""

    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path
        self.base_path.mkdir(exist_ok=True)

    def add_entry(self, prompt: str, result: str, topics: List[str] | None = None) -> Path:
        """Persist a single knowledge entry.

        Parameters
        ----------
        prompt:
            Input prompt text.
        result:
            Result returned by the pipeline.
        topics:
            Optional list of topics associated with the entry.
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        entry = {
            "prompt": prompt,
            "result": result,
            "topics": topics or [],
            "timestamp": timestamp,
        }
        path = self.base_path / f"{timestamp}.json"
        with path.open("w", encoding="utf-8") as fh:
            json.dump(entry, fh, ensure_ascii=False, indent=2)
        return path

    def export(self, path: str | Path) -> Path:
        """Export all entries into a single JSON file."""
        data: List[Any] = []
        for file in sorted(self.base_path.glob("*.json")):
            try:
                with file.open("r", encoding="utf-8") as fh:
                    data.append(json.load(fh))
            except json.JSONDecodeError:
                continue
        out_path = Path(path)
        with out_path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        return out_path
