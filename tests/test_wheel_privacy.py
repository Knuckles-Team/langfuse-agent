from __future__ import annotations

import importlib.util
import zipfile
from pathlib import Path
from types import ModuleType


def _gate_module() -> ModuleType:
    source = Path(__file__).parents[1] / "scripts" / "check_wheel_privacy.py"
    spec = importlib.util.spec_from_file_location("check_wheel_privacy", source)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _wheel(tmp_path: Path, members: dict[str, bytes]) -> Path:
    path = tmp_path / "synthetic.whl"
    with zipfile.ZipFile(path, "w") as archive:
        for name, payload in members.items():
            archive.writestr(name, payload)
    return path


def test_wheel_privacy_gate_accepts_runtime_only_content(tmp_path: Path) -> None:
    gate = _gate_module()
    wheel = _wheel(
        tmp_path,
        {
            "langfuse_agent/__init__.py": b'__version__ = "1.0.1"',
            "langfuse_agent-1.0.1.dist-info/METADATA": b"Name: langfuse-agent",
        },
    )

    assert gate.wheel_privacy_findings(wheel) == ()


def test_wheel_privacy_gate_rejects_non_runtime_and_identifying_content(
    tmp_path: Path,
) -> None:
    gate = _gate_module()
    wheel = _wheel(
        tmp_path,
        {
            "tests/test_fixture.py": b"identity@example.test",
            "langfuse_agent/__pycache__/module.pyc": b"/home/operator/project",
        },
    )

    assert gate.wheel_privacy_findings(wheel) == (
        "bytecode-content",
        "email-like-content",
        "machine-path-content",
        "non-runtime-content",
    )
