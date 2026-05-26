#!/usr/bin/env python
from langfuse_agent.api.api_client_annotation_queues import Api as AnnotationQueuesApi
from langfuse_agent.api.api_client_datasets import Api as DatasetsApi
from langfuse_agent.api.api_client_management import Api as ManagementApi
from langfuse_agent.api.api_client_observability import Api as ObservabilityApi
from langfuse_agent.api.api_client_prompts_models import Api as PromptsModelsApi


class LangfuseApi(
    AnnotationQueuesApi,
    DatasetsApi,
    ManagementApi,
    ObservabilityApi,
    PromptsModelsApi,
):
    pass
