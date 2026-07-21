# Backing platform — Langfuse

`langfuse-agent` is a client of a Langfuse service selected by the canonical
`LANGFUSE_HOST` setting. It does not provision or embed Langfuse.

For production, follow the upstream
[Langfuse self-hosting documentation](https://langfuse.com/self-hosting) or use
Langfuse Cloud. Pin reviewed image versions or digests, keep the service on a
private network, and inject every platform credential through the deployment's
secret manager.

## Self-hosted components

Current Langfuse self-hosting uses the web service plus PostgreSQL, ClickHouse,
Redis, and S3-compatible object storage. The authoritative topology and required
settings belong to the Langfuse release being deployed; do not copy static
database passwords or encryption keys from this connector repository.

At minimum, externalize:

- database, ClickHouse, Redis, and object-store credentials;
- application authentication, salt, and encryption keys;
- public service URL and ingress policy;
- image tags or digests, storage classes, backup policy, and retention; and
- the CA or TLS profile used by clients.

The platform and connector use separate secret scopes. A Langfuse project API
pair is issued after the platform is healthy; it is not a platform database
credential.

## Connect GraphOS

Store the project API pair and optional TLS profile in the configured secret
provider, then configure only references in `AgentConfig`:

```bash
export LANGFUSE_HOST=https://langfuse.example.invalid
export LANGFUSE_PUBLIC_KEY_REF=env://LANGFUSE_PROJECT_PUBLIC_KEY
export LANGFUSE_SECRET_KEY_REF=env://LANGFUSE_PROJECT_SECRET_KEY
export LANGFUSE_TLS_PROFILE_REF=env://LANGFUSE_RUNTIME_TLS_PROFILE
```

The `env://` references are neutral schema examples; a deployment may supply any
supported reference through `AgentConfig`. The TLS-profile reference is optional
when system trust is sufficient. GraphOS
resolves the references in memory and starts the installed provider module; no
Langfuse-specific MCP catalog entry is required.

For loopback-only development, `LANGFUSE_HOST=http://localhost:3000` is allowed.
Non-loopback deployments require HTTPS.

## Shared container network

When Langfuse and the provider share a container network, select the service URL
at deployment time and keep credential material in the orchestrator's secret
store. The provider container is a child runtime and therefore receives the
materialized project keys only from that orchestrator:

```yaml
services:
  langfuse-agent-mcp:
    image: example/langfuse-agent:mcp
    depends_on:
      - langfuse-web
    environment:
      - LANGFUSE_HOST
      - LANGFUSE_PUBLIC_KEY
      - LANGFUSE_SECRET_KEY
      - REQUESTS_CA_BUNDLE
      - SSL_CERT_FILE
      - TRANSPORT=streamable-http
      - HOST=0.0.0.0
      - PORT=8004
      - MCP_TLS_TERMINATED
      - MCP_TRUSTED_PROXY_CIDRS
      - MCP_ALLOWED_HOSTS
    ports:
      - "127.0.0.1:8004:8004"
```

The non-loopback listener is valid only behind the operator-supplied authenticated
TLS ingress selected by those exact proxy and host policies. Do not put key values,
platform passwords, deployment hostnames, or certificate paths in the Compose file.
A production GraphOS parent uses the corresponding `*_REF` settings and performs
this child materialization automatically.

## Verify

1. Check the Langfuse platform's documented health endpoint.
2. Run `agent-utilities doctor` without exposing secret values or service URLs.
3. Call `langfuse_observability` with `action=trace_list` and a small limit.
4. Treat an authenticated empty result as successful connectivity.

See [Deployment](deployment.md) for the provider runtime and
[Trust and privacy](trust-and-privacy.md) for private-CA handling.
