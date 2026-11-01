# CONN-LANGFUSE-AGENT-TRACE-INGEST — Data model

Entities, classes and tables this spec adds, one section per row.

## CONN-LANGFUSE-AGENT-TRACE-INGEST-R002

Row title: Datasets and dataset runs are ingested.

Definition from the row: Datasets and dataset runs are ingested. The ingest must map dataset items to `:DatasetItem` nodes and dataset-run items to `:DatasetRunItem` nodes. A run item must link its dataset item and its trace. Caller chain: (planned) `langfuse_ingest` tool (`langfuse_agent/tools/kg.py::register_langfuse_kg_t.
