"""The owned release workflow publishes one private, reproducible wheel only."""

from __future__ import annotations

import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/pipeline.yml"


def test_release_workflow_owns_a_twin_wheel_build() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")

    assert "Knuckles-Team/pipelines/.github/workflows/python_pipeline.yml" not in source
    assert 'SOURCE_DATE_EPOCH: "0"' in source
    assert source.count("uv build --wheel --no-build-isolation") == 2
    assert "--out-dir dist-primary" in source
    assert "--out-dir dist-reproduction" in source
    assert source.count("scripts/check_wheel_privacy.py") == 2
    assert "release wheel digest mismatch" in source
    assert "uv sync" not in source
    assert (
        "uv pip install --system --require-hashes -r release-build-requirements.txt"
    ) in source


def test_release_workflow_checks_contracts_and_publishes_no_source_archive() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")

    for contract in (
        "tests/test_wheel_sbom.py",
        "tests/test_wheel_privacy.py",
        "tests/test_release_version.py",
        "tests/test_release_image_contract.py",
        "tests/test_release_workflow_contract.py",
    ):
        assert contract in source
    assert "dist/langfuse_agent-*.whl" in source
    assert "--sdist" not in source
    assert "*.tar.gz" not in source
    assert " @ file:" not in source


def test_release_build_lock_is_a_governed_sanitizer_input() -> None:
    """The reproducible build lock must not make the source gate fail closed."""

    sanitizer = runpy.run_path(str(ROOT / "scripts" / "security_sanitizer.py"))
    assert "release-build-requirements.txt" in sanitizer["ALLOWED_TXT_NAMES"]
