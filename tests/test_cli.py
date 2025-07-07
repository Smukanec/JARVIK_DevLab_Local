import pathlib
import sys
from types import SimpleNamespace

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

import devlab.cli as cli

class DummyEngine:
    def __init__(self, config_path=None):
        self.config_path = config_path
    def run(self, prompt, log=False):
        return "ok"

def test_cli_config(tmp_path, monkeypatch, capsys):
    cfg = tmp_path / "config.json"
    cfg.write_text("{}")

    engine = DummyEngine()
    def fake_engine(config_path=None):
        nonlocal engine
        engine.__init__(config_path)
        return engine

    monkeypatch.setattr(cli, "DevEngine", fake_engine)
    monkeypatch.setattr(sys, "argv", ["devlab-cli", "--config", str(cfg), "hello"])

    cli.main()

    assert engine.config_path == cfg
