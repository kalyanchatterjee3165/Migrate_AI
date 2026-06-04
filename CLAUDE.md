# migrate.ai — Claude Code Project Guide

## What This Project Is

A conversational data migration tool powered by an LLM agent.
Users chat naturally to describe their source and destination, the agent
collects required config through conversation, then calls the right migration
tool to execute the job.

This is a **POC** — all data movement is simulated with Faker-generated data.
No real databases or cloud services are connected.

---

## Branches

| Branch          | Frontend         | Run command                               |
|-----------------|------------------|-------------------------------------------|
| `fastapi-react` | React + FastAPI  | see **How to Run** below ← active branch  |
| `main`          | Gradio           | `python app.py`                           |
| `streamlit`     | Streamlit        | `streamlit run streamlit_app.py`          |

Backend logic (LLM agent, tools, migrations) is identical across all branches.

---

## Stack

- **LLM**: Any OpenAI-compatible API — configured via `.env` (OpenAI, Gemini, Groq, Ollama…)
- **Backend**: FastAPI + Uvicorn (`backend/main.py`)
- **Frontend**: React 18 + Vite, plain CSS with token variables (no Tailwind, no CSS-in-JS)
- **Markdown rendering**: `react-markdown` (chat bubbles)
- **Icons**: `lucide-react`
- **Data generation**: `faker`, `pandas`
- **Database**: `sqlalchemy` (SQLite destination)
- **Python**: 3.11+  |  **Node**: 18+

---

## Project Structure

```
migrate-ai/
├── .env.example                  # copy to .env and fill in values
├── docker-compose.yml            # runs backend + frontend together
├── CLAUDE.md                     # You are here
│
├── backend/                      # FastAPI server
│   ├── main.py                   # FastAPI app entry point — run this
│   ├── requirements.txt
│   ├── Dockerfile
│   │
│   ├── config/
│   │   └── settings.py           # loads .env — LLM_*, OUTPUT_DIR, LOG_LEVEL
│   │
│   ├── routers/
│   │   ├── chat.py               # POST /api/chat
│   │   ├── session.py            # POST /api/reset · GET /api/status · GET /api/output
│   │   └── migrations.py         # POST /api/migrate · GET /api/migrate/types
│   │
│   ├── schemas/
│   │   └── chat.py               # Pydantic models: ChatRequest, ChatResponse, …
│   │
│   ├── middleware/
│   │   └── session_manager.py    # Thread-safe per-session MigrationAgent registry
│   │
│   ├── llm/
│   │   ├── agent.py              # MigrationAgent — chat loop + tool dispatch
│   │   ├── prompts.py            # SYSTEM_PROMPT
│   │   └── tool_registry.py      # ToolRegistry + OpenAI-format tool schemas
│   │
│   ├── tools/
│   │   ├── base.py               # BaseTool interface
│   │   ├── generators/           # Faker-based DataFrame generation
│   │   ├── sources/              # Fake Postgres, CSV, S3, MongoDB reads
│   │   └── destinations/         # Fake BigQuery, SQLite, S3, Snowflake writes
│   │
│   ├── migrations/
│   │   ├── executor.py           # Wires source.read() → dest.write()
│   │   └── validator.py          # Fake pre/post row count + schema checks
│   │
│   ├── session/
│   │   └── state.py              # Per-conversation config state
│   │
│   └── output/                   # Simulated migration output files land here
│
└── frontend/                     # React + Vite UI
    ├── package.json
    ├── vite.config.js            # proxies /api → localhost:8000
    └── src/
        ├── App.jsx               # Root — assembles Hero + Sidebar + Chat
        ├── api/
        │   └── chat.js           # fetch wrappers: sendMessage, resetSession, …
        ├── hooks/
        │   └── useChat.js        # all chat state + send + reset logic
        ├── styles/
        │   ├── tokens.css        # CSS custom properties (brand colours, spacing)
        │   └── global.css        # CSS reset + base styles
        └── components/
            ├── Hero.jsx          # Full-width header — logo, wordmark, pills, tabs
            ├── Sidebar.jsx       # Quick start buttons + Last Migration section
            ├── ChatArea.jsx      # Scrollable message list
            ├── Message.jsx       # Single AI / user bubble — renders markdown
            ├── ConfigCard.jsx    # Migration config summary card
            ├── TypingIndicator.jsx
            └── InputBar.jsx      # Textarea + send button
```

---

## How to Run

### Option A — Docker (both services in one command)

```bash
docker compose up --build
# Frontend → http://localhost:3000
# Backend  → http://localhost:8000
```

### Option B — Local dev (two terminals)

```bash
# Terminal 1 — Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend
npm install
npm run dev          # http://localhost:5173
```

---

## Common Commands

```bash
# Backend — hot reload
cd backend && uvicorn main:app --reload --port 8000

# Run tests (backend must be running first)
cd backend && python test.py

# View API docs
open http://localhost:8000/docs

# Frontend — Vite dev server
cd frontend && npm run dev

# Frontend — production build
cd frontend && npm run build

# Both via Docker
docker compose up --build

# Check simulated output files
ls backend/output/

# Python lint
cd backend && flake8 . --max-line-length=100
```

---

## LLM Configuration

All three variables live in the root `.env` file.
Changing them requires only a server restart — no code changes.

| Variable            | Required | Default  | Purpose                                         |
|---------------------|----------|----------|-------------------------------------------------|
| `LLM_API_KEY`       | Yes      | —        | API key (`OPENAI_API_KEY` accepted as fallback) |
| `LLM_BASE_URL`      | No       | —        | OpenAI-compatible endpoint; blank = OpenAI      |
| `LLM_MODEL`         | No       | `gpt-4o` | Model name supported by the chosen provider     |
| `LLM_EXTRA_HEADERS` | No       | —        | JSON object — sent as headers on every LLM call |

**Where these are used:**
- `backend/config/settings.py` — parsed from env
- `backend/llm/agent.py` — `MigrationAgent.__init__` builds the `OpenAI` client with `api_key`, `base_url`, and `default_headers`

**Provider examples:**

```env
# OpenAI (default)
LLM_API_KEY=sk-...

# Google Gemini
LLM_API_KEY=<google-ai-studio-key>
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
LLM_MODEL=gemini-2.0-flash

# Groq
LLM_API_KEY=<groq-key>
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_MODEL=llama-3.3-70b-versatile

# Extra headers
LLM_EXTRA_HEADERS={"use-case": "data-migration", "x-team": "platform"}
```

---

## API Endpoints

| Method | Path                        | Description                                      |
|--------|-----------------------------|--------------------------------------------------|
| GET    | `/`                         | Health root — name, version, status              |
| GET    | `/api/status`               | Model info + active session count                |
| POST   | `/api/chat`                 | Send message to agent (session-isolated)         |
| POST   | `/api/reset`                | Clear session conversation history               |
| DELETE | `/api/session/{id}`         | Remove a session and free its memory             |
| GET    | `/api/sessions`             | List all active session IDs                      |
| GET    | `/api/output`               | List files in `backend/output/`                  |
| GET    | `/files/{filename}`         | Download an output file                          |
| POST   | `/api/migrate`              | Directly trigger a migration (bypass agent)      |
| GET    | `/api/migrate/types`        | List migration types + required config fields    |

Interactive docs: **http://localhost:8000/docs**

---

## Key Design Decisions

**Fake-at-the-source-layer**: All sources return Faker DataFrames.
Destinations write to `backend/output/`. Agent, registry, executor are
production-ready; only I/O is mocked.

**Function calling over state machine**: The agent uses `tool_choice="auto"`.
The LLM decides when it has collected enough config — no hardcoded flow.

**Single registry pattern**: `tool_registry.py` is the only place to add
migration paths. Add a schema method + call `registry.register()` in
`build_default_registry()`.

**Stateful per-session agent**: `MigrationAgent.history` holds the full
message list. `agent.reset()` clears it. `POST /api/reset` triggers this
from the frontend.

**Plain CSS + tokens**: All colour/spacing values live in `tokens.css` as
CSS custom properties. No Tailwind, no CSS-in-JS.

**Markdown in chat**: `Message.jsx` uses `react-markdown` with custom
component overrides so that bubble text colour is always inherited correctly.

---

## Adding a New Migration Path

1. Add a source reader in `backend/tools/sources/` extending `BaseSource`
2. Add a destination writer in `backend/tools/destinations/` extending `BaseDestination`
3. Add a handler function in `backend/migrations/executor.py`
4. Add the JSON schema as a static method in `backend/llm/tool_registry.py`
5. Register it in `build_default_registry()`
6. Update `backend/connectors.yaml`
7. Update `SYSTEM_PROMPT` in `backend/llm/prompts.py`

---

## Supported Migration Paths

| Source   | Destination | Tool name                      |
|----------|-------------|-------------------------------|
| Postgres | BigQuery    | `migrate_postgres_to_bigquery` |
| CSV      | SQLite      | `migrate_csv_to_sqlite`        |
| S3       | Snowflake   | `migrate_s3_to_snowflake`      |
| MongoDB  | S3          | `migrate_mongo_to_s3`          |

---

## What NOT to Do

- Do not add real DB connection logic — keep sources/destinations fake for POC
- Do not store credentials anywhere except `.env` (gitignored)
- Do not put business logic in `main.py` — it is only app wiring
- Do not break the `BaseTool` / `BaseSource` / `BaseDestination` interfaces
- Do not use Tailwind or CSS-in-JS — plain CSS + `tokens.css` variables only
- Do not use Redux or Zustand — `useState` + custom hooks only
- Keep `App.jsx` under 80 lines — all logic in hooks, all UI in components
- Do not hardcode the LLM model or API key — always read from `settings.py`
