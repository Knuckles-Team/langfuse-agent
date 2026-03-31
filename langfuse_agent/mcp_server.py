import os
import sys
import logging
from typing import Any, Dict
from dotenv import load_dotenv, find_dotenv
from fastmcp import FastMCP

__version__ = "0.1.2"

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import create_mcp_server
from .auth import get_client

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def register_telemetry_tools(mcp: FastMCP):
    @mcp.tool(name="langfuse-get-traces", description="Get a paginated list of traces")
    def langfuse_get_traces(page: int = 1, limit: int = 50) -> Dict[str, Any]:
        return get_client().get_traces(page=page, limit=limit)

    @mcp.tool(
        name="langfuse-get-metrics", description="Get daily metrics from Langfuse"
    )
    def langfuse_get_metrics() -> Dict[str, Any]:
        return get_client().get_metrics()


def register_annotation_tools(mcp: FastMCP):
    @mcp.tool(
        name="langfuse-get-annotation-queues", description="Get all annotation queues"
    )
    def langfuse_get_annotation_queues(
        page: int = 1, limit: int = 50
    ) -> Dict[str, Any]:
        return get_client().get_annotation_queues(page=page, limit=limit)


def register_prompts(mcp: FastMCP):
    @mcp.prompt(
        name="langfuse-system-summary",
        description="Get a summary of the Langfuse application.",
    )
    def langfuse_system_summary() -> str:
        return "Check Langfuse metrics, traces, and available annotation queues."


def get_mcp_instance() -> tuple[Any, Any, Any, Any]:
    load_dotenv(find_dotenv())

    args, mcp, middlewares = create_mcp_server(
        name="langfuse",
        version=__version__,
        instructions="Langfuse Agent MCP Server",
    )

    registered_tags = []

    if to_boolean(os.getenv("TELEMETRYTOOL", "True")):
        register_telemetry_tools(mcp)
        registered_tags.append("telemetry")

    if to_boolean(os.getenv("ANNOTATIONTOOL", "True")):
        register_annotation_tools(mcp)
        registered_tags.append("annotation")

    register_prompts(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    return mcp, args, middlewares, registered_tags


def mcp_server():
    mcp, args, middlewares, registered_tags = get_mcp_instance()

    print(f"Langfuse Agent MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)
    print(f"  Dynamic Tags Loaded: {registered_tags}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error(f"Invalid transport: {args.transport}")
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
