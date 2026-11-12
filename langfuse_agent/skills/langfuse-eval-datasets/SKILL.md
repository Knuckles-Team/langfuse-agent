---
name: langfuse-eval-datasets
skill_type: skill
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
  author: Knuckles-Team
  version: '0.1.0'
---
# Langfuse Eval Datasets

Domain-typed access to the Langfuse **datasets & scoring** surface: datasets,
dataset items, dataset runs, score configs and scores. Use these to curate test
sets and grade LLM output. Use the dataset, score and annotation-queue tools.

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

## Tools
One typed tool per operation; pass each argument by name.

| Area | Tools |
|------|-------|
| Datasets | `langfuse_datasets_list`, `langfuse_datasets_create`, `langfuse_datasets_get` |
| Dataset items | `langfuse_dataset_items_create`, `langfuse_dataset_items_list`, `langfuse_dataset_items_get`, `langfuse_dataset_items_delete` |
| Runs | `langfuse_dataset_run_items_create`, `langfuse_dataset_run_items_list`, `langfuse_datasets_get_runs`, `langfuse_datasets_get_run`, `langfuse_datasets_delete_run` |
| Score configs | `langfuse_score_configs_create`, `langfuse_score_configs_get`, `langfuse_score_configs_get_by_id`, `langfuse_score_configs_update` |
| Scores | `langfuse_scores_create`, `langfuse_scores_get_many` |
| Annotation queues | `langfuse_annotation_queues_list_queues`, `langfuse_annotation_queues_create_queue`, `langfuse_annotation_queues_get_queue`, `langfuse_annotation_queues_list_queue_items`, `langfuse_annotation_queues_create_queue_item`, `langfuse_annotation_queues_get_queue_item`, `langfuse_annotation_queues_update_queue_item`, `langfuse_annotation_queues_delete_queue_item`, `langfuse_annotation_queues_create_queue_assignment`, `langfuse_annotation_queues_delete_queue_assignment` |

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
