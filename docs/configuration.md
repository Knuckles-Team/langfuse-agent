# Configuration, trust, and privacy

This page is the operator contract for `langfuse-agent`. Runtime values are
injected by the launcher; they do not belong in source, packaged skills, MCP
catalogs, traces, or generated reports.

## Capability configuration

The current capability surface is defined by three versioned artifacts:

- the action-routed MCP tools described in the README and `docs/usage.md`;
- the compact canonical skill plus any specialist `WORKFLOW.md` procedures;
- `connector_manifest.yml` and its ontology, mappings, shapes, fixtures,
  migrations, tool-schema fingerprints, and certification metadata.

Treat those artifacts as a unit during release and deployment. Do not enable a
skill whose certification or tool-schema fingerprint does not match the
installed package. Delegated agents use the compact, intent-oriented tool
surface.

## Canonical runtime settings

GraphOS reads these settings through `AgentConfig`:

| Setting | Purpose |
|---|---|
| `LANGFUSE_HOST` | Canonical Langfuse service URL; defaults to Langfuse Cloud |
| `LANGFUSE_PUBLIC_KEY_REF` | Runtime reference to the project public key |
| `LANGFUSE_SECRET_KEY_REF` | Runtime reference to the project secret key |
| `LANGFUSE_TLS_PROFILE_REF` | Runtime reference to a reusable TLS profile |
| `LANGFUSE_CA_BUNDLE_REF` | Runtime reference to a PEM trust store when a full profile is unnecessary |
| `LANGFUSE_CLIENT_CERT_REF` | Runtime reference to an mTLS client certificate |
| `LANGFUSE_CLIENT_KEY_REF` | Runtime reference to its matching mTLS private key |
| `LANGFUSE_CLIENT_KEY_PASSWORD_REF` | Optional runtime reference for an encrypted client key |
| `LANGFUSE_PERSISTENCE_HMAC_KEY_REF` | Dedicated identity-HMAC key reference required for graph persistence |

Secret references use `vault://`, `secret://`, or `env://`. GraphOS resolves
them in the parent process and starts the installed
`langfuse_agent.mcp_server` module with its current Python interpreter. The
private child environment receives materialized project keys and trust-file
locations; references and values are not written back to configuration.

Do not add a handwritten Langfuse server entry to a GraphOS MCP catalog. Once
the provider is installed, GraphOS registers it lazily when both credential
references are configured. This path performs no package-index lookup at
startup.

For a direct provider launch outside GraphOS, the process supervisor must inject
the materialized project keys at process creation. Do not persist those values
in a shell profile, `.env` file, Compose file, MCP catalog, or command line.

Additional operating rules:

- Supply tenant identifiers and model keys through runtime configuration or a
  secret provider.
- Use non-personal agent aliases and opaque tenant/correlation identifiers.
- Keep developer directories, workstation names, and deployment hostnames out
  of checked-in configuration.
- Bind network transports to an explicitly chosen interface and require the
  deployment's MCP authentication policy before accepting remote traffic.
- Enable optional agent, embedding, evolution, or observability features only
  when their dependencies and backends are configured and healthy.

The checked-in examples use `localhost` for loopback-only development and the
reserved `example.invalid` domain for replaceable network endpoints. Neither is
a production endpoint.

## TLS trust

Certificate and hostname verification are required. System trust is used when
no private trust material is configured. A referenced PEM trust store may
contain one root, multiple roots, or the relevant chain certificates. Agent
Utilities validates that the input is bounded, parseable CA material, then
materializes it with owner-only permissions and projects its runtime path to
both `SSL_CERT_FILE` and `REQUESTS_CA_BUNDLE` for the child.

The TLS client constructs and verifies the server's certificate path at
connection time. Static validation does not prove that a particular server
leaf chains to every certificate in the supplied trust store.

`UV_NATIVE_TLS=true` is an installer setting only when an administrator uses
`uv` to install or update packages through platform trust. Native GraphOS launch
does not invoke `uv`, so this setting does not belong in the Langfuse child
configuration.

Do not disable verification to work around an incomplete server chain. Keep CA
bundle locations environment-configured and stable for the runtime; never embed
a workstation path or certificate material in MCP configuration.

## Privacy and data governance

The default observability posture is metadata-only. Do not persist prompts,
message bodies, tool inputs/results, document content, raw traces, credentials,
local paths, hostnames, or personal identity unless an approved data contract
explicitly requires it. Keep Langfuse or OTLP content capture disabled unless a
reviewed retention and access policy authorizes it.

When connector ingestion is enabled, each change must carry tenant, ACL,
classification, retention, provenance, and checkpoint/delta metadata. Reject or
quarantine records that cannot satisfy that contract; never silently widen a
tenant scope. Logs and reports should contain counts, status, and opaque
references only.

## Deployment verification

1. Validate the capability bundle and skill metadata against the installed tool
   schemas.
2. Confirm required secrets are present without printing their values.
3. Make a verified TLS connection to the configured host.
4. Exercise health/readiness and one least-privilege read operation.
5. Confirm traces arrive under the expected opaque tenant/run identifiers and
   contain no captured content.
6. Record only sanitized pass/fail evidence and version identifiers.
