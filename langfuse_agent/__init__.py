#!/usr/bin/env python
"""langfuse-agent package.

CONCEPT:LA_1.0 — Langfuse MCP Integration
"""

import importlib
import inspect
from typing import Any

__all__: list[str] = []

CORE_MODULES: list[str] = ["langfuse_agent.api_client"]

OPTIONAL_MODULES = {
    "langfuse_agent.agent_server": "agent",
    "langfuse_agent.mcp_server": "mcp",
}


def _expose_members(module):
    """Expose public classes and functions from a module into globals and __all__."""
    for name, obj in inspect.getmembers(module):
        if (inspect.isclass(obj) or inspect.isfunction(obj)) and not name.startswith(
            "_"
        ):
            globals()[name] = obj
            if name not in __all__:
                __all__.append(name)


# Eagerly import core modules (keeps API wrappers fast & light)
for module_name in CORE_MODULES:
    if module_name:
        module = importlib.import_module(module_name)
        _expose_members(module)

# Dynamic/lazy loading of optional modules (agent_server, mcp_server)
_loaded_optional_modules: dict[str, Any] = {}


def _import_module_safely(module_name: str):
    """Try to import a module and return it, or None if not available."""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None


# Availability flags map to the substring identifying their optional module.
_AVAILABILITY_FLAGS = {
    "_MCP_AVAILABLE": "mcp_server",
    "_AGENT_AVAILABLE": "agent_server",
}

_MISSING = object()


def _optional_module_available(substring: str) -> bool:
    module_name = next((k for k in OPTIONAL_MODULES if substring in k), None)
    if module_name is None:
        return False
    return _import_module_safely(module_name) is not None


def _load_optional_module_attribute(module_name: str, name: str) -> Any:
    """Lazily import ``module_name`` and return its ``name`` attribute, or ``_MISSING``."""
    if module_name not in _loaded_optional_modules:
        module = _import_module_safely(module_name)
        if module is not None:
            _loaded_optional_modules[module_name] = module
            _expose_members(module)

    module = _loaded_optional_modules.get(module_name)
    if module is not None and hasattr(module, name):
        return getattr(module, name)
    return _MISSING


def __getattr__(name: str) -> Any:
    # Handle availability flags dynamically without eager imports
    if name in _AVAILABILITY_FLAGS:
        return _optional_module_available(_AVAILABILITY_FLAGS[name])

    # Check optional modules
    for module_name in OPTIONAL_MODULES:
        value = _load_optional_module_attribute(module_name, name)
        if value is not _MISSING:
            return value

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(list(globals().keys()) + __all__)
