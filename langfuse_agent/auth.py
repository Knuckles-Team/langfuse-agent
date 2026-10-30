"""Authentication and client factory for langfuse-agent.

CONCEPT:LA_1.0 — Langfuse MCP Integration
"""

import logging
import threading
from typing import Any

from scion_sdk.config import setting

from .api_client import LangfuseApi

local = threading.local()
logger = logging.getLogger(__name__)
_client = None


def resolve_langfuse_host() -> str:
    """Resolve the validated ``LANGFUSE_HOST`` setting (http/https URL, no trailing slash)."""
    host = (
        str(setting("LANGFUSE_HOST", "https://cloud.langfuse.com") or "")
        .strip()
        .rstrip("/")
    )
    if host and not host.startswith(("http://", "https://")):
        raise ValueError("LANGFUSE_HOST must be an http(s) URL")
    return host


def resolve_langfuse_requests_transport() -> dict[str, Any]:
    """Resolve the fail-closed Requests transport (TLS verify/cert) for Langfuse."""
    from scion_sdk.tls.resolve import resolve_tls_profile

    profile = resolve_tls_profile("langfuse")
    return profile.requests_kwargs()


def is_delegation_enabled() -> bool:
    """Whether the OIDC delegation path is configured.

    Follows the proven pattern from onetrust-api's ``auth.py`` (PR #5):
    ``scion_sdk.auth.delegation`` now has an end-to-end proof, so
    this no longer needs to stay on the SDK delegation module.
    """
    from scion_sdk.auth.delegation import DelegationSettings

    return DelegationSettings.from_settings().enabled


def get_client() -> LangfuseApi:
    """Get or create a singleton Langfuse client instance.

    CONCEPT:LA_1.0 — Langfuse MCP Integration

    OIDC delegation is recorded only as a boolean event; user identity is never
    copied into logs, traces, or client configuration.
    """
    global _client
    if _client is None:
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
