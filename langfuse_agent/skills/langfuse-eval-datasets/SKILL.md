---
name: langfuse-eval-datasets
description: >-
  Evaluation datasets and scoring on Langfuse via the langfuse-agent MCP server —
  create and read datasets and dataset items, launch/read dataset runs, define
  score configs, and write scores against traces/observations/sessions. Use when
  the agent must build or inspect an eval set, compare model/prompt versions
  across a dataset run, or attach numeric/categorical/boolean scores. Do NOT use
  for reading production traces/generations (use langfuse-trace-analytics) or the
  prompt/model registry (use langfuse-prompt-management).
license: MIT
tags: [langfuse, evaluation, datasets, scores, llm, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Langfuse Eval Datasets

Domain-typed access to the Langfuse **datasets & scoring** surface: datasets,
dataset items, dataset runs, score configs and scores. Use these to curate test
sets and grade LLM output. Prefer the condensed `langfuse_datasets` and
`langfuse_observability` (score endpoints) tools.

## When to use
- Create / list / read datasets and their items.
- Create dataset run items and read a dataset's runs (to compare versions).
- Define a **score config** (schema: name, data type, range/categories).
- Write a **score** (numeric/categorical/boolean) onto a trace, observation, or
  session; read scores back for analysis.

## When NOT to use
- Browsing production traffic (traces / generations / sessions) →
  `langfuse-trace-analytics`.
- Managing prompt templates or model pricing → `langfuse-prompt-management`.
- Bulk KG ingestion of scores → `langfuse_ingest kind=scores` (analytics skill).

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`langfuse-agent`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `LANGFUSE_PUBLIC_KEY` | ✅ | Project public key (`pk-lf-…`) |
| `LANGFUSE_SECRET_KEY` | ✅ | Project secret key (`sk-lf-…`) |
| `LANGFUSE_HOST` | optional | Base URL (defaults to Langfuse Cloud) |

## Tools & actions
| Condensed tool | Key actions |
|----------------|-------------|
| `langfuse_datasets` | `datasets_list`, `datasets_create`, `datasets_get`, `dataset_items_create`, `dataset_items_list`, `dataset_items_get`, `dataset_run_items_create`, `datasets_get_runs`, `datasets_get_run` |
| `langfuse_observability` | `score_configs_create`, `score_configs_get`, `score_configs_get_by_id`, `score_configs_update`, `scores_get_many`, `scores_get_by_id`, `legacy_score_v1_create` |

### Key parameters
- Create/update endpoints take a `body` object; `datasets_get` /
  `datasets_get_runs` take `dataset_name`.
- `score_configs_create` `body`: `{name, dataType, minValue/maxValue or categories}`.
- Score write (`legacy_score_v1_create`) `body`: `{name, value, traceId,
  observationId?, dataType?, comment?}`.

## Recipes (`body` is a JSON object)
Create a dataset:
```
action=datasets_create body={"name":"qa-regression","description":"golden QA set"}
```
Read a dataset and its runs:
```
action=datasets_get dataset_name="qa-regression"
action=datasets_get_runs dataset_name="qa-regression" page=1 limit=50
```
Define a numeric score config:
```
action=score_configs_create body={"name":"helpfulness","dataType":"NUMERIC","minValue":0,"maxValue":1}
```
Write a score on a trace:
```
action=legacy_score_v1_create body={"name":"helpfulness","value":0.9,"traceId":"<trace_id>","dataType":"NUMERIC"}
```

## Gotchas
- Datasets are addressed by **name**, not id, on `datasets_get` /
  `datasets_get_runs` / `datasets_get_run`.
- Score `dataType` must match its config: `NUMERIC` uses `value`; `CATEGORICAL`
  /`BOOLEAN` use the string/`stringValue` variant — a mismatch is rejected.
- A score must target exactly one of a trace / observation / session; supplying a
  `traceId` (plus optional `observationId`) is the common path.
- Dataset run items link a dataset item to a produced trace/observation — create
  the trace first, then `dataset_run_items_create` referencing it.

## Related
- **Read side:** `langfuse-trace-analytics` reads scores back and runs metrics.
- **KG:** scores ingest as `:Score` nodes linked via `:scores` to their
  `:Trace`/`:Observation`/`:Session` (`langfuse_agent.ontology`).
- **Sibling skills:** `langfuse-trace-analytics`, `langfuse-prompt-management`.
