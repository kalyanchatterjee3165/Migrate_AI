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
- **UI**: Gradio chat interface (`app.py`)
- **Data generation**: `faker`, `pandas`
- **Python**: 3.10+

---

## Project Structure

```
migrate-ai/
├── app.py                        # Gradio entry point — run this
├── CLAUDE.md                     # You are here
│
├── llm/
│   ├── agent.py                  # MigrationAgent: chat loop + tool dispatch
│   ├── prompts.py                # SYSTEM_PROMPT + confirmation helper
│   └── tool_registry.py         # ToolRegistry + OpenAI tool schemas
│
├── tools/
│   ├── base.py                   # BaseTool interface
│   ├── generators/
│   │   ├── base_generator.py     # Shared Faker instance + field helpers
│   │   ├── schema_profiles.py    # Named data profiles: users, orders, events
│   │   └── data_factory.py       # Entry point: profile + row_count → DataFrame
│   ├── sources/
│   │   ├── base_source.py        # BaseSource with fake connect/disconnect
│   │   ├── postgres_source.py    # Fakes Postgres, returns DataFrame via data_factory
│   │   ├── csv_source.py         # Fakes CSV read, returns DataFrame
│   │   ├── s3_source.py          # Fakes S3 download, returns DataFrame
│   │   └── mongo_source.py       # Fakes Mongo query, returns nested docs
│   └── destinations/
│       ├── base_destination.py   # BaseDestination with fake write + output save
│       ├── bigquery_dest.py      # Fakes BQ load, saves CSV to /output
│       ├── postgres_dest.py      # Fakes INSERT, saves CSV to /output
│       ├── s3_dest.py            # Fakes S3 upload, saves JSON/CSV to /output
│       └── snowflake_dest.py     # Fakes Snowflake COPY, saves CSV to /output
│
├── migrations/
│   ├── executor.py               # Wires source.read() → dest.write(), returns summary
│   └── validator.py              # Fake pre/post row count + schema checks
│
├── config/
│   ├── connectors.yaml           # Supported source/dest pairs + required fields
│   └── settings.py               # Loads .env vars (OPENAI_API_KEY, etc.)
│
├── session/
│   └── state.py                  # Per-conversation config state (used by Gradio)
│
└── output/                       # Simulated migration output files land here
```

---

## How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your OpenAI key
cp .env.example .env
# edit .env and add: OPENAI_API_KEY=sk-...

# 3. Launch
python app.py
# Gradio UI opens at http://localhost:7860
```

---

## Common Commands

```bash
# Run the app
python app.py

# Install deps
pip install -r requirements.txt

# Check output files after a simulated migration
ls output/

# Lint
flake8 . --max-line-length=100

# Run tests (once added)
pytest tests/
```

---

## Key Design Decisions

**Fake-at-the-source-layer**: All sources return Faker-generated DataFrames.
Destinations save to `/output` as CSV/JSON. The agent, tool registry, and
migration executor are all real and production-ready — only the I/O is mocked.

**OpenAI function calling**: The agent uses `tool_choice="auto"`. The LLM
decides when it has enough config to call a tool — no hardcoded state machine.

**Single registry pattern**: `tool_registry.py` is the only place to add new
migration paths. Add a schema method + call `registry.register()` in
`build_default_registry()`.

**Stateful chat history**: `MigrationAgent.history` holds the full OpenAI
message list. `agent.reset()` clears it. Gradio calls `reset()` on the
"New Migration" button.

---

## Adding a New Migration Path

1. Add a source reader in `tools/sources/` extending `BaseSource`
2. Add a destination writer in `tools/destinations/` extending `BaseDestination`
3. Add a handler function in `migrations/executor.py`
4. Add the JSON schema in `tool_registry.py` as a static method
5. Register it in `build_default_registry()`
6. Update `config/connectors.yaml`
7. Update the `SYSTEM_PROMPT` in `prompts.py` with the new source/dest fields

---

## Supported Migration Paths (POC)

| Source    | Destination | Tool name                      |
|-----------|-------------|-------------------------------|
| Postgres  | BigQuery    | `migrate_postgres_to_bigquery` |
| CSV       | Postgres    | `migrate_csv_to_postgres`      |
| S3        | Snowflake   | `migrate_s3_to_snowflake`      |
| MongoDB   | S3          | `migrate_mongo_to_s3`          |

---

## Environment Variables

| Variable         | Required | Description              |
|------------------|----------|--------------------------|
| `OPENAI_API_KEY` | Yes      | OpenAI API key           |
| `LOG_LEVEL`      | No       | Default: INFO            |
| `OUTPUT_DIR`     | No       | Default: `./output`      |

---

## What NOT to Do

- Do not add real DB connection logic — keep sources/destinations fake for POC
- Do not store credentials anywhere except `.env` (which is gitignored)
- Do not put business logic in `app.py` — it's only UI wiring
- Do not break the `BaseTool` / `BaseSource` / `BaseDestination` interfaces