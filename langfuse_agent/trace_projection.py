"""Closed, metadata-only projection for governed GraphOS trace discovery."""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

CERTIFICATION_TRACE_FIELDS = frozenset({"basic", "core", "metadata"})

_TRACE_ID_RE = re.compile(r"[a-f0-9]{32}", re.ASCII)
_TRACE_NAME_RE = re.compile(r"graph_run:pref_run_[a-f0-9]{64}", re.ASCII)
_TIMESTAMP_RE = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,9})?(?:Z|[+-]\d{2}:\d{2})",
    re.ASCII,
)
_METADATA_PATTERNS = {
    "run_ref": re.compile(r"pref_run_[a-f0-9]{64}", re.ASCII),
    "model_ref": re.compile(r"pref_model_[a-f0-9]{64}", re.ASCII),
    "model_class": re.compile(r"(?:economy|standard)", re.ASCII),
    "skill_ref": re.compile(r"pref_skill_[a-f0-9]{64}", re.ASCII),
    "skill_body_ref": re.compile(r"pref_skill_body_[a-f0-9]{64}", re.ASCII),
}
_PAGINATION_FIELDS = frozenset({"limit", "page", "totalItems", "totalPages"})


def is_certification_trace_projection(fields: Any) -> bool:
    """Return whether ``fields`` is exactly the closed certification field set."""

    if not isinstance(fields, str):
        return False
    parts = tuple(part.strip() for part in fields.split(","))
    return (
        len(parts) == len(CERTIFICATION_TRACE_FIELDS)
        and len(set(parts)) == len(parts)
        and frozenset(parts) == CERTIFICATION_TRACE_FIELDS
    )


def _project_metadata(value: Any) -> dict[str, str]:
    if not isinstance(value, Mapping):
        return {}
    projected: dict[str, str] = {}
    for key, pattern in _METADATA_PATTERNS.items():
        candidate = value.get(key)
        if isinstance(candidate, str) and pattern.fullmatch(candidate):
            projected[key] = candidate
    return projected


def _project_row(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, Mapping):
        return None
    trace_id = value.get("id")
    name = value.get("name")
    timestamp = value.get("timestamp")
    if not (
        isinstance(trace_id, str)
        and _TRACE_ID_RE.fullmatch(trace_id)
        and isinstance(name, str)
        and _TRACE_NAME_RE.fullmatch(name)
        and isinstance(timestamp, str)
        and _TIMESTAMP_RE.fullmatch(timestamp)
    ):
        return None
    return {
        "id": trace_id,
        "name": name,
        "timestamp": timestamp,
        "metadata": _project_metadata(value.get("metadata")),
    }


def project_certification_trace_list(result: Any) -> dict[str, Any]:
    """Drop every field outside the governed trace certification contract."""

    if not isinstance(result, Mapping):
        return {"data": []}
    rows = result.get("data")
    projected_rows = []
    if isinstance(rows, list):
        projected_rows = [
            projected_row
            for row in rows
            if (projected_row := _project_row(row)) is not None
        ]

    response: dict[str, Any] = {"data": projected_rows}
    meta = result.get("meta")
    if isinstance(meta, Mapping):
        safe_meta = {
            key: value
            for key, value in meta.items()
            if key in _PAGINATION_FIELDS
            and isinstance(value, int)
            and not isinstance(value, bool)
            and value >= 0
        }
        if safe_meta:
            response["meta"] = safe_meta
    return response
