from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


class StatusResponse(BaseModel):
    model: str
    connected: bool


class OutputFile(BaseModel):
    filename: str
    path: str
    size_bytes: int
