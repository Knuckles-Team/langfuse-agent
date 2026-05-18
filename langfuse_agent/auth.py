"""Langfuse Authentication Module.

**Identity Passthrough Pattern**

Langfuse uses API key pair authentication (``LANGFUSE_PUBLIC_KEY`` +
``LANGFUSE_SECRET_KEY``) and does not support OIDC token exchange.

When OIDC delegation is enabled on the MCP server, the SSO token
secures the **MCP server layer** (only authenticated users can call
tools).  The downstream Langfuse API call uses the service-account
API keys.  The user's identity from the SSO token is logged for
auditing purposes.

This is the standard "identity passthrough" pattern documented in
``docs/guides/oauth_sso.md`` in agent-utilities.
"""

import os
import threading

from langfuse import Langfuse

local = threading.local()

_client = None


def get_client() -> Langfuse:
    """Get or create a singleton Langfuse client instance.

    Logs user identity when OIDC delegation is active for audit trail.
    """
    global _client
    if _client is None:
        import logging

        from agent_utilities.mcp.delegated_auth import (
            get_user_identity,
            is_delegation_enabled,
        )

        logger = logging.getLogger(__name__)

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

        _client = Langfuse(public_key=public_key, secret_key=secret_key, host=host)
    return _client
