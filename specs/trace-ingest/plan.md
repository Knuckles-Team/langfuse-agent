# CONN-LANGFUSE-AGENT-TRACE-INGEST — Design and implementation plan

Governing spec: [spec.md](spec.md).

Component: Trace ingest
Code: ../../langfuse_agent/kg_ingest.py

`ingest_scores` in `langfuse_agent/kg_ingest.py` maps score records to `:Score` nodes with `belongsToTrace` links. This spec adds the score metadata and the dataset records. The engine turns each score into a training example with a grader kind.
