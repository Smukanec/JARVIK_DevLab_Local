"""Utilities for interacting with GitHub via its API."""

from __future__ import annotations

import base64
from typing import Any, Dict

import requests

GITHUB_API = "https://api.github.com"


def commit_file(repo: str, path: str, content: str, message: str, token: str) -> Dict[str, Any]:
    """Create or update a file in the repository."""
    url = f"{GITHUB_API}/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    encoded = base64.b64encode(content.encode()).decode()
    data = {"message": message, "content": encoded}
    resp = requests.put(url, headers=headers, json=data, timeout=30)
    resp.raise_for_status()
    return resp.json()


def open_pull_request(repo: str, head: str, base: str, title: str, body: str, token: str) -> Dict[str, Any]:
    """Open a pull request on GitHub."""
    url = f"{GITHUB_API}/repos/{repo}/pulls"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    data = {"title": title, "head": head, "base": base, "body": body}
    resp = requests.post(url, headers=headers, json=data, timeout=30)
    resp.raise_for_status()
    return resp.json()
