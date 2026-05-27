"""
executor.py — handler functions registered in tool_registry.py.

Each function:
  1. Reads data from the (fake) source
  2. Runs pre-migration validation
  3. Writes to the (fake) destination
  4. Runs post-migration validation
  5. Returns a summary dict the LLM uses to craft its reply
"""

from tools.sources import PostgresSource, CsvSource, S3Source, MongoSource
from tools.destinations import BigQueryDest, PostgresDest, S3Dest, SnowflakeDest
from migrations.validator import MigrationValidator

validator = MigrationValidator()


def migrate_postgres_to_bigquery(**kwargs) -> dict:
    df = PostgresSource().fetch(**kwargs)
    pre = validator.pre_check(df)
    result = BigQueryDest().save(df, **kwargs)
    post = validator.post_check(df, result["rows_written"])
    return _summary("postgres", "bigquery", pre, post, result)


def migrate_csv_to_postgres(**kwargs) -> dict:
    df = CsvSource().fetch(**kwargs)
    pre = validator.pre_check(df)
    result = PostgresDest().save(df, **kwargs)
    post = validator.post_check(df, result["rows_written"])
    return _summary("csv", "postgres", pre, post, result)


def migrate_s3_to_snowflake(**kwargs) -> dict:
    df = S3Source().fetch(**kwargs)
    pre = validator.pre_check(df)
    result = SnowflakeDest().save(df, **kwargs)
    post = validator.post_check(df, result["rows_written"])
    return _summary("s3", "snowflake", pre, post, result)


def migrate_mongo_to_s3(**kwargs) -> dict:
    df = MongoSource().fetch(**kwargs)
    pre = validator.pre_check(df)
    result = S3Dest().save(df, **kwargs)
    post = validator.post_check(df, result["rows_written"])
    return _summary("mongo", "s3", pre, post, result)


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _summary(source: str, dest: str, pre: dict, post: dict, result: dict) -> dict:
    return {
        "source":             source,
        "destination":        dest,
        "rows_read":          pre["row_count"],
        "rows_written":       result["rows_written"],
        "columns":            pre["columns"],
        "pre_check_passed":   pre["passed"],
        "post_check_passed":  post["passed"],
        "pre_issues":         pre["issues"],
        "output_path":        result.get("output_path", ""),
        "destination_ref":    result.get("destination", ""),
    }