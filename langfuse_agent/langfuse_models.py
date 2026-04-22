from pydantic import BaseModel


class LangfuseProjectConfig(BaseModel):
    public_key: str
    secret_key: str
    host: str


class AnnotationQueue(BaseModel):
    id: str
    name: str
    description: str | None = None
    createdAt: str
    updatedAt: str
