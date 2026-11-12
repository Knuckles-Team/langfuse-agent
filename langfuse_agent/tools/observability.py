"""Observability tools that are not client-method wrappers.

Every Langfuse API operation is served as one typed tool per ``LangfuseApi`` method
(``langfuse_trace_list``, ``langfuse_scores_get_many``, ...). Only the privacy
posture read, which needs no client, is written here.

CONCEPT:LA_1.0 — Langfuse MCP Integration
"""

from fastmcp import FastMCP

from langfuse_agent.runtime_posture import observability_runtime_posture


def register_langfuse_observability_tools(mcp: FastMCP):
    """Register the runtime posture tool.

    CONCEPT:LA_1.0 — Langfuse MCP Integration
    """

    @mcp.tool(tags={"langfuse"})
    async def langfuse_runtime_posture() -> dict[str, bool]:
        """Read the effective content-retention posture: whether content capture is on."""
        return observability_runtime_posture()
