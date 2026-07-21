# Deployment

`langfuse-agent` exposes an MCP server (`langfuse-mcp`) and an optional A2A
agent server (`langfuse-agent`). GraphOS is the production launcher: it owns
`AgentConfig`, resolves secret references, and lazily mounts the installed
provider.

<!-- BEGIN GENERATED: deployment-options -->
## Deployment Options

`langfuse-agent` exposes its MCP server (console script `langfuse-mcp`) four ways. Pick the row that
matches where the server runs relative to your MCP client, then copy the matching
`mcp_config.json` below. Replace the `<your-…>` placeholders with the values from the **Configuration / Environment Variables** section.

| # | Option | Transport | Where it runs | `mcp_config.json` key |
|---|--------|-----------|---------------|------------------------|
| 1 | stdio | `stdio` | client launches a subprocess | `command` |
| 2 | Streamable-HTTP (local) | `streamable-http` | a local network port | `command` or `url` |
| 3 | Local container / uv | `stdio` or `streamable-http` | Docker / Podman / uv on this host | `command` or `url` |
| 4 | Remote URL | `streamable-http` | a remote host behind Caddy | `url` |

### 1. stdio (local subprocess)

The client launches the server over stdio via `uvx` — best for local IDEs
(Cursor, Claude Desktop, VS Code):

```json
{
  "mcpServers": {
    "langfuse-mcp": {
      "command": "uvx",
      "args": ["--from", "langfuse-agent", "langfuse-mcp"],
      "env": {
        "LANGFUSE_BASE_URL": "<your-langfuse_base_url>",
        "LANGFUSE_TOKEN": "<your-langfuse_token>",
        "LANGFUSE_PUBLIC_KEY": "<your-langfuse_public_key>"
      }
    }
  }
}
```

### 2. Streamable-HTTP (local process)

Run the server as a long-lived HTTP process:

```bash
uvx --from langfuse-agent langfuse-mcp --transport streamable-http --host 0.0.0.0 --port 8000
curl -s http://localhost:8000/health        # {"status":"OK"}
```

Then either let the client launch it:

```json
{
  "mcpServers": {
    "langfuse-mcp": {
      "command": "uvx",
      "args": ["--from", "langfuse-agent", "langfuse-mcp", "--transport", "streamable-http", "--port", "8000"],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "LANGFUSE_BASE_URL": "<your-langfuse_base_url>",
        "LANGFUSE_TOKEN": "<your-langfuse_token>",
        "LANGFUSE_PUBLIC_KEY": "<your-langfuse_public_key>"
      }
    }
  }
}
```

…or connect to the already-running process by URL:

```json
{
  "mcpServers": {
    "langfuse-mcp": { "url": "http://localhost:8000/mcp" }
  }
}
```

### 3. Local container / uv

**(a) Launch a container directly from `mcp_config.json`** (stdio over the container —
no ports to manage). Swap `docker` for `podman` for a daemonless runtime:

```json
{
  "mcpServers": {
    "langfuse-mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "TRANSPORT=stdio",
        "-e", "LANGFUSE_BASE_URL=<your-langfuse_base_url>",
        "-e", "LANGFUSE_TOKEN=<your-langfuse_token>",
        "-e", "LANGFUSE_PUBLIC_KEY=<your-langfuse_public_key>",
        "knucklessg1/langfuse-agent:latest"
      ]
    }
  }
}
```

**(b) Run a local streamable-http container, then connect by URL:**

```bash
docker run -d --name langfuse-mcp -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  -e LANGFUSE_BASE_URL="<your-langfuse_base_url>" \
  -e LANGFUSE_TOKEN="<your-langfuse_token>" \
  -e LANGFUSE_PUBLIC_KEY="<your-langfuse_public_key>" \
  knucklessg1/langfuse-agent:latest
# or, from a clone of this repo:
docker compose -f docker/mcp.compose.yml up -d
```

```json
{
  "mcpServers": {
    "langfuse-mcp": { "url": "http://localhost:8000/mcp" }
  }
}
```

**(c) From a local checkout with `uv`:**

```bash
uv run langfuse-mcp --transport streamable-http --port 8000
```

### 4. Remote URL (deployed behind Caddy)

When the server is deployed remotely (e.g. as a Docker service) and published through
Caddy on an internal DNS zone, connect with the `"url"` key — no local process or
image required:

```json
{
  "mcpServers": {
    "langfuse-mcp": { "url": "http://langfuse-mcp.example.invalid/mcp" }
  }
}
```

Caddy reverse-proxies `http://langfuse-mcp.example.invalid` to the container's `:8000`
streamable-http listener; `http://langfuse-mcp.example.invalid/health` returns
`{"status":"OK"}` when the service is live.
<!-- END GENERATED: deployment-options -->

This page covers running `langfuse-agent` as a long-lived service: the transports, a
Docker Compose stack, the A2A agent server, putting it behind a Caddy reverse proxy,
and giving it a DNS name with Technitium. To provision the **Langfuse platform** it
connects to, see [Backing Platform](platform.md).

## Native GraphOS deployment

Install the package during image or host provisioning. Configure the GraphOS
parent with references rather than credential values:

```json
{
  "mcpServers": {
    "graph-os": {
      "command": "graph-os",
      "env": {
        "LANGFUSE_HOST": "https://langfuse.example.invalid",
        "LANGFUSE_PUBLIC_KEY_REF": "env://LANGFUSE_PROJECT_PUBLIC_KEY",
        "LANGFUSE_SECRET_KEY_REF": "env://LANGFUSE_PROJECT_SECRET_KEY",
        "LANGFUSE_TLS_PROFILE_REF": "env://LANGFUSE_RUNTIME_TLS_PROFILE"
      }
    }
  }
}
```

These `env://` values are neutral schema examples, not a required namespace;
runtime configuration may instead supply any supported `vault://` or
`secret://` reference. `LANGFUSE_TLS_PROFILE_REF` is optional when system trust
is sufficient. Do not
add a separate Langfuse entry to the MCP catalog. When both credential
references are configured, GraphOS registers the provider lazily and starts:

```text
<current-python-interpreter> -m langfuse_agent.mcp_server
```

The interpreter and module are already installed. This launch path performs no
package download, package-index lookup, or PATH-based provider selection.

## Canonical configuration

The GraphOS parent accepts the following Langfuse settings through
`AgentConfig`:

| Setting | Default | Purpose |
|---|---|---|
| `LANGFUSE_HOST` | Langfuse Cloud | Canonical service URL |
| `LANGFUSE_PUBLIC_KEY_REF` | unset | Runtime reference to the project public key |
| `LANGFUSE_SECRET_KEY_REF` | unset | Runtime reference to the project secret key |
| `LANGFUSE_TLS_PROFILE_REF` | unset | Runtime reference to a reusable TLS profile |
| `LANGFUSE_CA_BUNDLE_REF` | unset | Runtime reference to a PEM trust store |
| `LANGFUSE_CLIENT_CERT_REF` | unset | Runtime reference to an mTLS client certificate |
| `LANGFUSE_CLIENT_KEY_REF` | unset | Runtime reference to its matching mTLS private key |
| `LANGFUSE_CLIENT_KEY_PASSWORD_REF` | unset | Optional runtime reference for an encrypted client key |
| `LANGFUSE_PERSISTENCE_HMAC_KEY_REF` | unset | Dedicated identity-HMAC key reference required for graph persistence |
| `LANGFUSE_KG_AUTO_INGEST` | `false` | Opt in to privacy-guarded graph persistence |
| `LANGFUSE_MCP_ENABLED` | automatic | Explicitly enable or disable native registration |

Secret references use `vault://`, `secret://`, or `env://`. GraphOS resolves the
credential pair in the parent process. The private provider child receives only
the materialized `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` values required
by the Langfuse SDK; the references are removed from that child environment.
Neither values nor references are emitted in readiness results or logs.

Graph persistence requires its own
`LANGFUSE_PERSISTENCE_HMAC_KEY_REF`. The Langfuse API secret is not an identity
key and is never reused for that purpose.

## TLS trust

Certificate and hostname verification remain enabled. With no custom trust
setting, the provider uses system trust. For a private authority, reference a
PEM trust store containing the required root, roots, or chain certificates.
Agent Utilities:

1. resolves the trust reference in memory;
2. validates bounded, parseable CA certificates;
3. materializes the trust store with owner-only permissions;
4. supplies its runtime path to the child as both `REQUESTS_CA_BUNDLE` and
   `SSL_CERT_FILE`; and
5. leaves final certificate-path and hostname verification to the live TLS
   connection.

Static bundle validation does not claim that a specific server leaf is already
chained. OpenSSL and Requests construct and verify the target server's path at
connection time.

For mutual TLS, configure both `LANGFUSE_CLIENT_CERT_REF` and
`LANGFUSE_CLIENT_KEY_REF`; optionally configure
`LANGFUSE_CLIENT_KEY_PASSWORD_REF` for an encrypted key. Agent Utilities
validates the pair, creates a private process-lifetime client bundle, and passes
that bundle to the provider's Requests transport. The references, password, and
machine-specific paths are not persisted or logged.

If `uv` itself must use platform trust while installing or updating the package,
set `UV_NATIVE_TLS=true` in that installer process. Native GraphOS launch does
not invoke `uv`, so this setting does not belong in provider or MCP
configuration.

## Direct installed-provider launch

Direct launch is useful for isolated development and for supervisors that
already implement secret injection. The supervisor must materialize the project
keys only in the child process; never place their values in an MCP file,
Compose file, shell profile, or command line.

### stdio

```json
{
  "mcpServers": {
    "langfuse-mcp": {
      "command": "python",
      "args": ["-m", "langfuse_agent.mcp_server"],
      "env": {
        "MCP_TOOL_MODE": "condensed"
      }
    }
  }
}
```

The `python` command must be the interpreter in which the provider was
installed. Native GraphOS avoids this ambiguity by using its exact current
interpreter.

### Streamable HTTP

Run the installed module under a service supervisor and bind loopback unless a
reviewed network policy requires another interface:

```bash
python -m langfuse_agent.mcp_server \
  --transport streamable-http --host 127.0.0.1 --port 8004
curl -fsS http://127.0.0.1:8004/health
```

Connect an MCP client to the already-running service:

```json
{
  "mcpServers": {
    "langfuse-mcp": {
      "url": "http://127.0.0.1:8004/mcp"
    }
  }
}
```

For a remote deployment, replace the URL at runtime with the authenticated HTTPS
endpoint published by the service gateway. Do not commit a deployment hostname.

### Container

The direct container path uses the same child-materialization boundary. The
following command passes variable names only; a secret-aware process supervisor
must populate them:

```bash
docker run --rm -i \
  --read-only \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  -e LANGFUSE_HOST \
  -e LANGFUSE_PUBLIC_KEY \
  -e LANGFUSE_SECRET_KEY \
  -e REQUESTS_CA_BUNDLE \
  -e SSL_CERT_FILE \
  example/langfuse-agent:mcp
```

The repository Compose definitions likewise expect runtime injection. Do not
create a checked-in `.env` file containing materialized keys.

## A2A agent server

The optional `langfuse-agent` console script wraps the MCP tool surface in a
Pydantic-AI graph agent. After the process supervisor injects the Langfuse and
model-provider secrets, start the already-installed server:

```bash
langfuse-agent --provider openai --model-id gpt-4o
```

In a split deployment, configure `MCP_URL` with the runtime address of the MCP
service. Bind both services to loopback or a private service network and publish
only the authenticated gateway.

## Reverse proxy and DNS

Publish the HTTP transport behind an authenticated TLS reverse proxy. Runtime
configuration supplies the hostname:

```caddy
{$LANGFUSE_AGENT_HOSTNAME} {
    reverse_proxy langfuse-agent-mcp:8004
}
```

Create DNS records through the deployment's approved DNS automation. Keep API
tokens, zone names, addresses, and hostnames outside the repository.

## Safe verification

1. Run `agent-utilities doctor` and confirm that the two credential references
   resolve without printing their values.
2. Confirm that GraphOS reports the native Langfuse provider as available.
3. Call `langfuse_observability` with `action=trace_list` and a small `limit`.
   An empty data list is a successful authenticated response.
4. Emit one synthetic, content-free local-model trace and flush the exporter.
5. Confirm only a neutral trace identifier or aggregate count, then apply the
   configured retention policy.

Never print service URLs, project keys, certificate paths or subjects, raw
trace content, user identifiers, or source-system records during verification.
