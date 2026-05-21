from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .api_client import LangfuseApi

import logging
import os
import threading

local = threading.local()
logger = logging.getLogger(__name__)
_client = None


def get_client() -> "LangfuseApi":
    from .api_client import LangfuseApi

    """Get or create a singleton Langfuse client instance.

    Logs user identity when OIDC delegation is active for audit trail.
    """
    global _client
    if _client is None:
        from agent_utilities.mcp.delegated_auth import (
            get_user_identity,
            is_delegation_enabled,
        )

        host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
        public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "")
        secret_key = os.getenv("LANGFUSE_SECRET_KEY", "")

        # Log OIDC user identity for audit (identity passthrough pattern)
        if is_delegation_enabled():
            identity = get_user_identity()
            logger.info(
                "OIDC delegation active — Langfuse uses identity passthrough. "
                "MCP server is SSO-protected; downstream uses API keys.",
                extra={
                    "sso_user_email": identity.get("email"),
                    "sso_user_subject": identity.get("subject"),
                    "langfuse_host": host,
                },
            )

        _client = LangfuseApi(public_key=public_key, secret_key=secret_key, host=host)
    return _client
