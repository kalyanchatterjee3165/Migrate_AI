"""
test.py — end-to-end test for every MigrateAI API endpoint.

Usage:
  # Terminal 1 — start the server
  uvicorn main:app --reload --port 8000

  # Terminal 2 — run tests
  python test.py
"""

import requests
import json
import time

BASE = "http://localhost:8000"


def separator(title):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def check(label, response, expected_status=200):
    ok = response.status_code == expected_status
    icon = "✅" if ok else "❌"
    print(f"\n{icon} {label}")
    print(f"   Status: {response.status_code}")
    try:
        data = response.json()
        print(f"   Response: {json.dumps(data, indent=4)}")
    except Exception:
        print(f"   Response: {response.text}")
    return response


# ──────────────────────────────────────────────────────────────
separator("TEST 1 — Root endpoint")
# ──────────────────────────────────────────────────────────────
check("GET /", requests.get(f"{BASE}/"))

# ──────────────────────────────────────────────────────────────
separator("TEST 2 — Health check")
# ──────────────────────────────────────────────────────────────
check("GET /api/status", requests.get(f"{BASE}/api/status"))

# ──────────────────────────────────────────────────────────────
separator("TEST 3 — Chat conversation (session A)")
# ──────────────────────────────────────────────────────────────
check(
    "POST /api/chat — greeting",
    requests.post(f"{BASE}/api/chat", json={
        "message":    "hi",
        "session_id": "test_session_A",
    }),
)

check(
    "POST /api/chat — describe migration",
    requests.post(f"{BASE}/api/chat", json={
        "message":    "I want to migrate data from Postgres to BigQuery",
        "session_id": "test_session_A",
    }),
)

# ──────────────────────────────────────────────────────────────
separator("TEST 4 — Session isolation")
# ──────────────────────────────────────────────────────────────
check(
    "POST /api/chat — fresh session B",
    requests.post(f"{BASE}/api/chat", json={
        "message":    "What were we just talking about?",
        "session_id": "test_session_B",
    }),
)
print("\n  ℹ️  Session B should say it has no previous context")

# ──────────────────────────────────────────────────────────────
separator("TEST 5 — Session management")
# ──────────────────────────────────────────────────────────────
check("GET /api/sessions", requests.get(f"{BASE}/api/sessions"))

check(
    "POST /api/reset — clear session A",
    requests.post(f"{BASE}/api/reset", json={"session_id": "test_session_A"}),
)

check(
    "POST /api/chat after reset — should be fresh",
    requests.post(f"{BASE}/api/chat", json={
        "message":    "What were we just talking about?",
        "session_id": "test_session_A",
    }),
)

check(
    "DELETE /api/session/test_session_B",
    requests.delete(f"{BASE}/api/session/test_session_B"),
)

# ──────────────────────────────────────────────────────────────
separator("TEST 6 — Available migration types")
# ──────────────────────────────────────────────────────────────
check("GET /api/migrate/types", requests.get(f"{BASE}/api/migrate/types"))

# ──────────────────────────────────────────────────────────────
separator("TEST 7 — Direct migration: Postgres → BigQuery")
# ──────────────────────────────────────────────────────────────
check(
    "POST /api/migrate — postgres_to_bigquery",
    requests.post(f"{BASE}/api/migrate", json={
        "migration_type": "postgres_to_bigquery",
        "session_id":     "test_session_migrate",
        "config": {
            "pg_host":     "localhost",
            "pg_database": "prod_db",
            "pg_username": "admin",
            "pg_password": "secret",
            "pg_table":    "users",
            "row_limit":   50,
            "bq_project":  "my-project",
            "bq_dataset":  "analytics",
            "bq_table":    "users_export",
            "write_mode":  "append",
        },
    }),
)

# ──────────────────────────────────────────────────────────────
separator("TEST 8 — Direct migration: CSV → SQLite")
# ──────────────────────────────────────────────────────────────
check(
    "POST /api/migrate — csv_to_sqlite",
    requests.post(f"{BASE}/api/migrate", json={
        "migration_type": "csv_to_sqlite",
        "session_id":     "test_session_migrate",
        "config": {
            "file_path":  "data/orders.csv",
            "table_name": "orders",
            "db_path":    "./output/test.db",
            "if_exists":  "replace",
        },
    }),
)

# ──────────────────────────────────────────────────────────────
separator("TEST 9 — Direct migration: S3 → Snowflake")
# ──────────────────────────────────────────────────────────────
check(
    "POST /api/migrate — s3_to_snowflake",
    requests.post(f"{BASE}/api/migrate", json={
        "migration_type": "s3_to_snowflake",
        "session_id":     "test_session_migrate",
        "config": {
            "bucket_name":  "my-data-bucket",
            "object_key":   "exports/events_2024.csv",
            "file_format":  "csv",
            "aws_region":   "us-east-1",
            "sf_account":   "myaccount",
            "sf_warehouse": "COMPUTE_WH",
            "sf_database":  "ANALYTICS",
            "sf_schema":    "PUBLIC",
            "sf_table":     "events",
            "sf_username":  "sf_user",
            "sf_password":  "sf_pass",
        },
    }),
)

# ──────────────────────────────────────────────────────────────
separator("TEST 10 — Direct migration: Mongo → S3")
# ──────────────────────────────────────────────────────────────
check(
    "POST /api/migrate — mongo_to_s3",
    requests.post(f"{BASE}/api/migrate", json={
        "migration_type": "mongo_to_s3",
        "session_id":     "test_session_migrate",
        "config": {
            "mongo_host":       "localhost",
            "mongo_database":   "crm",
            "mongo_collection": "customers",
            "s3_bucket":        "my-archive-bucket",
            "s3_key":           "exports/customers.json",
            "aws_region":       "us-east-1",
            "file_format":      "json",
        },
    }),
)

# ──────────────────────────────────────────────────────────────
separator("TEST 11 — Invalid migration type (expect 400)")
# ──────────────────────────────────────────────────────────────
check(
    "POST /api/migrate — invalid type",
    requests.post(f"{BASE}/api/migrate", json={
        "migration_type": "oracle_to_redis",
        "session_id":     "test_session_migrate",
        "config":         {},
    }),
    expected_status=400,
)

# ──────────────────────────────────────────────────────────────
separator("TEST 12 — Output file listing")
# ──────────────────────────────────────────────────────────────
check("GET /api/output — list migrated files", requests.get(f"{BASE}/api/output"))

# ──────────────────────────────────────────────────────────────
separator("TEST 13 — Full conversation migration flow")
# ──────────────────────────────────────────────────────────────
session_id = "test_full_flow"
messages = [
    "I want to migrate data from MongoDB to S3",
    "Host is localhost, database is analytics, collection is events",
    "Bucket is my-bucket, key is exports/events.json, region is us-east-1",
    "yes",
]

for msg in messages:
    time.sleep(0.5)
    check(
        f"POST /api/chat — '{msg[:45]}...'",
        requests.post(f"{BASE}/api/chat", json={
            "message":    msg,
            "session_id": session_id,
        }),
    )

# ──────────────────────────────────────────────────────────────
separator("SUMMARY")
# ──────────────────────────────────────────────────────────────
print("\n  All tests completed.")
print("  Check output above for ✅ (pass) and ❌ (fail)")
print(f"\n  Interactive API docs: {BASE}/docs")
print(f"  Output files:         {BASE}/api/output")
print(f"  File downloads:       {BASE}/files/<filename>\n")
