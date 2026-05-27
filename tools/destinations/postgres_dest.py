import pandas as pd
from .base_destination import BaseDestination


class PostgresDest(BaseDestination):
    dest_type = "postgres"

    def write(self, df: pd.DataFrame, pg_host: str, pg_database: str,
              pg_username: str, pg_password: str, pg_table: str,
              pg_port: int = 5432, if_exists: str = "append", **kwargs) -> dict:

        filename = f"pg_{pg_database}_{pg_table}.csv"
        output_path = self._save_to_output(df, filename, fmt="csv")

        print(f"[postgres] Simulating INSERT INTO {pg_table} — {len(df)} rows "
              f"(if_exists={if_exists})")

        return {
            "rows_written": len(df),
            "destination":  f"{pg_host}/{pg_database}.{pg_table}",
            "if_exists":    if_exists,
            "output_path":  output_path,
        }