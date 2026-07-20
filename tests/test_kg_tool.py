"""Validation contracts for the explicit Langfuse KG ingestion tool."""

from unittest.mock import MagicMock, patch

import pytest
from fastmcp import FastMCP

from langfuse_agent.tools.kg import register_langfuse_kg_tools


async def _ingest_tool():
    mcp = FastMCP("test-langfuse-ingest")
    register_langfuse_kg_tools(mcp)
    return (await mcp.list_tools())[0].fn


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("params_json", "message"),
    [
        ('{"private-filter":', "params_json must be valid JSON"),
        ("[]", "params_json must decode to a JSON object"),
        ("null", "params_json must decode to a JSON object"),
        ("x" * (64 * 1024 + 1), "params_json exceeds the 65536-unit input limit"),
    ],
)
async def test_langfuse_ingest_rejects_invalid_params_before_client(
    params_json, message
):
    """Malformed, non-object, and oversized filters fail before API access."""
    tool = await _ingest_tool()

    with patch("langfuse_agent.tools.kg.get_client") as get_client:
        with pytest.raises(ValueError, match=message) as exc_info:
            await tool(kind="traces", limit=50, params_json=params_json)

    get_client.assert_not_called()
    assert "private-filter" not in str(exc_info.value)


@pytest.mark.asyncio
async def test_langfuse_ingest_rejects_unknown_kind_without_echo():
    tool = await _ingest_tool()

    with patch("langfuse_agent.tools.kg.get_client") as get_client:
        with pytest.raises(ValueError, match="Unknown kind") as exc_info:
            await tool(kind="private-value", limit=50, params_json="{}")

    get_client.assert_not_called()
    assert "private-value" not in str(exc_info.value)


@pytest.mark.asyncio
async def test_langfuse_ingest_uses_v2_observations_method_after_validation():
    """A valid object reaches the current v2 observations endpoint unchanged."""
    tool = await _ingest_tool()
    client = MagicMock()
    client.observations_get_many.return_value = {"data": []}
    ingest = MagicMock(return_value={"nodes": 0, "edges": 0})

    with (
        patch("langfuse_agent.tools.kg.get_client", return_value=client),
        patch.dict(
            "langfuse_agent.tools.kg._INGESTERS",
            {"observations": (ingest, "observations_get_many")},
        ),
    ):
        result = await tool(
            kind="observations",
            limit=50,
            params_json='{"page": 2, "limit": 7}',
        )

    client.observations_get_many.assert_called_once_with(page=2, limit=7)
    ingest.assert_called_once_with([])
    assert result == {
        "kind": "observations",
        "listed": 0,
        "ingested": {"nodes": 0, "edges": 0},
    }
