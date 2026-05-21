"""Tests for __main__.py - Package entry point."""


class TestMainModule:
    """Tests for __main__ module."""

    def test_main_imports_agent_server(self):
        """Test that __main__ imports agent_server."""
        from langfuse_agent import __main__

        assert hasattr(__main__, "agent_server")

    def test_main_has_agent_server_function(self):
        """Test that agent_server function is available."""
        from langfuse_agent.__main__ import agent_server

        assert callable(agent_server)

    def test_main_module_execution(self):
        """Test that __main__ module can be imported and has the expected structure."""
        # This test verifies the __main__ module structure without actually executing it
        # because execution requires optional dependencies (playwright) that may not be installed
        from langfuse_agent import __main__

        # Verify the module has the expected function
        assert hasattr(__main__, "agent_server")
        assert callable(__main__.agent_server)
