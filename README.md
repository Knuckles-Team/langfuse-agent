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

*Version: 2.0.0*

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
- **Optional Telemetry & Tracing:** OTLP export and Langfuse instrumentation activate only when their runtime configuration is present.

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

#### Condensed action-routed tools (`MCP_TOOL_MODE=condensed` or `both`)

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `langfuse_datasets` | `LANGFUSE_DATASETSTOOL` | Perform langfuse_datasets operations. |
| `langfuse_ingest` | `LANGFUSE_KGTOOL` | Perform langfuse_ingest operations. |
| `langfuse_management` | `LANGFUSE_MANAGEMENTTOOL` | Perform langfuse_management operations. |
| `langfuse_observability` | `LANGFUSE_OBSERVABILITYTOOL` | Perform langfuse_observability operations. |
| `langfuse_prompts_models` | `LANGFUSE_PROMPTS_MODELSTOOL` | Perform langfuse_prompts_models operations. |

#### Verbose 1:1 API-mapped tools (`MCP_TOOL_MODE=verbose` or `both`)

<details>
<summary>81 per-operation tools — one per current public API method (click to expand)</summary>

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `langfuse_annotation_queues_create_queue` | `APITOOL` | Create an annotation queue |
| `langfuse_annotation_queues_create_queue_assignment` | `APITOOL` | Create an assignment for a user to an annotation queue |
| `langfuse_annotation_queues_create_queue_item` | `APITOOL` | Add an item to an annotation queue |
| `langfuse_annotation_queues_delete_queue_assignment` | `APITOOL` | Delete an assignment for a user to an annotation queue |
| `langfuse_annotation_queues_delete_queue_item` | `APITOOL` | Remove an item from an annotation queue |
| `langfuse_annotation_queues_get_queue` | `APITOOL` | Get an annotation queue by ID |
| `langfuse_annotation_queues_get_queue_item` | `APITOOL` | Get a specific item from an annotation queue |
| `langfuse_annotation_queues_list_queue_items` | `APITOOL` | Get items for a specific annotation queue |
| `langfuse_annotation_queues_list_queues` | `APITOOL` | Get all annotation queues |
| `langfuse_annotation_queues_update_queue_item` | `APITOOL` | Update an annotation queue item |
| `langfuse_blob_storage_integrations_delete_blob_storage_integration` | `APITOOL` | Delete a blob storage integration by ID (requires organization-scoped API key) |
| `langfuse_blob_storage_integrations_get_blob_storage_integration_status` | `APITOOL` | Get the sync status of a blob storage integration by integration ID (requires organization-scoped API key) |
| `langfuse_blob_storage_integrations_get_blob_storage_integrations` | `APITOOL` | Get all blob storage integrations for the organization (requires organization-scoped API key) |
| `langfuse_blob_storage_integrations_upsert_blob_storage_integration` | `APITOOL` | Create or update a blob storage integration for a specific project (requires organization-scoped API key). The configuration is validated by performing a test upload to the bucket. |
| `langfuse_comments_create` | `APITOOL` | Create a comment. Comments may be attached to different object types (trace, observation, session, prompt). |
| `langfuse_comments_get` | `APITOOL` | Get all comments |
| `langfuse_comments_get_by_id` | `APITOOL` | Get a comment by id |
| `langfuse_dataset_items_create` | `APITOOL` | Create a dataset item |
| `langfuse_dataset_items_delete` | `APITOOL` | Delete a dataset item and all its run items. This action is irreversible. |
| `langfuse_dataset_items_get` | `APITOOL` | Get a dataset item |
| `langfuse_dataset_items_list` | `APITOOL` | Get dataset items. Optionally specify a version to get the items as they existed at that point in time. Note: If version parameter is provided, datasetName must also be provided. |
| `langfuse_dataset_run_items_create` | `APITOOL` | Create a dataset run item |
| `langfuse_dataset_run_items_list` | `APITOOL` | List dataset run items |
| `langfuse_datasets_create` | `APITOOL` | Create a dataset |
| `langfuse_datasets_delete_run` | `APITOOL` | Delete a dataset run and all its run items. This action is irreversible. |
| `langfuse_datasets_get` | `APITOOL` | Get a dataset |
| `langfuse_datasets_get_run` | `APITOOL` | Get a dataset run and its items |
| `langfuse_datasets_get_runs` | `APITOOL` | Get dataset runs |
| `langfuse_datasets_list` | `APITOOL` | Get all datasets |
| `langfuse_health_health` | `APITOOL` | Check health of API and database |
| `langfuse_llm_connections_list` | `APITOOL` | Get all LLM connections in a project |
| `langfuse_llm_connections_upsert` | `APITOOL` | Create or update an LLM connection. The connection is upserted on provider. |
| `langfuse_media_get` | `APITOOL` | Get a media record |
| `langfuse_media_get_upload_url` | `APITOOL` | Get a presigned upload URL for a media record |
| `langfuse_media_patch` | `APITOOL` | Patch a media record |
| `langfuse_metrics_get` | `APITOOL` | Query aggregate observation or score metrics through Metrics API v2. |
| `langfuse_models_create` | `APITOOL` | Create a model |
| `langfuse_models_delete` | `APITOOL` | Delete a model. Cannot delete models managed by Langfuse. You can create your own definition with the same modelName to override the definition though. |
| `langfuse_models_get` | `APITOOL` | Get a model |
| `langfuse_models_list` | `APITOOL` | Get all models |
| `langfuse_observations_get_many` | `APITOOL` | Get a list of observations with cursor-based pagination and flexible field selection. ## Cursor-based Pagination This endpoint uses cursor-based pagination for efficient traversal of large datasets. The cursor is returned in the response… |
| `langfuse_opentelemetry_export_traces` | `APITOOL` | **OpenTelemetry Traces Ingestion Endpoint** This endpoint implements the OTLP/HTTP specification for trace ingestion, providing native OpenTelemetry integration for Langfuse Observability. **Supported Formats:** - Binary Protobuf: `Conte… |
| `langfuse_organizations_delete_organization_membership` | `APITOOL` | Delete a membership from the organization associated with the API key (requires organization-scoped API key) |
| `langfuse_organizations_delete_project_membership` | `APITOOL` | Delete a membership from a specific project (requires organization-scoped API key). The user must be a member of the organization. |
| `langfuse_organizations_get_organization_api_keys` | `APITOOL` | Get all API keys for the organization associated with the API key (requires organization-scoped API key) |
| `langfuse_organizations_get_organization_memberships` | `APITOOL` | Get all memberships for the organization associated with the API key (requires organization-scoped API key) |
| `langfuse_organizations_get_organization_projects` | `APITOOL` | Get all projects for the organization associated with the API key (requires organization-scoped API key) |
| `langfuse_organizations_get_project_memberships` | `APITOOL` | Get all memberships for a specific project (requires organization-scoped API key) |
| `langfuse_organizations_update_organization_membership` | `APITOOL` | Create or update a membership for the organization associated with the API key (requires organization-scoped API key) |
| `langfuse_organizations_update_project_membership` | `APITOOL` | Create or update a membership for a specific project (requires organization-scoped API key). The user must already be a member of the organization. |
| `langfuse_projects_create` | `APITOOL` | Create a new project (requires organization-scoped API key) |
| `langfuse_projects_create_api_key` | `APITOOL` | Create a new API key for a project (requires organization-scoped API key) |
| `langfuse_projects_delete` | `APITOOL` | Delete a project by ID (requires organization-scoped API key). Project deletion is processed asynchronously. |
| `langfuse_projects_delete_api_key` | `APITOOL` | Delete an API key for a project (requires organization-scoped API key) |
| `langfuse_projects_get` | `APITOOL` | Get Project associated with API key (requires project-scoped API key). You can use GET /api/public/organizations/projects to get all projects with an organization-scoped key. |
| `langfuse_projects_get_api_keys` | `APITOOL` | Get all API keys for a project (requires organization-scoped API key) |
| `langfuse_projects_update` | `APITOOL` | Update a project by ID (requires organization-scoped API key). |
| `langfuse_prompt_version_update` | `APITOOL` | Update labels for a specific prompt version |
| `langfuse_prompts_create` | `APITOOL` | Create a new version for the prompt with the given `name` |
| `langfuse_prompts_delete` | `APITOOL` | Delete prompt versions. If neither version nor label is specified, all versions of the prompt are deleted. |
| `langfuse_prompts_get` | `APITOOL` | Get a prompt |
| `langfuse_prompts_list` | `APITOOL` | Get a list of prompt names with versions and labels |
| `langfuse_scim_create_user` | `APITOOL` | Create a new user in the organization (requires organization-scoped API key) |
| `langfuse_scim_delete_user` | `APITOOL` | Remove a user from the organization (requires organization-scoped API key). Note that this only removes the user from the organization but does not delete the user entity itself. |
| `langfuse_scim_get_resource_types` | `APITOOL` | Get SCIM Resource Types (requires organization-scoped API key) |
| `langfuse_scim_get_schemas` | `APITOOL` | Get SCIM Schemas (requires organization-scoped API key) |
| `langfuse_scim_get_service_provider_config` | `APITOOL` | Get SCIM Service Provider Configuration (requires organization-scoped API key) |
| `langfuse_scim_get_user` | `APITOOL` | Get a specific user by ID (requires organization-scoped API key) |
| `langfuse_scim_list_users` | `APITOOL` | List users in the organization (requires organization-scoped API key) |
| `langfuse_score_configs_create` | `APITOOL` | Create a score configuration (config). Score configs are used to define the structure of scores |
| `langfuse_score_configs_get` | `APITOOL` | Get all score configs |
| `langfuse_score_configs_get_by_id` | `APITOOL` | Get a score config |
| `langfuse_score_configs_update` | `APITOOL` | Update a score config |
| `langfuse_scores_create` | `APITOOL` | Create a typed score through Langfuse's current score-write API. |
| `langfuse_scores_get_many` | `APITOOL` | Query scores through the cursor-based Scores API v3. |
| `langfuse_sessions_get` | `APITOOL` | Get a session. Please note that `traces` on this endpoint are not paginated, if you plan to fetch large sessions, consider `GET /api/public/traces?sessionId=<sessionId>` |
| `langfuse_sessions_list` | `APITOOL` | Get sessions |
| `langfuse_trace_delete` | `APITOOL` | Delete a specific trace |
| `langfuse_trace_delete_multiple` | `APITOOL` | Delete multiple traces |
| `langfuse_trace_get` | `APITOOL` | Get a specific trace |
| `langfuse_trace_list` | `APITOOL` | Get list of traces |

</details>

_5 action-routed tool(s) · 81 verbose 1:1 tool(s). `MCP_TOOL_MODE` selects the surface (`intent` default · `condensed` action-routed · `verbose` 1:1 · `both`). Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/usage.md](docs/usage.md).

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

<!-- MCP-CONFIG-EXAMPLES:START -->

> **Install the connector-focused `[mcp]` extra.** Examples use `langfuse-agent[mcp]` to add
> FastMCP / FastAPI through `agent-utilities[mcp]`; the required Agent Utilities core
> still carries `epistemic-graph[full]`. The `[agent-runtime]` extra additionally
> enables model orchestration.

#### stdio Transport (local IDEs — Cursor, Claude Desktop, VS Code)

```json
{
  "mcpServers": {
    "langfuse-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "langfuse-agent[mcp]",
        "langfuse-mcp"
      ],
      "env": {
        "MCP_TOOL_MODE": "intent",
        "LANGFUSE_DATASETSTOOL": "True",
        "LANGFUSE_KGTOOL": "True",
        "LANGFUSE_MANAGEMENTTOOL": "True",
        "LANGFUSE_OBSERVABILITYTOOL": "True",
        "LANGFUSE_PROMPTS_MODELSTOOL": "True"
      }
    }
  }
}
```

Runtime references require an alias-aware launcher such as GraphOS. Other
launchers must omit those entries and inject the resolved values through their
own runtime secret boundary.

#### Streamable-HTTP Transport (networked / production)

```json
{
  "mcpServers": {
    "langfuse-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "langfuse-agent[mcp]",
        "langfuse-mcp",
        "--transport",
        "streamable-http",
        "--port",
        "8000"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "127.0.0.1",
        "PORT": "8000",
        "MCP_TOOL_MODE": "intent",
        "LANGFUSE_DATASETSTOOL": "True",
        "LANGFUSE_KGTOOL": "True",
        "LANGFUSE_MANAGEMENTTOOL": "True",
        "LANGFUSE_OBSERVABILITYTOOL": "True",
        "LANGFUSE_PROMPTS_MODELSTOOL": "True"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed Streamable-HTTP instance by `url`:

```json
{
  "mcpServers": {
    "langfuse-mcp": {
      "url": "http://localhost:8000/langfuse-mcp/mcp"
    }
  }
}
```

Run a reviewed container image as a least-privilege stdio child (no
listener or published port):

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  -e MCP_TOOL_MODE=intent \
  -e LANGFUSE_DATASETSTOOL=True \
  -e LANGFUSE_KGTOOL=True \
  -e LANGFUSE_MANAGEMENTTOOL=True \
  -e LANGFUSE_OBSERVABILITYTOOL=True \
  -e LANGFUSE_PROMPTS_MODELSTOOL=True \
  registry.example.invalid/langfuse-agent@sha256:<digest> langfuse-mcp
```

For containerized network HTTP, supply an authenticated TLS ingress (or
direct server TLS), exact `MCP_ALLOWED_HOSTS`, and an exact trusted-proxy
CIDR policy through the operator-owned deployment profile. The generator
does not emit an unauthenticated non-loopback listener.

_Auto-generated from the code-read env surface (`MCP_TOOL_MODE` + package vars) — do not edit._
<!-- MCP-CONFIG-EXAMPLES:END -->

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`langfuse-agent` can run as a local stdio process or container, or behind a remote
network boundary. The
[Deployment guide](https://knuckles-team.github.io/langfuse-agent/deployment/) carries
the detailed transport contract.

- **Local container** — launch a reviewed immutable image as a least-privilege
  stdio child with no listener or published port.
- **Remote URL** — connect through an operator-supplied authenticated HTTPS
  ingress. Keep its URL, outbound identity references, trust profile, and exact
  `MCP_ALLOWED_HOSTS` in `AgentConfig`.
<!-- END GENERATED: additional-deployment-options -->

## Agent

This repository features a fully integrated Pydantic AI Graph Agent. It communicates over the **Agent Control Protocol (ACP)** and interacts seamlessly with the **Agent Web UI (AG-UI)** and Terminal interface.

### Running the Agent CLI
To start the interactive command-line agent, first let the process supervisor
inject the Langfuse credentials and any model-provider secret. Then run:

```bash
langfuse-agent --provider openai --model-id gpt-4o
```

### Docker Compose Orchestration
The checked-in `docker/agent.compose.yml` runs the MCP and agent services with
restricted containers and loopback-published ports. Supply pinned image digests
and let the process supervisor inject materialized child credentials at runtime;
never add them to the Compose file or a checked-in env file. GraphOS deployments
keep only the corresponding `*_REF` settings in `AgentConfig`.

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/deployment.md](docs/deployment.md).

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

GraphOS configuration uses `AgentConfig` and secret references. Do not store
credential values in `.env` files or MCP catalogs.

### Core API & Credentials
| Variable | Description | Default |
|----------|-------------|---------|
| `LANGFUSE_HOST` | Canonical Langfuse service URL. | `https://cloud.langfuse.com` |
| `LANGFUSE_PUBLIC_KEY_REF` | Runtime reference to the project public key. | *(unset)* |
| `LANGFUSE_SECRET_KEY_REF` | Runtime reference to the project secret key. | *(unset)* |
| `LANGFUSE_TLS_PROFILE_REF` | Runtime reference to a reusable TLS profile. | *(unset)* |
| `LANGFUSE_CA_BUNDLE_REF` | Runtime reference to a PEM trust store. | *(unset)* |
| `LANGFUSE_CLIENT_CERT_REF` | Runtime reference to an mTLS client certificate. | *(unset)* |
| `LANGFUSE_CLIENT_KEY_REF` | Runtime reference to the matching mTLS private key. | *(unset)* |
| `LANGFUSE_CLIENT_KEY_PASSWORD_REF` | Optional runtime reference for an encrypted client key. | *(unset)* |
| `LANGFUSE_PERSISTENCE_HMAC_KEY_REF` | Dedicated identity-HMAC key reference for graph persistence. | *(unset)* |

### Server Configuration
| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | The hostname/address the server binds to. | `127.0.0.1` |
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
Individual tool modules can be enabled or disabled to minimize client context size.
These names match the authoritative "Toggle Env Var" column in the
[Available MCP Tools](#available-mcp-tools) table above:
- `LANGFUSE_OBSERVABILITYTOOL` (Default: `True`): Toggles observation/tracing tools.
- `LANGFUSE_DATASETSTOOL` (Default: `True`): Toggles datasets and annotation queue tools.
- `LANGFUSE_PROMPTS_MODELSTOOL` (Default: `True`): Toggles prompt template and model connectivity tools.
- `LANGFUSE_MANAGEMENTTOOL` (Default: `True`): Toggles comments, SCIM, and project management tools.

---

## Installation

Pick the extra that matches what you want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `langfuse-agent[mcp]` | Connector-focused MCP server (`agent-utilities[mcp]` — FastMCP/FastAPI + `epistemic-graph[full]`) | You only run the **MCP server** (smallest install / image) |
| `langfuse-agent[agent]` | Agent runtime (`agent-utilities[agent-runtime,logfire]` — model orchestration + `epistemic-graph[full]`) | You run the **integrated agent** |
| `langfuse-agent[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# Connector-focused MCP server (includes the shared graph engine)
uv pip install "langfuse-agent[mcp]"

# Agent runtime (adds model orchestration to the shared graph engine)
uv pip install "langfuse-agent[agent]"

# Everything (development)
uv pip install "langfuse-agent[all]"      # or: python -m pip install "langfuse-agent[all]"
```

### Container image targets

One multi-stage `docker/Dockerfile` builds two published profiles and one exact,
offline release profile selected by `--target`:

| Build target | Contents | Entrypoint |
|--------------|----------|------------|
| `mcp` | `langfuse-agent[mcp]` — **connector-focused**, includes `epistemic-graph[full]`; no model-orchestration stack | `langfuse-mcp` |
| `mcp-local` | exact hash-locked wheelhouse for the same MCP profile; release assembly only | `langfuse-mcp` |
| `agent` (default) | `langfuse-agent[agent]` — **agent runtime**, model orchestration + `epistemic-graph[full]` | `langfuse-agent` |

```bash
docker build --target mcp   -t langfuse-agent:mcp docker/
docker build --target agent -t langfuse-agent:agent docker/
```

Promote and deploy only an operator-reviewed immutable image digest.

### Knowledge-graph database (`epistemic-graph`)

Both `[mcp]` and `[agent]` carry the **epistemic-graph** engine through the required
Agent Utilities core dependency (`epistemic-graph[full]`, including its folded numeric
kernel). The `[mcp]` extra keeps
the server connector-focused; `[agent]` additionally enables model orchestration. Local
deployments can use the bundled engine. For production or shared state, run
**epistemic-graph as a dedicated database service** and configure the runtime to use it.
Deployment recipes (single-node + Raft HA), connection configuration, and architecture
diagrams are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).

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

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=example&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/example)
![GitHub User's stars](https://img.shields.io/github/stars/example)

---

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`


<!-- BEGIN agent-utilities-deployment (generated; do not edit between markers) -->

## Deploy with `agent-utilities-deployment`

Provision this package with the consolidated **`agent-utilities-deployment`**
workflow. It selects an installed-package, editable-source, or immutable-container
path; records only runtime secret and TLS-profile references in `AgentConfig`; and
runs doctor, registration, policy, observability, and rollback gates. Ask your agent
to **"deploy `langfuse-agent` with agent-utilities-deployment"**.

| Install mode | Command |
|------|---------|
| Installed package | `uv tool install "langfuse-agent[mcp]"`, then run `langfuse-mcp` |
| Editable source | `uv pip install -e ".[agent]"`, then run `langfuse-mcp` |
| Immutable container | deploy `registry.example.invalid/langfuse-agent@sha256:<digest>` through the operator-selected orchestrator |

The repository embeds no deployment profile, credential value, certificate path, or
environment-specific endpoint. Supply those at runtime through `AgentConfig` and the
configured secret provider.

<!-- END agent-utilities-deployment -->

## Environment Variables

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `HOST` | `127.0.0.1` |  |
| `PORT` | `8004` |  |
| `TRANSPORT` | `stdio` | options: stdio, streamable-http, sse |
| `ENABLE_OTEL` | `False` |  |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `https://otel.example.invalid` |  |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY_REF` | — |  |
| `OTEL_EXPORTER_OTLP_SECRET_KEY_REF` | — |  |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |  |
| `EUNOMIA_TYPE` | `none` | options: none, embedded, remote |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` |  |
| `EUNOMIA_REMOTE_URL` | `http://eunomia-server:8000` |  |
| `LANGFUSE_BASE_URL` | `http://localhost:8080` | LANGFUSE_BASE_URL takes precedence when set; otherwise LANGFUSE_HOST is used. |
| `LANGFUSE_HOST` | — |  |
| `LANGFUSE_PUBLIC_KEY` | secret-injected |  |
| `LANGFUSE_SECRET_KEY` | secret-injected |  |
| `LANGFUSE_PUBLIC_KEY_REF` | — | Secret references (resolved at runtime) — alternatives to the plaintext keys above: |
| `LANGFUSE_SECRET_KEY_REF` | — |  |
| `LANGFUSE_TLS_PROFILE_REF` | — |  |
| `LANGFUSE_CA_BUNDLE_REF` | — |  |
| `LANGFUSE_CLIENT_CERT_REF` | — |  |
| `LANGFUSE_CLIENT_KEY_REF` | — |  |
| `LANGFUSE_CLIENT_KEY_PASSWORD_REF` | — |  |
| `LANGFUSE_PERSISTENCE_HMAC_KEY_REF` | — | Required only when LANGFUSE_KG_AUTO_INGEST=True. |
| `AUTH_TYPE` | `key` | options: key, delegated, none |
| `DEFAULT_AGENT_NAME` | `"Langfuse Agent"` |  |
| `AGENT_DESCRIPTION` | `"AI agent for Langfuse Agent operations."` |  |
| `AGENT_SYSTEM_PROMPT` | `""` |  |
| `MCP_TOOL_MODE` | `intent` | MCP_TOOL_MODE selects intent (default), condensed, verbose, or both surfaces. |
| `LANGFUSE_OBSERVABILITYTOOL` | `True` | These names match the authoritative "Toggle Env Var" column in the README MCP tools table (condensed action-routed surface). |
| `LANGFUSE_DATASETSTOOL` | `True` |  |
| `LANGFUSE_PROMPTS_MODELSTOOL` | `True` |  |
| `LANGFUSE_MANAGEMENTTOOL` | `True` |  |
| `LANGFUSE_KGTOOL` | `True` |  |

#### Inherited agent-utilities variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `MCP_CLIENT_AUTH` | — | Outbound MCP child auth: `oidc-client-credentials` \| `basic` \| `none` |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET_REF` | `secret://identity/oidc-client-secret` | Runtime secret reference for the OIDC service account |
| `MCP_BASIC_AUTH_USERNAME` | — | HTTP Basic username (`MCP_CLIENT_AUTH=basic`) |
| `MCP_BASIC_AUTH_PASSWORD_REF` | `secret://identity/mcp-basic-password` | Runtime secret reference for HTTP Basic auth (`MCP_CLIENT_AUTH=basic`) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `MODEL_ID` | `gpt-4o` | Model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_33 package + 15 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
<!-- ENV-VARS-TABLE:END -->

<!-- GOVERNED-CAPABILITY:START -->
## Governed capability contract

This package ships a compact canonical skill surface with specialist procedures
kept as referenced workflows. The current MCP tools, skill metadata,
`connector_manifest.yml`, ontology, mappings, shapes, fixtures, migrations,
tool-schema fingerprints, and certification metadata form one versioned
capability contract. Validate them together; do not rely on stale tool names or
historical per-task skill wrappers.

Runtime endpoints, credentials, certificate trust, tenant identity, retention,
and observability policy are deployment inputs and are never packaged values.
See [Configuration, trust, and privacy](docs/configuration.md) before enabling a
network transport, connector ingestion, GraphOS delegation, or trace export.
<!-- GOVERNED-CAPABILITY:END -->
