from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    reply: str
    session_id: str


class ResetRequest(BaseModel):
    session_id: str = "default"


class ResetResponse(BaseModel):
    status: str
    session_id: str


class StatusResponse(BaseModel):
    model: str
    connected: bool
    active_sessions: int
    version: str = "1.0.0"


class OutputFile(BaseModel):
    filename: str
    path: str
    size_bytes: int
    created_at: str


class OutputListResponse(BaseModel):
    files: List[OutputFile]
    count: int


class MigrationRequest(BaseModel):
    migration_type: str
    config: dict
    session_id: str = "default"


class MigrationResponse(BaseModel):
    status: str
    rows_read: int
    rows_written: int
    source: str
    destination: str
    output_path: str
    pre_check_passed: bool
    post_check_passed: bool
    columns: List[str]
    error: Optional[str] = None
