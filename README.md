# NEXUS AI

**One USB. Any AI. Any Agent. Anywhere.**

NEXUS AI is an open-source project exploring a lightweight, portable way to manage local AI engines, cloud AI endpoints, and coding-agent integrations from one place.

> Early-stage project: the current release includes an endpoint-discovery CLI and a first lightweight desktop launcher. Full agent adapters and model lifecycle controls are still planned.

## Current MVP

- Python 3 CLI with no third-party Python dependencies.
- First desktop launcher built with Python Tkinter (no extra Python package required when Tkinter is installed).
- Checks common local endpoints for Ollama and OpenAI-compatible servers such as llama.cpp.
- Lists model IDs exposed by reachable endpoints.
- Lets users register their own local or remote LLM server through a custom models endpoint URL.
- Stores user configuration outside the repository.

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Hakersbkk/NEXUS-AI.git
```

### 2. Enter the project directory

```bash
cd NEXUS-AI
```

### 3. Run NEXUS AI (CLI)

```bash
python3 nexus.py
```

### 4. Open the desktop launcher

```bash
python3 launcher.py
```

On Ubuntu/Debian, if Tkinter is missing, install it with `sudo apt install python3-tk`. Check the installation with `python3 -m tkinter`.

### Available Commands

Check system status:

```bash
python3 nexus.py status
```

List available AI models:

```bash
python3 nexus.py models
```

Initialize configuration:

```bash
python3 nexus.py init
```

### Add Your Own LLM

NEXUS AI can connect to your own model server if it exposes a compatible models-list endpoint. This can be a local server (for example, LM Studio or llama.cpp) or a remote OpenAI-compatible provider.

Interactive setup:

```bash
python3 nexus.py add-endpoint
```

Or provide the name and full models endpoint directly:

```bash
python3 nexus.py add-endpoint "My LLM" "http://127.0.0.1:1234/v1/models"
```

Then check the connection and list the models:

```bash
python3 nexus.py status
python3 nexus.py models
```

Use the server's actual models endpoint URL (commonly `/v1/models` for OpenAI-compatible servers or `/api/tags` for Ollama). The model must already be running in its own engine; this command registers the endpoint and does not download or launch model files. Authenticated cloud endpoints/API keys are not yet supported by this MVP.

## Project direction

Planned integrations include llama.cpp, Ollama, cloud APIs, and coding agents such as OpenCode, Claude Code, OpenAI Codex, Pi, and Hermes Agent. Integrations will be delivered through adapters and only claimed as supported after testing.

Some tools require separate runtimes, installation, API credentials, or an internet connection. USB portability does not remove those requirements, and model performance depends on available hardware and memory.

See [ROADMAP](ROADMAP.md), [Architecture](docs/ARCHITECTURE.md), and [Security](SECURITY.md).

## Contributing

Issues and pull requests are welcome. Please describe your operating system, Python version, engine, and endpoint when reporting a problem.

## License

MIT — see [LICENSE](LICENSE).
