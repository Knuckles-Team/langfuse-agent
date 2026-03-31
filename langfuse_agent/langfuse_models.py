from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class LangfuseProjectConfig(BaseModel):
    public_key: str
    secret_key: str
    host: str

class AnnotationQueue(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    createdAt: str
    updatedAt: str
