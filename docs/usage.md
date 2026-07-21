# Usage — API / CLI / MCP

`langfuse-agent` exposes the same capability three ways: as **MCP tools** an agent
calls, as a **Python API** (`LangfuseApi`) you import, and as a **CLI**. The complete
tool surface and ecosystem role are in [Overview](overview.md).

## As an MCP server

Once [deployed](deployment.md), the catalog contains 5 action-routed tools and 81
one-to-one API tools. The default `intent` surface keeps those exact tools out of
the initial model context and discloses them on demand. Reads work with the platform
connection and a valid API key pair; each domain is toggled with its `*_TOOL`
setting.

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

`LangfuseApi` is a Requests-based facade composed from the per-domain clients.
The constructor receives a materialized project key pair only inside the trusted
runtime boundary. Application configuration keeps the corresponding references
in `AgentConfig`.

```python
from langfuse_agent.auth import get_client

# Inside the provider child, after GraphOS has privately materialized its refs.
api = get_client()

# Reads
health = api.health_health()                 # service health
traces = api.trace_list()                     # recent traces
datasets = api.datasets_list()                # configured datasets
sessions = api.sessions_list()                # session records
scores = api.scores_get_many()               # evaluation scores
```

Do not place key values in Python source. GraphOS resolves
`LANGFUSE_PUBLIC_KEY_REF` and `LANGFUSE_SECRET_KEY_REF` in its parent process,
then starts the provider child with only the materialized values it needs.

## As a CLI

The package installs two console scripts:

```bash
# MCP server
langfuse-mcp --transport streamable-http --host 127.0.0.1 --port 8004

# A2A agent server (Pydantic-AI graph agent + web UI)
langfuse-agent --provider openai --model-id gpt-4o
```

Both receive runtime configuration from their process supervisor. The native
GraphOS path uses secret references and remains inactive when either credential
reference is absent. The full configuration surface is documented in
[`.env.example`](https://github.com/Knuckles-Team/langfuse-agent/blob/main/.env.example)
and on the [Deployment](deployment.md#canonical-configuration) page.
