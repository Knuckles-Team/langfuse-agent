#!/usr/bin/env python
from typing import Any

from langfuse_agent.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def annotation_queues_list_queues(
        self, page: int | None = None, limit: int | None = None
    ) -> dict[str, Any]:
        """Get all annotation queues"""
        return self._request(
            "GET",
            "/api/public/annotation-queues",
            params={"page": page, "limit": limit},
            data=None,
        )

    def annotation_queues_create_queue(self, body: dict) -> dict[str, Any]:
        """Create an annotation queue"""
        return self._request(
            "POST", "/api/public/annotation-queues", params=None, data=body
        )

    def annotation_queues_get_queue(self, queue_id: str) -> dict[str, Any]:
        """Get an annotation queue by ID"""
        return self._request(
            "GET", f"/api/public/annotation-queues/{queue_id}", params=None, data=None
        )

    def annotation_queues_list_queue_items(
        self,
        queue_id: str,
        status: Any | None = None,
        page: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """Get items for a specific annotation queue"""
        return self._request(
            "GET",
            f"/api/public/annotation-queues/{queue_id}/items",
            params={"status": status, "page": page, "limit": limit},
            data=None,
        )

    def annotation_queues_create_queue_item(
        self, queue_id: str, body: dict
    ) -> dict[str, Any]:
        """Add an item to an annotation queue"""
        return self._request(
            "POST",
            f"/api/public/annotation-queues/{queue_id}/items",
            params=None,
            data=body,
        )

    def annotation_queues_get_queue_item(
        self, queue_id: str, item_id: str
    ) -> dict[str, Any]:
        """Get a specific item from an annotation queue"""
        return self._request(
            "GET",
            f"/api/public/annotation-queues/{queue_id}/items/{item_id}",
            params=None,
            data=None,
        )

    def annotation_queues_update_queue_item(
        self, queue_id: str, item_id: str, body: dict
    ) -> dict[str, Any]:
        """Update an annotation queue item"""
        return self._request(
            "PATCH",
            f"/api/public/annotation-queues/{queue_id}/items/{item_id}",
            params=None,
            data=body,
        )

    def annotation_queues_delete_queue_item(
        self, queue_id: str, item_id: str
    ) -> dict[str, Any]:
        """Remove an item from an annotation queue"""
        return self._request(
            "DELETE",
            f"/api/public/annotation-queues/{queue_id}/items/{item_id}",
            params=None,
            data=None,
        )

    def annotation_queues_create_queue_assignment(
        self, queue_id: str, body: dict
    ) -> dict[str, Any]:
        """Create an assignment for a user to an annotation queue"""
        return self._request(
            "POST",
            f"/api/public/annotation-queues/{queue_id}/assignments",
            params=None,
            data=body,
        )

    def annotation_queues_delete_queue_assignment(
        self, queue_id: str, body: dict
    ) -> dict[str, Any]:
        """Delete an assignment for a user to an annotation queue"""
        return self._request(
            "DELETE",
            f"/api/public/annotation-queues/{queue_id}/assignments",
            params=None,
            data=body,
        )
