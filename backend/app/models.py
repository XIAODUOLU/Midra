from __future__ import annotations

from pydantic import BaseModel


class CreateTaskRequest(BaseModel):
    prompt: str


class RetryTaskRequest(BaseModel):
    pass

