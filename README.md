# Langfuse Agent - A2A | AG-UI | MCP

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

*Version: 0.11.0*

## Overview

**Langfuse Agent MCP Server + A2A Agent**

Agent for interacting with Langfuse Observability API

This repository is actively maintained - Contributions are welcome!

## MCP

### Available MCP Tools

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

| Tool Name | Description |
|-----------|-------------|
| `langfuse_annotation_queues` | Consolidated Action-Routed tool for annotation_queues. Methods: annotation_queues_list_queues, annotation_queues_create_queue, annotation_queues_get_queue, annotation_queues_list_queue_items, annotation_queues_create_queue_item, annotation_queues_get_queue_item, annotation_queues_update_queue_item, annotation_queues_delete_queue_item, annotation_queues_create_queue_assignment, annotation_queues_delete_queue_assignment |
| `langfuse_blob_storage_integrations` | Consolidated Action-Routed tool for blob_storage_integrations. Methods: blob_storage_integrations_get_blob_storage_integrations, blob_storage_integrations_upsert_blob_storage_integration, blob_storage_integrations_get_blob_storage_integration_status, blob_storage_integrations_delete_blob_storage_integration |
| `langfuse_comments` | Consolidated Action-Routed tool for comments. Methods: comments_create, comments_get, comments_get_by_id |
| `langfuse_dataset_items` | Consolidated Action-Routed tool for dataset_items. Methods: dataset_items_create, dataset_items_list, dataset_items_get, dataset_items_delete |
| `langfuse_dataset_run_items` | Consolidated Action-Routed tool for dataset_run_items. Methods: dataset_run_items_create, dataset_run_items_list |
| `langfuse_datasets` | Consolidated Action-Routed tool for datasets. Methods: datasets_list, datasets_create, datasets_get, datasets_get_run, datasets_delete_run, datasets_get_runs |
| `langfuse_health` | Consolidated Action-Routed tool for health. Methods: health_health |
| `langfuse_ingestion` | Consolidated Action-Routed tool for ingestion. Methods: ingestion_batch |
| `langfuse_legacy_metrics_v1` | Consolidated Action-Routed tool for legacy_metrics_v1. Methods: legacy_metrics_v1_metrics |
| `langfuse_legacy_observations_v1` | Consolidated Action-Routed tool for legacy_observations_v1. Methods: legacy_observations_v1_get, legacy_observations_v1_get_many |
| `langfuse_legacy_score_v1` | Consolidated Action-Routed tool for legacy_score_v1. Methods: legacy_score_v1_create, legacy_score_v1_delete |
| `langfuse_llm_connections` | Consolidated Action-Routed tool for llm_connections. Methods: llm_connections_list, llm_connections_upsert |
| `langfuse_media` | Consolidated Action-Routed tool for media. Methods: media_get, media_patch, media_get_upload_url |
| `langfuse_metrics` | Consolidated Action-Routed tool for metrics. Methods: metrics_metrics |
| `langfuse_models` | Consolidated Action-Routed tool for models. Methods: models_create, models_list, models_get, models_delete |
| `langfuse_observations` | Consolidated Action-Routed tool for observations. Methods: observations_get_many |
| `langfuse_opentelemetry` | Consolidated Action-Routed tool for opentelemetry. Methods: opentelemetry_export_traces |
| `langfuse_organizations` | Consolidated Action-Routed tool for organizations. Methods: organizations_get_organization_memberships, organizations_update_organization_membership, organizations_delete_organization_membership, organizations_get_project_memberships, organizations_update_project_membership, organizations_delete_project_membership, organizations_get_organization_projects, organizations_get_organization_api_keys |
| `langfuse_projects` | Consolidated Action-Routed tool for projects. Methods: projects_get, projects_create, projects_update, projects_delete, projects_get_api_keys, projects_create_api_key, projects_delete_api_key |
| `langfuse_prompt_version` | Consolidated Action-Routed tool for prompt_version. Methods: prompt_version_update |
| `langfuse_prompts` | Consolidated Action-Routed tool for prompts. Methods: prompts_get, prompts_delete, prompts_list, prompts_create |
| `langfuse_scim` | Consolidated Action-Routed tool for scim. Methods: scim_get_service_provider_config, scim_get_resource_types, scim_get_schemas, scim_list_users, scim_create_user, scim_get_user, scim_delete_user |
| `langfuse_score_configs` | Consolidated Action-Routed tool for score_configs. Methods: score_configs_create, score_configs_get, score_configs_get_by_id, score_configs_update |
| `langfuse_scores` | Consolidated Action-Routed tool for scores. Methods: scores_get_many, scores_get_by_id |
| `langfuse_sessions` | Consolidated Action-Routed tool for sessions. Methods: sessions_list, sessions_get |
| `langfuse_trace` | Consolidated Action-Routed tool for trace. Methods: trace_get, trace_delete, trace_list, trace_delete_multiple |

## A2A Agent

### Run A2A Server
```bash
export LANGFUSE_URL="http://localhost:8080"
export LANGFUSE_TOKEN="your_token"
langfuse-agent --provider openai --model-id gpt-4o --api-key sk-...
```

The A2A agent uses agent-utilities for:
- Auto-discovery of MCP tools from mcp_config.json
- Pydantic AI agent with graph-based routing
- Web UI support
- OpenTelemetry integration
- Custom skills support

## Docker

### Build

```bash
docker build -t langfuse-agent .
```

### Run MCP Server

```bash
docker run -d \
  --name langfuse-agent \
  -p 8000:8000 \
  -e TRANSPORT=http \
  -e LANGFUSE_URL="http://your-service:8080" \
  -e LANGFUSE_TOKEN="your_token" \
  knucklessg1/langfuse-agent:latest
```

### Deploy with Docker Compose

```yaml
services:
  langfuse-agent:
    image: knucklessg1/langfuse-agent:latest
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=http
      - LANGFUSE_URL=http://your-service:8080
      - LANGFUSE_TOKEN=your_token
    ports:
      - 8000:8000
```

#### Configure `mcp.json` for AI Integration (e.g. Claude Desktop)

```json
{
  "mcpServers": {
    "langfuse": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "langfuse-agent",
        "langfuse-mcp"
      ],
      "env": {
        "LANGFUSE_URL": "http://your-service:8080",
        "LANGFUSE_TOKEN": "your_token"
      }
    }
  }
}
```

## Install Python Package

```bash
python -m pip install langfuse-agent
```
```bash
uv pip install langfuse-agent
```

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)


## MCP Configuration Examples

### 1. Standard IO (stdio) Deployment

```json
{
  "mcpServers": {
    "langfuse-agent": {
      "command": "uv",
      "args": [
        "run",
        "langfuse-mcp"
      ],
      "env": {
        "AGENT_DESCRIPTION": "<YOUR_AGENT_DESCRIPTION>",
        "AGENT_SYSTEM_PROMPT": "<YOUR_AGENT_SYSTEM_PROMPT>",
        "ANNOTATION_QUEUES_TOOL": "True",
        "BLOB_STORAGE_INTEGRATIONS_TOOL": "True",
        "COMMENTS_TOOL": "True",
        "DATASETS_TOOL": "True",
        "DATASET_ITEMS_TOOL": "True",
        "DATASET_RUN_ITEMS_TOOL": "True",
        "DEFAULT_AGENT_NAME": "<YOUR_DEFAULT_AGENT_NAME>",
        "HEALTH_TOOL": "True",
        "INGESTION_TOOL": "True",
        "LANGFUSE_HOST": "<YOUR_LANGFUSE_HOST>",
        "LANGFUSE_PUBLIC_KEY": "<YOUR_LANGFUSE_PUBLIC_KEY>",
        "LANGFUSE_SECRET_KEY": "<YOUR_LANGFUSE_SECRET_KEY>",
        "LEGACY_METRICS_V1_TOOL": "True",
        "LEGACY_OBSERVATIONS_V1_TOOL": "True",
        "LEGACY_SCORE_V1_TOOL": "True",
        "LLM_CONNECTIONS_TOOL": "True",
        "MEDIA_TOOL": "True",
        "METRICS_TOOL": "True",
        "MODELS_TOOL": "True",
        "OBSERVATIONS_TOOL": "True",
        "OPENTELEMETRY_TOOL": "True",
        "ORGANIZATIONS_TOOL": "True",
        "PROJECTS_TOOL": "True",
        "PROMPTS_TOOL": "True",
        "PROMPT_VERSION_TOOL": "True",
        "SCIM_TOOL": "True",
        "SCORES_TOOL": "True",
        "SCORE_CONFIGS_TOOL": "True",
        "SESSIONS_TOOL": "True",
        "TRACE_TOOL": "True"
      }
    }
  }
}
```

### 2. Streamable HTTP (SSE) Deployment

```json
{
  "mcpServers": {
    "langfuse-agent": {
      "command": "uv",
      "args": [
        "run",
        "langfuse-mcp",
        "--transport",
        "http",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
      ],
      "env": {
        "AGENT_DESCRIPTION": "<YOUR_AGENT_DESCRIPTION>",
        "AGENT_SYSTEM_PROMPT": "<YOUR_AGENT_SYSTEM_PROMPT>",
        "ANNOTATION_QUEUES_TOOL": "True",
        "BLOB_STORAGE_INTEGRATIONS_TOOL": "True",
        "COMMENTS_TOOL": "True",
        "DATASETS_TOOL": "True",
        "DATASET_ITEMS_TOOL": "True",
        "DATASET_RUN_ITEMS_TOOL": "True",
        "DEFAULT_AGENT_NAME": "<YOUR_DEFAULT_AGENT_NAME>",
        "HEALTH_TOOL": "True",
        "INGESTION_TOOL": "True",
        "LANGFUSE_HOST": "<YOUR_LANGFUSE_HOST>",
        "LANGFUSE_PUBLIC_KEY": "<YOUR_LANGFUSE_PUBLIC_KEY>",
        "LANGFUSE_SECRET_KEY": "<YOUR_LANGFUSE_SECRET_KEY>",
        "LEGACY_METRICS_V1_TOOL": "True",
        "LEGACY_OBSERVATIONS_V1_TOOL": "True",
        "LEGACY_SCORE_V1_TOOL": "True",
        "LLM_CONNECTIONS_TOOL": "True",
        "MEDIA_TOOL": "True",
        "METRICS_TOOL": "True",
        "MODELS_TOOL": "True",
        "OBSERVATIONS_TOOL": "True",
        "OPENTELEMETRY_TOOL": "True",
        "ORGANIZATIONS_TOOL": "True",
        "PROJECTS_TOOL": "True",
        "PROMPTS_TOOL": "True",
        "PROMPT_VERSION_TOOL": "True",
        "SCIM_TOOL": "True",
        "SCORES_TOOL": "True",
        "SCORE_CONFIGS_TOOL": "True",
        "SESSIONS_TOOL": "True",
        "TRACE_TOOL": "True"
      }
    }
  }
}
```
