import os
from datetime import datetime
from fastapi import APIRouter, Request
from schemas.chat import (
    ResetRequest, ResetResponse,
    StatusResponse, OutputFile, OutputListResponse,
)

router = APIRouter()

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "./output")


@router.post("/reset", response_model=ResetResponse)
async def reset(request: Request, body: ResetRequest) -> ResetResponse:
    """Clear conversation history for a session."""
    sm = request.app.state.session_manager
    sm.reset_session(body.session_id)
    return ResetResponse(status="ok", session_id=body.session_id)


@router.get("/status", response_model=StatusResponse)
async def status(request: Request) -> StatusResponse:
    """Health check — returns model info and active session count."""
    sm = request.app.state.session_manager
    return StatusResponse(
        model="gpt-4o",
        connected=True,
        active_sessions=sm.active_count(),
    )


@router.get("/output", response_model=OutputListResponse)
async def list_output(request: Request) -> OutputListResponse:
    """List all files in the output directory."""
    files = []
    if os.path.isdir(OUTPUT_DIR):
        for fname in os.listdir(OUTPUT_DIR):
            fpath = os.path.join(OUTPUT_DIR, fname)
            if os.path.isfile(fpath):
                stat = os.stat(fpath)
                files.append(OutputFile(
                    filename=fname,
                    path=f"/files/{fname}",
                    size_bytes=stat.st_size,
                    created_at=datetime.fromtimestamp(stat.st_ctime).isoformat(),
                ))
    return OutputListResponse(files=files, count=len(files))


@router.delete("/session/{session_id}")
async def delete_session(session_id: str, request: Request):
    """Completely remove a session and free its memory."""
    sm = request.app.state.session_manager
    sm.delete_session(session_id)
    return {"status": "deleted", "session_id": session_id}


@router.get("/sessions")
async def list_sessions(request: Request):
    """List all active session IDs."""
    sm = request.app.state.session_manager
    return {
        "sessions": sm.list_sessions(),
        "count":    sm.active_count(),
    }
