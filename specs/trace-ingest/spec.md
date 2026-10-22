# CONN-LANGFUSE-AGENT-TRACE-INGEST — Trace, score and dataset ingest from Langfuse

Owner: langfuse-agent.

## Purpose and user stories

The engine learns from evaluated runs (EG-DECISION-ENGINE-R813). This connector imports traces, scores and datasets from Langfuse into the graph through the SDK source ingest.

## Requirements and acceptance

The rows are in [requirements.md](requirements.md).

## Why a new spec

The repository had no local spec. `kg_ingest.py` already ingests `:Trace` and `:Score`, but it drops score metadata and does not ingest dataset items.

## Scope and interfaces

In scope: the Langfuse records that the ingest maps, and the parity of its tool surface. Out of scope: the training example model (EG-DECISION-ENGINE-R813) and the SDK sync runner (SDK-SOURCE-INGEST-R004.20).
