"""PIPE-CONNSPEC-R134.3: Langfuse Pages calls the shared dashboard workflow."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / ".github" / "spec-dashboard.json"

pytestmark = pytest.mark.spec("PIPE-CONNSPEC-R134.3")




def test_pages_dashboard_declares_generated_spec_status_source() -> None:
    dashboard = json.loads(DASHBOARD.read_text(encoding="utf-8"))

    assert dashboard == {
        "version": 1,
        "sources": [{"glob": "specs/*/status.json", "kind": "spec"}],
    }


def test_legacy_mkdocs_publisher_is_absent() -> None:
    assert not (ROOT / ".github/workflows/docs.yml").exists()
