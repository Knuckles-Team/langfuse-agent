#!/usr/bin/python
"""Langfuse MCP Server.

_1.0 — Langfuse MCP Integration
"""

import warnings

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


from langfuse_agent.tools.datasets import register_langfuse_datasets_tools
from langfuse_agent.tools.kg import register_langfuse_kg_tools
from langfuse_agent.tools.management import register_langfuse_management_tools
from langfuse_agent.tools.observability import register_langfuse_observability_tools
from langfuse_agent.tools.prompts import register_langfuse_prompts_models_tools

# Re-exported so register_tool_surface(tools_module=...) auto-discovers them as
# module attributes (and ruff treats the imports as used).
__all__ = [
    "register_langfuse_datasets_tools",
    "register_langfuse_kg_tools",
    "register_langfuse_management_tools",
    "register_langfuse_observability_tools",
    "register_langfuse_prompts_models_tools",
]
