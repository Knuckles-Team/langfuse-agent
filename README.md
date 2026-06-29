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

*Version: 1.0.0*

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

#### Condensed action-routed tools (default — `MCP_TOOL_MODE=condensed`)

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `langfuse_datasets` | `LANGFUSE_DATASETSTOOL` | Perform langfuse_datasets operations. |
| `langfuse_management` | `LANGFUSE_MANAGEMENTTOOL` | Perform langfuse_management operations. |
| `langfuse_observability` | `LANGFUSE_OBSERVABILITYTOOL` | Perform langfuse_observability operations. |
| `langfuse_prompts_models` | `LANGFUSE_PROMPTS_MODELSTOOL` | Perform langfuse_prompts_models operations. |

#### Verbose 1:1 API-mapped tools (`MCP_TOOL_MODE=verbose` or `both`)

<details>
<summary>87 per-operation tools — one per public API method (click to expand)</summary>

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
| `langfuse_ingestion_batch` | `APITOOL` | **Legacy endpoint for batch ingestion for Langfuse Observability.**  -> Please use the OpenTelemetry endpoint (`/api/public/otel/v1/traces`). Learn more: https://langfuse.com/integrations/native/opentelemetry  Within each batch, there can be multiple events. Each event has a type, an id, a timestamp, metadata and a body. Internally, we refer to this as the "event envelope" as it tells us something about the event but not the trace. We use the event id within this envelope to deduplicate messages to avoid processing the same event twice, i.e. the event id should be unique per request. The event.body.id is the ID of the actual trace and will be used for updates and will be visible within the Langfuse App. I.e. if you want to update a trace, you'd use the same body id, but separate event IDs.  Notes: - Introduction to data model: https://langfuse.com/docs/observability/data-model - Batch sizes are limited to 3.5 MB in total. You need to adjust the number of events per batch accordingly. - The API does not return a 4xx status code for input errors. Instead, it responds with a 207 status code, which includes a list of the encountered errors. |
| `langfuse_legacy_metrics_v1_metrics` | `APITOOL` | Get metrics from the Langfuse project using a query object.  Consider using the [v2 metrics endpoint](/api-reference#tag/metricsv2/GET/api/public/v2/metrics) for better performance.  For more details, see the [Metrics API documentation](https://langfuse.com/docs/metrics/features/metrics-api). |
| `langfuse_legacy_observations_v1_get` | `APITOOL` | Get a observation |
| `langfuse_legacy_observations_v1_get_many` | `APITOOL` | Get a list of observations.  Consider using the [v2 observations endpoint](/api-reference#tag/observationsv2/GET/api/public/v2/observations) for cursor-based pagination and field selection. |
| `langfuse_legacy_score_v1_create` | `APITOOL` | Create a score (supports both trace and session scores) |
| `langfuse_legacy_score_v1_delete` | `APITOOL` | Delete a score (supports both trace and session scores) |
| `langfuse_llm_connections_list` | `APITOOL` | Get all LLM connections in a project |
| `langfuse_llm_connections_upsert` | `APITOOL` | Create or update an LLM connection. The connection is upserted on provider. |
| `langfuse_media_get` | `APITOOL` | Get a media record |
| `langfuse_media_get_upload_url` | `APITOOL` | Get a presigned upload URL for a media record |
| `langfuse_media_patch` | `APITOOL` | Patch a media record |
| `langfuse_metrics_metrics` | `APITOOL` | Get metrics from the Langfuse project using a query object. V2 endpoint with optimized performance.  ## V2 Differences - Supports `observations`, `scores-numeric`, and `scores-categorical` views only (traces view not supported) - Direct access to tags and release fields on observations - Backwards-compatible: traceName, traceRelease, traceVersion dimensions are still available on observations view - High cardinality dimensions are not supported and will return a 400 error (see below)  For more details, see the [Metrics API documentation](https://langfuse.com/docs/metrics/features/metrics-api).  ## Available Views  ### observations Query observation-level data (spans, generations, events).  **Dimensions:** - `environment` - Deployment environment (e.g., production, staging) - `type` - Type of observation (SPAN, GENERATION, EVENT) - `name` - Name of the observation - `level` - Logging level of the observation - `version` - Version of the observation - `tags` - User-defined tags - `release` - Release version - `traceName` - Name of the parent trace (backwards-compatible) - `traceRelease` - Release version of the parent trace (backwards-compatible, maps to release) - `traceVersion` - Version of the parent trace (backwards-compatible, maps to version) - `providedModelName` - Name of the model used - `promptName` - Name of the prompt used - `promptVersion` - Version of the prompt used - `startTimeMonth` - Month of start_time in YYYY-MM format  **Measures:** - `count` - Total number of observations - `latency` - Observation latency (milliseconds) - `streamingLatency` - Generation latency from completion start to end (milliseconds) - `inputTokens` - Sum of input tokens consumed - `outputTokens` - Sum of output tokens produced - `totalTokens` - Sum of all tokens consumed - `outputTokensPerSecond` - Output tokens per second - `tokensPerSecond` - Total tokens per second - `inputCost` - Input cost (USD) - `outputCost` - Output cost (USD) - `totalCost` - Total cost (USD) - `timeToFirstToken` - Time to first token (milliseconds) - `countScores` - Number of scores attached to the observation  ### scores-numeric Query numeric and boolean score data.  **Dimensions:** - `environment` - Deployment environment - `name` - Name of the score (e.g., accuracy, toxicity) - `source` - Origin of the score (API, ANNOTATION, EVAL) - `dataType` - Data type (NUMERIC, BOOLEAN) - `configId` - Identifier of the score config - `timestampMonth` - Month in YYYY-MM format - `timestampDay` - Day in YYYY-MM-DD format - `value` - Numeric value of the score - `traceName` - Name of the parent trace - `tags` - Tags - `traceRelease` - Release version - `traceVersion` - Version - `observationName` - Name of the associated observation - `observationModelName` - Model name of the associated observation - `observationPromptName` - Prompt name of the associated observation - `observationPromptVersion` - Prompt version of the associated observation  **Measures:** - `count` - Total number of scores - `value` - Score value (for aggregations)  ### scores-categorical Query categorical score data. Same dimensions as scores-numeric except uses `stringValue` instead of `value`.  **Measures:** - `count` - Total number of scores  ## High Cardinality Dimensions The following dimensions cannot be used as grouping dimensions in v2 metrics API as they can cause performance issues. Use them in filters instead.  **observations view:** - `id` - Use traceId filter to narrow down results - `traceId` - Use traceId filter instead - `userId` - Use userId filter instead - `sessionId` - Use sessionId filter instead - `parentObservationId` - Use parentObservationId filter instead  **scores-numeric / scores-categorical views:** - `id` - Use specific filters to narrow down results - `traceId` - Use traceId filter instead - `userId` - Use userId filter instead - `sessionId` - Use sessionId filter instead - `observationId` - Use observationId filter instead  ## Aggregations Available aggregation functions: `sum`, `avg`, `count`, `max`, `min`, `p50`, `p75`, `p90`, `p95`, `p99`, `histogram`  ## Time Granularities Available granularities for timeDimension: `auto`, `minute`, `hour`, `day`, `week`, `month` - `auto` bins the data into approximately 50 buckets based on the time range |
| `langfuse_models_create` | `APITOOL` | Create a model |
| `langfuse_models_delete` | `APITOOL` | Delete a model. Cannot delete models managed by Langfuse. You can create your own definition with the same modelName to override the definition though. |
| `langfuse_models_get` | `APITOOL` | Get a model |
| `langfuse_models_list` | `APITOOL` | Get all models |
| `langfuse_observations_get_many` | `APITOOL` | Get a list of observations with cursor-based pagination and flexible field selection.  ## Cursor-based Pagination This endpoint uses cursor-based pagination for efficient traversal of large datasets. The cursor is returned in the response metadata and should be passed in subsequent requests to retrieve the next page of results.  ## Field Selection Use the `fields` parameter to control which observation fields are returned: - `core` - Always included: id, traceId, startTime, endTime, projectId, parentObservationId, type - `basic` - name, level, statusMessage, version, environment, bookmarked, public, userId, sessionId - `time` - completionStartTime, createdAt, updatedAt - `io` - input, output - `metadata` - metadata (truncated to 200 chars by default, use `expandMetadata` to get full values) - `model` - providedModelName, internalModelId, modelParameters - `usage` - usageDetails, costDetails, totalCost - `prompt` - promptId, promptName, promptVersion - `metrics` - latency, timeToFirstToken  If not specified, `core` and `basic` field groups are returned.  ## Filters Multiple filtering options are available via query parameters or the structured `filter` parameter. When using the `filter` parameter, it takes precedence over individual query parameter filters. |
| `langfuse_opentelemetry_export_traces` | `APITOOL` | **OpenTelemetry Traces Ingestion Endpoint**  This endpoint implements the OTLP/HTTP specification for trace ingestion, providing native OpenTelemetry integration for Langfuse Observability.  **Supported Formats:** - Binary Protobuf: `Content-Type: application/x-protobuf` - JSON Protobuf: `Content-Type: application/json` - Supports gzip compression via `Content-Encoding: gzip` header  **Specification Compliance:** - Conforms to [OTLP/HTTP Trace Export](https://opentelemetry.io/docs/specs/otlp/#otlphttp) - Implements `ExportTraceServiceRequest` message format  **Documentation:** - Integration guide: https://langfuse.com/integrations/native/opentelemetry - Data model: https://langfuse.com/docs/observability/data-model |
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
| `langfuse_scores_get_by_id` | `APITOOL` | Get a score (supports both trace and session scores) |
| `langfuse_scores_get_many` | `APITOOL` | Get a list of scores (supports both trace and session scores) |
| `langfuse_sessions_get` | `APITOOL` | Get a session. Please note that `traces` on this endpoint are not paginated, if you plan to fetch large sessions, consider `GET /api/public/traces?sessionId=<sessionId>` |
| `langfuse_sessions_list` | `APITOOL` | Get sessions |
| `langfuse_trace_delete` | `APITOOL` | Delete a specific trace |
| `langfuse_trace_delete_multiple` | `APITOOL` | Delete multiple traces |
| `langfuse_trace_get` | `APITOOL` | Get a specific trace |
| `langfuse_trace_list` | `APITOOL` | Get list of traces |

</details>

_4 action-routed tool(s) (default) · 87 verbose 1:1 tool(s). Each is enabled unless its `<DOMAIN>TOOL` toggle is set false; `MCP_TOOL_MODE` selects the surface (`condensed` default · `verbose` 1:1 · `both`). Auto-generated — do not edit._
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

> **Install the slim `[mcp]` extra.** All examples below install
> `langfuse-agent[mcp]` — the MCP-server extra that pulls only the FastMCP /
> FastAPI tooling (`agent-utilities[mcp]`). It deliberately **excludes** the heavy
> agent runtime (the epistemic-graph engine, `pydantic-ai`, `dspy`, `llama-index`,
> `tree-sitter`), so `uvx`/container installs are dramatically smaller and faster.
> Use the full `[agent]` extra only when you need the integrated Pydantic AI agent
> (see [Installation](#installation)).

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

```json
{
  "mcpServers": {
    "langfuse-agent": {
      "command": "uvx",
      "args": [
        "--from",
        "langfuse-agent[mcp]",
        "langfuse-mcp"
      ],
      "env": {
        "LANGFUSE_BASE_URL": "http://localhost:8080",
        "LANGFUSE_PUBLIC_KEY": "pk-lf-...",
        "LANGFUSE_SECRET_KEY": "sk-lf-...",
        "MCP_TOOL_MODE": "condensed"
      }
    }
  }
}
```

> **Tool surface** — `MCP_TOOL_MODE` selects which tools are exposed:
> `condensed` (default, 4 action-routed tools), `verbose` (1:1 per-operation
> tools), or `both`. Set it in the `env` block above. See
> [Configuration & Environment Variables](#configuration--environment-variables).

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
  -e LANGFUSE_PUBLIC_KEY="pk-lf-..." \
  -e LANGFUSE_SECRET_KEY="sk-lf-..." \
  knucklessg1/langfuse-agent:mcp
```

> The `:mcp` tag is the **slim MCP-server image** (built from
> `docker/Dockerfile --target mcp`, installing `langfuse-agent[mcp]`). The default
> `:latest` tag is the **full agent image** (`--target agent`, `langfuse-agent[agent]`)
> which also bundles the Pydantic AI agent and the epistemic-graph engine — use it
> when you run `langfuse-agent` (the agent), not just the MCP server. See
> [Container images](#container-images-mcp-vs-agent).

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
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."

# Run the agent server
langfuse-agent --provider openai --model-id gpt-4o
```

### Docker Compose Orchestration
The following `docker/agent.compose.yml` configures the Agent, Web UI, and Terminal Interface together:

```yaml
version: '3.8'

services:
  langfuse-agent-mcp:
    image: knucklessg1/langfuse-agent:mcp
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
| `LANGFUSE_BASE_URL` | Langfuse instance base URL (legacy alias: `LANGFUSE_HOST`). | `https://cloud.langfuse.com` |
| `LANGFUSE_PUBLIC_KEY` | Langfuse public API key. | `""` |
| `LANGFUSE_SECRET_KEY` | Langfuse secret API key. | `""` |

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
| `langfuse-agent[mcp]` | Slim MCP server only (`agent-utilities[mcp]` — FastMCP/FastAPI) | You only run the **MCP server** (smallest install / image) |
| `langfuse-agent[agent]` | Full agent runtime (`agent-utilities[agent,logfire]` — Pydantic AI + the epistemic-graph engine) | You run the **integrated agent** |
| `langfuse-agent[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# MCP server only (recommended for tool hosting — slim deps)
uv pip install "langfuse-agent[mcp]"

# Full agent runtime (Pydantic AI + epistemic-graph engine)
uv pip install "langfuse-agent[agent]"

# Everything (development)
uv pip install "langfuse-agent[all]"      # or: python -m pip install "langfuse-agent[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `knucklessg1/langfuse-agent:mcp` | `--target mcp` | `langfuse-agent[mcp]` — **slim**, no engine/`pydantic-ai`/`dspy`/`llama-index`/`tree-sitter` | `langfuse-mcp` |
| `knucklessg1/langfuse-agent:latest` | `--target agent` (default) | `langfuse-agent[agent]` — **full** agent runtime + epistemic-graph engine | `langfuse-agent` |

```bash
docker build --target mcp   -t knucklessg1/langfuse-agent:mcp    docker/   # slim MCP server
docker build --target agent -t knucklessg1/langfuse-agent:latest docker/   # full agent
```

### Knowledge-graph database (`epistemic-graph`)

The **full agent** (`[agent]` / `:latest`) embeds the **epistemic-graph** engine (pulled in
transitively via `agent-utilities[agent]`). For production — or to share one knowledge graph
across multiple agents — run **epistemic-graph as its own database container** and point the
agent at it instead of embedding it. Deployment recipes (single-node + Raft HA), connection
config, and the full database architecture (with diagrams) are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).
The slim `[mcp]` server does **not** require the database.

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

## Environment Variables

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` |  |
| `PORT` | `8004` |  |
| `TRANSPORT` | `stdio` | options: stdio, streamable-http, sse |
| `ENABLE_OTEL` | `True` |  |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:8080/api/public/otel` |  |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` | `pk-...` |  |
| `OTEL_EXPORTER_OTLP_SECRET_KEY` | `sk-...` |  |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |  |
| `EUNOMIA_TYPE` | `none` | options: none, embedded, remote |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` |  |
| `EUNOMIA_REMOTE_URL` | `http://eunomia-server:8000` |  |
| `LANGFUSE_BASE_URL` | `http://localhost:8080` |  |
| `LANGFUSE_PUBLIC_KEY` | `your_public_key_here` |  |
| `LANGFUSE_SECRET_KEY` | `your_secret_key_here` |  |
| `AUTH_TYPE` | `key` | options: key, delegated, none |
| `DEFAULT_AGENT_NAME` | `"Langfuse Agent"` |  |
| `AGENT_DESCRIPTION` | `"AI agent for Langfuse Agent operations."` |  |
| `AGENT_SYSTEM_PROMPT` | `""` |  |
| `MCP_TOOL_MODE` | `condensed` | action-routed tools) | verbose (1:1 per-operation tools) | both. |
| `LANGFUSE_OBSERVABILITYTOOL` | `True` | MCP tools table (condensed action-routed surface). |
| `LANGFUSE_DATASETSTOOL` | `True` |  |
| `LANGFUSE_PROMPTS_MODELSTOOL` | `True` |  |
| `LANGFUSE_MANAGEMENTTOOL` | `True` |  |

#### Inherited agent-utilities variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `MCP_CLIENT_AUTH` | — | Outbound MCP auth (`oidc-client-credentials` for fleet calls) |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET` | — | OIDC client secret (service-account auth) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `MODEL_ID` | `gpt-4o` | Model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_23 package + 13 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
<!-- ENV-VARS-TABLE:END -->
