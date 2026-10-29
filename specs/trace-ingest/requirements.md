# CONN-LANGFUSE-AGENT-TRACE-INGEST — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. The generator sets each row's state in `status.json`.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-LANGFUSE-AGENT-TRACE-INGEST-R001` | **Score metadata is kept.** `ingest_scores` in `langfuse_agent/kg_ingest.py` must keep the score name, the source kind, the comment and the author. The source kind is a closed set: `annotation`, `model_judge` and `api`. A record with an unknown source kind must refuse with `SCORE_SOURCE_UNKNOWN`. | `tests/test_kg_ingest.py::test_score_metadata_is_kept` maps one score per source kind and one unknown kind. |
| `CONN-LANGFUSE-AGENT-TRACE-INGEST-R002` | **Datasets and dataset runs are ingested.** The ingest must map dataset items to `:DatasetItem` nodes and dataset-run items to `:DatasetRunItem` nodes. A run item must link its dataset item and its trace. | `tests/test_kg_ingest.py::test_dataset_items_and_runs_link` asserts both node kinds and both links. |
| `CONN-LANGFUSE-AGENT-TRACE-INGEST-R003` | **Hot-path proof.** The entry point is the served SDK source sync of SCION-SOURCE-INGEST-R004.20 against a real engine. The test ingests two traces, three scores and one dataset run. The engine then builds one training corpus, per MEDULLA-DECISION-ENGINE-R813.6. | `tests/test_trace_ingest_served.py::test_scores_and_datasets_reach_the_engine` passes. |
| `CONN-LANGFUSE-AGENT-TRACE-INGEST-R004` | **Action-dispatch tools split.** The three action-dispatch tools must split into one tool per action, per SCION-CONNECTOR-CONTROL-R020.3. Every predecessor tool must stay kept, split or covered, per SCION-CONNECTOR-CONTROL-R020.4. | `tests/test_api_parity_gate.py` asserts no action-dispatch tool and no lost tool. |
| `CONN-LANGFUSE-AGENT-TRACE-INGEST-R005` | **Fleet name.** `pyproject.toml` declares `langfuse-mcp` as the single `agent_connector_sdk.connector` entry point. The content pack, the manifest `connector`, the fingerprints and the ingest binding all carry `langfuse-mcp`. Proving test: `tests/test_fleet_name.py::test_connector_name_is_the_fleet_name`. | Every connector name in the package is `langfuse-mcp`. |
