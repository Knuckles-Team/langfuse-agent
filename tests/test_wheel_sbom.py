"""The provider wheel always carries deterministic, path-neutral SBOM metadata."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

import pytest
import tomllib
from packaging.requirements import Requirement
from packaging.version import Version

import build_backend
from scripts import security_contract

ROOT = Path(__file__).resolve().parents[1]


def _requirement_named(declarations: list[str], name: str) -> Requirement:
    matches = [
        requirement
        for declaration in declarations
        if (requirement := Requirement(declaration)).name == name
    ]
    assert len(matches) == 1
    return matches[0]


def _license_catalog(
    path: Path,
    licenses: dict[str, str] | None = None,
) -> Path:
    path.write_text(
        json.dumps(
            {
                "version": 1,
                "licenses": licenses or {"fixture": "MIT", "requests": "Apache-2.0"},
            }
        ),
        encoding="utf-8",
    )
    return path


def _project_requirement_names(pyproject: dict) -> set[str]:
    declarations = list(pyproject["project"].get("dependencies") or ())
    for values in pyproject["project"].get("optional-dependencies", {}).values():
        declarations.extend(values)
    for values in pyproject.get("dependency-groups", {}).values():
        declarations.extend(values)
    return {
        build_backend._normalized_name(Requirement(value).name)
        for value in declarations
    } | {build_backend._normalized_name(pyproject["project"]["name"])}


def _project_metadata(pyproject: dict) -> bytes:
    declarations = list(pyproject["project"].get("dependencies") or ())
    for values in pyproject["project"].get("optional-dependencies", {}).values():
        declarations.extend(values)
    return (
        "\n".join(
            [
                "Metadata-Version: 2.4",
                f"Name: {pyproject['project']['name']}",
                f"Version: {pyproject['project']['version']}",
                *(f"Requires-Dist: {value}" for value in sorted(set(declarations))),
                "",
                "",
            ]
        )
    ).encode()


def _wheel(path: Path, requirement: str) -> None:
    dist = "fixture-1.0.0.dist-info/"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("fixture/__init__.py", b"")
        archive.writestr(
            dist + "METADATA",
            (
                "Metadata-Version: 2.4\n"
                "Name: fixture\n"
                "Version: 1.0.0\n"
                f"Requires-Dist: {requirement}\n\n"
            ).encode(),
        )
        archive.writestr(
            dist + "WHEEL",
            b"Wheel-Version: 1.0\nRoot-Is-Purelib: true\nTag: py3-none-any\n",
        )
        archive.writestr(dist + "RECORD", b"")


def _wheel_with_variant_zip_metadata(
    path: Path,
    *,
    timestamp: tuple[int, int, int, int, int, int],
    reverse: bool,
    permissive_modes: bool,
) -> None:
    """Write equivalent wheels whose source ZIP metadata deliberately differs."""

    dist = "fixture-1.0.0.dist-info/"
    regular_mode = 0o100666 if permissive_modes else 0o100600
    executable_mode = 0o100777 if permissive_modes else 0o100700
    directory_mode = 0o40777 if permissive_modes else 0o40700
    members = [
        ("fixture/", b"", directory_mode),
        ("fixture/__init__.py", b"", regular_mode),
        ("fixture/runner", b"#!/usr/bin/env python\n", executable_mode),
        (
            "fixture-1.0.0.data/scripts/fixture-tool",
            b"#!/usr/bin/env python\n",
            executable_mode,
        ),
        (
            dist + "METADATA",
            b"Metadata-Version: 2.4\n"
            b"Name: fixture\n"
            b"Version: 1.0.0\n"
            b"Requires-Dist: requests>=2\n\n",
            regular_mode,
        ),
        (
            dist + "WHEEL",
            b"Wheel-Version: 1.0\nRoot-Is-Purelib: true\nTag: py3-none-any\n",
            regular_mode,
        ),
        (dist + "RECORD", b"", regular_mode),
    ]
    with zipfile.ZipFile(path, "w") as archive:
        for name, payload, mode in reversed(members) if reverse else members:
            info = zipfile.ZipInfo(name, timestamp)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = mode << 16
            archive.writestr(info, payload)


def test_provider_build_backend_embeds_repeatable_cyclonedx(tmp_path: Path) -> None:
    wheel = tmp_path / "fixture-1.0.0-py3-none-any.whl"
    _wheel(wheel, "requests>=2")
    catalog = _license_catalog(tmp_path / "licenses.json")
    build_backend.embed_wheel_sbom(wheel, license_catalog=catalog)
    digest = hashlib.sha256(wheel.read_bytes()).digest()
    build_backend.embed_wheel_sbom(wheel, license_catalog=catalog)
    assert hashlib.sha256(wheel.read_bytes()).digest() == digest
    with zipfile.ZipFile(wheel) as archive:
        sbom = json.loads(
            archive.read("fixture-1.0.0.dist-info/sboms/package.cyclonedx.json")
        )
    assert sbom["bomFormat"] == "CycloneDX"
    assert sbom["metadata"]["component"]["licenses"] == [{"expression": "MIT"}]
    assert sbom["components"][0]["licenses"] == [{"expression": "Apache-2.0"}]
    assert "file:" not in json.dumps(sbom)


def test_provider_backend_normalizes_member_order_timestamps_and_modes(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first" / "fixture-1.0.0-py3-none-any.whl"
    second = tmp_path / "second" / "fixture-1.0.0-py3-none-any.whl"
    first.parent.mkdir()
    second.parent.mkdir()
    _wheel_with_variant_zip_metadata(
        first,
        timestamp=(2025, 1, 1, 0, 0, 0),
        reverse=False,
        permissive_modes=False,
    )
    _wheel_with_variant_zip_metadata(
        second,
        timestamp=(2026, 6, 1, 12, 30, 0),
        reverse=True,
        permissive_modes=True,
    )
    catalog = _license_catalog(tmp_path / "licenses.json")

    build_backend.embed_wheel_sbom(first, license_catalog=catalog)
    build_backend.embed_wheel_sbom(second, license_catalog=catalog)

    assert first.read_bytes() == second.read_bytes()
    with zipfile.ZipFile(first) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        sbom_name = "fixture-1.0.0.dist-info/sboms/package.cyclonedx.json"
        record_name = "fixture-1.0.0.dist-info/RECORD"
        assert names[:-2] == sorted(names[:-2])
        assert names[-2:] == [sbom_name, record_name]
        assert {info.date_time for info in infos} == {build_backend._FIXED_ZIP_TIME}
        assert {info.create_system for info in infos} == {3}
        modes = {info.filename: info.external_attr >> 16 for info in infos}
        assert modes["fixture/"] == 0o40755
        assert modes["fixture-1.0.0.data/scripts/fixture-tool"] == 0o100755
        for name in set(names) - {
            "fixture/",
            "fixture-1.0.0.data/scripts/fixture-tool",
        }:
            assert modes[name] == 0o100644


@pytest.mark.parametrize(
    "reference",
    [
        "file:fixture.whl",
        "https://example.invalid/fixture.whl",
        "ssh://example.invalid/fixture",
        "git+ssh://example.invalid/fixture.git",
        "git+https://example.invalid/fixture.git",
        "hg+ssh://example.invalid/fixture",
        "svn+ssh://example.invalid/fixture",
    ],
)
def test_provider_build_backend_rejects_every_direct_reference(
    tmp_path: Path,
    reference: str,
) -> None:
    wheel = tmp_path / "fixture-1.0.0-py3-none-any.whl"
    _wheel(wheel, f"fixture @ {reference}")
    with pytest.raises(build_backend.WheelSbomError):
        build_backend.embed_wheel_sbom(
            wheel,
            license_catalog=_license_catalog(
                tmp_path / "licenses.json", {"fixture": "MIT"}
            ),
        )


def test_provider_backend_rejects_missing_license_entry(tmp_path: Path) -> None:
    wheel = tmp_path / "fixture-1.0.0-py3-none-any.whl"
    _wheel(wheel, "requests>=2")
    catalog = _license_catalog(tmp_path / "licenses.json", {"fixture": "MIT"})
    with pytest.raises(build_backend.WheelSbomError, match="does not cover"):
        build_backend.embed_wheel_sbom(wheel, license_catalog=catalog)


def test_provider_catalog_covers_every_declared_dependency_group() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    catalog = build_backend._license_catalog(
        ROOT / "langfuse_agent/dependency-license-catalog.json"
    )
    assert set(catalog) == _project_requirement_names(pyproject)


def test_langfuse_dependency_is_strictly_supported_v4_line() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project_requirement = _requirement_named(
        list(pyproject["project"]["dependencies"]), "langfuse"
    )
    requirements = [
        line.strip()
        for line in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    requirements_file_requirement = _requirement_named(requirements, "langfuse")
    lock = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
    local_packages = [
        package
        for package in lock["package"]
        if package["name"] == pyproject["project"]["name"]
    ]
    assert len(local_packages) == 1
    lock_requirement = _requirement_named(
        [
            f"{entry['name']}{entry.get('specifier', '')}"
            for entry in local_packages[0]["metadata"]["requires-dist"]
            if "marker" not in entry
        ],
        "langfuse",
    )

    for requirement in (
        project_requirement,
        requirements_file_requirement,
        lock_requirement,
    ):
        assert str(requirement.specifier) == "<5,>=4"
        assert Version("4.0.0") in requirement.specifier
        assert Version("4.99.0") in requirement.specifier
        assert Version("3.99.0") not in requirement.specifier
        assert Version("5.0.0") not in requirement.specifier


def test_provider_generated_sbom_passes_strict_license_policy(tmp_path: Path) -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    sbom = json.loads(
        build_backend._sbom(
            _project_metadata(pyproject),
            "py3-none-any",
            ROOT / "langfuse_agent/dependency-license-catalog.json",
        )
    )
    assert all(component.get("licenses") for component in sbom["components"])
    (tmp_path / "sbom.json").write_text(json.dumps(sbom), encoding="utf-8")
    contract = security_contract.load_contract(ROOT, ".security/security-contract.json")
    security_contract.check_licenses(
        tmp_path, contract, "sbom.json", "license-evidence.json"
    )
    evidence = json.loads(
        (tmp_path / "license-evidence.json").read_text(encoding="utf-8")
    )
    assert evidence["unknown"] == 0
    assert evidence["violations"] == 0
