"""Tests for auth.py - Langfuse client authentication."""

import os
from unittest.mock import MagicMock, patch


class TestGetClient:
    """Tests for the get_client function."""

    def test_get_client_with_env_vars(self, clean_env):
        _ = clean_env
        """Test get_client with environment variables set."""
        os.environ["LANGFUSE_BASE_URL"] = "https://test.langfuse.com"
        os.environ["LANGFUSE_PUBLIC_KEY"] = "test_public_key"
        os.environ["LANGFUSE_SECRET_KEY"] = "test_secret_key"

        with patch("langfuse_agent.auth.LangfuseApi") as mock_langfuse:
            mock_client = MagicMock()
            mock_langfuse.return_value = mock_client

            # Import after setting env vars
            # Reset the global client to force re-initialization
            import langfuse_agent.auth
            from langfuse_agent.auth import get_client

            langfuse_agent.auth._client = None

            client = get_client()

            mock_langfuse.assert_called_once_with(
                public_key="test_public_key",
                secret_key="test_secret_key",
                host="https://test.langfuse.com",
            )
            assert client == mock_client

    def test_get_client_default_host(self, clean_env):
        _ = clean_env
        """Test get_client uses default host when not set."""
        os.environ["LANGFUSE_PUBLIC_KEY"] = "test_public_key"
        os.environ["LANGFUSE_SECRET_KEY"] = "test_secret_key"

        with patch("langfuse_agent.auth.LangfuseApi") as mock_langfuse:
            mock_client = MagicMock()
            mock_langfuse.return_value = mock_client

            # Import after setting env vars
            # Reset the global client to force re-initialization
            import langfuse_agent.auth
            from langfuse_agent.auth import get_client

            langfuse_agent.auth._client = None

            client = get_client()

            mock_langfuse.assert_called_once()
            call_kwargs = mock_langfuse.call_args[1]
            assert call_kwargs["host"] == "https://cloud.langfuse.com"

    def test_get_client_caching(self, clean_env):
        _ = clean_env
        """Test that get_client caches the client instance."""
        os.environ["LANGFUSE_PUBLIC_KEY"] = "test_public_key"
        os.environ["LANGFUSE_SECRET_KEY"] = "test_secret_key"

        with patch("langfuse_agent.auth.LangfuseApi") as mock_langfuse:
            mock_client = MagicMock()
            mock_langfuse.return_value = mock_client

            # Import after setting env vars
            # Reset the global client to force re-initialization
            import langfuse_agent.auth
            from langfuse_agent.auth import get_client

            langfuse_agent.auth._client = None

            client1 = get_client()
            client2 = get_client()

            # Should only call LangfuseApi once due to caching
            mock_langfuse.assert_called_once()
            assert client1 == mock_client
            assert client2 == mock_client

    def test_get_client_empty_credentials(self, clean_env):
        _ = clean_env
        """Test get_client with empty credentials."""
        with patch("langfuse_agent.auth.LangfuseApi") as mock_langfuse:
            mock_client = MagicMock()
            mock_langfuse.return_value = mock_client

            # Import after setting env vars
            # Reset the global client to force re-initialization
            import langfuse_agent.auth
            from langfuse_agent.auth import get_client

            langfuse_agent.auth._client = None

            client = get_client()

            mock_langfuse.assert_called_once()
            call_kwargs = mock_langfuse.call_args[1]
            assert call_kwargs["public_key"] == ""
            assert call_kwargs["secret_key"] == ""

    def test_get_client_custom_host(self, clean_env):
        _ = clean_env
        """Test get_client with custom host."""
        os.environ["LANGFUSE_BASE_URL"] = "https://custom.langfuse.com"
        os.environ["LANGFUSE_PUBLIC_KEY"] = "test_public_key"
        os.environ["LANGFUSE_SECRET_KEY"] = "test_secret_key"

        with patch("langfuse_agent.auth.LangfuseApi") as mock_langfuse:
            mock_client = MagicMock()
            mock_langfuse.return_value = mock_client

            # Import after setting env vars
            # Reset the global client to force re-initialization
            import langfuse_agent.auth
            from langfuse_agent.auth import get_client

            langfuse_agent.auth._client = None

            client = get_client()

            call_kwargs = mock_langfuse.call_args[1]
            assert call_kwargs["host"] == "https://custom.langfuse.com"

    def test_get_client_oidc_delegation(self, clean_env):
        _ = clean_env
        """Test get_client when OIDC delegation is enabled."""
        os.environ["LANGFUSE_PUBLIC_KEY"] = "test_public_key"
        os.environ["LANGFUSE_SECRET_KEY"] = "test_secret_key"

        with (
            patch("langfuse_agent.auth.LangfuseApi") as mock_langfuse,
            patch(
                "agent_utilities.mcp.delegated_auth.is_delegation_enabled",
                return_value=True,
            ),
            patch(
                "agent_utilities.mcp.delegated_auth.get_user_identity",
                return_value={"email": "test@example.com", "subject": "user-123"},
            ),
            patch("langfuse_agent.auth.logger") as mock_logger,
        ):
            mock_client = MagicMock()
            mock_langfuse.return_value = mock_client

            import langfuse_agent.auth
            from langfuse_agent.auth import get_client

            langfuse_agent.auth._client = None

            client = get_client()

            mock_logger.info.assert_called_once()
            assert client == mock_client
