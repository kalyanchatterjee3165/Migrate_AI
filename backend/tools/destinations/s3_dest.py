import pandas as pd
from .base_destination import BaseDestination


class S3Dest(BaseDestination):
    dest_type = "s3"

    def write(self, df: pd.DataFrame, s3_bucket: str, s3_key: str,
              file_format: str = "json", aws_region: str = "us-east-1",
              **kwargs) -> dict:

        safe_key = s3_key.replace("/", "_")
        filename = f"s3_{s3_bucket}_{safe_key}.{file_format}"
        output_path = self._save_to_output(df, filename, fmt=file_format)

        print(f"[s3] Simulating upload → s3://{s3_bucket}/{s3_key} "
              f"({file_format}) — {len(df)} rows")

        return {
            "rows_written": len(df),
            "destination":  f"s3://{s3_bucket}/{s3_key}",
            "file_format":  file_format,
            "output_path":  output_path,
        }