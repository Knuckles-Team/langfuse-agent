"""Privacy contract tests for governed trace certification reads."""

from __future__ import annotations

import inspect
from unittest.mock import MagicMock

import pytest

from langfuse_agent.api_client import LangfuseApi
from langfuse_agent.tools import observability
from langfuse_agent.trace_projection import is_certification_trace_projection

_TRACE_ID = "1" * 32
_RUN_REF = "pref_run_" + "2" * 64
_TRACE_NAME = f"graph_run:{_RUN_REF}"
_TIMESTAMP = "2026-07-17T18:30:00.123Z"


def _client(response: dict) -> tuple[LangfuseApi, MagicMock]:
    client = LangfuseApi(
        public_key="public",
        secret_key="secret",
        host="https://example.invalid",
    )
    request = MagicMock(return_value=response)
    client._request = request
    return client, request


def _governed_row(**overrides: object) -> dict:
    row = {
        "id": _TRACE_ID,
        "name": _TRACE_NAME,
        "timestamp": _TIMESTAMP,
        "metadata": {
            "run_ref": _RUN_REF,
            "model_ref": "pref_model_" + "3" * 64,
            "model_class": "economy",
            "skill_ref": "pref_skill_" + "4" * 64,
            "skill_body_ref": "pref_skill_body_" + "5" * 64,
        },
    }
    row.update(overrides)
    return row


def test_certification_projection_is_closed_and_fetches_default_response() -> None:
    raw = {
        "data": [
            {
                **_governed_row(),
                "input": "must never leave the connector",
                "output": {"free_form": "must never leave the connector"},
                "userId": "must-never-leave",
            }
        ],
        "meta": {
            "page": 1,
            "limit": 10,
            "totalItems": 1,
            "totalPages": 1,
            "cursor": "free-form-cursor",
        },
        "input": "top-level-content",
    }
    client, request = _client(raw)

    result = client.trace_list(fields="core,basic,metadata")

    assert result == {
        "data": [_governed_row()],
        "meta": {"page": 1, "limit": 10, "totalItems": 1, "totalPages": 1},
    }
    assert request.call_args.kwargs["params"]["fields"] is None
    assert is_certification_trace_projection("metadata, core, basic")
    assert not is_certification_trace_projection("core,basic,metadata,metadata")
    assert not is_certification_trace_projection("core,basic,metadata,io")


def test_certification_projection_drops_invalid_and_free_form_metadata() -> None:
    row = _governed_row(
        metadata={
            "run_ref": _RUN_REF,
            "model_ref": "raw-model-name",
            "model_class": "premium",
            "skill_ref": "pref_skill_" + "G" * 64,
            "skill_body_ref": 42,
            "prompt": "free-form-content",
            "tenant": "free-form-identity",
        }
    )
    client, _ = _client({"data": [row]})

    result = client.trace_list(fields="metadata,basic,core")

    assert result == {
        "data": [
            {
                "id": _TRACE_ID,
                "name": _TRACE_NAME,
                "timestamp": _TIMESTAMP,
                "metadata": {"run_ref": _RUN_REF},
            }
        ]
    }


def test_certification_projection_filters_non_governed_trace_names() -> None:
    client, _ = _client(
        {
            "data": [
                _governed_row(),
                _governed_row(id="2" * 32, name="graph_run:free-form-name"),
                _governed_row(id="3" * 32, name=_TRACE_NAME.upper()),
                _governed_row(id="4" * 32, name=f" {_TRACE_NAME}"),
            ]
        }
    )

    result = client.trace_list(fields="core, metadata, basic")

    assert result == {"data": [_governed_row()]}


def test_ordinary_trace_list_behavior_is_unchanged() -> None:
    raw = {
        "data": [
            {
                "id": "custom-trace-id",
                "name": "ordinary trace",
                "input": "ordinary caller requested this field",
            }
        ]
    }
    client, request = _client(raw)

    result = client.trace_list(fields="core,basic,io")

    assert result is raw
    assert request.call_args.kwargs["params"]["fields"] == "core,basic,io"


@pytest.mark.asyncio
async def test_auto_ingest_receives_only_the_projected_result(monkeypatch) -> None:
    raw = {
        "data": [
            {
                **_governed_row(),
                "input": "private-input",
                "output": "private-output",
                "metadata": {
                    **_governed_row()["metadata"],
                    "free_form": "private-metadata",
                },
            }
        ]
    }
    client, _ = _client(raw)
    ingest = MagicMock()
    monkeypatch.setattr(observability, "get_client", lambda: client)
    monkeypatch.setattr(observability, "auto_ingest", ingest)

    class ToolCapture:
        function = None

        def tool(self, **_kwargs):
            def capture(function):
                self.function = function
                return function

            return capture

    mcp = ToolCapture()
    observability.register_langfuse_observability_tools(mcp)
    assert mcp.function is not None
    arguments = {
        name: None
        for name in inspect.signature(mcp.function).parameters
        if name != "action"
    }
    arguments["fields"] = "core,basic,metadata"

    result = await mcp.function(action="trace_list", **arguments)

    assert result == {"data": [_governed_row()]}
    ingest.assert_called_once_with("trace_list", result)
