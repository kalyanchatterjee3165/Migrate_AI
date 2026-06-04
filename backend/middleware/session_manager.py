import threading
from typing import Dict

from llm.agent import MigrationAgent
from llm.tool_registry import build_default_registry
from migrations.executor import (
    migrate_postgres_to_bigquery,
    migrate_csv_to_sqlite,
    migrate_s3_to_snowflake,
    migrate_mongo_to_s3,
)


class SessionManager:
    """
    Thread-safe registry of per-session MigrationAgent instances.
    Each session_id gets its own agent with isolated conversation history.
    """

    def __init__(self):
        self._sessions: Dict[str, MigrationAgent] = {}
        self._lock = threading.Lock()
        self._registry = self._build_registry()

    def _build_registry(self):
        return build_default_registry(
            migrate_pg_to_bq      = migrate_postgres_to_bigquery,
            migrate_csv_to_sqlite = migrate_csv_to_sqlite,
            migrate_s3_to_sf      = migrate_s3_to_snowflake,
            migrate_mongo_to_s3   = migrate_mongo_to_s3,
        )

    def get_agent(self, session_id: str) -> MigrationAgent:
        """Return the existing agent for this session, or create a new one."""
        with self._lock:
            if session_id not in self._sessions:
                self._sessions[session_id] = MigrationAgent(
                    registry=self._registry
                )
            return self._sessions[session_id]

    def reset_session(self, session_id: str) -> None:
        """Clear agent conversation history for this session."""
        with self._lock:
            if session_id in self._sessions:
                self._sessions[session_id].reset()

    def delete_session(self, session_id: str) -> None:
        """Completely remove a session and free its memory."""
        with self._lock:
            self._sessions.pop(session_id, None)

    def active_count(self) -> int:
        with self._lock:
            return len(self._sessions)

    def list_sessions(self) -> list:
        with self._lock:
            return list(self._sessions.keys())


# Global singleton — one per server process
session_manager = SessionManager()
