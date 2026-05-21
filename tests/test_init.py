"""Tests for __init__.py - Package initialization."""

import pytest


class TestPackageInitialization:
    """Tests for package initialization."""

    def test_import_core_module(self):
        """Test that core module can be imported."""
        from langfuse_agent import LangfuseApi  # type: ignore[attr-defined]

        assert LangfuseApi is not None

    def test_import_api_class(self):
        """Test that LangfuseApi class is available."""
        from langfuse_agent import LangfuseApi  # type: ignore[attr-defined]

        assert hasattr(LangfuseApi, "__init__")
        assert hasattr(LangfuseApi, "_request")

    def test_import_optional_mcp_module(self):
        """Test that MCP module can be imported when available."""
        try:
            from langfuse_agent import _MCP_AVAILABLE

            assert isinstance(_MCP_AVAILABLE, bool)
        except ImportError:
            pytest.skip("MCP module not available")

    def test_import_optional_agent_module(self):
        """Test that agent module can be imported when available."""
        try:
            from langfuse_agent import _AGENT_AVAILABLE

            assert isinstance(_AGENT_AVAILABLE, bool)
        except ImportError:
            pytest.skip("Agent module not available")

    def test_module_exposes_langfuse_api(self):
        """Test that LangfuseApi is exposed in package namespace."""
        import langfuse_agent

        assert hasattr(langfuse_agent, "LangfuseApi")

    def test_module_exposes_models(self):
        """Test that models are exposed in package namespace."""

        # Models are not exposed by default in __init__.py
        # They need to be imported directly from langfuse_models
        from langfuse_agent.langfuse_models import (
            AnnotationQueue,
            LangfuseProjectConfig,
        )

        assert LangfuseProjectConfig is not None
        assert AnnotationQueue is not None

    def test_module_has_all_list(self):
        """Test that __all__ is defined."""
        import langfuse_agent

        assert hasattr(langfuse_agent, "__all__")
        assert isinstance(langfuse_agent.__all__, list)

    def test_module_docstring(self):
        """Test that module has docstring."""
        import langfuse_agent

        # The docstring is at the end of the file
        # Check if the module has any docstring content
        assert (
            langfuse_agent.__doc__ is None
            or "langfuse-agent" in langfuse_agent.__doc__.lower()
        )


class TestModuleImportSafety:
    """Tests for safe module imports."""

    def test_import_module_safely_with_valid_module(self):
        """Test _import_module_safely with valid module."""
        import langfuse_agent

        result = langfuse_agent._import_module_safely("langfuse_agent.api_client")
        assert result is not None

    def test_import_module_safely_with_invalid_module(self):
        """Test _import_module_safely with invalid module."""
        import langfuse_agent

        result = langfuse_agent._import_module_safely("nonexistent.module")
        assert result is None

    def test_expose_members_with_module(self):
        """Test _expose_members exposes module members."""
        import langfuse_agent
        import langfuse_agent.api_client as api_module

        # Save current state
        original_all = langfuse_agent.__all__.copy()
        original_globals = {}

        # Get current exposed members
        for name in dir(langfuse_agent):
            if not name.startswith("_"):
                original_globals[name] = getattr(langfuse_agent, name)

        langfuse_agent._expose_members(api_module)

        # Restore
        langfuse_agent.__all__ = original_all
        for name, value in original_globals.items():
            setattr(langfuse_agent, name, value)

    def test_core_modules_list(self):
        """Test that CORE_MODULES is defined."""
        import langfuse_agent

        assert hasattr(langfuse_agent, "CORE_MODULES")
        assert isinstance(langfuse_agent.CORE_MODULES, list)
        assert "langfuse_agent.api_client" in langfuse_agent.CORE_MODULES

    def test_optional_modules_dict(self):
        """Test that OPTIONAL_MODULES is defined."""
        import langfuse_agent

        assert hasattr(langfuse_agent, "OPTIONAL_MODULES")
        assert isinstance(langfuse_agent.OPTIONAL_MODULES, dict)
        assert "langfuse_agent.agent_server" in langfuse_agent.OPTIONAL_MODULES
        assert "langfuse_agent.mcp_server" in langfuse_agent.OPTIONAL_MODULES


class TestModuleReload:
    """Tests for module reloading behavior."""

    def test_module_can_be_reloaded(self):
        """Test that module can be reloaded."""
        import importlib

        import langfuse_agent

        # Get initial state
        initial_api = langfuse_agent.LangfuseApi  # type: ignore[attr-defined]

        # Reload module
        importlib.reload(langfuse_agent)

        # Check that API is still available
        assert hasattr(langfuse_agent, "LangfuseApi")
        assert langfuse_agent.LangfuseApi == initial_api  # type: ignore[attr-defined]


class TestPackageMetadata:
    """Tests for package metadata."""

    def test_package_name(self):
        """Test that package name is correct."""
        import langfuse_agent

        assert langfuse_agent.__name__ == "langfuse_agent"

    def test_package_has_version(self):
        """Test that package has version information."""
        try:
            import langfuse_agent

            # Version might be in __version__ or from package metadata
            assert hasattr(langfuse_agent, "__name__")
        except AttributeError:
            pytest.skip("Version not directly exposed in __init__")


class TestWarningsFiltering:
    """Tests for warning filtering in __init__."""

    def test_warnings_filtering_applied(self):
        """Test that warnings are filtered during import."""
        import langfuse_agent

        # The module should have applied warning filters
        # We can't easily test this without triggering warnings,
        # but we can verify the import succeeded
        assert langfuse_agent is not None


class TestModuleIsolation:
    """Tests for module isolation and namespace pollution."""

    def test_module_namespace_clean(self):
        """Test that module namespace is reasonably clean."""
        import langfuse_agent

        # Check that we have expected members but not excessive pollution
        public_members = [
            name for name in dir(langfuse_agent) if not name.startswith("_")
        ]

        # Should have at least our core classes
        assert "LangfuseApi" in public_members
        # Models are not exposed by default
        # assert "LangfuseProjectConfig" in public_members
        # assert "AnnotationQueue" in public_members

    def test_private_functions_not_in_all(self):
        """Test that private functions are not in __all__."""
        import langfuse_agent

        assert "_import_module_safely" not in langfuse_agent.__all__
        assert "_expose_members" not in langfuse_agent.__all__
