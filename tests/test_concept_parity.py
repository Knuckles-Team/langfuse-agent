import os
import re
from importlib.util import find_spec
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _master_overview_path() -> Path | None:
    """Resolve the registry from the installed package without fixed checkout paths."""
    spec = find_spec("agent_utilities")
    if spec is None or spec.origin is None:
        return None

    candidate = Path(spec.origin).resolve().parent.parent / "docs" / "overview.md"
    return candidate if candidate.is_file() else None


def extract_concepts_from_overview(filepath):
    """Extracts concepts from the markdown table in the master overview.md"""
    if filepath is None or not filepath.is_file():
        return set()

    concepts = set()
    with filepath.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip().startswith("|"):
                continue
            if "Pillar | Sub-Concept" in line or "|---|" in line:
                continue

            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5:
                raw_id = parts[1].replace("*", "").strip()
                if re.match(r"^[A-Z]+-\d+(?:\.\d+)?$", raw_id):
                    concepts.add(raw_id)
    return concepts


def extract_concepts_from_codebase(directory):
    """Recursively scans source files in the project for CONCEPT:ID tags."""
    found_concepts = set()
    excluded_directories = {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".tox",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "node_modules",
        "site",
        "venv",
    }
    for root, directories, filenames in os.walk(directory, followlinks=False):
        directories[:] = [
            name for name in directories if name not in excluded_directories
        ]
        root_path = Path(root)
        for filename in filenames:
            filepath = root_path / filename
            if filepath.suffix not in {".py", ".ts", ".tsx", ".md"}:
                continue
            try:
                content = filepath.read_text(encoding="utf-8")
                matches = re.findall(r"CONCEPT:([A-Z]+-\d+(?:\.\d+)?)", content)
                found_concepts.update(matches)
            except (OSError, UnicodeError):
                pass
    return found_concepts


def test_concept_scan_prunes_generated_environments(tmp_path):
    marker = "".join(("CON", "CEPT:"))
    source = tmp_path / "source.py"
    source.write_text(f"# {marker}OS-1\n", encoding="utf-8")
    ignored = tmp_path / ".venv" / "lib" / "ignored.py"
    ignored.parent.mkdir(parents=True)
    ignored.write_text(f"# {marker}OS-999\n", encoding="utf-8")

    assert extract_concepts_from_codebase(tmp_path) == {"OS-1"}


def test_concept_parity():
    """
    Enforces that all concepts documented or used in langfuse-agent
    exist in the master agent-utilities registry.
    """
    master_concepts = extract_concepts_from_overview(_master_overview_path())

    # Extract concepts from this project
    local_codebase_concepts = extract_concepts_from_codebase(PROJECT_ROOT)

    # Only enforce parity for agent-utilities 5-Pillar concepts
    # Project-specific concepts (SX-*, AU-*, CE-*, TP-*, CA-*, etc.) are excluded
    agent_utilities_pillars = ("ORCH-", "KG-", "AHE-", "ECO-", "OS-")
    local_codebase_concepts = {
        c for c in local_codebase_concepts if c.startswith(agent_utilities_pillars)
    }

    # Ensure every concept used locally is registered in the master overview.md
    unregistered_concepts = local_codebase_concepts - master_concepts

    assert not unregistered_concepts, (
        f"The following concepts are used in langfuse-agent but are NOT registered "
        f"in the master agent-utilities/docs/overview.md registry: {unregistered_concepts}. "
        f"Please register them first."
    )
