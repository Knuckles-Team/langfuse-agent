"""Authentication and client factory for langfuse-agent.

CONCEPT:LA_1.0 — Langfuse MCP Integration
"""

import logging
import threading
from typing import Any

from agent_connector_sdk.config import setting

from .api_client import LangfuseApi

local = threading.local()
logger = logging.getLogger(__name__)
_client = None

_LANGFUSE_DEFAULT_HOST = "https://cloud.langfuse.com"
_LANGFUSE_HOST_RE = __import__("re").compile(
    r"^https://[A-Za-z0-9.-]+(?::[0-9]{1,5})?/?$"
)


def resolve_langfuse_host() -> str:
    """Resolve ``LANGFUSE_HOST`` without exposing it in logs.

    SDK-GAP (EH-48x, SDK-GAPS.md #4): inlined port of
    agent_utilities.core.config.resolve_langfuse_host -- trivial (no
    agent_utilities dependency beyond `setting`, which is already SDK-native).
    """
    host = str(setting("LANGFUSE_HOST", "") or "") or _LANGFUSE_DEFAULT_HOST
    if not host:
        return ""
    if not _LANGFUSE_HOST_RE.match(host):
        raise ValueError("LANGFUSE_HOST must be an https:// origin")
    return host.rstrip("/")


def resolve_langfuse_requests_transport() -> dict[str, Any]:
    """Resolve TLS transport kwargs for the ``requests``-based Langfuse client.

    SDK-GAP (EH-48x, SDK-GAPS.md #4): agent_utilities.observability.langfuse_trust
    is a substantial (400+ line) fail-closed custom-CA-bundle/x509 validation
    module with no agent-connector-sdk equivalent -- porting it is out of
    scope for this migration. Falls back to the standard platform trust store
    (still secure TLS verification) instead of the operator's custom CA
    bundle; a deployment relying on ``LANGFUSE_TRUST_BUNDLE`` custom-CA
    material needs that gap closed first (see SDK-GAPS.md #4).
    """
    logger.warning(
        "resolve_langfuse_requests_transport: agent_utilities.observability."
        "langfuse_trust was not ported (SDK-GAPS.md #4); using the platform "
        "trust store instead of any operator-configured custom CA bundle."
    )
    return {}


def get_client() -> LangfuseApi:
    """Get or create a singleton Langfuse client instance.

    CONCEPT:LA_1.0 — Langfuse MCP Integration

    OIDC delegation is recorded only as a boolean event; user identity is never
    copied into logs, traces, or client configuration.
    """
    global _client
    if _client is None:
        from langfuse_agent._delegated_auth_compat import (
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
