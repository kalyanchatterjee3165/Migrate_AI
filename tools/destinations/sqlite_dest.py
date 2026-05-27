import os
import pandas as pd
from sqlalchemy import create_engine
from .base_destination import BaseDestination

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "./output")


class SQLiteDest(BaseDestination):
    dest_type = "sqlite"

    def write(self, df: pd.DataFrame, db_path: str, table_name: str,
              if_exists: str = "append", **kwargs) -> dict:

        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)

        engine = create_engine(f"sqlite:///{db_path}")
        df.to_sql(table_name, con=engine, if_exists=if_exists, index=False)
        engine.dispose()

        print(f"[sqlite] Wrote {len(df)} rows → {db_path} :: {table_name} "
              f"(if_exists={if_exists})")

        return {
            "rows_written": len(df),
            "table_name":   table_name,
            "db_path":      db_path,
            "if_exists":    if_exists,
            "destination":  f"{db_path}::{table_name}",
            "output_path":  db_path,
        }
