#!/usr/bin/env python3
import ast
import glob
import os
import sys

BASELINES = {
    "adguard-home-agent": 89.2,
    "ansible-tower-mcp": 94.7,
    "archivebox-api": 85.7,
    "documentdb-mcp": 100.0,
    "github-agent": 100.0,
    "gitlab-api": 6.4,
    "home-assistant-agent": 63.6,
    "jellyfin-mcp": 81.0,
    "langfuse-agent": 100.0,
    "listmonk-api": 87.5,
    "mealie-mcp": 96.4,
    "microsoft-agent": 99.6,
    "nextcloud-agent": 52.6,
    "owncast-agent": 100.0,
    "plane-agent": 54.9,
    "portainer-agent": 35.5,
    "postiz-agent": 0.0,
    "qbittorrent-agent": 70.8,
    "scholarx": 90.0,
    "servicenow-api": 73.1,
    "stirlingpdf-agent": 0.0,
    "wger-agent": 41.7,
}


def _is_api_client_class(node: ast.ClassDef) -> bool:
    # Focus on Api or Client classes
    class_name = node.name.lower()
    return "api" in class_name or "client" in class_name or node.name == "Api"


def _public_client_methods(node: ast.ClassDef) -> dict:
    methods = {}
    for item in node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Filter out private methods and constructor
            if not item.name.startswith("_") and item.name != "authenticate":
                methods[item.name] = {"line": item.lineno, "class": node.name}
    return methods


def parse_api_client(filepath):
    """
    Parses api_client.py to find the main API/Client class and its public methods.
    Returns a set of method names.
    """
    with open(filepath, encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filepath)

    methods = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and _is_api_client_class(node):
            methods.update(_public_client_methods(node))
    return methods


class MethodCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.called_methods = set()
        self.action_literals = set()

    def visit_Attribute(self, node):
        # E.g. client.get_repositories
        if isinstance(node.value, ast.Name):
            # Typically client, api, self
            if node.value.id in ("client", "api", "self"):
                self.called_methods.add(node.attr)
        self.generic_visit(node)

    def visit_Call(self, node):
        # E.g. getattr(client, "foo")
        if isinstance(node.func, ast.Name) and node.func.id == "getattr":
            if len(node.args) >= 2 and isinstance(node.args[0], ast.Name):
                if node.args[0].id in ("client", "api"):
                    if isinstance(node.args[1], ast.Constant):
                        self.called_methods.add(node.args[1].value)
        self.generic_visit(node)

    def visit_Compare(self, node):
        # Capture action comparisons, e.g. action == "get"
        for op, comparator in zip(node.ops, node.comparators, strict=False):
            if isinstance(op, (ast.Eq, ast.In)):
                if isinstance(comparator, ast.Constant) and isinstance(
                    comparator.value, str
                ):
                    self.action_literals.add(comparator.value)
        self.generic_visit(node)


def _register_tool_surface_call(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    is_register_call = (
        isinstance(func, ast.Name) and func.id == "register_tool_surface"
    ) or (isinstance(func, ast.Attribute) and func.attr == "register_tool_surface")
    if not is_register_call:
        return False
    return any(
        keyword.arg == "client_cls" and isinstance(keyword.value, ast.Name)
        for keyword in node.keywords
    )


def _uses_introspected_surface(tree: ast.AST) -> bool:
    # The current fleet surface is generated from the complete client class by
    # Agent Utilities.  Treat that binding as authoritative only when the call
    # explicitly supplies ``client_cls``; a bare helper import is insufficient.
    return any(_register_tool_surface_call(node) for node in ast.walk(tree))


_TOOL_NAME_PREFIXES = ("github_", "gitlab_", "adguard_", "atlassian_")


def _is_tool_decorated(node) -> bool:
    for dec in node.decorator_list:
        if isinstance(dec, ast.Call):
            func = dec.func
            if isinstance(func, ast.Attribute) and func.attr == "tool":
                return True
        elif isinstance(dec, ast.Attribute) and dec.attr == "tool":
            return True
    return False


def _is_relevant_tool_function(node) -> bool:
    # Check if this function is a tool (e.g. decorated with mcp.tool) or one
    # of the legacy fixed-prefix connector tool families.
    return _is_tool_decorated(node) or node.name.startswith(_TOOL_NAME_PREFIXES)


def _tool_mapping(node, api_methods):
    visitor = MethodCallVisitor()
    visitor.visit(node)
    # Find which of the visited methods are in our api_methods list
    mapped = visitor.called_methods.intersection(api_methods.keys())
    mapping = {"methods": list(mapped), "actions": list(visitor.action_literals)}
    return mapping, mapped


def parse_mcp_server(filepath, api_methods):
    """
    Parses mcp_server.py to extract registered tools and identify which
    api_methods they leverage.
    """
    with open(filepath, encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filepath)

    tool_mappings = {}
    all_mapped_methods = set()

    if _uses_introspected_surface(tree):
        all_mapped_methods.update(api_methods)

    for node in ast.walk(tree):
        if isinstance(
            node, (ast.FunctionDef, ast.AsyncFunctionDef)
        ) and _is_relevant_tool_function(node):
            mapping, mapped = _tool_mapping(node, api_methods)
            tool_mappings[node.name] = mapping
            all_mapped_methods.update(mapped)

    return tool_mappings, all_mapped_methods


def verify_agent(agent_dir):
    # Generated clients are split across ``api_client_<domain>.py`` modules and
    # composed by ``api_client.py``.  Scanning only the composition class yields
    # zero methods and used to turn this required gate into a silent skip.
    api_clients = sorted(
        glob.glob(os.path.join(agent_dir, "**", "api_client*.py"), recursive=True)
    )
    mcp_servers = glob.glob(
        os.path.join(agent_dir, "**", "mcp_server.py"), recursive=True
    )

    if not api_clients or not mcp_servers:
        return None

    mcp_server_path = mcp_servers[0]

    api_methods = {}
    for api_client_path in api_clients:
        api_methods.update(parse_api_client(api_client_path))
    if not api_methods:
        return None

    tool_mappings, mapped_methods = parse_mcp_server(mcp_server_path, api_methods)

    total_methods = len(api_methods)
    covered_methods = len(mapped_methods)
    coverage = (covered_methods / total_methods) * 100 if total_methods > 0 else 0.0

    unmapped = set(api_methods.keys()) - mapped_methods

    return {
        "agent_name": os.path.basename(agent_dir),
        "api_client_count": len(api_clients),
        "mcp_server": mcp_server_path,
        "total_methods": total_methods,
        "covered_methods": covered_methods,
        "coverage": coverage,
        "unmapped": sorted(list(unmapped)),
        "mapped": sorted(list(mapped_methods)),
        "tool_mappings": tool_mappings,
    }


def _print_local_report(res, baseline) -> bool:
    """Print the local single-agent coverage report; return whether it passed."""
    agent_name = res["agent_name"]
    coverage = res["coverage"]
    print(f"=== API-to-MCP Integration Parity Check for: {agent_name} ===")
    print(f"- API client methods: {res['total_methods']}")
    print(f"- Integrated methods: {res['covered_methods']}")
    print(f"- Current Coverage  : {coverage:.1f}%")
    print(f"- Target Baseline   : {baseline:.1f}%")

    # Allow small floating point tolerance (0.05%)
    if coverage < (baseline - 0.05):
        print(
            f"\n❌ FAILED: Integration coverage ({coverage:.1f}%) has DEGRADED below the required baseline of {baseline:.1f}%!"
        )
        print(
            "Please ensure any new or refactored API client methods are properly integrated into MCP server tools."
        )
        if res["unmapped"]:
            print("\nUnmapped API methods:")
            for m in res["unmapped"]:
                print(f"  - {m}")
        return False
    print("\n✅ PASSED: Integration coverage meets or exceeds the required baseline!")
    return True


def _run_local_mode() -> int:
    """Validate the current working directory as a single agent. Returns exit code."""
    cwd = os.getcwd()
    res = verify_agent(cwd)
    if not res:
        print("API-to-MCP integration parity failed: required surface unavailable.")
        return 1
    baseline = BASELINES.get(res["agent_name"], 0.0)
    return 0 if _print_local_report(res, baseline) else 1


def _fleet_agent_dirs(agents_dir: str) -> list:
    agent_dirs = [
        d for d in glob.glob(os.path.join(agents_dir, "*")) if os.path.isdir(d)
    ]
    # Also support nested subdirectories if any
    nested_dirs = [
        d for d in glob.glob(os.path.join(agents_dir, "*", "*")) if os.path.isdir(d)
    ]
    return sorted(set(agent_dirs + nested_dirs))


def _fleet_scan_results(agents_dir: str) -> list:
    results = []
    for agent_dir in _fleet_agent_dirs(agents_dir):
        # Avoid directories starting with dot or venv
        if (
            os.path.basename(agent_dir).startswith(".")
            or "venv" in agent_dir
            or "egg-info" in agent_dir
        ):
            continue
        try:
            res = verify_agent(agent_dir)
            if res:
                results.append(res)
        except Exception as e:
            print(f"Operation failed: {type(e).__name__}", file=sys.stderr)
    return results


def _print_fleet_summary_table(results: list) -> None:
    print("# API to MCP Integration Parity Report")
    print("Scan scope: provider fleet\n")
    print("| Agent Name | API Methods | Covered Methods | Coverage % | Status |")
    print("|---|---|---|---|---|")
    for r in results:
        status = "✅ 100%" if r["coverage"] >= 100.0 else "⚠️ Parity Gap"
        print(
            f"| {r['agent_name']} | {r['total_methods']} | {r['covered_methods']} | {r['coverage']:.1f}% | {status} |"
        )


def _print_fleet_gap_detail(r: dict, agents_dir: str) -> None:
    if r["coverage"] < 100.0:
        print(f"### ⚠️ {r['agent_name']} ({r['coverage']:.1f}% Integration)")
        print(f"- **API Client**: `{os.path.relpath(r['api_client'], agents_dir)}`")
        print(f"- **MCP Server**: `{os.path.relpath(r['mcp_server'], agents_dir)}`")
        print("- **Unmapped API Methods**:")
        for m in r["unmapped"]:
            print(f"  - `{m}`")
        print()
    else:
        print(f"### ✅ {r['agent_name']} (100% Integration)")
        print(f"- All {r['total_methods']} methods successfully mapped to MCP tools.")
        print()


def _run_workspace_scan() -> None:
    agents_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    results = _fleet_scan_results(agents_dir)
    _print_fleet_summary_table(results)
    print("\n## Detailed Parity Gaps\n")
    for r in results:
        _print_fleet_gap_detail(r, agents_dir)


def main():
    args = sys.argv[1:]

    # --- Local Mode (Single Agent Validation) ---
    if "--local" in args or "--pre-commit" in args:
        sys.exit(_run_local_mode())

    # --- Default Mode (Workspace-wide Scan) ---
    _run_workspace_scan()


if __name__ == "__main__":
    main()
