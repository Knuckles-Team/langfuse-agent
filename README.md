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

*Version: 0.1.2*

## Overview

**Langfuse Agent MCP Server + A2A Agent**

Agent for interacting with Langfuse Observability API

This repository is actively maintained - Contributions are welcome!

## MCP

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
