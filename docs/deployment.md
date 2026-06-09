# Deployment

This page covers running `langfuse-agent` as a long-lived service: the transports, a
Docker Compose stack, the A2A agent server, putting it behind a Caddy reverse proxy,
and giving it a DNS name with Technitium. To provision the **Langfuse platform** it
connects to, see [Backing Platform](platform.md).

> `langfuse-agent` ships **two** console scripts: an **MCP server** (`langfuse-mcp`)
> that exposes the typed tool surface, and an **A2A agent server** (`langfuse-agent`)
> that wraps those tools in a Pydantic-AI graph agent. They can be deployed together
> or independently.

## Run the MCP server

The transport is selected with `--transport` (or the `TRANSPORT` env var):

=== "stdio (default)"

    ```bash
    langfuse-mcp
    ```
    For IDE / desktop MCP clients that launch the server as a subprocess.

=== "streamable-http"

    ```bash
    langfuse-mcp --transport streamable-http --host 0.0.0.0 --port 8004
    ```
    A network server with a `/health` endpoint and `/mcp` route.

=== "sse"

    ```bash
    langfuse-mcp --transport sse --host 0.0.0.0 --port 8004
    ```

Health check (HTTP transports):

```bash
curl -s http://localhost:8004/health        # {"status":"OK"}
```

## Configuration (environment)

`langfuse-agent` is configured entirely from the environment. The **required** set:

| Var | Default | Meaning |
|---|---|---|
| `LANGFUSE_BASE_URL` | `http://localhost:8080` | Langfuse instance URL |
| `LANGFUSE_PUBLIC_KEY` | *(unset)* | Project public key (`pk-...`) |
| `LANGFUSE_SECRET_KEY` | *(unset)* | Project secret key (`sk-...`) |
| `AUTH_TYPE` | `key` | Auth mode: `key`, `delegated`, `none` |
| `HOST` | `0.0.0.0` | Bind address (HTTP transports) |
| `PORT` | `8004` | Bind port (HTTP transports) |
| `TRANSPORT` | `stdio` | `stdio`, `streamable-http`, `sse` |

Per-domain tool registration is toggled with `OBSERVABILITY_TOOL`, `DATASETS_TOOL`,
`PROMPTS_MODELS_TOOL`, `MANAGEMENT_TOOL` and the finer-grained category switches
(`TRACE_TOOL`, `SCORES_TOOL`, `PROMPTS_TOOL`, …). The full set is documented in
[`.env.example`](https://github.com/Knuckles-Team/langfuse-agent/blob/main/.env.example).
Copy it to `.env` and populate only what you use.

## Docker Compose

The repo ships [`docker/mcp.compose.yml`](https://github.com/Knuckles-Team/langfuse-agent/blob/main/docker/mcp.compose.yml).
It reads a sibling `.env` and publishes the HTTP server on `:8004`:

```yaml
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
```

```bash
cp .env.example .env          # then edit LANGFUSE_* values
docker compose -f docker/mcp.compose.yml up -d
docker compose -f docker/mcp.compose.yml logs -f
```

## A2A agent server

The A2A agent server (`langfuse-agent` console script) wraps the MCP tool surface in
a Pydantic-AI graph agent with a web UI and OpenTelemetry tracing. It auto-discovers
tools from `mcp_config.json` and connects to the MCP server over `MCP_URL`. The repo
ships [`docker/agent.compose.yml`](https://github.com/Knuckles-Team/langfuse-agent/blob/main/docker/agent.compose.yml),
which deploys the MCP server on `:8004` and the agent server on `:9004`:

```bash
export LANGFUSE_BASE_URL=http://your-langfuse:3000
export LANGFUSE_PUBLIC_KEY=pk-...
export LANGFUSE_SECRET_KEY=sk-...
langfuse-agent --provider openai --model-id gpt-4o --api-key sk-...
```

```yaml
services:
  langfuse-agent-agent:
    image: knucklessg1/langfuse-agent:latest
    container_name: langfuse-agent-agent
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
    ports:
      - "9004:9004"
```

```bash
docker compose -f docker/agent.compose.yml up -d
```

## Behind a Caddy reverse proxy

Expose the HTTP server on a hostname with automatic TLS. Add to your `Caddyfile`:

```caddy
# Internal (self-signed) — homelab .arpa zone
langfuse-agent.arpa {
    tls internal
    reverse_proxy langfuse-agent-mcp:8004
}
```

```caddy
# Public — automatic Let's Encrypt
langfuse-agent.example.com {
    reverse_proxy langfuse-agent-mcp:8004
}
```

Reload Caddy:

```bash
docker compose -f services/caddy/compose.yml exec caddy caddy reload --config /etc/caddy/Caddyfile
```

## DNS with Technitium

Point the hostname at the host running Caddy. Via the Technitium API:

```bash
curl -s "http://technitium.arpa:5380/api/zones/records/add" \
  --data-urlencode "token=$TECHNITIUM_DNS_TOKEN" \
  --data-urlencode "domain=langfuse-agent.arpa" \
  --data-urlencode "zone=arpa" \
  --data-urlencode "type=A" \
  --data-urlencode "ipAddress=10.0.0.10" \
  --data-urlencode "ttl=3600"
```

…or add an **A record** `langfuse-agent.arpa → <caddy-host-ip>` in the Technitium web
console (`http://technitium.arpa:5380`). The ecosystem
[`technitium-dns-mcp`](https://knuckles-team.github.io/technitium-dns-mcp/) automates
this as a tool.

## Register with an MCP client

Add to your client's `mcp_config.json` (multiplexer nickname `lf`):

```json
{
  "mcpServers": {
    "langfuse-agent": {
      "command": "uv",
      "args": ["run", "langfuse-mcp"],
      "env": {
        "LANGFUSE_BASE_URL": "http://your-langfuse:3000",
        "LANGFUSE_PUBLIC_KEY": "pk-...",
        "LANGFUSE_SECRET_KEY": "sk-..."
      }
    }
  }
}
```

For a remote HTTP server, point the client at `http://langfuse-agent.arpa/mcp` instead.
