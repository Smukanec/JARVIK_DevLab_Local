import base64
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from devlab.github_connector import commit_file, open_pull_request


def test_commit_file(monkeypatch):
    captured = {}

    def fake_put(url, headers=None, json=None, timeout=None):
        captured['url'] = url
        captured['headers'] = headers
        captured['json'] = json
        captured['timeout'] = timeout

        class Resp:
            def raise_for_status(self):
                pass

            def json(self):
                return {'ok': True}

        return Resp()

    monkeypatch.setattr('devlab.github_connector.requests.put', fake_put, raising=False)

    result = commit_file('user/repo', 'file.txt', 'data', 'msg', 'TOK')

    encoded = base64.b64encode(b'data').decode()
    assert captured['url'] == 'https://api.github.com/repos/user/repo/contents/file.txt'
    assert captured['headers'] == {
        'Authorization': 'token TOK',
        'Accept': 'application/vnd.github+json',
    }
    assert captured['json'] == {'message': 'msg', 'content': encoded}
    assert captured['timeout'] == 30
    assert result == {'ok': True}


def test_open_pull_request(monkeypatch):
    captured = {}

    def fake_post(url, headers=None, json=None, timeout=None):
        captured['url'] = url
        captured['headers'] = headers
        captured['json'] = json
        captured['timeout'] = timeout

        class Resp:
            def raise_for_status(self):
                pass

            def json(self):
                return {'pr': 1}

        return Resp()

    monkeypatch.setattr('devlab.github_connector.requests.post', fake_post)

    result = open_pull_request('user/repo', 'head', 'main', 'title', 'body', 'TOK')

    assert captured['url'] == 'https://api.github.com/repos/user/repo/pulls'
    assert captured['headers'] == {
        'Authorization': 'token TOK',
        'Accept': 'application/vnd.github+json',
    }
    assert captured['json'] == {
        'title': 'title',
        'head': 'head',
        'base': 'main',
        'body': 'body',
    }
    assert captured['timeout'] == 30
    assert result == {'pr': 1}
