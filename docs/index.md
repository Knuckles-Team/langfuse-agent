# langfuse-agent

Langfuse observability **MCP Server + A2A Agent** for the agent-utilities ecosystem
— typed, deterministic access to the Langfuse tracing, evaluation, prompt, and
dataset APIs.

!!! info "Official documentation"
    This site is the canonical reference for `langfuse-agent`, maintained alongside
    every release.

[![PyPI](https://img.shields.io/pypi/v/langfuse-agent)](https://pypi.org/project/langfuse-agent/)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
[![License](https://img.shields.io/pypi/l/langfuse-agent)](https://github.com/Knuckles-Team/langfuse-agent/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/source-GitHub-181717?logo=github)](https://github.com/Knuckles-Team/langfuse-agent)

## Overview

`langfuse-agent` wraps the [Langfuse](https://langfuse.com/) REST surface with typed,
deterministic MCP tools and a Pydantic-AI agent server. It provides:

- **`LangfuseApi`** — a `requests`-based REST facade over the Langfuse API, organized
  by domain (observability, datasets, prompts/models, management, annotation queues).
- **87 MCP tools** across 26 categories (`langfuse-mcp` console script): traces,
  observations, scores, sessions, datasets, prompts, models, projects, organizations,
  SCIM, and the OpenTelemetry export surface.
- **An A2A agent server** (`langfuse-agent` console script) that auto-discovers the
  MCP tools and routes requests through the agent-utilities graph engine.

The connector remains inactive when credentials are absent; reads require only a
Langfuse base URL and an API key pair.

## Explore the documentation

<div class="grid cards" markdown>

- :material-rocket-launch: **[Installation](installation.md)** — pip, source, extras, and the prebuilt Docker image.
- :material-server-network: **[Deployment](deployment.md)** — run the MCP and agent servers, Docker Compose, Caddy + Technitium.
- :material-console: **[Usage](usage.md)** — the MCP tools, the `LangfuseApi` client, and the CLI.
- :material-database-cog: **[Backing Platform](platform.md)** — deploy Langfuse with Docker.
- :material-information-outline: **[Overview](overview.md)** — the full tool surface and ecosystem role.
- :material-tag-multiple: **[Concepts](concepts.md)** — the `CONCEPT:LF-*` registry.

</div>

## Quick start

```bash
pip install langfuse-agent
langfuse-mcp                       # stdio MCP server (default transport)
```

Connect it to a Langfuse instance:

```bash
export LANGFUSE_BASE_URL=http://localhost:3000
export LANGFUSE_PUBLIC_KEY=pk-...
export LANGFUSE_SECRET_KEY=sk-...
langfuse-mcp --transport streamable-http --host 0.0.0.0 --port 8004
```

See **[Installation](installation.md)** and **[Deployment](deployment.md)** for the
full matrix (PyPI extras, Docker image, all transports, the agent server, reverse
proxy, DNS).
