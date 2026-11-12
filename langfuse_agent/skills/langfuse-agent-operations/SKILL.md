---
name: langfuse-agent-operations
skill_type: skill
description: >-
  Operate langfuse-agent through its governed MCP and Arbora capabilities, including langfuse eval datasets, langfuse prompt management, langfuse trace analytics. Use when a request requires this provider's read, change, automation, ingestion, troubleshooting, or evidence workflows.
---

# Langfuse Agent Operations

Use the provider's governed MCP tools through Arbora delegation.

## Workflow

1. Establish the verified GraphSession and tenant before discovery or retrieval.
2. Discover the current tool surface; never assume a stale tool name or schema.
3. Prefer read-only inspection first. For changes, present impact and use the provider's
   dry-run or preview mode when available.
4. Execute mutations as fenced WorkItems so retries remain idempotent and auditable.
5. Ingest source data only through the signed connector preset and ChangeEnvelope path.
6. Verify the durable result and its trace/evidence before reporting completion.

## Safety contract

- Never persist credentials, endpoints, raw personal identifiers, hostnames, or local paths.
- Resolve TLS trust and verification from environment/configuration; never hardcode bypasses.
- Treat unknown ACL, tenant, schema, or tool-contract state as a hard failure.
- Require explicit approval for destructive, externally visible, or irreversible actions.
- Keep runtime traces policy-scoped and privacy-sanitized.

## Specialized workflows

Read [the workflow catalog](references/catalog.md) only when the request needs a
provider-specific procedure, parameter map, script, or reference asset.

## Tools by task

Every served tool is named below under the task it serves. Pass each argument by name.

- **analyze-traces**: Find traces by user, session or name and read their observations, sessions and metrics. `langfuse_comments_create`, `langfuse_comments_get`, `langfuse_comments_get_by_id`, `langfuse_metrics_get`, `langfuse_observations_get_many`, `langfuse_sessions_list`, `langfuse_sessions_get`, `langfuse_trace_get`, `langfuse_trace_list`
- **export-and-store-trace-media**: Export OpenTelemetry spans and handle trace media uploads. `langfuse_opentelemetry_export_traces`, `langfuse_media_get`, `langfuse_media_patch`, `langfuse_media_get_upload_url`
- **delete-traces**: Delete one trace or a batch of traces after confirming the ids. `langfuse_trace_delete`, `langfuse_trace_delete_multiple`
- **score-and-configure-evaluations**: Define score configurations and read and write scores. `langfuse_scores_create`, `langfuse_score_configs_create`, `langfuse_score_configs_get`, `langfuse_score_configs_get_by_id`, `langfuse_score_configs_update`, `langfuse_scores_get_many`
- **curate-eval-datasets**: Create datasets, add items and read or delete dataset runs. `langfuse_dataset_items_create`, `langfuse_dataset_items_list`, `langfuse_dataset_items_get`, `langfuse_dataset_items_delete`, `langfuse_dataset_run_items_create`, `langfuse_dataset_run_items_list`, `langfuse_datasets_list`, `langfuse_datasets_create`, `langfuse_datasets_get`, `langfuse_datasets_get_run`, `langfuse_datasets_delete_run`, `langfuse_datasets_get_runs`
- **run-annotation-queue**: Create an annotation queue, add and update its items and assign reviewers. `langfuse_annotation_queues_list_queues`, `langfuse_annotation_queues_create_queue`, `langfuse_annotation_queues_get_queue`, `langfuse_annotation_queues_list_queue_items`, `langfuse_annotation_queues_create_queue_item`, `langfuse_annotation_queues_get_queue_item`, `langfuse_annotation_queues_update_queue_item`, `langfuse_annotation_queues_delete_queue_item`, `langfuse_annotation_queues_create_queue_assignment`, `langfuse_annotation_queues_delete_queue_assignment`
- **manage-prompts**: List, read, create and relabel versioned prompts. `langfuse_prompt_version_update`, `langfuse_prompts_get`, `langfuse_prompts_delete`, `langfuse_prompts_list`, `langfuse_prompts_create`
- **manage-models-and-llm-connections**: Maintain the model pricing definitions and the LLM connections. `langfuse_llm_connections_list`, `langfuse_llm_connections_upsert`, `langfuse_models_create`, `langfuse_models_list`, `langfuse_models_get`, `langfuse_models_delete`
- **administer-projects**: Manage projects, their API keys and blob storage integrations and check service health. `langfuse_blob_storage_integrations_get_blob_storage_integrations`, `langfuse_blob_storage_integrations_upsert_blob_storage_integration`, `langfuse_blob_storage_integrations_get_blob_storage_integration_status`, `langfuse_blob_storage_integrations_delete_blob_storage_integration`, `langfuse_health_health`, `langfuse_projects_get`, `langfuse_projects_create`, `langfuse_projects_update`, `langfuse_projects_delete`, `langfuse_projects_get_api_keys`, `langfuse_projects_create_api_key`, `langfuse_projects_delete_api_key`, `langfuse_runtime_posture`
- **administer-organization-access**: Manage organization and project memberships and SCIM users. `langfuse_organizations_get_organization_memberships`, `langfuse_organizations_update_organization_membership`, `langfuse_organizations_delete_organization_membership`, `langfuse_organizations_get_project_memberships`, `langfuse_organizations_update_project_membership`, `langfuse_organizations_delete_project_membership`, `langfuse_organizations_get_organization_projects`, `langfuse_organizations_get_organization_api_keys`, `langfuse_scim_get_service_provider_config`, `langfuse_scim_get_resource_types`, `langfuse_scim_get_schemas`, `langfuse_scim_list_users`, `langfuse_scim_create_user`, `langfuse_scim_get_user`, `langfuse_scim_delete_user`
- **ingest-trace-records**: Push traces, observations, sessions and scores into the knowledge graph. `langfuse_ingest`
