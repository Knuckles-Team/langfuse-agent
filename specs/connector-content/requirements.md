# CONN-LANGFUSE-AGENT-CONNECTOR-CONTENT — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. A row names the file it touches and the test that proves it. The generator sets each row's state in `status.json`.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-LANGFUSE-AGENT-CONNECTOR-CONTENT-R001` | **Default content.** `pyproject.toml` declares `langfuse-mcp` as the single `scion_sdk.connector` entry point. The server lists the packaged `skill://` and `ontology://` resources and the packaged prompts with no `content=` argument. Proving test: `tests/test_default_content_surfaces.py`. Caller chain: the `langfuse-mcp = scion_sdk.cli:serve` console script in `pyproject.toml` -> `scion_sdk.connector` entry point `langfuse_agent:connector` (`langfuse_agent/__init__.py` line 101) -> SDK-built server serving the packaged `langfuse_agent/skills`, `prompts` and `ontology` content. Shape: the content is the packaged directories `langfuse_agent/skills/`, `langfuse_agent/prompts/` and `langfuse_agent/ontology/`; add the test by copying `tests/test_default_content_surfaces.py` of immich-api (`fastmcp.Client` listing resources and prompts), building the server as `tests/test_api_parity_gate.py` does with `scion_sdk.connector.build_server`. The pack extends only the core ontology: it redeclares no class or property the core already declares and carries no pre-rename IRI base. | `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. Planned test: `tests/test_default_content_surfaces.py::test_default_content_surfaces`. Also: `tests/test_ontology_one_schema.py::test_pack_declares_no_core_owned_term`. |
