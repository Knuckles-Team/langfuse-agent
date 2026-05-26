"""Pytest configuration and fixtures for langfuse-agent tests.

CONCEPT:LA_1.0 — Langfuse MCP Integration
"""

import os
import sys
from unittest.mock import MagicMock, patch

# Mock agent_utilities.mcp.delegated_auth module before any tests import it
mock_delegated_auth = MagicMock()
mock_delegated_auth.is_delegation_enabled.return_value = False
mock_delegated_auth.get_user_identity.return_value = {}
sys.modules["agent_utilities.mcp.delegated_auth"] = mock_delegated_auth

# Mock tree_sitter_javascript which is a dynamic dependency of agent_utilities
sys.modules["tree_sitter_javascript"] = MagicMock()
sys.modules["tree_sitter_python"] = MagicMock()
sys.modules["tree_sitter_typescript"] = MagicMock()
sys.modules["tree_sitter_go"] = MagicMock()
sys.modules["tree_sitter_rust"] = MagicMock()
sys.modules["tree_sitter"] = MagicMock()

import pytest


@pytest.fixture
def mock_langfuse_client():
    """Mock Langfuse client for testing."""
    with patch("langfuse_agent.auth.LangfuseApi") as mock_langfuse:
        mock_client = MagicMock()
        mock_langfuse.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_api_client():
    """Mock LangfuseApi client for testing."""
    from langfuse_agent.api_client import LangfuseApi

    client = LangfuseApi(
        public_key="test_public_key",
        secret_key="test_secret_key",
        host="https://test.langfuse.com",
    )

    return client


@pytest.fixture
def mock_requests():
    """Mock requests module for HTTP request testing.

    CONCEPT:LA_1.0 — Langfuse MCP Integration
    """
    import requests

    with patch("langfuse_agent.api.api_client_base.requests") as mock_req:
        # Setup real exception for try-except block in client
        mock_req.exceptions.RequestException = requests.exceptions.RequestException
        # Setup default mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"success": true}'
        mock_response.json.return_value = {"success": True}
        mock_req.request.return_value = mock_response

        yield mock_req


@pytest.fixture
def sample_api_response():
    """Sample API response data."""
    return {"data": [{"id": "1", "name": "test"}], "meta": {"page": 1, "limit": 10}}


@pytest.fixture
def sample_queue_data():
    """Sample annotation queue data."""
    return {
        "id": "queue-123",
        "name": "Test Queue",
        "description": "A test queue",
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T00:00:00Z",
    }


@pytest.fixture
def sample_dataset_data():
    """Sample dataset data."""
    return {
        "name": "test-dataset",
        "description": "Test dataset",
        "metadata": {"key": "value"},
    }


@pytest.fixture
def clean_env():
    """Clean environment variables before and after tests."""
    original_env = os.environ.copy()

    # Clear relevant env vars
    env_vars_to_clear = [
        "LANGFUSE_BASE_URL",
        "LANGFUSE_PUBLIC_KEY",
        "LANGFUSE_SECRET_KEY",
        "LANGFUSE_URL",
        "LANGFUSE_TOKEN",
    ]

    for var in env_vars_to_clear:
        if var in os.environ:
            del os.environ[var]

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def mock_env_vars():
    """Set up mock environment variables."""
    original_env = os.environ.copy()

    os.environ["LANGFUSE_BASE_URL"] = "https://test.langfuse.com"
    os.environ["LANGFUSE_PUBLIC_KEY"] = "test_public_key"
    os.environ["LANGFUSE_SECRET_KEY"] = "test_secret_key"

    yield

    os.environ.clear()
    os.environ.update(original_env)
