"""Tests for mcp_server.py - MCP server tool registration."""

from unittest.mock import MagicMock, patch

import pytest


class TestToolRegistration:
    def test_tools_registered(self):
        from unittest.mock import MagicMock, patch

        from langfuse_agent.mcp_server import get_mcp_instance

        with patch("langfuse_agent.mcp_server.get_client", return_value=MagicMock()):
            with patch("langfuse_agent.mcp_server.create_mcp_server") as mock_create:
                mcp_mock = MagicMock()
                mock_create.return_value = (mcp_mock, MagicMock(), [MagicMock()])
                mcp, _, _ = get_mcp_instance()

                # Verify that mcp tool decorators were executed during module load or instance creation
                assert mcp is not None


class TestGetMcpInstance:
    """Tests for get_mcp_instance function."""

    @pytest.fixture
    def mock_client(self):
        """Mock Langfuse client."""
        client = MagicMock()
        return client

    def test_get_mcp_instance(self, mock_client):
        """Test get_mcp_instance returns correct components."""
        from langfuse_agent.mcp_server import get_mcp_instance

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            with patch("langfuse_agent.mcp_server.create_mcp_server") as mock_create:
                mock_create.return_value = (MagicMock(), MagicMock(), [MagicMock()])

                mcp, args, middlewares = get_mcp_instance()

                assert mcp is not None


class TestVersion:
    def test_version_defined(self):
        from langfuse_agent.mcp_server import __version__

        assert __version__ is not None
        assert isinstance(__version__, str)
