# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2026-07-17

### Fixed
- Enforce a closed, metadata-only projection for governed GraphOS trace
  certification so connector results and automatic ingestion cannot expose
  trace input, output, or free-form metadata.

## [1.0.2] - 2026-07-15

### Added
- Governed connector metadata, ontology/SHACL assets, mappings, migrations,
  schema fingerprints, and privacy-safe certification fixtures.
- One comprehensive `langfuse-agent-operations` skill; specialized prompt,
  dataset, and trace procedures remain explicit workflows without duplicating
  activation guidance.

### Changed
- Require the current Agent Utilities 1.27 runtime and its full Epistemic Graph
  authority for MCP and agent deployments.
- Consume endpoint, credential-reference, proxy, and TLS inputs only through
  runtime configuration; distributable assets contain no environment profile.

### Fixed
- Harden MCP ingestion, API verification, configuration sanitization, and
  privacy boundaries so runtime paths, credentials, and local identity are not
  materialized into connector records or documentation.

## [0.1.7] - 2026-04-29

### Added
- Initial release
