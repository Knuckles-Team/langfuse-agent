"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` + record mappers (``ingest_traces`` /
``ingest_observations`` / ``ingest_sessions`` / ``ingest_scores``) with a
ChangeEnvelope-capable fake client (no engine required), asserting the governed commit
and Langfuse record → typed-node mapping. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from typing import Any

import msgpack
import pytest
from agent_utilities.knowledge_graph.core.session import GraphSession, use_session
from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError
from agent_utilities.models.company_brain import ActorType
from agent_utilities.security.brain_context import ActorContext

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
    monkeypatch.setattr(
        kg_ingest.config,
        "langfuse_persistence_hmac_key_ref",
        "env://TEST_LANGFUSE_PERSISTENCE_HMAC_KEY",
    )
    monkeypatch.setenv(
        "TEST_LANGFUSE_PERSISTENCE_HMAC_KEY",
        "synthetic-persistence-key-material-32",
    )


@pytest.fixture(autouse=True)
def _verified_graph_session():
    actor = ActorContext(
        actor_id="subject:opaque:synthetic",
        actor_type=ActorType.SYSTEM,
        roles=(),
        tenant_id="tenant:opaque:synthetic",
        authenticated=True,
    )
    session = GraphSession(
        actor=actor,
        tenant=actor.tenant_id,
        scopes=frozenset({"kg:write"}),
        graph="__commons__",
        audience="epistemic-graph",
        policy_version="policy:synthetic",
    )
    with use_session(session):
        yield


def _node_of_type(client, entity_type):
    return next(
        node
        for node in client.nodes.values.values()
        if node["node_type"] == entity_type
    )


class _FakeNodes:
    def __init__(self) -> None:
        self.values: dict[str, dict[str, Any]] = {}

    def properties(self, node_id: str) -> dict[str, Any] | None:
        return self.values.get(node_id)

    def list(self) -> list[tuple[str, dict[str, Any]]]:
        return list(self.values.items())


class _FakeChanges:
    def __init__(self, nodes: _FakeNodes) -> None:
        self.nodes = nodes
        self.edges: list[tuple[str, str, dict[str, Any]]] = []
        self.applied: list[dict[str, Any]] = []
        self.records: dict[str, dict[str, Any]] = {}
        self.versions: dict[str, dict[str, Any]] = {}

    def get(self, envelope_id: str) -> dict[str, Any] | None:
        return self.records.get(envelope_id)

    def content_version(self, object_id: str) -> dict[str, Any] | None:
        return self.versions.get(object_id)

    def cursor(self, _source: str, _partition: str = "") -> None:
        return None

    def apply(self, envelope: dict[str, Any]) -> dict[str, Any]:
        self.applied.append(envelope)
        mutation = envelope["mutation"]
        for operation in mutation["operations"]:
            method = operation["method"]
            params = method["params"]
            properties = msgpack.unpackb(params["properties_msgpack"], raw=False)
            if method["method"] == "AddNode":
                self.nodes.values[params["node_id"]] = properties
            elif method["method"] == "AddEdge":
                self.edges.append(
                    (params["source_id"], params["target_id"], properties)
                )
        version = envelope["content_version"]
        self.versions[version["object_id"]] = version
        self.records[envelope["envelope_id"]] = envelope
        return {
            "batch_id": mutation["batch_id"],
            "replayed": False,
            "projection_pending": False,
        }


class _FakeRdf:
    def validate_shacl(self, _shapes: str, _data_graph: str) -> dict[str, Any]:
        return {"conforms": True, "results": []}


class _FakeClient:
    def __init__(self) -> None:
        self.nodes = _FakeNodes()
        self.changes = _FakeChanges(self.nodes)
        self.rdf = _FakeRdf()

    @staticmethod
    def supports(operation: str) -> bool:
        return operation == "ApplyChangeEnvelope"


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "Trace", "name": "t"},
            {"id": "b", "node_type": "Session"},
        ],
        [{"source": "a", "target": "b", "relationship": "inSession"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert len(c.changes.applied) == 1
    assert set(c.nodes.values).isdisjoint({"a", "b"})
    assert all(node_id.startswith("langfuse:") for node_id in c.nodes.values)
    # provenance is stamped
    trace = _node_of_type(c, "Trace")
    assert trace["source"] == "langfuse-agent"
    assert trace["domain"] == "langfuse"
    assert trace["external_access"] == {
        "is_public": False,
        "user_emails": [],
        "group_ids": [],
        "read_roles": ["kg:read", "kg:write", "kg:admin"],
        "markings": [],
    }
    assert len(c.changes.edges) == 1
    assert c.changes.edges[0][2] == {"relationship": "inSession"}


def test_ingest_traces_maps_trace_session_and_user():
    c = _FakeClient()
    res = ingest_traces(
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
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert "name" not in _node_of_type(c, "Trace")
    assert _node_of_type(c, "Session")["node_type"] == "Session"
    assert all(node["node_type"] != "Person" for node in c.nodes.values.values())
    persisted = repr({"nodes": c.nodes.values, "edges": c.changes.edges})
    assert "tr-1" not in persisted
    assert "sess-9" not in persisted
    assert "alice" not in persisted
    assert c.changes.edges[0][2] == {"relationship": "inSession"}


def test_ingest_traces_persists_exact_governed_opaque_name():
    client = _FakeClient()
    governed_name = "graph_run:pref_run_" + "a1" * 32

    ingest_traces(
        [{"id": "trace-governed", "name": governed_name}],
        client=client,
    )

    assert _node_of_type(client, "Trace")["name"] == governed_name


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
def test_ingest_traces_drops_arbitrary_and_near_match_names(unsafe_name):
    client = _FakeClient()

    ingest_traces(
        [{"id": "trace-untrusted", "name": unsafe_name}],
        client=client,
    )

    trace = _node_of_type(client, "Trace")
    assert "name" not in trace
    assert unsafe_name not in repr(client.nodes.values)


def test_ingest_observations_generation_maps_model_and_links():
    c = _FakeClient()
    res = ingest_observations(
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
        client=c,
        graph="__commons__",
    )
    # obs-1 (Generation) + Model node + obs-2 (Observation) = 3 nodes
    assert res["nodes"] == 3
    generation = _node_of_type(c, "Generation")
    assert "modelName" not in generation
    assert generation["totalTokens"] == 1234
    assert _node_of_type(c, "Observation")["node_type"] == "Observation"
    assert _node_of_type(c, "Model")["node_type"] == "Model"
    assert "gpt-4o" not in repr(c.nodes.values)
    assert {edge[2]["relationship"] for edge in c.changes.edges} == {
        "belongsToTrace",
        "parentObservation",
        "usedModel",
    }


def test_ingest_sessions_and_scores():
    c = _FakeClient()
    res = ingest_sessions(
        [{"id": "sess-9", "createdAt": "2026-07-04T00:00:00Z"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 0}
    assert _node_of_type(c, "Session")["node_type"] == "Session"

    c2 = _FakeClient()
    res2 = ingest_scores(
        [
            {
                "id": "sc-1",
                "name": "helpfulness",
                "value": 0.9,
                "dataType": "NUMERIC",
                "traceId": "tr-1",
            }
        ],
        client=c2,
        graph="__commons__",
    )
    assert res2 == {"nodes": 1, "edges": 1}
    assert _node_of_type(c2, "Score")["scoreValue"] == "0.9"
    assert c2.changes.edges[0][2] == {"relationship": "scores"}


def test_records_normalises_wrapped_and_single():
    assert _records({"data": [{"id": "a"}, {"id": "b"}]}) == [{"id": "a"}, {"id": "b"}]
    assert _records({"id": "x", "name": "n"}) == [{"id": "x", "name": "n"}]
    assert _records(None) == []


def test_auto_ingest_uses_typed_agent_config_opt_in(monkeypatch):
    ingested = []
    monkeypatch.setitem(
        kg_ingest._INGEST_BY_ACTION,
        "trace_list",
        lambda rows: ingested.extend(rows),
    )
    monkeypatch.setattr(kg_ingest.config, "langfuse_kg_auto_ingest", False)

    auto_ingest("trace_list", {"data": [{"id": "trace-1"}]})
    assert ingested == []

    monkeypatch.setattr(kg_ingest.config, "langfuse_kg_auto_ingest", True)
    auto_ingest("trace_list", {"data": []})
    assert ingested == []

    auto_ingest("trace_list", {"data": [{"id": "trace-1"}]})
    assert ingested == [{"id": "trace-1"}]


def test_parent_mediated_read_ingestion_has_no_second_feature_gate(monkeypatch):
    ingested = []
    monkeypatch.setitem(
        kg_ingest._INGEST_BY_ACTION,
        "trace_list",
        lambda rows: ingested.extend(rows),
    )
    monkeypatch.setattr(kg_ingest.config, "langfuse_kg_auto_ingest", False)

    ingest_read_result("trace_list", {"data": [{"id": "trace-1"}]})

    assert ingested == [{"id": "trace-1"}]


def test_ingest_rejects_retired_structural_fields():
    with pytest.raises(NativeIngestError, match="canonical node_type"):
        ingest_entities(
            [{"id": "invalid-shape", "type": "Retired"}], client=_FakeClient()
        )


def test_persistence_key_resolves_dedicated_secret_ref(monkeypatch):
    monkeypatch.setenv(
        "TEST_LANGFUSE_PERSISTENCE_HMAC_KEY", "dedicated-key-material-at-least-32"
    )

    assert _persistence_key() == b"dedicated-key-material-at-least-32"


def test_persistence_key_accepts_only_flagged_child_material(monkeypatch):
    monkeypatch.setattr(kg_ingest.config, "langfuse_persistence_hmac_key_ref", None)
    monkeypatch.setenv(
        "LANGFUSE_PERSISTENCE_HMAC_KEY", "materialized-child-key-at-least-32"
    )

    with pytest.raises(NativeIngestError, match="identity key is required"):
        _persistence_key()

    monkeypatch.setenv("LANGFUSE_PERSISTENCE_HMAC_MATERIALIZED", "true")
    assert _persistence_key() == b"materialized-child-key-at-least-32"


def test_ingest_fails_closed_without_identity_key(monkeypatch):
    monkeypatch.setattr(kg_ingest.config, "langfuse_persistence_hmac_key_ref", None)
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "api-secret-must-not-be-reused")
    monkeypatch.setenv("PERSISTENCE_ID_HMAC_KEY", "plaintext-must-not-be-used")

    with pytest.raises(NativeIngestError, match="identity key is required"):
        ingest_traces([{"id": "trace-1"}], client=_FakeClient())


def test_persistence_key_rejects_plaintext_configuration(monkeypatch):
    monkeypatch.setattr(
        kg_ingest.config,
        "langfuse_persistence_hmac_key_ref",
        "plaintext-must-not-be-used",
    )

    with pytest.raises(NativeIngestError, match="identity key is required"):
        _persistence_key()


def test_persisted_payload_redacts_identity_and_machine_location():
    client = _FakeClient()

    result = ingest_traces(
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
        client=client,
    )

    assert result == {"nodes": 1, "edges": 0}
    persisted = repr(client.nodes.values)
    assert "trace-sensitive" not in persisted
    assert "Ordinary Person Label" not in persisted
    assert "https://private-host.invalid" not in persisted
    assert "private-host.invalid" not in persisted
    assert "Personal Sandbox Name" not in persisted
    assert "Private Release Label" not in persisted
    assert "person-sensitive" not in persisted


def test_persisted_observability_metadata_rejects_free_text_values():
    observations = _FakeClient()
    ingest_observations(
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
        client=observations,
    )

    scores = _FakeClient()
    ingest_scores(
        [
            {
                "id": "score-sensitive",
                "name": "Ordinary Person Label",
                "dataType": "CATEGORICAL",
                "stringValue": "Ordinary Person Label",
            }
        ],
        client=scores,
    )

    persisted = repr(
        {"observations": observations.nodes.values, "scores": scores.nodes.values}
    )
    assert "Ordinary Person Label" not in persisted
    assert "Private Model Label" not in persisted
    assert _node_of_type(observations, "Generation")["totalTokens"] == 12
    assert "scoreValue" not in _node_of_type(scores, "Score")
    assert _node_of_type(scores, "Score")["dataType"] == "CATEGORICAL"


def test_ingest_empty_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([], client=_FakeClient())
