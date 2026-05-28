import pandas as pd
from .base_source import BaseSource
from ..generators.data_factory import generate


class CsvSource(BaseSource):
    source_type = "csv"

    def read(self, file_path: str, delimiter: str = ",",
             has_header: bool = True, **kwargs) -> pd.DataFrame:

        print(f"[csv] Simulating read of: {file_path}")
        # Infer profile from filename, fall back to users
        profile = _infer_profile(file_path)
        df = generate(profile=profile, row_count=150)
        print(f"[csv] Read {len(df)} rows (profile: {profile})")
        return df


def _infer_profile(file_path: str) -> str:
    from ..generators.schema_profiles import PROFILES
    name = file_path.lower()
    for profile in PROFILES:
        if profile in name:
            return profile
    return "users"