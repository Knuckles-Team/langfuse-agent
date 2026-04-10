import warnings

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning
        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

# General urllib3/chardet mismatch warnings
warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import os
import sys
import logging
from typing import Any, Dict, Optional
from fastmcp import FastMCP

__version__ = "0.1.6"

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import create_mcp_server
from .auth import get_client

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def register_prompts(mcp: FastMCP):
    @mcp.prompt(
        name="langfuse-system-summary",
        description="Get a summary of the Langfuse application.",
    )
    def langfuse_system_summary() -> str:
        return "Check Langfuse metrics, traces, and available annotation queues."


### BEGIN GENERATED TOOL REGISTRATION ###


### BEGIN GENERATED TOOL REGISTRATION ###


def register_annotation_queues_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-annotation-queues-annotation-queues-list-queues",
        description="Get all annotation queues",
        tags={"annotation_queues"},
    )
    def annotation_queues_list_queues(
        page: Optional[int] = None, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        return get_client().annotation_queues_list_queues(page, limit)

    @mcp.tool(
        name="langfuse-annotation-queues-annotation-queues-create-queue",
        description="Create an annotation queue",
        tags={"annotation_queues"},
    )
    def annotation_queues_create_queue(body: dict) -> Dict[str, Any]:
        return get_client().annotation_queues_create_queue(body)

    @mcp.tool(
        name="langfuse-annotation-queues-annotation-queues-get-queue",
        description="Get an annotation queue by ID",
        tags={"annotation_queues"},
    )
    def annotation_queues_get_queue(queue_id: str) -> Dict[str, Any]:
        return get_client().annotation_queues_get_queue(queue_id)

    @mcp.tool(
        name="langfuse-annotation-queues-annotation-queues-list-queue-items",
        description="Get items for a specific annotation queue",
        tags={"annotation_queues"},
    )
    def annotation_queues_list_queue_items(
        queue_id: str,
        status: Optional[Any] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        return get_client().annotation_queues_list_queue_items(
            queue_id, status, page, limit
        )

    @mcp.tool(
        name="langfuse-annotation-queues-annotation-queues-create-queue-item",
        description="Add an item to an annotation queue",
        tags={"annotation_queues"},
    )
    def annotation_queues_create_queue_item(
        queue_id: str, body: dict
    ) -> Dict[str, Any]:
        return get_client().annotation_queues_create_queue_item(queue_id, body)

    @mcp.tool(
        name="langfuse-annotation-queues-annotation-queues-get-queue-item",
        description="Get a specific item from an annotation queue",
        tags={"annotation_queues"},
    )
    def annotation_queues_get_queue_item(queue_id: str, item_id: str) -> Dict[str, Any]:
        return get_client().annotation_queues_get_queue_item(queue_id, item_id)

    @mcp.tool(
        name="langfuse-annotation-queues-annotation-queues-update-queue-item",
        description="Update an annotation queue item",
        tags={"annotation_queues"},
    )
    def annotation_queues_update_queue_item(
        queue_id: str, item_id: str, body: dict
    ) -> Dict[str, Any]:
        return get_client().annotation_queues_update_queue_item(queue_id, item_id, body)

    @mcp.tool(
        name="langfuse-annotation-queues-annotation-queues-delete-queue-item",
        description="Remove an item from an annotation queue",
        tags={"annotation_queues"},
    )
    def annotation_queues_delete_queue_item(
        queue_id: str, item_id: str
    ) -> Dict[str, Any]:
        return get_client().annotation_queues_delete_queue_item(queue_id, item_id)

    @mcp.tool(
        name="langfuse-annotation-queues-annotation-queues-create-queue-assignment",
        description="Create an assignment for a user to an annotation queue",
        tags={"annotation_queues"},
    )
    def annotation_queues_create_queue_assignment(
        queue_id: str, body: dict
    ) -> Dict[str, Any]:
        return get_client().annotation_queues_create_queue_assignment(queue_id, body)

    @mcp.tool(
        name="langfuse-annotation-queues-annotation-queues-delete-queue-assignment",
        description="Delete an assignment for a user to an annotation queue",
        tags={"annotation_queues"},
    )
    def annotation_queues_delete_queue_assignment(
        queue_id: str, body: dict
    ) -> Dict[str, Any]:
        return get_client().annotation_queues_delete_queue_assignment(queue_id, body)


def register_blob_storage_integrations_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-blob-storage-integrations-blob-storage-integrations-get-blob-storage-integrations",
        description="Get all blob storage integrations for the organization (requires organization-scoped API key)",
        tags={"blob_storage_integrations"},
    )
    def blob_storage_integrations_get_blob_storage_integrations() -> Dict[str, Any]:
        return get_client().blob_storage_integrations_get_blob_storage_integrations()

    @mcp.tool(
        name="langfuse-blob-storage-integrations-blob-storage-integrations-upsert-blob-storage-integration",
        description="Create or update a blob storage integration for a specific project (requires organization-scoped API key). The configuration is validated by performing a test upload to the bucket.",
        tags={"blob_storage_integrations"},
    )
    def blob_storage_integrations_upsert_blob_storage_integration(
        body: dict,
    ) -> Dict[str, Any]:
        return get_client().blob_storage_integrations_upsert_blob_storage_integration(
            body
        )

    @mcp.tool(
        name="langfuse-blob-storage-integrations-blob-storage-integrations-get-blob-storage-integration-status",
        description="Get the sync status of a blob storage integration by integration ID (requires organization-scoped API key)",
        tags={"blob_storage_integrations"},
    )
    def blob_storage_integrations_get_blob_storage_integration_status(
        id: str,
    ) -> Dict[str, Any]:
        return (
            get_client().blob_storage_integrations_get_blob_storage_integration_status(
                id
            )
        )

    @mcp.tool(
        name="langfuse-blob-storage-integrations-blob-storage-integrations-delete-blob-storage-integration",
        description="Delete a blob storage integration by ID (requires organization-scoped API key)",
        tags={"blob_storage_integrations"},
    )
    def blob_storage_integrations_delete_blob_storage_integration(
        id: str,
    ) -> Dict[str, Any]:
        return get_client().blob_storage_integrations_delete_blob_storage_integration(
            id
        )


def register_comments_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-comments-create",
        description="Create a comment. Comments may be attached to different object types (trace, observation, session, prompt).",
        tags={"comments"},
    )
    def comments_create(body: dict) -> Dict[str, Any]:
        return get_client().comments_create(body)

    @mcp.tool(
        name="langfuse-comments-get", description="Get all comments", tags={"comments"}
    )
    def comments_get(
        page: Optional[int] = None,
        limit: Optional[int] = None,
        object_type: Optional[str] = None,
        object_id: Optional[str] = None,
        author_user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        return get_client().comments_get(
            page, limit, object_type, object_id, author_user_id
        )

    @mcp.tool(
        name="langfuse-comments-get-by-id",
        description="Get a comment by id",
        tags={"comments"},
    )
    def comments_get_by_id(comment_id: str) -> Dict[str, Any]:
        return get_client().comments_get_by_id(comment_id)


def register_dataset_items_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-dataset-items-dataset-items-create",
        description="Create a dataset item",
        tags={"dataset_items"},
    )
    def dataset_items_create(body: dict) -> Dict[str, Any]:
        return get_client().dataset_items_create(body)

    @mcp.tool(
        name="langfuse-dataset-items-dataset-items-list",
        description="Get dataset items. Optionally specify a version to get the items as they existed at that point in time. Note: If version parameter is provided, datasetName must also be provided.",
        tags={"dataset_items"},
    )
    def dataset_items_list(
        dataset_name: Optional[str] = None,
        source_trace_id: Optional[str] = None,
        source_observation_id: Optional[str] = None,
        version: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        return get_client().dataset_items_list(
            dataset_name, source_trace_id, source_observation_id, version, page, limit
        )

    @mcp.tool(
        name="langfuse-dataset-items-dataset-items-get",
        description="Get a dataset item",
        tags={"dataset_items"},
    )
    def dataset_items_get(id: str) -> Dict[str, Any]:
        return get_client().dataset_items_get(id)

    @mcp.tool(
        name="langfuse-dataset-items-dataset-items-delete",
        description="Delete a dataset item and all its run items. This action is irreversible.",
        tags={"dataset_items"},
    )
    def dataset_items_delete(id: str) -> Dict[str, Any]:
        return get_client().dataset_items_delete(id)


def register_dataset_run_items_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-dataset-run-items-dataset-run-items-create",
        description="Create a dataset run item",
        tags={"dataset_run_items"},
    )
    def dataset_run_items_create(body: dict) -> Dict[str, Any]:
        return get_client().dataset_run_items_create(body)

    @mcp.tool(
        name="langfuse-dataset-run-items-dataset-run-items-list",
        description="List dataset run items",
        tags={"dataset_run_items"},
    )
    def dataset_run_items_list(
        dataset_id: str,
        run_name: str,
        page: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        return get_client().dataset_run_items_list(dataset_id, run_name, page, limit)


def register_datasets_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-datasets-list", description="Get all datasets", tags={"datasets"}
    )
    def datasets_list(
        page: Optional[int] = None, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        return get_client().datasets_list(page, limit)

    @mcp.tool(
        name="langfuse-datasets-create",
        description="Create a dataset",
        tags={"datasets"},
    )
    def datasets_create(body: dict) -> Dict[str, Any]:
        return get_client().datasets_create(body)

    @mcp.tool(
        name="langfuse-datasets-get", description="Get a dataset", tags={"datasets"}
    )
    def datasets_get(dataset_name: str) -> Dict[str, Any]:
        return get_client().datasets_get(dataset_name)

    @mcp.tool(
        name="langfuse-datasets-get-run",
        description="Get a dataset run and its items",
        tags={"datasets"},
    )
    def datasets_get_run(dataset_name: str, run_name: str) -> Dict[str, Any]:
        return get_client().datasets_get_run(dataset_name, run_name)

    @mcp.tool(
        name="langfuse-datasets-delete-run",
        description="Delete a dataset run and all its run items. This action is irreversible.",
        tags={"datasets"},
    )
    def datasets_delete_run(dataset_name: str, run_name: str) -> Dict[str, Any]:
        return get_client().datasets_delete_run(dataset_name, run_name)

    @mcp.tool(
        name="langfuse-datasets-get-runs",
        description="Get dataset runs",
        tags={"datasets"},
    )
    def datasets_get_runs(
        dataset_name: str, page: Optional[int] = None, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        return get_client().datasets_get_runs(dataset_name, page, limit)


def register_health_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-health-health",
        description="Check health of API and database",
        tags={"health"},
    )
    def health_health() -> Dict[str, Any]:
        return get_client().health_health()


def register_ingestion_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-ingestion-batch",
        description='**Legacy endpoint for batch ingestion for Langfuse Observability.**  -> Please use the OpenTelemetry endpoint (`/api/public/otel/v1/traces`). Learn more: https://langfuse.com/integrations/native/opentelemetry  Within each batch, there can be multiple events. Each event has a type, an id, a timestamp, metadata and a body. Internally, we refer to this as the "event envelope" as it tells us something about the event but not the trace. We use the event id within this envelope to deduplicate messages to avoid processing the same event twice, i.e. the event id should be unique per request. The event.body.id is the ID of the actual trace and will be used for updates and will be visible within the Langfuse App. I.e. if you want to update a trace, you\'d use the same body id, but separate event IDs.  Notes: - Introduction to data model: https://langfuse.com/docs/observability/data-model - Batch sizes are limited to 3.5 MB in total. You need to adjust the number of events per batch accordingly. - The API does not return a 4xx status code for input errors. Instead, it responds with a 207 status code, which includes a list of the encountered errors.',
        tags={"ingestion"},
    )
    def ingestion_batch(batch: list, metadata: Optional[Any] = None) -> Dict[str, Any]:
        return get_client().ingestion_batch(batch, metadata)


def register_legacy_metrics_v1_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-legacy-metrics-v1-legacy-metrics-v1-metrics",
        description="Get metrics from the Langfuse project using a query object.  Consider using the [v2 metrics endpoint](/api-reference#tag/metricsv2/GET/api/public/v2/metrics) for better performance.  For more details, see the [Metrics API documentation](https://langfuse.com/docs/metrics/features/metrics-api).",
        tags={"legacy_metrics_v1"},
    )
    def legacy_metrics_v1_metrics(query: str) -> Dict[str, Any]:
        return get_client().legacy_metrics_v1_metrics(query)


def register_legacy_observations_v1_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-legacy-observations-v1-legacy-observations-v1-get",
        description="Get a observation",
        tags={"legacy_observations_v1"},
    )
    def legacy_observations_v1_get(observation_id: str) -> Dict[str, Any]:
        return get_client().legacy_observations_v1_get(observation_id)

    @mcp.tool(
        name="langfuse-legacy-observations-v1-legacy-observations-v1-get-many",
        description="Get a list of observations.  Consider using the [v2 observations endpoint](/api-reference#tag/observationsv2/GET/api/public/v2/observations) for cursor-based pagination and field selection.",
        tags={"legacy_observations_v1"},
    )
    def legacy_observations_v1_get_many(
        page: Optional[int] = None,
        limit: Optional[int] = None,
        name: Optional[str] = None,
        user_id: Optional[str] = None,
        type: Optional[str] = None,
        trace_id: Optional[str] = None,
        level: Optional[Any] = None,
        parent_observation_id: Optional[str] = None,
        environment: Optional[list] = None,
        from_start_time: Optional[str] = None,
        to_start_time: Optional[str] = None,
        version: Optional[str] = None,
        filter: Optional[str] = None,
    ) -> Dict[str, Any]:
        return get_client().legacy_observations_v1_get_many(
            page,
            limit,
            name,
            user_id,
            type,
            trace_id,
            level,
            parent_observation_id,
            environment,
            from_start_time,
            to_start_time,
            version,
            filter,
        )


def register_legacy_score_v1_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-legacy-score-v1-legacy-score-v1-create",
        description="Create a score (supports both trace and session scores)",
        tags={"legacy_score_v1"},
    )
    def legacy_score_v1_create(body: dict) -> Dict[str, Any]:
        return get_client().legacy_score_v1_create(body)

    @mcp.tool(
        name="langfuse-legacy-score-v1-legacy-score-v1-delete",
        description="Delete a score (supports both trace and session scores)",
        tags={"legacy_score_v1"},
    )
    def legacy_score_v1_delete(score_id: str) -> Dict[str, Any]:
        return get_client().legacy_score_v1_delete(score_id)


def register_llm_connections_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-llm-connections-llm-connections-list",
        description="Get all LLM connections in a project",
        tags={"llm_connections"},
    )
    def llm_connections_list(
        page: Optional[int] = None, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        return get_client().llm_connections_list(page, limit)

    @mcp.tool(
        name="langfuse-llm-connections-llm-connections-upsert",
        description="Create or update an LLM connection. The connection is upserted on provider.",
        tags={"llm_connections"},
    )
    def llm_connections_upsert(body: dict) -> Dict[str, Any]:
        return get_client().llm_connections_upsert(body)


def register_media_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-media-get", description="Get a media record", tags={"media"}
    )
    def media_get(media_id: str) -> Dict[str, Any]:
        return get_client().media_get(media_id)

    @mcp.tool(
        name="langfuse-media-patch", description="Patch a media record", tags={"media"}
    )
    def media_patch(media_id: str, body: dict) -> Dict[str, Any]:
        return get_client().media_patch(media_id, body)

    @mcp.tool(
        name="langfuse-media-get-upload-url",
        description="Get a presigned upload URL for a media record",
        tags={"media"},
    )
    def media_get_upload_url(body: dict) -> Dict[str, Any]:
        return get_client().media_get_upload_url(body)


def register_metrics_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-metrics-metrics",
        description="Get metrics from the Langfuse project using a query object. V2 endpoint with optimized performance.  ## V2 Differences - Supports `observations`, `scores-numeric`, and `scores-categorical` views only (traces view not supported) - Direct access to tags and release fields on observations - Backwards-compatible: traceName, traceRelease, traceVersion dimensions are still available on observations view - High cardinality dimensions are not supported and will return a 400 error (see below)  For more details, see the [Metrics API documentation](https://langfuse.com/docs/metrics/features/metrics-api).  ## Available Views  ### observations Query observation-level data (spans, generations, events).  **Dimensions:** - `environment` - Deployment environment (e.g., production, staging) - `type` - Type of observation (SPAN, GENERATION, EVENT) - `name` - Name of the observation - `level` - Logging level of the observation - `version` - Version of the observation - `tags` - User-defined tags - `release` - Release version - `traceName` - Name of the parent trace (backwards-compatible) - `traceRelease` - Release version of the parent trace (backwards-compatible, maps to release) - `traceVersion` - Version of the parent trace (backwards-compatible, maps to version) - `providedModelName` - Name of the model used - `promptName` - Name of the prompt used - `promptVersion` - Version of the prompt used - `startTimeMonth` - Month of start_time in YYYY-MM format  **Measures:** - `count` - Total number of observations - `latency` - Observation latency (milliseconds) - `streamingLatency` - Generation latency from completion start to end (milliseconds) - `inputTokens` - Sum of input tokens consumed - `outputTokens` - Sum of output tokens produced - `totalTokens` - Sum of all tokens consumed - `outputTokensPerSecond` - Output tokens per second - `tokensPerSecond` - Total tokens per second - `inputCost` - Input cost (USD) - `outputCost` - Output cost (USD) - `totalCost` - Total cost (USD) - `timeToFirstToken` - Time to first token (milliseconds) - `countScores` - Number of scores attached to the observation  ### scores-numeric Query numeric and boolean score data.  **Dimensions:** - `environment` - Deployment environment - `name` - Name of the score (e.g., accuracy, toxicity) - `source` - Origin of the score (API, ANNOTATION, EVAL) - `dataType` - Data type (NUMERIC, BOOLEAN) - `configId` - Identifier of the score config - `timestampMonth` - Month in YYYY-MM format - `timestampDay` - Day in YYYY-MM-DD format - `value` - Numeric value of the score - `traceName` - Name of the parent trace - `tags` - Tags - `traceRelease` - Release version - `traceVersion` - Version - `observationName` - Name of the associated observation - `observationModelName` - Model name of the associated observation - `observationPromptName` - Prompt name of the associated observation - `observationPromptVersion` - Prompt version of the associated observation  **Measures:** - `count` - Total number of scores - `value` - Score value (for aggregations)  ### scores-categorical Query categorical score data. Same dimensions as scores-numeric except uses `stringValue` instead of `value`.  **Measures:** - `count` - Total number of scores  ## High Cardinality Dimensions The following dimensions cannot be used as grouping dimensions in v2 metrics API as they can cause performance issues. Use them in filters instead.  **observations view:** - `id` - Use traceId filter to narrow down results - `traceId` - Use traceId filter instead - `userId` - Use userId filter instead - `sessionId` - Use sessionId filter instead - `parentObservationId` - Use parentObservationId filter instead  **scores-numeric / scores-categorical views:** - `id` - Use specific filters to narrow down results - `traceId` - Use traceId filter instead - `userId` - Use userId filter instead - `sessionId` - Use sessionId filter instead - `observationId` - Use observationId filter instead  ## Aggregations Available aggregation functions: `sum`, `avg`, `count`, `max`, `min`, `p50`, `p75`, `p90`, `p95`, `p99`, `histogram`  ## Time Granularities Available granularities for timeDimension: `auto`, `minute`, `hour`, `day`, `week`, `month` - `auto` bins the data into approximately 50 buckets based on the time range",
        tags={"metrics"},
    )
    def metrics_metrics(query: str) -> Dict[str, Any]:
        return get_client().metrics_metrics(query)


def register_models_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-models-create", description="Create a model", tags={"models"}
    )
    def models_create(body: dict) -> Dict[str, Any]:
        return get_client().models_create(body)

    @mcp.tool(
        name="langfuse-models-list", description="Get all models", tags={"models"}
    )
    def models_list(
        page: Optional[int] = None, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        return get_client().models_list(page, limit)

    @mcp.tool(name="langfuse-models-get", description="Get a model", tags={"models"})
    def models_get(id: str) -> Dict[str, Any]:
        return get_client().models_get(id)

    @mcp.tool(
        name="langfuse-models-delete",
        description="Delete a model. Cannot delete models managed by Langfuse. You can create your own definition with the same modelName to override the definition though.",
        tags={"models"},
    )
    def models_delete(id: str) -> Dict[str, Any]:
        return get_client().models_delete(id)


def register_observations_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-observations-get-many",
        description="Get a list of observations with cursor-based pagination and flexible field selection.  ## Cursor-based Pagination This endpoint uses cursor-based pagination for efficient traversal of large datasets. The cursor is returned in the response metadata and should be passed in subsequent requests to retrieve the next page of results.  ## Field Selection Use the `fields` parameter to control which observation fields are returned: - `core` - Always included: id, traceId, startTime, endTime, projectId, parentObservationId, type - `basic` - name, level, statusMessage, version, environment, bookmarked, public, userId, sessionId - `time` - completionStartTime, createdAt, updatedAt - `io` - input, output - `metadata` - metadata (truncated to 200 chars by default, use `expandMetadata` to get full values) - `model` - providedModelName, internalModelId, modelParameters - `usage` - usageDetails, costDetails, totalCost - `prompt` - promptId, promptName, promptVersion - `metrics` - latency, timeToFirstToken  If not specified, `core` and `basic` field groups are returned.  ## Filters Multiple filtering options are available via query parameters or the structured `filter` parameter. When using the `filter` parameter, it takes precedence over individual query parameter filters.",
        tags={"observations"},
    )
    def observations_get_many(
        fields: Optional[str] = None,
        expand_metadata: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        parse_io_as_json: Optional[bool] = None,
        name: Optional[str] = None,
        user_id: Optional[str] = None,
        type: Optional[str] = None,
        trace_id: Optional[str] = None,
        level: Optional[Any] = None,
        parent_observation_id: Optional[str] = None,
        environment: Optional[list] = None,
        from_start_time: Optional[str] = None,
        to_start_time: Optional[str] = None,
        version: Optional[str] = None,
        filter: Optional[str] = None,
    ) -> Dict[str, Any]:
        return get_client().observations_get_many(
            fields,
            expand_metadata,
            limit,
            cursor,
            parse_io_as_json,
            name,
            user_id,
            type,
            trace_id,
            level,
            parent_observation_id,
            environment,
            from_start_time,
            to_start_time,
            version,
            filter,
        )


def register_opentelemetry_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-opentelemetry-export-traces",
        description="**OpenTelemetry Traces Ingestion Endpoint**  This endpoint implements the OTLP/HTTP specification for trace ingestion, providing native OpenTelemetry integration for Langfuse Observability.  **Supported Formats:** - Binary Protobuf: `Content-Type: application/x-protobuf` - JSON Protobuf: `Content-Type: application/json` - Supports gzip compression via `Content-Encoding: gzip` header  **Specification Compliance:** - Conforms to [OTLP/HTTP Trace Export](https://opentelemetry.io/docs/specs/otlp/#otlphttp) - Implements `ExportTraceServiceRequest` message format  **Documentation:** - Integration guide: https://langfuse.com/integrations/native/opentelemetry - Data model: https://langfuse.com/docs/observability/data-model",
        tags={"opentelemetry"},
    )
    def opentelemetry_export_traces(resource_spans: list) -> Dict[str, Any]:
        return get_client().opentelemetry_export_traces(resource_spans)


def register_organizations_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-organizations-get-organization-memberships",
        description="Get all memberships for the organization associated with the API key (requires organization-scoped API key)",
        tags={"organizations"},
    )
    def organizations_get_organization_memberships() -> Dict[str, Any]:
        return get_client().organizations_get_organization_memberships()

    @mcp.tool(
        name="langfuse-organizations-update-organization-membership",
        description="Create or update a membership for the organization associated with the API key (requires organization-scoped API key)",
        tags={"organizations"},
    )
    def organizations_update_organization_membership(body: dict) -> Dict[str, Any]:
        return get_client().organizations_update_organization_membership(body)

    @mcp.tool(
        name="langfuse-organizations-delete-organization-membership",
        description="Delete a membership from the organization associated with the API key (requires organization-scoped API key)",
        tags={"organizations"},
    )
    def organizations_delete_organization_membership(body: dict) -> Dict[str, Any]:
        return get_client().organizations_delete_organization_membership(body)

    @mcp.tool(
        name="langfuse-organizations-get-project-memberships",
        description="Get all memberships for a specific project (requires organization-scoped API key)",
        tags={"organizations"},
    )
    def organizations_get_project_memberships(project_id: str) -> Dict[str, Any]:
        return get_client().organizations_get_project_memberships(project_id)

    @mcp.tool(
        name="langfuse-organizations-update-project-membership",
        description="Create or update a membership for a specific project (requires organization-scoped API key). The user must already be a member of the organization.",
        tags={"organizations"},
    )
    def organizations_update_project_membership(
        project_id: str, body: dict
    ) -> Dict[str, Any]:
        return get_client().organizations_update_project_membership(project_id, body)

    @mcp.tool(
        name="langfuse-organizations-delete-project-membership",
        description="Delete a membership from a specific project (requires organization-scoped API key). The user must be a member of the organization.",
        tags={"organizations"},
    )
    def organizations_delete_project_membership(
        project_id: str, body: dict
    ) -> Dict[str, Any]:
        return get_client().organizations_delete_project_membership(project_id, body)

    @mcp.tool(
        name="langfuse-organizations-get-organization-projects",
        description="Get all projects for the organization associated with the API key (requires organization-scoped API key)",
        tags={"organizations"},
    )
    def organizations_get_organization_projects() -> Dict[str, Any]:
        return get_client().organizations_get_organization_projects()

    @mcp.tool(
        name="langfuse-organizations-get-organization-api-keys",
        description="Get all API keys for the organization associated with the API key (requires organization-scoped API key)",
        tags={"organizations"},
    )
    def organizations_get_organization_api_keys() -> Dict[str, Any]:
        return get_client().organizations_get_organization_api_keys()


def register_projects_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-projects-get",
        description="Get Project associated with API key (requires project-scoped API key). You can use GET /api/public/organizations/projects to get all projects with an organization-scoped key.",
        tags={"projects"},
    )
    def projects_get() -> Dict[str, Any]:
        return get_client().projects_get()

    @mcp.tool(
        name="langfuse-projects-create",
        description="Create a new project (requires organization-scoped API key)",
        tags={"projects"},
    )
    def projects_create(
        name: str, retention: int, metadata: Optional[dict] = None
    ) -> Dict[str, Any]:
        return get_client().projects_create(name, retention, metadata)

    @mcp.tool(
        name="langfuse-projects-update",
        description="Update a project by ID (requires organization-scoped API key).",
        tags={"projects"},
    )
    def projects_update(
        project_id: str,
        name: str,
        metadata: Optional[dict] = None,
        retention: Optional[int] = None,
    ) -> Dict[str, Any]:
        return get_client().projects_update(project_id, name, metadata, retention)

    @mcp.tool(
        name="langfuse-projects-delete",
        description="Delete a project by ID (requires organization-scoped API key). Project deletion is processed asynchronously.",
        tags={"projects"},
    )
    def projects_delete(project_id: str) -> Dict[str, Any]:
        return get_client().projects_delete(project_id)

    @mcp.tool(
        name="langfuse-projects-get-api-keys",
        description="Get all API keys for a project (requires organization-scoped API key)",
        tags={"projects"},
    )
    def projects_get_api_keys(project_id: str) -> Dict[str, Any]:
        return get_client().projects_get_api_keys(project_id)

    @mcp.tool(
        name="langfuse-projects-create-api-key",
        description="Create a new API key for a project (requires organization-scoped API key)",
        tags={"projects"},
    )
    def projects_create_api_key(
        project_id: str,
        note: Optional[str] = None,
        public_key: Optional[str] = None,
        secret_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        return get_client().projects_create_api_key(
            project_id, note, public_key, secret_key
        )

    @mcp.tool(
        name="langfuse-projects-delete-api-key",
        description="Delete an API key for a project (requires organization-scoped API key)",
        tags={"projects"},
    )
    def projects_delete_api_key(project_id: str, api_key_id: str) -> Dict[str, Any]:
        return get_client().projects_delete_api_key(project_id, api_key_id)


def register_prompt_version_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-prompt-version-prompt-version-update",
        description="Update labels for a specific prompt version",
        tags={"prompt_version"},
    )
    def prompt_version_update(
        name: str, version: int, new_labels: list
    ) -> Dict[str, Any]:
        return get_client().prompt_version_update(name, version, new_labels)


def register_prompts_tools(mcp: FastMCP):
    @mcp.tool(name="langfuse-prompts-get", description="Get a prompt", tags={"prompts"})
    def prompts_get(
        prompt_name: str,
        version: Optional[int] = None,
        label: Optional[str] = None,
        resolve: Optional[bool] = None,
    ) -> Dict[str, Any]:
        return get_client().prompts_get(prompt_name, version, label, resolve)

    @mcp.tool(
        name="langfuse-prompts-delete",
        description="Delete prompt versions. If neither version nor label is specified, all versions of the prompt are deleted.",
        tags={"prompts"},
    )
    def prompts_delete(
        prompt_name: str, label: Optional[str] = None, version: Optional[int] = None
    ) -> Dict[str, Any]:
        return get_client().prompts_delete(prompt_name, label, version)

    @mcp.tool(
        name="langfuse-prompts-list",
        description="Get a list of prompt names with versions and labels",
        tags={"prompts"},
    )
    def prompts_list(
        name: Optional[str] = None,
        label: Optional[str] = None,
        tag: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        from_updated_at: Optional[str] = None,
        to_updated_at: Optional[str] = None,
    ) -> Dict[str, Any]:
        return get_client().prompts_list(
            name, label, tag, page, limit, from_updated_at, to_updated_at
        )

    @mcp.tool(
        name="langfuse-prompts-create",
        description="Create a new version for the prompt with the given `name`",
        tags={"prompts"},
    )
    def prompts_create(body: dict) -> Dict[str, Any]:
        return get_client().prompts_create(body)


def register_scim_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-scim-get-service-provider-config",
        description="Get SCIM Service Provider Configuration (requires organization-scoped API key)",
        tags={"scim"},
    )
    def scim_get_service_provider_config() -> Dict[str, Any]:
        return get_client().scim_get_service_provider_config()

    @mcp.tool(
        name="langfuse-scim-get-resource-types",
        description="Get SCIM Resource Types (requires organization-scoped API key)",
        tags={"scim"},
    )
    def scim_get_resource_types() -> Dict[str, Any]:
        return get_client().scim_get_resource_types()

    @mcp.tool(
        name="langfuse-scim-get-schemas",
        description="Get SCIM Schemas (requires organization-scoped API key)",
        tags={"scim"},
    )
    def scim_get_schemas() -> Dict[str, Any]:
        return get_client().scim_get_schemas()

    @mcp.tool(
        name="langfuse-scim-list-users",
        description="List users in the organization (requires organization-scoped API key)",
        tags={"scim"},
    )
    def scim_list_users(
        filter: Optional[str] = None,
        start_index: Optional[int] = None,
        count: Optional[int] = None,
    ) -> Dict[str, Any]:
        return get_client().scim_list_users(filter, start_index, count)

    @mcp.tool(
        name="langfuse-scim-create-user",
        description="Create a new user in the organization (requires organization-scoped API key)",
        tags={"scim"},
    )
    def scim_create_user(
        user_name: str,
        name: Any,
        emails: Optional[list] = None,
        active: Optional[bool] = None,
        password: Optional[str] = None,
    ) -> Dict[str, Any]:
        return get_client().scim_create_user(user_name, name, emails, active, password)

    @mcp.tool(
        name="langfuse-scim-get-user",
        description="Get a specific user by ID (requires organization-scoped API key)",
        tags={"scim"},
    )
    def scim_get_user(user_id: str) -> Dict[str, Any]:
        return get_client().scim_get_user(user_id)

    @mcp.tool(
        name="langfuse-scim-delete-user",
        description="Remove a user from the organization (requires organization-scoped API key). Note that this only removes the user from the organization but does not delete the user entity itself.",
        tags={"scim"},
    )
    def scim_delete_user(user_id: str) -> Dict[str, Any]:
        return get_client().scim_delete_user(user_id)


def register_score_configs_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-score-configs-score-configs-create",
        description="Create a score configuration (config). Score configs are used to define the structure of scores",
        tags={"score_configs"},
    )
    def score_configs_create(body: dict) -> Dict[str, Any]:
        return get_client().score_configs_create(body)

    @mcp.tool(
        name="langfuse-score-configs-score-configs-get",
        description="Get all score configs",
        tags={"score_configs"},
    )
    def score_configs_get(
        page: Optional[int] = None, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        return get_client().score_configs_get(page, limit)

    @mcp.tool(
        name="langfuse-score-configs-score-configs-get-by-id",
        description="Get a score config",
        tags={"score_configs"},
    )
    def score_configs_get_by_id(config_id: str) -> Dict[str, Any]:
        return get_client().score_configs_get_by_id(config_id)

    @mcp.tool(
        name="langfuse-score-configs-score-configs-update",
        description="Update a score config",
        tags={"score_configs"},
    )
    def score_configs_update(config_id: str, body: dict) -> Dict[str, Any]:
        return get_client().score_configs_update(config_id, body)


def register_scores_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-scores-get-many",
        description="Get a list of scores (supports both trace and session scores)",
        tags={"scores"},
    )
    def scores_get_many(
        page: Optional[int] = None,
        limit: Optional[int] = None,
        user_id: Optional[str] = None,
        name: Optional[str] = None,
        from_timestamp: Optional[str] = None,
        to_timestamp: Optional[str] = None,
        environment: Optional[list] = None,
        source: Optional[Any] = None,
        operator: Optional[str] = None,
        value: Optional[int] = None,
        score_ids: Optional[str] = None,
        config_id: Optional[str] = None,
        session_id: Optional[str] = None,
        dataset_run_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        observation_id: Optional[str] = None,
        queue_id: Optional[str] = None,
        data_type: Optional[Any] = None,
        trace_tags: Optional[list] = None,
        fields: Optional[str] = None,
        filter: Optional[str] = None,
    ) -> Dict[str, Any]:
        return get_client().scores_get_many(
            page,
            limit,
            user_id,
            name,
            from_timestamp,
            to_timestamp,
            environment,
            source,
            operator,
            value,
            score_ids,
            config_id,
            session_id,
            dataset_run_id,
            trace_id,
            observation_id,
            queue_id,
            data_type,
            trace_tags,
            fields,
            filter,
        )

    @mcp.tool(
        name="langfuse-scores-get-by-id",
        description="Get a score (supports both trace and session scores)",
        tags={"scores"},
    )
    def scores_get_by_id(score_id: str) -> Dict[str, Any]:
        return get_client().scores_get_by_id(score_id)


def register_sessions_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-sessions-list", description="Get sessions", tags={"sessions"}
    )
    def sessions_list(
        page: Optional[int] = None,
        limit: Optional[int] = None,
        from_timestamp: Optional[str] = None,
        to_timestamp: Optional[str] = None,
        environment: Optional[list] = None,
    ) -> Dict[str, Any]:
        return get_client().sessions_list(
            page, limit, from_timestamp, to_timestamp, environment
        )

    @mcp.tool(
        name="langfuse-sessions-get",
        description="Get a session. Please note that `traces` on this endpoint are not paginated, if you plan to fetch large sessions, consider `GET /api/public/traces?sessionId=<sessionId>`",
        tags={"sessions"},
    )
    def sessions_get(session_id: str) -> Dict[str, Any]:
        return get_client().sessions_get(session_id)


def register_trace_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-trace-get", description="Get a specific trace", tags={"trace"}
    )
    def trace_get(trace_id: str) -> Dict[str, Any]:
        return get_client().trace_get(trace_id)

    @mcp.tool(
        name="langfuse-trace-delete",
        description="Delete a specific trace",
        tags={"trace"},
    )
    def trace_delete(trace_id: str) -> Dict[str, Any]:
        return get_client().trace_delete(trace_id)

    @mcp.tool(
        name="langfuse-trace-list", description="Get list of traces", tags={"trace"}
    )
    def trace_list(
        page: Optional[int] = None,
        limit: Optional[int] = None,
        user_id: Optional[str] = None,
        name: Optional[str] = None,
        session_id: Optional[str] = None,
        from_timestamp: Optional[str] = None,
        to_timestamp: Optional[str] = None,
        order_by: Optional[str] = None,
        tags: Optional[list] = None,
        version: Optional[str] = None,
        release: Optional[str] = None,
        environment: Optional[list] = None,
        fields: Optional[str] = None,
        filter: Optional[str] = None,
    ) -> Dict[str, Any]:
        return get_client().trace_list(
            page,
            limit,
            user_id,
            name,
            session_id,
            from_timestamp,
            to_timestamp,
            order_by,
            tags,
            version,
            release,
            environment,
            fields,
            filter,
        )

    @mcp.tool(
        name="langfuse-trace-delete-multiple",
        description="Delete multiple traces",
        tags={"trace"},
    )
    def trace_delete_multiple(trace_ids: list) -> Dict[str, Any]:
        return get_client().trace_delete_multiple(trace_ids)


def register_all_tools(mcp: FastMCP) -> list[str]:
    registered_tags = []
    if to_boolean(os.getenv("ANNOTATION_QUEUES_TOOL", "True")):
        register_annotation_queues_tools(mcp)
        registered_tags.append("annotationqueues")
    if to_boolean(os.getenv("BLOB_STORAGE_INTEGRATIONS_TOOL", "True")):
        register_blob_storage_integrations_tools(mcp)
        registered_tags.append("blobstorageintegrations")
    if to_boolean(os.getenv("COMMENTS_TOOL", "True")):
        register_comments_tools(mcp)
        registered_tags.append("comments")
    if to_boolean(os.getenv("DATASET_ITEMS_TOOL", "True")):
        register_dataset_items_tools(mcp)
        registered_tags.append("datasetitems")
    if to_boolean(os.getenv("DATASET_RUN_ITEMS_TOOL", "True")):
        register_dataset_run_items_tools(mcp)
        registered_tags.append("datasetrunitems")
    if to_boolean(os.getenv("DATASETS_TOOL", "True")):
        register_datasets_tools(mcp)
        registered_tags.append("datasets")
    if to_boolean(os.getenv("HEALTH_TOOL", "True")):
        register_health_tools(mcp)
        registered_tags.append("health")
    if to_boolean(os.getenv("INGESTION_TOOL", "True")):
        register_ingestion_tools(mcp)
        registered_tags.append("ingestion")
    if to_boolean(os.getenv("LEGACY_METRICS_V1_TOOL", "True")):
        register_legacy_metrics_v1_tools(mcp)
        registered_tags.append("legacymetricsv1")
    if to_boolean(os.getenv("LEGACY_OBSERVATIONS_V1_TOOL", "True")):
        register_legacy_observations_v1_tools(mcp)
        registered_tags.append("legacyobservationsv1")
    if to_boolean(os.getenv("LEGACY_SCORE_V1_TOOL", "True")):
        register_legacy_score_v1_tools(mcp)
        registered_tags.append("legacyscorev1")
    if to_boolean(os.getenv("LLM_CONNECTIONS_TOOL", "True")):
        register_llm_connections_tools(mcp)
        registered_tags.append("llmconnections")
    if to_boolean(os.getenv("MEDIA_TOOL", "True")):
        register_media_tools(mcp)
        registered_tags.append("media")
    if to_boolean(os.getenv("METRICS_TOOL", "True")):
        register_metrics_tools(mcp)
        registered_tags.append("metrics")
    if to_boolean(os.getenv("MODELS_TOOL", "True")):
        register_models_tools(mcp)
        registered_tags.append("models")
    if to_boolean(os.getenv("OBSERVATIONS_TOOL", "True")):
        register_observations_tools(mcp)
        registered_tags.append("observations")
    if to_boolean(os.getenv("OPENTELEMETRY_TOOL", "True")):
        register_opentelemetry_tools(mcp)
        registered_tags.append("opentelemetry")
    if to_boolean(os.getenv("ORGANIZATIONS_TOOL", "True")):
        register_organizations_tools(mcp)
        registered_tags.append("organizations")
    if to_boolean(os.getenv("PROJECTS_TOOL", "True")):
        register_projects_tools(mcp)
        registered_tags.append("projects")
    if to_boolean(os.getenv("PROMPT_VERSION_TOOL", "True")):
        register_prompt_version_tools(mcp)
        registered_tags.append("promptversion")
    if to_boolean(os.getenv("PROMPTS_TOOL", "True")):
        register_prompts_tools(mcp)
        registered_tags.append("prompts")
    if to_boolean(os.getenv("SCIM_TOOL", "True")):
        register_scim_tools(mcp)
        registered_tags.append("scim")
    if to_boolean(os.getenv("SCORE_CONFIGS_TOOL", "True")):
        register_score_configs_tools(mcp)
        registered_tags.append("scoreconfigs")
    if to_boolean(os.getenv("SCORES_TOOL", "True")):
        register_scores_tools(mcp)
        registered_tags.append("scores")
    if to_boolean(os.getenv("SESSIONS_TOOL", "True")):
        register_sessions_tools(mcp)
        registered_tags.append("sessions")
    if to_boolean(os.getenv("TRACE_TOOL", "True")):
        register_trace_tools(mcp)
        registered_tags.append("trace")
    return registered_tags


### END GENERATED TOOL REGISTRATION ###
def get_mcp_instance() -> tuple[Any, Any, Any, Any]:
    args, mcp, middlewares = create_mcp_server(
        name="langfuse",
        version=__version__,
        instructions="Langfuse Agent MCP Server",
    )

    registered_tags = register_all_tools(mcp)
    register_prompts(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    return mcp, args, middlewares, registered_tags


def mcp_server():
    mcp, args, middlewares, registered_tags = get_mcp_instance()

    print(f"Langfuse Agent MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)
    print(f"  Dynamic Tags Loaded: {registered_tags}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error(f"Invalid transport: {args.transport}")
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()