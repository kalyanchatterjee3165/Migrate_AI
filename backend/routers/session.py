import os
from fastapi import APIRouter, Request
from schemas.chat import StatusResponse, OutputFile

router = APIRouter()

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "./output")


@router.post("/reset")
async def reset(request: Request) -> dict:
    request.app.state.agent.reset()
    return {"status": "ok"}


@router.get("/status", response_model=StatusResponse)
async def status() -> StatusResponse:
    return StatusResponse(model="gpt-4o", connected=True)


@router.get("/output", response_model=list[OutputFile])
async def list_output_files() -> list[OutputFile]:
    files = []
    if os.path.isdir(OUTPUT_DIR):
        for name in os.listdir(OUTPUT_DIR):
            path = os.path.join(OUTPUT_DIR, name)
            if os.path.isfile(path):
                files.append(OutputFile(
                    filename=name,
                    path=path,
                    size_bytes=os.path.getsize(path),
                ))
    return files
