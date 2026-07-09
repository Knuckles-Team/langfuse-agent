---
name: langfuse-prompt-management
skill_type: skill
description: >-
  Prompt registry and model definitions on Langfuse via the langfuse-agent MCP
  server — create, version, label, and fetch prompt templates, and manage the
  model/pricing definitions used to compute generation cost. Use when the agent
  must publish a new prompt version, resolve the production prompt for an app,
  promote a label, or register a model match-pattern with a unit price. Do NOT
  use for reading traces/generations (use langfuse-trace-analytics) or building
  eval datasets & scores (use langfuse-eval-datasets).
license: MIT
tags: [langfuse, prompts, models, registry, llm, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Langfuse Prompt Management

Domain-typed access to the Langfuse **prompt registry & model definitions**:
versioned prompt templates (with labels like `production`) and model/pricing
records that drive generation-cost calculation. Prefer the condensed
`langfuse_prompts_models` tool.

## When to use
- Create a new prompt or a new **version** of an existing prompt.
- Fetch a prompt by name (optionally a specific `version` or `label`).
- List prompts / promote a label (e.g. point `production` at a version).
- Register / list / read / delete **model** definitions (match pattern + unit
  price) used to attribute generation cost.

## When NOT to use
- Reading what prompts actually did in production (traces/generations) →
  `langfuse-trace-analytics`.
- Datasets, dataset runs, or scores → `langfuse-eval-datasets`.
- LLM-connection / project admin → the `langfuse_management` tool.

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
| `langfuse_prompts_models` | `prompts_list`, `prompts_get`, `prompts_create`, `prompts_delete`, `prompt_version_update`, `models_list`, `models_get`, `models_create`, `models_delete`, `llm_connections_list`, `llm_connections_upsert` |

### Key parameters
- `prompts_get`: `name` (required), optional `version` (int) or `label` (str).
- `prompts_create` / `prompts_delete` / `prompt_version_update`: take a `body`
  (and, for delete/version-update, the prompt `name`/version).
- `models_create` `body`: `{modelName, matchPattern, unit, inputPrice,
  outputPrice, …}`.

## Recipes
Fetch the production prompt for an app:
```
action=prompts_get name="support-agent" label="production"
```
Fetch a pinned version:
```
action=prompts_get name="support-agent" version=7
```
Create a new prompt version:
```
action=prompts_create body={"name":"support-agent","prompt":"You are…","labels":["production"],"type":"text"}
```
Register a model + pricing:
```
action=models_create body={"modelName":"gpt-4o","matchPattern":"(?i)^gpt-4o$","unit":"TOKENS","inputPrice":0.0000025,"outputPrice":0.00001}
```

## Gotchas
- Prompts are immutable per version: `prompts_create` on an existing name
  publishes a **new version**; you never edit a version in place.
- Labels (e.g. `production`, `latest`) are pointers — moving a label re-points
  which version resolves, it does not copy content.
- Resolve prompts by `label` in app code so a promotion rolls out without a
  redeploy; pin by `version` only for reproducible evals.
- Model `matchPattern` is a regex matched against the generation's model name;
  ordering/specificity of patterns determines which pricing wins.

## Related
- **Usage side:** `langfuse-trace-analytics` shows which prompt/model a
  generation used (`:usedPrompt` / `:usedModel`).
- **KG:** prompts and models federate as `:Prompt` / `:Model`
  (`langfuse_agent.ontology`).
- **Sibling skills:** `langfuse-trace-analytics`, `langfuse-eval-datasets`.
