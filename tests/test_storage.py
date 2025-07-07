import pathlib
import sys
import json
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from devlab.dev_engine import DevEngine
from devlab.knowledge_db import KnowledgeDB


def _create_config(tmpdir: pathlib.Path) -> pathlib.Path:
    mem_dir = tmpdir / "mem"
    know_dir = tmpdir / "know"
    cfg = {"url": "", "memory_path": str(mem_dir), "knowledge_path": str(know_dir)}
    config_path = tmpdir / "config.json"
    with config_path.open("w", encoding="utf-8") as fh:
        json.dump(cfg, fh)
    return config_path


def test_store_context_unique_files(tmp_path: pathlib.Path) -> None:
    cfg = _create_config(tmp_path)
    engine = DevEngine(cfg)
    engine._store_context("a", "b")
    engine._store_context("c", "d")
    mem_dir = tmp_path / "mem"
    files = sorted(mem_dir.glob("*.json"))
    assert len(files) == 2
    assert files[0].name != files[1].name


def test_knowledge_db_unique_files(tmp_path: pathlib.Path) -> None:
    db = KnowledgeDB(tmp_path)
    p1 = db.add_entry("a", "b")
    p2 = db.add_entry("c", "d")
    assert p1 != p2
    files = sorted(tmp_path.glob("*.json"))
    assert len(files) == 2


def test_log_output_unique_files(tmp_path: pathlib.Path) -> None:
    cfg = _create_config(tmp_path)
    engine = DevEngine(cfg)
    engine.log_dir = tmp_path / "logs"
    engine.log_dir.mkdir(exist_ok=True)

    engine._log_output("one")
    engine._log_output("two")

    logs = sorted(engine.log_dir.glob("*.log"))
    assert len(logs) == 2
    assert logs[0].name != logs[1].name




def test_missing_config(tmp_path: pathlib.Path) -> None:
    missing = tmp_path / "does_not_exist.json"
    with pytest.raises(FileNotFoundError) as excinfo:
        DevEngine(missing)
    assert "Configuration file not found" in str(excinfo.value)
