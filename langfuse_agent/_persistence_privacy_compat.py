"""Local port of ``agent_utilities.security.persistence_privacy`` primitives.

SDK-GAP (EH-48x, SDK-GAPS.md #5): agent_connector_sdk has no equivalent of
agent_utilities.security.persistence_privacy (a deep sanitizer for data
entering durable/external observability stores). This is a compact,
deliberately simpler local replacement -- a recursive walk that redacts
string values under sensitive-looking keys (via agent_connector_sdk's own
``is_sensitive_name`` heuristic, already used for HTTP header/query
redaction) -- not the original's full deny-term/entropy-based detection.
See SDK-GAPS.md for the proposal to port the original into the SDK.
"""

from __future__ import annotations

import hashlib
import hmac
import re
from dataclasses import dataclass
from typing import Any

from agent_connector_sdk.config import setting
from agent_connector_sdk.http.redaction import REDACTED, is_sensitive_name

__all__ = [
    "PersistencePrivacyGuard",
    "PrivacyReport",
    "persistence_reference",
    "sanitize_for_persistence",
]

_REFERENCE_RE = re.compile(r"^pref_[a-z0-9_]+_[0-9a-f]{64}$")


def _persistence_identity_key() -> bytes | None:
    """Optional HMAC key for :func:`persistence_reference` (env-only; no secret store).

    SDK-GAP: the original also resolved an OpenBao-backed secret reference and
    refused a keyless HMAC in a production profile; neither is ported here --
    see SDK-GAPS.md #5. Falls back to plain SHA-256 (still non-reversible,
    just not keyed) when no key is configured.
    """
    configured = str(setting("GRAPH_SERVICE_AUTH_SECRET", "") or "").strip()
    return configured.encode("utf-8") if configured else None


def persistence_reference(kind: str, value: Any, *, namespace: str = "") -> str:
    """Return a stable non-reversible reference for a durable identity field."""
    text = str(value or "")
    if not text:
        return ""
    if _REFERENCE_RE.fullmatch(text):
        return text
    label = re.sub(r"[^a-z0-9_]+", "_", str(kind).lower()).strip("_") or "value"
    framed = b"\x00".join(
        (
            b"agent-connector-sdk:persistence-reference:v1",
            label.encode("utf-8"),
            str(namespace or "").encode("utf-8"),
            text.encode("utf-8"),
        )
    )
    key = _persistence_identity_key()
    digest = (
        hmac.new(key, framed, hashlib.sha256).hexdigest()
        if key is not None
        else hashlib.sha256(framed).hexdigest()
    )
    return f"pref_{label}_{digest}"


@dataclass(frozen=True)
class PrivacyReport:
    """Non-sensitive summary of a sanitization pass."""

    redactions: int
    detected_types: tuple[str, ...]

    @property
    def changed(self) -> bool:
        return self.redactions > 0

    def as_dict(self) -> dict[str, Any]:
        return {
            "redactions": self.redactions,
            "detected_types": list(self.detected_types),
        }


class PersistencePrivacyGuard:
    """Recursive sanitizer: redacts string values under sensitive-looking keys."""

    def __init__(
        self, *, deny_terms: tuple[str, ...] | list[str] | None = None
    ) -> None:
        # SDK-GAP: deny_terms (identity-term denylist matching) not ported.
        self._deny_terms = tuple(deny_terms or ())

    def sanitize(self, value: Any) -> tuple[Any, PrivacyReport]:
        counts = {"key_redaction": 0}
        clean = self._walk(value, counts, parent_key=None)
        detected = tuple(k for k, n in counts.items() if n)
        return clean, PrivacyReport(
            redactions=sum(counts.values()), detected_types=detected
        )

    def _walk(self, value: Any, counts: dict[str, int], parent_key: str | None) -> Any:
        if isinstance(value, dict):
            return {k: self._walk(v, counts, k) for k, v in value.items()}
        if isinstance(value, list):
            return [self._walk(v, counts, parent_key) for v in value]
        if isinstance(value, tuple):
            return tuple(self._walk(v, counts, parent_key) for v in value)
        if isinstance(value, str) and parent_key and is_sensitive_name(parent_key):
            counts["key_redaction"] += 1
            return REDACTED
        return value


def sanitize_for_persistence(
    value: Any, *, deny_terms: tuple[str, ...] | list[str] | None = None
) -> tuple[Any, PrivacyReport]:
    """Sanitize ``value`` and return only a count/type report alongside it."""
    return PersistencePrivacyGuard(deny_terms=deny_terms).sanitize(value)
