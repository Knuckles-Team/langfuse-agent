"""Prompts and models tools registration for langfuse-agent.

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
    "llm_connections_list": ("page", "limit"),
    "llm_connections_upsert": ("body",),
    "media_get": ("media_id",),
    "media_patch": ("media_id", "body"),
    "media_get_upload_url": ("body",),
    "models_create": ("body",),
    "models_list": ("page", "limit"),
    "models_get": ("id",),
    "models_delete": ("id",),
    "prompt_version_update": ("name", "version", "new_labels"),
    "prompts_get": ("prompt_name", "version", "label", "resolve"),
    "prompts_delete": ("prompt_name", "label", "version"),
    "prompts_list": (
        "name",
        "label",
        "tag",
        "page",
        "limit",
        "from_updated_at",
        "to_updated_at",
    ),
    "prompts_create": ("body",),
}


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

        # Same insertion order as the original if-chain, so the assembled
        # kwargs dict (and therefore any downstream filtered subset) is
        # identical to before.
        candidates = (
            ("body", body),
            ("from_updated_at", from_updated_at),
            ("id", id),
            ("label", label),
            ("limit", limit),
            ("media_id", media_id),
            ("name", name),
            ("new_labels", new_labels),
            ("page", page),
            ("prompt_name", prompt_name),
            ("resolve", resolve),
            ("tag", tag),
            ("to_updated_at", to_updated_at),
            ("version", version),
        )
        kwargs = {k: v for k, v in candidates if v is not None}

        if action not in _ACTION_PARAMS:
            raise ValueError(f"Unknown action: {action}")
        method_kwargs = {k: v for k, v in kwargs.items() if k in _ACTION_PARAMS[action]}
        return getattr(client, action)(**method_kwargs)
