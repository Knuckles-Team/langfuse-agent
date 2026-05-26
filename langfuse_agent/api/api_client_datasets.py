#!/usr/bin/env python
from typing import Any

from langfuse_agent.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def dataset_items_create(self, body: dict) -> dict[str, Any]:
        """Create a dataset item"""
        return self._request(
            "POST", "/api/public/dataset-items", params=None, data=body
        )

    def dataset_items_list(
        self,
        dataset_name: str | None = None,
        source_trace_id: str | None = None,
        source_observation_id: str | None = None,
        version: str | None = None,
        page: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
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

    def dataset_items_get(self, id: str) -> dict[str, Any]:
        """Get a dataset item"""
        return self._request(
            "GET", f"/api/public/dataset-items/{id}", params=None, data=None
        )

    def dataset_items_delete(self, id: str) -> dict[str, Any]:
        """Delete a dataset item and all its run items. This action is irreversible."""
        return self._request(
            "DELETE", f"/api/public/dataset-items/{id}", params=None, data=None
        )

    def dataset_run_items_create(self, body: dict) -> dict[str, Any]:
        """Create a dataset run item"""
        return self._request(
            "POST", "/api/public/dataset-run-items", params=None, data=body
        )

    def dataset_run_items_list(
        self,
        dataset_id: str,
        run_name: str,
        page: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
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
        self, page: int | None = None, limit: int | None = None
    ) -> dict[str, Any]:
        """Get all datasets"""
        return self._request(
            "GET",
            "/api/public/v2/datasets",
            params={"page": page, "limit": limit},
            data=None,
        )

    def datasets_create(self, body: dict) -> dict[str, Any]:
        """Create a dataset"""
        return self._request("POST", "/api/public/v2/datasets", params=None, data=body)

    def datasets_get(self, dataset_name: str) -> dict[str, Any]:
        """Get a dataset"""
        return self._request(
            "GET", f"/api/public/v2/datasets/{dataset_name}", params=None, data=None
        )

    def datasets_get_run(self, dataset_name: str, run_name: str) -> dict[str, Any]:
        """Get a dataset run and its items"""
        return self._request(
            "GET",
            f"/api/public/datasets/{dataset_name}/runs/{run_name}",
            params=None,
            data=None,
        )

    def datasets_delete_run(self, dataset_name: str, run_name: str) -> dict[str, Any]:
        """Delete a dataset run and all its run items. This action is irreversible."""
        return self._request(
            "DELETE",
            f"/api/public/datasets/{dataset_name}/runs/{run_name}",
            params=None,
            data=None,
        )

    def datasets_get_runs(
        self, dataset_name: str, page: int | None = None, limit: int | None = None
    ) -> dict[str, Any]:
        """Get dataset runs"""
        return self._request(
            "GET",
            f"/api/public/datasets/{dataset_name}/runs",
            params={"page": page, "limit": limit},
            data=None,
        )
