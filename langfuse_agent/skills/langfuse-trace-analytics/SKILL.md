---
name: langfuse-trace-analytics
skill_type: skill
description: >-
  Langfuse observability via the langfuse-agent MCP server: list and read traces, observations, generations, sessions, scores and metrics. Use to inspect what an LLM app did. Do NOT use for datasets and scores (langfuse-eval-datasets) or the prompt registry (langfuse-prompt-management).
license: MIT
tags: [langfuse, observability, tracing, llm, metrics, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---
# Langfuse Trace Analytics

Scope: LLM-observability analytics on Langfuse via the langfuse-agent MCP server — list and read traces, drill into their observations and generations, group by session, read scores, and run aggregate metrics. Use when the agent must inspect what an LLM app did: find recent/slow/expensive traces, follow a trace's generation tree, attribute activity to a user or session, or ingest that activity into the knowledge graph as typed :Trace/:Observation/:Generation nodes. Do NOT use for creating/managing datasets and scores as an eval set (use langfuse-eval-datasets) or the prompt/model registry (use langfuse-prompt-management).

Domain-typed read access to the Langfuse **observability** surface: traces,
observations (spans/events/generations), sessions, scores and metrics. Use the typed trace, observation,
session, score and metrics tools; they call the Langfuse public API and return
trace-shaped records.

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
- Org/project/member/SCIM admin → the project, organization and SCIM tools of `langfuse-agent-operations`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`langfuse-agent`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `LANGFUSE_PUBLIC_KEY` | ✅ | Project public key (`pk-lf-…`) |
| `LANGFUSE_SECRET_KEY` | ✅ | Project secret key (`sk-lf-…`) |
| `LANGFUSE_HOST` | optional | Base URL (defaults to Langfuse Cloud) |


## Steps

1. Confirm the target project by calling `langfuse_runtime_posture`. Verify the response returns without an authentication error before reading anything.
2. List candidate traces with `langfuse_trace_list` (set `from_timestamp`, `to_timestamp` and `limit`). Verify the result is non-empty and the traces match the requested user or session.
3. Read the chosen trace with `langfuse_trace_get` (`trace_id`). Verify the returned id equals the one requested.
4. Fetch its generations with `langfuse_observations_get_many` (`trace_id`, `type="GENERATION"`, `fields="core,basic,model,usage,metrics"`). Verify model, usage and cost fields are present.
5. Run `langfuse_metrics_get` for aggregates when counts, latency or cost over a window are needed. Verify the query window matches the request.
6. Optionally push records to the graph with `langfuse_ingest` (`kind="traces"`, `limit=100`). Verify the reported ingested count is above zero.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| 401 or authentication error | `LANGFUSE_PUBLIC_KEY` or `LANGFUSE_SECRET_KEY` missing or wrong project | Set both variables for the intended project, then call `langfuse_runtime_posture` to confirm access. |
| Empty trace list | Time window too narrow or wrong `user_id` / `session_id` | Widen `from_timestamp` and `to_timestamp`, drop filters one at a time, and list again with `langfuse_trace_list`. |
| Generation fields missing | `fields` omitted so only `core,basic` returned | Re-call `langfuse_observations_get_many` with `fields="core,basic,model,usage,metrics"`. |

## Tools
One typed tool per operation; pass each argument by name.

| Tool | Use |
|------|-----|
| `langfuse_trace_list`, `langfuse_trace_get` | List and read traces |
| `langfuse_observations_get_many` | Observations (generations, spans, events) |
| `langfuse_sessions_list`, `langfuse_sessions_get` | Sessions |
| `langfuse_scores_get_many` | Scores attached to traces and observations |
| `langfuse_metrics_get` | Aggregated metrics for a query |
| `langfuse_comments_get`, `langfuse_comments_get_by_id`, `langfuse_comments_create` | Comments on traces and observations |
| `langfuse_ingest` | `kind=traces\|observations\|sessions\|scores` - list and push to the knowledge graph |
| `langfuse_runtime_posture` | Whether content capture is on |

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
