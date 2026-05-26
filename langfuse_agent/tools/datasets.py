"""Datasets tools registration for langfuse-agent.

CONCEPT:LA_1.0 — Langfuse MCP Integration
"""

from typing import Any

from fastmcp import FastMCP
from pydantic import Field

from langfuse_agent.auth import get_client


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
        kwargs = {}
        if body is not None:
            kwargs["body"] = body
        if dataset_id is not None:
            kwargs["dataset_id"] = dataset_id
        if dataset_name is not None:
            kwargs["dataset_name"] = dataset_name
        if id is not None:
            kwargs["id"] = id
        if item_id is not None:
            kwargs["item_id"] = item_id
        if limit is not None:
            kwargs["limit"] = limit
        if page is not None:
            kwargs["page"] = page
        if queue_id is not None:
            kwargs["queue_id"] = queue_id
        if run_name is not None:
            kwargs["run_name"] = run_name
        if source_observation_id is not None:
            kwargs["source_observation_id"] = source_observation_id
        if source_trace_id is not None:
            kwargs["source_trace_id"] = source_trace_id
        if status is not None:
            kwargs["status"] = status
        if version is not None:
            kwargs["version"] = version

        if action == "annotation_queues_list_queues":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["page", "limit"]}
            return client.annotation_queues_list_queues(**method_kwargs)
        elif action == "annotation_queues_create_queue":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["body"]}
            return client.annotation_queues_create_queue(**method_kwargs)
        elif action == "annotation_queues_get_queue":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["queue_id"]}
            return client.annotation_queues_get_queue(**method_kwargs)
        elif action == "annotation_queues_list_queue_items":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k in ["queue_id", "status", "page", "limit"]
            }
            return client.annotation_queues_list_queue_items(**method_kwargs)
        elif action == "annotation_queues_create_queue_item":
            method_kwargs = {
                k: v for k, v in kwargs.items() if k in ["queue_id", "body"]
            }
            return client.annotation_queues_create_queue_item(**method_kwargs)
        elif action == "annotation_queues_get_queue_item":
            method_kwargs = {
                k: v for k, v in kwargs.items() if k in ["queue_id", "item_id"]
            }
            return client.annotation_queues_get_queue_item(**method_kwargs)
        elif action == "annotation_queues_update_queue_item":
            method_kwargs = {
                k: v for k, v in kwargs.items() if k in ["queue_id", "item_id", "body"]
            }
            return client.annotation_queues_update_queue_item(**method_kwargs)
        elif action == "annotation_queues_delete_queue_item":
            method_kwargs = {
                k: v for k, v in kwargs.items() if k in ["queue_id", "item_id"]
            }
            return client.annotation_queues_delete_queue_item(**method_kwargs)
        elif action == "annotation_queues_create_queue_assignment":
            method_kwargs = {
                k: v for k, v in kwargs.items() if k in ["queue_id", "body"]
            }
            return client.annotation_queues_create_queue_assignment(**method_kwargs)
        elif action == "annotation_queues_delete_queue_assignment":
            method_kwargs = {
                k: v for k, v in kwargs.items() if k in ["queue_id", "body"]
            }
            return client.annotation_queues_delete_queue_assignment(**method_kwargs)
        elif action == "dataset_items_create":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["body"]}
            return client.dataset_items_create(**method_kwargs)
        elif action == "dataset_items_list":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k
                in [
                    "dataset_name",
                    "source_trace_id",
                    "source_observation_id",
                    "version",
                    "page",
                    "limit",
                ]
            }
            return client.dataset_items_list(**method_kwargs)
        elif action == "dataset_items_get":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["id"]}
            return client.dataset_items_get(**method_kwargs)
        elif action == "dataset_items_delete":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["id"]}
            return client.dataset_items_delete(**method_kwargs)
        elif action == "dataset_run_items_create":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["body"]}
            return client.dataset_run_items_create(**method_kwargs)
        elif action == "dataset_run_items_list":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k in ["dataset_id", "run_name", "page", "limit"]
            }
            return client.dataset_run_items_list(**method_kwargs)
        elif action == "datasets_list":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["page", "limit"]}
            return client.datasets_list(**method_kwargs)
        elif action == "datasets_create":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["body"]}
            return client.datasets_create(**method_kwargs)
        elif action == "datasets_get":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["dataset_name"]}
            return client.datasets_get(**method_kwargs)
        elif action == "datasets_get_run":
            method_kwargs = {
                k: v for k, v in kwargs.items() if k in ["dataset_name", "run_name"]
            }
            return client.datasets_get_run(**method_kwargs)
        elif action == "datasets_delete_run":
            method_kwargs = {
                k: v for k, v in kwargs.items() if k in ["dataset_name", "run_name"]
            }
            return client.datasets_delete_run(**method_kwargs)
        elif action == "datasets_get_runs":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k in ["dataset_name", "page", "limit"]
            }
            return client.datasets_get_runs(**method_kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")
