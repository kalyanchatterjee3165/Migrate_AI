import pandas as pd
from .base_destination import BaseDestination


class SnowflakeDest(BaseDestination):
    dest_type = "snowflake"

    def write(self, df: pd.DataFrame, sf_account: str, sf_warehouse: str,
              sf_database: str, sf_schema: str, sf_table: str,
              sf_username: str, sf_password: str, **kwargs) -> dict:

        filename = f"sf_{sf_database}_{sf_schema}_{sf_table}.csv"
        output_path = self._save_to_output(df, filename, fmt="csv")

        print(f"[snowflake] Simulating COPY INTO {sf_database}.{sf_schema}.{sf_table} "
              f"— {len(df)} rows via {sf_warehouse}")

        return {
            "rows_written": len(df),
            "destination":  f"{sf_account}/{sf_database}.{sf_schema}.{sf_table}",
            "warehouse":    sf_warehouse,
            "output_path":  output_path,
        }