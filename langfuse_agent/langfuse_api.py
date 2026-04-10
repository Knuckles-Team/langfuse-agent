from typing import Dict, Any, Optional
import requests
from agent_utilities.exceptions import AuthError, ApiError


class LangfuseApi:
    def __init__(self, public_key: str, secret_key: str, host: str):
        self.public_key = public_key
        self.secret_key = secret_key
        self.host = host.rstrip("/")

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.host}{endpoint}"
        try:
            response = requests.request(
                method,
                url,
                auth=(self.public_key, self.secret_key),
                json=data,
                params=params,
                headers={"Content-Type": "application/json"},
            )
            if response.status_code == 401:
                raise AuthError(f"Unauthorized: {response.text}")
            response.raise_for_status()
            if response.text:
                return response.json()
            return {"success": True}
        except requests.exceptions.RequestException as e:
            raise ApiError(f"API request failed: {e}")

    def annotation_queues_list_queues(
        self, page: Optional[int] = None, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all annotation queues"""
        return self._request(
            "GET",
            "/api/public/annotation-queues",
            params={"page": page, "limit": limit},
            data=None,
        )

    def annotation_queues_create_queue(self, body: dict) -> Dict[str, Any]:
        """Create an annotation queue"""
        return self._request(
            "POST", "/api/public/annotation-queues", params=None, data=body
        )

    def annotation_queues_get_queue(self, queue_id: str) -> Dict[str, Any]:
        """Get an annotation queue by ID"""
        return self._request(
            "GET", f"/api/public/annotation-queues/{queue_id}", params=None, data=None
        )

    def annotation_queues_list_queue_items(
        self,
        queue_id: str,
        status: Optional[Any] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get items for a specific annotation queue"""
        return self._request(
            "GET",
            f"/api/public/annotation-queues/{queue_id}/items",
            params={"status": status, "page": page, "limit": limit},
            data=None,
        )

    def annotation_queues_create_queue_item(
        self, queue_id: str, body: dict
    ) -> Dict[str, Any]:
        """Add an item to an annotation queue"""
        return self._request(
            "POST",
            f"/api/public/annotation-queues/{queue_id}/items",
            params=None,
            data=body,
        )

    def annotation_queues_get_queue_item(
        self, queue_id: str, item_id: str
    ) -> Dict[str, Any]:
        """Get a specific item from an annotation queue"""
        return self._request(
            "GET",
            f"/api/public/annotation-queues/{queue_id}/items/{item_id}",
            params=None,
            data=None,
        )

    def annotation_queues_update_queue_item(
        self, queue_id: str, item_id: str, body: dict
    ) -> Dict[str, Any]:
        """Update an annotation queue item"""
        return self._request(
            "PATCH",
            f"/api/public/annotation-queues/{queue_id}/items/{item_id}",
            params=None,
            data=body,
        )

    def annotation_queues_delete_queue_item(
        self, queue_id: str, item_id: str
    ) -> Dict[str, Any]:
        """Remove an item from an annotation queue"""
        return self._request(
            "DELETE",
            f"/api/public/annotation-queues/{queue_id}/items/{item_id}",
            params=None,
            data=None,
        )

    def annotation_queues_create_queue_assignment(
        self, queue_id: str, body: dict
    ) -> Dict[str, Any]:
        """Create an assignment for a user to an annotation queue"""
        return self._request(
            "POST",
            f"/api/public/annotation-queues/{queue_id}/assignments",
            params=None,
            data=body,
        )

    def annotation_queues_delete_queue_assignment(
        self, queue_id: str, body: dict
    ) -> Dict[str, Any]:
        """Delete an assignment for a user to an annotation queue"""
        return self._request(
            "DELETE",
            f"/api/public/annotation-queues/{queue_id}/assignments",
            params=None,
            data=body,
        )

    def blob_storage_integrations_get_blob_storage_integrations(
        self,
    ) -> Dict[str, Any]:
        """Get all blob storage integrations for the organization (requires organization-scoped API key)"""
        return self._request(
            "GET", "/api/public/integrations/blob-storage", params=None, data=None
        )

    def blob_storage_integrations_upsert_blob_storage_integration(
        self, body: dict
    ) -> Dict[str, Any]:
        """Create or update a blob storage integration for a specific project (requires organization-scoped API key). The configuration is validated by performing a test upload to the bucket."""
        return self._request(
            "PUT", "/api/public/integrations/blob-storage", params=None, data=body
        )

    def blob_storage_integrations_get_blob_storage_integration_status(
        self, id: str
    ) -> Dict[str, Any]:
        """Get the sync status of a blob storage integration by integration ID (requires organization-scoped API key)"""
        return self._request(
            "GET", f"/api/public/integrations/blob-storage/{id}", params=None, data=None
        )

    def blob_storage_integrations_delete_blob_storage_integration(
        self, id: str
    ) -> Dict[str, Any]:
        """Delete a blob storage integration by ID (requires organization-scoped API key)"""
        return self._request(
            "DELETE",
            f"/api/public/integrations/blob-storage/{id}",
            params=None,
            data=None,
        )

    def comments_create(self, body: dict) -> Dict[str, Any]:
        """Create a comment. Comments may be attached to different object types (trace, observation, session, prompt)."""
        return self._request("POST", "/api/public/comments", params=None, data=body)

    def comments_get(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        object_type: Optional[str] = None,
        object_id: Optional[str] = None,
        author_user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get all comments"""
        return self._request(
            "GET",
            "/api/public/comments",
            params={
                "page": page,
                "limit": limit,
                "objectType": object_type,
                "objectId": object_id,
                "authorUserId": author_user_id,
            },
            data=None,
        )

    def comments_get_by_id(self, comment_id: str) -> Dict[str, Any]:
        """Get a comment by id"""
        return self._request(
            "GET", f"/api/public/comments/{comment_id}", params=None, data=None
        )

    def dataset_items_create(self, body: dict) -> Dict[str, Any]:
        """Create a dataset item"""
        return self._request(
            "POST", "/api/public/dataset-items", params=None, data=body
        )

    def dataset_items_list(
        self,
        dataset_name: Optional[str] = None,
        source_trace_id: Optional[str] = None,
        source_observation_id: Optional[str] = None,
        version: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get dataset items. Optionally specify a version to get the items as they existed at that point in time. Note: If version parameter is provided, datasetName must also be provided."""
        return self._request(
            "GET",
            "/api/public/dataset-items",
            params={
                "datasetName": dataset_name,
                "sourceTraceId": source_trace_id,
                "sourceObservationId": source_observation_id,
                "version": version,
                "page": page,
                "limit": limit,
            },
            data=None,
        )

    def dataset_items_get(self, id: str) -> Dict[str, Any]:
        """Get a dataset item"""
        return self._request(
            "GET", f"/api/public/dataset-items/{id}", params=None, data=None
        )

    def dataset_items_delete(self, id: str) -> Dict[str, Any]:
        """Delete a dataset item and all its run items. This action is irreversible."""
        return self._request(
            "DELETE", f"/api/public/dataset-items/{id}", params=None, data=None
        )

    def dataset_run_items_create(self, body: dict) -> Dict[str, Any]:
        """Create a dataset run item"""
        return self._request(
            "POST", "/api/public/dataset-run-items", params=None, data=body
        )

    def dataset_run_items_list(
        self,
        dataset_id: str,
        run_name: str,
        page: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List dataset run items"""
        return self._request(
            "GET",
            "/api/public/dataset-run-items",
            params={
                "datasetId": dataset_id,
                "runName": run_name,
                "page": page,
                "limit": limit,
            },
            data=None,
        )

    def datasets_list(
        self, page: Optional[int] = None, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all datasets"""
        return self._request(
            "GET",
            "/api/public/v2/datasets",
            params={"page": page, "limit": limit},
            data=None,
        )

    def datasets_create(self, body: dict) -> Dict[str, Any]:
        """Create a dataset"""
        return self._request("POST", "/api/public/v2/datasets", params=None, data=body)

    def datasets_get(self, dataset_name: str) -> Dict[str, Any]:
        """Get a dataset"""
        return self._request(
            "GET", f"/api/public/v2/datasets/{dataset_name}", params=None, data=None
        )

    def datasets_get_run(self, dataset_name: str, run_name: str) -> Dict[str, Any]:
        """Get a dataset run and its items"""
        return self._request(
            "GET",
            f"/api/public/datasets/{dataset_name}/runs/{run_name}",
            params=None,
            data=None,
        )

    def datasets_delete_run(self, dataset_name: str, run_name: str) -> Dict[str, Any]:
        """Delete a dataset run and all its run items. This action is irreversible."""
        return self._request(
            "DELETE",
            f"/api/public/datasets/{dataset_name}/runs/{run_name}",
            params=None,
            data=None,
        )

    def datasets_get_runs(
        self, dataset_name: str, page: Optional[int] = None, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get dataset runs"""
        return self._request(
            "GET",
            f"/api/public/datasets/{dataset_name}/runs",
            params={"page": page, "limit": limit},
            data=None,
        )

    def health_health(
        self,
    ) -> Dict[str, Any]:
        """Check health of API and database"""
        return self._request("GET", "/api/public/health", params=None, data=None)

    def ingestion_batch(
        self, batch: list, metadata: Optional[Any] = None
    ) -> Dict[str, Any]:
        """**Legacy endpoint for batch ingestion for Langfuse Observability.**  -> Please use the OpenTelemetry endpoint (`/api/public/otel/v1/traces`). Learn more: https://langfuse.com/integrations/native/opentelemetry  Within each batch, there can be multiple events. Each event has a type, an id, a timestamp, metadata and a body. Internally, we refer to this as the "event envelope" as it tells us something about the event but not the trace. We use the event id within this envelope to deduplicate messages to avoid processing the same event twice, i.e. the event id should be unique per request. The event.body.id is the ID of the actual trace and will be used for updates and will be visible within the Langfuse App. I.e. if you want to update a trace, you'd use the same body id, but separate event IDs.  Notes: - Introduction to data model: https://langfuse.com/docs/observability/data-model - Batch sizes are limited to 3.5 MB in total. You need to adjust the number of events per batch accordingly. - The API does not return a 4xx status code for input errors. Instead, it responds with a 207 status code, which includes a list of the encountered errors."""
        return self._request(
            "POST",
            "/api/public/ingestion",
            params=None,
            data={"batch": batch, "metadata": metadata},
        )

    def legacy_metrics_v1_metrics(self, query: str) -> Dict[str, Any]:
        """Get metrics from the Langfuse project using a query object.  Consider using the [v2 metrics endpoint](/api-reference#tag/metricsv2/GET/api/public/v2/metrics) for better performance.  For more details, see the [Metrics API documentation](https://langfuse.com/docs/metrics/features/metrics-api)."""
        return self._request(
            "GET", "/api/public/metrics", params={"query": query}, data=None
        )

    def legacy_observations_v1_get(self, observation_id: str) -> Dict[str, Any]:
        """Get a observation"""
        return self._request(
            "GET", f"/api/public/observations/{observation_id}", params=None, data=None
        )

    def legacy_observations_v1_get_many(
        self,
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
        """Get a list of observations.  Consider using the [v2 observations endpoint](/api-reference#tag/observationsv2/GET/api/public/v2/observations) for cursor-based pagination and field selection."""
        return self._request(
            "GET",
            "/api/public/observations",
            params={
                "page": page,
                "limit": limit,
                "name": name,
                "userId": user_id,
                "type": type,
                "traceId": trace_id,
                "level": level,
                "parentObservationId": parent_observation_id,
                "environment": environment,
                "fromStartTime": from_start_time,
                "toStartTime": to_start_time,
                "version": version,
                "filter": filter,
            },
            data=None,
        )

    def legacy_score_v1_create(self, body: dict) -> Dict[str, Any]:
        """Create a score (supports both trace and session scores)"""
        return self._request("POST", "/api/public/scores", params=None, data=body)

    def legacy_score_v1_delete(self, score_id: str) -> Dict[str, Any]:
        """Delete a score (supports both trace and session scores)"""
        return self._request(
            "DELETE", f"/api/public/scores/{score_id}", params=None, data=None
        )

    def llm_connections_list(
        self, page: Optional[int] = None, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all LLM connections in a project"""
        return self._request(
            "GET",
            "/api/public/llm-connections",
            params={"page": page, "limit": limit},
            data=None,
        )

    def llm_connections_upsert(self, body: dict) -> Dict[str, Any]:
        """Create or update an LLM connection. The connection is upserted on provider."""
        return self._request(
            "PUT", "/api/public/llm-connections", params=None, data=body
        )

    def media_get(self, media_id: str) -> Dict[str, Any]:
        """Get a media record"""
        return self._request(
            "GET", f"/api/public/media/{media_id}", params=None, data=None
        )

    def media_patch(self, media_id: str, body: dict) -> Dict[str, Any]:
        """Patch a media record"""
        return self._request(
            "PATCH", f"/api/public/media/{media_id}", params=None, data=body
        )

    def media_get_upload_url(self, body: dict) -> Dict[str, Any]:
        """Get a presigned upload URL for a media record"""
        return self._request("POST", "/api/public/media", params=None, data=body)

    def metrics_metrics(self, query: str) -> Dict[str, Any]:
        """Get metrics from the Langfuse project using a query object. V2 endpoint with optimized performance.  ## V2 Differences - Supports `observations`, `scores-numeric`, and `scores-categorical` views only (traces view not supported) - Direct access to tags and release fields on observations - Backwards-compatible: traceName, traceRelease, traceVersion dimensions are still available on observations view - High cardinality dimensions are not supported and will return a 400 error (see below)  For more details, see the [Metrics API documentation](https://langfuse.com/docs/metrics/features/metrics-api).  ## Available Views  ### observations Query observation-level data (spans, generations, events).  **Dimensions:** - `environment` - Deployment environment (e.g., production, staging) - `type` - Type of observation (SPAN, GENERATION, EVENT) - `name` - Name of the observation - `level` - Logging level of the observation - `version` - Version of the observation - `tags` - User-defined tags - `release` - Release version - `traceName` - Name of the parent trace (backwards-compatible) - `traceRelease` - Release version of the parent trace (backwards-compatible, maps to release) - `traceVersion` - Version of the parent trace (backwards-compatible, maps to version) - `providedModelName` - Name of the model used - `promptName` - Name of the prompt used - `promptVersion` - Version of the prompt used - `startTimeMonth` - Month of start_time in YYYY-MM format  **Measures:** - `count` - Total number of observations - `latency` - Observation latency (milliseconds) - `streamingLatency` - Generation latency from completion start to end (milliseconds) - `inputTokens` - Sum of input tokens consumed - `outputTokens` - Sum of output tokens produced - `totalTokens` - Sum of all tokens consumed - `outputTokensPerSecond` - Output tokens per second - `tokensPerSecond` - Total tokens per second - `inputCost` - Input cost (USD) - `outputCost` - Output cost (USD) - `totalCost` - Total cost (USD) - `timeToFirstToken` - Time to first token (milliseconds) - `countScores` - Number of scores attached to the observation  ### scores-numeric Query numeric and boolean score data.  **Dimensions:** - `environment` - Deployment environment - `name` - Name of the score (e.g., accuracy, toxicity) - `source` - Origin of the score (API, ANNOTATION, EVAL) - `dataType` - Data type (NUMERIC, BOOLEAN) - `configId` - Identifier of the score config - `timestampMonth` - Month in YYYY-MM format - `timestampDay` - Day in YYYY-MM-DD format - `value` - Numeric value of the score - `traceName` - Name of the parent trace - `tags` - Tags - `traceRelease` - Release version - `traceVersion` - Version - `observationName` - Name of the associated observation - `observationModelName` - Model name of the associated observation - `observationPromptName` - Prompt name of the associated observation - `observationPromptVersion` - Prompt version of the associated observation  **Measures:** - `count` - Total number of scores - `value` - Score value (for aggregations)  ### scores-categorical Query categorical score data. Same dimensions as scores-numeric except uses `stringValue` instead of `value`.  **Measures:** - `count` - Total number of scores  ## High Cardinality Dimensions The following dimensions cannot be used as grouping dimensions in v2 metrics API as they can cause performance issues. Use them in filters instead.  **observations view:** - `id` - Use traceId filter to narrow down results - `traceId` - Use traceId filter instead - `userId` - Use userId filter instead - `sessionId` - Use sessionId filter instead - `parentObservationId` - Use parentObservationId filter instead  **scores-numeric / scores-categorical views:** - `id` - Use specific filters to narrow down results - `traceId` - Use traceId filter instead - `userId` - Use userId filter instead - `sessionId` - Use sessionId filter instead - `observationId` - Use observationId filter instead  ## Aggregations Available aggregation functions: `sum`, `avg`, `count`, `max`, `min`, `p50`, `p75`, `p90`, `p95`, `p99`, `histogram`  ## Time Granularities Available granularities for timeDimension: `auto`, `minute`, `hour`, `day`, `week`, `month` - `auto` bins the data into approximately 50 buckets based on the time range"""
        return self._request(
            "GET", "/api/public/v2/metrics", params={"query": query}, data=None
        )

    def models_create(self, body: dict) -> Dict[str, Any]:
        """Create a model"""
        return self._request("POST", "/api/public/models", params=None, data=body)

    def models_list(
        self, page: Optional[int] = None, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all models"""
        return self._request(
            "GET",
            "/api/public/models",
            params={"page": page, "limit": limit},
            data=None,
        )

    def models_get(self, id: str) -> Dict[str, Any]:
        """Get a model"""
        return self._request("GET", f"/api/public/models/{id}", params=None, data=None)

    def models_delete(self, id: str) -> Dict[str, Any]:
        """Delete a model. Cannot delete models managed by Langfuse. You can create your own definition with the same modelName to override the definition though."""
        return self._request(
            "DELETE", f"/api/public/models/{id}", params=None, data=None
        )

    def observations_get_many(
        self,
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
        """Get a list of observations with cursor-based pagination and flexible field selection.  ## Cursor-based Pagination This endpoint uses cursor-based pagination for efficient traversal of large datasets. The cursor is returned in the response metadata and should be passed in subsequent requests to retrieve the next page of results.  ## Field Selection Use the `fields` parameter to control which observation fields are returned: - `core` - Always included: id, traceId, startTime, endTime, projectId, parentObservationId, type - `basic` - name, level, statusMessage, version, environment, bookmarked, public, userId, sessionId - `time` - completionStartTime, createdAt, updatedAt - `io` - input, output - `metadata` - metadata (truncated to 200 chars by default, use `expandMetadata` to get full values) - `model` - providedModelName, internalModelId, modelParameters - `usage` - usageDetails, costDetails, totalCost - `prompt` - promptId, promptName, promptVersion - `metrics` - latency, timeToFirstToken  If not specified, `core` and `basic` field groups are returned.  ## Filters Multiple filtering options are available via query parameters or the structured `filter` parameter. When using the `filter` parameter, it takes precedence over individual query parameter filters."""
        return self._request(
            "GET",
            "/api/public/v2/observations",
            params={
                "fields": fields,
                "expandMetadata": expand_metadata,
                "limit": limit,
                "cursor": cursor,
                "parseIoAsJson": parse_io_as_json,
                "name": name,
                "userId": user_id,
                "type": type,
                "traceId": trace_id,
                "level": level,
                "parentObservationId": parent_observation_id,
                "environment": environment,
                "fromStartTime": from_start_time,
                "toStartTime": to_start_time,
                "version": version,
                "filter": filter,
            },
            data=None,
        )

    def opentelemetry_export_traces(self, resource_spans: list) -> Dict[str, Any]:
        """**OpenTelemetry Traces Ingestion Endpoint**  This endpoint implements the OTLP/HTTP specification for trace ingestion, providing native OpenTelemetry integration for Langfuse Observability.  **Supported Formats:** - Binary Protobuf: `Content-Type: application/x-protobuf` - JSON Protobuf: `Content-Type: application/json` - Supports gzip compression via `Content-Encoding: gzip` header  **Specification Compliance:** - Conforms to [OTLP/HTTP Trace Export](https://opentelemetry.io/docs/specs/otlp/#otlphttp) - Implements `ExportTraceServiceRequest` message format  **Documentation:** - Integration guide: https://langfuse.com/integrations/native/opentelemetry - Data model: https://langfuse.com/docs/observability/data-model"""
        return self._request(
            "POST",
            "/api/public/otel/v1/traces",
            params=None,
            data={"resourceSpans": resource_spans},
        )

    def organizations_get_organization_memberships(
        self,
    ) -> Dict[str, Any]:
        """Get all memberships for the organization associated with the API key (requires organization-scoped API key)"""
        return self._request(
            "GET", "/api/public/organizations/memberships", params=None, data=None
        )

    def organizations_update_organization_membership(
        self, body: dict
    ) -> Dict[str, Any]:
        """Create or update a membership for the organization associated with the API key (requires organization-scoped API key)"""
        return self._request(
            "PUT", "/api/public/organizations/memberships", params=None, data=body
        )

    def organizations_delete_organization_membership(
        self, body: dict
    ) -> Dict[str, Any]:
        """Delete a membership from the organization associated with the API key (requires organization-scoped API key)"""
        return self._request(
            "DELETE", "/api/public/organizations/memberships", params=None, data=body
        )

    def organizations_get_project_memberships(self, project_id: str) -> Dict[str, Any]:
        """Get all memberships for a specific project (requires organization-scoped API key)"""
        return self._request(
            "GET",
            f"/api/public/projects/{project_id}/memberships",
            params=None,
            data=None,
        )

    def organizations_update_project_membership(
        self, project_id: str, body: dict
    ) -> Dict[str, Any]:
        """Create or update a membership for a specific project (requires organization-scoped API key). The user must already be a member of the organization."""
        return self._request(
            "PUT",
            f"/api/public/projects/{project_id}/memberships",
            params=None,
            data=body,
        )

    def organizations_delete_project_membership(
        self, project_id: str, body: dict
    ) -> Dict[str, Any]:
        """Delete a membership from a specific project (requires organization-scoped API key). The user must be a member of the organization."""
        return self._request(
            "DELETE",
            f"/api/public/projects/{project_id}/memberships",
            params=None,
            data=body,
        )

    def organizations_get_organization_projects(
        self,
    ) -> Dict[str, Any]:
        """Get all projects for the organization associated with the API key (requires organization-scoped API key)"""
        return self._request(
            "GET", "/api/public/organizations/projects", params=None, data=None
        )

    def organizations_get_organization_api_keys(
        self,
    ) -> Dict[str, Any]:
        """Get all API keys for the organization associated with the API key (requires organization-scoped API key)"""
        return self._request(
            "GET", "/api/public/organizations/apiKeys", params=None, data=None
        )

    def projects_get(
        self,
    ) -> Dict[str, Any]:
        """Get Project associated with API key (requires project-scoped API key). You can use GET /api/public/organizations/projects to get all projects with an organization-scoped key."""
        return self._request("GET", "/api/public/projects", params=None, data=None)

    def projects_create(
        self, name: str, retention: int, metadata: Optional[dict] = None
    ) -> Dict[str, Any]:
        """Create a new project (requires organization-scoped API key)"""
        return self._request(
            "POST",
            "/api/public/projects",
            params=None,
            data={"name": name, "metadata": metadata, "retention": retention},
        )

    def projects_update(
        self,
        project_id: str,
        name: str,
        metadata: Optional[dict] = None,
        retention: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update a project by ID (requires organization-scoped API key)."""
        return self._request(
            "PUT",
            f"/api/public/projects/{project_id}",
            params=None,
            data={"name": name, "metadata": metadata, "retention": retention},
        )

    def projects_delete(self, project_id: str) -> Dict[str, Any]:
        """Delete a project by ID (requires organization-scoped API key). Project deletion is processed asynchronously."""
        return self._request(
            "DELETE", f"/api/public/projects/{project_id}", params=None, data=None
        )

    def projects_get_api_keys(self, project_id: str) -> Dict[str, Any]:
        """Get all API keys for a project (requires organization-scoped API key)"""
        return self._request(
            "GET", f"/api/public/projects/{project_id}/apiKeys", params=None, data=None
        )

    def projects_create_api_key(
        self,
        project_id: str,
        note: Optional[str] = None,
        public_key: Optional[str] = None,
        secret_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new API key for a project (requires organization-scoped API key)"""
        return self._request(
            "POST",
            f"/api/public/projects/{project_id}/apiKeys",
            params=None,
            data={"note": note, "publicKey": public_key, "secretKey": secret_key},
        )

    def projects_delete_api_key(
        self, project_id: str, api_key_id: str
    ) -> Dict[str, Any]:
        """Delete an API key for a project (requires organization-scoped API key)"""
        return self._request(
            "DELETE",
            f"/api/public/projects/{project_id}/apiKeys/{api_key_id}",
            params=None,
            data=None,
        )

    def prompt_version_update(
        self, name: str, version: int, new_labels: list
    ) -> Dict[str, Any]:
        """Update labels for a specific prompt version"""
        return self._request(
            "PATCH",
            f"/api/public/v2/prompts/{name}/versions/{version}",
            params=None,
            data={"newLabels": new_labels},
        )

    def prompts_get(
        self,
        prompt_name: str,
        version: Optional[int] = None,
        label: Optional[str] = None,
        resolve: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Get a prompt"""
        return self._request(
            "GET",
            f"/api/public/v2/prompts/{prompt_name}",
            params={"version": version, "label": label, "resolve": resolve},
            data=None,
        )

    def prompts_delete(
        self,
        prompt_name: str,
        label: Optional[str] = None,
        version: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Delete prompt versions. If neither version nor label is specified, all versions of the prompt are deleted."""
        return self._request(
            "DELETE",
            f"/api/public/v2/prompts/{prompt_name}",
            params={"label": label, "version": version},
            data=None,
        )

    def prompts_list(
        self,
        name: Optional[str] = None,
        label: Optional[str] = None,
        tag: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        from_updated_at: Optional[str] = None,
        to_updated_at: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get a list of prompt names with versions and labels"""
        return self._request(
            "GET",
            "/api/public/v2/prompts",
            params={
                "name": name,
                "label": label,
                "tag": tag,
                "page": page,
                "limit": limit,
                "fromUpdatedAt": from_updated_at,
                "toUpdatedAt": to_updated_at,
            },
            data=None,
        )

    def prompts_create(self, body: dict) -> Dict[str, Any]:
        """Create a new version for the prompt with the given `name`"""
        return self._request("POST", "/api/public/v2/prompts", params=None, data=body)

    def scim_get_service_provider_config(
        self,
    ) -> Dict[str, Any]:
        """Get SCIM Service Provider Configuration (requires organization-scoped API key)"""
        return self._request(
            "GET", "/api/public/scim/ServiceProviderConfig", params=None, data=None
        )

    def scim_get_resource_types(
        self,
    ) -> Dict[str, Any]:
        """Get SCIM Resource Types (requires organization-scoped API key)"""
        return self._request(
            "GET", "/api/public/scim/ResourceTypes", params=None, data=None
        )

    def scim_get_schemas(
        self,
    ) -> Dict[str, Any]:
        """Get SCIM Schemas (requires organization-scoped API key)"""
        return self._request("GET", "/api/public/scim/Schemas", params=None, data=None)

    def scim_list_users(
        self,
        filter: Optional[str] = None,
        start_index: Optional[int] = None,
        count: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List users in the organization (requires organization-scoped API key)"""
        return self._request(
            "GET",
            "/api/public/scim/Users",
            params={"filter": filter, "startIndex": start_index, "count": count},
            data=None,
        )

    def scim_create_user(
        self,
        user_name: str,
        name: Any,
        emails: Optional[list] = None,
        active: Optional[bool] = None,
        password: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new user in the organization (requires organization-scoped API key)"""
        return self._request(
            "POST",
            "/api/public/scim/Users",
            params=None,
            data={
                "userName": user_name,
                "name": name,
                "emails": emails,
                "active": active,
                "password": password,
            },
        )

    def scim_get_user(self, user_id: str) -> Dict[str, Any]:
        """Get a specific user by ID (requires organization-scoped API key)"""
        return self._request(
            "GET", f"/api/public/scim/Users/{user_id}", params=None, data=None
        )

    def scim_delete_user(self, user_id: str) -> Dict[str, Any]:
        """Remove a user from the organization (requires organization-scoped API key). Note that this only removes the user from the organization but does not delete the user entity itself."""
        return self._request(
            "DELETE", f"/api/public/scim/Users/{user_id}", params=None, data=None
        )

    def score_configs_create(self, body: dict) -> Dict[str, Any]:
        """Create a score configuration (config). Score configs are used to define the structure of scores"""
        return self._request(
            "POST", "/api/public/score-configs", params=None, data=body
        )

    def score_configs_get(
        self, page: Optional[int] = None, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get all score configs"""
        return self._request(
            "GET",
            "/api/public/score-configs",
            params={"page": page, "limit": limit},
            data=None,
        )

    def score_configs_get_by_id(self, config_id: str) -> Dict[str, Any]:
        """Get a score config"""
        return self._request(
            "GET", f"/api/public/score-configs/{config_id}", params=None, data=None
        )

    def score_configs_update(self, config_id: str, body: dict) -> Dict[str, Any]:
        """Update a score config"""
        return self._request(
            "PATCH", f"/api/public/score-configs/{config_id}", params=None, data=body
        )

    def scores_get_many(
        self,
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
        """Get a list of scores (supports both trace and session scores)"""
        return self._request(
            "GET",
            "/api/public/v2/scores",
            params={
                "page": page,
                "limit": limit,
                "userId": user_id,
                "name": name,
                "fromTimestamp": from_timestamp,
                "toTimestamp": to_timestamp,
                "environment": environment,
                "source": source,
                "operator": operator,
                "value": value,
                "scoreIds": score_ids,
                "configId": config_id,
                "sessionId": session_id,
                "datasetRunId": dataset_run_id,
                "traceId": trace_id,
                "observationId": observation_id,
                "queueId": queue_id,
                "dataType": data_type,
                "traceTags": trace_tags,
                "fields": fields,
                "filter": filter,
            },
            data=None,
        )

    def scores_get_by_id(self, score_id: str) -> Dict[str, Any]:
        """Get a score (supports both trace and session scores)"""
        return self._request(
            "GET", f"/api/public/v2/scores/{score_id}", params=None, data=None
        )

    def sessions_list(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        from_timestamp: Optional[str] = None,
        to_timestamp: Optional[str] = None,
        environment: Optional[list] = None,
    ) -> Dict[str, Any]:
        """Get sessions"""
        return self._request(
            "GET",
            "/api/public/sessions",
            params={
                "page": page,
                "limit": limit,
                "fromTimestamp": from_timestamp,
                "toTimestamp": to_timestamp,
                "environment": environment,
            },
            data=None,
        )

    def sessions_get(self, session_id: str) -> Dict[str, Any]:
        """Get a session. Please note that `traces` on this endpoint are not paginated, if you plan to fetch large sessions, consider `GET /api/public/traces?sessionId=<sessionId>`"""
        return self._request(
            "GET", f"/api/public/sessions/{session_id}", params=None, data=None
        )

    def trace_get(self, trace_id: str) -> Dict[str, Any]:
        """Get a specific trace"""
        return self._request(
            "GET", f"/api/public/traces/{trace_id}", params=None, data=None
        )

    def trace_delete(self, trace_id: str) -> Dict[str, Any]:
        """Delete a specific trace"""
        return self._request(
            "DELETE", f"/api/public/traces/{trace_id}", params=None, data=None
        )

    def trace_list(
        self,
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
        """Get list of traces"""
        return self._request(
            "GET",
            "/api/public/traces",
            params={
                "page": page,
                "limit": limit,
                "userId": user_id,
                "name": name,
                "sessionId": session_id,
                "fromTimestamp": from_timestamp,
                "toTimestamp": to_timestamp,
                "orderBy": order_by,
                "tags": tags,
                "version": version,
                "release": release,
                "environment": environment,
                "fields": fields,
                "filter": filter,
            },
            data=None,
        )

    def trace_delete_multiple(self, trace_ids: list) -> Dict[str, Any]:
        """Delete multiple traces"""
        return self._request(
            "DELETE", "/api/public/traces", params=None, data={"traceIds": trace_ids}
        )
