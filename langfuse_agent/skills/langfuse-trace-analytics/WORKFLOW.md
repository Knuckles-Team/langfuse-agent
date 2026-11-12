# Langfuse Trace Analytics

LLM-observability analytics on Langfuse via the langfuse-agent MCP server — list and read traces, drill into their observations and generations, group by session, read scores, and run aggregate metrics. Use when the agent must inspect what an LLM app did: find recent/slow/expensive traces, follow a trace's generation tree, attribute activity to a user or session, or ingest that activity into the knowledge graph as typed :Trace/:Observation/:Generation nodes. Do NOT use for creating/managing datasets & scores as an eval set (use langfuse-eval-datasets) or the prompt/model registry (use langfuse-prompt-management).

## Scope

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
| `LANGFUSE_PUBLIC_KEY_REF` | ✅ | Runtime secret reference for the project public key |
| `LANGFUSE_SECRET_KEY_REF` | ✅ | Runtime secret reference for the project secret key |
| `LANGFUSE_HOST` | optional | Base URL (defaults to Langfuse Cloud) |

Arbora resolves the references in its parent process. Never place materialized
keys in skill content or delegated tool arguments.


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
- `scores_get_many`: `id`, `trace_id`, `observation_id`, `session_id`,
  `experiment_id`, `name`, `data_type`, `cursor`, `value_min`, `value_max`.

## Recipes
Recent traces for a user, newest first:
```
action=trace_list user_id="<opaque_user_id>" order_by="timestamp.desc" limit=25
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
- `observations_get_many` and Scores API v3 use **cursor** pagination (`cursor`
  from response metadata). `trace_list` and `sessions_list` remain page-based.
- Field groups are lazy: request `model`, `usage`, `metrics`, `io` explicitly via
  `fields` or you only get `core,basic`.
- A **Generation** is an observation with `type=GENERATION`; token usage lives
  under `usage` and cost under `calculatedTotalCost`.
- When `LANGFUSE_KG_AUTO_INGEST=true`, `trace_list` / `trace_get` /
  `observations_get_many` / `sessions_list` / `scores_get_many` perform an
  authoritative native KG write and surface engine or validation failures.
- Bound reads with `from_timestamp`/`to_timestamp` + a sane `limit`; unbounded
  trace scans are slow on busy projects.

## Related
- **KG ingestion:** `langfuse_agent.kg_ingest` maps these records to
  `:Trace`/`:Observation`/`:Generation`/`:Session`/`:Score` nodes (federated by
  `langfuse_agent.ontology`).
- **Sibling skills:** `langfuse-eval-datasets`, `langfuse-prompt-management`.
