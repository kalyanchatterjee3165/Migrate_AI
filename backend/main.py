from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# Load .env from project root before any config import
load_dotenv(find_dotenv(usecwd=False))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import chat as chat_router
from routers import session as session_router
from llm.agent import MigrationAgent
from llm.tool_registry import build_default_registry
from migrations.executor import (
    migrate_postgres_to_bigquery,
    migrate_csv_to_sqlite,
    migrate_s3_to_snowflake,
    migrate_mongo_to_s3,
)

app = FastAPI(title="migrate.ai", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router.router, prefix="/api")
app.include_router(session_router.router, prefix="/api")

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
app.mount("/files", StaticFiles(directory=str(OUTPUT_DIR)), name="files")


@app.on_event("startup")
async def startup():
    registry = build_default_registry(
        migrate_pg_to_bq=migrate_postgres_to_bigquery,
        migrate_csv_to_sqlite=migrate_csv_to_sqlite,
        migrate_s3_to_sf=migrate_s3_to_snowflake,
        migrate_mongo_to_s3=migrate_mongo_to_s3,
    )
    app.state.agent = MigrationAgent(registry=registry)
