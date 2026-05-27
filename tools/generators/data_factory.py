import pandas as pd
from .schema_profiles import PROFILES, DEFAULT_PROFILE


def generate(profile: str = DEFAULT_PROFILE, row_count: int = 100) -> pd.DataFrame:
    """
    Generate a fake DataFrame for the given profile.

    Args:
        profile:   Name of the schema profile (users, orders, events, products, transactions)
        row_count: Number of rows to generate

    Returns:
        A pandas DataFrame with realistic fake data.

    Raises:
        ValueError: If the profile name is not recognised.
    """
    if profile not in PROFILES:
        available = ", ".join(PROFILES.keys())
        raise ValueError(f"Unknown profile '{profile}'. Available: {available}")

    builder = PROFILES[profile]
    rows = [builder(i) for i in range(row_count)]
    return pd.DataFrame(rows)


def available_profiles() -> list[str]:
    return list(PROFILES.keys())