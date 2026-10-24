"""Release version consistency checks: the version is spelled once, in pyproject.toml."""

from __future__ import annotations

from importlib.metadata import version as installed_version
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[1]


def test_release_version_is_consistent_across_runtime_and_metadata() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    lock = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
    local_package = next(
        package for package in lock["package"] if package["name"] == "langfuse-agent"
    )
    expected = pyproject["project"]["version"]

    assert local_package["version"] == expected
    assert installed_version("langfuse-agent") == expected
    assert f"## [{expected}]" in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
