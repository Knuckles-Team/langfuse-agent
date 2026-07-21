"""Static contract for Langfuse Agent's production and exact release images."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCKERFILE = ROOT / "docker" / "Dockerfile"
DOCKERIGNORE = ROOT / ".dockerignore"
PYTHON_IMAGE = (
    "python:3.12-slim@sha256:"
    "57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de"
)


def test_mcp_local_is_python312_hash_locked_and_path_origin_free() -> None:
    source = DOCKERFILE.read_text(encoding="utf-8")
    local_stage = source.split("FROM builder-base AS builder-mcp-local", 1)[1]
    local_stage = local_stage.split(f"FROM {PYTHON_IMAGE}", 1)[0]

    for required in (
        "--offline",
        "--no-index",
        "--only-binary :all:",
        "--require-hashes",
        "RELEASE_REQUIREMENTS_SHA256",
        'm.version("agent-utilities")',
        'm.version("epistemic-graph")',
        'm.version("langfuse-agent")',
        'shutil.which("graph-os")',
        'shutil.which("langfuse-mcp")',
        'glob("*.dist-info/direct_url.json")',
        "import epistemic_graph.numeric",
        "sys.version_info[:2] == (3, 12)",
    ):
        assert required in local_stage

    assert " @ file:" not in local_stage
    assert "FROM runtime-base AS mcp-local" in source
    exact_target = source.split("FROM runtime-base AS mcp-local", 1)[1]
    exact_target = exact_target.split("FROM runtime-base AS agent", 1)[0]
    assert 'CMD ["langfuse-mcp"]' in exact_target
    assert 'CMD ["langfuse-agent"]' not in exact_target
    assert source.count(f"FROM {PYTHON_IMAGE}") == 2
    assert "python:3.11" not in source
    assert source.rsplit("FROM runtime-base AS ", 1)[1].startswith("agent\n")
    assert "agent-utilities[agent]" not in source
    assert "dspy" not in source.casefold()
    assert "litellm" not in source.casefold()


def test_release_context_admits_only_wheels_and_requirements() -> None:
    ignored = DOCKERIGNORE.read_text(encoding="utf-8").splitlines()

    assert "release-wheelhouse/*" in ignored
    assert "!release-wheelhouse/*.whl" in ignored
    assert "!release-wheelhouse/*.txt" in ignored
