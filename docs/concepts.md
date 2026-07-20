# Concept Registry — langfuse-agent

> **Prefix**: `CONCEPT:LF-*`
> **Version**: 0.14.0
> **Bridge**: [`CONCEPT:AU-ECO.messaging.native-backend-abstraction`](https://github.com/Knuckles-Team/agent-utilities/blob/main/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:LF-OS.governance.lf` | Langfuse Datasets Operations | MCP tool domain `langfuse_datasets` — Action-routed dynamic tool registration |
| `CONCEPT:LF-OS.governance.lf-2` | Langfuse Management Operations | MCP tool domain `langfuse_management` — Action-routed dynamic tool registration |
| `CONCEPT:LF-OS.governance.lf-3` | Langfuse Observability Operations | MCP tool domain `langfuse_observability` — Action-routed dynamic tool registration |
| `CONCEPT:LF-OS.governance.lf-4` | Langfuse Prompts Models Operations | MCP tool domain `langfuse_prompts_models` — Action-routed dynamic tool registration |

## Cross-Project References (from agent-utilities)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:AU-ECO.messaging.native-backend-abstraction` | Unified Toolkit Ingestion | agent-utilities |
| `CONCEPT:AU-ORCH.adapter.hot-cache-invalidation` | Confidence-Gated Router | agent-utilities |
| `CONCEPT:AU-OS.config.secrets-authentication` | Prompt Injection Defense | agent-utilities |
| `CONCEPT:AU-OS.state.cognitive-scheduler-preemption` | Cognitive Scheduler | agent-utilities |
| `CONCEPT:AU-OS.governance.reactive-multi-axis-budget` | Guardrail Engine | agent-utilities |
| `CONCEPT:AU-OS.governance.wasm-micro-agent-sandbox` | Audit Logging | agent-utilities |
| `CONCEPT:AU-KG.query.object-graph-mapper` | Knowledge Graph Core | agent-utilities |

## Synergy with agent-utilities

This project integrates with `agent-utilities` via `CONCEPT:AU-ECO.messaging.native-backend-abstraction` (Unified Toolkit Ingestion). The `langfuse_agent` MCP server registers its tools with the agent-utilities FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all LF-* concepts.
