#!/usr/bin/python
import warnings

from fastmcp import FastMCP
from fastmcp.utilities.logging import get_logger
from pydantic import Field

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

from langfuse_agent.auth import get_client

__version__ = "0.14.0"

logger = get_logger(name="langfuse-agent")
logger.setLevel(logging.INFO)


def register_langfuse_observability_tools(mcp: FastMCP):
    @mcp.tool(tags=["langfuse"])
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


def register_langfuse_datasets_tools(mcp: FastMCP):
    @mcp.tool(tags=["langfuse"])
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


def register_langfuse_prompts_models_tools(mcp: FastMCP):
    @mcp.tool(tags=["langfuse"])
    async def langfuse_prompts_models(
        action: str = Field(
            description="Action to perform. Must be one of: llm_connections_list, llm_connections_upsert, media_get, media_patch, media_get_upload_url, models_create, models_list, models_get, models_delete, prompt_version_update, prompts_get, prompts_delete, prompts_list, prompts_create"
        ),
        body: Any = Field(default=None, description="body"),
        from_updated_at: Any = Field(default=None, description="from updated at"),
        id: Any = Field(default=None, description="id"),
        label: Any = Field(default=None, description="label"),
        limit: Any = Field(default=None, description="limit"),
        media_id: Any = Field(default=None, description="media id"),
        name: Any = Field(default=None, description="name"),
        new_labels: Any = Field(default=None, description="new labels"),
        page: Any = Field(default=None, description="page"),
        prompt_name: Any = Field(default=None, description="prompt name"),
        resolve: Any = Field(default=None, description="resolve"),
        tag: Any = Field(default=None, description="tag"),
        to_updated_at: Any = Field(default=None, description="to updated at"),
        version: Any = Field(default=None, description="version"),
    ) -> Any:
        """Perform langfuse_prompts_models operations."""
        client = get_client()
        kwargs = {}
        if body is not None:
            kwargs["body"] = body
        if from_updated_at is not None:
            kwargs["from_updated_at"] = from_updated_at
        if id is not None:
            kwargs["id"] = id
        if label is not None:
            kwargs["label"] = label
        if limit is not None:
            kwargs["limit"] = limit
        if media_id is not None:
            kwargs["media_id"] = media_id
        if name is not None:
            kwargs["name"] = name
        if new_labels is not None:
            kwargs["new_labels"] = new_labels
        if page is not None:
            kwargs["page"] = page
        if prompt_name is not None:
            kwargs["prompt_name"] = prompt_name
        if resolve is not None:
            kwargs["resolve"] = resolve
        if tag is not None:
            kwargs["tag"] = tag
        if to_updated_at is not None:
            kwargs["to_updated_at"] = to_updated_at
        if version is not None:
            kwargs["version"] = version

        if action == "llm_connections_list":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["page", "limit"]}
            return client.llm_connections_list(**method_kwargs)
        elif action == "llm_connections_upsert":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["body"]}
            return client.llm_connections_upsert(**method_kwargs)
        elif action == "media_get":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["media_id"]}
            return client.media_get(**method_kwargs)
        elif action == "media_patch":
            method_kwargs = {
                k: v for k, v in kwargs.items() if k in ["media_id", "body"]
            }
            return client.media_patch(**method_kwargs)
        elif action == "media_get_upload_url":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["body"]}
            return client.media_get_upload_url(**method_kwargs)
        elif action == "models_create":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["body"]}
            return client.models_create(**method_kwargs)
        elif action == "models_list":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["page", "limit"]}
            return client.models_list(**method_kwargs)
        elif action == "models_get":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["id"]}
            return client.models_get(**method_kwargs)
        elif action == "models_delete":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["id"]}
            return client.models_delete(**method_kwargs)
        elif action == "prompt_version_update":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k in ["name", "version", "new_labels"]
            }
            return client.prompt_version_update(**method_kwargs)
        elif action == "prompts_get":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k in ["prompt_name", "version", "label", "resolve"]
            }
            return client.prompts_get(**method_kwargs)
        elif action == "prompts_delete":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k in ["prompt_name", "label", "version"]
            }
            return client.prompts_delete(**method_kwargs)
        elif action == "prompts_list":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k
                in [
                    "name",
                    "label",
                    "tag",
                    "page",
                    "limit",
                    "from_updated_at",
                    "to_updated_at",
                ]
            }
            return client.prompts_list(**method_kwargs)
        elif action == "prompts_create":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["body"]}
            return client.prompts_create(**method_kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")


def register_langfuse_management_tools(mcp: FastMCP):
    @mcp.tool(tags=["langfuse"])
    async def langfuse_management(
        action: str = Field(
            description="Action to perform. Must be one of: blob_storage_integrations_get_blob_storage_integrations, blob_storage_integrations_upsert_blob_storage_integration, blob_storage_integrations_get_blob_storage_integration_status, blob_storage_integrations_delete_blob_storage_integration, comments_create, comments_get, comments_get_by_id, health_health, organizations_get_organization_memberships, organizations_update_organization_membership, organizations_delete_organization_membership, organizations_get_project_memberships, organizations_update_project_membership, organizations_delete_project_membership, organizations_get_organization_projects, organizations_get_organization_api_keys, projects_get, projects_create, projects_update, projects_delete, projects_get_api_keys, projects_create_api_key, projects_delete_api_key, scim_get_service_provider_config, scim_get_resource_types, scim_get_schemas, scim_list_users, scim_create_user, scim_get_user, scim_delete_user"
        ),
        active: Any = Field(default=None, description="active"),
        api_key_id: Any = Field(default=None, description="api key id"),
        author_user_id: Any = Field(default=None, description="author user id"),
        body: Any = Field(default=None, description="body"),
        comment_id: Any = Field(default=None, description="comment id"),
        count: Any = Field(default=None, description="count"),
        emails: Any = Field(default=None, description="emails"),
        filter: Any = Field(default=None, description="filter"),
        id: Any = Field(default=None, description="id"),
        limit: Any = Field(default=None, description="limit"),
        metadata: Any = Field(default=None, description="metadata"),
        name: Any = Field(default=None, description="name"),
        note: Any = Field(default=None, description="note"),
        object_id: Any = Field(default=None, description="object id"),
        object_type: Any = Field(default=None, description="object type"),
        page: Any = Field(default=None, description="page"),
        password: Any = Field(default=None, description="password"),
        project_id: Any = Field(default=None, description="project id"),
        public_key: Any = Field(default=None, description="public key"),
        retention: Any = Field(default=None, description="retention"),
        secret_key: Any = Field(default=None, description="secret key"),
        start_index: Any = Field(default=None, description="start index"),
        user_id: Any = Field(default=None, description="user id"),
        user_name: Any = Field(default=None, description="user name"),
    ) -> Any:
        """Perform langfuse_management operations."""
        client = get_client()
        kwargs = {}
        if active is not None:
            kwargs["active"] = active
        if api_key_id is not None:
            kwargs["api_key_id"] = api_key_id
        if author_user_id is not None:
            kwargs["author_user_id"] = author_user_id
        if body is not None:
            kwargs["body"] = body
        if comment_id is not None:
            kwargs["comment_id"] = comment_id
        if count is not None:
            kwargs["count"] = count
        if emails is not None:
            kwargs["emails"] = emails
        if filter is not None:
            kwargs["filter"] = filter
        if id is not None:
            kwargs["id"] = id
        if limit is not None:
            kwargs["limit"] = limit
        if metadata is not None:
            kwargs["metadata"] = metadata
        if name is not None:
            kwargs["name"] = name
        if note is not None:
            kwargs["note"] = note
        if object_id is not None:
            kwargs["object_id"] = object_id
        if object_type is not None:
            kwargs["object_type"] = object_type
        if page is not None:
            kwargs["page"] = page
        if password is not None:
            kwargs["password"] = password
        if project_id is not None:
            kwargs["project_id"] = project_id
        if public_key is not None:
            kwargs["public_key"] = public_key
        if retention is not None:
            kwargs["retention"] = retention
        if secret_key is not None:
            kwargs["secret_key"] = secret_key
        if start_index is not None:
            kwargs["start_index"] = start_index
        if user_id is not None:
            kwargs["user_id"] = user_id
        if user_name is not None:
            kwargs["user_name"] = user_name

        if action == "blob_storage_integrations_get_blob_storage_integrations":
            return client.blob_storage_integrations_get_blob_storage_integrations()
        elif action == "blob_storage_integrations_upsert_blob_storage_integration":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["body"]}
            return client.blob_storage_integrations_upsert_blob_storage_integration(
                **method_kwargs
            )
        elif action == "blob_storage_integrations_get_blob_storage_integration_status":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["id"]}
            return client.blob_storage_integrations_get_blob_storage_integration_status(
                **method_kwargs
            )
        elif action == "blob_storage_integrations_delete_blob_storage_integration":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["id"]}
            return client.blob_storage_integrations_delete_blob_storage_integration(
                **method_kwargs
            )
        elif action == "comments_create":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["body"]}
            return client.comments_create(**method_kwargs)
        elif action == "comments_get":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k in ["page", "limit", "object_type", "object_id", "author_user_id"]
            }
            return client.comments_get(**method_kwargs)
        elif action == "comments_get_by_id":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["comment_id"]}
            return client.comments_get_by_id(**method_kwargs)
        elif action == "health_health":
            return client.health_health()
        elif action == "organizations_get_organization_memberships":
            return client.organizations_get_organization_memberships()
        elif action == "organizations_update_organization_membership":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["body"]}
            return client.organizations_update_organization_membership(**method_kwargs)
        elif action == "organizations_delete_organization_membership":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["body"]}
            return client.organizations_delete_organization_membership(**method_kwargs)
        elif action == "organizations_get_project_memberships":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["project_id"]}
            return client.organizations_get_project_memberships(**method_kwargs)
        elif action == "organizations_update_project_membership":
            method_kwargs = {
                k: v for k, v in kwargs.items() if k in ["project_id", "body"]
            }
            return client.organizations_update_project_membership(**method_kwargs)
        elif action == "organizations_delete_project_membership":
            method_kwargs = {
                k: v for k, v in kwargs.items() if k in ["project_id", "body"]
            }
            return client.organizations_delete_project_membership(**method_kwargs)
        elif action == "organizations_get_organization_projects":
            return client.organizations_get_organization_projects()
        elif action == "organizations_get_organization_api_keys":
            return client.organizations_get_organization_api_keys()
        elif action == "projects_get":
            return client.projects_get()
        elif action == "projects_create":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k in ["name", "retention", "metadata"]
            }
            return client.projects_create(**method_kwargs)
        elif action == "projects_update":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k in ["project_id", "name", "metadata", "retention"]
            }
            return client.projects_update(**method_kwargs)
        elif action == "projects_delete":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["project_id"]}
            return client.projects_delete(**method_kwargs)
        elif action == "projects_get_api_keys":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["project_id"]}
            return client.projects_get_api_keys(**method_kwargs)
        elif action == "projects_create_api_key":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k in ["project_id", "note", "public_key", "secret_key"]
            }
            return client.projects_create_api_key(**method_kwargs)
        elif action == "projects_delete_api_key":
            method_kwargs = {
                k: v for k, v in kwargs.items() if k in ["project_id", "api_key_id"]
            }
            return client.projects_delete_api_key(**method_kwargs)
        elif action == "scim_get_service_provider_config":
            return client.scim_get_service_provider_config()
        elif action == "scim_get_resource_types":
            return client.scim_get_resource_types()
        elif action == "scim_get_schemas":
            return client.scim_get_schemas()
        elif action == "scim_list_users":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k in ["filter", "start_index", "count"]
            }
            return client.scim_list_users(**method_kwargs)
        elif action == "scim_create_user":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k in ["user_name", "name", "emails", "active", "password"]
            }
            return client.scim_create_user(**method_kwargs)
        elif action == "scim_get_user":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["user_id"]}
            return client.scim_get_user(**method_kwargs)
        elif action == "scim_delete_user":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["user_id"]}
            return client.scim_delete_user(**method_kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")


def get_mcp_instance():
    args, mcp, middlewares = create_mcp_server(
        name="langfuse",
        version=__version__,
        instructions="langfuse-agent MCP Server — Condensed Action-Routed Tools.",
    )
    DEFAULT_OBSERVABILITYTOOL = to_boolean(os.getenv("OBSERVABILITY_TOOL", "True"))
    if DEFAULT_OBSERVABILITYTOOL:
        register_langfuse_observability_tools(mcp)
    DEFAULT_DATASETSTOOL = to_boolean(os.getenv("DATASETS_TOOL", "True"))
    if DEFAULT_DATASETSTOOL:
        register_langfuse_datasets_tools(mcp)
    DEFAULT_PROMPTSMODELSTOOL = to_boolean(os.getenv("PROMPTS_MODELS_TOOL", "True"))
    if DEFAULT_PROMPTSMODELSTOOL:
        register_langfuse_prompts_models_tools(mcp)
    DEFAULT_MANAGEMENTTOOL = to_boolean(os.getenv("MANAGEMENT_TOOL", "True"))
    if DEFAULT_MANAGEMENTTOOL:
        register_langfuse_management_tools(mcp)

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
