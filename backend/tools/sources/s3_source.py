import pandas as pd
from .base_source import BaseSource
from ..generators.data_factory import generate


class S3Source(BaseSource):
    source_type = "s3"

    def read(self, bucket_name: str, object_key: str, file_format: str = "csv",
             aws_region: str = "us-east-1", **kwargs) -> pd.DataFrame:

        print(f"[s3] Simulating download: s3://{bucket_name}/{object_key} ({file_format})")
        profile = _infer_profile(object_key)
        df = generate(profile=profile, row_count=300)
        print(f"[s3] Downloaded {len(df)} rows (profile: {profile})")
        return df


def _infer_profile(object_key: str) -> str:
    from ..generators.schema_profiles import PROFILES
    key = object_key.lower()
    for profile in PROFILES:
        if profile in key:
            return profile
    return "events"