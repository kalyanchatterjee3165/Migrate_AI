# MigrateAI

An AI-powered conversational data migration tool. Describe what you want to migrate in plain English — the agent asks clarifying questions, collects configuration through conversation, then executes the migration.

> **POC:** All data movement is simulated. Sources return Faker-generated data; destinations write output files to `backend/output/`. No real databases or cloud services are connected.

---

## Demo

```
You:   I want to migrate my Postgres users table to BigQuery.
Agent: Sure! What's the Postgres host and database name?
You:   localhost, mydb
Agent: Got it. What BigQuery project and dataset should I load into?
...
Agent: Migration complete. 200 rows written to analytics.users in BigQuery.
```

---

## Supported Migration Paths

| Source     | Destination | Tool name                      |
|------------|-------------|-------------------------------|
| PostgreSQL | BigQuery    | `migrate_postgres_to_bigquery` |
| CSV file   | SQLite      | `migrate_csv_to_sqlite`        |
| S3         | Snowflake   | `migrate_s3_to_snowflake`      |
| MongoDB    | S3          | `migrate_mongo_to_s3`          |

---

## Branches

| Branch           | Frontend              | Entry point                              | URL                    |
|------------------|-----------------------|------------------------------------------|------------------------|
| `main`           | Gradio                | `python app.py`                          | http://localhost:7860  |
| `fastapi-react`  | React (Vite) + Next.js + FastAPI | see **Running** below         | http://localhost:3000  |
| `streamlit`      | Streamlit             | `streamlit run streamlit_app.py`         | http://localhost:8501  |
| `streamlit-ui`   | Streamlit (rebuilt)   | `streamlit run streamlit_app.py`         | http://localhost:8501  |
| `fastapi-nextjs` | Next.js + FastAPI     | see **Running** below                    | http://localhost:3000  |

Backend LLM agent, tools, and migration logic are identical across all branches.

---

## Stack

| Layer       | Technology                                                        |
|-------------|-------------------------------------------------------------------|
| LLM         | Any OpenAI-compatible API (OpenAI, Gemini, Groq, Ollama…)        |
| Backend     | FastAPI + Uvicorn                                                 |
| Frontend    | Next.js 16 (App Router, TypeScript, Tailwind) · React 18 + Vite  |
| UI alt.     | Gradio (`main`) · Streamlit (`streamlit`, `streamlit-ui`)         |
| Data        | Faker + Pandas (simulated sources)                                |
| Database    | SQLAlchemy + SQLite (destination)                                 |
| Language    | Python 3.11+ · Node 20+                                          |

---

## Quick Start

### Step 1 — Clone and checkout

```bash
git clone https://github.com/kalyanchatterjee3165/Migrate_AI.git
cd Migrate_AI
git checkout fastapi-react
```

### Step 2 — Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Required
LLM_API_KEY=sk-...

# Optional — switch providers (see Provider Examples below)
# LLM_BASE_URL=
# LLM_MODEL=gpt-4o

# Optional — extra headers on every LLM request
# LLM_EXTRA_HEADERS={"use-case": "data-migration"}
```

---

## Running — Option A: Docker Compose (recommended)

Runs backend and Next.js frontend together.

```bash
docker compose up --build
```

| Service  | URL                   |
|----------|-----------------------|
| Frontend | http://localhost:3000 |
| Backend  | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

```bash
docker compose down   # stop
```

---

## Running — Option B: Manual (two terminals)

### Terminal 1 — Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend: **http://localhost:8000** · Docs: **http://localhost:8000/docs**

### Terminal 2 — Frontend (Next.js)

```bash
cd frontend-next
npm install
npm run dev
```

Frontend: **http://localhost:3000**

---

## Running Tests

With the backend running:

```bash
cd backend
python test.py
```

Covers all 10 API endpoints across 13 test groups.

---

## LLM Provider Examples

| Provider       | `LLM_BASE_URL`                                              | `LLM_MODEL`               |
|----------------|-------------------------------------------------------------|---------------------------|
| OpenAI         | *(leave blank)*                                             | `gpt-4o`                  |
| Google Gemini  | `https://generativelanguage.googleapis.com/v1beta/openai/`  | `gemini-2.0-flash`        |
| Groq           | `https://api.groq.com/openai/v1`                            | `llama-3.3-70b-versatile` |
| Ollama (local) | `http://localhost:11434/v1`                                 | `llama3.2`                |

> `OPENAI_API_KEY` is accepted as a fallback for backward compatibility.

---

## Environment Variables

| Variable            | Required | Default    | Description                                      |
|---------------------|----------|------------|--------------------------------------------------|
| `LLM_API_KEY`       | Yes      | —          | API key for the chosen provider                  |
| `LLM_BASE_URL`      | No       | —          | OpenAI-compatible endpoint (blank = OpenAI)      |
| `LLM_MODEL`         | No       | `gpt-4o`   | Model name                                       |
| `LLM_EXTRA_HEADERS` | No       | —          | JSON object of headers sent on every LLM request |
| `LOG_LEVEL`         | No       | `INFO`     | Logging verbosity                                |
| `OUTPUT_DIR`        | No       | `./output` | Directory for simulated migration output files   |

---

## API Endpoints

| Method | Path                    | Description                                   |
|--------|-------------------------|-----------------------------------------------|
| GET    | `/`                     | Health root — name, version, status           |
| GET    | `/api/status`           | Model info + active session count             |
| POST   | `/api/chat`             | Send message to agent (session-isolated)      |
| POST   | `/api/reset`            | Clear session conversation history            |
| DELETE | `/api/session/{id}`     | Remove a session and free its memory          |
| GET    | `/api/sessions`         | List all active session IDs                   |
| GET    | `/api/output`           | List files in `backend/output/`               |
| GET    | `/files/{filename}`     | Download an output file                       |
| POST   | `/api/migrate`          | Directly trigger a migration (bypass agent)   |
| GET    | `/api/migrate/types`    | List migration types + required config fields |

Interactive docs: **http://localhost:8000/docs**

---

## Project Structure

```
migrate-ai/
├── .env.example
├── .env                              # your local config (gitignored)
├── docker-compose.yml
├── CLAUDE.md                         # developer guide for Claude Code
│
├── backend/                          # FastAPI server
│   ├── main.py                       # app entry point
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── test.py                       # end-to-end API tests (no framework needed)
│   │
│   ├── config/
│   │   └── settings.py               # loads .env — LLM_*, OUTPUT_DIR, etc.
│   │
│   ├── middleware/
│   │   └── session_manager.py        # thread-safe per-session agent registry
│   │
│   ├── routers/
│   │   ├── chat.py                   # POST /api/chat
│   │   ├── session.py                # reset, status, output, sessions
│   │   └── migrations.py            # POST /api/migrate, GET /api/migrate/types
│   │
│   ├── schemas/
│   │   └── chat.py                   # Pydantic request/response models
│   │
│   ├── llm/
│   │   ├── agent.py                  # MigrationAgent — chat loop + tool dispatch
│   │   ├── prompts.py                # system prompt
│   │   └── tool_registry.py          # tool schemas + ToolRegistry
│   │
│   ├── migrations/
│   │   ├── executor.py               # wires source → destination
│   │   └── validator.py              # fake pre/post validation
│   │
│   ├── tools/
│   │   ├── sources/                  # Postgres, CSV, S3, MongoDB (simulated reads)
│   │   ├── destinations/             # BigQuery, SQLite, S3, Snowflake (simulated writes)
│   │   └── generators/               # Faker-based data generation
│   │
│   └── output/                       # simulated migration output files
│
├── frontend-next/                    # Next.js 16 frontend (primary)
│   ├── next.config.ts                # proxies /api/* → backend, standalone output
│   ├── Dockerfile                    # multi-stage build for production
│   ├── package.json
│   └── src/
│       ├── app/
│       │   ├── layout.tsx            # root layout
│       │   ├── page.tsx              # renders <MigrateApp />
│       │   └── globals.css           # CSS variables + reset
│       ├── components/
│       │   ├── MigrateApp.tsx        # root layout component
│       │   ├── Hero.tsx              # full-width header
│       │   ├── Sidebar.tsx           # quick start + last migration
│       │   ├── ChatArea.tsx          # scrollable message list
│       │   ├── Message.tsx           # single bubble (renders markdown)
│       │   ├── InputBar.tsx          # text input + send button
│       │   ├── ConfigCard.tsx        # migration config summary card
│       │   └── TypingIndicator.tsx   # 3-dot bounce animation
│       ├── hooks/
│       │   ├── useChat.ts            # chat state + API calls
│       │   └── useSession.ts         # UUID session_id per browser tab
│       ├── api/
│       │   └── client.ts             # typed fetch wrappers for all endpoints
│       └── types/
│           └── index.ts              # shared TypeScript types
│
└── frontend/                         # original React 18 + Vite frontend
    ├── vite.config.js
    └── src/
        ├── App.jsx
        ├── api/chat.js
        ├── hooks/useChat.js
        └── components/               # Hero, Sidebar, Chat, Message, InputBar…
```

---

## How It Works

```
User message (Next.js)
    │  POST /api/chat  { message, session_id }
    ▼
FastAPI router  →  SessionManager.get_agent(session_id)
    │
    ▼
MigrationAgent (llm/agent.py)
    │  sends conversation + tool schemas to LLM
    ▼
LLM (OpenAI / Gemini / Groq / …)
    │  asks clarifying questions until all fields collected
    │  then emits a function call
    ▼
migrations/executor.py
    │  reads from simulated source  (Faker DataFrame)
    │  writes to simulated destination  (CSV / JSON / SQLite in /output)
    ▼
Agent returns plain-English summary  →  Next.js UI
```

---

## Adding a New Migration Path

1. Add a source reader in `backend/tools/sources/` extending `BaseSource`
2. Add a destination writer in `backend/tools/destinations/` extending `BaseDestination`
3. Add a handler function in `backend/migrations/executor.py`
4. Add the JSON schema as a static method in `backend/llm/tool_registry.py`
5. Register it in `build_default_registry()`
6. Update `backend/config/connectors.yaml`
7. Update `SYSTEM_PROMPT` in `backend/llm/prompts.py`

---

## License

MIT
