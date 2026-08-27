"""Datasets tools registration for langfuse-agent.

CONCEPT:LA_1.0 — Langfuse MCP Integration
"""

from typing import Any

from fastmcp import FastMCP
from pydantic import Field

from langfuse_agent.auth import get_client

# Every action name below is identical to the client method it dispatches to
# (verified against the elif chain this table replaced); the tuple is the
# exact, order-independent set of kwargs that branch used to forward.
_ACTION_PARAMS: dict[str, tuple[str, ...]] = {
    "annotation_queues_list_queues": ("page", "limit"),
    "annotation_queues_create_queue": ("body",),
    "annotation_queues_get_queue": ("queue_id",),
    "annotation_queues_list_queue_items": ("queue_id", "status", "page", "limit"),
    "annotation_queues_create_queue_item": ("queue_id", "body"),
    "annotation_queues_get_queue_item": ("queue_id", "item_id"),
    "annotation_queues_update_queue_item": ("queue_id", "item_id", "body"),
    "annotation_queues_delete_queue_item": ("queue_id", "item_id"),
    "annotation_queues_create_queue_assignment": ("queue_id", "body"),
    "annotation_queues_delete_queue_assignment": ("queue_id", "body"),
    "dataset_items_create": ("body",),
    "dataset_items_list": (
        "dataset_name",
        "source_trace_id",
        "source_observation_id",
        "version",
        "page",
        "limit",
    ),
    "dataset_items_get": ("id",),
    "dataset_items_delete": ("id",),
    "dataset_run_items_create": ("body",),
    "dataset_run_items_list": ("dataset_id", "run_name", "page", "limit"),
    "datasets_list": ("page", "limit"),
    "datasets_create": ("body",),
    "datasets_get": ("dataset_name",),
    "datasets_get_run": ("dataset_name", "run_name"),
    "datasets_delete_run": ("dataset_name", "run_name"),
    "datasets_get_runs": ("dataset_name", "page", "limit"),
}


def register_langfuse_datasets_tools(mcp: FastMCP):
    """Register all dataset-related tools.

    CONCEPT:LA_1.0 — Langfuse MCP Integration
    """

    @mcp.tool(tags={"langfuse"})
    async def langfuse_datasets(
        action: str = Field(
            description="Action to perform. Must be one of: annotation_queues_list_queues, annotation_queues_create_queue, annotation_queues_get_queue, annotation_queues_list_queue_items, annotation_queues_create_queue_item, annotation_queues_get_queue_item, annotation_queues_update_queue_item, annotation_queues_delete_queue_item, annotation_queues_create_queue_assignment, annotation_queues_delete_queue_assignment, dataset_items_create, dataset_items_list, dataset_items_get, dataset_items_delete, dataset_run_items_create, dataset_run_items_list, datasets_list, datasets_create, datasets_get, datasets_get_run, datasets_delete_run, datasets_get_runs"
        ),
        body: Any = Field(default=None, description="body"),
        dataset_id: Any = Field(default=None, description="dataset id"),
        dataset_name: Any = Field(default=None, description="dataset name"),
        id: Any = Field(default=None, description="id"),
        item_id: Any = Field(default=None, description="item id"),
        limit: Any = Field(default=None, description="limit"),
        page: Any = Field(default=None, description="page"),
        queue_id: Any = Field(default=None, description="queue id"),
        run_name: Any = Field(default=None, description="run name"),
        source_observation_id: Any = Field(
            default=None, description="source observation id"
        ),
        source_trace_id: Any = Field(default=None, description="source trace id"),
        status: Any = Field(default=None, description="status"),
        version: Any = Field(default=None, description="version"),
    ) -> Any:
        """Perform langfuse_datasets operations."""
        client = get_client()

        # Same insertion order as the original if-chain, so the assembled
        # kwargs dict (and therefore any downstream filtered subset) is
        # identical to before.
        candidates = (
            ("body", body),
            ("dataset_id", dataset_id),
            ("dataset_name", dataset_name),
            ("id", id),
            ("item_id", item_id),
            ("limit", limit),
            ("page", page),
            ("queue_id", queue_id),
            ("run_name", run_name),
            ("source_observation_id", source_observation_id),
            ("source_trace_id", source_trace_id),
            ("status", status),
            ("version", version),
        )
        kwargs = {k: v for k, v in candidates if v is not None}

        if action not in _ACTION_PARAMS:
            raise ValueError(f"Unknown action: {action}")
        method_kwargs = {k: v for k, v in kwargs.items() if k in _ACTION_PARAMS[action]}
        return getattr(client, action)(**method_kwargs)
