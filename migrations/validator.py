import pandas as pd


class MigrationValidator:
    """
    Simulates pre- and post-migration validation checks.
    Returns structured results the executor includes in its summary.
    """

    def pre_check(self, df: pd.DataFrame) -> dict:
        """Validate the source DataFrame before writing."""
        issues = []

        if df.empty:
            issues.append("Source DataFrame is empty.")

        null_counts = df.isnull().sum()
        high_null_cols = null_counts[null_counts > len(df) * 0.5].index.tolist()
        if high_null_cols:
            issues.append(f"High null rate (>50%) in columns: {high_null_cols}")

        return {
            "passed":      len(issues) == 0,
            "row_count":   len(df),
            "col_count":   len(df.columns),
            "columns":     list(df.columns),
            "null_counts": null_counts.to_dict(),
            "issues":      issues,
        }

    def post_check(self, source_df: pd.DataFrame, rows_written: int) -> dict:
        """Compare source row count against what was written."""
        source_rows = len(source_df)
        match = source_rows == rows_written
        return {
            "passed":        match,
            "source_rows":   source_rows,
            "written_rows":  rows_written,
            "discrepancy":   source_rows - rows_written,
        }