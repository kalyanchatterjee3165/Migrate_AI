from typing import Callable


class ToolRegistry:
    """
    Central registry of all migration tools available to the LLM.

    Each tool has:
      - name:        unique snake_case identifier
      - description: what the LLM uses to decide when to call this tool
      - parameters:  JSON Schema the LLM must populate before calling
      - handler:     the actual Python function that executes the migration
    """

    def __init__(self):
        self._tools: dict[str, dict] = {}
        self._handlers: dict[str, Callable] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, name: str, description: str, parameters: dict, handler: Callable):
        """Register a migration tool with its schema and handler function."""
        self._tools[name] = {
            "name":        name,
            "description": description,
            "parameters":  parameters,
        }
        self._handlers[name] = handler

    def get_handler(self, name: str) -> Callable:
        if name not in self._handlers:
            raise ValueError(f"No handler registered for tool: {name}")
        return self._handlers[name]

    def get_openai_tools(self) -> list[dict]:
        """Return tool definitions in OpenAI function-calling format."""
        return [
            {
                "type": "function",
                "function": {
                    "name":        t["name"],
                    "description": t["description"],
                    "parameters":  t["parameters"],
                },
            }
            for t in self._tools.values()
        ]

    # ------------------------------------------------------------------
    # Built-in tool schemas (one per migration path)
    # ------------------------------------------------------------------

    @staticmethod
    def postgres_to_bigquery_schema() -> dict:
        return {
            "type": "object",
            "properties": {
                "pg_host":     {"type": "string",  "description": "Postgres host"},
                "pg_port":     {"type": "integer", "description": "Postgres port (default 5432)"},
                "pg_database": {"type": "string",  "description": "Postgres database name"},
                "pg_username": {"type": "string",  "description": "Postgres username"},
                "pg_password": {"type": "string",  "description": "Postgres password"},
                "pg_table":    {"type": "string",  "description": "Source table name"},
                "row_limit":   {"type": "integer", "description": "Max rows to migrate (optional)"},
                "bq_project":  {"type": "string",  "description": "BigQuery project ID"},
                "bq_dataset":  {"type": "string",  "description": "BigQuery dataset ID"},
                "bq_table":    {"type": "string",  "description": "BigQuery destination table"},
                "write_mode":  {
                    "type": "string",
                    "enum": ["append", "overwrite"],
                    "description": "Write mode (default: append)",
                },
            },
            "required": [
                "pg_host", "pg_database", "pg_username", "pg_password", "pg_table",
                "bq_project", "bq_dataset", "bq_table",
            ],
        }

    @staticmethod
    def csv_to_sqlite_schema() -> dict:
        return {
            "type": "object",
            "properties": {
                "file_path":   {"type": "string",  "description": "Path to the source CSV file"},
                "delimiter":   {"type": "string",  "description": "CSV delimiter character (default: comma)"},
                "has_header":  {"type": "boolean", "description": "Whether CSV has a header row (default: true)"},
                "db_path":     {"type": "string",  "description": "Path for the SQLite .db file (e.g. ./output/migrate.db)"},
                "table_name":  {"type": "string",  "description": "Destination table name inside the SQLite database"},
                "if_exists":   {
                    "type": "string",
                    "enum": ["append", "replace"],
                    "description": "What to do if the table already exists (default: append)",
                },
            },
            "required": ["file_path", "db_path", "table_name"],
        }

    @staticmethod
    def s3_to_snowflake_schema() -> dict:
        return {
            "type": "object",
            "properties": {
                "bucket_name":  {"type": "string", "description": "S3 bucket name"},
                "object_key":   {"type": "string", "description": "S3 object key / path"},
                "file_format":  {"type": "string", "enum": ["csv", "json"], "description": "File format in S3"},
                "aws_region":   {"type": "string", "description": "AWS region"},
                "sf_account":   {"type": "string", "description": "Snowflake account identifier"},
                "sf_warehouse": {"type": "string", "description": "Snowflake warehouse"},
                "sf_database":  {"type": "string", "description": "Snowflake database"},
                "sf_schema":    {"type": "string", "description": "Snowflake schema"},
                "sf_table":     {"type": "string", "description": "Snowflake destination table"},
                "sf_username":  {"type": "string", "description": "Snowflake username"},
                "sf_password":  {"type": "string", "description": "Snowflake password"},
            },
            "required": [
                "bucket_name", "object_key", "file_format", "aws_region",
                "sf_account", "sf_warehouse", "sf_database",
                "sf_schema", "sf_table", "sf_username", "sf_password",
            ],
        }

    @staticmethod
    def mongo_to_s3_schema() -> dict:
        return {
            "type": "object",
            "properties": {
                "mongo_host":       {"type": "string",  "description": "MongoDB host"},
                "mongo_port":       {"type": "integer", "description": "MongoDB port (default 27017)"},
                "mongo_database":   {"type": "string",  "description": "MongoDB database name"},
                "mongo_collection": {"type": "string",  "description": "Source collection name"},
                "mongo_username":   {"type": "string",  "description": "MongoDB username (optional)"},
                "mongo_password":   {"type": "string",  "description": "MongoDB password (optional)"},
                "s3_bucket":        {"type": "string",  "description": "Destination S3 bucket"},
                "s3_key":           {"type": "string",  "description": "Destination S3 object key"},
                "file_format":      {"type": "string",  "enum": ["csv", "json"], "description": "Output format"},
                "aws_region":       {"type": "string",  "description": "AWS region"},
            },
            "required": [
                "mongo_host", "mongo_database", "mongo_collection",
                "s3_bucket", "s3_key", "aws_region",
            ],
        }


# ------------------------------------------------------------------
# Factory: build a fully-wired registry with all default tools
# ------------------------------------------------------------------

def build_default_registry(
    migrate_pg_to_bq:      Callable,
    migrate_csv_to_sqlite: Callable,
    migrate_s3_to_sf:      Callable,
    migrate_mongo_to_s3:   Callable,
) -> ToolRegistry:
    """
    Instantiate and return a ToolRegistry pre-loaded with all
    supported migration tools.

    Pass in the actual handler functions from migrations/executor.py.
    """
    registry = ToolRegistry()

    registry.register(
        name="migrate_postgres_to_bigquery",
        description=(
            "Migrate a full table from PostgreSQL into a BigQuery dataset. "
            "Use when source is Postgres and destination is BigQuery."
        ),
        parameters=ToolRegistry.postgres_to_bigquery_schema(),
        handler=migrate_pg_to_bq,
    )

    registry.register(
        name="migrate_csv_to_sqlite",
        description=(
            "Load data from a local CSV file into a SQLite database table. "
            "Use when source is a CSV file and destination is SQLite."
        ),
        parameters=ToolRegistry.csv_to_sqlite_schema(),
        handler=migrate_csv_to_sqlite,
    )

    registry.register(
        name="migrate_s3_to_snowflake",
        description=(
            "Copy a file from S3 into a Snowflake table. "
            "Use when source is S3 and destination is Snowflake."
        ),
        parameters=ToolRegistry.s3_to_snowflake_schema(),
        handler=migrate_s3_to_sf,
    )

    registry.register(
        name="migrate_mongo_to_s3",
        description=(
            "Export a MongoDB collection and upload it to S3 as JSON or CSV. "
            "Use when source is MongoDB and destination is S3."
        ),
        parameters=ToolRegistry.mongo_to_s3_schema(),
        handler=migrate_mongo_to_s3,
    )

    return registry