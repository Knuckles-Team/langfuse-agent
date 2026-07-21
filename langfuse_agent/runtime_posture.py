"""Privacy-safe runtime posture shared by Langfuse tool surfaces."""

from agent_utilities.core.config import setting


def observability_runtime_posture() -> dict[str, bool]:
    """Return only the effective content-retention posture."""

    value = str(setting("LANGFUSE_CAPTURE_CONTENT", "false") or "false").casefold()
    if value in {"1", "true", "yes", "on"}:
        enabled = True
    elif value in {"0", "false", "no", "off"}:
        enabled = False
    else:
        raise ValueError("langfuse_capture_content_invalid")
    return {"content_capture_enabled": enabled, "metadata_only": not enabled}


__all__ = ["observability_runtime_posture"]
