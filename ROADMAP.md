# NEXUS AI Roadmap

NEXUS AI aims to make local and cloud AI tools easier to carry and use across computers.

## MVP — in progress
- [x] Standard-library Python CLI
- [x] Detect common Ollama and OpenAI-compatible local endpoints
- [x] First lightweight Tkinter desktop launcher
- [ ] User-editable engine configuration

## Next
- [x] Initial Ollama model inventory and basic pull/delete controls
- [x] Basic GGUF launch/stop controls using an existing llama-server binary
- [ ] Adapter interface for coding agents
- [ ] Guided setup for llama.cpp and Ollama
- [ ] Optional cloud-provider configuration (API keys stored locally and never committed)
- [x] Initial desktop dashboard, endpoint status, model list, and add-LLM form

## Later
- [ ] Portable runtime profiles for Linux, Windows, and macOS
- [ ] Agent lifecycle controls and logs
- [ ] Import/export configuration
- [ ] Automated tests and release packages

Compatibility will be added through tested adapters. Not every agent, model, operating system, or low-memory device can be assumed to work without its required runtime, credentials, hardware, or network access.
