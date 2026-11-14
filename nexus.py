#!/usr/bin/env python3
"""NEXUS AI — lightweight portable manager for local and compatible AI APIs.

This first MVP uses only the Python standard library. It detects common local
AI endpoints; it does not install or launch third-party agents yet.
"""
from __future__ import annotations

import json
import os
import platform
import subprocess
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


def configured_endpoints():
    endpoints = load_config().get("endpoints", DEFAULT_ENDPOINTS)
    normalized = []
    for item in endpoints:
        if isinstance(item, dict) and item.get("name") and item.get("url"):
            normalized.append((item["name"], item["url"]))
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            normalized.append((str(item[0]), str(item[1])))
    return normalized


def status() -> None:
    print(f"\n{APP_NAME} — SYSTEM STATUS")
    for name, url in configured_endpoints():
        ok, detail = check_endpoint(name, url)
        print(f"[{'ONLINE' if ok else 'OFFLINE'}] {name}: {detail}")
    print(f"\nConfig: {config_path()}")


def models() -> None:
    print(f"\n{APP_NAME} — AVAILABLE MODELS")
    found = False
    for name, url in configured_endpoints():
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


def add_endpoint(name: str | None = None, url: str | None = None) -> None:
    """Register a custom model server that exposes a models-list endpoint."""
    if not name:
        name = input("Name for this LLM/server: ").strip()
    if not url:
        url = input("Models endpoint URL (for example http://127.0.0.1:1234/v1/models): ").strip()
    if not name or not url:
        print("Both a name and URL are required.")
        return
    if not url.startswith(("http://", "https://")):
        print("URL must start with http:// or https://")
        return

    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    config = load_config()
    endpoints = config.get("endpoints", DEFAULT_ENDPOINTS)
    if not isinstance(endpoints, list):
        endpoints = []
    normalized = []
    for item in endpoints:
        if isinstance(item, dict):
            normalized.append(item)
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            normalized.append({"name": str(item[0]), "url": str(item[1])})
    if any(item.get("url") == url for item in normalized):
        print(f"That endpoint is already configured: {url}")
        return
    normalized.append({"name": name, "url": url})
    config["endpoints"] = normalized
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    print(f"Added: {name} — {url}")
    print("Run 'python3 nexus.py status' and 'python3 nexus.py models' to check it.")



def ollama_request(path: str, payload: dict | None = None, timeout: float = 30.0):
    """Call the local Ollama HTTP API."""
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json", "User-Agent": "NEXUS-AI/0.1"}
    req = urllib.request.Request("http://127.0.0.1:11434" + path, data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read()
    return json.loads(raw.decode("utf-8")) if raw else {}


def ollama_list_models() -> list[dict]:
    data = ollama_request("/api/tags", timeout=5)
    return data.get("models", []) if isinstance(data, dict) else []


def ollama_pull_model(model_name: str, progress_callback=None) -> None:
    """Pull an Ollama model, reporting streamed progress when requested."""
    payload = json.dumps({"name": model_name, "stream": True}).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/pull", data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "NEXUS-AI/0.1"}
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        for raw_line in response:
            if not raw_line.strip():
                continue
            item = json.loads(raw_line.decode("utf-8"))
            if progress_callback:
                progress_callback(item)
            if item.get("error"):
                raise RuntimeError(item["error"])


def ollama_delete_model(model_name: str) -> None:
    ollama_request("/api/delete", {"name": model_name}, timeout=30)


def start_llama_server(binary: str, model_path: str, port: int = 8080,
                       context: int = 4096) -> subprocess.Popen:
    """Launch llama-server without a shell; return the child process handle."""
    executable = Path(binary).expanduser()
    model = Path(model_path).expanduser()
    if not executable.is_file():
        raise FileNotFoundError(f"llama-server executable not found: {executable}")
    if not model.is_file() or model.suffix.lower() != ".gguf":
        raise FileNotFoundError(f"Select an existing .gguf model file: {model}")
    if not 1 <= int(port) <= 65535:
        raise ValueError("Port must be between 1 and 65535.")
    if int(context) < 256:
        raise ValueError("Context size must be at least 256.")
    return subprocess.Popen(
        [str(executable), "-m", str(model), "--host", "127.0.0.1",
         "--port", str(int(port)), "-c", str(int(context))],
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL, shell=False
    )


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
    parser.add_argument("command", nargs="?", choices=["status", "models", "init", "add-endpoint"], default="status")
    parser.add_argument("name", nargs="?", help="Display name for a custom LLM endpoint")
    parser.add_argument("url", nargs="?", help="Full models endpoint URL")
    args = parser.parse_args()
    if args.command == "add-endpoint":
        add_endpoint(args.name, args.url)
    else:
        {"status": status, "models": models, "init": init_config}[args.command]()


if __name__ == "__main__":
    main()
