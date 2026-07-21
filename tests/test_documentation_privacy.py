"""Keep public deployment examples independent of private environments."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_IPV4 = re.compile(
    r"\b(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|"
    r"172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})\b"
)
ENVIRONMENT_DNS = re.compile(r"(?i)\b(?:[A-Za-z0-9-]+\.)+(?:arpa|local)(?=[:/\s\"'])")
MACHINE_HOME = re.compile(
    r"(?i)(?:[A-Z]:[\\/]Users[\\/](?![<%$])[^\\/\s]+|"
    r"/(?:home|Users)/(?![<%$])[^/\s]+|"
    r"/mnt/[A-Z]/Users/(?![<%$])[^/\s]+)"
)


def test_public_deployment_examples_are_environment_neutral() -> None:
    for relative in ("README.md", "docs/deployment.md", "docs/installation.md"):
        content = (ROOT / relative).read_text(encoding="utf-8")
        assert PRIVATE_IPV4.search(content) is None, relative
        assert ENVIRONMENT_DNS.search(content) is None, relative
        assert MACHINE_HOME.search(content) is None, relative


def test_readme_tool_inventory_matches_current_generator() -> None:
    script = ROOT / "scripts" / "generate_readme_tools.py"
    spec = importlib.util.spec_from_file_location("generate_readme_tools", script)
    assert spec is not None and spec.loader is not None
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    current = readme[readme.index(generator.START) :]
    current = current[: current.index(generator.END) + len(generator.END)]
    assert current == generator._render()
    assert "`intent` default" in current
    assert "5 action-routed tool(s)" in current
    assert "81 verbose 1:1 tool(s)" in current


def test_local_documentation_links_resolve() -> None:
    pattern = re.compile(r"!?\[[^]]*\]\(([^)\n]+)\)")
    for page in [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]:
        for raw in pattern.findall(page.read_text(encoding="utf-8")):
            target = raw.strip().split(maxsplit=1)[0].strip("<>").split("#", 1)[0]
            if not target or "://" in target or target.startswith(("#", "/")):
                continue
            assert (page.parent / target).resolve().exists(), f"{page}: {target}"
