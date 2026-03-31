import os
from langfuse import Langfuse

_client = None

def get_client() -> Langfuse:
    global _client
    if _client is None:
        host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
        public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "")
        secret_key = os.getenv("LANGFUSE_SECRET_KEY", "")
        _client = Langfuse(public_key=public_key, secret_key=secret_key, host=host)
    return _client
