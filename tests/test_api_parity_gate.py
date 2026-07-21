"""Fail-closed coverage for the Langfuse API-to-MCP source gate."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_api_integration.py"


def _module():
    spec = importlib.util.spec_from_file_location("verify_api_integration", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_current_composed_client_is_fully_bound_to_mcp() -> None:
    result = _module().verify_agent(ROOT)

    assert result is not None
    assert result["total_methods"] > 0
    assert result["covered_methods"] == result["total_methods"]
    assert result["coverage"] == 100.0


def test_local_cli_executes_instead_of_skipping() -> None:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--local"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert completed.returncode == 0
    assert "Skipping" not in completed.stdout
    assert "100.0%" in completed.stdout


def test_local_cli_fails_closed_without_a_surface(tmp_path: Path) -> None:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--local"],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert completed.returncode == 1
    assert "required surface unavailable" in completed.stdout
    assert str(tmp_path) not in completed.stdout + completed.stderr
