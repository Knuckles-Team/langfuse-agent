# CONN-LANGFUSE-AGENT-CONNECTOR-CONTENT — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Architecture

`pyproject.toml` declares `langfuse-mcp` as the connector identity. `create_mcp_server` resolves the packaged content of `langfuse_agent` from it.
