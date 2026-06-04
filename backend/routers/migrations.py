from fastapi import APIRouter, HTTPException
from schemas.chat import MigrationRequest, MigrationResponse
from migrations.executor import (
    migrate_postgres_to_bigquery,
    migrate_csv_to_sqlite,
    migrate_s3_to_snowflake,
    migrate_mongo_to_s3,
)

router = APIRouter()

MIGRATION_HANDLERS = {
    "postgres_to_bigquery": migrate_postgres_to_bigquery,
    "csv_to_sqlite":        migrate_csv_to_sqlite,
    "s3_to_snowflake":      migrate_s3_to_snowflake,
    "mongo_to_s3":          migrate_mongo_to_s3,
}


@router.post("/migrate", response_model=MigrationResponse)
async def trigger_migration(body: MigrationRequest) -> MigrationResponse:
    """
    Directly trigger a migration without going through the agent.

    migration_type options:
      - postgres_to_bigquery
      - csv_to_sqlite
      - s3_to_snowflake
      - mongo_to_s3
    """
    if body.migration_type not in MIGRATION_HANDLERS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unknown migration_type '{body.migration_type}'. "
                f"Valid options: {list(MIGRATION_HANDLERS.keys())}"
            ),
        )

    handler = MIGRATION_HANDLERS[body.migration_type]

    try:
        result = handler(**body.config)
        return MigrationResponse(
            status="success",
            rows_read=result.get("rows_read", 0),
            rows_written=result.get("rows_written", 0),
            source=result.get("source", ""),
            destination=result.get("destination", ""),
            output_path=result.get("output_path", ""),
            pre_check_passed=result.get("pre_check_passed", False),
            post_check_passed=result.get("post_check_passed", False),
            columns=result.get("columns", []),
        )
    except Exception as e:
        return MigrationResponse(
            status="error",
            rows_read=0,
            rows_written=0,
            source="",
            destination="",
            output_path="",
            columns=[],
            pre_check_passed=False,
            post_check_passed=False,
            error=str(e),
        )


@router.get("/migrate/types")
async def migration_types():
    """List all available migration types and their required config fields."""
    return {
        "migration_types": {
            "postgres_to_bigquery": {
                "description": "Migrate from PostgreSQL to BigQuery",
                "required": [
                    "pg_host", "pg_database", "pg_username",
                    "pg_password", "pg_table",
                    "bq_project", "bq_dataset", "bq_table",
                ],
                "optional": ["pg_port", "row_limit", "write_mode"],
            },
            "csv_to_sqlite": {
                "description": "Load a CSV file into SQLite",
                "required": ["file_path", "table_name", "db_path"],
                "optional": ["delimiter", "has_header", "if_exists"],
            },
            "s3_to_snowflake": {
                "description": "Copy from S3 into Snowflake",
                "required": [
                    "bucket_name", "object_key", "file_format", "aws_region",
                    "sf_account", "sf_warehouse", "sf_database",
                    "sf_schema", "sf_table", "sf_username", "sf_password",
                ],
                "optional": [],
            },
            "mongo_to_s3": {
                "description": "Export MongoDB collection to S3",
                "required": [
                    "mongo_host", "mongo_database",
                    "mongo_collection", "s3_bucket",
                    "s3_key", "aws_region",
                ],
                "optional": [
                    "mongo_port", "mongo_username",
                    "mongo_password", "file_format",
                ],
            },
        }
    }
