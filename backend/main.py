from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# Load .env from project root before any config import
load_dotenv(find_dotenv(usecwd=False))

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import chat, session, migrations
from middleware.session_manager import session_manager

app = FastAPI(
    title="MigrateAI API",
    description="Conversational data migration backend",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8501",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
app.mount("/files", StaticFiles(directory=str(OUTPUT_DIR)), name="files")

app.include_router(chat.router,       prefix="/api")
app.include_router(session.router,    prefix="/api")
app.include_router(migrations.router, prefix="/api")


@app.on_event("startup")
async def startup():
    app.state.session_manager = session_manager
    print("MigrateAI backend started")
    print("Docs: http://localhost:8000/docs")


@app.get("/")
async def root():
    return {
        "name":    "MigrateAI API",
        "version": "1.0.0",
        "status":  "running",
        "docs":    "/docs",
    }
