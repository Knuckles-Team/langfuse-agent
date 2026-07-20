"""Release version consistency checks."""

from __future__ import annotations

import re
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "1.0.3"


def test_release_version_is_consistent_across_runtime_and_metadata() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    lock = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
    local_package = next(
        package for package in lock["package"] if package["name"] == "langfuse-agent"
    )

    assert pyproject["project"]["version"] == EXPECTED_VERSION
    assert local_package["version"] == EXPECTED_VERSION
    assert f"current_version = {EXPECTED_VERSION}" in (
        ROOT / ".bumpversion.cfg"
    ).read_text(encoding="utf-8")
    assert f"*Version: {EXPECTED_VERSION}*" in (ROOT / "README.md").read_text(
        encoding="utf-8"
    )
    dockerfile = (ROOT / "docker/Dockerfile").read_text(encoding="utf-8")
    assert dockerfile.count(f"langfuse-agent[mcp]=={EXPECTED_VERSION}") == 1
    assert dockerfile.count(f"langfuse-agent[agent]=={EXPECTED_VERSION}") == 1
    assert f"## [{EXPECTED_VERSION}] - 2026-07-17" in (ROOT / "CHANGELOG.md").read_text(
        encoding="utf-8"
    )
    for relative_path in (
        "langfuse_agent/agent_server.py",
        "langfuse_agent/mcp_server.py",
    ):
        source = (ROOT / relative_path).read_text(encoding="utf-8")
        version = re.search(r'^__version__ = "([^"]+)"$', source, re.MULTILINE)
        assert version is not None
        assert version.group(1) == EXPECTED_VERSION
