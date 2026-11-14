# NEXUS AI

**One USB. Any AI. Any Agent. Anywhere.**

NEXUS AI is an open-source project exploring a lightweight, portable way to manage local AI engines, cloud AI endpoints, and coding-agent integrations from one place.

> Early-stage project: the current release is a small endpoint-discovery CLI. The unified launcher and agent adapters are planned, not yet implemented.

## Current MVP

- Python 3 CLI with no third-party Python dependencies.
- Checks common local endpoints for Ollama and OpenAI-compatible servers such as llama.cpp.
- Lists model IDs exposed by reachable endpoints.
- Stores user configuration outside the repository.

## Quick start

```bash
python3 nexus.py
python3 nexus.py status
python3 nexus.py models
python3 nexus.py init
```

The default checks are:
- Ollama: `http://127.0.0.1:11434/api/tags`
- OpenAI-compatible server: `http://127.0.0.1:8080/v1/models`
- OpenAI-compatible server: `http://127.0.0.1:8081/v1/models`

The initial configuration is created at:
- Linux: `~/.config/nexus-ai/config.json`
- macOS: `~/Library/Application Support/NEXUS-AI/config.json`
- Windows: `%APPDATA%\\NEXUS-AI\\config.json`

## Project direction

Planned integrations include llama.cpp, Ollama, cloud APIs, and coding agents such as OpenCode, Claude Code, OpenAI Codex, Pi, and Hermes Agent. Integrations will be delivered through adapters and only claimed as supported after testing.

Some tools require separate runtimes, installation, API credentials, or an internet connection. USB portability does not remove those requirements, and model performance depends on available hardware and memory.

See [ROADMAP](ROADMAP.md), [Architecture](docs/ARCHITECTURE.md), and [Security](SECURITY.md).

## Contributing

Issues and pull requests are welcome. Please describe your operating system, Python version, engine, and endpoint when reporting a problem.

## License

MIT — see [LICENSE](LICENSE).
