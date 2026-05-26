"""Observability tools registration for langfuse-agent.

CONCEPT:LA_1.0 — Langfuse MCP Integration
"""

from typing import Any

from fastmcp import FastMCP
from pydantic import Field

from langfuse_agent.auth import get_client


def register_langfuse_observability_tools(mcp: FastMCP):
    """Register all observability-related tools.

    CONCEPT:LA_1.0 — Langfuse MCP Integration
    """

    @mcp.tool(tags={"langfuse"})
    async def langfuse_observability(
        action: str = Field(
            description="Action to perform. Must be one of: legacy_metrics_v1_metrics, legacy_observations_v1_get, legacy_observations_v1_get_many, legacy_score_v1_create, legacy_score_v1_delete, metrics_metrics, observations_get_many, opentelemetry_export_traces, score_configs_create, score_configs_get, score_configs_get_by_id, score_configs_update, scores_get_many, scores_get_by_id, sessions_list, sessions_get, trace_get, trace_delete, trace_list, trace_delete_multiple, ingestion_batch"
        ),
        batch: Any = Field(default=None, description="batch"),
        body: Any = Field(default=None, description="body"),
        config_id: Any = Field(default=None, description="config id"),
        cursor: Any = Field(default=None, description="cursor"),
        data_type: Any = Field(default=None, description="data type"),
        dataset_run_id: Any = Field(default=None, description="dataset run id"),
        environment: Any = Field(default=None, description="environment"),
        expand_metadata: Any = Field(default=None, description="expand metadata"),
        fields: Any = Field(default=None, description="fields"),
        filter: Any = Field(default=None, description="filter"),
        from_start_time: Any = Field(default=None, description="from start time"),
        from_timestamp: Any = Field(default=None, description="from timestamp"),
        level: Any = Field(default=None, description="level"),
        limit: Any = Field(default=None, description="limit"),
        metadata: Any = Field(default=None, description="metadata"),
        name: Any = Field(default=None, description="name"),
        observation_id: Any = Field(default=None, description="observation id"),
        operator: Any = Field(default=None, description="operator"),
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
        score_id: Any = Field(default=None, description="score id"),
        score_ids: Any = Field(default=None, description="score ids"),
        session_id: Any = Field(default=None, description="session id"),
        source: Any = Field(default=None, description="source"),
        tags: Any = Field(default=None, description="tags"),
        to_start_time: Any = Field(default=None, description="to start time"),
        to_timestamp: Any = Field(default=None, description="to timestamp"),
        trace_id: Any = Field(default=None, description="trace id"),
        trace_ids: Any = Field(default=None, description="trace ids"),
        trace_tags: Any = Field(default=None, description="trace tags"),
        type: Any = Field(default=None, description="type"),
        user_id: Any = Field(default=None, description="user id"),
        value: Any = Field(default=None, description="value"),
        version: Any = Field(default=None, description="version"),
    ) -> Any:
        """Perform langfuse_observability operations."""
        client = get_client()
        kwargs = {}
        if batch is not None:
            kwargs["batch"] = batch
        if body is not None:
            kwargs["body"] = body
        if config_id is not None:
            kwargs["config_id"] = config_id
        if cursor is not None:
            kwargs["cursor"] = cursor
        if data_type is not None:
            kwargs["data_type"] = data_type
        if dataset_run_id is not None:
            kwargs["dataset_run_id"] = dataset_run_id
        if environment is not None:
            kwargs["environment"] = environment
        if expand_metadata is not None:
            kwargs["expand_metadata"] = expand_metadata
        if fields is not None:
            kwargs["fields"] = fields
        if filter is not None:
            kwargs["filter"] = filter
        if from_start_time is not None:
            kwargs["from_start_time"] = from_start_time
        if from_timestamp is not None:
            kwargs["from_timestamp"] = from_timestamp
        if level is not None:
            kwargs["level"] = level
        if limit is not None:
            kwargs["limit"] = limit
        if metadata is not None:
            kwargs["metadata"] = metadata
        if name is not None:
            kwargs["name"] = name
        if observation_id is not None:
            kwargs["observation_id"] = observation_id
        if operator is not None:
            kwargs["operator"] = operator
        if order_by is not None:
            kwargs["order_by"] = order_by
        if page is not None:
            kwargs["page"] = page
        if parent_observation_id is not None:
            kwargs["parent_observation_id"] = parent_observation_id
        if parse_io_as_json is not None:
            kwargs["parse_io_as_json"] = parse_io_as_json
        if query is not None:
            kwargs["query"] = query
        if queue_id is not None:
            kwargs["queue_id"] = queue_id
        if release is not None:
            kwargs["release"] = release
        if resource_spans is not None:
            kwargs["resource_spans"] = resource_spans
        if score_id is not None:
            kwargs["score_id"] = score_id
        if score_ids is not None:
            kwargs["score_ids"] = score_ids
        if session_id is not None:
            kwargs["session_id"] = session_id
        if source is not None:
            kwargs["source"] = source
        if tags is not None:
            kwargs["tags"] = tags
        if to_start_time is not None:
            kwargs["to_start_time"] = to_start_time
        if to_timestamp is not None:
            kwargs["to_timestamp"] = to_timestamp
        if trace_id is not None:
            kwargs["trace_id"] = trace_id
        if trace_ids is not None:
            kwargs["trace_ids"] = trace_ids
        if trace_tags is not None:
            kwargs["trace_tags"] = trace_tags
        if type is not None:
            kwargs["type"] = type
        if user_id is not None:
            kwargs["user_id"] = user_id
        if value is not None:
            kwargs["value"] = value
        if version is not None:
            kwargs["version"] = version

        if action == "legacy_metrics_v1_metrics":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["query"]}
            return client.legacy_metrics_v1_metrics(**method_kwargs)
        elif action == "legacy_observations_v1_get":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["observation_id"]}
            return client.legacy_observations_v1_get(**method_kwargs)
        elif action == "legacy_observations_v1_get_many":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k
                in [
                    "page",
                    "limit",
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
                ]
            }
            return client.legacy_observations_v1_get_many(**method_kwargs)
        elif action == "legacy_score_v1_create":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["body"]}
            return client.legacy_score_v1_create(**method_kwargs)
        elif action == "legacy_score_v1_delete":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["score_id"]}
            return client.legacy_score_v1_delete(**method_kwargs)
        elif action == "metrics_metrics":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["query"]}
            return client.metrics_metrics(**method_kwargs)
        elif action == "observations_get_many":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k
                in [
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
                ]
            }
            return client.observations_get_many(**method_kwargs)
        elif action == "opentelemetry_export_traces":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["resource_spans"]}
            return client.opentelemetry_export_traces(**method_kwargs)
        elif action == "score_configs_create":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["body"]}
            return client.score_configs_create(**method_kwargs)
        elif action == "score_configs_get":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["page", "limit"]}
            return client.score_configs_get(**method_kwargs)
        elif action == "score_configs_get_by_id":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["config_id"]}
            return client.score_configs_get_by_id(**method_kwargs)
        elif action == "score_configs_update":
            method_kwargs = {
                k: v for k, v in kwargs.items() if k in ["config_id", "body"]
            }
            return client.score_configs_update(**method_kwargs)
        elif action == "scores_get_many":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k
                in [
                    "page",
                    "limit",
                    "user_id",
                    "name",
                    "from_timestamp",
                    "to_timestamp",
                    "environment",
                    "source",
                    "operator",
                    "value",
                    "score_ids",
                    "config_id",
                    "session_id",
                    "dataset_run_id",
                    "trace_id",
                    "observation_id",
                    "queue_id",
                    "data_type",
                    "trace_tags",
                    "fields",
                    "filter",
                ]
            }
            return client.scores_get_many(**method_kwargs)
        elif action == "scores_get_by_id":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["score_id"]}
            return client.scores_get_by_id(**method_kwargs)
        elif action == "sessions_list":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k
                in ["page", "limit", "from_timestamp", "to_timestamp", "environment"]
            }
            return client.sessions_list(**method_kwargs)
        elif action == "sessions_get":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["session_id"]}
            return client.sessions_get(**method_kwargs)
        elif action == "trace_get":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["trace_id"]}
            return client.trace_get(**method_kwargs)
        elif action == "trace_delete":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["trace_id"]}
            return client.trace_delete(**method_kwargs)
        elif action == "trace_list":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k
                in [
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
                ]
            }
            return client.trace_list(**method_kwargs)
        elif action == "trace_delete_multiple":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["trace_ids"]}
            return client.trace_delete_multiple(**method_kwargs)
        elif action == "ingestion_batch":
            method_kwargs = {
                k: v for k, v in kwargs.items() if k in ["batch", "metadata"]
            }
            return client.ingestion_batch(**method_kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")
