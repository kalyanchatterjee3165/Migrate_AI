from fastapi import APIRouter, Request
from schemas.chat import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: Request, body: ChatRequest) -> ChatResponse:
    agent = request.app.state.agent
    reply = agent.chat(body.message)
    return ChatResponse(reply=reply)
