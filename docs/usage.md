# Usage — API / CLI / MCP

`langfuse-agent` exposes the same capability three ways: as **MCP tools** an agent
calls, as a **Python API** (`LangfuseApi`) you import, and as a **CLI**. The complete
tool surface and ecosystem role are in [Overview](overview.md).

## As an MCP server

Once [deployed](deployment.md), the server registers 87 tools across 26 categories.
Reads work with the platform connection and a valid API key pair. Each domain is
toggled with its `*_TOOL` environment switch.

| Group | Tools |
|---|---|
| Observability | `trace_list`, `trace_get`, `observations_get_many`, `scores_get_many`, `sessions_list`, `metrics_metrics` |
| Datasets | `datasets_list`, `datasets_get`, `dataset_items_list`, `dataset_run_items_list` |
| Prompts & Models | `prompts_list`, `prompts_get`, `models_list`, `models_get` |
| Management | `projects_get`, `organizations_get_organization_memberships`, `comments_get`, `health_health` |
| Annotation queues | `annotation_queues_list`, `annotation_queues_get` |
| OpenTelemetry | `opentelemetry_export_traces` |

Example agent prompts that map onto these tools:

- *"List the most recent traces for this project"* → `trace_list`
- *"Show the scores attached to trace `<id>`"* → `scores_get_many`
- *"What datasets are configured?"* → `datasets_list`

## As a Python API

`LangfuseApi` is a `requests`-based facade composed from the per-domain clients. It
authenticates with the project public/secret key pair.

```python
from langfuse_agent.api_client import LangfuseApi

api = LangfuseApi(
    public_key="pk-...",
    secret_key="sk-...",
    host="http://localhost:3000",
)

# Reads
health = api.health_health()                 # service health
traces = api.trace_list()                     # recent traces
datasets = api.datasets_list()                # configured datasets
sessions = api.sessions_list()                # session records
scores = api.scores_get_many()               # evaluation scores
```

Build a client straight from the environment:

```python
from langfuse_agent.auth import get_client
api = get_client()        # reads LANGFUSE_* from the environment / .env
```

## As a CLI

The package installs two console scripts:

```bash
# MCP server
langfuse-mcp --transport streamable-http --host 0.0.0.0 --port 8004

# A2A agent server (Pydantic-AI graph agent + web UI)
langfuse-agent --provider openai --model-id gpt-4o --api-key sk-...
```

Both read their configuration from the environment (or a sibling `.env`). Each
connector reads its own credentials and remains inactive when those credentials are
absent. The full environment surface is documented in
[`.env.example`](https://github.com/Knuckles-Team/langfuse-agent/blob/main/.env.example)
and on the [Deployment](deployment.md#configuration-environment) page.
