import os
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------------
# LLM provider — change these three to switch between any
# OpenAI-compatible provider (OpenAI, Gemini, Groq, Ollama, …)
# ------------------------------------------------------------------

import json as _json

LLM_API_KEY  = os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY", "")
LLM_BASE_URL = os.environ.get("LLM_BASE_URL") or None
LLM_MODEL    = (
    os.environ.get("LLM_MODEL")
    or os.environ.get("OPENAI_MODEL")
    or "gpt-4o"
)

# Optional extra headers sent on every LLM request.
# Set as a JSON object in .env, e.g.:
#   LLM_EXTRA_HEADERS={"use-case": "data-migration", "x-team": "platform"}
_raw_headers  = os.environ.get("LLM_EXTRA_HEADERS", "")
LLM_EXTRA_HEADERS: dict = _json.loads(_raw_headers) if _raw_headers.strip() else {}

# ------------------------------------------------------------------
# App / output settings
# ------------------------------------------------------------------

OUTPUT_DIR   = os.environ.get("OUTPUT_DIR", "./output")
LOG_LEVEL    = os.environ.get("LOG_LEVEL", "INFO")
APP_USERNAME = os.environ.get("APP_USERNAME", "admin")
APP_PASSWORD = os.environ.get("APP_PASSWORD", "")

if not LLM_API_KEY:
    raise EnvironmentError(
        "No API key found. Set LLM_API_KEY in your .env file.\n"
        "  OpenAI:  LLM_API_KEY=sk-...\n"
        "  Gemini:  LLM_API_KEY=<google-ai-studio-key>\n"
        "  Other:   LLM_API_KEY=<your-provider-key>"
    )