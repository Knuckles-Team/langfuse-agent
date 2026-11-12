"""The hand-written Langfuse tools and the privacy posture."""

import asyncio

from fastmcp import Client, FastMCP

from langfuse_agent.mcp_server import register_langfuse_observability_tools


def test_runtime_posture_tool_is_typed_and_metadata_only(monkeypatch):
    monkeypatch.setenv("LANGFUSE_CAPTURE_CONTENT", "false")
    mcp = FastMCP("test-mcp")
    register_langfuse_observability_tools(mcp)

    async def call():
        async with Client(mcp) as client:
            tools = await client.list_tools()
            assert [t.name for t in tools] == ["langfuse_runtime_posture"]
            assert "action" not in tools[0].inputSchema.get("properties", {})
            return await client.call_tool("langfuse_runtime_posture", {})

    result = asyncio.run(call())
    assert result.data == {"content_capture_enabled": False, "metadata_only": True}


def test_observability_runtime_posture_is_metadata_only(monkeypatch):
    from langfuse_agent.runtime_posture import observability_runtime_posture

    monkeypatch.setenv("LANGFUSE_CAPTURE_CONTENT", "false")

    assert observability_runtime_posture() == {
        "content_capture_enabled": False,
        "metadata_only": True,
    }
