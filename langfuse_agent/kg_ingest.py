"""Native epistemic-graph ingestion for Langfuse records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. The langfuse-agent connector natively
pushes its observability data into the ONE epistemic-graph knowledge graph as **typed OWL
nodes** (``:Trace``, ``:Observation``, ``:Generation``, ``:Session``, ``:Score``,
``:Dataset``, ``:Prompt``, ``:Model``) plus links through the required
``agent_utilities.knowledge_graph.memory.native_ingest`` authority. Node ids follow
``langfuse:<class>:<externalId>``; ``node_type`` on each entity
matches a class federated by ``langfuse_agent.ontology``.
"""

from __future__ import annotations

import hashlib
import hmac
import math
import re
from datetime import date, datetime
from typing import Any


_SOURCE = "langfuse-agent"
_DOMAIN = "langfuse"
_UNSAFE_ID_FIELDS = frozenset(
    {
        "externaltoolid",
        "observationid",
        "sessionid",
        "sourcetraceid",
        "traceid",
        "userid",
    }
)
_OBSERVABILITY_PERSISTENCE_POLICY: dict[str, tuple[str, frozenset[str]]] = {
    "trace": ("Trace", frozenset({"name", "timestamp", "latency", "totalcost"})),
    "session": ("Session", frozenset({"timestamp"})),
    "observation": (
        "Observation",
        frozenset({"observationtype", "starttime", "endtime", "level"}),
    ),
    "generation": (
        "Generation",
        frozenset(
            {
                "observationtype",
                "starttime",
                "endtime",
                "level",
                "totaltokens",
                "totalcost",
            }
        ),
    ),
    "model": ("Model", frozenset()),
    "score": (
        "Score",
        frozenset({"scorevalue", "datatype", "timestamp"}),
    ),
}
_NUMERIC_FIELDS = frozenset({"latency", "scorevalue", "totalcost", "totaltokens"})
_TIMESTAMP_FIELDS = frozenset({"endtime", "starttime", "timestamp"})
_ENUM_FIELDS = {
    "datatype": frozenset({"BOOLEAN", "CATEGORICAL", "NUMERIC"}),
    "level": frozenset({"DEBUG", "DEFAULT", "ERROR", "WARNING"}),
    "observationtype": frozenset({"EVENT", "GENERATION", "SPAN"}),
}
_ISO_TIMESTAMP_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,9})?(?:Z|[+-]\d{2}:\d{2})$"
)
_GOVERNED_TRACE_NAME_RE = re.compile(r"^graph_run:pref_run_[a-f0-9]{64}$")


def _field_name(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value or "").casefold())


def _safe_name_value(value: Any) -> str | None:
    rendered = str(value or "")
    return rendered if _GOVERNED_TRACE_NAME_RE.fullmatch(rendered) else None


def _safe_numeric_value(field: str, value: Any) -> Any | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    try:
        finite = math.isfinite(float(value))
    except (OverflowError, ValueError):
        return None
    if not finite:
        return None
    return str(value) if field == "scorevalue" else value


def _safe_timestamp_value(value: Any) -> str | None:
    if isinstance(value, datetime):
        value = value.isoformat()
    elif isinstance(value, date):
        return None
    rendered = str(value or "")
    return rendered if _ISO_TIMESTAMP_RE.fullmatch(rendered) else None


def _safe_enum_value(field: str, value: Any) -> str | None:
    allowed = _ENUM_FIELDS.get(field)
    if allowed is None:
        return None
    rendered = str(value or "").upper()
    return rendered if rendered in allowed else None


def _safe_observability_value(field: str, value: Any) -> Any | None:
    """Validate one metadata-only value before durable graph persistence."""

    if field == "name":
        return _safe_name_value(value)
    if field in _NUMERIC_FIELDS:
        return _safe_numeric_value(field, value)
    if field in _TIMESTAMP_FIELDS:
        return _safe_timestamp_value(value)
    return _safe_enum_value(field, value)


def _persistence_key(*args: object, **kwargs: object) -> object:
    """Resolve the dedicated identity-HMAC key without credential fallback.

    SDK-GAP: Always raises now; see KnowledgeGraphIngestUnavailable.
    """
    _kg_unavailable("_persistence_key")


def _opaque_id(kind: str, raw_id: str, key: bytes) -> str:
    parts = raw_id.split(":")
    namespace = parts[1] if len(parts) >= 3 and parts[0] == "langfuse" else kind
    normalized = re.sub(r"[^a-z0-9]+", "-", namespace.casefold()).strip("-")
    normalized = normalized or "entity"
    digest = hmac.new(
        key,
        raw_id.encode(),
        hashlib.sha256,
    ).hexdigest()
    return f"langfuse:{normalized}:{digest[:32]}"


def _entity_payload_fields(
    entity: dict[str, Any], allowed_fields: frozenset[str]
) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for key_name, value in entity.items():
        field = _field_name(key_name)
        if field not in allowed_fields:
            continue
        safe_value = _safe_observability_value(field, value)
        if safe_value is not None:
            payload[key_name] = safe_value
    return payload


def _entity_payload_passthrough(entity: dict[str, Any], raw_id: str) -> dict[str, Any]:
    payload = {
        key_name: value
        for key_name, value in entity.items()
        if key_name != "id" and _field_name(key_name) not in _UNSAFE_ID_FIELDS
    }
    raw_suffix = raw_id.rsplit(":", 1)[-1]
    if str(payload.get("name") or "") == raw_suffix:
        payload.pop("name", None)
    return payload


def _prepared_entity(*args: object, **kwargs: object) -> object:
    """Return ``(raw_id, sanitized clean entity)``, or ``None`` to skip this entity.

    SDK-GAP: No-op: nothing left to register/write; preserves the graceful-degradation contract.
    """
    return None


def _prepared_entities(*args: object, **kwargs: object) -> object:
    """Was: _prepared_entities.

    SDK-GAP: Always raises now; see KnowledgeGraphIngestUnavailable.
    """
    _kg_unavailable("_prepared_entities")


def _relationship_touches_person(raw_source: str, raw_target: str) -> bool:
    return any(
        marker in value.casefold()
        for value in (raw_source, raw_target)
        for marker in (":person:", ":user:")
    )


def _resolved_relationship_endpoint(
    raw_id: str, id_map: dict[str, str], key: bytes
) -> str | None:
    return id_map.get(raw_id) or (_opaque_id("Entity", raw_id, key) if raw_id else None)


def _prepared_relationship(*args: object, **kwargs: object) -> object:
    """Was: _prepared_relationship.

    SDK-GAP: No-op: nothing left to register/write; preserves the graceful-degradation contract.
    """
    return None


def _prepared_relationships(*args: object, **kwargs: object) -> object:
    """Was: _prepared_relationships.

    SDK-GAP: Always raises now; see KnowledgeGraphIngestUnavailable.
    """
    _kg_unavailable("_prepared_relationships")


def _prepare_for_persistence(*args: object, **kwargs: object) -> object:
    """Minimize metadata and replace every external identity with an HMAC.

    SDK-GAP: Always raises now; see KnowledgeGraphIngestUnavailable.
    """
    _kg_unavailable("_prepare_for_persistence")


def ingest_entities(*args: object, **kwargs: object) -> object:
    """Sanitize and write canonical nodes and relationships through native ingestion.

    SDK-GAP: Always raises now; see KnowledgeGraphIngestUnavailable.
    """
    _kg_unavailable("ingest_entities")


def ingest_documents(
    docs: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Write text records as ``:Document`` nodes (semantic-search fodder).

    Each doc: ``{"id":..., "text":..., "title"?:..., "source_uri"?:..., ...props}``.
    Documents pass through the same privacy guard before native ingestion.
    """
    prepared: list[dict[str, Any]] = []
    for doc in docs or []:
        did = doc.get("id")
        text = doc.get("text") or doc.get("content")
        if not did or not text:
            continue
        node = {k: v for k, v in doc.items() if k != "content" and v is not None}
        node["id"] = did
        node["node_type"] = "Document"
        node["text"] = text
        prepared.append(node)
    return ingest_entities(
        prepared,
        source=source,
        domain=domain,
        client=client,
        graph=graph,
    )


# --------------------------------------------------------------------------- #
# Record -> entity mappers (thin; the txn dance lives above / in the primitive)
# --------------------------------------------------------------------------- #


def _records(resp: Any) -> list[dict[str, Any]]:
    """Normalise a Langfuse API response into a list of plain record dicts."""
    if resp is None:
        return []
    data = resp
    if isinstance(resp, dict):
        # list endpoints wrap rows under "data"; single-object endpoints are the record
        data = resp.get("data", resp) if "data" in resp else resp
    if isinstance(data, dict):
        data = [data]
    out: list[dict[str, Any]] = []
    for r in data or []:
        if r is None:
            continue
        out.append(r.model_dump() if hasattr(r, "model_dump") else r)
    return out


def ingest_traces(
    traces: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Map traces to opaque, metadata-minimized ``:Trace``/``:Session`` nodes."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for tr in traces or []:
        tid = tr.get("id")
        if not tid:
            continue
        node_id = f"langfuse:trace:{tid}"
        entities.append(
            {
                "id": node_id,
                "node_type": "Trace",
                "name": tr.get("name"),
                "timestamp": tr.get("timestamp"),
                "latency": tr.get("latency"),
                "totalCost": tr.get("totalCost"),
                "externalToolId": str(tid),
            }
        )
        sid = tr.get("sessionId")
        if sid:
            entities.append(
                {
                    "id": f"langfuse:session:{sid}",
                    "node_type": "Session",
                }
            )
            relationships.append(
                {
                    "source": node_id,
                    "target": f"langfuse:session:{sid}",
                    "relationship": "inSession",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


def _usage_total(obs: dict[str, Any]) -> Any:
    usage = obs.get("usage") or {}
    if isinstance(usage, dict):
        return usage.get("total") or usage.get("totalTokens")
    return None


def _observation_node(
    obs: dict[str, Any], node_id: str, is_generation: bool
) -> dict[str, Any]:
    node = {
        "id": node_id,
        "node_type": "Generation" if is_generation else "Observation",
        "observationType": obs.get("type"),
        "startTime": obs.get("startTime"),
        "endTime": obs.get("endTime"),
        "level": obs.get("level"),
        "externalToolId": str(obs.get("id")),
    }
    if is_generation:
        node["totalTokens"] = _usage_total(obs)
        node["totalCost"] = obs.get("calculatedTotalCost") or obs.get("totalCost")
    return node


def _observation_relationships(
    obs: dict[str, Any], node_id: str, is_generation: bool
) -> list[dict[str, Any]]:
    relationships: list[dict[str, Any]] = []
    trace_id = obs.get("traceId")
    if trace_id:
        relationships.append(
            {
                "source": node_id,
                "target": f"langfuse:trace:{trace_id}",
                "relationship": "belongsToTrace",
            }
        )
    parent = obs.get("parentObservationId")
    if parent:
        relationships.append(
            {
                "source": node_id,
                "target": f"langfuse:observation:{parent}",
                "relationship": "parentObservation",
            }
        )
    model = obs.get("model")
    if is_generation and model:
        relationships.append(
            {
                "source": node_id,
                "target": f"langfuse:model:{model}",
                "relationship": "usedModel",
            }
        )
    return relationships


def _observation_model_entity(
    obs: dict[str, Any], is_generation: bool
) -> dict[str, Any] | None:
    model = obs.get("model")
    if is_generation and model:
        return {"id": f"langfuse:model:{model}", "node_type": "Model"}
    return None


def ingest_observations(
    observations: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Map observation records → ``:Observation`` / ``:Generation`` nodes (+ links).

    ``type=GENERATION`` records become ``:Generation`` (with model/token/cost fields);
    all others become ``:Observation``. Links each to its ``:Trace`` (belongsToTrace),
    parent observation (parentObservation) and, for generations, its ``:Model``.
    """
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for obs in observations or []:
        oid = obs.get("id")
        if not oid:
            continue
        node_id = f"langfuse:observation:{oid}"
        is_generation = (obs.get("type") or "").upper() == "GENERATION"
        entities.append(_observation_node(obs, node_id, is_generation))
        relationships.extend(_observation_relationships(obs, node_id, is_generation))
        model_entity = _observation_model_entity(obs, is_generation)
        if model_entity is not None:
            entities.append(model_entity)
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_sessions(
    sessions: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Map session records → ``:Session`` nodes."""
    entities: list[dict[str, Any]] = []
    for sess in sessions or []:
        sid = sess.get("id")
        if not sid:
            continue
        entities.append(
            {
                "id": f"langfuse:session:{sid}",
                "node_type": "Session",
                "timestamp": sess.get("createdAt"),
                "externalToolId": str(sid),
            }
        )
    return ingest_entities(entities, client=client, graph=graph)


def ingest_scores(
    scores: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Map score records → ``:Score`` nodes (+ ``scores`` / ``belongsToTrace`` links)."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for sc in scores or []:
        sid = sc.get("id")
        if not sid:
            continue
        node_id = f"langfuse:score:{sid}"
        entities.append(
            {
                "id": node_id,
                "node_type": "Score",
                "scoreValue": sc.get("value"),
                "dataType": sc.get("dataType"),
                "timestamp": sc.get("timestamp"),
                "externalToolId": str(sid),
            }
        )
        tid = sc.get("traceId")
        if tid:
            relationships.append(
                {
                    "source": node_id,
                    "target": f"langfuse:trace:{tid}",
                    "relationship": "scores",
                }
            )
        oid = sc.get("observationId")
        if oid:
            relationships.append(
                {
                    "source": node_id,
                    "target": f"langfuse:observation:{oid}",
                    "relationship": "scores",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


# Dispatch used by the observability tool to auto-ingest read results.
_INGEST_BY_ACTION = {
    "trace_list": ingest_traces,
    "trace_get": ingest_traces,
    "observations_get_many": ingest_observations,
    "sessions_list": ingest_sessions,
    "scores_get_many": ingest_scores,
}


def auto_ingest(*args: object, **kwargs: object) -> object:
    """Opt-in standalone ingestion of a read result.

    SDK-GAP: No-op: nothing left to register/write; preserves the graceful-degradation contract.
    """
    return None


def ingest_read_result(action: str, result: Any) -> None:
    """Ingest one supported API read under the caller's existing authority.

    This function never synthesizes identity and has no configuration bypass.
    The native ingestion boundary still requires a verified ambient
    ``GraphSession`` and surfaces every write failure to its caller.
    """

    fn = _INGEST_BY_ACTION.get(action)
    if fn is None:
        return
    records = _records(result)
    if not records:
        return
    fn(records)


class KnowledgeGraphIngestUnavailable(RuntimeError):
    """Direct-to-graph ingestion is unavailable from this connector.

    SDK-GAP (EH-48x, /var/tmp/l9/finish/au-decon-G4c/SDK-GAPS.md): raised in
    place of the old ``agent_utilities.knowledge_graph`` native-ingest call --
    agent-connector-sdk has no facade over EG's typed ingestion protocol yet,
    and the fleet precedent (agents/world-reference-mcp) moves direct-to-graph
    delivery to agent_connector_sdk.runner/sinks at the deployment layer, out
    of connector scope.
    """


def _kg_unavailable(name: str) -> None:
    raise KnowledgeGraphIngestUnavailable(
        f"{name}: direct-to-graph ingestion moved out of connector code "
        "(agent-utilities removed); no agent-connector-sdk facade exists yet "
        "-- see SDK-GAPS.md"
    )
