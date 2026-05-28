# migrate.ai — Claude Code Project Guide

## What This Project Is

A conversational data migration tool powered by an LLM agent.
Users chat naturally to describe their source and destination, the agent
collects required config through conversation, then calls the right migration
tool to execute the job.

This is a **POC** — all data movement is simulated with Faker-generated data.
No real databases or cloud services are connected.

---

## Stack

- **LLM**: OpenAI GPT-4o via `openai` SDK (tool/function calling)
- **Backend**: FastAPI + Uvicorn (`backend/main.py`)
- **Frontend**: React 18 + Vite, plain CSS (no Tailwind, no CSS-in-JS)
- **UI icons**: lucide-react
- **Data generation**: `faker`, `pandas`
- **Database**: `sqlalchemy` (SQLite destination)
- **Python**: 3.10+
- **Node**: 20+

---

## Project Structure

```
migrate-ai/
├── app.py                        # Legacy Gradio entry point (deprecated)
├── CLAUDE.md                     # You are here
├── docker-compose.yml            # Runs backend + frontend together
│
├── backend/                      # FastAPI server
│   ├── main.py                   # FastAPI app — run this
│   ├── requirements.txt          # Python deps (FastAPI, uvicorn, openai, …)
│   ├── Dockerfile
│   ├── schemas/
│   │   └── chat.py               # Pydantic models: ChatRequest, ChatResponse, …
│   ├── routers/
│   │   ├── chat.py               # POST /api/chat
│   │   └── session.py            # POST /api/reset, GET /api/status, GET /api/output
│   │
│   ├── llm/
│   │   ├── agent.py              # MigrationAgent: chat loop + tool dispatch
│   │   ├── prompts.py            # SYSTEM_PROMPT + confirmation helper
│   │   └── tool_registry.py      # ToolRegistry + OpenAI tool schemas
│   │
│   ├── tools/
│   │   ├── base.py               # BaseTool interface
│   │   ├── generators/           # Faker-based data generation
│   │   ├── sources/              # Fake Postgres, CSV, S3, Mongo sources
│   │   └── destinations/         # Fake BigQuery, SQLite, S3, Snowflake dests
│   │
│   ├── migrations/
│   │   ├── executor.py           # Wires source.read() → dest.write()
│   │   └── validator.py          # Fake pre/post validation
│   │
│   ├── config/
│   │   ├── connectors.yaml       # Supported source/dest pairs + required fields
│   │   └── settings.py           # Loads .env vars
│   │
│   ├── session/
│   │   └── state.py              # Per-conversation config state
│   │
│   └── output/                   # Simulated migration output files land here
│
└── frontend/                     # React + Vite UI
    ├── package.json
    ├── vite.config.js            # Proxies /api → localhost:8000
    ├── index.html
    └── src/
        ├── main.jsx
        ├── App.jsx               # Root — assembles Hero + Sidebar + Chat
        ├── api/
        │   └── chat.js           # fetch wrappers: sendMessage, resetSession, …
        ├── hooks/
        │   └── useChat.js        # All chat state + sendMessage + resetSession
        ├── styles/
        │   ├── tokens.css        # Liberty Mutual CSS variables
        │   └── global.css        # CSS reset + base styles
        └── components/
            ├── Hero.jsx          # Full-width header with logo, tabs, pills
            ├── Sidebar.jsx       # Quick start panel + New Migration button
            ├── ChatArea.jsx      # Scrollable message list
            ├── Message.jsx       # Single AI / user bubble
            ├── ConfigCard.jsx    # Yellow-bordered collected-config card
            ├── TypingIndicator.jsx # Three bouncing dots
            └── InputBar.jsx      # Text input + send button
```

---

## How to Run

### Local development (recommended)

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend (separate terminal) — requires Node 20
cd frontend
npm install
npm run dev
# Vite opens at http://localhost:5173
```

### Both via Docker

```bash
docker-compose up --build
# Backend → http://localhost:8000
# Frontend → http://localhost:3000
```

---

## Common Commands

```bash
# Backend — start with hot reload
cd backend && uvicorn main:app --reload --port 8000

# Frontend — Vite dev server
cd frontend && npm run dev

# Frontend — production build
cd frontend && npm run build

# Both via Docker
docker-compose up --build

# Check output files after a simulated migration
ls backend/output/

# Lint Python
cd backend && flake8 . --max-line-length=100

# Run Python tests (once added)
cd backend && pytest tests/
```

---

## API Endpoints

| Method | Path         | Description                        |
|--------|--------------|------------------------------------|
| POST   | /api/chat    | Send a message, get a reply        |
| POST   | /api/reset   | Reset the conversation             |
| GET    | /api/status  | Returns `{ model, connected }`     |
| GET    | /api/output  | List files in backend/output/      |

---

## Key Design Decisions

**Fake-at-the-source-layer**: All sources return Faker-generated DataFrames.
Destinations save to `backend/output/` as CSV/JSON. The agent, tool registry,
and migration executor are all real and production-ready — only the I/O is mocked.

**OpenAI function calling**: The agent uses `tool_choice="auto"`. The LLM
decides when it has enough config to call a tool — no hardcoded state machine.

**Single registry pattern**: `tool_registry.py` is the only place to add new
migration paths. Add a schema method + call `registry.register()` in
`build_default_registry()`.

**Stateful chat history**: `MigrationAgent.history` holds the full OpenAI
message list. `agent.reset()` clears it. The React `useChat` hook calls
`POST /api/reset` on the "New Migration" button.

**Plain CSS with tokens**: No Tailwind, no CSS-in-JS. All colour values live
in `frontend/src/styles/tokens.css` as CSS custom properties.

---

## Adding a New Migration Path

1. Add a source reader in `backend/tools/sources/` extending `BaseSource`
2. Add a destination writer in `backend/tools/destinations/` extending `BaseDestination`
3. Add a handler function in `backend/migrations/executor.py`
4. Add the JSON schema in `backend/llm/tool_registry.py` as a static method
5. Register it in `build_default_registry()`
6. Update `backend/config/connectors.yaml`
7. Update the `SYSTEM_PROMPT` in `backend/llm/prompts.py` with the new fields

---

## Supported Migration Paths (POC)

| Source    | Destination | Tool name                      |
|-----------|-------------|-------------------------------|
| Postgres  | BigQuery    | `migrate_postgres_to_bigquery` |
| CSV       | SQLite      | `migrate_csv_to_sqlite`        |
| S3        | Snowflake   | `migrate_s3_to_snowflake`      |
| MongoDB   | S3          | `migrate_mongo_to_s3`          |

---

## Environment Variables

| Variable         | Required | Description              |
|------------------|----------|--------------------------|
| `OPENAI_API_KEY` | Yes      | OpenAI API key           |
| `LOG_LEVEL`      | No       | Default: INFO            |
| `OUTPUT_DIR`     | No       | Default: `./output`      |

The `.env` file lives at the project root. The backend loads it automatically
via `find_dotenv()` (searches parent directories from `backend/`).

---

## What NOT to Do

- Do not add real DB connection logic — keep sources/destinations fake for POC
- Do not store credentials anywhere except `.env` (which is gitignored)
- Do not put business logic in `main.py` — it's only app wiring
- Do not break the `BaseTool` / `BaseSource` / `BaseDestination` interfaces
- Do not use Tailwind or CSS-in-JS in the frontend — plain CSS + token variables only
- Do not use Redux — useState + custom hooks only
- Keep `App.jsx` under 80 lines — all logic in hooks, all UI in components
