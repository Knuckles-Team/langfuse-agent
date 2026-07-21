# langfuse-agent — Concept Overview

> **Category**: Observability | **Ecosystem Role**: MCP Server + A2A Agent
> Built on [`agent-utilities`](https://github.com/Knuckles-Team/agent-utilities) — the unified AGI Harness.

## Description

Agent for interacting with Langfuse Observability API

## Enterprise Readiness

All agents in the ecosystem inherit enterprise-grade infrastructure from `agent-utilities`:

| Feature | Status | Source |
|:--------|:-------|:-------|
| **JWT/OIDC Authentication** | ✅ Built-in | `agent-utilities[auth]` — Authlib JWKS + API key middleware |
| **OpenTelemetry Instrumentation** | ✅ Built-in | `agent-utilities[logfire]` — OTLP export, FastAPI auto-instrumentation |
| **HashiCorp Vault Integration** | ✅ Built-in | `agent-utilities[vault]` — `secret://`, `env://`, `vault://` URI schemes |
| **Audit Logging** | ✅ Built-in | Append-only compliance trail with 30+ action types (CONCEPT:AU-OS.governance.wasm-micro-agent-sandbox) |
| **Token Usage Analytics** | ✅ Built-in | 4-bucket tracking with budget alerting (CONCEPT:AU-OS.governance.wasm-micro-agent-sandbox) |
| **Prompt Injection Defense** | ✅ Built-in | 25+ pattern scanner + jailbreak taxonomy (CONCEPT:AU-OS.config.secrets-authentication) |
| **Guardrail Engine** | ✅ Built-in | Input/output interception with block/redact/warn (CONCEPT:AU-OS.governance.reactive-multi-axis-budget) |
| **Action Execution Pipeline** | ✅ Built-in | Token, cost, duration, and node transition limits Dry-run / commit / rollback phases (CONCEPT:AU-ORCH.adapter.kg-graph-materialization) |
| **Resource Scheduling** | ✅ Built-in | Priority queuing + preemption limits (CONCEPT:AU-OS.state.cognitive-scheduler-preemption) |
| **Session Concurrency** | ✅ Built-in | Enqueue/reject/interrupt/rollback (CONCEPT:AU-OS.governance.reactive-multi-axis-budget) |

## Concept Registry

This project implements or inherits the following ecosystem concepts:

| Concept ID | Description | Source |
|:-----------|:------------|:-------|
| ECO-4.1 | MCP & Universal Skills | `agent-utilities` (inherited) |
| OS-5.5 | **Token Usage Tracker** | `agent-utilities` (inherited) |
| OS-5.8 | **Telemetry & Observability** | `agent-utilities` (inherited) |

> 📖 **Full Registry**: See [`agent-utilities/docs/overview.md`](https://github.com/Knuckles-Team/agent-utilities/blob/main/docs/overview.md) for the complete 5-Pillar concept index.

## Architecture

This project follows the standardized agent-package pattern:

```
langfuse-agent/
├── langfuse_agent/          # Provider source
│   ├── api/                    # Per-domain REST clients
│   ├── agent_server.py         # Optional A2A agent entry point
│   ├── kg_ingest.py            # Governed graph materialization
│   ├── runtime_posture.py      # Native-provider readiness proof
│   ├── trace_projection.py     # Privacy-safe trace projection
│   ├── mcp_server.py           # FastMCP provider entry point
│   └── skills/                 # Consolidated operations workflow
├── tests/                   # Test suite
├── docs/                    # Documentation
├── docker/Dockerfile        # Agent and MCP image targets
├── pyproject.toml           # Package metadata
├── mcp_config.json          # MCP server configuration
└── main_agent.json          # Agent identity and system prompt
```

## Native GraphOS configuration

GraphOS registers the installed provider lazily from `AgentConfig`. Configure
only the canonical service URL and runtime secret references on the parent:

```json
{
  "mcpServers": {
    "graph-os": {
      "command": "graph-os",
      "env": {
        "LANGFUSE_HOST": "https://langfuse.example.invalid",
        "LANGFUSE_PUBLIC_KEY_REF": "env://LANGFUSE_PROJECT_PUBLIC_KEY",
        "LANGFUSE_SECRET_KEY_REF": "env://LANGFUSE_PROJECT_SECRET_KEY"
      }
    }
  }
}
```

The `env://` values are neutral schema examples; runtime configuration may use
any supported reference provider. The parent resolves the references and starts the installed
`langfuse_agent.mcp_server` module with its current interpreter. Startup does
not invoke a package manager. For a direct, supervisor-managed HTTP child:

```bash
python -m langfuse_agent.mcp_server \
  --transport streamable-http --host 127.0.0.1 --port 8001
```

See [Deployment](deployment.md) for the secret-materialization and TLS trust
boundaries.
