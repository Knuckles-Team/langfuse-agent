# CONN-LANGFUSE-AGENT-TRACE-INGEST — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Expected observation |
|---|---|---|
| T-R001 | CONN-LANGFUSE-AGENT-TRACE-INGEST-R001 | `tests/test_kg_ingest.py::test_score_metadata_is_kept` maps one score per source kind and one unknown kind. |
| T-R002 | CONN-LANGFUSE-AGENT-TRACE-INGEST-R002 | `tests/test_kg_ingest.py::test_dataset_items_and_runs_link` asserts both node kinds and both links. |
| T-R003 | CONN-LANGFUSE-AGENT-TRACE-INGEST-R003 | `tests/test_trace_ingest_served.py::test_scores_and_datasets_reach_the_engine` passes. |
| T-R004 | CONN-LANGFUSE-AGENT-TRACE-INGEST-R004 | `tests/test_api_parity_gate.py` asserts no action-dispatch tool and no lost tool. |
