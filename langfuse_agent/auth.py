"""Authentication and client factory for langfuse-agent.

CONCEPT:LA_1.0 — Langfuse MCP Integration
"""

import logging
import threading
from typing import Any

from agent_utilities.core.config import resolve_langfuse_host as _resolve_host
from agent_utilities.core.config import setting
from agent_utilities.observability.langfuse_trust import (
    resolve_langfuse_requests_transport as _resolve_requests_transport,
)

from .api_client import LangfuseApi

local = threading.local()
logger = logging.getLogger(__name__)
_client = None


def resolve_langfuse_host() -> str:
    """Resolve the sole current Agent Utilities Langfuse host contract."""
    return str(_resolve_host())


def resolve_langfuse_requests_transport() -> dict[str, Any]:
    """Resolve the current fail-closed Requests transport contract."""
    return _resolve_requests_transport()


def get_client() -> LangfuseApi:
    """Get or create a singleton Langfuse client instance.

    CONCEPT:LA_1.0 — Langfuse MCP Integration

    OIDC delegation is recorded only as a boolean event; user identity is never
    copied into logs, traces, or client configuration.
    """
    global _client
    if _client is None:
        from agent_utilities.mcp.delegated_auth import (
            is_delegation_enabled,
        )

        transport_kwargs = resolve_langfuse_requests_transport()
        # LANGFUSE_BASE_URL is the official Langfuse variable and wins when set;
        # otherwise fall back to the centralized, validated LANGFUSE_HOST contract.
        host = setting("LANGFUSE_BASE_URL", "") or resolve_langfuse_host()
        public_key = setting("LANGFUSE_PUBLIC_KEY", "")
        secret_key = setting("LANGFUSE_SECRET_KEY", "")

        if is_delegation_enabled():
            logger.info("OIDC delegation active for Langfuse MCP.")

        _client = LangfuseApi(
            public_key=public_key,
            secret_key=secret_key,
            host=host,
            transport_kwargs=transport_kwargs,
        )
    return _client
