import pandas as pd
from .base_source import BaseSource
from ..generators.data_factory import generate


class MongoSource(BaseSource):
    source_type = "mongo"

    def read(self, mongo_host: str, mongo_database: str, mongo_collection: str,
             mongo_port: int = 27017, mongo_username: str = "",
             mongo_password: str = "", **kwargs) -> pd.DataFrame:

        print(f"[mongo] Simulating: db.{mongo_collection}.find({{}}) on {mongo_host}/{mongo_database}")
        profile = _infer_profile(mongo_collection)
        df = generate(profile=profile, row_count=250)
        print(f"[mongo] Fetched {len(df)} documents (profile: {profile})")
        return df


def _infer_profile(collection: str) -> str:
    from ..generators.schema_profiles import PROFILES
    name = collection.lower()
    for profile in PROFILES:
        if profile in name:
            return profile
    return "users"