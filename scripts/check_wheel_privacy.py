#!/usr/bin/env python3
"""Fail closed when a built wheel contains non-runtime or identifying artifacts."""

from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path, PurePosixPath

_EMAIL = re.compile(rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_MACHINE_PATHS = (
    re.compile(rb"(?i)[A-Z]:\\\\Users\\\\[^\\\\\s]+"),
    re.compile(rb"(?<![A-Za-z0-9._-])/mnt/[A-Za-z]/Users/[^/\s]+"),
    re.compile(rb"(?<![A-Za-z0-9._-])/Users/[^/\s]+"),
    re.compile(rb"(?<![A-Za-z0-9._-])/home/[^/\s]+"),
)
_NON_RUNTIME_PARTS = {"__pycache__", "docs", "scripts", "tests"}
_BYTECODE_SUFFIXES = {".pyc", ".pyo"}


def wheel_privacy_findings(wheel: Path) -> tuple[str, ...]:
    """Return stable finding categories without exposing matched content."""
    findings: set[str] = set()
    with zipfile.ZipFile(wheel) as archive:
        for member in archive.infolist():
            path = PurePosixPath(member.filename)
            parts = path.parts
            if path.is_absolute() or ".." in parts:
                findings.add("unsafe-member-path")
            if any(part in _NON_RUNTIME_PARTS for part in parts):
                findings.add("non-runtime-content")
            if path.suffix.lower() in _BYTECODE_SUFFIXES:
                findings.add("bytecode-content")
            if member.is_dir():
                continue
            payload = archive.read(member)
            if _EMAIL.search(payload):
                findings.add("email-like-content")
            if any(pattern.search(payload) for pattern in _MACHINE_PATHS):
                findings.add("machine-path-content")
    return tuple(sorted(findings))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wheel", type=Path)
    args = parser.parse_args()
    findings = wheel_privacy_findings(args.wheel)
    if findings:
        print(f"wheel_privacy_gate=failed findings={','.join(findings)}")
        return 1
    print("wheel_privacy_gate=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
