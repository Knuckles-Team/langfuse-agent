---
name: langfuse-agent-development
skill_type: skill
domain: development
description: >-
  Develop, test, gate, and release the langfuse-agent connector. Use this skill
  when changing Langfuse API mappings, governed MCP tools, authentication,
  knowledge-graph ingestion, packaged content, or repository gates.
license: MIT
tags: [langfuse, observability, development, connector, test, gates]
tier: repository
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---

# langfuse-agent development

This repository owns the Langfuse API facade, the governed MCP tool surface,
authentication boundary, typed graph-ingestion mappings, and packaged connector
content. Shared connector contracts, transports, TLS profiles, and credential
helpers belong to `scion-sdk`; admission, serving, and durable graph
state belong to their owning repositories. Read `AGENTS.md` before changing
code. Keep credentials, private endpoints, tenant data, and customer records out
of source, logs, fixtures, and skill content.

## Rapid delivery: the 5-minute contract

Specs are already designed. Deliver small, reviewable slices and cite the
owning spec row in the commit trailer.

- Find the owning row first with `git grep -n "<term>" -- specs` and extend the
  existing spec before adding requirement text. Generated `specs/*/status.json`
  files come from the shared hooks; never hand-edit them.
- Reuse the `Connector` in `langfuse_agent/__init__.py`, the `LangfuseApi`
  facade in `langfuse_agent/api_client.py`, the API modules under
  `langfuse_agent/api/`, and the registered tools in `langfuse_agent/tools/`
  plus `langfuse_agent/mcp_server.py`. Do not create a second API, MCP,
  authentication, or transport plane.
- Preserve `LANGFUSE_BASE_URL`, `LANGFUSE_HOST`, `LANGFUSE_PUBLIC_KEY`,
  `LANGFUSE_SECRET_KEY`, the `LANGFUSE_*_REF` credential and TLS settings,
  and `LANGFUSE_PERSISTENCE_HMAC_KEY_REF` handling at the existing
  `langfuse_agent/auth.py` and `langfuse_agent/kg_ingest.py` boundaries. Use
  the SDK TLS and credential resolvers; never print credentials or add a
  verification bypass.
- Keep the `MCP_TOOL_MODE` surface and the existing Langfuse tool toggle
  settings aligned with `langfuse_agent/mcp_server.py` and the generated README
  inventory. Mock provider HTTP responses in tests; never call a live Langfuse
  project or use live credentials in a gate.
- Preserve typed, privacy-bounded ingestion through
  `scion_sdk.ingest`, source declarations in
  `langfuse_agent/connector_sources.py`, and neutral ontology assets under
  `langfuse_agent/ontology/`. Do not bypass the shared ingestion facade.
- Keep `skills/**`, `ontology/**`, `connectors/**`, prompts, and
  `mcp_config.json` coherent with the `langfuse_agent` package data and the
  `langfuse-mcp` project script. Every delivered
  requirement needs a bound focused test.

## Setup and gates

Use the pinned environment from `uv sync --locked`, then run the shared gates:

```bash
uv sync --locked
uvx pre-commit run --all-files
uvx pre-commit run --all-files --hook-stage pre-push
```

For focused feedback, run the smallest affected tests with the locked
environment, for example:

```bash
uv run --locked --extra test pytest -q tests/test_langfuse_development_skill.py
uv run --locked --extra test pytest -q tests/test_pages_workflow.py
```

The canonical `.pre-commit-config.yaml` delegates connector-standard, secrets,
spec, tests-fast, and dependency-readiness to `Knuckles-Team/pipelines` at
`rev: main`. Do not copy those hooks locally or bypass a failing check.

## Connector-specific checks

- Keep Langfuse API operation names, request models, pagination, and response
  projections stable when changing `langfuse_agent/api/`; add a focused mocked
  request test for a changed provider path.
- Preserve the validated host, SDK TLS profile, credential-reference, and OIDC
  delegation behavior in `langfuse_agent/auth.py`. Translate provider failures
  through the existing client boundary and keep raw inputs out of persisted
  graph records.
- Keep observability, dataset, prompt/model, management, and KG tools registered
  through the existing modules under `langfuse_agent/tools/`. Keep source
  metadata tenant-neutral and ingestion best-effort only where the current
  implementation already defines that behavior.
- Keep `langfuse_agent/skills/`, `langfuse_agent/ontology/`,
  `langfuse_agent/connectors/`, prompts, and `langfuse_agent/mcp_config.json`
  in package data. Documentation is published by the existing Pages workflow
  with its checked-in spec dashboard configuration and
  `pages_pipeline.yml@main` caller.

## Packaging and publication

`pyproject.toml` packages `skills/**`, `ontology/**`, `connectors/**`, prompts,
and `mcp_config.json` and exposes the `langfuse-mcp` project script. When
packaged content changes, inspect the build output for
`langfuse_agent/skills/langfuse-agent-development/SKILL.md`; leave the current
package version and lock entry unchanged unless an existing release contract
requires a release. Do not commit generated Docker artifacts or claim package,
container, or Pages publication from a local build; require exact hosted
evidence for those claims.

## Delivery discipline

Work in a real Git worktree based on `origin/main`. Inspect the complete diff,
stage only reviewed paths, and verify `git status --short` after every gate. Do
not use `git stash`, `git add -A`, or `git add .`; preserve unrelated working
tree changes. Keep runtime, ontology, status, and generated artifacts outside a
bounded documentation or skill slice unless the owning requirement explicitly
requires them.
