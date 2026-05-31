#!/usr/bin/python
"""Langfuse MCP Server.

_1.0 — Langfuse MCP Integration
"""

import warnings

from fastmcp.utilities.logging import get_logger

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import logging
import os
import sys

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import create_mcp_server

from langfuse_agent.tools.datasets import register_langfuse_datasets_tools
from langfuse_agent.tools.management import register_langfuse_management_tools
from langfuse_agent.tools.observability import register_langfuse_observability_tools
from langfuse_agent.tools.prompts import register_langfuse_prompts_models_tools

__version__ = "0.24.0"

logger = get_logger(name="langfuse-agent")
logger.setLevel(logging.INFO)


def get_mcp_instance():
    """Get the configured FastMCP instance.

    _1.0 — Langfuse MCP Integration
    """
    args, mcp, middlewares = create_mcp_server(
        name="langfuse",
        version=__version__,
        instructions="langfuse-agent MCP Server — Condensed Action-Routed Tools.",
    )
    DEFAULT_OBSERVABILITYTOOL = to_boolean(os.getenv("OBSERVABILITY_TOOL", "True"))
    if DEFAULT_OBSERVABILITYTOOL:
        register_langfuse_observability_tools(mcp)
    DEFAULT_DATASETSTOOL = to_boolean(os.getenv("DATASETS_TOOL", "True"))
    if DEFAULT_DATASETSTOOL:
        register_langfuse_datasets_tools(mcp)
    DEFAULT_PROMPTSMODELSTOOL = to_boolean(os.getenv("PROMPTS_MODELS_TOOL", "True"))
    if DEFAULT_PROMPTSMODELSTOOL:
        register_langfuse_prompts_models_tools(mcp)
    DEFAULT_MANAGEMENTTOOL = to_boolean(os.getenv("MANAGEMENT_TOOL", "True"))
    if DEFAULT_MANAGEMENTTOOL:
        register_langfuse_management_tools(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)
    return mcp, args, middlewares


def mcp_server() -> None:
    """Run the MCP server.

    _1.0 — Langfuse MCP Integration
    """
    mcp, args, middlewares = get_mcp_instance()
    print(f"langfuse-agent MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error("Invalid transport", extra={"transport": args.transport})
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
