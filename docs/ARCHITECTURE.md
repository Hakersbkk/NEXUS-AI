# Architecture

## Design goals
- Lightweight core with minimal dependencies.
- Separate engine discovery from agent integrations.
- Prefer documented HTTP APIs and explicit adapters.
- Keep provider credentials out of the repository.
- Degrade gracefully when an optional engine is unavailable.

## Current MVP
`nexus.py` is a standard-library-only command-line utility. It probes configured HTTP endpoints and lists model identifiers returned by common Ollama and OpenAI-compatible APIs.

## Planned components
1. **Core** — configuration, logging, capability checks, and lifecycle coordination.
2. **Engine adapters** — Ollama, llama.cpp server, and compatible remote endpoints.
3. **Agent adapters** — integrations for agents that expose a supported CLI or API. Each adapter declares its runtime and credential requirements.
4. **User interface** — portable launcher first, optional desktop UI later.

## Portability
The project should keep user configuration outside the repository and avoid assuming that USB storage alone makes runtimes portable. OS-specific binaries, permissions, drivers, model memory requirements, and network access must be checked explicitly.
