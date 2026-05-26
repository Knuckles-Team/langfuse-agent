#!/usr/bin/env python
from typing import Any

from langfuse_agent.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def blob_storage_integrations_get_blob_storage_integrations(
        self,
    ) -> dict[str, Any]:
        """Get all blob storage integrations for the organization (requires organization-scoped API key)"""
        return self._request(
            "GET", "/api/public/integrations/blob-storage", params=None, data=None
        )

    def blob_storage_integrations_upsert_blob_storage_integration(
        self, body: dict
    ) -> dict[str, Any]:
        """Create or update a blob storage integration for a specific project (requires organization-scoped API key). The configuration is validated by performing a test upload to the bucket."""
        return self._request(
            "PUT", "/api/public/integrations/blob-storage", params=None, data=body
        )

    def blob_storage_integrations_get_blob_storage_integration_status(
        self, id: str
    ) -> dict[str, Any]:
        """Get the sync status of a blob storage integration by integration ID (requires organization-scoped API key)"""
        return self._request(
            "GET", f"/api/public/integrations/blob-storage/{id}", params=None, data=None
        )

    def blob_storage_integrations_delete_blob_storage_integration(
        self, id: str
    ) -> dict[str, Any]:
        """Delete a blob storage integration by ID (requires organization-scoped API key)"""
        return self._request(
            "DELETE",
            f"/api/public/integrations/blob-storage/{id}",
            params=None,
            data=None,
        )

    def comments_create(self, body: dict) -> dict[str, Any]:
        """Create a comment. Comments may be attached to different object types (trace, observation, session, prompt)."""
        return self._request("POST", "/api/public/comments", params=None, data=body)

    def comments_get(
        self,
        page: int | None = None,
        limit: int | None = None,
        object_type: str | None = None,
        object_id: str | None = None,
        author_user_id: str | None = None,
    ) -> dict[str, Any]:
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

    def comments_get_by_id(self, comment_id: str) -> dict[str, Any]:
        """Get a comment by id"""
        return self._request(
            "GET", f"/api/public/comments/{comment_id}", params=None, data=None
        )

    def health_health(
        self,
    ) -> dict[str, Any]:
        """Check health of API and database"""
        return self._request("GET", "/api/public/health", params=None, data=None)

    def organizations_get_organization_memberships(
        self,
    ) -> dict[str, Any]:
        """Get all memberships for the organization associated with the API key (requires organization-scoped API key)"""
        return self._request(
            "GET", "/api/public/organizations/memberships", params=None, data=None
        )

    def organizations_update_organization_membership(
        self, body: dict
    ) -> dict[str, Any]:
        """Create or update a membership for the organization associated with the API key (requires organization-scoped API key)"""
        return self._request(
            "PUT", "/api/public/organizations/memberships", params=None, data=body
        )

    def organizations_delete_organization_membership(
        self, body: dict
    ) -> dict[str, Any]:
        """Delete a membership from the organization associated with the API key (requires organization-scoped API key)"""
        return self._request(
            "DELETE", "/api/public/organizations/memberships", params=None, data=body
        )

    def organizations_get_project_memberships(self, project_id: str) -> dict[str, Any]:
        """Get all memberships for a specific project (requires organization-scoped API key)"""
        return self._request(
            "GET",
            f"/api/public/projects/{project_id}/memberships",
            params=None,
            data=None,
        )

    def organizations_update_project_membership(
        self, project_id: str, body: dict
    ) -> dict[str, Any]:
        """Create or update a membership for a specific project (requires organization-scoped API key). The user must already be a member of the organization."""
        return self._request(
            "PUT",
            f"/api/public/projects/{project_id}/memberships",
            params=None,
            data=body,
        )

    def organizations_delete_project_membership(
        self, project_id: str, body: dict
    ) -> dict[str, Any]:
        """Delete a membership from a specific project (requires organization-scoped API key). The user must be a member of the organization."""
        return self._request(
            "DELETE",
            f"/api/public/projects/{project_id}/memberships",
            params=None,
            data=body,
        )

    def organizations_get_organization_projects(
        self,
    ) -> dict[str, Any]:
        """Get all projects for the organization associated with the API key (requires organization-scoped API key)"""
        return self._request(
            "GET", "/api/public/organizations/projects", params=None, data=None
        )

    def organizations_get_organization_api_keys(
        self,
    ) -> dict[str, Any]:
        """Get all API keys for the organization associated with the API key (requires organization-scoped API key)"""
        return self._request(
            "GET", "/api/public/organizations/apiKeys", params=None, data=None
        )

    def projects_get(
        self,
    ) -> dict[str, Any]:
        """Get Project associated with API key (requires project-scoped API key). You can use GET /api/public/organizations/projects to get all projects with an organization-scoped key."""
        return self._request("GET", "/api/public/projects", params=None, data=None)

    def projects_create(
        self, name: str, retention: int, metadata: dict | None = None
    ) -> dict[str, Any]:
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
        metadata: dict | None = None,
        retention: int | None = None,
    ) -> dict[str, Any]:
        """Update a project by ID (requires organization-scoped API key)."""
        return self._request(
            "PUT",
            f"/api/public/projects/{project_id}",
            params=None,
            data={"name": name, "metadata": metadata, "retention": retention},
        )

    def projects_delete(self, project_id: str) -> dict[str, Any]:
        """Delete a project by ID (requires organization-scoped API key). Project deletion is processed asynchronously."""
        return self._request(
            "DELETE", f"/api/public/projects/{project_id}", params=None, data=None
        )

    def projects_get_api_keys(self, project_id: str) -> dict[str, Any]:
        """Get all API keys for a project (requires organization-scoped API key)"""
        return self._request(
            "GET", f"/api/public/projects/{project_id}/apiKeys", params=None, data=None
        )

    def projects_create_api_key(
        self,
        project_id: str,
        note: str | None = None,
        public_key: str | None = None,
        secret_key: str | None = None,
    ) -> dict[str, Any]:
        """Create a new API key for a project (requires organization-scoped API key)"""
        return self._request(
            "POST",
            f"/api/public/projects/{project_id}/apiKeys",
            params=None,
            data={"note": note, "publicKey": public_key, "secretKey": secret_key},
        )

    def projects_delete_api_key(
        self, project_id: str, api_key_id: str
    ) -> dict[str, Any]:
        """Delete an API key for a project (requires organization-scoped API key)"""
        return self._request(
            "DELETE",
            f"/api/public/projects/{project_id}/apiKeys/{api_key_id}",
            params=None,
            data=None,
        )

    def scim_get_service_provider_config(
        self,
    ) -> dict[str, Any]:
        """Get SCIM Service Provider Configuration (requires organization-scoped API key)"""
        return self._request(
            "GET", "/api/public/scim/ServiceProviderConfig", params=None, data=None
        )

    def scim_get_resource_types(
        self,
    ) -> dict[str, Any]:
        """Get SCIM Resource Types (requires organization-scoped API key)"""
        return self._request(
            "GET", "/api/public/scim/ResourceTypes", params=None, data=None
        )

    def scim_get_schemas(
        self,
    ) -> dict[str, Any]:
        """Get SCIM Schemas (requires organization-scoped API key)"""
        return self._request("GET", "/api/public/scim/Schemas", params=None, data=None)

    def scim_list_users(
        self,
        filter: str | None = None,
        start_index: int | None = None,
        count: int | None = None,
    ) -> dict[str, Any]:
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
        emails: list | None = None,
        active: bool | None = None,
        password: str | None = None,
    ) -> dict[str, Any]:
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

    def scim_get_user(self, user_id: str) -> dict[str, Any]:
        """Get a specific user by ID (requires organization-scoped API key)"""
        return self._request(
            "GET", f"/api/public/scim/Users/{user_id}", params=None, data=None
        )

    def scim_delete_user(self, user_id: str) -> dict[str, Any]:
        """Remove a user from the organization (requires organization-scoped API key). Note that this only removes the user from the organization but does not delete the user entity itself."""
        return self._request(
            "DELETE", f"/api/public/scim/Users/{user_id}", params=None, data=None
        )
