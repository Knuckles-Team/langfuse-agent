#!/usr/bin/env python
from typing import Any

from langfuse_agent.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def llm_connections_list(
        self, page: int | None = None, limit: int | None = None
    ) -> dict[str, Any]:
        """Get all LLM connections in a project"""
        return self._request(
            "GET",
            "/api/public/llm-connections",
            params={"page": page, "limit": limit},
            data=None,
        )

    def llm_connections_upsert(self, body: dict) -> dict[str, Any]:
        """Create or update an LLM connection. The connection is upserted on provider."""
        return self._request(
            "PUT", "/api/public/llm-connections", params=None, data=body
        )

    def media_get(self, media_id: str) -> dict[str, Any]:
        """Get a media record"""
        return self._request(
            "GET", f"/api/public/media/{media_id}", params=None, data=None
        )

    def media_patch(self, media_id: str, body: dict) -> dict[str, Any]:
        """Patch a media record"""
        return self._request(
            "PATCH", f"/api/public/media/{media_id}", params=None, data=body
        )

    def media_get_upload_url(self, body: dict) -> dict[str, Any]:
        """Get a presigned upload URL for a media record"""
        return self._request("POST", "/api/public/media", params=None, data=body)

    def models_create(self, body: dict) -> dict[str, Any]:
        """Create a model"""
        return self._request("POST", "/api/public/models", params=None, data=body)

    def models_list(
        self, page: int | None = None, limit: int | None = None
    ) -> dict[str, Any]:
        """Get all models"""
        return self._request(
            "GET",
            "/api/public/models",
            params={"page": page, "limit": limit},
            data=None,
        )

    def models_get(self, id: str) -> dict[str, Any]:
        """Get a model"""
        return self._request("GET", f"/api/public/models/{id}", params=None, data=None)

    def models_delete(self, id: str) -> dict[str, Any]:
        """Delete a model. Cannot delete models managed by Langfuse. You can create your own definition with the same modelName to override the definition though."""
        return self._request(
            "DELETE", f"/api/public/models/{id}", params=None, data=None
        )

    def prompt_version_update(
        self, name: str, version: int, new_labels: list
    ) -> dict[str, Any]:
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
        version: int | None = None,
        label: str | None = None,
        resolve: bool | None = None,
    ) -> dict[str, Any]:
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
        label: str | None = None,
        version: int | None = None,
    ) -> dict[str, Any]:
        """Delete prompt versions. If neither version nor label is specified, all versions of the prompt are deleted."""
        return self._request(
            "DELETE",
            f"/api/public/v2/prompts/{prompt_name}",
            params={"label": label, "version": version},
            data=None,
        )

    def prompts_list(
        self,
        name: str | None = None,
        label: str | None = None,
        tag: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        from_updated_at: str | None = None,
        to_updated_at: str | None = None,
    ) -> dict[str, Any]:
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

    def prompts_create(self, body: dict) -> dict[str, Any]:
        """Create a new version for the prompt with the given `name`"""
        return self._request("POST", "/api/public/v2/prompts", params=None, data=body)
