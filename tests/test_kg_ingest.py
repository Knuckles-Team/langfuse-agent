"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` + record mappers (``ingest_traces`` /
``ingest_observations`` / ``ingest_sessions`` / ``ingest_scores``) with a fake engine
client (no engine required), asserting the txn add_node/commit + edge calls and the
Langfuse record → typed-node mapping. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from langfuse_agent.kg_ingest import (
    _records,
    ingest_entities,
    ingest_observations,
    ingest_scores,
    ingest_sessions,
    ingest_traces,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.committed = False
        self.graph = None

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def commit(self, txn):
        self.committed = True
        return True


class _FakeEdges:
    def __init__(self):
        self.edges = []

    def add(self, src, dst, props):
        self.edges.append((src, dst, props))


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()
        self.edges = _FakeEdges()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "type": "Trace", "name": "t"},
            {"id": "b", "type": "Session"},
        ],
        [{"source": "a", "target": "b", "type": "inSession"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "langfuse-agent"
    assert c.txn.nodes["a"]["domain"] == "langfuse"
    assert c.edges.edges == [("a", "b", {"type": "inSession"})]


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
    assert res == {"nodes": 3, "edges": 2}
    assert c.txn.nodes["langfuse:trace:tr-1"]["type"] == "Trace"
    assert c.txn.nodes["langfuse:trace:tr-1"]["externalToolId"] == "tr-1"
    assert c.txn.nodes["langfuse:session:sess-9"]["type"] == "Session"
    assert c.txn.nodes["langfuse:person:alice"]["type"] == "Person"
    assert (
        "langfuse:trace:tr-1",
        "langfuse:session:sess-9",
        {"type": "inSession"},
    ) in c.edges.edges
    assert (
        "langfuse:trace:tr-1",
        "langfuse:person:alice",
        {"type": "tracedUser"},
    ) in c.edges.edges


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
    assert c.txn.nodes["langfuse:observation:obs-1"]["type"] == "Generation"
    assert c.txn.nodes["langfuse:observation:obs-1"]["modelName"] == "gpt-4o"
    assert c.txn.nodes["langfuse:observation:obs-1"]["totalTokens"] == 1234
    assert c.txn.nodes["langfuse:observation:obs-2"]["type"] == "Observation"
    assert c.txn.nodes["langfuse:model:gpt-4o"]["type"] == "Model"
    assert (
        "langfuse:observation:obs-1",
        "langfuse:trace:tr-1",
        {"type": "belongsToTrace"},
    ) in c.edges.edges
    assert (
        "langfuse:observation:obs-1",
        "langfuse:observation:obs-0",
        {"type": "parentObservation"},
    ) in c.edges.edges
    assert (
        "langfuse:observation:obs-1",
        "langfuse:model:gpt-4o",
        {"type": "usedModel"},
    ) in c.edges.edges


def test_ingest_sessions_and_scores():
    c = _FakeClient()
    res = ingest_sessions(
        [{"id": "sess-9", "createdAt": "2026-07-04T00:00:00Z"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 0}
    assert c.txn.nodes["langfuse:session:sess-9"]["type"] == "Session"

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
    assert c2.txn.nodes["langfuse:score:sc-1"]["type"] == "Score"
    assert c2.txn.nodes["langfuse:score:sc-1"]["scoreValue"] == "0.9"
    assert (
        "langfuse:score:sc-1",
        "langfuse:trace:tr-1",
        {"type": "scores"},
    ) in c2.edges.edges


def test_records_normalises_wrapped_and_single():
    assert _records({"data": [{"id": "a"}, {"id": "b"}]}) == [{"id": "a"}, {"id": "b"}]
    assert _records({"id": "x", "name": "n"}) == [{"id": "x", "name": "n"}]
    assert _records(None) == []


def test_ingest_noops_without_engine():
    # No injected client + no reachable engine -> clean no-op.
    assert ingest_traces([{"id": "tr-1"}]) is None


def test_ingest_empty_is_noop():
    assert ingest_entities([], client=_FakeClient()) is None
    assert ingest_traces([], client=_FakeClient()) is None
    assert ingest_observations([], client=_FakeClient()) is None
    assert ingest_scores([], client=_FakeClient()) is None
