---
name: langfuse-prompt-management
skill_type: skill
description: >-
  Langfuse prompt registry and model definitions via the langfuse-agent MCP server: create, version, label and fetch prompts, manage model pricing. Use to publish a prompt version or promote a label. Do NOT use for traces (langfuse-trace-analytics) or datasets and scores (langfuse-eval-datasets).
license: MIT
tags: [langfuse, prompts, models, registry, llm, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---
# Langfuse Prompt Management

Scope: Prompt registry and model definitions on Langfuse via the langfuse-agent MCP server — create, version, label, and fetch prompt templates, and manage the model/pricing definitions used to compute generation cost. Use when the agent must publish a new prompt version, resolve the production prompt for an app, promote a label, or register a model match-pattern with a unit price. Do NOT use for reading traces/generations (use langfuse-trace-analytics) or building eval datasets and scores (use langfuse-eval-datasets).

Domain-typed access to the Langfuse **prompt registry & model definitions**:
versioned prompt templates (with labels like `production`) and model/pricing
records that drive generation-cost calculation. Use the typed prompt, model and
LLM-connection tools.

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
- LLM-connection / project admin → the project, organization and SCIM tools of `langfuse-agent-operations`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`langfuse-agent`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `LANGFUSE_PUBLIC_KEY` | ✅ | Project public key (`pk-lf-…`) |
| `LANGFUSE_SECRET_KEY` | ✅ | Project secret key (`sk-lf-…`) |
| `LANGFUSE_HOST` | optional | Base URL (defaults to Langfuse Cloud) |

## Steps

1. List existing prompts with `langfuse_prompts_list`. Verify whether the prompt name already exists before creating anything.
2. Read the current prompt with `langfuse_prompts_get` (`name`, plus `label` or `version`). Verify the returned version and labels are what you expect.
3. Publish a new version with `langfuse_prompts_create` (`body` with name, prompt, type, labels). Verify a follow-up `langfuse_prompts_get` returns the incremented version.
4. Move a label such as `production` with `langfuse_prompt_version_update`. Verify `langfuse_prompts_get` with `label="production"` resolves to the target version.
5. Register pricing for a model with `langfuse_models_create` (`body` with `modelName`, `matchPattern`, `unit`, prices). Verify `langfuse_models_list` shows the new entry.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| Prompt not found | Wrong `name`, or the label or version does not exist | Call `langfuse_prompts_list` for exact names, then re-read with a valid `label` or `version`. |
| Label resolves to the wrong version | The label pointer was not moved | Call `langfuse_prompt_version_update` for the intended version and confirm with `langfuse_prompts_get` using `label`. |
| Model pricing not applied | `matchPattern` regex does not match the generation's model name | Fix the regex, recreate with `langfuse_models_create`, and remove the bad entry with `langfuse_models_delete`. |

## Tools
One typed tool per operation; pass each argument by name.

| Area | Tools |
|------|-------|
| Prompts | `langfuse_prompts_list`, `langfuse_prompts_get`, `langfuse_prompts_create`, `langfuse_prompts_delete`, `langfuse_prompt_version_update` |
| Models | `langfuse_models_list`, `langfuse_models_get`, `langfuse_models_create`, `langfuse_models_delete` |
| LLM connections | `langfuse_llm_connections_list`, `langfuse_llm_connections_upsert` |

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
