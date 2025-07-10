import pathlib
import sys
import types
import asyncio

# Provide minimal FastAPI stub if the real package is missing
if 'fastapi' not in sys.modules:
    fastapi = types.ModuleType('fastapi')
    class FastAPI:
        def __init__(self):
            self.routes = {}
        def mount(self, path, app, name=None):
            pass
        def get(self, path):
            def decorator(fn):
                self.routes[('GET', path)] = fn
                return fn
            return decorator
        def post(self, path):
            def decorator(fn):
                self.routes[('POST', path)] = fn
                return fn
            return decorator
    class FileResponse:
        def __init__(self, path, filename=None):
            self.path = pathlib.Path(path)
            self.filename = filename
    class StaticFiles:
        def __init__(self, directory):
            self.directory = directory
    class TestClient:
        def __init__(self, app):
            self.app = app
        def post(self, path, params=None):
            func = self.app.routes[('POST', path)]
            result = func(**(params or {}))
            if asyncio.iscoroutine(result):
                result = asyncio.get_event_loop().run_until_complete(result)
            return types.SimpleNamespace(status_code=200, json=lambda: result, text='')
        def get(self, path):
            func = self.app.routes[('GET', path)]
            result = func()
            if asyncio.iscoroutine(result):
                result = asyncio.get_event_loop().run_until_complete(result)
            text = result.path.read_text() if isinstance(result, FileResponse) else ''
            return types.SimpleNamespace(status_code=200, json=lambda: result, text=text)
    fastapi.FastAPI = FastAPI
    responses_mod = types.ModuleType('fastapi.responses')
    responses_mod.FileResponse = FileResponse
    static_mod = types.ModuleType('fastapi.staticfiles')
    static_mod.StaticFiles = StaticFiles
    testclient_mod = types.ModuleType('fastapi.testclient')
    testclient_mod.TestClient = TestClient

    fastapi.responses = responses_mod
    fastapi.staticfiles = static_mod
    fastapi.testclient = testclient_mod

    sys.modules['fastapi'] = fastapi
    sys.modules['fastapi.responses'] = responses_mod
    sys.modules['fastapi.staticfiles'] = static_mod
    sys.modules['fastapi.testclient'] = testclient_mod

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))

from fastapi.testclient import TestClient
import devlab.app as app_mod

class DummyEngine:
    def run(self, prompt: str) -> str:
        return 'ok'


def test_root_and_ask(monkeypatch):
    monkeypatch.setattr(app_mod, 'DevEngine', lambda *a, **kw: DummyEngine())
    client = TestClient(app_mod.app)

    resp = client.post('/ask', params={'prompt': 'hi'})
    assert resp.status_code == 200
    assert resp.json()['response'] == 'ok'

    resp = client.get('/')
    assert resp.status_code == 200
    assert '<!DOCTYPE html>' in resp.text

