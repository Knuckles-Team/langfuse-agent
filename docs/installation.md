# Installation

`langfuse-agent` is a standard Python package and a prebuilt container image. Pick the
path that matches how you want to run it.

## Requirements

- **Python 3.11 – 3.14**.
- A reachable **Langfuse** instance (self-hosted or Langfuse Cloud) — see
  [Backing Platform](platform.md) to deploy one locally.

## From PyPI (recommended)

```bash
pip install langfuse-agent
```

### Optional extras

The base install ships the MCP server runtime. Install the extra for what you need:

| Extra | Install | Pulls in |
|---|---|---|
| *(base)* | `pip install langfuse-agent` | FastMCP MCP-server runtime (`agent-utilities[mcp]`) + `langfuse` |
| `agent` | `pip install "langfuse-agent[agent]"` | Pydantic-AI agent server + Logfire tracing |
| `all` | `pip install "langfuse-agent[all]"` | The MCP server, the agent server, and tracing |
| `test` | `pip install "langfuse-agent[test]"` | `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-xdist` |

```bash
# Typical: run the MCP server and the A2A agent server
pip install "langfuse-agent[all]"
```

## From source

```bash
git clone https://github.com/Knuckles-Team/langfuse-agent.git
cd langfuse-agent
pip install -e ".[all]"          # editable install with every extra
```

With [`uv`](https://docs.astral.sh/uv/):

```bash
uv pip install -e ".[all]"
uv run langfuse-mcp
```

## Prebuilt Docker image

A multi-stage, slim image is published on every release (entrypoint `langfuse-mcp`):

```bash
docker pull knucklessg1/langfuse-agent:latest

docker run --rm -i \
  -e LANGFUSE_BASE_URL=http://your-langfuse:3000 \
  -e LANGFUSE_PUBLIC_KEY=pk-... \
  -e LANGFUSE_SECRET_KEY=sk-... \
  knucklessg1/langfuse-agent:latest        # stdio transport (default)
```

For an HTTP server with a published port and the agent server, see
[Deployment](deployment.md).

## Verify the install

```bash
langfuse-mcp --help
python -c "import langfuse_agent; print(langfuse_agent.__version__)"
```

## Next steps

- **[Deployment](deployment.md)** — run it as a long-lived MCP server and agent behind Caddy + DNS.
- **[Usage](usage.md)** — call the tools, the API, and the CLI.
- **[Configuration](deployment.md#configuration-environment)** — every environment variable.
