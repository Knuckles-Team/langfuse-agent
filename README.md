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

*Version: 0.7.1*

## Overview

**Langfuse Agent MCP Server + A2A Agent**

Agent for interacting with Langfuse Observability API

This repository is actively maintained - Contributions are welcome!

## MCP

### Available MCP Tools

The MCP server provides 87 tools across 26 categories:

- **Annotation Queues**: List, create, get, update, delete queues and items
- **Blob Storage Integrations**: Get, upsert, check status, delete integrations
- **Comments**: Create, get comments
- **Dataset Items**: Create, list, get, delete dataset items
- **Dataset Run Items**: Create, list dataset run items
- **Datasets**: List, create, get, delete runs, get runs
- **Health**: Health check
- **Ingestion**: Batch ingestion
- **Legacy Metrics**: V1 metrics
- **Legacy Observations**: V1 get observations
- **Legacy Score**: V1 create/delete scores
- **LLM Connections**: List, upsert connections
- **Media**: Get, patch, get upload URL
- **Metrics**: Metrics query
- **Models**: Create, list, get, delete models
- **Observations**: Get many observations
- **OpenTelemetry**: Export traces
- **Organizations**: Manage organization and project memberships
- **Projects**: Get, create, update, delete projects and API keys
- **Prompts**: Version update, get, delete, list, create prompts
- **SCIM**: Service provider config, resource types, schemas, user management
- **Score Configs**: Create, get, update score configs
- **Scores**: Get many scores, get by ID
- **Sessions**: List, get sessions
- **Traces**: Get, delete, list, delete multiple traces


### Using as an MCP Server

The MCP Server can be run in two modes: `stdio` (for local testing) or `http` (for networked access).

#### Environment Variables

*   `LANGFUSE_URL`: The URL of the target service.
*   `LANGFUSE_TOKEN`: The API token or access token.

#### Run in stdio mode (default):
```bash
export LANGFUSE_URL="http://localhost:8080"
export LANGFUSE_TOKEN="your_token"
langfuse-mcp --transport "stdio"
```

#### Run in HTTP mode:
```bash
export LANGFUSE_URL="http://localhost:8080"
export LANGFUSE_TOKEN="your_token"
langfuse-mcp --transport "http" --host "0.0.0.0" --port "8000"
```

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
