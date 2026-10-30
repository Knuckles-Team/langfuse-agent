"""PIPE-CONNSPEC-R134.4: the Langfuse development skill is packaged."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "langfuse_agent" / "skills" / "langfuse-agent-development" / "SKILL.md"

pytestmark = pytest.mark.spec("PIPE-CONNSPEC-R134.4")


def test_development_skill_has_rapid_contract_and_package_binding() -> None:
    text = SKILL.read_text(encoding="utf-8")
    frontmatter = text.split("---", 2)[1]
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert SKILL.is_file()
    assert re.search(r"^name:\s*langfuse-agent-development\s*$", frontmatter, re.M)
    assert re.search(r"^skill_type:\s*skill\s*$", frontmatter, re.M)
    assert "## Rapid delivery: the 5-minute contract" in text
    for term in (
        "langfuse_agent/__init__.py",
        "langfuse_agent/api_client.py",
        "langfuse_agent/api/",
        "langfuse_agent/auth.py",
        "langfuse_agent/tools/",
        "langfuse_agent/mcp_server.py",
        "langfuse_agent/kg_ingest.py",
        "langfuse_agent/connector_sources.py",
        "langfuse_agent/ontology/",
        "LANGFUSE_BASE_URL",
        "LANGFUSE_HOST",
        "LANGFUSE_PUBLIC_KEY",
        "LANGFUSE_SECRET_KEY",
        "LANGFUSE_PERSISTENCE_HMAC_KEY_REF",
        "MCP_TOOL_MODE",
        "skills/**",
        "pages_pipeline.yml@main",
        "uv run --locked --extra test pytest",
    ):
        assert term in text

    assert "verify=False" not in text
    assert "--no-verify" not in text
    package_data = project["tool"]["setuptools"]["package-data"]["langfuse_agent"]
    assert "skills/**" in package_data
    assert project["project"]["scripts"] == {
        "langfuse-mcp": "scion_sdk.cli:serve",
    }
