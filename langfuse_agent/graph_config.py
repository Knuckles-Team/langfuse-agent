import os
from pydantic import BaseModel, ConfigDict
from agent_utilities.base_utilities import to_boolean

class GraphConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    mcp_url: str | None = None
    mcp_config: str | None = None
    custom_skills_directory: str | None = None

TAG_PROMPTS: dict[str, str] = {
    "telemetry": "You are a Langfuse Telemetry specialist. Evaluate metrics and traces.",
    "annotation": "You are an Annotation specialist for LLMs. Get and manage annotation queues in Langfuse.",
}

TAG_ENV_VARS: dict[str, str] = {
    "telemetry": "TELEMETRYTOOL",
    "annotation": "ANNOTATIONTOOL",
}

def get_sys_prompt(raw_query: str) -> str:
    active_prompts = []
    has_active_tags = False

    for tag, env_var in TAG_ENV_VARS.items():
        if to_boolean(os.getenv(env_var, "True")):
            has_active_tags = True
            if tag in TAG_PROMPTS:
                active_prompts.append(TAG_PROMPTS[tag])

                                                        
    if not active_prompts and has_active_tags:
        active_prompts.append("You are a Langfuse Observability Agent specialist.")

    domain_sys_prompt = " ".join(active_prompts)

    return f"""
You are the Langfuse Agent, a specialized AI assistant designed to manage LLM observability in Langfuse.
{domain_sys_prompt}

Your task is to answer the following query:
{raw_query}
"""
