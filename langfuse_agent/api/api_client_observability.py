#!/usr/bin/env python
from typing import Any

from langfuse_agent.api.api_client_base import BaseApiClient
from langfuse_agent.trace_projection import (
    is_certification_trace_projection,
    project_certification_trace_list,
)


class Api(BaseApiClient):
    def scores_create(self, body: dict) -> dict[str, Any]:
        """Create a typed score through Langfuse's current score-write API."""
        return self._request("POST", "/api/public/scores", params=None, data=body)

    def metrics_get(self, query: str) -> dict[str, Any]:
        """Query aggregate observation or score metrics through Metrics API v2."""
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
        limit: int | None = None,
        cursor: str | None = None,
        id: str | None = None,
        name: str | None = None,
        from_timestamp: str | None = None,
        to_timestamp: str | None = None,
        environment: str | None = None,
        source: str | None = None,
        value: str | None = None,
        value_min: float | None = None,
        value_max: float | None = None,
        config_id: str | None = None,
        session_id: str | None = None,
        experiment_id: str | None = None,
        trace_id: str | None = None,
        observation_id: str | None = None,
        queue_id: str | None = None,
        author_user_id: str | None = None,
        data_type: str | None = None,
        fields: str | None = None,
    ) -> dict[str, Any]:
        """Query scores through the cursor-based Scores API v3."""
        return self._request(
            "GET",
            "/api/public/v3/scores",
            params={
                "limit": limit,
                "cursor": cursor,
                "id": id,
                "name": name,
                "fromTimestamp": from_timestamp,
                "toTimestamp": to_timestamp,
                "environment": environment,
                "source": source,
                "value": value,
                "valueMin": value_min,
                "valueMax": value_max,
                "configId": config_id,
                "sessionId": session_id,
                "experimentId": experiment_id,
                "traceId": trace_id,
                "observationId": observation_id,
                "queueId": queue_id,
                "authorUserId": author_user_id,
                "dataType": data_type,
                "fields": fields,
            },
            data=None,
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
        certification_projection = is_certification_trace_projection(fields)
        result = self._request(
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
                # Some self-hosted Langfuse versions omit metadata when this
                # field set is sent. Fetch the default representation, then
                # enforce the closed projection locally before any consumer
                # can return or persist it.
                "fields": None if certification_projection else fields,
                "filter": filter,
            },
            data=None,
        )
        if certification_projection:
            return project_certification_trace_list(result)
        return result

    def trace_delete_multiple(self, trace_ids: list) -> dict[str, Any]:
        """Delete multiple traces"""
        return self._request(
            "DELETE", "/api/public/traces", params=None, data={"traceIds": trace_ids}
        )
