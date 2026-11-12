# Concept Registry — langfuse-agent

> **Prefix**: `CONCEPT:LF-*`
> **Version**: 0.14.0
> **Bridge**: [`CONCEPT:AU-ECO.messaging.native-backend-abstraction`](https://github.com/Knuckles-Team/scion-sdk/blob/main/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:LF-OS.governance.lf` | Langfuse Datasets Operations | Typed dataset, dataset item, dataset run and annotation queue tools (`langfuse_datasets_*`, `langfuse_dataset_items_*`) |
| `CONCEPT:LF-OS.governance.lf-2` | Langfuse Management Operations | Typed project, organization, SCIM and storage tools (`langfuse_projects_*`, `langfuse_organizations_*`, `langfuse_scim_*`) |
| `CONCEPT:LF-OS.governance.lf-3` | Langfuse Observability Operations | Typed trace, observation, session, score and metrics tools (`langfuse_trace_*`, `langfuse_scores_*`) and `langfuse_runtime_posture` |
| `CONCEPT:LF-OS.governance.lf-4` | Langfuse Prompts Models Operations | Typed prompt, model and LLM connection tools (`langfuse_prompts_*`, `langfuse_models_*`) |

## Cross-Project References (from scion-sdk)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:AU-ECO.messaging.native-backend-abstraction` | Unified Toolkit Ingestion | scion-sdk |
| `CONCEPT:AU-ORCH.adapter.hot-cache-invalidation` | Confidence-Gated Router | scion-sdk |
| `CONCEPT:AU-OS.config.secrets-authentication` | Prompt Injection Defense | scion-sdk |
| `CONCEPT:AU-OS.state.cognitive-scheduler-preemption` | Cognitive Scheduler | scion-sdk |
| `CONCEPT:AU-OS.governance.reactive-multi-axis-budget` | Guardrail Engine | scion-sdk |
| `CONCEPT:AU-OS.governance.wasm-micro-agent-sandbox` | Audit Logging | scion-sdk |
| `CONCEPT:AU-KG.query.object-graph-mapper` | Knowledge Graph Core | scion-sdk |

## Synergy with scion-sdk

This project integrates with `scion-sdk` via `CONCEPT:AU-ECO.messaging.native-backend-abstraction` (Unified Toolkit Ingestion). The `langfuse_agent` MCP server registers its tools with the scion-sdk FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all LF-* concepts.
