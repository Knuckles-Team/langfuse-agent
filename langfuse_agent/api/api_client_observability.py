#!/usr/bin/env python
from typing import Any

from langfuse_agent.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def legacy_metrics_v1_metrics(self, query: str) -> dict[str, Any]:
        """Get metrics from the Langfuse project using a query object.  Consider using the [v2 metrics endpoint](/api-reference#tag/metricsv2/GET/api/public/v2/metrics) for better performance.  For more details, see the [Metrics API documentation](https://langfuse.com/docs/metrics/features/metrics-api)."""
        return self._request(
            "GET", "/api/public/metrics", params={"query": query}, data=None
        )

    def legacy_observations_v1_get(self, observation_id: str) -> dict[str, Any]:
        """Get a observation"""
        return self._request(
            "GET", f"/api/public/observations/{observation_id}", params=None, data=None
        )

    def legacy_observations_v1_get_many(
        self,
        page: int | None = None,
        limit: int | None = None,
        name: str | None = None,
        user_id: str | None = None,
        type: str | None = None,
        trace_id: str | None = None,
        level: Any | None = None,
        parent_observation_id: str | None = None,
        environment: list | None = None,
        from_start_time: str | None = None,
        to_start_time: str | None = None,
        version: str | None = None,
        filter: str | None = None,
    ) -> dict[str, Any]:
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

    def legacy_score_v1_create(self, body: dict) -> dict[str, Any]:
        """Create a score (supports both trace and session scores)"""
        return self._request("POST", "/api/public/scores", params=None, data=body)

    def legacy_score_v1_delete(self, score_id: str) -> dict[str, Any]:
        """Delete a score (supports both trace and session scores)"""
        return self._request(
            "DELETE", f"/api/public/scores/{score_id}", params=None, data=None
        )

    def metrics_metrics(self, query: str) -> dict[str, Any]:
        """Get metrics from the Langfuse project using a query object. V2 endpoint with optimized performance.  ## V2 Differences - Supports `observations`, `scores-numeric`, and `scores-categorical` views only (traces view not supported) - Direct access to tags and release fields on observations - Backwards-compatible: traceName, traceRelease, traceVersion dimensions are still available on observations view - High cardinality dimensions are not supported and will return a 400 error (see below)  For more details, see the [Metrics API documentation](https://langfuse.com/docs/metrics/features/metrics-api).  ## Available Views  ### observations Query observation-level data (spans, generations, events).  **Dimensions:** - `environment` - Deployment environment (e.g., production, staging) - `type` - Type of observation (SPAN, GENERATION, EVENT) - `name` - Name of the observation - `level` - Logging level of the observation - `version` - Version of the observation - `tags` - User-defined tags - `release` - Release version - `traceName` - Name of the parent trace (backwards-compatible) - `traceRelease` - Release version of the parent trace (backwards-compatible, maps to release) - `traceVersion` - Version of the parent trace (backwards-compatible, maps to version) - `providedModelName` - Name of the model used - `promptName` - Name of the prompt used - `promptVersion` - Version of the prompt used - `startTimeMonth` - Month of start_time in YYYY-MM format  **Measures:** - `count` - Total number of observations - `latency` - Observation latency (milliseconds) - `streamingLatency` - Generation latency from completion start to end (milliseconds) - `inputTokens` - Sum of input tokens consumed - `outputTokens` - Sum of output tokens produced - `totalTokens` - Sum of all tokens consumed - `outputTokensPerSecond` - Output tokens per second - `tokensPerSecond` - Total tokens per second - `inputCost` - Input cost (USD) - `outputCost` - Output cost (USD) - `totalCost` - Total cost (USD) - `timeToFirstToken` - Time to first token (milliseconds) - `countScores` - Number of scores attached to the observation  ### scores-numeric Query numeric and boolean score data.  **Dimensions:** - `environment` - Deployment environment - `name` - Name of the score (e.g., accuracy, toxicity) - `source` - Origin of the score (API, ANNOTATION, EVAL) - `dataType` - Data type (NUMERIC, BOOLEAN) - `configId` - Identifier of the score config - `timestampMonth` - Month in YYYY-MM format - `timestampDay` - Day in YYYY-MM-DD format - `value` - Numeric value of the score - `traceName` - Name of the parent trace - `tags` - Tags - `traceRelease` - Release version - `traceVersion` - Version - `observationName` - Name of the associated observation - `observationModelName` - Model name of the associated observation - `observationPromptName` - Prompt name of the associated observation - `observationPromptVersion` - Prompt version of the associated observation  **Measures:** - `count` - Total number of scores - `value` - Score value (for aggregations)  ### scores-categorical Query categorical score data. Same dimensions as scores-numeric except uses `stringValue` instead of `value`.  **Measures:** - `count` - Total number of scores  ## High Cardinality Dimensions The following dimensions cannot be used as grouping dimensions in v2 metrics API as they can cause performance issues. Use them in filters instead.  **observations view:** - `id` - Use traceId filter to narrow down results - `traceId` - Use traceId filter instead - `userId` - Use userId filter instead - `sessionId` - Use sessionId filter instead - `parentObservationId` - Use parentObservationId filter instead  **scores-numeric / scores-categorical views:** - `id` - Use specific filters to narrow down results - `traceId` - Use traceId filter instead - `userId` - Use userId filter instead - `sessionId` - Use sessionId filter instead - `observationId` - Use observationId filter instead  ## Aggregations Available aggregation functions: `sum`, `avg`, `count`, `max`, `min`, `p50`, `p75`, `p90`, `p95`, `p99`, `histogram`  ## Time Granularities Available granularities for timeDimension: `auto`, `minute`, `hour`, `day`, `week`, `month` - `auto` bins the data into approximately 50 buckets based on the time range"""
        return self._request(
            "GET", "/api/public/v2/metrics", params={"query": query}, data=None
        )

    def observations_get_many(
        self,
        fields: str | None = None,
        expand_metadata: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
        parse_io_as_json: bool | None = None,
        name: str | None = None,
        user_id: str | None = None,
        type: str | None = None,
        trace_id: str | None = None,
        level: Any | None = None,
        parent_observation_id: str | None = None,
        environment: list | None = None,
        from_start_time: str | None = None,
        to_start_time: str | None = None,
        version: str | None = None,
        filter: str | None = None,
    ) -> dict[str, Any]:
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

    def opentelemetry_export_traces(self, resource_spans: list) -> dict[str, Any]:
        """**OpenTelemetry Traces Ingestion Endpoint**  This endpoint implements the OTLP/HTTP specification for trace ingestion, providing native OpenTelemetry integration for Langfuse Observability.  **Supported Formats:** - Binary Protobuf: `Content-Type: application/x-protobuf` - JSON Protobuf: `Content-Type: application/json` - Supports gzip compression via `Content-Encoding: gzip` header  **Specification Compliance:** - Conforms to [OTLP/HTTP Trace Export](https://opentelemetry.io/docs/specs/otlp/#otlphttp) - Implements `ExportTraceServiceRequest` message format  **Documentation:** - Integration guide: https://langfuse.com/integrations/native/opentelemetry - Data model: https://langfuse.com/docs/observability/data-model"""
        return self._request(
            "POST",
            "/api/public/otel/v1/traces",
            params=None,
            data={"resourceSpans": resource_spans},
        )

    def score_configs_create(self, body: dict) -> dict[str, Any]:
        """Create a score configuration (config). Score configs are used to define the structure of scores"""
        return self._request(
            "POST", "/api/public/score-configs", params=None, data=body
        )

    def score_configs_get(
        self, page: int | None = None, limit: int | None = None
    ) -> dict[str, Any]:
        """Get all score configs"""
        return self._request(
            "GET",
            "/api/public/score-configs",
            params={"page": page, "limit": limit},
            data=None,
        )

    def score_configs_get_by_id(self, config_id: str) -> dict[str, Any]:
        """Get a score config"""
        return self._request(
            "GET", f"/api/public/score-configs/{config_id}", params=None, data=None
        )

    def score_configs_update(self, config_id: str, body: dict) -> dict[str, Any]:
        """Update a score config"""
        return self._request(
            "PATCH", f"/api/public/score-configs/{config_id}", params=None, data=body
        )

    def scores_get_many(
        self,
        page: int | None = None,
        limit: int | None = None,
        user_id: str | None = None,
        name: str | None = None,
        from_timestamp: str | None = None,
        to_timestamp: str | None = None,
        environment: list | None = None,
        source: Any | None = None,
        operator: str | None = None,
        value: int | None = None,
        score_ids: str | None = None,
        config_id: str | None = None,
        session_id: str | None = None,
        dataset_run_id: str | None = None,
        trace_id: str | None = None,
        observation_id: str | None = None,
        queue_id: str | None = None,
        data_type: Any | None = None,
        trace_tags: list | None = None,
        fields: str | None = None,
        filter: str | None = None,
    ) -> dict[str, Any]:
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

    def scores_get_by_id(self, score_id: str) -> dict[str, Any]:
        """Get a score (supports both trace and session scores)"""
        return self._request(
            "GET", f"/api/public/v2/scores/{score_id}", params=None, data=None
        )

    def sessions_list(
        self,
        page: int | None = None,
        limit: int | None = None,
        from_timestamp: str | None = None,
        to_timestamp: str | None = None,
        environment: list | None = None,
    ) -> dict[str, Any]:
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

    def sessions_get(self, session_id: str) -> dict[str, Any]:
        """Get a session. Please note that `traces` on this endpoint are not paginated, if you plan to fetch large sessions, consider `GET /api/public/traces?sessionId=<sessionId>`"""
        return self._request(
            "GET", f"/api/public/sessions/{session_id}", params=None, data=None
        )

    def trace_get(self, trace_id: str) -> dict[str, Any]:
        """Get a specific trace"""
        return self._request(
            "GET", f"/api/public/traces/{trace_id}", params=None, data=None
        )

    def trace_delete(self, trace_id: str) -> dict[str, Any]:
        """Delete a specific trace"""
        return self._request(
            "DELETE", f"/api/public/traces/{trace_id}", params=None, data=None
        )

    def trace_list(
        self,
        page: int | None = None,
        limit: int | None = None,
        user_id: str | None = None,
        name: str | None = None,
        session_id: str | None = None,
        from_timestamp: str | None = None,
        to_timestamp: str | None = None,
        order_by: str | None = None,
        tags: list | None = None,
        version: str | None = None,
        release: str | None = None,
        environment: list | None = None,
        fields: str | None = None,
        filter: str | None = None,
    ) -> dict[str, Any]:
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

    def trace_delete_multiple(self, trace_ids: list) -> dict[str, Any]:
        """Delete multiple traces"""
        return self._request(
            "DELETE", "/api/public/traces", params=None, data={"traceIds": trace_ids}
        )

    def ingestion_batch(
        self, batch: list, metadata: Any | None = None
    ) -> dict[str, Any]:
        """**Legacy endpoint for batch ingestion for Langfuse Observability.**  -> Please use the OpenTelemetry endpoint (`/api/public/otel/v1/traces`). Learn more: https://langfuse.com/integrations/native/opentelemetry  Within each batch, there can be multiple events. Each event has a type, an id, a timestamp, metadata and a body. Internally, we refer to this as the "event envelope" as it tells us something about the event but not the trace. We use the event id within this envelope to deduplicate messages to avoid processing the same event twice, i.e. the event id should be unique per request. The event.body.id is the ID of the actual trace and will be used for updates and will be visible within the Langfuse App. I.e. if you want to update a trace, you'd use the same body id, but separate event IDs.  Notes: - Introduction to data model: https://langfuse.com/docs/observability/data-model - Batch sizes are limited to 3.5 MB in total. You need to adjust the number of events per batch accordingly. - The API does not return a 4xx status code for input errors. Instead, it responds with a 207 status code, which includes a list of the encountered errors."""
        return self._request(
            "POST",
            "/api/public/ingestion",
            params=None,
            data={"batch": batch, "metadata": metadata},
        )
