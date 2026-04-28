"""Tests for langfuse_models.py - Pydantic models."""

import pytest
from pydantic import ValidationError

from langfuse_agent.langfuse_models import LangfuseProjectConfig, AnnotationQueue


class TestLangfuseProjectConfig:
    """Tests for LangfuseProjectConfig model."""

    def test_langfuse_project_config_valid(self):
        """Test creating a valid LangfuseProjectConfig."""
        config = LangfuseProjectConfig(
            public_key="test_public_key",
            secret_key="test_secret_key",
            host="https://test.langfuse.com",
        )

        assert config.public_key == "test_public_key"
        assert config.secret_key == "test_secret_key"
        assert config.host == "https://test.langfuse.com"

    def test_langfuse_project_config_missing_field(self):
        """Test that missing required fields raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            LangfuseProjectConfig(
                public_key="test_public_key",
                secret_key="test_secret_key",
                # Missing host
            )

        assert "host" in str(exc_info.value).lower()

    def test_langfuse_project_config_from_dict(self):
        """Test creating LangfuseProjectConfig from dictionary."""
        data = {
            "public_key": "test_public_key",
            "secret_key": "test_secret_key",
            "host": "https://test.langfuse.com",
        }

        config = LangfuseProjectConfig(**data)

        assert config.public_key == "test_public_key"
        assert config.secret_key == "test_secret_key"
        assert config.host == "https://test.langfuse.com"

    def test_langfuse_project_config_serialization(self):
        """Test serializing LangfuseProjectConfig to dict."""
        config = LangfuseProjectConfig(
            public_key="test_public_key",
            secret_key="test_secret_key",
            host="https://test.langfuse.com",
        )

        data = config.model_dump()

        assert data["public_key"] == "test_public_key"
        assert data["secret_key"] == "test_secret_key"
        assert data["host"] == "https://test.langfuse.com"

    def test_langfuse_project_config_json_serialization(self):
        """Test serializing LangfuseProjectConfig to JSON."""
        config = LangfuseProjectConfig(
            public_key="test_public_key",
            secret_key="test_secret_key",
            host="https://test.langfuse.com",
        )

        json_str = config.model_dump_json()

        assert "test_public_key" in json_str
        assert "test_secret_key" in json_str
        assert "https://test.langfuse.com" in json_str


class TestAnnotationQueue:
    """Tests for AnnotationQueue model."""

    def test_annotation_queue_valid(self):
        """Test creating a valid AnnotationQueue."""
        queue = AnnotationQueue(
            id="queue-123",
            name="Test Queue",
            description="A test queue",
            createdAt="2024-01-01T00:00:00Z",
            updatedAt="2024-01-01T00:00:00Z",
        )

        assert queue.id == "queue-123"
        assert queue.name == "Test Queue"
        assert queue.description == "A test queue"
        assert queue.createdAt == "2024-01-01T00:00:00Z"
        assert queue.updatedAt == "2024-01-01T00:00:00Z"

    def test_annotation_queue_without_description(self):
        """Test creating AnnotationQueue without optional description."""
        queue = AnnotationQueue(
            id="queue-123",
            name="Test Queue",
            createdAt="2024-01-01T00:00:00Z",
            updatedAt="2024-01-01T00:00:00Z",
        )

        assert queue.description is None

    def test_annotation_queue_missing_required_field(self):
        """Test that missing required fields raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            AnnotationQueue(
                id="queue-123",
                name="Test Queue",
                # Missing createdAt and updatedAt
            )

        assert (
            "createdAt" in str(exc_info.value).lower()
            or "updatedat" in str(exc_info.value).lower()
        )

    def test_annotation_queue_from_dict(self):
        """Test creating AnnotationQueue from dictionary."""
        data = {
            "id": "queue-123",
            "name": "Test Queue",
            "description": "A test queue",
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:00:00Z",
        }

        queue = AnnotationQueue(**data)

        assert queue.id == "queue-123"
        assert queue.name == "Test Queue"

    def test_annotation_queue_serialization(self):
        """Test serializing AnnotationQueue to dict."""
        queue = AnnotationQueue(
            id="queue-123",
            name="Test Queue",
            description="A test queue",
            createdAt="2024-01-01T00:00:00Z",
            updatedAt="2024-01-01T00:00:00Z",
        )

        data = queue.model_dump()

        assert data["id"] == "queue-123"
        assert data["name"] == "Test Queue"
        assert data["description"] == "A test queue"

    def test_annotation_queue_json_serialization(self):
        """Test serializing AnnotationQueue to JSON."""
        queue = AnnotationQueue(
            id="queue-123",
            name="Test Queue",
            createdAt="2024-01-01T00:00:00Z",
            updatedAt="2024-01-01T00:00:00Z",
        )

        json_str = queue.model_dump_json()

        assert "queue-123" in json_str
        assert "Test Queue" in json_str
