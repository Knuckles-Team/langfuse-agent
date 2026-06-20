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

*Version: 0.33.0*

> **Documentation** — Installation, deployment, usage across the API, CLI, and MCP
> interfaces, and guidance for provisioning the Langfuse platform are maintained in
> the [official documentation](https://knuckles-team.github.io/langfuse-agent/).

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
Auto-generated — do not edit between the markers below.
<!-- MCP-TOOLS-TABLE:START -->

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `langfuse_datasets` | `LANGFUSE_DATASETSTOOL` | Perform langfuse_datasets operations. |
| `langfuse_management` | `LANGFUSE_MANAGEMENTTOOL` | Perform langfuse_management operations. |
| `langfuse_observability` | `LANGFUSE_OBSERVABILITYTOOL` | Perform langfuse_observability operations. |
| `langfuse_prompts_models` | `LANGFUSE_PROMPTS_MODELSTOOL` | Perform langfuse_prompts_models operations. |

_4 action-routed tools (default `MCP_TOOL_MODE=condensed`). Each is enabled unless its toggle is set false; set `MCP_TOOL_MODE=verbose` (or `both`) for the 1:1 per-operation surface. Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

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

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`langfuse-agent` can also run as a **local container** (Docker / Podman / `uv`) or be
consumed from a **remote deployment**. The
[Deployment guide](https://knuckles-team.github.io/langfuse-agent/deployment/) has full, copy-paste
`mcp_config.json` for all four transports — **stdio**, **streamable-http**,
**local container / uv**, and **remote URL**:

- **Local container / uv** — launch the server from `mcp_config.json` via `uvx`,
  `docker run`, or `podman run`, or point at a local streamable-http container by `url`.
- **Remote URL** — connect to a server deployed behind Caddy at
  `http://langfuse-mcp.arpa/mcp` using the `"url"` key.
<!-- END GENERATED: additional-deployment-options -->

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

## Documentation

The complete documentation is published as the
[official documentation site](https://knuckles-team.github.io/langfuse-agent/) and is
the recommended reference for installation, deployment, and day-to-day operation.

| Page | Contents |
|---|---|
| [Installation](https://knuckles-team.github.io/langfuse-agent/installation/) | pip, source, extras, prebuilt Docker image |
| [Deployment](https://knuckles-team.github.io/langfuse-agent/deployment/) | run the MCP and agent servers, Compose, Caddy + Technitium, env config |
| [Usage](https://knuckles-team.github.io/langfuse-agent/usage/) | the MCP tools, the `LangfuseApi` client, the CLI |
| [Backing Platform](https://knuckles-team.github.io/langfuse-agent/platform/) | deploy Langfuse with Docker |
| [Overview](https://knuckles-team.github.io/langfuse-agent/overview/) | the full tool surface and ecosystem role |
| [Concepts](https://knuckles-team.github.io/langfuse-agent/concepts/) | concept registry (`CONCEPT:LF-*`) |

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


<!-- BEGIN agent-os-genesis-deploy (generated; do not edit between markers) -->

## Deploy with `agent-os-genesis`

This package can be provisioned for you — skill-guided — by the **`agent-os-genesis`**
universal skill (its *single-package deploy mode*): it picks your install method, seeds
secrets to OpenBao/Vault (or `.env`), trusts your enterprise CA, registers the MCP
server, and verifies it — the same machinery that stands up the whole Agent OS, narrowed
to just this package. Ask your agent to **"deploy `langfuse-agent` with agent-os-genesis"**.

| Install mode | Command |
|------|---------|
| Bare-metal, prod (PyPI) | `uvx langfuse-mcp` · or `uv tool install langfuse-agent` |
| Bare-metal, dev (editable) | `uv pip install -e ".[all]"` · or `pip install -e ".[all]"` |
| Container, prod | deploy `knucklessg1/langfuse-agent:latest` via docker-compose / swarm / podman / podman-compose / kubernetes |
| Container, dev (editable) | deploy `docker/compose.dev.yml` (source-mounted at `/src`; edits live on restart) |

Secrets are read-existing + seeded via `vault_sync` — you are only prompted for what's missing.

<!-- END agent-os-genesis-deploy -->
