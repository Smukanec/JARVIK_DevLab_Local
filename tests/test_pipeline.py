import pathlib
import sys
import json
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from devlab.pipeline import Pipeline
from devlab.dev_engine import DevEngine
import devlab.pipeline as pipeline_mod


def _create_config(tmpdir: pathlib.Path) -> pathlib.Path:
    mem_dir = tmpdir / "mem"
    know_dir = tmpdir / "know"
    cfg = {"url": "", "memory_path": str(mem_dir), "knowledge_path": str(know_dir)}
    config_path = tmpdir / "config.json"
    with config_path.open("w", encoding="utf-8") as fh:
        json.dump(cfg, fh)
    return config_path


@pytest.mark.parametrize(
    "prompt,language,models",
    [
        ("def foo():\n    pass", "python", ["Command R+", "StrCoder"]),
        ("<html></html>", "html", ["Code Llama"]),
        ("<?php echo 'hi'; ?>", "php", ["Code Llama"]),
        ("just some text", "text", ["Command R+"]),
    ],
)
def test_pipeline_model_selection(tmp_path, prompt, language, models):
    pipeline = Pipeline("", log_dir=tmp_path)
    pipeline.run(prompt)
    logs = list(tmp_path.glob("*_pipeline.log"))
    assert len(logs) == 1
    content = logs[0].read_text()
    assert f"language: {language}" in content
    assert f"models: {', '.join(models)}" in content


def test_pipeline_unique_logs(tmp_path):
    pipeline = Pipeline("", log_dir=tmp_path)
    pipeline.run("print('a')")
    pipeline.run("print('b')")
    logs = sorted(tmp_path.glob("*_pipeline.log"))
    assert len(logs) == 2
    assert logs[0].name != logs[1].name


def test_pipeline_separate_error_logs(tmp_path, monkeypatch):
    dir1 = tmp_path / "one"
    dir2 = tmp_path / "two"
    p1 = Pipeline("", log_dir=dir1)
    p2 = Pipeline("", log_dir=dir2)

    def fail(*args, **kwargs):
        raise pipeline_mod.requests.RequestException("boom")

    monkeypatch.setattr(pipeline_mod.requests, "post", fail)

    p1._run_model("m", "x")
    p2._run_model("m", "x")

    log1 = dir1 / "errors.log"
    log2 = dir2 / "errors.log"
    assert log1.is_file()
    assert log2.is_file()
    assert log1 != log2
    assert log1.read_text()
    assert log2.read_text()


def test_export_functions(tmp_path):
    cfg = _create_config(tmp_path)
    engine = DevEngine(cfg)
    engine._store_context("a", "b")
    engine._store_context("c", "d")
    engine.knowledge_db.add_entry("e", "f")
    engine.knowledge_db.add_entry("g", "h")

    mem_zip = engine.export_memory(tmp_path / "mem.zip")
    assert mem_zip.is_file()
    import zipfile

    with zipfile.ZipFile(mem_zip) as zf:
        names = sorted(zf.namelist())
    assert len(names) == 2
    for n in names:
        assert n.endswith(".json")

    know_json = engine.export_knowledge(tmp_path / "know.json")
    assert know_json.is_file()
    data = json.loads(know_json.read_text())
    assert isinstance(data, list)
    assert len(data) == 2
