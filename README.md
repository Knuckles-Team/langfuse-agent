# Langfuse Agent
## API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/langfuse-agent)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/langfuse-agent)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/langfuse-agent)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/langfuse-agent)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/langfuse-agent)
![PyPI - License](https://img.shields.io/pypi/l/langfuse-agent)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/langfuse-agent)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/langfuse-agent)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/langfuse-agent)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/langfuse-agent)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/langfuse-agent)
![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/langfuse-agent)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/langfuse-agent)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/langfuse-agent)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/langfuse-agent)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/langfuse-agent)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/langfuse-agent)

*Version: 0.14.0*

---

## Overview

**Langfuse Agent** is a production-grade Agent and Model Context Protocol (MCP) server designed to interface directly with the Langfuse LLM Engineering and Observability platform. It enables agentic models to query, create, and manage observability traces, datasets, prompt templates, and system configurations.

---

## Key Features

- **Consolidated Action-Routed MCP Tools:** Minimizes token overhead and eliminates tool bloat in LLM contexts by grouping 80+ methods into 4 optimized, togglable tool modules.
- **Enterprise-Grade Security:** Comprehensive support for Eunomia policies, OIDC token delegation, and granular execution context tracking.
- **Integrated Graph Agent:** Built-in Pydantic AI agent supporting the Agent Control Protocol (ACP) and standard Web interfaces (AG-UI).
- **Native Telemetry & Tracing:** Out-of-the-box OpenTelemetry exports and native Langfuse tracing tracking every trace and span.

---

## CLI or API

This agent wraps the Langfuse API. You can interact with it programmatically or via its integrated execution entrypoints.

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](file:///home/apps/workspace/agent-packages/agents/langfuse-agent/docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools
| Tool Module | Toggle Env Var | Enabled by Default | Description & Nested Methods |
|-------------|----------------|--------------------|------------------------------|
| **Observability Tools** | `OBSERVABILITY_TOOL` | `True` | Trace, metrics, observations, and sessions tracking tools. Action-routed methods: `metrics`, `observations`, `scores`, `sessions`, `trace`, `opentelemetry`, `legacy_metrics_v1`, `legacy_observations_v1`, `legacy_score_v1`. |
| **Datasets Tools** | `DATASETS_TOOL` | `True` | Manage datasets, dataset items, runs, and annotation queues. Action-routed methods: `datasets`, `dataset_items`, `dataset_run_items`, `annotation_queues`. |
| **Prompts & Models Tools** | `PROMPTS_MODELS_TOOL` | `True` | Manage prompt versions, media attachments, and model registries. Action-routed methods: `prompts`, `prompt_version`, `models`, `llm_connections`, `media`. |
| **Management Tools** | `MANAGEMENT_TOOL` | `True` | Manage organizations, projects, API keys, SCIM provisioning, comments, and blob storage integrations. Action-routed methods: `projects`, `organizations`, `scim`, `comments`, `blob_storage_integrations`, `health`. |

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/mcp.md](file:///home/apps/workspace/agent-packages/agents/langfuse-agent/docs/mcp.md).

### MCP Configuration Examples

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

```json
{
  "mcpServers": {
    "langfuse-agent": {
      "command": "uvx",
      "args": [
        "--from",
        "langfuse-agent",
        "langfuse-mcp"
      ],
      "env": {
        "LANGFUSE_BASE_URL": "http://localhost:8080",
        "LANGFUSE_TOKEN": "your_token_here"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (Recommended for production deployments)
To run the server as a long-running Streamable-HTTP service:

```json
{
  "mcpServers": {
    "langfuse-agent": {
      "url": "http://localhost:8004/langfuse-agent/mcp"
    }
  }
}
```

Deploying the Streamable-HTTP server via Docker:

```bash
docker run -d \
  --name langfuse-agent-mcp \
  -p 8004:8004 \
  -e TRANSPORT=streamable-http \
  -e PORT=8004 \
  -e LANGFUSE_BASE_URL="http://your-langfuse-instance:8080" \
  -e LANGFUSE_TOKEN="your_token" \
  knucklessg1/langfuse-agent:latest
```

---

## Agent

This repository features a fully integrated Pydantic AI Graph Agent. It communicates over the **Agent Control Protocol (ACP)** and interacts seamlessly with the **Agent Web UI (AG-UI)** and Terminal interface.

### Running the Agent CLI
To start the interactive command-line agent:

```bash
# Set credentials
export LANGFUSE_BASE_URL="http://localhost:8080"
export LANGFUSE_TOKEN="your_token"

# Run the agent server
langfuse-agent --provider openai --model-id gpt-4o
```

### Docker Compose Orchestration
The following `docker/agent.compose.yml` configures the Agent, Web UI, and Terminal Interface together:

```yaml
version: '3.8'

services:
  langfuse-agent-mcp:
    image: knucklessg1/langfuse-agent:latest
    container_name: langfuse-agent-mcp
    hostname: langfuse-agent-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=8004
      - TRANSPORT=streamable-http
    ports:
      - "8004:8004"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8004/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  langfuse-agent-agent:
    image: knucklessg1/langfuse-agent:latest
    container_name: langfuse-agent-agent
    hostname: langfuse-agent-agent
    restart: always
    depends_on:
      - langfuse-agent-mcp
    env_file:
      - ../.env
    command: [ "langfuse-agent" ]
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=9004
      - MCP_URL=http://langfuse-agent-mcp:8004/mcp
      - PROVIDER=${PROVIDER:-openai}
      - MODEL_ID=${MODEL_ID:-gpt-4o}
      - ENABLE_WEB_UI=True
      - ENABLE_OTEL=True
    ports:
      - "9004:9004"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:9004/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/agent.md](file:///home/apps/workspace/agent-packages/agents/langfuse-agent/docs/agent.md).

---

## Security & Governance

Built directly upon the enterprise-ready [`agent-utilities`](https://github.com/Knuckles-Team/agent-utilities) core, standard security parameters are fully supported:

### Access Control & Policy Enforcement
- **Eunomia Policies:** Fine-grained, policy-driven tool authorization. Supports `none`, local `embedded` (`mcp_policies.json`), or centralized `remote` modes.
- **OIDC Token Delegation:** Compliant with RFC 8693 token exchange for flowing authenticating user credentials from Web UI / ACP → Agent → MCP.
- **Scoped Credentials:** Execution context runs restricted to the specific caller identity.

### Runtime Security Grid
| Feature | Functionality | Enablement |
|---------|---------------|------------|
| **Tool Guard** | Sensitivity inspection with human-in-the-loop validation | Enabled by default |
| **Prompt Injection Defense** | Input scanning, repetition monitoring, and recursive loop blocks | Enabled by default |
| **Context Safety Guard** | Stuck-loop detectors and contextual overflow preemptive alerts | Enabled by default |

---

## Installation

Install the Python package locally:

```bash
# Using uv (highly recommended)
uv pip install langfuse-agent[all]

# Using standard pip
python -m pip install langfuse-agent[all]
```

---

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)

---

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`
