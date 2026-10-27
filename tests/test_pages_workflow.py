"""PIPE-CONNSPEC-R134.3: Langfuse Pages calls the shared dashboard workflow."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "pages.yml"
DASHBOARD = ROOT / ".github" / "spec-dashboard.json"

pytestmark = pytest.mark.spec("PIPE-CONNSPEC-R134.3")


def test_pages_workflow_enables_dashboard_and_pages_permissions() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "Knuckles-Team/pipelines/.github/workflows/pages_pipeline.yml@main" in workflow
    assert re.search(r"(?m)^\s*spec_dashboard_enabled:\s*true\s*$", workflow)
    assert re.search(r"(?m)^\s*spec_dashboard_config:\s*\.github/spec-dashboard\.json\s*$", workflow)
    assert re.search(r"(?m)^\s*pages:\s*write\s*$", workflow)
    assert re.search(r"(?m)^\s*id-token:\s*write\s*$", workflow)
    assert "workflow_dispatch: {}" in workflow
    assert "specs/**" in workflow


def test_pages_dashboard_declares_generated_spec_status_source() -> None:
    dashboard = json.loads(DASHBOARD.read_text(encoding="utf-8"))

    assert dashboard == {
        "version": 1,
        "sources": [{"glob": "specs/*/status.json", "kind": "spec"}],
    }


def test_legacy_mkdocs_publisher_is_absent() -> None:
    assert not (ROOT / ".github/workflows/docs.yml").exists()
