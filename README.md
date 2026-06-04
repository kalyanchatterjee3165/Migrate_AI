# migrate.ai

An AI-powered data migration assistant. Describe what you want to migrate in plain English — the agent asks clarifying questions, collects configuration through conversation, and executes the migration.

> **POC:** All data movement is simulated. Sources return Faker-generated data; destinations write output files to `/output`. No real databases or cloud services are connected.

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

| Branch         | Frontend         | Entry point                          | URL                     |
|----------------|------------------|--------------------------------------|-------------------------|
| `fastapi-react`| React + FastAPI  | see **Running** section below        | http://localhost:5173   |
| `main`         | Gradio           | `python app.py`                      | http://localhost:7860   |
| `streamlit`    | Streamlit        | `streamlit run streamlit_app.py`     | http://localhost:8501   |

The backend LLM agent, tools, and migration logic are identical across all branches.

---

## Stack

| Layer    | Technology                                      |
|----------|-------------------------------------------------|
| LLM      | Any OpenAI-compatible API (OpenAI, Gemini, Groq, Ollama…) |
| Backend  | FastAPI + Uvicorn (`fastapi-react` branch)      |
| Frontend | React 18 + Vite (`fastapi-react` branch)        |
| UI alt.  | Gradio (`main`) · Streamlit (`streamlit`)       |
| Data     | Faker + Pandas (simulated sources)              |
| Database | SQLAlchemy + SQLite (destination)               |
| Language | Python 3.11+ · Node 18+                        |

---

## Quick Start

### Step 1 — Clone the repo

```bash
git clone https://github.com/kalyanchatterjee3165/Migrate_AI.git
cd Migrate_AI
git checkout fastapi-react
```

### Step 2 — Set environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Required
LLM_API_KEY=sk-...

# Optional — change to switch providers (see Provider Examples below)
# LLM_BASE_URL=
# LLM_MODEL=gpt-4o

# Optional — extra headers on every LLM request
# LLM_EXTRA_HEADERS={"use-case": "data-migration"}
```

---

## Running — Option A: Docker Compose (recommended)

Runs both backend and frontend in one command.

```bash
docker compose up --build
```

| Service  | URL                    |
|----------|------------------------|
| Frontend | http://localhost:3000  |
| Backend  | http://localhost:8000  |

To stop:
```bash
docker compose down
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

Backend runs at **http://localhost:8000**  
API docs at **http://localhost:8000/docs**

### Terminal 2 — Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at **http://localhost:5173**

---

## LLM Provider Examples

Change just three variables in `.env` to switch providers:

| Provider        | `LLM_BASE_URL`                                                    | `LLM_MODEL`               |
|-----------------|-------------------------------------------------------------------|---------------------------|
| OpenAI          | *(leave blank)*                                                   | `gpt-4o`                  |
| Google Gemini   | `https://generativelanguage.googleapis.com/v1beta/openai/`        | `gemini-2.0-flash`        |
| Groq            | `https://api.groq.com/openai/v1`                                  | `llama-3.3-70b-versatile` |
| Ollama (local)  | `http://localhost:11434/v1`                                       | `llama3.2`                |

> `OPENAI_API_KEY` is still accepted as a fallback for backward compatibility.

---

## Environment Variables

| Variable            | Required | Default  | Description                                             |
|---------------------|----------|----------|---------------------------------------------------------|
| `LLM_API_KEY`       | Yes      | —        | API key for the chosen provider                         |
| `LLM_BASE_URL`      | No       | —        | OpenAI-compatible endpoint (blank = OpenAI)             |
| `LLM_MODEL`         | No       | `gpt-4o` | Model name                                              |
| `LLM_EXTRA_HEADERS` | No       | —        | JSON object of headers sent on every LLM request        |
| `LOG_LEVEL`         | No       | `INFO`   | Logging verbosity                                       |
| `OUTPUT_DIR`        | No       | `./output` | Directory for simulated migration output files        |

---

## API Endpoints

| Method | Path          | Description                              |
|--------|---------------|------------------------------------------|
| POST   | `/api/chat`   | Send a message, get agent reply          |
| POST   | `/api/reset`  | Reset the conversation and agent state   |
| GET    | `/api/status` | Health check + current model info        |
| GET    | `/api/output` | List simulated output files              |

Interactive docs: **http://localhost:8000/docs**

---

## Project Structure

```
migrate-ai/
├── .env.example
├── .env                          # your local config (gitignored)
├── docker-compose.yml
│
├── backend/
│   ├── main.py                   # FastAPI app + startup
│   ├── requirements.txt
│   ├── Dockerfile
│   │
│   ├── config/
│   │   └── settings.py           # loads .env — LLM_*, OUTPUT_DIR, etc.
│   │
│   ├── routers/
│   │   ├── chat.py               # POST /api/chat
│   │   └── session.py            # POST /api/reset, GET /api/status
│   │
│   ├── schemas/
│   │   └── chat.py               # Pydantic request/response models
│   │
│   ├── llm/
│   │   ├── agent.py              # MigrationAgent — chat loop + tool dispatch
│   │   ├── prompts.py            # System prompt
│   │   └── tool_registry.py      # Tool schemas + ToolRegistry
│   │
│   ├── migrations/
│   │   ├── executor.py           # Wires source → destination
│   │   └── validator.py          # Fake pre/post validation
│   │
│   ├── tools/
│   │   ├── sources/              # Postgres, CSV, S3, MongoDB (simulated reads)
│   │   ├── destinations/         # BigQuery, SQLite, S3, Snowflake (simulated writes)
│   │   └── generators/           # Faker-based data generation
│   │
│   └── output/                   # Simulated migration output files
│
└── frontend/
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── App.jsx               # Root component + layout
        ├── api/
        │   └── chat.js           # fetch wrappers for all API calls
        ├── hooks/
        │   └── useChat.js        # chat state management
        ├── components/
        │   ├── Hero.jsx          # Top header bar
        │   ├── Sidebar.jsx       # Quick start + last migration
        │   ├── ChatArea.jsx      # Message list
        │   ├── Message.jsx       # Single message bubble (renders markdown)
        │   ├── InputBar.jsx      # Text input + send button
        │   ├── ConfigCard.jsx    # Migration config summary card
        │   └── TypingIndicator.jsx
        └── styles/
            ├── tokens.css        # Brand color / spacing variables
            └── global.css        # Base styles
```

---

## How It Works

```
User message (React)
    │  POST /api/chat
    ▼
FastAPI router (routers/chat.py)
    │
    ▼
MigrationAgent (llm/agent.py)
    │  sends conversation + tool schemas to LLM
    │
    ▼
LLM (OpenAI / Gemini / Groq / …)
    │  asks clarifying questions until all fields collected
    │  then emits a function call
    │
    ▼
migrations/executor.py
    │  reads from simulated source  (Faker DataFrame)
    │  writes to simulated destination  (CSV/JSON in /output)
    │
    ▼
Agent returns plain-English summary → React UI
```

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

## License

MIT
