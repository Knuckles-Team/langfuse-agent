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
- **A current catalog of 5 action-routed and 81 one-to-one tools**
  (`langfuse-mcp` console script): traces, observations, scores, sessions, datasets,
  prompts, models, projects, organizations, SCIM, graph ingestion, and the
  OpenTelemetry export surface. The default intent mode discloses exact tools only
  when needed.
- **An A2A agent server** (`langfuse-agent` console script) that auto-discovers the
  MCP tools and routes requests through the agent-utilities graph engine.

The connector remains inactive when credential references are absent. GraphOS
resolves the references only when it launches the provider.

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

Install the package during provisioning, configure `AgentConfig`, and start the
already-installed GraphOS runtime:

```bash
python -m pip install "langfuse-agent[mcp]"
export LANGFUSE_HOST=https://langfuse.example.invalid
export LANGFUSE_PUBLIC_KEY_REF=env://LANGFUSE_PROJECT_PUBLIC_KEY
export LANGFUSE_SECRET_KEY_REF=env://LANGFUSE_PROJECT_SECRET_KEY
export LANGFUSE_TLS_PROFILE_REF=env://LANGFUSE_RUNTIME_TLS_PROFILE
graph-os
```

GraphOS registers the provider lazily and starts the installed
`langfuse_agent.mcp_server` module with its own interpreter. No package download
occurs at runtime. The TLS-profile reference is optional when system trust is
sufficient.

See **[Installation](installation.md)** and **[Deployment](deployment.md)** for the
full matrix (PyPI extras, Docker image, all transports, the agent server, reverse
proxy, DNS).
