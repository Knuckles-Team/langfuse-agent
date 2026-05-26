"""Management tools registration for langfuse-agent.

CONCEPT:LA_1.0 — Langfuse MCP Integration
"""

from typing import Any

from fastmcp import FastMCP
from pydantic import Field

from langfuse_agent.auth import get_client


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
