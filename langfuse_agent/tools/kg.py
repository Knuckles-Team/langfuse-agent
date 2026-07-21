"""Native knowledge-graph ingestion tools for langfuse-agent (Wire-First surface).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. Exposes an explicit MCP tool that lists
Langfuse observability records via the real client and natively pushes them into the ONE
epistemic-graph knowledge graph as typed OWL nodes (:Trace / :Observation / :Generation /
:Session / :Score). Best-effort: returns ``{"ingested": None}`` when no engine is reachable.
"""

from typing import Any

from agent_utilities.mcp.action_dispatch import parse_json_object
from fastmcp import FastMCP
from pydantic import Field

from langfuse_agent.auth import get_client
from langfuse_agent.kg_ingest import (
    _records,
    ingest_observations,
    ingest_scores,
    ingest_sessions,
    ingest_traces,
)

_INGESTERS = {
    "traces": (ingest_traces, "trace_list"),
    "observations": (ingest_observations, "observations_get_many"),
    "sessions": (ingest_sessions, "sessions_list"),
    "scores": (ingest_scores, "scores_get_many"),
}


def register_langfuse_kg_tools(mcp: FastMCP):
    """Register native KG ingestion tools.

    CONCEPT:AU-KG.ingest.enterprise-source-extractor.
    """

    @mcp.tool(tags={"langfuse"})
    async def langfuse_ingest(
        kind: str = Field(
            default="traces",
            description="Record kind to ingest: traces, observations, sessions, scores.",
        ),
        limit: int = Field(default=50, description="Max records to list and ingest."),
        params_json: str = Field(
            default="{}",
            description="JSON string of extra list filters passed to the client method.",
        ),
    ) -> Any:
        """Natively ingest Langfuse records into epistemic-graph as typed nodes.

        Lists records of ``kind`` via the langfuse client and pushes them (with their
        :Session/:Person/:Trace/:Model links) into the knowledge graph via the fast
        engine client. Best-effort: ``{"ingested": None}`` when no engine is reachable.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        if kind not in _INGESTERS:
            raise ValueError(f"Unknown kind. Expected one of: {sorted(_INGESTERS)}.")
        ingest_fn, _ = _INGESTERS[kind]
        kwargs = parse_json_object(params_json)
        kwargs.setdefault("limit", limit)
        client = get_client()

        method = {
            "traces": client.trace_list,
            "observations": client.observations_get_many,
            "sessions": client.sessions_list,
            "scores": client.scores_get_many,
        }[kind]
        resp = method(**kwargs)
        records = _records(resp)
        result = ingest_fn(records)
        return {"kind": kind, "listed": len(records), "ingested": result}

    return None
