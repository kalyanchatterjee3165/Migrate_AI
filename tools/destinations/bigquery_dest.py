import pandas as pd
from .base_destination import BaseDestination


class BigQueryDest(BaseDestination):
    dest_type = "bigquery"

    def write(self, df: pd.DataFrame, bq_project: str, bq_dataset: str,
              bq_table: str, write_mode: str = "append", **kwargs) -> dict:

        filename = f"bq_{bq_project}_{bq_dataset}_{bq_table}.csv"
        output_path = self._save_to_output(df, filename, fmt="csv")

        print(f"[bigquery] Simulating load → {bq_project}.{bq_dataset}.{bq_table} "
              f"({write_mode}) — {len(df)} rows")

        return {
            "rows_written":  len(df),
            "destination":   f"{bq_project}.{bq_dataset}.{bq_table}",
            "write_mode":    write_mode,
            "output_path":   output_path,
        }