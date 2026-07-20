#!/usr/bin/env python3
"""Regenerate the README MCP tool inventory from the current source surface."""

from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
START = "<!-- MCP-TOOLS-TABLE:START -->"
END = "<!-- MCP-TOOLS-TABLE:END -->"

CONDENSED = (
    ("langfuse_datasets", "LANGFUSE_DATASETSTOOL"),
    ("langfuse_ingest", "LANGFUSE_KGTOOL"),
    ("langfuse_management", "LANGFUSE_MANAGEMENTTOOL"),
    ("langfuse_observability", "LANGFUSE_OBSERVABILITYTOOL"),
    ("langfuse_prompts_models", "LANGFUSE_PROMPTS_MODELSTOOL"),
)


def _description(node: ast.FunctionDef) -> str:
    text = " ".join(
        (ast.get_docstring(node) or "Current Langfuse API operation.").split()
    )
    text = text.replace("|", "\\|")
    return text if len(text) <= 240 else f"{text[:237].rstrip()}…"


def _api_methods() -> list[tuple[str, str]]:
    methods: dict[str, str] = {}
    for path in sorted((ROOT / "langfuse_agent" / "api").glob("api_client_*.py")):
        if path.name == "api_client_base.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for item in tree.body:
            if not isinstance(item, ast.ClassDef) or item.name != "Api":
                continue
            for node in item.body:
                if isinstance(
                    node, (ast.FunctionDef, ast.AsyncFunctionDef)
                ) and not node.name.startswith("_"):
                    methods[node.name] = _description(node)
    return sorted(methods.items())


def _render() -> str:
    methods = _api_methods()
    lines = [
        START,
        "",
        "#### Condensed action-routed tools (`MCP_TOOL_MODE=condensed` or `both`)",
        "",
        "| MCP Tool | Toggle Env Var | Description |",
        "|----------|----------------|-------------|",
    ]
    lines.extend(
        f"| `{name}` | `{toggle}` | Perform {name} operations. |"
        for name, toggle in CONDENSED
    )
    lines.extend(
        [
            "",
            "#### Verbose 1:1 API-mapped tools (`MCP_TOOL_MODE=verbose` or `both`)",
            "",
            "<details>",
            f"<summary>{len(methods)} per-operation tools — one per current public API method (click to expand)</summary>",
            "",
            "| MCP Tool | Toggle Env Var | Description |",
            "|----------|----------------|-------------|",
        ]
    )
    lines.extend(
        f"| `langfuse_{name}` | `APITOOL` | {description} |"
        for name, description in methods
    )
    lines.extend(
        [
            "",
            "</details>",
            "",
            f"_{len(CONDENSED)} action-routed tool(s) · {len(methods)} verbose 1:1 tool(s). "
            "`MCP_TOOL_MODE` selects the surface (`intent` default · `condensed` "
            "action-routed · `verbose` 1:1 · `both`). Auto-generated — do not edit._",
            END,
        ]
    )
    return "\n".join(lines)


def main() -> int:
    text = README.read_text(encoding="utf-8")
    pattern = re.compile(rf"{re.escape(START)}.*?{re.escape(END)}", re.DOTALL)
    if len(pattern.findall(text)) != 1:
        raise SystemExit("README tool inventory markers must occur exactly once")
    rendered = pattern.sub(_render(), text)
    README.write_text(rendered, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
