"""Native epistemic-graph ingestion for Langfuse records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. The langfuse-agent connector natively
pushes its observability data into the ONE epistemic-graph knowledge graph as **typed OWL
nodes** (``:Trace``, ``:Observation``, ``:Generation``, ``:Session``, ``:Score``,
``:Dataset``, ``:Prompt``, ``:Model``) plus links, using the lightweight engine client
(``GraphComputeEngine()._client`` + ``txn``) — the same fast client the blob ``MediaStore``
uses, NOT the heavy in-process ingestion engine.

Thin mapper over the shared primitive
``agent_utilities.knowledge_graph.memory.native_ingest``: when that primitive is importable
it is used for the txn write path; otherwise a self-contained txn fallback is used. Either
way everything is dependency-/engine-guarded — with no KG stack or no reachable engine every
entry point **no-ops** (returns ``None``), so the connector keeps working with zero KG
infrastructure. Node ids follow ``langfuse:<class>:<externalId>``; ``type`` on each entity
matches a class federated by ``langfuse_agent.ontology``.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("langfuse_agent.kg")

_SOURCE = "langfuse-agent"
_DOMAIN = "langfuse"
_DEFAULT_GRAPH = "__commons__"

# Prefer the shared fleet primitive for the txn write path; fall back to a
# self-contained implementation when agent_utilities does not yet ship it.
try:  # pragma: no cover - import wiring
    from agent_utilities.knowledge_graph.memory.native_ingest import (
        ingest_entities as _shared_ingest_entities,
    )
except Exception:  # noqa: BLE001 — primitive absent in installed agent_utilities
    _shared_ingest_entities = None


def _client() -> tuple[Any | None, str]:
    """Return ``(engine_client, graph_name)`` or ``(None, "")`` when unavailable."""
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG ingest unavailable (import): %s", e)
        return None, ""
    try:
        engine = GraphComputeEngine()
        client = getattr(engine, "_client", None)
        if client is None:
            return None, ""
        graph = getattr(engine, "graph_name", None) or _DEFAULT_GRAPH
        return client, graph
    except Exception as e:  # noqa: BLE001 — engine unreachable
        logger.debug("KG ingest: engine unreachable: %s", e)
        return None, ""


def _write_local(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None,
    *,
    client: Any,
    graph: str,
) -> dict[str, int] | None:
    """Self-contained txn write path (used when the shared primitive is absent)."""
    try:
        txn = client.txn.begin(graph=graph)
        for ent in entities:
            props = {k: v for k, v in ent.items() if k != "id" and v is not None}
            props.setdefault("source", _SOURCE)
            props.setdefault("domain", _DOMAIN)
            client.txn.add_node(txn, ent["id"], props)
        committed = client.txn.commit(txn)
    except Exception as e:  # noqa: BLE001 — engine/txn failure is non-fatal
        logger.warning("KG ingest: txn failed: %s", e)
        return None
    if not committed:
        logger.warning("KG ingest: txn not committed (conflict)")
        return None

    edges = 0
    for rel in relationships or []:
        try:
            client.edges.add(
                rel["source"], rel["target"], {"type": rel.get("type", "RELATED")}
            )
            edges += 1
        except Exception as e:  # noqa: BLE001 — pure edge link, best-effort
            logger.debug("KG ingest: edge skipped: %s", e)

    logger.info("KG ingest: wrote %d nodes, %d edges", len(entities), edges)
    return {"nodes": len(entities), "edges": edges}


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write typed OWL nodes (+ edges) into epistemic-graph.

    ``entities``: ``[{"id":..., "type":<owl:Class>, ...props}]``.
    ``relationships``: ``[{"source":id, "target":id, "type":rel}]``.
    Returns ``{"nodes":n, "edges":m}`` or ``None`` (no engine / failure; never raises).
    ``client``/``graph`` may be injected (tests); otherwise resolved on demand.
    """
    entities = [e for e in (entities or []) if e.get("id")]
    if not entities:
        return None
    # Injected client -> always use the local write path (deterministic for tests).
    if client is not None:
        return _write_local(
            entities, relationships, client=client, graph=graph or _DEFAULT_GRAPH
        )
    # Delegate to the shared fleet primitive when it is available.
    if _shared_ingest_entities is not None:
        return _shared_ingest_entities(
            entities, relationships, source=source, domain=domain, graph=graph
        )
    client, resolved = _client()
    if client is None:
        return None
    return _write_local(entities, relationships, client=client, graph=graph or resolved)


def ingest_documents(
    docs: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write text records as ``:Document`` nodes (semantic-search fodder).

    Each doc: ``{"id":..., "text":..., "title"?:..., "source_uri"?:..., ...props}``.
    Delegates to the shared primitive when available; otherwise writes ``:Document``
    nodes via the local txn path. Returns ``{"nodes":n, "edges":0}`` or ``None``.
    """
    prepared: list[dict[str, Any]] = []
    for doc in docs or []:
        did = doc.get("id")
        text = doc.get("text") or doc.get("content")
        if not did or not text:
            continue
        node = {k: v for k, v in doc.items() if k != "content" and v is not None}
        node["id"] = did
        node["type"] = "Document"
        node["text"] = text
        prepared.append(node)
    if not prepared:
        return None
    if client is None and _shared_ingest_entities is not None:
        try:
            from agent_utilities.knowledge_graph.memory.native_ingest import (
                ingest_documents as _shared_ingest_documents,
            )

            return _shared_ingest_documents(
                docs, source=source, domain=domain, graph=graph
            )
        except Exception as e:  # noqa: BLE001 — fall through to local path
            logger.debug("KG ingest: shared ingest_documents unavailable: %s", e)
    if client is None:
        client, resolved = _client()
        graph = graph or resolved
    if client is None:
        return None
    return _write_local(prepared, None, client=client, graph=graph or _DEFAULT_GRAPH)


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
) -> dict[str, int] | None:
    """Map Langfuse trace records → ``:Trace`` (+ ``:Session`` / ``:Person``) nodes."""
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
                "type": "Trace",
                "name": tr.get("name"),
                "timestamp": tr.get("timestamp"),
                "latency": tr.get("latency"),
                "totalCost": tr.get("totalCost"),
                "release": tr.get("release"),
                "version": tr.get("version"),
                "environment": tr.get("environment"),
                "tags": tr.get("tags"),
                "webUrl": tr.get("htmlPath") or tr.get("webUrl"),
                "externalToolId": str(tid),
            }
        )
        sid = tr.get("sessionId")
        if sid:
            entities.append(
                {"id": f"langfuse:session:{sid}", "type": "Session", "name": sid}
            )
            relationships.append(
                {
                    "source": node_id,
                    "target": f"langfuse:session:{sid}",
                    "type": "inSession",
                }
            )
        uid = tr.get("userId")
        if uid:
            entities.append(
                {"id": f"langfuse:person:{uid}", "type": "Person", "name": uid}
            )
            relationships.append(
                {
                    "source": node_id,
                    "target": f"langfuse:person:{uid}",
                    "type": "tracedUser",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


def _usage_total(obs: dict[str, Any]) -> Any:
    usage = obs.get("usage") or {}
    if isinstance(usage, dict):
        return usage.get("total") or usage.get("totalTokens")
    return None


def ingest_observations(
    observations: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
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
        otype = (obs.get("type") or "").upper()
        is_gen = otype == "GENERATION"
        node = {
            "id": node_id,
            "type": "Generation" if is_gen else "Observation",
            "name": obs.get("name"),
            "observationType": obs.get("type"),
            "startTime": obs.get("startTime"),
            "endTime": obs.get("endTime"),
            "level": obs.get("level"),
            "externalToolId": str(oid),
        }
        if is_gen:
            node["modelName"] = obs.get("model")
            node["totalTokens"] = _usage_total(obs)
            node["totalCost"] = obs.get("calculatedTotalCost") or obs.get("totalCost")
        entities.append(node)

        tid = obs.get("traceId")
        if tid:
            relationships.append(
                {
                    "source": node_id,
                    "target": f"langfuse:trace:{tid}",
                    "type": "belongsToTrace",
                }
            )
        parent = obs.get("parentObservationId")
        if parent:
            relationships.append(
                {
                    "source": node_id,
                    "target": f"langfuse:observation:{parent}",
                    "type": "parentObservation",
                }
            )
        model = obs.get("model")
        if is_gen and model:
            entities.append(
                {"id": f"langfuse:model:{model}", "type": "Model", "modelName": model}
            )
            relationships.append(
                {
                    "source": node_id,
                    "target": f"langfuse:model:{model}",
                    "type": "usedModel",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_sessions(
    sessions: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map session records → ``:Session`` nodes."""
    entities: list[dict[str, Any]] = []
    for sess in sessions or []:
        sid = sess.get("id")
        if not sid:
            continue
        entities.append(
            {
                "id": f"langfuse:session:{sid}",
                "type": "Session",
                "name": sid,
                "timestamp": sess.get("createdAt"),
                "environment": sess.get("environment"),
                "externalToolId": str(sid),
            }
        )
    return ingest_entities(entities, client=client, graph=graph)


def ingest_scores(
    scores: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
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
                "type": "Score",
                "name": sc.get("name"),
                "scoreValue": str(sc.get("value"))
                if sc.get("value") is not None
                else sc.get("stringValue"),
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
                    "type": "scores",
                }
            )
        oid = sc.get("observationId")
        if oid:
            relationships.append(
                {
                    "source": node_id,
                    "target": f"langfuse:observation:{oid}",
                    "type": "scores",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


# Dispatch used by the observability tool to auto-ingest read results (best-effort).
_INGEST_BY_ACTION = {
    "trace_list": ingest_traces,
    "trace_get": ingest_traces,
    "observations_get_many": ingest_observations,
    "legacy_observations_v1_get_many": ingest_observations,
    "sessions_list": ingest_sessions,
    "scores_get_many": ingest_scores,
}


def auto_ingest(action: str, result: Any) -> None:
    """Best-effort default-on ingestion of a read action's result. Never raises."""
    fn = _INGEST_BY_ACTION.get(action)
    if fn is None:
        return
    try:
        fn(_records(result))
    except Exception as e:  # noqa: BLE001 — ingestion must never break the tool
        logger.debug("KG auto-ingest skipped for %s: %s", action, e)
