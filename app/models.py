from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional

class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = Field(..., description="Service version")

class Finding(BaseModel):
    source: str
    path: str
    line: Optional[int] = None
    issue: str
    severity: str = Field(default="info", pattern="^(info|low|medium|high)$")
    detail: Optional[str] = None

class ScanResponse(BaseModel):
    findings: List[Finding]

class ScanRequest(BaseModel):
    text: Optional[str] = None
    filename: Optional[str] = None

class ChatRequest(BaseModel):
    prompt: str
    context: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
