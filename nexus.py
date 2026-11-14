#!/usr/bin/env python3
"""NEXUS AI — lightweight portable manager for local and compatible AI APIs.

This first MVP uses only the Python standard library. It detects common local
AI endpoints; it does not install or launch third-party agents yet.
"""
from __future__ import annotations

import json
import os
import platform
import urllib.error
import urllib.request
from pathlib import Path

APP_NAME = "NEXUS AI"
DEFAULT_ENDPOINTS = [
    ("Ollama", "http://127.0.0.1:11434/api/tags"),
    ("llama.cpp / OpenAI-compatible", "http://127.0.0.1:8080/v1/models"),
    ("OpenAI-compatible (port 8081)", "http://127.0.0.1:8081/v1/models"),
]


def config_path() -> Path:
    system = platform.system()
    if system == "Windows":
        base = Path(os.environ.get("APPDATA", Path.home()))
        return base / "NEXUS-AI" / "config.json"
    if system == "Darwin":
        return Path.home() / "Library" / "Application Support" / "NEXUS-AI" / "config.json"
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "nexus-ai" / "config.json"


def load_config() -> dict:
    path = config_path()
    if not path.exists():
        return {"endpoints": DEFAULT_ENDPOINTS}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {"endpoints": DEFAULT_ENDPOINTS}
    except (OSError, json.JSONDecodeError):
        return {"endpoints": DEFAULT_ENDPOINTS}


def request_json(url: str, timeout: float = 1.5):
    req = urllib.request.Request(url, headers={"User-Agent": "NEXUS-AI/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def check_endpoint(name: str, url: str) -> tuple[bool, str]:
    try:
        data = request_json(url)
        if isinstance(data, dict):
            models = data.get("models") or data.get("data") or []
            count = len(models) if isinstance(models, list) else 0
            return True, f"online — {count} model(s) reported"
        return True, "online"
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        reason = getattr(exc, "reason", None) or str(exc)
        return False, str(reason)


def status() -> None:
    print(f"\n{APP_NAME} — SYSTEM STATUS")
    for name, url in load_config().get("endpoints", DEFAULT_ENDPOINTS):
        ok, detail = check_endpoint(name, url)
        print(f"[{'ONLINE' if ok else 'OFFLINE'}] {name}: {detail}")
    print(f"\nConfig: {config_path()}")


def models() -> None:
    print(f"\n{APP_NAME} — AVAILABLE MODELS")
    found = False
    for name, url in load_config().get("endpoints", DEFAULT_ENDPOINTS):
        try:
            data = request_json(url)
            entries = data.get("models") or data.get("data") or []
            for item in entries:
                model = item.get("name") or item.get("id") if isinstance(item, dict) else str(item)
                print(f"- {name}: {model}")
                found = True
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError):
            continue
    if not found:
        print("No reachable models found. Start a local engine or check its endpoint.")


def init_config() -> None:
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        print(f"Config already exists: {path}")
        return
    path.write_text(json.dumps({
        "endpoints": [{"name": n, "url": u} for n, u in DEFAULT_ENDPOINTS]
    }, indent=2) + "\n", encoding="utf-8")
    print(f"Created: {path}")


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Portable local AI endpoint checker")
    parser.add_argument("command", nargs="?", choices=["status", "models", "init"], default="status")
    args = parser.parse_args()
    {"status": status, "models": models, "init": init_config}[args.command]()


if __name__ == "__main__":
    main()
