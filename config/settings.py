import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL   = os.environ.get("OPENAI_MODEL", "gpt-4o")
OUTPUT_DIR     = os.environ.get("OUTPUT_DIR", "./output")
LOG_LEVEL      = os.environ.get("LOG_LEVEL", "INFO")

APP_USERNAME   = os.environ.get("APP_USERNAME", "admin")
APP_PASSWORD   = os.environ.get("APP_PASSWORD", "")

if not OPENAI_API_KEY:
    raise EnvironmentError(
        "OPENAI_API_KEY is not set. Add it to your .env file."
    )