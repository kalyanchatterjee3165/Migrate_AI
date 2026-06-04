from fastapi import APIRouter, Request
from schemas.chat import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: Request, body: ChatRequest) -> ChatResponse:
    """
    Send a message to the MigrateAI agent.
    Each session_id has isolated conversation history.
    """
    sm = request.app.state.session_manager
    agent = sm.get_agent(body.session_id)
    reply = agent.chat(body.message)
    return ChatResponse(reply=reply, session_id=body.session_id)
