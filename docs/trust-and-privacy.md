# Trust and privacy

`langfuse-agent` inherits its runtime configuration from the process that
launches it. Keep service addresses, credentials, certificate locations, user
identities, and trace payloads out of repository files and MCP catalogs.

## Minimal GraphOS configuration

With the current `agent-utilities` runtime, no handwritten Langfuse MCP entry is
required. GraphOS registers the installed provider lazily when both credential
references are available. The parent process supplies:

| Setting | Purpose |
|---|---|
| `LANGFUSE_HOST` | Canonical service URL |
| `LANGFUSE_PUBLIC_KEY_REF` | `vault://`, `secret://`, or `env://` reference to the project public key |
| `LANGFUSE_SECRET_KEY_REF` | `vault://`, `secret://`, or `env://` reference to the project secret key |
| `LANGFUSE_TLS_PROFILE_REF` | Optional reference to a reusable TLS profile |
| `LANGFUSE_CA_BUNDLE_REF` | Preferred secret reference for a private CA bundle |
| `LANGFUSE_CLIENT_CERT_REF` | Optional reference to an mTLS client certificate |
| `LANGFUSE_CLIENT_KEY_REF` | Reference to the matching mTLS private key |
| `LANGFUSE_CLIENT_KEY_PASSWORD_REF` | Optional reference for an encrypted client key |
| `LANGFUSE_PERSISTENCE_HMAC_KEY_REF` | Dedicated identity-HMAC key reference for optional graph persistence |

GraphOS resolves references in memory and starts
`python -m langfuse_agent.mcp_server` with its own interpreter. It passes only
the materialized runtime values required by that child. The launch performs no
package download or package-index lookup.

## Private certificate authorities

Use system trust when it contains the issuing authority. Otherwise reference a
PEM trust store containing the required root, roots, or chain certificates. Do
not disable TLS verification and do not point Requests at a binary certificate.

At startup, `agent-utilities`:

1. resolves `LANGFUSE_CA_BUNDLE_REF` in memory;
2. validates bounded, parseable CA certificates and current validity windows;
3. materializes it with owner-only permissions in the runtime directory;
4. projects the runtime-only location to both `REQUESTS_CA_BUNDLE` and
   `SSL_CERT_FILE`; and
5. leaves hostname and certificate-path verification enabled for the live
   connection.

An operator-managed PEM may instead be supplied through
`LANGFUSE_CA_BUNDLE`. Existing `REQUESTS_CA_BUNDLE` and `SSL_CERT_FILE`
settings are accepted only after the same validation. Certificate paths and
subjects are never returned by readiness checks or written to logs.

The order and number of certificates are not used to claim a pre-verified
server chain. OpenSSL and Requests construct and verify the target server's
certificate path at connection time.

The MCP configuration stores neither a certificate path nor project keys.
GraphOS resolves the secret reference, creates the bounded runtime file, and
supplies the two CA environment variables only to the child process.

Mutual TLS uses the same boundary. Both client-certificate and private-key
references are required; an encrypted key may use the password reference.
GraphOS validates the pair and gives the provider only a private,
process-lifetime combined client bundle. The Requests adapter applies that
bundle to every Langfuse API request.

When `uv` itself must install or update the package through platform trust, set
`UV_NATIVE_TLS=true` in that installer process. Native GraphOS launch uses the
already-installed module and does not invoke `uv`.

## Safe verification

Use a synthetic trace and inspect only status, counts, and neutral identifiers:

1. call `langfuse_observability` with `action=runtime_posture` and require
   `content_capture_enabled=false` plus `metadata_only=true`;
2. emit a synthetic local-LLM trace with no source documents or user fields;
3. call `langfuse_observability` with `action=trace_list`, the exact opaque
   tenant-qualified trace name, metadata-only fields, and a small limit;
4. require exactly one matching trace whose controlled metadata binds the same
   run, configured model, model class, skill, and skill-body digest; and
5. discard the synthetic trace according to the project's retention policy.

Do not use an unfiltered project-wide trace list as certification evidence; it
can expose unrelated project metadata and cannot prove which runtime emitted a
trace.

Never print project keys, service URLs, certificate paths, raw trace inputs or
outputs, user IDs, email addresses, or source-system content during this check.

## Knowledge-graph persistence

Reading a trace through MCP does not persist it. `LANGFUSE_KG_AUTO_INGEST` is
off by default; enable it only after the governed graph destination and
retention policy are approved. Explicit or automatic ingestion requires the
shared persistence privacy guard and a dedicated key resolved only from
`LANGFUSE_PERSISTENCE_HMAC_KEY_REF`. The Langfuse API secret is never reused for
identity derivation.

Before a node crosses the persistence boundary, the connector:

- drops person and user entities and their relationships;
- removes raw external, trace, session, observation, and user identifiers;
- replaces every node identity with a stable HMAC-derived identifier;
- persists only validated structural enums, timestamps, and numeric usage/cost
  metadata for traces, sessions, observations, generations, models, and scores;
- drops free-form names, tags, URLs, host/path fields, environment/release
  labels, model labels, and categorical score text; and
- emits only exception categories in logs.

If the privacy guard or HMAC key is unavailable, ingestion fails closed while
read-only MCP access remains available.

## Failure behavior

Custom trust fails closed. An incomplete, expired, malformed, or unrelated CA
bundle prevents the Langfuse child from being registered. Network and
authentication exceptions expose stable error categories only; response bodies,
request URLs, and exception causes are not propagated.
