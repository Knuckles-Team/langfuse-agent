# CONN-LANGFUSE-AGENT-TRACE-INGEST — Trace, score and dataset ingest from Langfuse

Owner: langfuse-agent.

## Purpose and user stories

The engine learns from evaluated runs (MEDULLA-DECISION-ENGINE-R813). This connector imports traces, scores and datasets from Langfuse into the graph through the SDK source ingest.

## Why a new spec

The repository had no local spec. `kg_ingest.py` already ingests `:Trace` and `:Score`, but it drops score metadata and does not ingest dataset items.

## Scope and interfaces

In scope: the Langfuse records that the ingest maps, and the parity of its tool surface. Out of scope: the training example model (MEDULLA-DECISION-ENGINE-R813) and the SDK sync runner (SCION-SOURCE-INGEST-R004.20).

## User Scenarios & Testing

### User Story 1 - Trace, score and dataset ingest from Langfuse (Priority: P1)

The engine learns from evaluated runs (MEDULLA-DECISION-ENGINE-R813). This connector imports traces, scores and datasets from Langfuse into the graph through the SDK source ingest.

**Acceptance Scenarios**:

1. **Given** the connector is configured, **When** the behaviour of row `CONN-LANGFUSE-AGENT-TRACE-INGEST-R001` (score metadata is kept) is exercised, **Then** `tests/test_kg_ingest.py::test_score_metadata_is_kept` maps one score per source kind and one unknown kind.
2. **Given** the connector is configured, **When** the behaviour of row `CONN-LANGFUSE-AGENT-TRACE-INGEST-R002` (datasets and dataset runs are ingested) is exercised, **Then** `tests/test_kg_ingest.py::test_dataset_items_and_runs_link` asserts both node kinds and both links.
3. **Given** the connector is configured, **When** the behaviour of row `CONN-LANGFUSE-AGENT-TRACE-INGEST-R003` (hot-path proof) is exercised, **Then** `tests/test_trace_ingest_served.py::test_scores_and_datasets_reach_the_engine` passes.

### Edge Cases

- If `CONN-LANGFUSE-AGENT-TRACE-INGEST-R001` is not met, its proving test fails: score metadata is kept.
- If `CONN-LANGFUSE-AGENT-TRACE-INGEST-R002` is not met, its proving test fails: datasets and dataset runs are ingested.
- If `CONN-LANGFUSE-AGENT-TRACE-INGEST-R003` is not met, its proving test fails: hot-path proof.

## Requirements

- **FR-001**: Score metadata is kept. Rows: `CONN-LANGFUSE-AGENT-TRACE-INGEST-R001`.
- **FR-002**: Datasets and dataset runs are ingested. Rows: `CONN-LANGFUSE-AGENT-TRACE-INGEST-R002`.
- **FR-003**: Hot-path proof. Rows: `CONN-LANGFUSE-AGENT-TRACE-INGEST-R003`.
- **FR-004**: Action-dispatch tools split. Rows: `CONN-LANGFUSE-AGENT-TRACE-INGEST-R004`.
- **FR-005**: Fleet name. Rows: `CONN-LANGFUSE-AGENT-TRACE-INGEST-R005`.
- **FR-006**: Score properties for evaluation corpora. Rows: `CONN-LANGFUSE-AGENT-TRACE-INGEST-R006`.

## Success Criteria

- **SC-001**: `tests/test_kg_ingest.py::test_score_metadata_is_kept` maps one score per source kind and one unknown kind. Rows: `CONN-LANGFUSE-AGENT-TRACE-INGEST-R001`.
- **SC-002**: `tests/test_kg_ingest.py::test_dataset_items_and_runs_link` asserts both node kinds and both links. Rows: `CONN-LANGFUSE-AGENT-TRACE-INGEST-R002`.
- **SC-003**: `tests/test_trace_ingest_served.py::test_scores_and_datasets_reach_the_engine` passes. Rows: `CONN-LANGFUSE-AGENT-TRACE-INGEST-R003`.
- **SC-004**: `tests/test_api_parity_gate.py` asserts no action-dispatch tool and no lost tool. Rows: `CONN-LANGFUSE-AGENT-TRACE-INGEST-R004`.
- **SC-005**: Every connector name in the package is `langfuse-mcp`. Rows: `CONN-LANGFUSE-AGENT-TRACE-INGEST-R005`.
- **SC-006**: A connector test maps one score per grader kind and asserts every property and the run link. Rows: `CONN-LANGFUSE-AGENT-TRACE-INGEST-R006`.

## Assumptions

- The external system is reachable with operator-supplied credentials.
- The SDK and engine contracts the rows cite are at the floors declared in `pyproject.toml`.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-LANGFUSE-AGENT-TRACE-INGEST-R001` | [plan.md](plan.md) | T-001 | [test-spec.md](test-spec.md) |
| FR-002 | `CONN-LANGFUSE-AGENT-TRACE-INGEST-R002` | [plan.md](plan.md) | T-002 | [test-spec.md](test-spec.md) |
| FR-003 | `CONN-LANGFUSE-AGENT-TRACE-INGEST-R003` | [plan.md](plan.md) | T-003 | [test-spec.md](test-spec.md) |
| FR-004 | `CONN-LANGFUSE-AGENT-TRACE-INGEST-R004` | [plan.md](plan.md) | T-004 | [test-spec.md](test-spec.md) |
| FR-005 | `CONN-LANGFUSE-AGENT-TRACE-INGEST-R005` | [plan.md](plan.md) | T-005 | [test-spec.md](test-spec.md) |
| FR-006 | `CONN-LANGFUSE-AGENT-TRACE-INGEST-R006` | [plan.md](plan.md) | T-006 | [test-spec.md](test-spec.md) |
