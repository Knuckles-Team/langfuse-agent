# CONN-LANGFUSE-AGENT-TRACE-INGEST — Implementation plan

Governing spec: [spec.md](spec.md). Rows: [requirements.md](requirements.md).

## Summary

This plan delivers trace, score and dataset ingest from langfuse for the connector, reusing the SDK for shared capabilities.

## Technical Context

- **Language/Version**: Python 3.14 (floor 3.12)
- **Primary Dependencies**: scion-sdk, fastmcp
- **Storage**: N/A; the connector stores nothing
- **Testing**: pytest; the proof level each row names
- **Target Platform**: Linux containers
- **Project Type**: connector (MCP server)
- **Performance Goals**: N/A
- **Constraints**: one tool per API operation; shared capabilities come from the SDK
- **Scale/Scope**: 6 rows

## Constitution Check

- One owner per concept: pass. The connector owns one external system's calls, mappings and tools only.
- Connectors depend on the SDK and are called through arbora: pass.
- No ratchets: pass. The rows add no suppression.

## Project Structure

```text
langfuse_agent/kg_ingest.py  existing
langfuse_agent/tools/kg.py  existing
langfuse_agent/tools/datasets.py  existing
langfuse_agent/connector_sources.py  existing
langfuse_agent/mcp_server.py  existing
langfuse_agent/__init__.py  existing
tests/test_api_parity_gate.py  existing
pyproject.toml  existing
tests/test_fleet_name.py  existing
langfuse_agent/tools/observability.py  existing
langfuse_agent/ontology/langfuse.ttl  existing
```

## Phase 0: Research

No unknowns. Each row names the code it touches.

## Phase 1: Design

The rows are delivered in place; the design is the caller chain below.

## Phase 2: Task approach

`tasks.md` holds one task line per row, producer first.

## Complexity Tracking

None. The constitution check passed.

## Build contract

The repository pre-commit hooks apply: `ruff-format`, `connector-standard`, `secrets`, `tests-fast`. Each row names its proving test. No suppression and no duplicate implementation.

## Production caller chain

1. `CONN-LANGFUSE-AGENT-TRACE-INGEST-R001`: the typed `langfuse_scores_get_many` tool, whose result the platform ingests through `ingest_read_result` (`langfuse_agent/kg_ingest.py`) -> `_INGEST_BY_ACTION["scores_get_many"]` -> `ingest_scores` (line 581); `langfuse_ingest` in `langfuse_agent/tools/kg.py` also calls it.
2. `CONN-LANGFUSE-AGENT-TRACE-INGEST-R002`: (planned) `langfuse_ingest` tool (`langfuse_agent/tools/kg.py::register_langfuse_kg_tools`, line 34) -> `_INGESTERS` map (line 25) -> new dataset and run-item ingesters in `langfuse_agent/kg_ingest.py`; no `:DatasetItem` or `:DatasetRunItem` mapping exists today.
3. `CONN-LANGFUSE-AGENT-TRACE-INGEST-R003`: (planned) the served SDK source sync (SCION-SOURCE-INGEST-R004.20) -> sources declared in `langfuse_agent/connector_sources.py::SOURCES` -> the connector served from `langfuse_agent:connector`; the dataset sources and the served sync test do not exist yet.
4. `CONN-LANGFUSE-AGENT-TRACE-INGEST-R004`: arbora `fleet.call` -> the typed tools that `Connector(api=LangfuseApi, ...)` in `langfuse_agent/__init__.py` serves, one per `LangfuseApi` method, plus the hand-written `langfuse_ingest` and `langfuse_runtime_posture` of `langfuse_agent/tools/`.
5. `CONN-LANGFUSE-AGENT-TRACE-INGEST-R005`: the `langfuse-mcp` entry point in `pyproject.toml` -> `langfuse_agent/__init__.py::connector` -> `IngestBinding(connector="langfuse-mcp", ...)` in `langfuse_agent/kg_ingest.py` (line 319) and `source_meta(server="langfuse-mcp")` in `langfuse_agent/connector_sources.py`.
6. `CONN-LANGFUSE-AGENT-TRACE-INGEST-R006`: the typed `langfuse_scores_get_many` tool -> `ingest_read_result` (`langfuse_agent/kg_ingest.py`) -> `ingest_scores`, which builds the `:Score` node and the `scores` relationship today; `scoresRun`, `grader_kind` and `split` are not mapped yet.

## Cross-repo seams

none. The cited owner rows are library capabilities the connector calls in process; spec.md names them.
