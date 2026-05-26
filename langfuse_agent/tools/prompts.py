"""Prompts and models tools registration for langfuse-agent.

CONCEPT:LA_1.0 — Langfuse MCP Integration
"""

from typing import Any

from fastmcp import FastMCP
from pydantic import Field

from langfuse_agent.auth import get_client


def register_langfuse_prompts_models_tools(mcp: FastMCP):
    """Register all prompt and model-related tools.

    CONCEPT:LA_1.0 — Langfuse MCP Integration
    """

    @mcp.tool(tags={"langfuse"})
    async def langfuse_prompts_models(
        action: str = Field(
            description="Action to perform. Must be one of: llm_connections_list, llm_connections_upsert, media_get, media_patch, media_get_upload_url, models_create, models_list, models_get, models_delete, prompt_version_update, prompts_get, prompts_delete, prompts_list, prompts_create"
        ),
        body: Any = Field(default=None, description="body"),
        from_updated_at: Any = Field(default=None, description="from updated at"),
        id: Any = Field(default=None, description="id"),
        label: Any = Field(default=None, description="label"),
        limit: Any = Field(default=None, description="limit"),
        media_id: Any = Field(default=None, description="media id"),
        name: Any = Field(default=None, description="name"),
        new_labels: Any = Field(default=None, description="new labels"),
        page: Any = Field(default=None, description="page"),
        prompt_name: Any = Field(default=None, description="prompt name"),
        resolve: Any = Field(default=None, description="resolve"),
        tag: Any = Field(default=None, description="tag"),
        to_updated_at: Any = Field(default=None, description="to updated at"),
        version: Any = Field(default=None, description="version"),
    ) -> Any:
        """Perform langfuse_prompts_models operations."""
        client = get_client()
        kwargs = {}
        if body is not None:
            kwargs["body"] = body
        if from_updated_at is not None:
            kwargs["from_updated_at"] = from_updated_at
        if id is not None:
            kwargs["id"] = id
        if label is not None:
            kwargs["label"] = label
        if limit is not None:
            kwargs["limit"] = limit
        if media_id is not None:
            kwargs["media_id"] = media_id
        if name is not None:
            kwargs["name"] = name
        if new_labels is not None:
            kwargs["new_labels"] = new_labels
        if page is not None:
            kwargs["page"] = page
        if prompt_name is not None:
            kwargs["prompt_name"] = prompt_name
        if resolve is not None:
            kwargs["resolve"] = resolve
        if tag is not None:
            kwargs["tag"] = tag
        if to_updated_at is not None:
            kwargs["to_updated_at"] = to_updated_at
        if version is not None:
            kwargs["version"] = version

        if action == "llm_connections_list":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["page", "limit"]}
            return client.llm_connections_list(**method_kwargs)
        elif action == "llm_connections_upsert":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["body"]}
            return client.llm_connections_upsert(**method_kwargs)
        elif action == "media_get":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["media_id"]}
            return client.media_get(**method_kwargs)
        elif action == "media_patch":
            method_kwargs = {
                k: v for k, v in kwargs.items() if k in ["media_id", "body"]
            }
            return client.media_patch(**method_kwargs)
        elif action == "media_get_upload_url":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["body"]}
            return client.media_get_upload_url(**method_kwargs)
        elif action == "models_create":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["body"]}
            return client.models_create(**method_kwargs)
        elif action == "models_list":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["page", "limit"]}
            return client.models_list(**method_kwargs)
        elif action == "models_get":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["id"]}
            return client.models_get(**method_kwargs)
        elif action == "models_delete":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["id"]}
            return client.models_delete(**method_kwargs)
        elif action == "prompt_version_update":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k in ["name", "version", "new_labels"]
            }
            return client.prompt_version_update(**method_kwargs)
        elif action == "prompts_get":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k in ["prompt_name", "version", "label", "resolve"]
            }
            return client.prompts_get(**method_kwargs)
        elif action == "prompts_delete":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k in ["prompt_name", "label", "version"]
            }
            return client.prompts_delete(**method_kwargs)
        elif action == "prompts_list":
            method_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k
                in [
                    "name",
                    "label",
                    "tag",
                    "page",
                    "limit",
                    "from_updated_at",
                    "to_updated_at",
                ]
            }
            return client.prompts_list(**method_kwargs)
        elif action == "prompts_create":
            method_kwargs = {k: v for k, v in kwargs.items() if k in ["body"]}
            return client.prompts_create(**method_kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")
