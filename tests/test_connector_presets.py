"""Current-only privacy and pagination contracts for MCP source presets."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PRESETS = ROOT / "langfuse_agent" / "connectors" / "mcp_source_presets.json"
CERTIFICATION = ROOT / "langfuse_agent" / "ontology" / "certification.json"
SENSITIVE_FIELDS = {"input", "output", "metadata", "userId", "sessionId"}


def _presets() -> dict[str, dict]:
    value = json.loads(PRESETS.read_text(encoding="utf-8"))
    return {name: preset for name, preset in value.items() if not name.startswith("_")}


def test_source_presets_use_current_pagination_enum() -> None:
    for preset in _presets().values():
        assert preset["pagination"] == "page"
        assert preset["page_kind"] == "number"


def test_source_presets_exclude_raw_observability_content() -> None:
    presets = _presets()

    assert presets["langfuse-traces"]["text_field"] == "name"
    assert presets["langfuse-sessions"]["text_field"] == "id"
    for preset in presets.values():
        assert preset["metadata_fields"]
        assert SENSITIVE_FIELDS.isdisjoint(preset["metadata_fields"])
        assert preset["text_field"] not in SENSITIVE_FIELDS


def test_signed_manifest_embeds_the_current_source_presets() -> None:
    manifest = yaml.safe_load((ROOT / "connector_manifest.yml").read_text("utf-8"))
    signed = {item["preset"]: item["raw"] for item in manifest["sync"]}

    assert signed == _presets()


def test_source_preset_digest_is_attested() -> None:
    certification = json.loads(CERTIFICATION.read_text(encoding="utf-8"))
    relative = PRESETS.relative_to(ROOT).as_posix()

    assert (
        certification["artifacts"][relative]
        == hashlib.sha256(PRESETS.read_bytes()).hexdigest()
    )
