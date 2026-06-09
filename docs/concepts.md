# Concept Registry — langfuse-agent

> **Prefix**: `CONCEPT:LF-*`
> **Version**: 0.14.0
> **Bridge**: [`CONCEPT:ECO-4.0`](https://github.com/Knuckles-Team/agent-utilities/blob/main/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:LF-001` | Langfuse Datasets Operations | MCP tool domain `langfuse_datasets` — Action-routed dynamic tool registration |
| `CONCEPT:LF-002` | Langfuse Management Operations | MCP tool domain `langfuse_management` — Action-routed dynamic tool registration |
| `CONCEPT:LF-003` | Langfuse Observability Operations | MCP tool domain `langfuse_observability` — Action-routed dynamic tool registration |
| `CONCEPT:LF-004` | Langfuse Prompts Models Operations | MCP tool domain `langfuse_prompts_models` — Action-routed dynamic tool registration |

## Cross-Project References (from agent-utilities)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:ECO-4.0` | Unified Toolkit Ingestion | agent-utilities |
| `CONCEPT:ORCH-1.2` | Confidence-Gated Router | agent-utilities |
| `CONCEPT:OS-5.1` | Prompt Injection Defense | agent-utilities |
| `CONCEPT:OS-5.2` | Cognitive Scheduler | agent-utilities |
| `CONCEPT:OS-5.3` | Guardrail Engine | agent-utilities |
| `CONCEPT:OS-5.4` | Audit Logging | agent-utilities |
| `CONCEPT:KG-2.0` | Knowledge Graph Core | agent-utilities |

## Synergy with agent-utilities

This project integrates with `agent-utilities` via `CONCEPT:ECO-4.0` (Unified Toolkit Ingestion). The `langfuse_agent` MCP server registers its tools with the agent-utilities FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all LF-* concepts.
