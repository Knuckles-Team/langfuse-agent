"""Observability tools registration for langfuse-agent.

CONCEPT:LA_1.0 — Langfuse MCP Integration
"""

from typing import Any

from fastmcp import FastMCP
from pydantic import Field

from langfuse_agent.auth import get_client
from langfuse_agent.kg_ingest import auto_ingest
from langfuse_agent.runtime_posture import observability_runtime_posture

# Every action name below (aside from the client-less "runtime_posture",
# handled as its own special case before this table is consulted) is
# identical to the client method it dispatches to; the tuple is the exact,
# order-independent set of kwargs that branch used to forward.
_ACTION_PARAMS: dict[str, tuple[str, ...]] = {
    "metrics_get": ("query",),
    "observations_get_many": (
        "fields",
        "expand_metadata",
        "limit",
        "cursor",
        "parse_io_as_json",
        "name",
        "user_id",
        "type",
        "trace_id",
        "level",
        "parent_observation_id",
        "environment",
        "from_start_time",
        "to_start_time",
        "version",
        "filter",
    ),
    "opentelemetry_export_traces": ("resource_spans",),
    "score_configs_create": ("body",),
    "score_configs_get": ("page", "limit"),
    "score_configs_get_by_id": ("config_id",),
    "score_configs_update": ("config_id", "body"),
    "scores_create": ("body",),
    "scores_get_many": (
        "limit",
        "cursor",
        "id",
        "name",
        "from_timestamp",
        "to_timestamp",
        "environment",
        "source",
        "value",
        "value_min",
        "value_max",
        "config_id",
        "session_id",
        "experiment_id",
        "trace_id",
        "observation_id",
        "queue_id",
        "author_user_id",
        "data_type",
        "fields",
    ),
    "sessions_list": ("page", "limit", "from_timestamp", "to_timestamp", "environment"),
    "sessions_get": ("session_id",),
    "trace_get": ("trace_id",),
    "trace_delete": ("trace_id",),
    "trace_list": (
        "page",
        "limit",
        "user_id",
        "name",
        "session_id",
        "from_timestamp",
        "to_timestamp",
        "order_by",
        "tags",
        "version",
        "release",
        "environment",
        "fields",
        "filter",
    ),
    "trace_delete_multiple": ("trace_ids",),
}

# Actions whose result is fed to the default-on KG ingestion pipeline after
# the client call (same as each former branch's trailing auto_ingest call).
_AUTO_INGEST_ACTIONS = frozenset(
    {
        "observations_get_many",
        "scores_get_many",
        "sessions_list",
        "trace_get",
        "trace_list",
    }
)


def register_langfuse_observability_tools(mcp: FastMCP):
    """Register all observability-related tools.

    CONCEPT:LA_1.0 — Langfuse MCP Integration
    """

    @mcp.tool(tags={"langfuse"})
    async def langfuse_observability(
        action: str = Field(
            description="Action to perform. Must be one of: runtime_posture, metrics_get, observations_get_many, opentelemetry_export_traces, score_configs_create, score_configs_get, score_configs_get_by_id, score_configs_update, scores_create, scores_get_many, sessions_list, sessions_get, trace_get, trace_delete, trace_list, trace_delete_multiple"
        ),
        author_user_id: Any = Field(default=None, description="author user id"),
        body: Any = Field(default=None, description="body"),
        config_id: Any = Field(default=None, description="config id"),
        cursor: Any = Field(default=None, description="cursor"),
        data_type: Any = Field(default=None, description="data type"),
        environment: Any = Field(default=None, description="environment"),
        experiment_id: Any = Field(default=None, description="experiment id"),
        expand_metadata: Any = Field(default=None, description="expand metadata"),
        fields: Any = Field(default=None, description="fields"),
        filter: Any = Field(default=None, description="filter"),
        from_start_time: Any = Field(default=None, description="from start time"),
        from_timestamp: Any = Field(default=None, description="from timestamp"),
        level: Any = Field(default=None, description="level"),
        limit: Any = Field(default=None, description="limit"),
        id: Any = Field(default=None, description="score id filter"),
        name: Any = Field(default=None, description="name"),
        observation_id: Any = Field(default=None, description="observation id"),
        order_by: Any = Field(default=None, description="order by"),
        page: Any = Field(default=None, description="page"),
        parent_observation_id: Any = Field(
            default=None, description="parent observation id"
        ),
        parse_io_as_json: Any = Field(default=None, description="parse io as json"),
        query: Any = Field(default=None, description="query"),
        queue_id: Any = Field(default=None, description="queue id"),
        release: Any = Field(default=None, description="release"),
        resource_spans: Any = Field(default=None, description="resource spans"),
        session_id: Any = Field(default=None, description="session id"),
        source: Any = Field(default=None, description="source"),
        tags: Any = Field(default=None, description="tags"),
        to_start_time: Any = Field(default=None, description="to start time"),
        to_timestamp: Any = Field(default=None, description="to timestamp"),
        trace_id: Any = Field(default=None, description="trace id"),
        trace_ids: Any = Field(default=None, description="trace ids"),
        type: Any = Field(default=None, description="type"),
        user_id: Any = Field(default=None, description="user id"),
        value: Any = Field(default=None, description="value"),
        value_max: Any = Field(default=None, description="maximum numeric score value"),
        value_min: Any = Field(default=None, description="minimum numeric score value"),
        version: Any = Field(default=None, description="version"),
    ) -> Any:
        """Perform langfuse_observability operations."""
        if action == "runtime_posture":
            return observability_runtime_posture()
        client = get_client()

        # Same insertion order as the original if-chain, so the assembled
        # kwargs dict (and therefore any downstream filtered subset) is
        # identical to before.
        candidates = (
            ("author_user_id", author_user_id),
            ("body", body),
            ("config_id", config_id),
            ("cursor", cursor),
            ("data_type", data_type),
            ("environment", environment),
            ("experiment_id", experiment_id),
            ("expand_metadata", expand_metadata),
            ("fields", fields),
            ("filter", filter),
            ("from_start_time", from_start_time),
            ("from_timestamp", from_timestamp),
            ("level", level),
            ("limit", limit),
            ("id", id),
            ("name", name),
            ("observation_id", observation_id),
            ("order_by", order_by),
            ("page", page),
            ("parent_observation_id", parent_observation_id),
            ("parse_io_as_json", parse_io_as_json),
            ("query", query),
            ("queue_id", queue_id),
            ("release", release),
            ("resource_spans", resource_spans),
            ("session_id", session_id),
            ("source", source),
            ("tags", tags),
            ("to_start_time", to_start_time),
            ("to_timestamp", to_timestamp),
            ("trace_id", trace_id),
            ("trace_ids", trace_ids),
            ("type", type),
            ("user_id", user_id),
            ("value", value),
            ("value_max", value_max),
            ("value_min", value_min),
            ("version", version),
        )
        kwargs = {k: v for k, v in candidates if v is not None}

        if action not in _ACTION_PARAMS:
            raise ValueError(f"Unknown action: {action}")
        method_kwargs = {k: v for k, v in kwargs.items() if k in _ACTION_PARAMS[action]}
        result = getattr(client, action)(**method_kwargs)
        if action in _AUTO_INGEST_ACTIONS:
            auto_ingest(action, result)  # default-on KG ingestion
        return result
