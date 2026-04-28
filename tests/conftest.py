"""Pytest configuration and fixtures for langfuse-agent tests."""

import os
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_langfuse_client():
    """Mock Langfuse client for testing."""
    with patch("langfuse_agent.auth.Langfuse") as mock_langfuse:
        mock_client = MagicMock()
        mock_langfuse.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_api_client():
    """Mock LangfuseApi client for testing."""
    from langfuse_agent.langfuse_api import LangfuseApi

    client = LangfuseApi(
        public_key="test_public_key",
        secret_key="test_secret_key",
        host="https://test.langfuse.com",
    )

    return client


@pytest.fixture
def mock_requests():
    """Mock requests module for HTTP request testing."""
    with patch("langfuse_agent.langfuse_api.requests") as mock_req:
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
        "LANGFUSE_HOST",
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

    os.environ["LANGFUSE_HOST"] = "https://test.langfuse.com"
    os.environ["LANGFUSE_PUBLIC_KEY"] = "test_public_key"
    os.environ["LANGFUSE_SECRET_KEY"] = "test_secret_key"

    yield

    os.environ.clear()
    os.environ.update(original_env)
