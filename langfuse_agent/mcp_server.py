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
import sys

from agent_utilities.mcp_utilities import (
    create_mcp_server,
    load_config,
    register_tool_surface,
)

from langfuse_agent.api_client import LangfuseApi
from langfuse_agent.auth import get_client
from langfuse_agent.tools.datasets import register_langfuse_datasets_tools
from langfuse_agent.tools.management import register_langfuse_management_tools
from langfuse_agent.tools.observability import register_langfuse_observability_tools
from langfuse_agent.tools.prompts import register_langfuse_prompts_models_tools

__version__ = "1.0.1"

logger = get_logger(name="langfuse-agent")
logger.setLevel(logging.INFO)

# Re-exported so register_tool_surface(tools_module=...) auto-discovers them as
# module attributes (and ruff treats the imports as used).
__all__ = [
    "register_langfuse_datasets_tools",
    "register_langfuse_management_tools",
    "register_langfuse_observability_tools",
    "register_langfuse_prompts_models_tools",
]


def get_mcp_instance():
    """Get the configured FastMCP instance.

    _1.0 — Langfuse MCP Integration
    """
    load_config()
    args, mcp, middlewares = create_mcp_server(
        name="langfuse",
        version=__version__,
        instructions="langfuse-agent MCP Server — Condensed Action-Routed Tools.",
    )
    registered_tags = register_tool_surface(
        mcp,
        client_cls=LangfuseApi,
        get_client=get_client,
        service="langfuse-agent",
        tools_module=sys.modules[__name__],
    )
    logger.info("Registered condensed tool tags", extra={"tags": registered_tags})

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
