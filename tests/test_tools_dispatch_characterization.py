"""Characterization tests for the dispatch behavior of the four Langfuse MCP
tool-registration closures (management, observability, datasets, prompts).

These pin down behavior that ``tests/test_mcp_brute_force.py`` exercises for
line/branch *coverage* but does not *assert* on: which underlying client
method is called, with which (filtered) kwargs, and the unknown-action
``ValueError`` path. Written ahead of a table-driven-dispatch refactor of the
CXA-FL-LANGFUSEAGENT-01/02 lane so the refactor can be verified
behavior-preserving.
"""

from __future__ import annotations

import inspect
from unittest.mock import MagicMock, patch

import pytest

from langfuse_agent.tools import datasets, management, observability, prompts


class _ToolCapture:
    """Minimal fake FastMCP that captures the decorated tool function."""

    def __init__(self) -> None:
        self.function = None

    def tool(self, **_kwargs):
        def _capture(function):
            self.function = function
            return function

        return _capture


def _register(register_fn):
    mcp = _ToolCapture()
    register_fn(mcp)
    assert mcp.function is not None
    return mcp.function


async def _call(fn, action: str, **overrides):
    """Call the raw tool function, defaulting every non-action param to None.

    The real defaults on the function signature are ``pydantic.Field(...)``
    sentinel objects (resolved to ``None`` only by FastMCP's own calling
    convention), so a direct call must supply an explicit value for every
    parameter or the "if x is not None" guards inside the function would see
    a ``FieldInfo`` instead of ``None``.
    """
    arguments = {
        name: None for name in inspect.signature(fn).parameters if name != "action"
    }
    arguments.update(overrides)
    return await fn(action=action, **arguments)


# ---------------------------------------------------------------------------
# management.py
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_management_unknown_action_raises_value_error():
    fn = _register(management.register_langfuse_management_tools)
    mock_client = MagicMock()
    with patch("langfuse_agent.tools.management.get_client", return_value=mock_client):
        with pytest.raises(ValueError, match="Unknown action: not_a_real_action"):
            await _call(fn, "not_a_real_action")


@pytest.mark.asyncio
async def test_management_forwards_only_filtered_kwargs():
    fn = _register(management.register_langfuse_management_tools)
    mock_client = MagicMock()
    with patch("langfuse_agent.tools.management.get_client", return_value=mock_client):
        await _call(
            fn,
            "organizations_update_project_membership",
            project_id="proj-1",
            body={"role": "admin"},
            # extra, unrelated params that must NOT reach the client call
            name="should-be-dropped",
            user_id="should-be-dropped-too",
        )
    mock_client.organizations_update_project_membership.assert_called_once_with(
        project_id="proj-1", body={"role": "admin"}
    )


@pytest.mark.asyncio
async def test_management_zero_arg_action_ignores_extra_params():
    fn = _register(management.register_langfuse_management_tools)
    mock_client = MagicMock()
    with patch("langfuse_agent.tools.management.get_client", return_value=mock_client):
        await _call(fn, "health_health", name="ignored", project_id="ignored")
    mock_client.health_health.assert_called_once_with()


# ---------------------------------------------------------------------------
# observability.py
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_observability_unknown_action_raises_value_error():
    fn = _register(observability.register_langfuse_observability_tools)
    mock_client = MagicMock()
    with patch(
        "langfuse_agent.tools.observability.get_client", return_value=mock_client
    ):
        with pytest.raises(ValueError, match="Unknown action: not_a_real_action"):
            await _call(fn, "not_a_real_action")


@pytest.mark.asyncio
async def test_observability_runtime_posture_never_calls_get_client():
    fn = _register(observability.register_langfuse_observability_tools)
    with patch("langfuse_agent.tools.observability.get_client") as mock_get_client:
        mock_get_client.side_effect = AssertionError(
            "runtime_posture must not touch the Langfuse client"
        )
        result = await _call(fn, "runtime_posture")
    mock_get_client.assert_not_called()
    assert result == observability.observability_runtime_posture()


@pytest.mark.parametrize(
    "action,call_kwargs,expected_call_kwargs",
    [
        ("observations_get_many", {"trace_id": "t1"}, {"trace_id": "t1"}),
        ("scores_get_many", {"trace_id": "t1"}, {"trace_id": "t1"}),
        ("sessions_list", {"page": 1}, {"page": 1}),
        ("trace_get", {"trace_id": "t1"}, {"trace_id": "t1"}),
    ],
)
@pytest.mark.asyncio
async def test_observability_auto_ingest_called_for_each_ingestable_action(
    action, call_kwargs, expected_call_kwargs
):
    fn = _register(observability.register_langfuse_observability_tools)
    mock_client = MagicMock()
    sentinel_result = object()
    getattr(mock_client, action).return_value = sentinel_result
    with (
        patch(
            "langfuse_agent.tools.observability.get_client", return_value=mock_client
        ),
        patch("langfuse_agent.tools.observability.auto_ingest") as mock_ingest,
    ):
        result = await _call(fn, action, **call_kwargs)
    getattr(mock_client, action).assert_called_once_with(**expected_call_kwargs)
    mock_ingest.assert_called_once_with(action, sentinel_result)
    assert result is sentinel_result


@pytest.mark.asyncio
async def test_observability_non_ingest_action_does_not_call_auto_ingest():
    fn = _register(observability.register_langfuse_observability_tools)
    mock_client = MagicMock()
    with (
        patch(
            "langfuse_agent.tools.observability.get_client", return_value=mock_client
        ),
        patch("langfuse_agent.tools.observability.auto_ingest") as mock_ingest,
    ):
        await _call(fn, "metrics_get", query="q")
    mock_client.metrics_get.assert_called_once_with(query="q")
    mock_ingest.assert_not_called()


# ---------------------------------------------------------------------------
# datasets.py
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_datasets_unknown_action_raises_value_error():
    fn = _register(datasets.register_langfuse_datasets_tools)
    mock_client = MagicMock()
    with patch("langfuse_agent.tools.datasets.get_client", return_value=mock_client):
        with pytest.raises(ValueError, match="Unknown action: not_a_real_action"):
            await _call(fn, "not_a_real_action")


@pytest.mark.asyncio
async def test_datasets_forwards_only_filtered_kwargs():
    fn = _register(datasets.register_langfuse_datasets_tools)
    mock_client = MagicMock()
    with patch("langfuse_agent.tools.datasets.get_client", return_value=mock_client):
        await _call(
            fn,
            "dataset_run_items_list",
            dataset_id="ds-1",
            run_name="run-1",
            page=2,
            limit=10,
            # extra, unrelated params that must NOT reach the client call
            id="should-be-dropped",
            status="should-be-dropped-too",
        )
    mock_client.dataset_run_items_list.assert_called_once_with(
        dataset_id="ds-1", run_name="run-1", page=2, limit=10
    )


@pytest.mark.asyncio
async def test_datasets_zero_arg_action_ignores_extra_params():
    fn = _register(datasets.register_langfuse_datasets_tools)
    mock_client = MagicMock()
    with patch("langfuse_agent.tools.datasets.get_client", return_value=mock_client):
        await _call(fn, "dataset_items_create", body=None, dataset_id="ignored")
    mock_client.dataset_items_create.assert_called_once_with()


# ---------------------------------------------------------------------------
# prompts.py
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_prompts_models_unknown_action_raises_value_error():
    fn = _register(prompts.register_langfuse_prompts_models_tools)
    mock_client = MagicMock()
    with patch("langfuse_agent.tools.prompts.get_client", return_value=mock_client):
        with pytest.raises(ValueError, match="Unknown action: not_a_real_action"):
            await _call(fn, "not_a_real_action")


@pytest.mark.asyncio
async def test_prompts_models_forwards_only_filtered_kwargs():
    fn = _register(prompts.register_langfuse_prompts_models_tools)
    mock_client = MagicMock()
    with patch("langfuse_agent.tools.prompts.get_client", return_value=mock_client):
        await _call(
            fn,
            "prompts_get",
            prompt_name="p1",
            version=3,
            label="prod",
            resolve=True,
            # extra, unrelated params that must NOT reach the client call
            body="should-be-dropped",
            media_id="should-be-dropped-too",
        )
    mock_client.prompts_get.assert_called_once_with(
        prompt_name="p1", version=3, label="prod", resolve=True
    )


@pytest.mark.asyncio
async def test_prompts_models_zero_arg_style_action_uses_single_param():
    fn = _register(prompts.register_langfuse_prompts_models_tools)
    mock_client = MagicMock()
    with patch("langfuse_agent.tools.prompts.get_client", return_value=mock_client):
        await _call(fn, "media_get", media_id="m1", name="ignored")
    mock_client.media_get.assert_called_once_with(media_id="m1")
