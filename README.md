# migrate.ai

An AI-powered data migration assistant. Describe what you want to migrate in plain English — the agent asks the right questions, collects the required configuration through conversation, and executes the migration.

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
| CSV file   | PostgreSQL  | `migrate_csv_to_postgres`      |
| S3         | Snowflake   | `migrate_s3_to_snowflake`      |
| MongoDB    | S3          | `migrate_mongo_to_s3`          |

---

## Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| LLM         | OpenAI GPT-4o (function calling)  |
| UI          | Gradio (chat interface)           |
| Data        | Faker + Pandas (simulated)        |
| Language    | Python 3.10+                      |

---

## Setup

**1. Clone the repo**

```bash
git clone https://github.com/<your-username>/migrate-ai.git
cd migrate-ai
```

**2. Create and activate a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure your API key**

```bash
cp .env.example .env
```

Edit `.env` and add your key:

```
OPENAI_API_KEY=sk-...
```

**5. Run**

```bash
python app.py
```

Open [http://localhost:7860](http://localhost:7860) in your browser.

---

## Project Structure

```
migrate-ai/
├── app.py                        # Gradio entry point
├── requirements.txt
├── .env.example
│
├── llm/
│   ├── agent.py                  # MigrationAgent: chat loop + tool dispatch
│   ├── prompts.py                # System prompt
│   └── tool_registry.py         # Tool schemas + ToolRegistry
│
├── tools/
│   ├── generators/               # Faker-based data generation
│   ├── sources/                  # Postgres, CSV, S3, MongoDB (simulated reads)
│   └── destinations/             # BigQuery, Postgres, S3, Snowflake (simulated writes)
│
├── migrations/
│   ├── executor.py               # Wires source → destination
│   └── validator.py              # Pre/post row count + schema checks
│
├── config/
│   ├── connectors.yaml           # Supported source/dest pairs + required fields
│   └── settings.py               # Loads environment variables
│
├── session/
│   └── state.py                  # Per-conversation config state
│
└── output/                       # Simulated migration output files
```

---

## How It Works

1. The user describes a migration in the chat UI.
2. `MigrationAgent` sends the conversation to GPT-4o along with JSON schemas for each migration tool.
3. GPT-4o asks clarifying questions until it has collected all required fields.
4. Once ready, GPT-4o emits a function call — the agent dispatches it to the matching handler in `migrations/executor.py`.
5. The executor reads from a simulated source (Faker-generated DataFrame) and writes to a simulated destination (CSV/JSON in `/output`).
6. The agent summarises the result in plain English.

---

## Environment Variables

| Variable         | Required | Default    | Description           |
|------------------|----------|------------|-----------------------|
| `OPENAI_API_KEY` | Yes      | —          | OpenAI API key        |
| `LOG_LEVEL`      | No       | `INFO`     | Logging verbosity     |
| `OUTPUT_DIR`     | No       | `./output` | Migration output path |

---

## Adding a New Migration Path

1. Add a source reader in `tools/sources/` extending `BaseSource`
2. Add a destination writer in `tools/destinations/` extending `BaseDestination`
3. Add a handler function in `migrations/executor.py`
4. Add the JSON schema as a static method in `llm/tool_registry.py`
5. Register it in `build_default_registry()`
6. Update `config/connectors.yaml`
7. Update `SYSTEM_PROMPT` in `llm/prompts.py`

---

## License

MIT
