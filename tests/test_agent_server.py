"""Tests for agent_server.py - Agent server implementation."""

from unittest.mock import MagicMock, patch


class TestAgentServer:
    """Tests for agent_server function."""

    def test_agent_server_imports(self):
        """Test that agent_server can be imported."""
        from langfuse_agent.agent_server import agent_server

        assert callable(agent_server)

    def test_agent_server_version_defined(self):
        """Test that __version__ is defined."""
        from langfuse_agent.agent_server import __version__

        assert __version__ is not None
        assert isinstance(__version__, str)
        assert "." in __version__

    def test_agent_server_function_exists(self):
        """Test that agent_server function exists."""
        from langfuse_agent.agent_server import agent_server

        assert agent_server is not None

    def test_agent_server_has_logging(self):
        """Test that agent_server sets up logging."""
        from langfuse_agent.agent_server import logger

        assert logger is not None
        assert logger.name == "langfuse_agent.agent_server"

    @patch("langfuse_agent.agent_server.create_agent_server")
    @patch("langfuse_agent.agent_server.create_agent_parser")
    def test_agent_server_calls_create_agent_server(
        self, mock_parser, mock_create_server
    ):
        """Test that agent_server calls create_agent_server."""
        import sys
        from io import StringIO

        from langfuse_agent.agent_server import agent_server

        # Mock the parser
        mock_args = MagicMock()
        mock_args.debug = False
        mock_args.mcp_url = None
        mock_args.mcp_config = "mcp_config.json"
        mock_args.host = "0.0.0.0"
        mock_args.port = 8000
        mock_args.provider = "openai"
        mock_args.model_id = "gpt-4"
        mock_args.base_url = None
        mock_args.api_key = None
        mock_args.custom_skills_directory = None
        mock_args.web = False
        mock_args.otel = False
        mock_args.otel_endpoint = None
        mock_args.otel_headers = None
        mock_args.otel_public_key = None
        mock_args.otel_secret_key = None
        mock_args.otel_protocol = None

        mock_parser.return_value.parse_args.return_value = mock_args

        # Capture stderr
        old_stderr = sys.stderr
        sys.stderr = StringIO()

        try:
            agent_server()
        except Exception:
            # We expect it might fail due to mocking, but we want to check the call
            pass
        finally:
            sys.stderr = old_stderr

        # Verify that create_agent_server was called
        mock_create_server.assert_called_once()

    def test_agent_server_default_constants(self):
        """Test that default constants are set."""
        from langfuse_agent.agent_server import (
            DEFAULT_AGENT_DESCRIPTION,
            DEFAULT_AGENT_NAME,
        )

        assert DEFAULT_AGENT_NAME is not None
        assert DEFAULT_AGENT_DESCRIPTION is not None
        assert isinstance(DEFAULT_AGENT_NAME, str)
        assert isinstance(DEFAULT_AGENT_DESCRIPTION, str)
