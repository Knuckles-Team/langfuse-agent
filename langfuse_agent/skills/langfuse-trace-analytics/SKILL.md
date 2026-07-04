---
name: langfuse-trace-analytics
description: >-
  LLM-observability analytics on Langfuse via the langfuse-agent MCP server —
  list and read traces, drill into their observations and generations, group by
  session, read scores, and run aggregate metrics. Use when the agent must
  inspect what an LLM app did: find recent/slow/expensive traces, follow a
  trace's generation tree, attribute activity to a user or session, or ingest
  that activity into the knowledge graph as typed :Trace/:Observation/:Generation
  nodes. Do NOT use for creating/managing datasets & scores as an eval set (use
  langfuse-eval-datasets) or the prompt/model registry (use
  langfuse-prompt-management).
license: MIT
tags: [langfuse, observability, tracing, llm, metrics, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Langfuse Trace Analytics

Domain-typed read access to the Langfuse **observability** surface: traces,
observations (spans/events/generations), sessions, scores and metrics. Prefer the
condensed `langfuse_observability` tool — it action-routes to the Langfuse public
API and returns trace-shaped records.

## When to use
- Triage recent traces (slowest, most expensive, errored) and read one by id.
- Follow a trace's tree of observations / LLM generations (model, tokens, cost).
- Group traces by `sessionId` or attribute them to a `userId`.
- Read evaluation scores attached to traces/observations/sessions.
- Run aggregate metrics (counts, latency, cost) over a time window.
- Push observability activity into the KG as typed nodes (`langfuse_ingest`).

## When NOT to use
- Building an eval set — creating datasets, dataset items/runs, or writing scores
  → `langfuse-eval-datasets`.
- Managing prompt versions or model/pricing definitions →
  `langfuse-prompt-management`.
- Org/project/member/SCIM admin → the `langfuse_management` tool directly.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`langfuse-agent`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `LANGFUSE_PUBLIC_KEY` | ✅ | Project public key (`pk-lf-…`) |
| `LANGFUSE_SECRET_KEY` | ✅ | Project secret key (`sk-lf-…`) |
| `LANGFUSE_HOST` | optional | Base URL (defaults to Langfuse Cloud) |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed
`langfuse_observability` tool (used below) vs. the one-to-one verbose tools.

## Tools & actions
| Condensed tool | Key actions |
|----------------|-------------|
| `langfuse_observability` | `trace_list`, `trace_get`, `observations_get_many`, `sessions_list`, `sessions_get`, `scores_get_many`, `scores_get_by_id`, `metrics_metrics` |
| `langfuse_ingest` | `kind=traces\|observations\|sessions\|scores` — list + push to KG |

### Key parameters (passed as top-level tool args)
- `trace_list`: `user_id`, `session_id`, `name`, `tags`, `from_timestamp`,
  `to_timestamp`, `order_by`, `limit`, `page`, `environment`, `filter`.
- `trace_get`: `trace_id` (required).
- `observations_get_many`: `trace_id`, `type` (`GENERATION`/`SPAN`/`EVENT`),
  `parent_observation_id`, `fields` (`core,basic,io,usage,model,metrics`), `cursor`.
- `scores_get_many`: `trace_id`, `observation_id`, `session_id`, `name`, `data_type`.

## Recipes
Recent traces for a user, newest first:
```
action=trace_list user_id="alice" order_by="timestamp.desc" limit=25
```
Read one trace by id:
```
action=trace_get trace_id="<trace_id>"
```
Every generation under a trace, with model + token/cost fields:
```
action=observations_get_many trace_id="<trace_id>" type="GENERATION" fields="core,basic,model,usage,metrics"
```
Scores attached to a trace:
```
action=scores_get_many trace_id="<trace_id>"
```
Ingest the last 100 traces into the knowledge graph as typed nodes:
```
tool=langfuse_ingest kind="traces" limit=100
```

## Gotchas
- `observations_get_many` uses **cursor** pagination (`cursor` from the response
  metadata), while `trace_list` / `sessions_list` / `scores_get_many` use
  **page**-based pagination (`page` + `limit`). Don't mix them.
- Field groups are lazy: request `model`, `usage`, `metrics`, `io` explicitly via
  `fields` or you only get `core,basic`.
- A **Generation** is an observation with `type=GENERATION`; token usage lives
  under `usage` and cost under `calculatedTotalCost`.
- `trace_list` / `trace_get` / `observations_get_many` / `sessions_list` /
  `scores_get_many` **auto-ingest** into the KG best-effort when an engine is
  reachable; it is a no-op otherwise and never blocks the read.
- Bound reads with `from_timestamp`/`to_timestamp` + a sane `limit`; unbounded
  trace scans are slow on busy projects.

## Related
- **KG ingestion:** `langfuse_agent.kg_ingest` maps these records to
  `:Trace`/`:Observation`/`:Generation`/`:Session`/`:Score` nodes (federated by
  `langfuse_agent.ontology`).
- **Sibling skills:** `langfuse-eval-datasets`, `langfuse-prompt-management`.
