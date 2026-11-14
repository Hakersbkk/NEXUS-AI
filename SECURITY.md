# Security Policy

## Reporting a vulnerability
Please do not publish exploitable security details in a public issue. Contact the repository maintainer privately through GitHub so the issue can be assessed and fixed.

## Secrets
- Never commit API keys, access tokens, passwords, or private configuration files.
- Use environment variables or a local secrets manager for provider credentials.
- Treat downloaded models, agent plugins, and external tools as untrusted until verified.

## Scope
This is an early-stage project. Security controls and supported deployment environments are still evolving. Do not use it to handle sensitive workloads until the relevant integrations have been reviewed.
