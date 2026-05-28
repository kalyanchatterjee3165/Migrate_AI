import pandas as pd
from .base_source import BaseSource
from ..generators.data_factory import generate


class PostgresSource(BaseSource):
    source_type = "postgres"

    def read(self, pg_host: str, pg_database: str, pg_username: str,
             pg_password: str, pg_table: str, pg_port: int = 5432,
             row_limit: int = 200, **kwargs) -> pd.DataFrame:

        # Infer a sensible profile from the table name
        profile = _infer_profile(pg_table)
        rows = min(row_limit or 200, 500)

        print(f"[postgres] Simulating: SELECT * FROM {pg_table} LIMIT {rows}")
        df = generate(profile=profile, row_count=rows)
        print(f"[postgres] Fetched {len(df)} rows from '{pg_table}' (profile: {profile})")
        return df


def _infer_profile(table_name: str) -> str:
    from ..generators.schema_profiles import PROFILES
    name = table_name.lower()
    for profile in PROFILES:
        if profile in name:
            return profile
    return "users"