"""Native epistemic-graph typed-node ingestion -- Wire-First coverage.

Exercises the real ``ingest_entities`` + record mappers (``ingest_traces`` /
``ingest_observations`` / ``ingest_sessions`` / ``ingest_scores``) against a fake
``agent_connector_sdk.ingest`` transport (no engine required). The real SDK request
builder (``agent_connector_sdk.ingest.request.build_request``) still runs, so a
malformed change set is still caught by the SDK's own contract, not re-derived here;
only the final network commit is faked. Privacy-critical: asserts that every raw
Langfuse id, free-text label, host/path, and other PII the connector's own
metadata-minimization layer is meant to strip NEVER reaches the submitted payload.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import IngestError, KnowledgeIngest
from epistemic_graph.generated.source_ingestion import SourceIngestionRequest

import langfuse_agent.kg_ingest as kg_ingest
from langfuse_agent.kg_ingest import (
    _persistence_key,
    _records,
    auto_ingest,
    ingest_entities,
    ingest_observations,
    ingest_read_result,
    ingest_scores,
    ingest_sessions,
    ingest_traces,
)


@pytest.fixture(autouse=True)
def _synthetic_persistence_key(monkeypatch):
    monkeypatch.delenv("LANGFUSE_PERSISTENCE_HMAC_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_PERSISTENCE_HMAC_MATERIALIZED", raising=False)
    monkeypatch.setenv(
        "LANGFUSE_PERSISTENCE_HMAC_KEY_REF", "env://TEST_LANGFUSE_PERSISTENCE_HMAC_KEY"
    )
    monkeypatch.setenv(
        "TEST_LANGFUSE_PERSISTENCE_HMAC_KEY",
        "synthetic-persistence-key-material-32",
    )


class _FakeTransport:
    """Records every submitted request; no epistemic-graph engine required."""

    def __init__(self) -> None:
        self.requests: list[SourceIngestionRequest] = []

    async def source_status(self, _connector: str, _stream: str) -> Any:
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request: SourceIngestionRequest) -> Any:
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, _data: bytes) -> str:
        raise AssertionError("langfuse-agent typed-node ingestion carries no media")


@pytest.fixture
def ingest() -> tuple[KnowledgeIngest, _FakeTransport]:
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


def _node_type_of(record: Any) -> str:
    return record.mapping_reference.rsplit("/", 1)[-1]


def _record_of_type(transport: _FakeTransport, node_type: str) -> Any:
    for request in transport.requests:
        for record in request.records:
            if _node_type_of(record) == node_type:
                return record
    raise AssertionError(f"no submitted record of type {node_type!r}")


def _all_records(transport: _FakeTransport) -> list[Any]:
    return [record for request in transport.requests for record in request.records]


@pytest.mark.asyncio
async def test_ingest_entities_writes_nodes_and_edges(ingest):
    service, transport = ingest
    res = await ingest_entities(
        [
            {"id": "a", "node_type": "Trace", "name": "t"},
            {"id": "b", "node_type": "Session"},
        ],
        [{"source": "a", "target": "b", "relationship": "inSession"}],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    request = transport.requests[0]
    assert {r.record_id for r in request.records}.isdisjoint({"a", "b"})
    assert all(r.record_id.startswith("langfuse:") for r in request.records)
    trace = _record_of_type(transport, "Trace")
    assert trace.payload["external_access"] == {
        "is_public": False,
        "user_emails": [],
        "group_ids": [],
        "read_roles": ["kg:read", "kg:write", "kg:admin"],
        "markings": [],
    }
    assert len(request.relationships) == 1
    assert request.relationships[0].relation_reference.endswith(
        "resources/Trace/relations/inSession"
    )


@pytest.mark.asyncio
async def test_ingest_traces_maps_trace_session_and_user(ingest):
    service, transport = ingest
    res = await ingest_traces(
        [
            {
                "id": "tr-1",
                "name": "chat",
                "sessionId": "sess-9",
                "userId": "alice",
                "totalCost": 0.02,
                "environment": "production",
            }
        ],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert "name" not in _record_of_type(transport, "Trace").payload
    assert _record_of_type(transport, "Session")
    assert all(_node_type_of(r) != "Person" for r in _all_records(transport))
    persisted = repr([r.payload for r in _all_records(transport)])
    assert "tr-1" not in persisted
    assert "sess-9" not in persisted
    assert "alice" not in persisted
    assert (
        transport.requests[0]
        .relationships[0]
        .relation_reference.endswith("relations/inSession")
    )


@pytest.mark.asyncio
async def test_ingest_traces_persists_exact_governed_opaque_name(ingest):
    service, transport = ingest
    governed_name = "graph_run:pref_run_" + "a1" * 32

    await ingest_traces(
        [{"id": "trace-governed", "name": governed_name}],
        ingest=service,
    )

    assert _record_of_type(transport, "Trace").payload["name"] == governed_name


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "unsafe_name",
    [
        "graph_run:pref_run_" + "a" * 63,
        "graph_run:pref_run_" + "a" * 65,
        "graph_run:pref_run_" + "A" * 64,
        "graph_run:pref_run_" + "g" * 64,
        " graph_run:pref_run_" + "a" * 64,
        "graph_run:pref_run_" + "a" * 64 + ":suffix",
        "provider-trace-name",
        "contact@example.test",
    ],
)
async def test_ingest_traces_drops_arbitrary_and_near_match_names(ingest, unsafe_name):
    service, transport = ingest

    await ingest_traces(
        [{"id": "trace-untrusted", "name": unsafe_name}],
        ingest=service,
    )

    trace = _record_of_type(transport, "Trace")
    assert "name" not in trace.payload
    assert unsafe_name not in repr(trace.payload)


@pytest.mark.asyncio
async def test_ingest_observations_generation_maps_model_and_links(ingest):
    service, transport = ingest
    res = await ingest_observations(
        [
            {
                "id": "obs-1",
                "type": "GENERATION",
                "name": "openai-call",
                "traceId": "tr-1",
                "parentObservationId": "obs-0",
                "model": "gpt-4o",
                "usage": {"total": 1234},
                "calculatedTotalCost": 0.01,
            },
            {
                "id": "obs-2",
                "type": "SPAN",
                "name": "retriever",
                "traceId": "tr-1",
            },
        ],
        ingest=service,
    )
    # obs-1 (Generation) + Model node + obs-2 (Observation) = 3 nodes
    assert res["nodes"] == 3
    generation = _record_of_type(transport, "Generation")
    assert "modelName" not in generation.payload
    assert generation.payload["totalTokens"] == 1234
    assert _record_of_type(transport, "Observation")
    assert _record_of_type(transport, "Model")
    assert "gpt-4o" not in repr([r.payload for r in _all_records(transport)])
    relation_refs = {
        rel.relation_reference.rsplit("/", 1)[-1]
        for rel in transport.requests[0].relationships
    }
    assert relation_refs == {"belongsToTrace", "parentObservation", "usedModel"}


@pytest.mark.asyncio
async def test_ingest_sessions_and_scores(ingest):
    service, transport = ingest
    res = await ingest_sessions(
        [{"id": "sess-9", "createdAt": "2026-07-04T00:00:00Z"}],
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 0}
    assert _record_of_type(transport, "Session")

    transport2 = _FakeTransport()
    service2 = KnowledgeIngest(transport2, loop=None)
    res2 = await ingest_scores(
        [
            {
                "id": "sc-1",
                "name": "helpfulness",
                "value": 0.9,
                "dataType": "NUMERIC",
                "traceId": "tr-1",
            }
        ],
        ingest=service2,
    )
    assert res2 == {"nodes": 1, "edges": 1}
    assert _record_of_type(transport2, "Score").payload["scoreValue"] == "0.9"
    assert (
        transport2.requests[0]
        .relationships[0]
        .relation_reference.endswith("relations/scores")
    )


@pytest.mark.asyncio
async def test_records_normalises_wrapped_and_single():
    assert _records({"data": [{"id": "a"}, {"id": "b"}]}) == [{"id": "a"}, {"id": "b"}]
    assert _records({"id": "x", "name": "n"}) == [{"id": "x", "name": "n"}]
    assert _records(None) == []


@pytest.mark.asyncio
async def test_auto_ingest_uses_typed_agent_config_opt_in(monkeypatch):
    ingested = []

    async def _fake_ingest_trace_list(rows):
        ingested.extend(rows)

    monkeypatch.setitem(
        kg_ingest._INGEST_BY_ACTION, "trace_list", _fake_ingest_trace_list
    )
    monkeypatch.setenv("LANGFUSE_KG_AUTO_INGEST", "false")

    await auto_ingest("trace_list", {"data": [{"id": "trace-1"}]})
    assert ingested == []

    monkeypatch.setenv("LANGFUSE_KG_AUTO_INGEST", "true")
    await auto_ingest("trace_list", {"data": []})
    assert ingested == []

    await auto_ingest("trace_list", {"data": [{"id": "trace-1"}]})
    assert ingested == [{"id": "trace-1"}]


@pytest.mark.asyncio
async def test_parent_mediated_read_ingestion_has_no_second_feature_gate(monkeypatch):
    ingested = []

    async def _fake_ingest_trace_list(rows):
        ingested.extend(rows)

    monkeypatch.setitem(
        kg_ingest._INGEST_BY_ACTION, "trace_list", _fake_ingest_trace_list
    )
    monkeypatch.setenv("LANGFUSE_KG_AUTO_INGEST", "false")

    await ingest_read_result("trace_list", {"data": [{"id": "trace-1"}]})

    assert ingested == [{"id": "trace-1"}]


@pytest.mark.asyncio
async def test_ingest_rejects_retired_structural_fields(ingest):
    service, _transport = ingest
    with pytest.raises(IngestError, match="node_type"):
        await ingest_entities(
            [{"id": "invalid-shape", "type": "Retired"}], ingest=service
        )


def test_persistence_key_resolves_dedicated_secret_ref(monkeypatch):
    monkeypatch.setenv(
        "TEST_LANGFUSE_PERSISTENCE_HMAC_KEY", "dedicated-key-material-at-least-32"
    )

    assert _persistence_key() == b"dedicated-key-material-at-least-32"


def test_persistence_key_accepts_only_flagged_child_material(monkeypatch):
    monkeypatch.delenv("LANGFUSE_PERSISTENCE_HMAC_KEY_REF", raising=False)
    monkeypatch.setenv(
        "LANGFUSE_PERSISTENCE_HMAC_KEY", "materialized-child-key-at-least-32"
    )

    with pytest.raises(IngestError, match="identity key is required"):
        _persistence_key()

    monkeypatch.setenv("LANGFUSE_PERSISTENCE_HMAC_MATERIALIZED", "true")
    assert _persistence_key() == b"materialized-child-key-at-least-32"


@pytest.mark.asyncio
async def test_ingest_fails_closed_without_identity_key(monkeypatch, ingest):
    service, _transport = ingest
    monkeypatch.delenv("LANGFUSE_PERSISTENCE_HMAC_KEY_REF", raising=False)
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "api-secret-must-not-be-reused")
    monkeypatch.setenv("PERSISTENCE_ID_HMAC_KEY", "plaintext-must-not-be-used")

    with pytest.raises(IngestError, match="identity key is required"):
        await ingest_traces([{"id": "trace-1"}], ingest=service)


def test_persistence_key_rejects_plaintext_configuration(monkeypatch):
    monkeypatch.setenv(
        "LANGFUSE_PERSISTENCE_HMAC_KEY_REF", "plaintext-must-not-be-used"
    )

    with pytest.raises(IngestError, match="identity key is required"):
        _persistence_key()


@pytest.mark.asyncio
async def test_persisted_payload_redacts_identity_and_machine_location(ingest):
    service, transport = ingest

    result = await ingest_traces(
        [
            {
                "id": "trace-sensitive",
                "name": "Ordinary Person Label",
                "htmlPath": "https://private-host.invalid/trace-sensitive",
                "userId": "person-sensitive",
                "environment": "Personal Sandbox Name",
                "release": "Private Release Label",
                "tags": ["Ordinary Person Label", "private-host.invalid"],
            }
        ],
        ingest=service,
    )

    assert result == {"nodes": 1, "edges": 0}
    persisted = repr([r.payload for r in _all_records(transport)])
    assert "trace-sensitive" not in persisted
    assert "Ordinary Person Label" not in persisted
    assert "https://private-host.invalid" not in persisted
    assert "private-host.invalid" not in persisted
    assert "Personal Sandbox Name" not in persisted
    assert "Private Release Label" not in persisted
    assert "person-sensitive" not in persisted


@pytest.mark.asyncio
async def test_persisted_observability_metadata_rejects_free_text_values(ingest):
    service, transport = ingest
    await ingest_observations(
        [
            {
                "id": "observation-sensitive",
                "type": "GENERATION",
                "name": "Ordinary Person Label",
                "model": "Private Model Label",
                "level": "Ordinary Person Label",
                "startTime": "Ordinary Person Label",
                "usage": {"total": 12},
            }
        ],
        ingest=service,
    )

    transport2 = _FakeTransport()
    service2 = KnowledgeIngest(transport2, loop=None)
    await ingest_scores(
        [
            {
                "id": "score-sensitive",
                "name": "Ordinary Person Label",
                "dataType": "CATEGORICAL",
                "stringValue": "Ordinary Person Label",
            }
        ],
        ingest=service2,
    )

    persisted = repr(
        [r.payload for r in _all_records(transport) + _all_records(transport2)]
    )
    assert "Ordinary Person Label" not in persisted
    assert "Private Model Label" not in persisted
    assert _record_of_type(transport, "Generation").payload["totalTokens"] == 12
    assert "scoreValue" not in _record_of_type(transport2, "Score").payload
    assert _record_of_type(transport2, "Score").payload["dataType"] == "CATEGORICAL"


@pytest.mark.asyncio
async def test_ingest_empty_is_rejected(ingest):
    service, _transport = ingest
    with pytest.raises(IngestError, match="at least one entity"):
        await ingest_entities([], ingest=service)
