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

*Version: 0.22.0*

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

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools
| Tool Module | Toggle Env Var | Enabled by Default | Description & Nested Methods |
|-------------|----------------|--------------------|------------------------------|
| **Langfuse Observability** | `LANGFUSE_OBSERVABILITY_TOOL` | `True` | Perform langfuse_observability operations. Action-routed methods: `ingestion_batch`, `legacy_metrics_v1_metrics`, `legacy_observations_v1_get`, `legacy_observations_v1_get_many`, `legacy_score_v1_create`, `legacy_score_v1_delete`, `metrics_metrics`, `observations_get_many`, `opentelemetry_export_traces`, `score_configs_create`, `score_configs_get`, `score_configs_get_by_id`, `score_configs_update`, `scores_get_by_id`, `scores_get_many`, `sessions_get`, `sessions_list`, `trace_delete`, `trace_delete_multiple`, `trace_get`, `trace_list`. |
| **Langfuse Datasets** | `LANGFUSE_DATASETS_TOOL` | `True` | Perform langfuse_datasets operations. Action-routed methods: `annotation_queues_create_queue`, `annotation_queues_create_queue_assignment`, `annotation_queues_create_queue_item`, `annotation_queues_delete_queue_assignment`, `annotation_queues_delete_queue_item`, `annotation_queues_get_queue`, `annotation_queues_get_queue_item`, `annotation_queues_list_queue_items`, `annotation_queues_list_queues`, `annotation_queues_update_queue_item`, `dataset_items_create`, `dataset_items_delete`, `dataset_items_get`, `dataset_items_list`, `dataset_run_items_create`, `dataset_run_items_list`, `datasets_create`, `datasets_delete_run`, `datasets_get`, `datasets_get_run`, `datasets_get_runs`, `datasets_list`. |
| **Langfuse Prompts Models** | `LANGFUSE_PROMPTS_MODELS_TOOL` | `True` | Perform langfuse_prompts_models operations. Action-routed methods: `llm_connections_list`, `llm_connections_upsert`, `media_get`, `media_get_upload_url`, `media_patch`, `models_create`, `models_delete`, `models_get`, `models_list`, `prompt_version_update`, `prompts_create`, `prompts_delete`, `prompts_get`, `prompts_list`. |
| **Langfuse Management** | `LANGFUSE_MANAGEMENT_TOOL` | `True` | Perform langfuse_management operations. Action-routed methods: `blob_storage_integrations_delete_blob_storage_integration`, `blob_storage_integrations_get_blob_storage_integration_status`, `blob_storage_integrations_get_blob_storage_integrations`, `blob_storage_integrations_upsert_blob_storage_integration`, `comments_create`, `comments_get`, `comments_get_by_id`, `health_health`, `organizations_delete_organization_membership`, `organizations_delete_project_membership`, `organizations_get_organization_api_keys`, `organizations_get_organization_memberships`, `organizations_get_organization_projects`, `organizations_get_project_memberships`, `organizations_update_organization_membership`, `organizations_update_project_membership`, `projects_create`, `projects_create_api_key`, `projects_delete`, `projects_delete_api_key`, `projects_get`, `projects_get_api_keys`, `projects_update`, `scim_create_user`, `scim_delete_user`, `scim_get_resource_types`, `scim_get_schemas`, `scim_get_service_provider_config`, `scim_get_user`, `scim_list_users`. |

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/mcp.md](docs/mcp.md).

### Dynamic Tool Selection & Visibility

This MCP server supports dynamic toolset selection and visibility filtering at runtime. This allows you to restrict the set of exposed tools in order to prevent blowing up the LLM's context window.

You can configure tool filtering via multiple input channels:

- **CLI Arguments:** Pass `--tools` or `--toolsets` (or their disabled counterparts `--disabled-tools` and `--disabled-toolsets`) during startup.
- **Environment Variables:** Define standard environment variables:
  - `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS`
  - `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS`
- **HTTP SSE Request Headers:** Pass custom headers during transport initialization:
  - `x-mcp-enabled-tools` / `x-mcp-disabled-tools`
  - `x-mcp-enabled-tags` / `x-mcp-disabled-tags`
- **HTTP SSE Request Query Parameters:** Append query parameters directly to your transport connection URL:
  - `?tools=tool1,tool2`
  - `?tags=tag1`

When query strings or parameters are supplied, an LLM-free **Knowledge Graph resolution layer** (using `DynamicToolOrchestrator`) matches query intents against known tool tags, names, or descriptions, with safe fallback and automated 24-hour background cache refreshing.

---

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

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/agent.md](docs/agent.md).

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

## Configuration & Environment Variables

The agent can be fully configured using environment variables or a `.env` file. Below is the list of all supported variables:

### Core API & Credentials
| Variable | Description | Default |
|----------|-------------|---------|
| `LANGFUSE_BASE_URL` | Langfuse instance base URL. | `https://cloud.langfuse.com` |
| `LANGFUSE_PUBLIC_KEY` | Langfuse public API key. | `""` |
| `LANGFUSE_SECRET_KEY` | Langfuse secret API key. | `""` |
| `LANGFUSE_TOKEN` | Consolidated authentication token. | `""` |

### Server Configuration
| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | The hostname/address the server binds to. | `0.0.0.0` |
| `PORT` | The port the server listens on. | `8004` |
| `TRANSPORT` | The communication protocol (`stdio`, `streamable-http`, `sse`). | `stdio` |
| `AUTH_TYPE` | Server authentication strategy (`key`, `delegated`, `none`). | `key` |

### Agent Customization
| Variable | Description | Default |
|----------|-------------|---------|
| `DEFAULT_AGENT_NAME` | Custom name displayed for the Pydantic AI Graph Agent. | `"Langfuse Agent"` |
| `AGENT_DESCRIPTION` | Short description of the agent's responsibilities. | `"AI agent for Langfuse Agent operations."` |
| `AGENT_SYSTEM_PROMPT` | Custom system instructions override for the agent. | `""` |

### Tool Toggle Switches
Individual tool modules can be enabled or disabled to minimize client context size:
- `OBSERVABILITY_TOOL` (Default: `True`): Toggles observation/tracing tools.
- `DATASETS_TOOL` (Default: `True`): Toggles datasets and annotation queue tools.
- `PROMPTS_MODELS_TOOL` (Default: `True`): Toggles prompt template and model connectivity tools.
- `MANAGEMENT_TOOL` (Default: `True`): Toggles comments, SCIM, and project management tools.

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
