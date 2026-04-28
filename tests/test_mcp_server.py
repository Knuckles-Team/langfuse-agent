"""Tests for mcp_server.py - MCP server tool registration."""

import os
import pytest
from unittest.mock import MagicMock, patch


class TestToolRegistration:
    """Tests for tool registration functions."""

    @pytest.fixture
    def mock_mcp(self):
        """Mock FastMCP instance."""
        mcp = MagicMock()
        mcp.tool = MagicMock()
        mcp.prompt = MagicMock()
        return mcp

    @pytest.fixture
    def mock_client(self):
        """Mock Langfuse client."""
        client = MagicMock()
        client.annotation_queues_list_queues = MagicMock(return_value={"queues": []})
        client.annotation_queues_create_queue = MagicMock(
            return_value={"id": "queue-1"}
        )
        return client

    def test_register_prompts(self, mock_mcp):
        """Test prompt registration."""
        from langfuse_agent.mcp_server import register_prompts

        register_prompts(mock_mcp)

        mock_mcp.prompt.assert_called_once()
        call_kwargs = mock_mcp.prompt.call_args[1]
        assert call_kwargs["name"] == "langfuse-system-summary"

    def test_register_annotation_queues_tools(self, mock_mcp, mock_client):
        """Test annotation queues tools registration."""
        from langfuse_agent.mcp_server import register_annotation_queues_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_annotation_queues_tools(mock_mcp)

        # Should register 10 tools
        assert mock_mcp.tool.call_count == 10

    def test_register_blob_storage_integrations_tools(self, mock_mcp, mock_client):
        """Test blob storage integrations tools registration."""
        from langfuse_agent.mcp_server import register_blob_storage_integrations_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_blob_storage_integrations_tools(mock_mcp)

        # Should register 4 tools
        assert mock_mcp.tool.call_count == 4

    def test_register_comments_tools(self, mock_mcp, mock_client):
        """Test comments tools registration."""
        from langfuse_agent.mcp_server import register_comments_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_comments_tools(mock_mcp)

        # Should register 3 tools
        assert mock_mcp.tool.call_count == 3

    def test_register_dataset_items_tools(self, mock_mcp, mock_client):
        """Test dataset items tools registration."""
        from langfuse_agent.mcp_server import register_dataset_items_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_dataset_items_tools(mock_mcp)

        # Should register 4 tools
        assert mock_mcp.tool.call_count == 4

    def test_register_dataset_run_items_tools(self, mock_mcp, mock_client):
        """Test dataset run items tools registration."""
        from langfuse_agent.mcp_server import register_dataset_run_items_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_dataset_run_items_tools(mock_mcp)

        # Should register 2 tools
        assert mock_mcp.tool.call_count == 2

    def test_register_datasets_tools(self, mock_mcp, mock_client):
        """Test datasets tools registration."""
        from langfuse_agent.mcp_server import register_datasets_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_datasets_tools(mock_mcp)

        # Should register 6 tools
        assert mock_mcp.tool.call_count == 6

    def test_register_health_tools(self, mock_mcp, mock_client):
        """Test health tools registration."""
        from langfuse_agent.mcp_server import register_health_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_health_tools(mock_mcp)

        # Should register 1 tool
        assert mock_mcp.tool.call_count == 1

    def test_register_ingestion_tools(self, mock_mcp, mock_client):
        """Test ingestion tools registration."""
        from langfuse_agent.mcp_server import register_ingestion_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_ingestion_tools(mock_mcp)

        # Should register 1 tool
        assert mock_mcp.tool.call_count == 1

    def test_register_legacy_metrics_v1_tools(self, mock_mcp, mock_client):
        """Test legacy metrics v1 tools registration."""
        from langfuse_agent.mcp_server import register_legacy_metrics_v1_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_legacy_metrics_v1_tools(mock_mcp)

        # Should register 1 tool
        assert mock_mcp.tool.call_count == 1

    def test_register_legacy_observations_v1_tools(self, mock_mcp, mock_client):
        """Test legacy observations v1 tools registration."""
        from langfuse_agent.mcp_server import register_legacy_observations_v1_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_legacy_observations_v1_tools(mock_mcp)

        # Should register 2 tools
        assert mock_mcp.tool.call_count == 2

    def test_register_legacy_score_v1_tools(self, mock_mcp, mock_client):
        """Test legacy score v1 tools registration."""
        from langfuse_agent.mcp_server import register_legacy_score_v1_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_legacy_score_v1_tools(mock_mcp)

        # Should register 2 tools
        assert mock_mcp.tool.call_count == 2

    def test_register_llm_connections_tools(self, mock_mcp, mock_client):
        """Test LLM connections tools registration."""
        from langfuse_agent.mcp_server import register_llm_connections_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_llm_connections_tools(mock_mcp)

        # Should register 2 tools
        assert mock_mcp.tool.call_count == 2

    def test_register_media_tools(self, mock_mcp, mock_client):
        """Test media tools registration."""
        from langfuse_agent.mcp_server import register_media_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_media_tools(mock_mcp)

        # Should register 3 tools
        assert mock_mcp.tool.call_count == 3

    def test_register_metrics_tools(self, mock_mcp, mock_client):
        """Test metrics tools registration."""
        from langfuse_agent.mcp_server import register_metrics_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_metrics_tools(mock_mcp)

        # Should register 1 tool
        assert mock_mcp.tool.call_count == 1

    def test_register_models_tools(self, mock_mcp, mock_client):
        """Test models tools registration."""
        from langfuse_agent.mcp_server import register_models_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_models_tools(mock_mcp)

        # Should register 4 tools
        assert mock_mcp.tool.call_count == 4

    def test_register_observations_tools(self, mock_mcp, mock_client):
        """Test observations tools registration."""
        from langfuse_agent.mcp_server import register_observations_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_observations_tools(mock_mcp)

        # Should register 1 tool
        assert mock_mcp.tool.call_count == 1

    def test_register_opentelemetry_tools(self, mock_mcp, mock_client):
        """Test OpenTelemetry tools registration."""
        from langfuse_agent.mcp_server import register_opentelemetry_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_opentelemetry_tools(mock_mcp)

        # Should register 1 tool
        assert mock_mcp.tool.call_count == 1

    def test_register_organizations_tools(self, mock_mcp, mock_client):
        """Test organizations tools registration."""
        from langfuse_agent.mcp_server import register_organizations_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_organizations_tools(mock_mcp)

        # Should register 8 tools (based on actual implementation)
        assert mock_mcp.tool.call_count == 8

    def test_register_projects_tools(self, mock_mcp, mock_client):
        """Test projects tools registration."""
        from langfuse_agent.mcp_server import register_projects_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_projects_tools(mock_mcp)

        # Should register 7 tools
        assert mock_mcp.tool.call_count == 7

    def test_register_prompt_version_tools(self, mock_mcp, mock_client):
        """Test prompt version tools registration."""
        from langfuse_agent.mcp_server import register_prompt_version_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_prompt_version_tools(mock_mcp)

        # Should register 1 tool
        assert mock_mcp.tool.call_count == 1

    def test_register_prompts_tools(self, mock_mcp, mock_client):
        """Test prompts tools registration."""
        from langfuse_agent.mcp_server import register_prompts_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_prompts_tools(mock_mcp)

        # Should register 4 tools
        assert mock_mcp.tool.call_count == 4

    def test_register_scim_tools(self, mock_mcp, mock_client):
        """Test SCIM tools registration."""
        from langfuse_agent.mcp_server import register_scim_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_scim_tools(mock_mcp)

        # Should register 7 tools
        assert mock_mcp.tool.call_count == 7

    def test_register_score_configs_tools(self, mock_mcp, mock_client):
        """Test score configs tools registration."""
        from langfuse_agent.mcp_server import register_score_configs_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_score_configs_tools(mock_mcp)

        # Should register 4 tools
        assert mock_mcp.tool.call_count == 4

    def test_register_scores_tools(self, mock_mcp, mock_client):
        """Test scores tools registration."""
        from langfuse_agent.mcp_server import register_scores_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_scores_tools(mock_mcp)

        # Should register 2 tools
        assert mock_mcp.tool.call_count == 2

    def test_register_sessions_tools(self, mock_mcp, mock_client):
        """Test sessions tools registration."""
        from langfuse_agent.mcp_server import register_sessions_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_sessions_tools(mock_mcp)

        # Should register 2 tools
        assert mock_mcp.tool.call_count == 2

    def test_register_trace_tools(self, mock_mcp, mock_client):
        """Test trace tools registration."""
        from langfuse_agent.mcp_server import register_trace_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_trace_tools(mock_mcp)

        # Should register 4 tools
        assert mock_mcp.tool.call_count == 4


class TestRegisterAllTools:
    """Tests for register_all_tools function."""

    @pytest.fixture
    def mock_mcp(self):
        """Mock FastMCP instance."""
        mcp = MagicMock()
        mcp.tool = MagicMock()
        mcp.prompt = MagicMock()
        return mcp

    @pytest.fixture
    def mock_client(self):
        """Mock Langfuse client."""
        client = MagicMock()
        return client

    def test_register_all_tools_default(self, mock_mcp, mock_client):
        """Test register_all_tools with default settings."""
        from langfuse_agent.mcp_server import register_all_tools

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            registered_tags = register_all_tools(mock_mcp)

        # Should register all tool groups by default
        expected_tags = [
            "annotationqueues",
            "blobstorageintegrations",
            "comments",
            "datasetitems",
            "datasetrunitems",
            "datasets",
            "health",
            "ingestion",
            "legacymetricsv1",
            "legacyobservationsv1",
            "legacyscorev1",
            "llmconnections",
            "media",
            "metrics",
            "models",
            "observations",
            "opentelemetry",
            "organizations",
            "projects",
            "promptversion",
            "prompts",
            "scim",
            "scoreconfigs",
            "scores",
            "sessions",
            "trace",
        ]

        assert set(registered_tags) == set(expected_tags)

    def test_register_all_tools_with_disabled_tools(self, mock_mcp, mock_client):
        """Test register_all_tools with some tools disabled."""
        from langfuse_agent.mcp_server import register_all_tools

        os.environ["ANNOTATION_QUEUES_TOOL"] = "False"
        os.environ["DATASETS_TOOL"] = "False"

        try:
            with patch(
                "langfuse_agent.mcp_server.get_client", return_value=mock_client
            ):
                registered_tags = register_all_tools(mock_mcp)

            assert "annotationqueues" not in registered_tags
            assert "datasets" not in registered_tags
            assert "health" in registered_tags  # Should still be enabled
        finally:
            del os.environ["ANNOTATION_QUEUES_TOOL"]
            del os.environ["DATASETS_TOOL"]


class TestToolExecution:
    """Tests for tool execution."""

    @pytest.fixture
    def mock_mcp(self):
        """Mock FastMCP instance."""
        mcp = MagicMock()
        mcp.tool = MagicMock()
        mcp.prompt = MagicMock()
        return mcp

    @pytest.fixture
    def mock_client(self):
        """Mock Langfuse client."""
        client = MagicMock()
        client.annotation_queues_list_queues = MagicMock(return_value={"queues": []})
        client.datasets_list = MagicMock(return_value={"datasets": []})
        client.health_health = MagicMock(return_value={"status": "healthy"})
        return client

    # Tool execution tests are skipped due to complex mock setup requirements
    # The tool registration tests above provide sufficient coverage for the MCP server


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

                mcp, args, middlewares, registered_tags = get_mcp_instance()

                assert mcp is not None
                assert args is not None
                assert middlewares is not None
                assert isinstance(registered_tags, list)
                assert len(registered_tags) > 0


class TestVersion:
    """Tests for version constant."""

    def test_version_defined(self):
        """Test that __version__ is defined."""
        from langfuse_agent.mcp_server import __version__

        assert __version__ is not None
        assert isinstance(__version__, str)
        assert "." in __version__


class TestMCPServer:
    """Tests for mcp_server function."""

    @pytest.fixture
    def mock_mcp_instance(self):
        """Mock MCP instance."""
        mcp = MagicMock()
        mcp.run = MagicMock()
        return mcp

    @pytest.fixture
    def mock_args(self):
        """Mock args."""
        args = MagicMock()
        args.transport = "stdio"
        args.host = "0.0.0.0"
        args.port = 8000
        args.auth_type = "none"
        return args

    @patch("langfuse_agent.mcp_server.get_mcp_instance")
    def test_mcp_server_stdio_transport(
        self, mock_get_instance, mock_mcp_instance, mock_args
    ):
        """Test mcp_server with stdio transport."""
        from langfuse_agent.mcp_server import mcp_server
        import sys
        from io import StringIO

        mock_get_instance.return_value = (mock_mcp_instance, mock_args, [], [])

        # Capture stderr
        old_stderr = sys.stderr
        sys.stderr = StringIO()

        try:
            mcp_server()
        except Exception:
            pass  # We expect it might fail due to mocking
        finally:
            sys.stderr = old_stderr

        # Verify that mcp.run was called with stdio transport
        mock_mcp_instance.run.assert_called_once_with(transport="stdio")

    @patch("langfuse_agent.mcp_server.get_mcp_instance")
    def test_mcp_server_http_transport(
        self, mock_get_instance, mock_mcp_instance, mock_args
    ):
        """Test mcp_server with streamable-http transport."""
        from langfuse_agent.mcp_server import mcp_server
        import sys
        from io import StringIO

        mock_args.transport = "streamable-http"
        mock_get_instance.return_value = (mock_mcp_instance, mock_args, [], [])

        # Capture stderr
        old_stderr = sys.stderr
        sys.stderr = StringIO()

        try:
            mcp_server()
        except Exception:
            pass  # We expect it might fail due to mocking
        finally:
            sys.stderr = old_stderr

        # Verify that mcp.run was called with streamable-http transport
        mock_mcp_instance.run.assert_called_once_with(
            transport="streamable-http", host="0.0.0.0", port=8000
        )

    @patch("langfuse_agent.mcp_server.get_mcp_instance")
    def test_mcp_server_sse_transport(
        self, mock_get_instance, mock_mcp_instance, mock_args
    ):
        """Test mcp_server with sse transport."""
        from langfuse_agent.mcp_server import mcp_server
        import sys
        from io import StringIO

        mock_args.transport = "sse"
        mock_get_instance.return_value = (mock_mcp_instance, mock_args, [], [])

        # Capture stderr
        old_stderr = sys.stderr
        sys.stderr = StringIO()

        try:
            mcp_server()
        except Exception:
            pass  # We expect it might fail due to mocking
        finally:
            sys.stderr = old_stderr

        # Verify that mcp.run was called with sse transport
        mock_mcp_instance.run.assert_called_once_with(
            transport="sse", host="0.0.0.0", port=8000
        )


class TestToolExecution:
    """Tests for actual tool function execution."""

    @pytest.fixture
    def mock_client(self):
        """Mock Langfuse client."""
        client = MagicMock()
        client.annotation_queues_list_queues = MagicMock(return_value={"queues": []})
        client.annotation_queues_create_queue = MagicMock(
            return_value={"id": "queue-1"}
        )
        client.annotation_queues_get_queue = MagicMock(return_value={"id": "queue-1"})
        client.annotation_queues_list_queue_items = MagicMock(
            return_value={"items": []}
        )
        client.annotation_queues_create_queue_item = MagicMock(
            return_value={"id": "item-1"}
        )
        client.annotation_queues_get_queue_item = MagicMock(
            return_value={"id": "item-1"}
        )
        client.annotation_queues_update_queue_item = MagicMock(
            return_value={"id": "item-1"}
        )
        client.annotation_queues_delete_queue_item = MagicMock(
            return_value={"success": True}
        )
        client.annotation_queues_create_queue_assignment = MagicMock(
            return_value={"id": "assignment-1"}
        )
        client.annotation_queues_delete_queue_assignment = MagicMock(
            return_value={"success": True}
        )
        client.blob_storage_integrations_get_blob_storage_integrations = MagicMock(
            return_value={"integrations": []}
        )
        client.blob_storage_integrations_upsert_blob_storage_integration = MagicMock(
            return_value={"id": "integration-1"}
        )
        client.blob_storage_integrations_get_blob_storage_integration_status = (
            MagicMock(return_value={"status": "active"})
        )
        client.blob_storage_integrations_delete_blob_storage_integration = MagicMock(
            return_value={"success": True}
        )
        client.comments_create = MagicMock(return_value={"id": "comment-1"})
        client.comments_get = MagicMock(return_value={"id": "comment-1"})
        client.comments_get_by_id = MagicMock(return_value={"id": "comment-1"})
        client.dataset_items_create = MagicMock(return_value={"id": "item-1"})
        client.dataset_items_list = MagicMock(return_value={"items": []})
        client.dataset_items_get = MagicMock(return_value={"id": "item-1"})
        client.dataset_items_delete = MagicMock(return_value={"success": True})
        client.dataset_run_items_create = MagicMock(return_value={"id": "item-1"})
        client.dataset_run_items_list = MagicMock(return_value={"items": []})
        client.datasets_list = MagicMock(return_value={"datasets": []})
        client.datasets_create = MagicMock(return_value={"id": "dataset-1"})
        client.datasets_get = MagicMock(return_value={"id": "dataset-1"})
        client.datasets_get_run = MagicMock(return_value={"id": "run-1"})
        client.datasets_delete_run = MagicMock(return_value={"success": True})
        client.datasets_get_runs = MagicMock(return_value={"runs": []})
        client.health_health = MagicMock(return_value={"status": "ok"})
        client.ingestion_batch = MagicMock(return_value={"success": True})
        client.legacy_metrics_v1_metrics = MagicMock(return_value={"metrics": []})
        client.legacy_observations_v1_get = MagicMock(return_value={"id": "obs-1"})
        client.legacy_observations_v1_get_many = MagicMock(
            return_value={"observations": []}
        )
        client.legacy_score_v1_create = MagicMock(return_value={"id": "score-1"})
        client.legacy_score_v1_delete = MagicMock(return_value={"success": True})
        client.llm_connections_list = MagicMock(return_value={"connections": []})
        client.llm_connections_upsert = MagicMock(return_value={"id": "connection-1"})
        client.media_get = MagicMock(return_value={"id": "media-1"})
        client.media_patch = MagicMock(return_value={"id": "media-1"})
        client.media_get_upload_url = MagicMock(
            return_value={"url": "https://example.com"}
        )
        client.metrics_metrics = MagicMock(return_value={"metrics": []})
        client.models_create = MagicMock(return_value={"id": "model-1"})
        client.models_list = MagicMock(return_value={"models": []})
        client.models_get = MagicMock(return_value={"id": "model-1"})
        client.models_delete = MagicMock(return_value={"success": True})
        client.observations_get_many = MagicMock(return_value={"observations": []})
        client.opentelemetry_export_traces = MagicMock(return_value={"success": True})
        client.organizations_get_organization_memberships = MagicMock(
            return_value={"memberships": []}
        )
        client.organizations_update_organization_membership = MagicMock(
            return_value={"id": "membership-1"}
        )
        client.organizations_delete_organization_membership = MagicMock(
            return_value={"success": True}
        )
        client.organizations_get_project_memberships = MagicMock(
            return_value={"memberships": []}
        )
        client.organizations_update_project_membership = MagicMock(
            return_value={"id": "membership-1"}
        )
        client.organizations_delete_project_membership = MagicMock(
            return_value={"success": True}
        )
        client.organizations_get_organization_projects = MagicMock(
            return_value={"projects": []}
        )
        client.organizations_get_organization_api_keys = MagicMock(
            return_value={"keys": []}
        )
        client.projects_get = MagicMock(return_value={"id": "project-1"})
        client.projects_create = MagicMock(return_value={"id": "project-1"})
        client.projects_update = MagicMock(return_value={"id": "project-1"})
        client.projects_delete = MagicMock(return_value={"success": True})
        client.projects_get_api_keys = MagicMock(return_value={"keys": []})
        client.projects_create_api_key = MagicMock(return_value={"id": "key-1"})
        client.projects_delete_api_key = MagicMock(return_value={"success": True})
        client.prompt_version_update = MagicMock(return_value={"id": "version-1"})
        client.prompts_get = MagicMock(return_value={"id": "prompt-1"})
        client.prompts_delete = MagicMock(return_value={"success": True})
        client.prompts_list = MagicMock(return_value={"prompts": []})
        client.prompts_create = MagicMock(return_value={"id": "prompt-1"})
        client.scim_get_service_provider_config = MagicMock(return_value={"config": {}})
        client.scim_get_resource_types = MagicMock(return_value={"types": []})
        client.scim_get_schemas = MagicMock(return_value={"schemas": []})
        client.scim_list_users = MagicMock(return_value={"users": []})
        client.scim_create_user = MagicMock(return_value={"id": "user-1"})
        client.scim_get_user = MagicMock(return_value={"id": "user-1"})
        client.scim_delete_user = MagicMock(return_value={"success": True})
        client.score_configs_create = MagicMock(return_value={"id": "config-1"})
        client.score_configs_get = MagicMock(return_value={"id": "config-1"})
        client.score_configs_get_by_id = MagicMock(return_value={"id": "config-1"})
        client.score_configs_update = MagicMock(return_value={"id": "config-1"})
        client.scores_get_many = MagicMock(return_value={"scores": []})
        client.scores_get_by_id = MagicMock(return_value={"id": "score-1"})
        client.sessions_list = MagicMock(return_value={"sessions": []})
        client.sessions_get = MagicMock(return_value={"id": "session-1"})
        client.trace_get = MagicMock(return_value={"id": "trace-1"})
        client.trace_delete = MagicMock(return_value={"success": True})
        client.trace_list = MagicMock(return_value={"traces": []})
        client.trace_delete_multiple = MagicMock(return_value={"success": True})
        return client

    def test_annotation_queues_tool_execution(self, mock_client):
        """Test execution of annotation queues tools."""
        from langfuse_agent.mcp_server import register_annotation_queues_tools

        captured_functions = {}
        mock_mcp = MagicMock()

        def capture_tool(name=None, description=None, tags=None):
            def decorator(func):
                captured_functions[name] = func
                return func

            return decorator

        mock_mcp.tool = capture_tool

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_annotation_queues_tools(mock_mcp)

            # Execute the captured functions
            result = captured_functions[
                "langfuse-annotation-queues-annotation-queues-list-queues"
            ]()
            assert result == {"queues": []}
            mock_client.annotation_queues_list_queues.assert_called_once()

            result = captured_functions[
                "langfuse-annotation-queues-annotation-queues-create-queue"
            ]({"name": "test"})
            assert result == {"id": "queue-1"}
            mock_client.annotation_queues_create_queue.assert_called_once()

    def test_datasets_tool_execution(self, mock_client):
        """Test execution of datasets tools."""
        from langfuse_agent.mcp_server import register_datasets_tools

        captured_functions = {}
        mock_mcp = MagicMock()

        def capture_tool(name=None, description=None, tags=None):
            def decorator(func):
                captured_functions[name] = func
                return func

            return decorator

        mock_mcp.tool = capture_tool

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_datasets_tools(mock_mcp)

            # Execute the captured functions
            result = captured_functions["langfuse-datasets-list"]()
            assert result == {"datasets": []}
            mock_client.datasets_list.assert_called_once()

            result = captured_functions["langfuse-datasets-create"]({"name": "test"})
            assert result == {"id": "dataset-1"}
            mock_client.datasets_create.assert_called_once()

    def test_projects_tool_execution(self, mock_client):
        """Test execution of projects tools."""
        from langfuse_agent.mcp_server import register_projects_tools

        captured_functions = {}
        mock_mcp = MagicMock()

        def capture_tool(name=None, description=None, tags=None):
            def decorator(func):
                captured_functions[name] = func
                return func

            return decorator

        mock_mcp.tool = capture_tool

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_projects_tools(mock_mcp)

            # Execute the captured functions
            result = captured_functions["langfuse-projects-get"]()
            assert result == {"id": "project-1"}
            mock_client.projects_get.assert_called_once()

            result = captured_functions["langfuse-projects-create"]("test", 30)
            assert result == {"id": "project-1"}
            mock_client.projects_create.assert_called_once()

    def test_traces_tool_execution(self, mock_client):
        """Test execution of traces tools."""
        from langfuse_agent.mcp_server import register_trace_tools

        captured_functions = {}
        mock_mcp = MagicMock()

        def capture_tool(name=None, description=None, tags=None):
            def decorator(func):
                captured_functions[name] = func
                return func

            return decorator

        mock_mcp.tool = capture_tool

        with patch("langfuse_agent.mcp_server.get_client", return_value=mock_client):
            register_trace_tools(mock_mcp)

            # Execute the captured functions
            result = captured_functions["langfuse-trace-get"]("trace-1")
            assert result == {"id": "trace-1"}
            mock_client.trace_get.assert_called_once()

            result = captured_functions["langfuse-trace-list"]()
            assert result == {"traces": []}
            mock_client.trace_list.assert_called_once()
