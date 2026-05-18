#!/usr/bin/python
import warnings

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import logging
import os
import sys
from typing import Any

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import create_mcp_server
from dotenv import find_dotenv, load_dotenv
from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field
from starlette.requests import Request
from starlette.responses import JSONResponse

from langfuse_agent.auth import get_client

__version__ = "0.10.0"

logger = get_logger(name="langfuse-agent")
logger.setLevel(logging.INFO)


def register_annotation_queues_tools(mcp: FastMCP):
    @mcp.tool(tags={"annotation_queues"})
    async def langfuse_annotation_queues(
        action: str = Field(
            description="Action to perform. Must be one of: 'annotation_queues_list_queues', 'annotation_queues_create_queue', 'annotation_queues_get_queue', 'annotation_queues_list_queue_items', 'annotation_queues_create_queue_item', 'annotation_queues_get_queue_item', 'annotation_queues_update_queue_item', 'annotation_queues_delete_queue_item', 'annotation_queues_create_queue_assignment', 'annotation_queues_delete_queue_assignment'"
        ),
        page: int | None = Field(default=None, description="page"),
        limit: int | None = Field(default=None, description="limit"),
        body: dict | None = Field(default=None, description="body"),
        queue_id: str | None = Field(default=None, description="queue id"),
        status: Any | None = Field(default=None, description="status"),
        item_id: str | None = Field(default=None, description="item id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage annotation queues operations.

        Actions:
          - 'annotation_queues_list_queues': Get all annotation queues
          - 'annotation_queues_create_queue': Create an annotation queue
          - 'annotation_queues_get_queue': Get an annotation queue by ID
          - 'annotation_queues_list_queue_items': Get items for a specific annotation queue
          - 'annotation_queues_create_queue_item': Add an item to an annotation queue
          - 'annotation_queues_get_queue_item': Get a specific item from an annotation queue
          - 'annotation_queues_update_queue_item': Update an annotation queue item
          - 'annotation_queues_delete_queue_item': Remove an item from an annotation queue
          - 'annotation_queues_create_queue_assignment': Create an assignment for a user to an annotation queue
          - 'annotation_queues_delete_queue_assignment': Delete an assignment for a user to an annotation queue
        """
        kwargs: dict[str, Any]
        if action == "annotation_queues_list_queues":
            kwargs = {"page": page, "limit": limit}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.annotation_queues_list_queues(**kwargs)
        if action == "annotation_queues_create_queue":
            kwargs = {"body": body}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.annotation_queues_create_queue(**kwargs)
        if action == "annotation_queues_get_queue":
            kwargs = {"queue_id": queue_id}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.annotation_queues_get_queue(**kwargs)
        if action == "annotation_queues_list_queue_items":
            kwargs = {
                "queue_id": queue_id,  # type: ignore
                "status": status,
                "page": page,
                "limit": limit,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.annotation_queues_list_queue_items(**kwargs)
        if action == "annotation_queues_create_queue_item":
            kwargs = {"queue_id": queue_id, "body": body}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.annotation_queues_create_queue_item(**kwargs)
        if action == "annotation_queues_get_queue_item":
            kwargs = {"queue_id": queue_id, "item_id": item_id}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.annotation_queues_get_queue_item(**kwargs)
        if action == "annotation_queues_update_queue_item":
            kwargs = {
                "queue_id": queue_id,
                "item_id": item_id,
                "body": body,
            }  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.annotation_queues_update_queue_item(**kwargs)
        if action == "annotation_queues_delete_queue_item":
            kwargs = {"queue_id": queue_id, "item_id": item_id}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.annotation_queues_delete_queue_item(**kwargs)
        if action == "annotation_queues_create_queue_assignment":
            kwargs = {"queue_id": queue_id, "body": body}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.annotation_queues_create_queue_assignment(**kwargs)
        if action == "annotation_queues_delete_queue_assignment":
            kwargs = {"queue_id": queue_id, "body": body}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.annotation_queues_delete_queue_assignment(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: annotation_queues_list_queues', 'annotation_queues_create_queue', 'annotation_queues_get_queue', 'annotation_queues_list_queue_items', 'annotation_queues_create_queue_item', 'annotation_queues_get_queue_item', 'annotation_queues_update_queue_item', 'annotation_queues_delete_queue_item', 'annotation_queues_create_queue_assignment', 'annotation_queues_delete_queue_assignment"
        )


def register_blob_storage_integrations_tools(mcp: FastMCP):
    @mcp.tool(tags={"blob_storage_integrations"})
    async def langfuse_blob_storage_integrations(
        action: str = Field(
            description="Action to perform. Must be one of: 'blob_storage_integrations_get_blob_storage_integrations', 'blob_storage_integrations_upsert_blob_storage_integration', 'blob_storage_integrations_get_blob_storage_integration_status', 'blob_storage_integrations_delete_blob_storage_integration'"
        ),
        body: dict | None = Field(default=None, description="body"),
        id: str | None = Field(default=None, description="id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage blob storage integrations operations.

        Actions:
          - 'blob_storage_integrations_get_blob_storage_integrations': Get all blob storage integrations for the organization (requires organization-scoped API key)
          - 'blob_storage_integrations_upsert_blob_storage_integration': Create or update a blob storage integration for a specific project (requires organization-scoped API key). The configuration is validated by performing a test upload to the bucket.
          - 'blob_storage_integrations_get_blob_storage_integration_status': Get the sync status of a blob storage integration by integration ID (requires organization-scoped API key)
          - 'blob_storage_integrations_delete_blob_storage_integration': Delete a blob storage integration by ID (requires organization-scoped API key)
        """
        kwargs: dict[str, Any]
        if action == "blob_storage_integrations_get_blob_storage_integrations":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.blob_storage_integrations_get_blob_storage_integrations(
                **kwargs
            )
        if action == "blob_storage_integrations_upsert_blob_storage_integration":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.blob_storage_integrations_upsert_blob_storage_integration(
                **kwargs
            )
        if action == "blob_storage_integrations_get_blob_storage_integration_status":
            kwargs = {"id": id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.blob_storage_integrations_get_blob_storage_integration_status(
                **kwargs
            )
        if action == "blob_storage_integrations_delete_blob_storage_integration":
            kwargs = {"id": id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.blob_storage_integrations_delete_blob_storage_integration(
                **kwargs
            )
        raise ValueError(
            f"Unknown action: {action}. Must be one of: blob_storage_integrations_get_blob_storage_integrations', 'blob_storage_integrations_upsert_blob_storage_integration', 'blob_storage_integrations_get_blob_storage_integration_status', 'blob_storage_integrations_delete_blob_storage_integration"
        )


def register_comments_tools(mcp: FastMCP):
    @mcp.tool(tags={"comments"})
    async def langfuse_comments(
        action: str = Field(
            description="Action to perform. Must be one of: 'comments_create', 'comments_get', 'comments_get_by_id'"
        ),
        body: dict | None = Field(default=None, description="body"),
        page: int | None = Field(default=None, description="page"),
        limit: int | None = Field(default=None, description="limit"),
        object_type: str | None = Field(default=None, description="object type"),
        object_id: str | None = Field(default=None, description="object id"),
        author_user_id: str | None = Field(default=None, description="author user id"),
        comment_id: str | None = Field(default=None, description="comment id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage comments operations.

        Actions:
          - 'comments_create': Create a comment. Comments may be attached to different object types (trace, observation, session, prompt).
          - 'comments_get': Get all comments
          - 'comments_get_by_id': Get a comment by id
        """
        kwargs: dict[str, Any]
        if action == "comments_create":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.comments_create(**kwargs)
        if action == "comments_get":
            kwargs = {
                "page": page,  # type: ignore
                "limit": limit,  # type: ignore
                "object_type": object_type,  # type: ignore
                "object_id": object_id,  # type: ignore
                "author_user_id": author_user_id,  # type: ignore
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.comments_get(**kwargs)
        if action == "comments_get_by_id":
            kwargs = {"comment_id": comment_id}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.comments_get_by_id(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: comments_create', 'comments_get', 'comments_get_by_id"
        )


def register_dataset_items_tools(mcp: FastMCP):
    @mcp.tool(tags={"dataset_items"})
    async def langfuse_dataset_items(
        action: str = Field(
            description="Action to perform. Must be one of: 'dataset_items_create', 'dataset_items_list', 'dataset_items_get', 'dataset_items_delete'"
        ),
        body: dict | None = Field(default=None, description="body"),
        dataset_name: str | None = Field(default=None, description="dataset name"),
        source_trace_id: str | None = Field(
            default=None, description="source trace id"
        ),
        source_observation_id: str | None = Field(
            default=None, description="source observation id"
        ),
        version: str | None = Field(default=None, description="version"),
        page: int | None = Field(default=None, description="page"),
        limit: int | None = Field(default=None, description="limit"),
        id: str | None = Field(default=None, description="id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage dataset items operations.

        Actions:
          - 'dataset_items_create': Create a dataset item
          - 'dataset_items_list': Get dataset items. Optionally specify a version to get the items as they existed at that point in time. Note: If version parameter is provided, datasetName must also be provided.
          - 'dataset_items_get': Get a dataset item
          - 'dataset_items_delete': Delete a dataset item and all its run items. This action is irreversible.
        """
        kwargs: dict[str, Any]
        if action == "dataset_items_create":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.dataset_items_create(**kwargs)
        if action == "dataset_items_list":
            kwargs = {
                "dataset_name": dataset_name,  # type: ignore
                "source_trace_id": source_trace_id,  # type: ignore
                "source_observation_id": source_observation_id,  # type: ignore
                "version": version,  # type: ignore
                "page": page,  # type: ignore
                "limit": limit,  # type: ignore
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.dataset_items_list(**kwargs)
        if action == "dataset_items_get":
            kwargs = {"id": id}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.dataset_items_get(**kwargs)
        if action == "dataset_items_delete":
            kwargs = {"id": id}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.dataset_items_delete(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: dataset_items_create', 'dataset_items_list', 'dataset_items_get', 'dataset_items_delete"
        )


def register_dataset_run_items_tools(mcp: FastMCP):
    @mcp.tool(tags={"dataset_run_items"})
    async def langfuse_dataset_run_items(
        action: str = Field(
            description="Action to perform. Must be one of: 'dataset_run_items_create', 'dataset_run_items_list'"
        ),
        body: dict | None = Field(default=None, description="body"),
        dataset_id: str | None = Field(default=None, description="dataset id"),
        run_name: str | None = Field(default=None, description="run name"),
        page: int | None = Field(default=None, description="page"),
        limit: int | None = Field(default=None, description="limit"),
        client=Depends(get_client),
    ) -> dict:
        """Manage dataset run items operations.

        Actions:
          - 'dataset_run_items_create': Create a dataset run item
          - 'dataset_run_items_list': List dataset run items
        """
        kwargs: dict[str, Any]
        if action == "dataset_run_items_create":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.dataset_run_items_create(**kwargs)
        if action == "dataset_run_items_list":
            kwargs = {
                "dataset_id": dataset_id,  # type: ignore
                "run_name": run_name,  # type: ignore
                "page": page,  # type: ignore
                "limit": limit,  # type: ignore
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.dataset_run_items_list(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: dataset_run_items_create', 'dataset_run_items_list"
        )


def register_datasets_tools(mcp: FastMCP):
    @mcp.tool(tags={"datasets"})
    async def langfuse_datasets(
        action: str = Field(
            description="Action to perform. Must be one of: 'datasets_list', 'datasets_create', 'datasets_get', 'datasets_get_run', 'datasets_delete_run', 'datasets_get_runs'"
        ),
        page: int | None = Field(default=None, description="page"),
        limit: int | None = Field(default=None, description="limit"),
        body: dict | None = Field(default=None, description="body"),
        dataset_name: str | None = Field(default=None, description="dataset name"),
        run_name: str | None = Field(default=None, description="run name"),
        client=Depends(get_client),
    ) -> dict:
        """Manage datasets operations.

        Actions:
          - 'datasets_list': Get all datasets
          - 'datasets_create': Create a dataset
          - 'datasets_get': Get a dataset
          - 'datasets_get_run': Get a dataset run and its items
          - 'datasets_delete_run': Delete a dataset run and all its run items. This action is irreversible.
          - 'datasets_get_runs': Get dataset runs
        """
        kwargs: dict[str, Any]
        if action == "datasets_list":
            kwargs = {"page": page, "limit": limit}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.datasets_list(**kwargs)
        if action == "datasets_create":
            kwargs = {"body": body}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.datasets_create(**kwargs)
        if action == "datasets_get":
            kwargs = {"dataset_name": dataset_name}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.datasets_get(**kwargs)
        if action == "datasets_get_run":
            kwargs = {
                "dataset_name": dataset_name,
                "run_name": run_name,
            }  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.datasets_get_run(**kwargs)
        if action == "datasets_delete_run":
            kwargs = {
                "dataset_name": dataset_name,
                "run_name": run_name,
            }  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.datasets_delete_run(**kwargs)
        if action == "datasets_get_runs":
            kwargs = {
                "dataset_name": dataset_name,
                "page": page,
                "limit": limit,
            }  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.datasets_get_runs(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: datasets_list', 'datasets_create', 'datasets_get', 'datasets_get_run', 'datasets_delete_run', 'datasets_get_runs"
        )


def register_health_tools(mcp: FastMCP):
    @mcp.tool(tags={"health"})
    async def langfuse_health(
        action: str = Field(
            description="Action to perform. Must be one of: 'health_health'"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage health operations.

        Actions:
          - 'health_health': Check health of API and database
        """
        kwargs: dict[str, Any]
        if action == "health_health":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.health_health(**kwargs)
        raise ValueError(f"Unknown action: {action}. Must be one of: health_health")


def register_ingestion_tools(mcp: FastMCP):
    @mcp.tool(tags={"ingestion"})
    async def langfuse_ingestion(
        action: str = Field(
            description="Action to perform. Must be one of: 'ingestion_batch'"
        ),
        batch: list | None = Field(default=None, description="batch"),
        metadata: Any | None = Field(default=None, description="metadata"),
        client=Depends(get_client),
    ) -> dict:
        """Manage ingestion operations.

        Actions:
          - 'ingestion_batch': **Legacy endpoint for batch ingestion for Langfuse Observability.**  -> Please use the OpenTelemetry endpoint (`/api/public/otel/v1/traces`). Learn more: https://langfuse.com/integrations/native/opentelemetry  Within each batch, there can be multiple events. Each event has a type, an id, a timestamp, metadata and a body. Internally, we refer to this as the "event envelope" as it tells us something about the event but not the trace. We use the event id within this envelope to deduplicate messages to avoid processing the same event twice, i.e. the event id should be unique per request. The event.body.id is the ID of the actual trace and will be used for updates and will be visible within the Langfuse App. I.e. if you want to update a trace, you'd use the same body id, but separate event IDs.  Notes: - Introduction to data model: https://langfuse.com/docs/observability/data-model - Batch sizes are limited to 3.5 MB in total. You need to adjust the number of events per batch accordingly. - The API does not return a 4xx status code for input errors. Instead, it responds with a 207 status code, which includes a list of the encountered errors.
        """
        kwargs: dict[str, Any]
        if action == "ingestion_batch":
            kwargs = {"batch": batch, "metadata": metadata}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.ingestion_batch(**kwargs)
        raise ValueError(f"Unknown action: {action}. Must be one of: ingestion_batch")


def register_legacy_metrics_v1_tools(mcp: FastMCP):
    @mcp.tool(tags={"legacy_metrics_v1"})
    async def langfuse_legacy_metrics_v1(
        action: str = Field(
            description="Action to perform. Must be one of: 'legacy_metrics_v1_metrics'"
        ),
        query: str | None = Field(default=None, description="query"),
        client=Depends(get_client),
    ) -> dict:
        """Manage legacy metrics v1 operations.

        Actions:
          - 'legacy_metrics_v1_metrics': Get metrics from the Langfuse project using a query object.  Consider using the [v2 metrics endpoint](/api-reference#tag/metricsv2/GET/api/public/v2/metrics) for better performance.  For more details, see the [Metrics API documentation](https://langfuse.com/docs/metrics/features/metrics-api).
        """
        kwargs: dict[str, Any]
        if action == "legacy_metrics_v1_metrics":
            kwargs = {"query": query}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.legacy_metrics_v1_metrics(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: legacy_metrics_v1_metrics"
        )


def register_legacy_observations_v1_tools(mcp: FastMCP):
    @mcp.tool(tags={"legacy_observations_v1"})
    async def langfuse_legacy_observations_v1(
        action: str = Field(
            description="Action to perform. Must be one of: 'legacy_observations_v1_get', 'legacy_observations_v1_get_many'"
        ),
        observation_id: str | None = Field(default=None, description="observation id"),
        page: int | None = Field(default=None, description="page"),
        limit: int | None = Field(default=None, description="limit"),
        name: str | None = Field(default=None, description="name"),
        user_id: str | None = Field(default=None, description="user id"),
        type: str | None = Field(default=None, description="type"),
        trace_id: str | None = Field(default=None, description="trace id"),
        level: Any | None = Field(default=None, description="level"),
        parent_observation_id: str | None = Field(
            default=None, description="parent observation id"
        ),
        environment: list | None = Field(default=None, description="environment"),
        from_start_time: str | None = Field(
            default=None, description="from start time"
        ),
        to_start_time: str | None = Field(default=None, description="to start time"),
        version: str | None = Field(default=None, description="version"),
        filter: str | None = Field(default=None, description="filter"),
        client=Depends(get_client),
    ) -> dict:
        """Manage legacy observations v1 operations.

        Actions:
          - 'legacy_observations_v1_get': Get a observation
          - 'legacy_observations_v1_get_many': Get a list of observations.  Consider using the [v2 observations endpoint](/api-reference#tag/observationsv2/GET/api/public/v2/observations) for cursor-based pagination and field selection.
        """
        kwargs: dict[str, Any]
        if action == "legacy_observations_v1_get":
            kwargs = {"observation_id": observation_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.legacy_observations_v1_get(**kwargs)
        if action == "legacy_observations_v1_get_many":
            kwargs = {
                "page": page,  # type: ignore
                "limit": limit,  # type: ignore
                "name": name,
                "user_id": user_id,
                "type": type,
                "trace_id": trace_id,
                "level": level,
                "parent_observation_id": parent_observation_id,
                "environment": environment,  # type: ignore
                "from_start_time": from_start_time,
                "to_start_time": to_start_time,
                "version": version,
                "filter": filter,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.legacy_observations_v1_get_many(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: legacy_observations_v1_get', 'legacy_observations_v1_get_many"
        )


def register_legacy_score_v1_tools(mcp: FastMCP):
    @mcp.tool(tags={"legacy_score_v1"})
    async def langfuse_legacy_score_v1(
        action: str = Field(
            description="Action to perform. Must be one of: 'legacy_score_v1_create', 'legacy_score_v1_delete'"
        ),
        body: dict | None = Field(default=None, description="body"),
        score_id: str | None = Field(default=None, description="score id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage legacy score v1 operations.

        Actions:
          - 'legacy_score_v1_create': Create a score (supports both trace and session scores)
          - 'legacy_score_v1_delete': Delete a score (supports both trace and session scores)
        """
        kwargs: dict[str, Any]
        if action == "legacy_score_v1_create":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.legacy_score_v1_create(**kwargs)
        if action == "legacy_score_v1_delete":
            kwargs = {"score_id": score_id}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.legacy_score_v1_delete(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: legacy_score_v1_create', 'legacy_score_v1_delete"
        )


def register_llm_connections_tools(mcp: FastMCP):
    @mcp.tool(tags={"llm_connections"})
    async def langfuse_llm_connections(
        action: str = Field(
            description="Action to perform. Must be one of: 'llm_connections_list', 'llm_connections_upsert'"
        ),
        page: int | None = Field(default=None, description="page"),
        limit: int | None = Field(default=None, description="limit"),
        body: dict | None = Field(default=None, description="body"),
        client=Depends(get_client),
    ) -> dict:
        """Manage llm connections operations.

        Actions:
          - 'llm_connections_list': Get all LLM connections in a project
          - 'llm_connections_upsert': Create or update an LLM connection. The connection is upserted on provider.
        """
        kwargs: dict[str, Any]
        if action == "llm_connections_list":
            kwargs = {"page": page, "limit": limit}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.llm_connections_list(**kwargs)
        if action == "llm_connections_upsert":
            kwargs = {"body": body}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.llm_connections_upsert(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: llm_connections_list', 'llm_connections_upsert"
        )


def register_media_tools(mcp: FastMCP):
    @mcp.tool(tags={"media"})
    async def langfuse_media(
        action: str = Field(
            description="Action to perform. Must be one of: 'media_get', 'media_patch', 'media_get_upload_url'"
        ),
        media_id: str | None = Field(default=None, description="media id"),
        body: dict | None = Field(default=None, description="body"),
        client=Depends(get_client),
    ) -> dict:
        """Manage media operations.

        Actions:
          - 'media_get': Get a media record
          - 'media_patch': Patch a media record
          - 'media_get_upload_url': Get a presigned upload URL for a media record
        """
        kwargs: dict[str, Any]
        if action == "media_get":
            kwargs = {"media_id": media_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.media_get(**kwargs)
        if action == "media_patch":
            kwargs = {"media_id": media_id, "body": body}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.media_patch(**kwargs)
        if action == "media_get_upload_url":
            kwargs = {"body": body}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.media_get_upload_url(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: media_get', 'media_patch', 'media_get_upload_url"
        )


def register_metrics_tools(mcp: FastMCP):
    @mcp.tool(tags={"metrics"})
    async def langfuse_metrics(
        action: str = Field(
            description="Action to perform. Must be one of: 'metrics_metrics'"
        ),
        query: str | None = Field(default=None, description="query"),
        client=Depends(get_client),
    ) -> dict:
        """Manage metrics operations.

        Actions:
          - 'metrics_metrics': Get metrics from the Langfuse project using a query object. V2 endpoint with optimized performance.  ## V2 Differences - Supports `observations`, `scores-numeric`, and `scores-categorical` views only (traces view not supported) - Direct access to tags and release fields on observations - Backwards-compatible: traceName, traceRelease, traceVersion dimensions are still available on observations view - High cardinality dimensions are not supported and will return a 400 error (see below)  For more details, see the [Metrics API documentation](https://langfuse.com/docs/metrics/features/metrics-api).  ## Available Views  ### observations Query observation-level data (spans, generations, events).  **Dimensions:** - `environment` - Deployment environment (e.g., production, staging) - `type` - Type of observation (SPAN, GENERATION, EVENT) - `name` - Name of the observation - `level` - Logging level of the observation - `version` - Version of the observation - `tags` - User-defined tags - `release` - Release version - `traceName` - Name of the parent trace (backwards-compatible) - `traceRelease` - Release version of the parent trace (backwards-compatible, maps to release) - `traceVersion` - Version of the parent trace (backwards-compatible, maps to version) - `providedModelName` - Name of the model used - `promptName` - Name of the prompt used - `promptVersion` - Version of the prompt used - `startTimeMonth` - Month of start_time in YYYY-MM format  **Measures:** - `count` - Total number of observations - `latency` - Observation latency (milliseconds) - `streamingLatency` - Generation latency from completion start to end (milliseconds) - `inputTokens` - Sum of input tokens consumed - `outputTokens` - Sum of output tokens produced - `totalTokens` - Sum of all tokens consumed - `outputTokensPerSecond` - Output tokens per second - `tokensPerSecond` - Total tokens per second - `inputCost` - Input cost (USD) - `outputCost` - Output cost (USD) - `totalCost` - Total cost (USD) - `timeToFirstToken` - Time to first token (milliseconds) - `countScores` - Number of scores attached to the observation  ### scores-numeric Query numeric and boolean score data.  **Dimensions:** - `environment` - Deployment environment - `name` - Name of the score (e.g., accuracy, toxicity) - `source` - Origin of the score (API, ANNOTATION, EVAL) - `dataType` - Data type (NUMERIC, BOOLEAN) - `configId` - Identifier of the score config - `timestampMonth` - Month in YYYY-MM format - `timestampDay` - Day in YYYY-MM-DD format - `value` - Numeric value of the score - `traceName` - Name of the parent trace - `tags` - Tags - `traceRelease` - Release version - `traceVersion` - Version - `observationName` - Name of the associated observation - `observationModelName` - Model name of the associated observation - `observationPromptName` - Prompt name of the associated observation - `observationPromptVersion` - Prompt version of the associated observation  **Measures:** - `count` - Total number of scores - `value` - Score value (for aggregations)  ### scores-categorical Query categorical score data. Same dimensions as scores-numeric except uses `stringValue` instead of `value`.  **Measures:** - `count` - Total number of scores  ## High Cardinality Dimensions The following dimensions cannot be used as grouping dimensions in v2 metrics API as they can cause performance issues. Use them in filters instead.  **observations view:** - `id` - Use traceId filter to narrow down results - `traceId` - Use traceId filter instead - `userId` - Use userId filter instead - `sessionId` - Use sessionId filter instead - `parentObservationId` - Use parentObservationId filter instead  **scores-numeric / scores-categorical views:** - `id` - Use specific filters to narrow down results - `traceId` - Use traceId filter instead - `userId` - Use userId filter instead - `sessionId` - Use sessionId filter instead - `observationId` - Use observationId filter instead  ## Aggregations Available aggregation functions: `sum`, `avg`, `count`, `max`, `min`, `p50`, `p75`, `p90`, `p95`, `p99`, `histogram`  ## Time Granularities Available granularities for timeDimension: `auto`, `minute`, `hour`, `day`, `week`, `month` - `auto` bins the data into approximately 50 buckets based on the time range
        """
        kwargs: dict[str, Any]
        if action == "metrics_metrics":
            kwargs = {"query": query}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.metrics_metrics(**kwargs)
        raise ValueError(f"Unknown action: {action}. Must be one of: metrics_metrics")


def register_models_tools(mcp: FastMCP):
    @mcp.tool(tags={"models"})
    async def langfuse_models(
        action: str = Field(
            description="Action to perform. Must be one of: 'models_create', 'models_list', 'models_get', 'models_delete'"
        ),
        body: dict | None = Field(default=None, description="body"),
        page: int | None = Field(default=None, description="page"),
        limit: int | None = Field(default=None, description="limit"),
        id: str | None = Field(default=None, description="id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage models operations.

        Actions:
          - 'models_create': Create a model
          - 'models_list': Get all models
          - 'models_get': Get a model
          - 'models_delete': Delete a model. Cannot delete models managed by Langfuse. You can create your own definition with the same modelName to override the definition though.
        """
        kwargs: dict[str, Any]
        if action == "models_create":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.models_create(**kwargs)
        if action == "models_list":
            kwargs = {"page": page, "limit": limit}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.models_list(**kwargs)
        if action == "models_get":
            kwargs = {"id": id}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.models_get(**kwargs)
        if action == "models_delete":
            kwargs = {"id": id}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.models_delete(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: models_create', 'models_list', 'models_get', 'models_delete"
        )


def register_observations_tools(mcp: FastMCP):
    @mcp.tool(tags={"observations"})
    async def langfuse_observations(
        action: str = Field(
            description="Action to perform. Must be one of: 'observations_get_many'"
        ),
        fields: str | None = Field(default=None, description="fields"),
        expand_metadata: str | None = Field(
            default=None, description="expand metadata"
        ),
        limit: int | None = Field(default=None, description="limit"),
        cursor: str | None = Field(default=None, description="cursor"),
        parse_io_as_json: bool | None = Field(
            default=None, description="parse io as json"
        ),
        name: str | None = Field(default=None, description="name"),
        user_id: str | None = Field(default=None, description="user id"),
        type: str | None = Field(default=None, description="type"),
        trace_id: str | None = Field(default=None, description="trace id"),
        level: Any | None = Field(default=None, description="level"),
        parent_observation_id: str | None = Field(
            default=None, description="parent observation id"
        ),
        environment: list | None = Field(default=None, description="environment"),
        from_start_time: str | None = Field(
            default=None, description="from start time"
        ),
        to_start_time: str | None = Field(default=None, description="to start time"),
        version: str | None = Field(default=None, description="version"),
        filter: str | None = Field(default=None, description="filter"),
        client=Depends(get_client),
    ) -> dict:
        """Manage observations operations.

        Actions:
          - 'observations_get_many': Get a list of observations with cursor-based pagination and flexible field selection.  ## Cursor-based Pagination This endpoint uses cursor-based pagination for efficient traversal of large datasets. The cursor is returned in the response metadata and should be passed in subsequent requests to retrieve the next page of results.  ## Field Selection Use the `fields` parameter to control which observation fields are returned: - `core` - Always included: id, traceId, startTime, endTime, projectId, parentObservationId, type - `basic` - name, level, statusMessage, version, environment, bookmarked, public, userId, sessionId - `time` - completionStartTime, createdAt, updatedAt - `io` - input, output - `metadata` - metadata (truncated to 200 chars by default, use `expandMetadata` to get full values) - `model` - providedModelName, internalModelId, modelParameters - `usage` - usageDetails, costDetails, totalCost - `prompt` - promptId, promptName, promptVersion - `metrics` - latency, timeToFirstToken  If not specified, `core` and `basic` field groups are returned.  ## Filters Multiple filtering options are available via query parameters or the structured `filter` parameter. When using the `filter` parameter, it takes precedence over individual query parameter filters.
        """
        kwargs: dict[str, Any]
        if action == "observations_get_many":
            kwargs = {
                "fields": fields,
                "expand_metadata": expand_metadata,
                "limit": limit,
                "cursor": cursor,
                "parse_io_as_json": parse_io_as_json,
                "name": name,
                "user_id": user_id,
                "type": type,
                "trace_id": trace_id,
                "level": level,
                "parent_observation_id": parent_observation_id,
                "environment": environment,
                "from_start_time": from_start_time,
                "to_start_time": to_start_time,
                "version": version,
                "filter": filter,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.observations_get_many(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: observations_get_many"
        )


def register_opentelemetry_tools(mcp: FastMCP):
    @mcp.tool(tags={"opentelemetry"})
    async def langfuse_opentelemetry(
        action: str = Field(
            description="Action to perform. Must be one of: 'opentelemetry_export_traces'"
        ),
        resource_spans: list | None = Field(default=None, description="resource spans"),
        client=Depends(get_client),
    ) -> dict:
        """Manage opentelemetry operations.

        Actions:
          - 'opentelemetry_export_traces': **OpenTelemetry Traces Ingestion Endpoint**  This endpoint implements the OTLP/HTTP specification for trace ingestion, providing native OpenTelemetry integration for Langfuse Observability.  **Supported Formats:** - Binary Protobuf: `Content-Type: application/x-protobuf` - JSON Protobuf: `Content-Type: application/json` - Supports gzip compression via `Content-Encoding: gzip` header  **Specification Compliance:** - Conforms to [OTLP/HTTP Trace Export](https://opentelemetry.io/docs/specs/otlp/#otlphttp) - Implements `ExportTraceServiceRequest` message format  **Documentation:** - Integration guide: https://langfuse.com/integrations/native/opentelemetry - Data model: https://langfuse.com/docs/observability/data-model
        """
        kwargs: dict[str, Any]
        if action == "opentelemetry_export_traces":
            kwargs = {"resource_spans": resource_spans}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.opentelemetry_export_traces(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: opentelemetry_export_traces"
        )


def register_organizations_tools(mcp: FastMCP):
    @mcp.tool(tags={"organizations"})
    async def langfuse_organizations(
        action: str = Field(
            description="Action to perform. Must be one of: 'organizations_get_organization_memberships', 'organizations_update_organization_membership', 'organizations_delete_organization_membership', 'organizations_get_project_memberships', 'organizations_update_project_membership', 'organizations_delete_project_membership', 'organizations_get_organization_projects', 'organizations_get_organization_api_keys'"
        ),
        body: dict | None = Field(default=None, description="body"),
        project_id: str | None = Field(default=None, description="project id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage organizations operations.

        Actions:
          - 'organizations_get_organization_memberships': Get all memberships for the organization associated with the API key (requires organization-scoped API key)
          - 'organizations_update_organization_membership': Create or update a membership for the organization associated with the API key (requires organization-scoped API key)
          - 'organizations_delete_organization_membership': Delete a membership from the organization associated with the API key (requires organization-scoped API key)
          - 'organizations_get_project_memberships': Get all memberships for a specific project (requires organization-scoped API key)
          - 'organizations_update_project_membership': Create or update a membership for a specific project (requires organization-scoped API key). The user must already be a member of the organization.
          - 'organizations_delete_project_membership': Delete a membership from a specific project (requires organization-scoped API key). The user must be a member of the organization.
          - 'organizations_get_organization_projects': Get all projects for the organization associated with the API key (requires organization-scoped API key)
          - 'organizations_get_organization_api_keys': Get all API keys for the organization associated with the API key (requires organization-scoped API key)
        """
        kwargs: dict[str, Any]
        if action == "organizations_get_organization_memberships":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.organizations_get_organization_memberships(**kwargs)
        if action == "organizations_update_organization_membership":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.organizations_update_organization_membership(**kwargs)
        if action == "organizations_delete_organization_membership":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.organizations_delete_organization_membership(**kwargs)
        if action == "organizations_get_project_memberships":
            kwargs = {"project_id": project_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.organizations_get_project_memberships(**kwargs)
        if action == "organizations_update_project_membership":
            kwargs = {"project_id": project_id, "body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.organizations_update_project_membership(**kwargs)
        if action == "organizations_delete_project_membership":
            kwargs = {"project_id": project_id, "body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.organizations_delete_project_membership(**kwargs)
        if action == "organizations_get_organization_projects":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.organizations_get_organization_projects(**kwargs)
        if action == "organizations_get_organization_api_keys":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.organizations_get_organization_api_keys(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: organizations_get_organization_memberships', 'organizations_update_organization_membership', 'organizations_delete_organization_membership', 'organizations_get_project_memberships', 'organizations_update_project_membership', 'organizations_delete_project_membership', 'organizations_get_organization_projects', 'organizations_get_organization_api_keys"
        )


def register_projects_tools(mcp: FastMCP):
    @mcp.tool(tags={"projects"})
    async def langfuse_projects(
        action: str = Field(
            description="Action to perform. Must be one of: 'projects_get', 'projects_create', 'projects_update', 'projects_delete', 'projects_get_api_keys', 'projects_create_api_key', 'projects_delete_api_key'"
        ),
        name: str | None = Field(default=None, description="name"),
        retention: Any | None = Field(default=None, description="retention"),
        metadata: dict | None = Field(default=None, description="metadata"),
        project_id: str | None = Field(default=None, description="project id"),
        note: str | None = Field(default=None, description="note"),
        public_key: str | None = Field(default=None, description="public key"),
        secret_key: str | None = Field(default=None, description="secret key"),
        api_key_id: str | None = Field(default=None, description="api key id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage projects operations.

        Actions:
          - 'projects_get': Get Project associated with API key (requires project-scoped API key). You can use GET /api/public/organizations/projects to get all projects with an organization-scoped key.
          - 'projects_create': Create a new project (requires organization-scoped API key)
          - 'projects_update': Update a project by ID (requires organization-scoped API key).
          - 'projects_delete': Delete a project by ID (requires organization-scoped API key). Project deletion is processed asynchronously.
          - 'projects_get_api_keys': Get all API keys for a project (requires organization-scoped API key)
          - 'projects_create_api_key': Create a new API key for a project (requires organization-scoped API key)
          - 'projects_delete_api_key': Delete an API key for a project (requires organization-scoped API key)
        """
        kwargs: dict[str, Any]
        if action == "projects_get":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.projects_get(**kwargs)
        if action == "projects_create":
            kwargs = {
                "name": name,
                "retention": retention,
                "metadata": metadata,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.projects_create(**kwargs)
        if action == "projects_update":
            kwargs = {
                "project_id": project_id,
                "name": name,
                "metadata": metadata,
                "retention": retention,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.projects_update(**kwargs)
        if action == "projects_delete":
            kwargs = {"project_id": project_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.projects_delete(**kwargs)
        if action == "projects_get_api_keys":
            kwargs = {"project_id": project_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.projects_get_api_keys(**kwargs)
        if action == "projects_create_api_key":
            kwargs = {
                "project_id": project_id,
                "note": note,
                "public_key": public_key,
                "secret_key": secret_key,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.projects_create_api_key(**kwargs)
        if action == "projects_delete_api_key":
            kwargs = {
                "project_id": project_id,
                "api_key_id": api_key_id,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.projects_delete_api_key(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: projects_get', 'projects_create', 'projects_update', 'projects_delete', 'projects_get_api_keys', 'projects_create_api_key', 'projects_delete_api_key"
        )


def register_prompt_version_tools(mcp: FastMCP):
    @mcp.tool(tags={"prompt_version"})
    async def langfuse_prompt_version(
        action: str = Field(
            description="Action to perform. Must be one of: 'prompt_version_update'"
        ),
        name: str | None = Field(default=None, description="name"),
        version: int | None = Field(default=None, description="version"),
        new_labels: list | None = Field(default=None, description="new labels"),
        client=Depends(get_client),
    ) -> dict:
        """Manage prompt version operations.

        Actions:
          - 'prompt_version_update': Update labels for a specific prompt version
        """
        kwargs: dict[str, Any]
        if action == "prompt_version_update":
            kwargs = {
                "name": name,
                "version": version,
                "new_labels": new_labels,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.prompt_version_update(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: prompt_version_update"
        )


def register_prompts_tools(mcp: FastMCP):
    @mcp.tool(tags={"prompts"})
    async def langfuse_prompts(
        action: str = Field(
            description="Action to perform. Must be one of: 'prompts_get', 'prompts_delete', 'prompts_list', 'prompts_create'"
        ),
        prompt_name: str | None = Field(default=None, description="prompt name"),
        version: int | None = Field(default=None, description="version"),
        label: str | None = Field(default=None, description="label"),
        resolve: bool | None = Field(default=None, description="resolve"),
        name: str | None = Field(default=None, description="name"),
        tag: str | None = Field(default=None, description="tag"),
        page: int | None = Field(default=None, description="page"),
        limit: int | None = Field(default=None, description="limit"),
        from_updated_at: str | None = Field(
            default=None, description="from updated at"
        ),
        to_updated_at: str | None = Field(default=None, description="to updated at"),
        body: dict | None = Field(default=None, description="body"),
        client=Depends(get_client),
    ) -> dict:
        """Manage prompts operations.

        Actions:
          - 'prompts_get': Get a prompt
          - 'prompts_delete': Delete prompt versions. If neither version nor label is specified, all versions of the prompt are deleted.
          - 'prompts_list': Get a list of prompt names with versions and labels
          - 'prompts_create': Create a new version for the prompt with the given `name`
        """
        kwargs: dict[str, Any]
        if action == "prompts_get":
            kwargs = {
                "prompt_name": prompt_name,
                "version": version,
                "label": label,
                "resolve": resolve,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.prompts_get(**kwargs)
        if action == "prompts_delete":
            kwargs = {
                "prompt_name": prompt_name,
                "label": label,
                "version": version,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.prompts_delete(**kwargs)
        if action == "prompts_list":
            kwargs = {
                "name": name,
                "label": label,
                "tag": tag,
                "page": page,
                "limit": limit,
                "from_updated_at": from_updated_at,
                "to_updated_at": to_updated_at,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.prompts_list(**kwargs)
        if action == "prompts_create":
            kwargs = {"body": body}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.prompts_create(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: prompts_get', 'prompts_delete', 'prompts_list', 'prompts_create"
        )


def register_scim_tools(mcp: FastMCP):
    @mcp.tool(tags={"scim"})
    async def langfuse_scim(
        action: str = Field(
            description="Action to perform. Must be one of: 'scim_get_service_provider_config', 'scim_get_resource_types', 'scim_get_schemas', 'scim_list_users', 'scim_create_user', 'scim_get_user', 'scim_delete_user'"
        ),
        filter: str | None = Field(default=None, description="filter"),
        start_index: int | None = Field(default=None, description="start index"),
        count: int | None = Field(default=None, description="count"),
        user_name: str | None = Field(default=None, description="user name"),
        name: Any | None = Field(default=None, description="name"),
        emails: list | None = Field(default=None, description="emails"),
        active: bool | None = Field(default=None, description="active"),
        password: str | None = Field(default=None, description="password"),
        user_id: str | None = Field(default=None, description="user id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage scim operations.

        Actions:
          - 'scim_get_service_provider_config': Get SCIM Service Provider Configuration (requires organization-scoped API key)
          - 'scim_get_resource_types': Get SCIM Resource Types (requires organization-scoped API key)
          - 'scim_get_schemas': Get SCIM Schemas (requires organization-scoped API key)
          - 'scim_list_users': List users in the organization (requires organization-scoped API key)
          - 'scim_create_user': Create a new user in the organization (requires organization-scoped API key)
          - 'scim_get_user': Get a specific user by ID (requires organization-scoped API key)
          - 'scim_delete_user': Remove a user from the organization (requires organization-scoped API key). Note that this only removes the user from the organization but does not delete the user entity itself.
        """
        kwargs: dict[str, Any]
        if action == "scim_get_service_provider_config":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.scim_get_service_provider_config(**kwargs)
        if action == "scim_get_resource_types":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.scim_get_resource_types(**kwargs)
        if action == "scim_get_schemas":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.scim_get_schemas(**kwargs)
        if action == "scim_list_users":
            kwargs = {
                "filter": filter,
                "start_index": start_index,
                "count": count,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.scim_list_users(**kwargs)
        if action == "scim_create_user":
            kwargs = {
                "user_name": user_name,
                "name": name,
                "emails": emails,
                "active": active,
                "password": password,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.scim_create_user(**kwargs)
        if action == "scim_get_user":
            kwargs = {"user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.scim_get_user(**kwargs)
        if action == "scim_delete_user":
            kwargs = {"user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.scim_delete_user(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: scim_get_service_provider_config', 'scim_get_resource_types', 'scim_get_schemas', 'scim_list_users', 'scim_create_user', 'scim_get_user', 'scim_delete_user"
        )


def register_score_configs_tools(mcp: FastMCP):
    @mcp.tool(tags={"score_configs"})
    async def langfuse_score_configs(
        action: str = Field(
            description="Action to perform. Must be one of: 'score_configs_create', 'score_configs_get', 'score_configs_get_by_id', 'score_configs_update'"
        ),
        body: dict | None = Field(default=None, description="body"),
        page: int | None = Field(default=None, description="page"),
        limit: int | None = Field(default=None, description="limit"),
        config_id: str | None = Field(default=None, description="config id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage score configs operations.

        Actions:
          - 'score_configs_create': Create a score configuration (config). Score configs are used to define the structure of scores
          - 'score_configs_get': Get all score configs
          - 'score_configs_get_by_id': Get a score config
          - 'score_configs_update': Update a score config
        """
        kwargs: dict[str, Any]
        if action == "score_configs_create":
            kwargs = {"body": body}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.score_configs_create(**kwargs)
        if action == "score_configs_get":
            kwargs = {"page": page, "limit": limit}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.score_configs_get(**kwargs)
        if action == "score_configs_get_by_id":
            kwargs = {"config_id": config_id}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.score_configs_get_by_id(**kwargs)
        if action == "score_configs_update":
            kwargs = {"config_id": config_id, "body": body}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.score_configs_update(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: score_configs_create', 'score_configs_get', 'score_configs_get_by_id', 'score_configs_update"
        )


def register_scores_tools(mcp: FastMCP):
    @mcp.tool(tags={"scores"})
    async def langfuse_scores(
        action: str = Field(
            description="Action to perform. Must be one of: 'scores_get_many', 'scores_get_by_id'"
        ),
        page: int | None = Field(default=None, description="page"),
        limit: int | None = Field(default=None, description="limit"),
        user_id: str | None = Field(default=None, description="user id"),
        name: str | None = Field(default=None, description="name"),
        from_timestamp: str | None = Field(default=None, description="from timestamp"),
        to_timestamp: str | None = Field(default=None, description="to timestamp"),
        environment: list | None = Field(default=None, description="environment"),
        source: Any | None = Field(default=None, description="source"),
        operator: str | None = Field(default=None, description="operator"),
        value: int | None = Field(default=None, description="value"),
        score_ids: str | None = Field(default=None, description="score ids"),
        config_id: str | None = Field(default=None, description="config id"),
        session_id: str | None = Field(default=None, description="session id"),
        dataset_run_id: str | None = Field(default=None, description="dataset run id"),
        trace_id: str | None = Field(default=None, description="trace id"),
        observation_id: str | None = Field(default=None, description="observation id"),
        queue_id: str | None = Field(default=None, description="queue id"),
        data_type: Any | None = Field(default=None, description="data type"),
        trace_tags: list | None = Field(default=None, description="trace tags"),
        fields: str | None = Field(default=None, description="fields"),
        filter: str | None = Field(default=None, description="filter"),
        score_id: str | None = Field(default=None, description="score id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage scores operations.

        Actions:
          - 'scores_get_many': Get a list of scores (supports both trace and session scores)
          - 'scores_get_by_id': Get a score (supports both trace and session scores)
        """
        kwargs: dict[str, Any]
        if action == "scores_get_many":
            kwargs = {
                "page": page,
                "limit": limit,
                "user_id": user_id,
                "name": name,
                "from_timestamp": from_timestamp,
                "to_timestamp": to_timestamp,
                "environment": environment,
                "source": source,
                "operator": operator,
                "value": value,
                "score_ids": score_ids,
                "config_id": config_id,
                "session_id": session_id,
                "dataset_run_id": dataset_run_id,
                "trace_id": trace_id,
                "observation_id": observation_id,
                "queue_id": queue_id,
                "data_type": data_type,
                "trace_tags": trace_tags,
                "fields": fields,
                "filter": filter,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.scores_get_many(**kwargs)
        if action == "scores_get_by_id":
            kwargs = {"score_id": score_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.scores_get_by_id(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: scores_get_many', 'scores_get_by_id"
        )


def register_sessions_tools(mcp: FastMCP):
    @mcp.tool(tags={"sessions"})
    async def langfuse_sessions(
        action: str = Field(
            description="Action to perform. Must be one of: 'sessions_list', 'sessions_get'"
        ),
        page: int | None = Field(default=None, description="page"),
        limit: int | None = Field(default=None, description="limit"),
        from_timestamp: str | None = Field(default=None, description="from timestamp"),
        to_timestamp: str | None = Field(default=None, description="to timestamp"),
        environment: list | None = Field(default=None, description="environment"),
        session_id: str | None = Field(default=None, description="session id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage sessions operations.

        Actions:
          - 'sessions_list': Get sessions
          - 'sessions_get': Get a session. Please note that `traces` on this endpoint are not paginated, if you plan to fetch large sessions, consider `GET /api/public/traces?sessionId=<sessionId>`
        """
        kwargs: dict[str, Any]
        if action == "sessions_list":
            kwargs = {
                "page": page,
                "limit": limit,
                "from_timestamp": from_timestamp,
                "to_timestamp": to_timestamp,
                "environment": environment,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.sessions_list(**kwargs)
        if action == "sessions_get":
            kwargs = {"session_id": session_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.sessions_get(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: sessions_list', 'sessions_get"
        )


def register_trace_tools(mcp: FastMCP):
    @mcp.tool(tags={"trace"})
    async def langfuse_trace(
        action: str = Field(
            description="Action to perform. Must be one of: 'trace_get', 'trace_delete', 'trace_list', 'trace_delete_multiple'"
        ),
        trace_id: str | None = Field(default=None, description="trace id"),
        page: int | None = Field(default=None, description="page"),
        limit: int | None = Field(default=None, description="limit"),
        user_id: str | None = Field(default=None, description="user id"),
        name: str | None = Field(default=None, description="name"),
        session_id: str | None = Field(default=None, description="session id"),
        from_timestamp: str | None = Field(default=None, description="from timestamp"),
        to_timestamp: str | None = Field(default=None, description="to timestamp"),
        order_by: str | None = Field(default=None, description="order by"),
        tags: list | None = Field(default=None, description="tags"),
        version: str | None = Field(default=None, description="version"),
        release: str | None = Field(default=None, description="release"),
        environment: list | None = Field(default=None, description="environment"),
        fields: str | None = Field(default=None, description="fields"),
        filter: str | None = Field(default=None, description="filter"),
        trace_ids: list | None = Field(default=None, description="trace ids"),
        client=Depends(get_client),
    ) -> dict:
        """Manage trace operations.

        Actions:
          - 'trace_get': Get a specific trace
          - 'trace_delete': Delete a specific trace
          - 'trace_list': Get list of traces
          - 'trace_delete_multiple': Delete multiple traces
        """
        kwargs: dict[str, Any]
        if action == "trace_get":
            kwargs = {"trace_id": trace_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.trace_get(**kwargs)
        if action == "trace_delete":
            kwargs = {"trace_id": trace_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.trace_delete(**kwargs)
        if action == "trace_list":
            kwargs = {
                "page": page,  # type: ignore
                "limit": limit,  # type: ignore
                "user_id": user_id,
                "name": name,
                "session_id": session_id,
                "from_timestamp": from_timestamp,
                "to_timestamp": to_timestamp,
                "order_by": order_by,
                "tags": tags,  # type: ignore
                "version": version,
                "release": release,
                "environment": environment,  # type: ignore
                "fields": fields,
                "filter": filter,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.trace_list(**kwargs)
        if action == "trace_delete_multiple":
            kwargs = {"trace_ids": trace_ids}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.trace_delete_multiple(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: trace_get', 'trace_delete', 'trace_list', 'trace_delete_multiple"
        )


def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance."""
    load_dotenv(find_dotenv())
    args, mcp, middlewares = create_mcp_server(
        name="langfuse-agent MCP",
        version=__version__,
        instructions="langfuse-agent MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    DEFAULT_ANNOTATION_QUEUESTOOL = to_boolean(
        os.getenv("ANNOTATION_QUEUESTOOL", "True")
    )
    if DEFAULT_ANNOTATION_QUEUESTOOL:
        register_annotation_queues_tools(mcp)
    DEFAULT_BLOB_STORAGE_INTEGRATIONSTOOL = to_boolean(
        os.getenv("BLOB_STORAGE_INTEGRATIONSTOOL", "True")
    )
    if DEFAULT_BLOB_STORAGE_INTEGRATIONSTOOL:
        register_blob_storage_integrations_tools(mcp)
    DEFAULT_COMMENTSTOOL = to_boolean(os.getenv("COMMENTSTOOL", "True"))
    if DEFAULT_COMMENTSTOOL:
        register_comments_tools(mcp)
    DEFAULT_DATASET_ITEMSTOOL = to_boolean(os.getenv("DATASET_ITEMSTOOL", "True"))
    if DEFAULT_DATASET_ITEMSTOOL:
        register_dataset_items_tools(mcp)
    DEFAULT_DATASET_RUN_ITEMSTOOL = to_boolean(
        os.getenv("DATASET_RUN_ITEMSTOOL", "True")
    )
    if DEFAULT_DATASET_RUN_ITEMSTOOL:
        register_dataset_run_items_tools(mcp)
    DEFAULT_DATASETSTOOL = to_boolean(os.getenv("DATASETSTOOL", "True"))
    if DEFAULT_DATASETSTOOL:
        register_datasets_tools(mcp)
    DEFAULT_HEALTHTOOL = to_boolean(os.getenv("HEALTHTOOL", "True"))
    if DEFAULT_HEALTHTOOL:
        register_health_tools(mcp)
    DEFAULT_INGESTIONTOOL = to_boolean(os.getenv("INGESTIONTOOL", "True"))
    if DEFAULT_INGESTIONTOOL:
        register_ingestion_tools(mcp)
    DEFAULT_LEGACY_METRICS_V1TOOL = to_boolean(
        os.getenv("LEGACY_METRICS_V1TOOL", "True")
    )
    if DEFAULT_LEGACY_METRICS_V1TOOL:
        register_legacy_metrics_v1_tools(mcp)
    DEFAULT_LEGACY_OBSERVATIONS_V1TOOL = to_boolean(
        os.getenv("LEGACY_OBSERVATIONS_V1TOOL", "True")
    )
    if DEFAULT_LEGACY_OBSERVATIONS_V1TOOL:
        register_legacy_observations_v1_tools(mcp)
    DEFAULT_LEGACY_SCORE_V1TOOL = to_boolean(os.getenv("LEGACY_SCORE_V1TOOL", "True"))
    if DEFAULT_LEGACY_SCORE_V1TOOL:
        register_legacy_score_v1_tools(mcp)
    DEFAULT_LLM_CONNECTIONSTOOL = to_boolean(os.getenv("LLM_CONNECTIONSTOOL", "True"))
    if DEFAULT_LLM_CONNECTIONSTOOL:
        register_llm_connections_tools(mcp)
    DEFAULT_MEDIATOOL = to_boolean(os.getenv("MEDIATOOL", "True"))
    if DEFAULT_MEDIATOOL:
        register_media_tools(mcp)
    DEFAULT_METRICSTOOL = to_boolean(os.getenv("METRICSTOOL", "True"))
    if DEFAULT_METRICSTOOL:
        register_metrics_tools(mcp)
    DEFAULT_MODELSTOOL = to_boolean(os.getenv("MODELSTOOL", "True"))
    if DEFAULT_MODELSTOOL:
        register_models_tools(mcp)
    DEFAULT_OBSERVATIONSTOOL = to_boolean(os.getenv("OBSERVATIONSTOOL", "True"))
    if DEFAULT_OBSERVATIONSTOOL:
        register_observations_tools(mcp)
    DEFAULT_OPENTELEMETRYTOOL = to_boolean(os.getenv("OPENTELEMETRYTOOL", "True"))
    if DEFAULT_OPENTELEMETRYTOOL:
        register_opentelemetry_tools(mcp)
    DEFAULT_ORGANIZATIONSTOOL = to_boolean(os.getenv("ORGANIZATIONSTOOL", "True"))
    if DEFAULT_ORGANIZATIONSTOOL:
        register_organizations_tools(mcp)
    DEFAULT_PROJECTSTOOL = to_boolean(os.getenv("PROJECTSTOOL", "True"))
    if DEFAULT_PROJECTSTOOL:
        register_projects_tools(mcp)
    DEFAULT_PROMPT_VERSIONTOOL = to_boolean(os.getenv("PROMPT_VERSIONTOOL", "True"))
    if DEFAULT_PROMPT_VERSIONTOOL:
        register_prompt_version_tools(mcp)
    DEFAULT_PROMPTSTOOL = to_boolean(os.getenv("PROMPTSTOOL", "True"))
    if DEFAULT_PROMPTSTOOL:
        register_prompts_tools(mcp)
    DEFAULT_SCIMTOOL = to_boolean(os.getenv("SCIMTOOL", "True"))
    if DEFAULT_SCIMTOOL:
        register_scim_tools(mcp)
    DEFAULT_SCORE_CONFIGSTOOL = to_boolean(os.getenv("SCORE_CONFIGSTOOL", "True"))
    if DEFAULT_SCORE_CONFIGSTOOL:
        register_score_configs_tools(mcp)
    DEFAULT_SCORESTOOL = to_boolean(os.getenv("SCORESTOOL", "True"))
    if DEFAULT_SCORESTOOL:
        register_scores_tools(mcp)
    DEFAULT_SESSIONSTOOL = to_boolean(os.getenv("SESSIONSTOOL", "True"))
    if DEFAULT_SESSIONSTOOL:
        register_sessions_tools(mcp)
    DEFAULT_TRACETOOL = to_boolean(os.getenv("TRACETOOL", "True"))
    if DEFAULT_TRACETOOL:
        register_trace_tools(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)
    return mcp, args, middlewares


def mcp_server() -> None:
    mcp, args, middlewares = get_mcp_instance()
    print(f"langfuse-agent MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error("Invalid transport", extra={"transport": args.transport})
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
