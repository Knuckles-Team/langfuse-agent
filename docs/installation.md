# Installation

`langfuse-agent` is a standard Python package and a prebuilt container image. Pick the
path that matches how you want to run it.

Every built wheel contains a deterministic CycloneDX 1.6 SBOM at
`.dist-info/sboms/package.cyclonedx.json`. The PEP 517 build backend derives it from the
final wheel metadata and rebuilds `RECORD`; every direct-reference URL fails the build so
package artifacts cannot retain workstation or network locations. A packaged,
source-controlled catalog supplies canonical SPDX expressions for the root, runtime,
optional, documentation, test, and development components. Missing or invalid entries
fail closed, and every emitted SBOM component therefore has reviewed license metadata.

The repository-owned release job is wheel-only. It deliberately does not synchronize the
development lock's editable sibling checkouts; instead, it builds twice from the package
metadata with the same bounded PEP 517 environment and fixed `SOURCE_DATE_EPOCH`. Both
candidates must pass the SBOM, version, image, and privacy contracts and have identical
filenames and SHA-256 digests. Only that byte-identical wheel is uploaded and published;
no source archive or local-source provenance is admitted to the release.

## Requirements

- **Python 3.11 – 3.14**.
- A reachable **Langfuse** instance (self-hosted or Langfuse Cloud) — see
  [Backing Platform](platform.md) to deploy one locally.
- For a private CA, a referenced PEM trust store containing the required root,
  roots, or chain certificates; see [Trust and privacy](trust-and-privacy.md).

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

If `uv` must use the platform trust store while provisioning, set
`UV_NATIVE_TLS=true` in the installer environment. This is not a provider
runtime setting.

## Prebuilt container images

The multi-stage build publishes separate MCP and full-agent targets. Deploy a
reviewed immutable MCP-image digest supplied by the operator:

```bash
export LANGFUSE_MCP_IMAGE='registry.example.invalid/langfuse-agent@sha256:<digest>'
docker run --rm -i \
  -e LANGFUSE_HOST \
  -e LANGFUSE_PUBLIC_KEY \
  -e LANGFUSE_SECRET_KEY \
  -e REQUESTS_CA_BUNDLE \
  -e SSL_CERT_FILE \
  "$LANGFUSE_MCP_IMAGE" langfuse-mcp
```

This direct-container form expects the process supervisor to inject the
materialized key variables and optional trust-store paths at container creation.
Do not place their values in the command, a Compose file, or a checked-in env
file. Production GraphOS deployments instead configure
`LANGFUSE_PUBLIC_KEY_REF` and `LANGFUSE_SECRET_KEY_REF`; GraphOS performs the
private child materialization.

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
- **[Configuration](deployment.md#canonical-configuration)** — canonical runtime settings.
