"""Local port of ``agent_utilities.mcp.delegated_auth`` onto agent-connector-sdk.

SDK-GAP (EH-48x, SDK-GAPS.md #3): agent_connector_sdk.auth.delegation replaces
this module (per its own docstring) but with a different, more explicit shape
(``DelegationSettings`` + ``exchange_token(settings, subject_token=,
http_client=)`` instead of a single ``get_delegated_token(audience=,
scopes=)`` call that resolved the subject token and built its own HTTP
client internally). This file preserves the old call surface
(``is_delegation_enabled``, ``get_delegated_token``, ``get_user_token``) so
callers need no changes, implemented on top of the SDK's real primitives.
"""

from __future__ import annotations

import dataclasses
from typing import Any

import httpx

from agent_connector_sdk.auth.delegation import (
    DelegationSettings,
    current_user_token,
    exchange_token,
)

__all__ = ["get_delegated_token", "get_user_token", "is_delegation_enabled"]

_EXCHANGE_TIMEOUT_S = 10.0


def _settings(config: dict[str, Any] | None = None) -> DelegationSettings:
    settings = DelegationSettings.from_settings()
    if not config:
        return settings
    overrides: dict[str, Any] = {}
    if config.get("audience"):
        overrides["audience"] = str(config["audience"])
    if config.get("delegated_scopes") or config.get("scopes"):
        overrides["scopes"] = str(
            config.get("delegated_scopes") or config.get("scopes")
        )
    if "enabled" in config:
        overrides["enabled"] = bool(config["enabled"])
    return dataclasses.replace(settings, **overrides) if overrides else settings


def is_delegation_enabled(config: dict[str, Any] | None = None) -> bool:
    """Whether OIDC token-exchange delegation is enabled."""
    return _settings(config).enabled


def get_user_token() -> str | None:
    """The verified access token of the MCP request being served, if any."""
    return current_user_token()


def get_delegated_token(
    *,
    config: dict[str, Any] | None = None,
    audience: str | None = None,
    scopes: str | None = None,
) -> str:
    """Exchange the calling principal's own token for one scoped to ``audience``.

    Raises if delegation is disabled or no verified caller token is bound --
    same "no silent fallback" contract as the original.
    """
    merged_config = dict(config or {})
    if audience:
        merged_config["audience"] = audience
    if scopes:
        merged_config["delegated_scopes"] = scopes
    settings = _settings(merged_config)
    subject_token = current_user_token()
    if not subject_token:
        raise RuntimeError(
            "delegation requires a verified caller token and none is bound"
        )
    with httpx.Client(timeout=_EXCHANGE_TIMEOUT_S) as http_client:
        access_token = exchange_token(
            settings, subject_token=subject_token, http_client=http_client
        )
    return access_token.value
