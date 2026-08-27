"""Management tools registration for langfuse-agent.

CONCEPT:LA_1.0 — Langfuse MCP Integration
"""

from typing import Any

from fastmcp import FastMCP
from pydantic import Field

from langfuse_agent.auth import get_client

# Every action name below is identical to the client method it dispatches to
# (verified against the elif chain this table replaced); the tuple is the
# exact, order-independent set of kwargs that branch used to forward.
_ACTION_PARAMS: dict[str, tuple[str, ...]] = {
    "blob_storage_integrations_get_blob_storage_integrations": (),
    "blob_storage_integrations_upsert_blob_storage_integration": ("body",),
    "blob_storage_integrations_get_blob_storage_integration_status": ("id",),
    "blob_storage_integrations_delete_blob_storage_integration": ("id",),
    "comments_create": ("body",),
    "comments_get": ("page", "limit", "object_type", "object_id", "author_user_id"),
    "comments_get_by_id": ("comment_id",),
    "health_health": (),
    "organizations_get_organization_memberships": (),
    "organizations_update_organization_membership": ("body",),
    "organizations_delete_organization_membership": ("body",),
    "organizations_get_project_memberships": ("project_id",),
    "organizations_update_project_membership": ("project_id", "body"),
    "organizations_delete_project_membership": ("project_id", "body"),
    "organizations_get_organization_projects": (),
    "organizations_get_organization_api_keys": (),
    "projects_get": (),
    "projects_create": ("name", "retention", "metadata"),
    "projects_update": ("project_id", "name", "metadata", "retention"),
    "projects_delete": ("project_id",),
    "projects_get_api_keys": ("project_id",),
    "projects_create_api_key": ("project_id", "note", "public_key", "secret_key"),
    "projects_delete_api_key": ("project_id", "api_key_id"),
    "scim_get_service_provider_config": (),
    "scim_get_resource_types": (),
    "scim_get_schemas": (),
    "scim_list_users": ("filter", "start_index", "count"),
    "scim_create_user": ("user_name", "name", "emails", "active", "password"),
    "scim_get_user": ("user_id",),
    "scim_delete_user": ("user_id",),
}


def register_langfuse_management_tools(mcp: FastMCP):
    """Register all management-related tools.

    CONCEPT:LA_1.0 — Langfuse MCP Integration
    """

    @mcp.tool(tags={"langfuse"})
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

        # Same insertion order as the original if-chain, so the resulting
        # kwargs dict (and therefore any downstream filtered subset) is
        # identical to before.
        candidates = (
            ("active", active),
            ("api_key_id", api_key_id),
            ("author_user_id", author_user_id),
            ("body", body),
            ("comment_id", comment_id),
            ("count", count),
            ("emails", emails),
            ("filter", filter),
            ("id", id),
            ("limit", limit),
            ("metadata", metadata),
            ("name", name),
            ("note", note),
            ("object_id", object_id),
            ("object_type", object_type),
            ("page", page),
            ("password", password),
            ("project_id", project_id),
            ("public_key", public_key),
            ("retention", retention),
            ("secret_key", secret_key),
            ("start_index", start_index),
            ("user_id", user_id),
            ("user_name", user_name),
        )
        kwargs = {k: v for k, v in candidates if v is not None}

        if action not in _ACTION_PARAMS:
            raise ValueError(f"Unknown action: {action}")
        method_kwargs = {k: v for k, v in kwargs.items() if k in _ACTION_PARAMS[action]}
        return getattr(client, action)(**method_kwargs)
