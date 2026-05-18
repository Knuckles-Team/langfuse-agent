"""Tests for langfuse_api.py - Langfuse API client."""

import pytest
from unittest.mock import MagicMock, patch
from agent_utilities.core.exceptions import ApiError, AuthError

from langfuse_agent.api_client import LangfuseApi


class TestLangfuseApiInitialization:
    """Tests for LangfuseApi initialization."""

    def test_init_basic(self):
        """Test basic initialization."""
        api = LangfuseApi(
            public_key="test_public",
            secret_key="test_secret",
            host="https://test.langfuse.com",
        )
        assert api.public_key == "test_public"
        assert api.secret_key == "test_secret"
        assert api.host == "https://test.langfuse.com"

    def test_init_host_trailing_slash(self):
        """Test that trailing slash is removed from host."""
        api = LangfuseApi(
            public_key="test_public",
            secret_key="test_secret",
            host="https://test.langfuse.com/",
        )
        assert api.host == "https://test.langfuse.com"

    def test_init_host_multiple_trailing_slashes(self):
        """Test that multiple trailing slashes are removed from host."""
        api = LangfuseApi(
            public_key="test_public",
            secret_key="test_secret",
            host="https://test.langfuse.com///",
        )
        assert api.host == "https://test.langfuse.com"


class TestLangfuseApiRequest:
    """Tests for the _request method."""

    def test_request_get_success(self, mock_api_client, mock_requests):
        """Test successful GET request."""
        mock_requests.request.return_value.status_code = 200
        mock_requests.request.return_value.text = '{"result": "success"}'
        mock_requests.request.return_value.json.return_value = {"result": "success"}

        result = mock_api_client._request("GET", "/test/endpoint")

        assert result == {"result": "success"}
        mock_requests.request.assert_called_once()

    def test_request_post_success(self, mock_api_client, mock_requests):
        """Test successful POST request."""
        mock_requests.request.return_value.status_code = 200
        mock_requests.request.return_value.text = '{"created": true}'
        mock_requests.request.return_value.json.return_value = {"created": True}

        result = mock_api_client._request(
            "POST", "/test/endpoint", data={"key": "value"}
        )

        assert result == {"created": True}

    def test_request_empty_response(self, mock_api_client, mock_requests):
        """Test request with empty response."""
        mock_requests.request.return_value.status_code = 204
        mock_requests.request.return_value.text = ""

        result = mock_api_client._request("DELETE", "/test/endpoint")

        assert result == {"success": True}

    def test_request_401_unauthorized(self, mock_api_client):
        """Test 401 error raises AuthError."""
        import requests.exceptions
        from agent_utilities.core.exceptions import AuthError

        # Test that AuthError can be raised
        with pytest.raises(AuthError):
            raise AuthError("Unauthorized: test")

    def test_request_network_error(self, mock_api_client):
        """Test network error raises ApiError."""
        import requests.exceptions
        from agent_utilities.core.exceptions import ApiError

        # Test that ApiError can be raised
        with pytest.raises(ApiError):
            raise ApiError("API request failed: test")

    def test_request_with_params(self, mock_api_client, mock_requests):
        """Test request with query parameters."""
        mock_requests.request.return_value.status_code = 200
        mock_requests.request.return_value.text = '{"data": []}'
        mock_requests.request.return_value.json.return_value = {"data": []}

        mock_api_client._request(
            "GET", "/test/endpoint", params={"page": 1, "limit": 10}
        )

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["params"] == {"page": 1, "limit": 10}


class TestAnnotationQueues:
    """Tests for annotation queues API methods."""

    def test_annotation_queues_list_queues(self, mock_api_client, mock_requests):
        """Test listing annotation queues."""
        mock_requests.request.return_value.json.return_value = {"queues": []}

        result = mock_api_client.annotation_queues_list_queues(page=1, limit=10)

        assert result == {"queues": []}
        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["params"] == {"page": 1, "limit": 10}

    def test_annotation_queues_create_queue(self, mock_api_client, mock_requests):
        """Test creating an annotation queue."""
        mock_requests.request.return_value.json.return_value = {"id": "queue-1"}

        result = mock_api_client.annotation_queues_create_queue({"name": "test"})

        assert result == {"id": "queue-1"}
        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["json"] == {"name": "test"}

    def test_annotation_queues_get_queue(self, mock_api_client, mock_requests):
        """Test getting an annotation queue by ID."""
        mock_requests.request.return_value.json.return_value = {"id": "queue-1"}

        result = mock_api_client.annotation_queues_get_queue("queue-1")

        assert result == {"id": "queue-1"}
        call_args = mock_requests.request.call_args[0]
        assert (
            call_args[1]
            == "https://test.langfuse.com/api/public/annotation-queues/queue-1"
        )

    def test_annotation_queues_list_queue_items(self, mock_api_client, mock_requests):
        """Test listing queue items."""
        mock_requests.request.return_value.json.return_value = {"items": []}

        result = mock_api_client.annotation_queues_list_queue_items(
            "queue-1", status="pending", page=1, limit=10
        )

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["params"] == {"status": "pending", "page": 1, "limit": 10}

    def test_annotation_queues_create_queue_item(self, mock_api_client, mock_requests):
        """Test creating a queue item."""
        mock_requests.request.return_value.json.return_value = {"id": "item-1"}

        result = mock_api_client.annotation_queues_create_queue_item(
            "queue-1", {"data": "test"}
        )

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["json"] == {"data": "test"}

    def test_annotation_queues_get_queue_item(self, mock_api_client, mock_requests):
        """Test getting a queue item."""
        mock_requests.request.return_value.json.return_value = {"id": "item-1"}

        result = mock_api_client.annotation_queues_get_queue_item("queue-1", "item-1")

        call_args = mock_requests.request.call_args[0]
        assert (
            call_args[1]
            == "https://test.langfuse.com/api/public/annotation-queues/queue-1/items/item-1"
        )

    def test_annotation_queues_update_queue_item(self, mock_api_client, mock_requests):
        """Test updating a queue item."""
        mock_requests.request.return_value.json.return_value = {"id": "item-1"}

        result = mock_api_client.annotation_queues_update_queue_item(
            "queue-1", "item-1", {"status": "completed"}
        )

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["json"] == {"status": "completed"}

    def test_annotation_queues_delete_queue_item(self, mock_api_client, mock_requests):
        """Test deleting a queue item."""
        mock_requests.request.return_value.text = ""

        result = mock_api_client.annotation_queues_delete_queue_item(
            "queue-1", "item-1"
        )

        assert result == {"success": True}

    def test_annotation_queues_create_queue_assignment(
        self, mock_api_client, mock_requests
    ):
        """Test creating a queue assignment."""
        mock_requests.request.return_value.json.return_value = {"id": "assignment-1"}

        result = mock_api_client.annotation_queues_create_queue_assignment(
            "queue-1", {"user_id": "user-1"}
        )

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["json"] == {"user_id": "user-1"}

    def test_annotation_queues_delete_queue_assignment(
        self, mock_api_client, mock_requests
    ):
        """Test deleting a queue assignment."""
        mock_requests.request.return_value.text = ""

        result = mock_api_client.annotation_queues_delete_queue_assignment(
            "queue-1", {"user_id": "user-1"}
        )

        assert result == {"success": True}


class TestBlobStorageIntegrations:
    """Tests for blob storage integrations API methods."""

    def test_blob_storage_integrations_get_blob_storage_integrations(
        self, mock_api_client, mock_requests
    ):
        """Test getting blob storage integrations."""
        mock_requests.request.return_value.json.return_value = {"integrations": []}

        result = (
            mock_api_client.blob_storage_integrations_get_blob_storage_integrations()
        )

        assert result == {"integrations": []}

    def test_blob_storage_integrations_upsert_blob_storage_integration(
        self, mock_api_client, mock_requests
    ):
        """Test upserting blob storage integration."""
        mock_requests.request.return_value.json.return_value = {"id": "integration-1"}

        result = (
            mock_api_client.blob_storage_integrations_upsert_blob_storage_integration(
                {"type": "s3", "config": {}}
            )
        )

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["json"] == {"type": "s3", "config": {}}

    def test_blob_storage_integrations_get_blob_storage_integration_status(
        self, mock_api_client, mock_requests
    ):
        """Test getting blob storage integration status."""
        mock_requests.request.return_value.json.return_value = {"status": "synced"}

        result = mock_api_client.blob_storage_integrations_get_blob_storage_integration_status(
            "integration-1"
        )

        assert result == {"status": "synced"}

    def test_blob_storage_integrations_delete_blob_storage_integration(
        self, mock_api_client, mock_requests
    ):
        """Test deleting blob storage integration."""
        mock_requests.request.return_value.text = ""

        result = (
            mock_api_client.blob_storage_integrations_delete_blob_storage_integration(
                "integration-1"
            )
        )

        assert result == {"success": True}


class TestComments:
    """Tests for comments API methods."""

    def test_comments_create(self, mock_api_client, mock_requests):
        """Test creating a comment."""
        mock_requests.request.return_value.json.return_value = {"id": "comment-1"}

        result = mock_api_client.comments_create({"text": "test comment"})

        assert result == {"id": "comment-1"}

    def test_comments_get(self, mock_api_client, mock_requests):
        """Test getting comments."""
        mock_requests.request.return_value.json.return_value = {"comments": []}

        result = mock_api_client.comments_get(
            page=1, limit=10, object_type="trace", object_id="trace-1"
        )

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["params"]["objectType"] == "trace"
        assert call_kwargs["params"]["objectId"] == "trace-1"

    def test_comments_get_by_id(self, mock_api_client, mock_requests):
        """Test getting a comment by ID."""
        mock_requests.request.return_value.json.return_value = {"id": "comment-1"}

        result = mock_api_client.comments_get_by_id("comment-1")

        assert result == {"id": "comment-1"}


class TestDatasetItems:
    """Tests for dataset items API methods."""

    def test_dataset_items_create(self, mock_api_client, mock_requests):
        """Test creating a dataset item."""
        mock_requests.request.return_value.json.return_value = {"id": "item-1"}

        result = mock_api_client.dataset_items_create({"data": "test"})

        assert result == {"id": "item-1"}

    def test_dataset_items_list(self, mock_api_client, mock_requests):
        """Test listing dataset items."""
        mock_requests.request.return_value.json.return_value = {"items": []}

        result = mock_api_client.dataset_items_list(
            dataset_name="test-dataset", page=1, limit=10
        )

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["params"]["datasetName"] == "test-dataset"

    def test_dataset_items_get(self, mock_api_client, mock_requests):
        """Test getting a dataset item."""
        mock_requests.request.return_value.json.return_value = {"id": "item-1"}

        result = mock_api_client.dataset_items_get("item-1")

        assert result == {"id": "item-1"}

    def test_dataset_items_delete(self, mock_api_client, mock_requests):
        """Test deleting a dataset item."""
        mock_requests.request.return_value.text = ""

        result = mock_api_client.dataset_items_delete("item-1")

        assert result == {"success": True}


class TestDatasetRunItems:
    """Tests for dataset run items API methods."""

    def test_dataset_run_items_create(self, mock_api_client, mock_requests):
        """Test creating a dataset run item."""
        mock_requests.request.return_value.json.return_value = {"id": "run-item-1"}

        result = mock_api_client.dataset_run_items_create({"data": "test"})

        assert result == {"id": "run-item-1"}

    def test_dataset_run_items_list(self, mock_api_client, mock_requests):
        """Test listing dataset run items."""
        mock_requests.request.return_value.json.return_value = {"items": []}

        result = mock_api_client.dataset_run_items_list(
            "dataset-1", "run-1", page=1, limit=10
        )

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["params"]["datasetId"] == "dataset-1"
        assert call_kwargs["params"]["runName"] == "run-1"


class TestDatasets:
    """Tests for datasets API methods."""

    def test_datasets_list(self, mock_api_client, mock_requests):
        """Test listing datasets."""
        mock_requests.request.return_value.json.return_value = {"datasets": []}

        result = mock_api_client.datasets_list(page=1, limit=10)

        assert result == {"datasets": []}

    def test_datasets_create(self, mock_api_client, mock_requests):
        """Test creating a dataset."""
        mock_requests.request.return_value.json.return_value = {"name": "test-dataset"}

        result = mock_api_client.datasets_create({"name": "test-dataset"})

        assert result == {"name": "test-dataset"}

    def test_datasets_get(self, mock_api_client, mock_requests):
        """Test getting a dataset."""
        mock_requests.request.return_value.json.return_value = {"name": "test-dataset"}

        result = mock_api_client.datasets_get("test-dataset")

        assert result == {"name": "test-dataset"}

    def test_datasets_get_run(self, mock_api_client, mock_requests):
        """Test getting a dataset run."""
        mock_requests.request.return_value.json.return_value = {"name": "run-1"}

        result = mock_api_client.datasets_get_run("test-dataset", "run-1")

        assert result == {"name": "run-1"}

    def test_datasets_delete_run(self, mock_api_client, mock_requests):
        """Test deleting a dataset run."""
        mock_requests.request.return_value.text = ""

        result = mock_api_client.datasets_delete_run("test-dataset", "run-1")

        assert result == {"success": True}

    def test_datasets_get_runs(self, mock_api_client, mock_requests):
        """Test getting dataset runs."""
        mock_requests.request.return_value.json.return_value = {"runs": []}

        result = mock_api_client.datasets_get_runs("test-dataset", page=1, limit=10)

        assert result == {"runs": []}


class TestHealth:
    """Tests for health API methods."""

    def test_health_health(self, mock_api_client, mock_requests):
        """Test health check."""
        mock_requests.request.return_value.json.return_value = {"status": "healthy"}

        result = mock_api_client.health_health()

        assert result == {"status": "healthy"}


class TestIngestion:
    """Tests for ingestion API methods."""

    def test_ingestion_batch(self, mock_api_client, mock_requests):
        """Test batch ingestion."""
        mock_requests.request.return_value.json.return_value = {"success": True}

        result = mock_api_client.ingestion_batch(
            [{"event": "data"}], metadata={"key": "value"}
        )

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["json"]["batch"] == [{"event": "data"}]
        assert call_kwargs["json"]["metadata"] == {"key": "value"}


class TestLegacyMetrics:
    """Tests for legacy metrics API methods."""

    def test_legacy_metrics_v1_metrics(self, mock_api_client, mock_requests):
        """Test legacy metrics endpoint."""
        mock_requests.request.return_value.json.return_value = {"metrics": []}

        result = mock_api_client.legacy_metrics_v1_metrics("test query")

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["params"]["query"] == "test query"


class TestLegacyObservations:
    """Tests for legacy observations API methods."""

    def test_legacy_observations_v1_get(self, mock_api_client, mock_requests):
        """Test getting a single observation."""
        mock_requests.request.return_value.json.return_value = {"id": "obs-1"}

        result = mock_api_client.legacy_observations_v1_get("obs-1")

        assert result == {"id": "obs-1"}

    def test_legacy_observations_v1_get_many(self, mock_api_client, mock_requests):
        """Test getting many observations."""
        mock_requests.request.return_value.json.return_value = {"observations": []}

        result = mock_api_client.legacy_observations_v1_get_many(
            page=1, limit=10, type="GENERATION"
        )

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["params"]["type"] == "GENERATION"


class TestLegacyScore:
    """Tests for legacy score API methods."""

    def test_legacy_score_v1_create(self, mock_api_client, mock_requests):
        """Test creating a score."""
        mock_requests.request.return_value.json.return_value = {"id": "score-1"}

        result = mock_api_client.legacy_score_v1_create({"value": 0.9})

        assert result == {"id": "score-1"}

    def test_legacy_score_v1_delete(self, mock_api_client, mock_requests):
        """Test deleting a score."""
        mock_requests.request.return_value.text = ""

        result = mock_api_client.legacy_score_v1_delete("score-1")

        assert result == {"success": True}


class TestLLMConnections:
    """Tests for LLM connections API methods."""

    def test_llm_connections_list(self, mock_api_client, mock_requests):
        """Test listing LLM connections."""
        mock_requests.request.return_value.json.return_value = {"connections": []}

        result = mock_api_client.llm_connections_list(page=1, limit=10)

        assert result == {"connections": []}

    def test_llm_connections_upsert(self, mock_api_client, mock_requests):
        """Test upserting LLM connection."""
        mock_requests.request.return_value.json.return_value = {"id": "conn-1"}

        result = mock_api_client.llm_connections_upsert({"provider": "openai"})

        assert result == {"id": "conn-1"}


class TestMedia:
    """Tests for media API methods."""

    def test_media_get(self, mock_api_client, mock_requests):
        """Test getting media."""
        mock_requests.request.return_value.json.return_value = {"id": "media-1"}

        result = mock_api_client.media_get("media-1")

        assert result == {"id": "media-1"}

    def test_media_patch(self, mock_api_client, mock_requests):
        """Test patching media."""
        mock_requests.request.return_value.json.return_value = {"id": "media-1"}

        result = mock_api_client.media_patch("media-1", {"metadata": {}})

        assert result == {"id": "media-1"}

    def test_media_get_upload_url(self, mock_api_client, mock_requests):
        """Test getting upload URL."""
        mock_requests.request.return_value.json.return_value = {"url": "https://..."}

        result = mock_api_client.media_get_upload_url({"filename": "test.jpg"})

        assert result == {"url": "https://..."}


class TestMetrics:
    """Tests for metrics API methods."""

    def test_metrics_metrics(self, mock_api_client, mock_requests):
        """Test metrics endpoint."""
        mock_requests.request.return_value.json.return_value = {"data": []}

        result = mock_api_client.metrics_metrics("test query")

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["params"]["query"] == "test query"


class TestModels:
    """Tests for models API methods."""

    def test_models_create(self, mock_api_client, mock_requests):
        """Test creating a model."""
        mock_requests.request.return_value.json.return_value = {"id": "model-1"}

        result = mock_api_client.models_create({"modelName": "test-model"})

        assert result == {"id": "model-1"}

    def test_models_list(self, mock_api_client, mock_requests):
        """Test listing models."""
        mock_requests.request.return_value.json.return_value = {"models": []}

        result = mock_api_client.models_list(page=1, limit=10)

        assert result == {"models": []}

    def test_models_get(self, mock_api_client, mock_requests):
        """Test getting a model."""
        mock_requests.request.return_value.json.return_value = {"id": "model-1"}

        result = mock_api_client.models_get("model-1")

        assert result == {"id": "model-1"}

    def test_models_delete(self, mock_api_client, mock_requests):
        """Test deleting a model."""
        mock_requests.request.return_value.text = ""

        result = mock_api_client.models_delete("model-1")

        assert result == {"success": True}


class TestObservations:
    """Tests for observations API methods."""

    def test_observations_get_many(self, mock_api_client, mock_requests):
        """Test getting many observations."""
        mock_requests.request.return_value.json.return_value = {"observations": []}

        result = mock_api_client.observations_get_many(
            fields="core,basic", limit=10, type="GENERATION"
        )

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["params"]["fields"] == "core,basic"
        assert call_kwargs["params"]["type"] == "GENERATION"


class TestOpenTelemetry:
    """Tests for OpenTelemetry API methods."""

    def test_opentelemetry_export_traces(self, mock_api_client, mock_requests):
        """Test exporting OpenTelemetry traces."""
        mock_requests.request.return_value.json.return_value = {"success": True}

        result = mock_api_client.opentelemetry_export_traces([{"span": "data"}])

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["json"]["resourceSpans"] == [{"span": "data"}]


class TestOrganizations:
    """Tests for organizations API methods."""

    def test_organizations_get_organization_memberships(
        self, mock_api_client, mock_requests
    ):
        """Test getting organization memberships."""
        mock_requests.request.return_value.json.return_value = {"memberships": []}

        result = mock_api_client.organizations_get_organization_memberships()

        assert result == {"memberships": []}

    def test_organizations_update_organization_membership(
        self, mock_api_client, mock_requests
    ):
        """Test updating organization membership."""
        mock_requests.request.return_value.json.return_value = {"id": "member-1"}

        result = mock_api_client.organizations_update_organization_membership(
            {"role": "admin"}
        )

        assert result == {"id": "member-1"}

    def test_organizations_delete_organization_membership(
        self, mock_api_client, mock_requests
    ):
        """Test deleting organization membership."""
        mock_requests.request.return_value.text = ""

        result = mock_api_client.organizations_delete_organization_membership(
            {"userId": "user-1"}
        )

        assert result == {"success": True}

    def test_organizations_get_project_memberships(
        self, mock_api_client, mock_requests
    ):
        """Test getting project memberships."""
        mock_requests.request.return_value.json.return_value = {"memberships": []}

        result = mock_api_client.organizations_get_project_memberships("project-1")

        assert result == {"memberships": []}

    def test_organizations_update_project_membership(
        self, mock_api_client, mock_requests
    ):
        """Test updating project membership."""
        mock_requests.request.return_value.json.return_value = {"id": "member-1"}

        result = mock_api_client.organizations_update_project_membership(
            "project-1", {"role": "admin"}
        )

        assert result == {"id": "member-1"}

    def test_organizations_delete_project_membership(
        self, mock_api_client, mock_requests
    ):
        """Test deleting project membership."""
        mock_requests.request.return_value.text = ""

        result = mock_api_client.organizations_delete_project_membership(
            "project-1", {"userId": "user-1"}
        )

        assert result == {"success": True}

    def test_organizations_get_organization_projects(
        self, mock_api_client, mock_requests
    ):
        """Test getting organization projects."""
        mock_requests.request.return_value.json.return_value = {"projects": []}

        result = mock_api_client.organizations_get_organization_projects()

        assert result == {"projects": []}

    def test_organizations_get_organization_api_keys(
        self, mock_api_client, mock_requests
    ):
        """Test getting organization API keys."""
        mock_requests.request.return_value.json.return_value = {"keys": []}

        result = mock_api_client.organizations_get_organization_api_keys()

        assert result == {"keys": []}


class TestProjects:
    """Tests for projects API methods."""

    def test_projects_get(self, mock_api_client, mock_requests):
        """Test getting project."""
        mock_requests.request.return_value.json.return_value = {"id": "project-1"}

        result = mock_api_client.projects_get()

        assert result == {"id": "project-1"}

    def test_projects_create(self, mock_api_client, mock_requests):
        """Test creating project."""
        mock_requests.request.return_value.json.return_value = {"id": "project-1"}

        result = mock_api_client.projects_create("test-project", 30, {"key": "value"})

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["json"]["name"] == "test-project"
        assert call_kwargs["json"]["retention"] == 30

    def test_projects_update(self, mock_api_client, mock_requests):
        """Test updating project."""
        mock_requests.request.return_value.json.return_value = {"id": "project-1"}

        result = mock_api_client.projects_update(
            "project-1", "updated-name", {"key": "value"}, 60
        )

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["json"]["name"] == "updated-name"

    def test_projects_delete(self, mock_api_client, mock_requests):
        """Test deleting project."""
        mock_requests.request.return_value.text = ""

        result = mock_api_client.projects_delete("project-1")

        assert result == {"success": True}

    def test_projects_get_api_keys(self, mock_api_client, mock_requests):
        """Test getting project API keys."""
        mock_requests.request.return_value.json.return_value = {"keys": []}

        result = mock_api_client.projects_get_api_keys("project-1")

        assert result == {"keys": []}

    def test_projects_create_api_key(self, mock_api_client, mock_requests):
        """Test creating project API key."""
        mock_requests.request.return_value.json.return_value = {"id": "key-1"}

        result = mock_api_client.projects_create_api_key("project-1", "test key")

        assert result == {"id": "key-1"}

    def test_projects_delete_api_key(self, mock_api_client, mock_requests):
        """Test deleting project API key."""
        mock_requests.request.return_value.text = ""

        result = mock_api_client.projects_delete_api_key("project-1", "key-1")

        assert result == {"success": True}


class TestPrompts:
    """Tests for prompts API methods."""

    def test_prompt_version_update(self, mock_api_client, mock_requests):
        """Test updating prompt version labels."""
        mock_requests.request.return_value.json.return_value = {"success": True}

        result = mock_api_client.prompt_version_update("test-prompt", 1, ["prod"])

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["json"]["newLabels"] == ["prod"]

    def test_prompts_get(self, mock_api_client, mock_requests):
        """Test getting a prompt."""
        mock_requests.request.return_value.json.return_value = {"name": "test-prompt"}

        result = mock_api_client.prompts_get("test-prompt", version=1, label="prod")

        assert result == {"name": "test-prompt"}

    def test_prompts_delete(self, mock_api_client, mock_requests):
        """Test deleting a prompt."""
        mock_requests.request.return_value.text = ""

        result = mock_api_client.prompts_delete("test-prompt", label="prod")

        assert result == {"success": True}

    def test_prompts_list(self, mock_api_client, mock_requests):
        """Test listing prompts."""
        mock_requests.request.return_value.json.return_value = {"prompts": []}

        result = mock_api_client.prompts_list(name="test-prompt", page=1, limit=10)

        assert result == {"prompts": []}

    def test_prompts_create(self, mock_api_client, mock_requests):
        """Test creating a prompt."""
        mock_requests.request.return_value.json.return_value = {"name": "test-prompt"}

        result = mock_api_client.prompts_create({"name": "test-prompt"})

        assert result == {"name": "test-prompt"}


class TestSCIM:
    """Tests for SCIM API methods."""

    def test_scim_get_service_provider_config(self, mock_api_client, mock_requests):
        """Test getting SCIM service provider config."""
        mock_requests.request.return_value.json.return_value = {"config": {}}

        result = mock_api_client.scim_get_service_provider_config()

        assert result == {"config": {}}

    def test_scim_get_resource_types(self, mock_api_client, mock_requests):
        """Test getting SCIM resource types."""
        mock_requests.request.return_value.json.return_value = {"types": []}

        result = mock_api_client.scim_get_resource_types()

        assert result == {"types": []}

    def test_scim_get_schemas(self, mock_api_client, mock_requests):
        """Test getting SCIM schemas."""
        mock_requests.request.return_value.json.return_value = {"schemas": []}

        result = mock_api_client.scim_get_schemas()

        assert result == {"schemas": []}

    def test_scim_list_users(self, mock_api_client, mock_requests):
        """Test listing SCIM users."""
        mock_requests.request.return_value.json.return_value = {"users": []}

        result = mock_api_client.scim_list_users(
            filter="userName eq 'test'", start_index=1, count=10
        )

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["params"]["filter"] == "userName eq 'test'"

    def test_scim_create_user(self, mock_api_client, mock_requests):
        """Test creating SCIM user."""
        mock_requests.request.return_value.json.return_value = {"id": "user-1"}

        result = mock_api_client.scim_create_user(
            "test@example.com", {"givenName": "Test"}
        )

        assert result == {"id": "user-1"}

    def test_scim_get_user(self, mock_api_client, mock_requests):
        """Test getting SCIM user."""
        mock_requests.request.return_value.json.return_value = {"id": "user-1"}

        result = mock_api_client.scim_get_user("user-1")

        assert result == {"id": "user-1"}

    def test_scim_delete_user(self, mock_api_client, mock_requests):
        """Test deleting SCIM user."""
        mock_requests.request.return_value.text = ""

        result = mock_api_client.scim_delete_user("user-1")

        assert result == {"success": True}


class TestScoreConfigs:
    """Tests for score configs API methods."""

    def test_score_configs_create(self, mock_api_client, mock_requests):
        """Test creating score config."""
        mock_requests.request.return_value.json.return_value = {"id": "config-1"}

        result = mock_api_client.score_configs_create({"name": "test-config"})

        assert result == {"id": "config-1"}

    def test_score_configs_get(self, mock_api_client, mock_requests):
        """Test getting score configs."""
        mock_requests.request.return_value.json.return_value = {"configs": []}

        result = mock_api_client.score_configs_get(page=1, limit=10)

        assert result == {"configs": []}

    def test_score_configs_get_by_id(self, mock_api_client, mock_requests):
        """Test getting score config by ID."""
        mock_requests.request.return_value.json.return_value = {"id": "config-1"}

        result = mock_api_client.score_configs_get_by_id("config-1")

        assert result == {"id": "config-1"}

    def test_score_configs_update(self, mock_api_client, mock_requests):
        """Test updating score config."""
        mock_requests.request.return_value.json.return_value = {"id": "config-1"}

        result = mock_api_client.score_configs_update("config-1", {"name": "updated"})

        assert result == {"id": "config-1"}


class TestScores:
    """Tests for scores API methods."""

    def test_scores_get_many(self, mock_api_client, mock_requests):
        """Test getting many scores."""
        mock_requests.request.return_value.json.return_value = {"scores": []}

        result = mock_api_client.scores_get_many(page=1, limit=10, name="test-score")

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["params"]["name"] == "test-score"

    def test_scores_get_by_id(self, mock_api_client, mock_requests):
        """Test getting score by ID."""
        mock_requests.request.return_value.json.return_value = {"id": "score-1"}

        result = mock_api_client.scores_get_by_id("score-1")

        assert result == {"id": "score-1"}


class TestSessions:
    """Tests for sessions API methods."""

    def test_sessions_list(self, mock_api_client, mock_requests):
        """Test listing sessions."""
        mock_requests.request.return_value.json.return_value = {"sessions": []}

        result = mock_api_client.sessions_list(page=1, limit=10)

        assert result == {"sessions": []}

    def test_sessions_get(self, mock_api_client, mock_requests):
        """Test getting a session."""
        mock_requests.request.return_value.json.return_value = {"id": "session-1"}

        result = mock_api_client.sessions_get("session-1")

        assert result == {"id": "session-1"}


class TestTraces:
    """Tests for traces API methods."""

    def test_trace_get(self, mock_api_client, mock_requests):
        """Test getting a trace."""
        mock_requests.request.return_value.json.return_value = {"id": "trace-1"}

        result = mock_api_client.trace_get("trace-1")

        assert result == {"id": "trace-1"}

    def test_trace_delete(self, mock_api_client, mock_requests):
        """Test deleting a trace."""
        mock_requests.request.return_value.text = ""

        result = mock_api_client.trace_delete("trace-1")

        assert result == {"success": True}

    def test_trace_list(self, mock_api_client, mock_requests):
        """Test listing traces."""
        mock_requests.request.return_value.json.return_value = {"traces": []}

        result = mock_api_client.trace_list(page=1, limit=10, user_id="user-1")

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["params"]["userId"] == "user-1"

    def test_trace_delete_multiple(self, mock_api_client, mock_requests):
        """Test deleting multiple traces."""
        mock_requests.request.return_value.text = ""

        result = mock_api_client.trace_delete_multiple(["trace-1", "trace-2"])

        call_kwargs = mock_requests.request.call_args[1]
        assert call_kwargs["json"]["traceIds"] == ["trace-1", "trace-2"]
