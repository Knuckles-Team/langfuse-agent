"""Fail-closed coverage for the Langfuse API-to-MCP surface, measured on the served tools.

The connector surface comes from the SDK declaration (``Connector(api=LangfuseApi, ...)``); these tests build the server
the way the console script does and compare its tools with the public methods of the API client.
"""

from __future__ import annotations

import asyncio
import inspect

import pytest
from agent_connector_sdk.connector import build_server
from fastmcp import Client

from langfuse_agent.api_client import LangfuseApi


def _served_tool_names() -> list[str]:
    _, mcp = build_server("langfuse_agent", command_args=["--transport", "stdio"])

    async def _list() -> list[str]:
        async with Client(mcp) as client:
            return [tool.name for tool in await client.list_tools()]

    return asyncio.run(_list())


def test_current_composed_client_is_fully_bound_to_mcp() -> None:
    names = _served_tool_names()
    methods = [n for n, _f in inspect.getmembers(LangfuseApi, inspect.isfunction) if not n.startswith("_")]

    assert methods
    unbound = [m for m in methods if not any(name.endswith(m) for name in names)]
    assert not unbound, f"API methods with no served tool: {unbound}"


def test_the_served_surface_is_built_instead_of_skipped() -> None:
    names = _served_tool_names()

    assert len(names) > 0
    assert all(name.startswith("langfuse_") for name in names)


def test_building_a_server_fails_closed_without_a_surface() -> None:
    with pytest.raises(Exception) as raised:  # noqa: PT011 - any failure to build counts, none may serve an empty surface
        build_server("no_such_connector_package", command_args=["--transport", "stdio"])

    assert raised.value is not None
