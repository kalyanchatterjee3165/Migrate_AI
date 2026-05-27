import os
import time
import pandas as pd
from abc import ABC, abstractmethod

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "./output")

class BaseDestination(ABC):

    dest_type: str = "base"

    def connect(self, **kwargs) -> None:
        time.sleep(0.3)
        print(f"[{self.dest_type}] Connected (simulated)")

    def disconnect(self) -> None:
        time.sleep(0.1)
        print(f"[{self.dest_type}] Disconnected (simulated)")

    @abstractmethod
    def write(self, df: pd.DataFrame, **kwargs) -> dict:
        ...

    def save(self, df: pd.DataFrame, **kwargs) -> dict:
        self.connect(**kwargs)
        try:
            result = self.write(df, **kwargs)
        finally:
            self.disconnect()
        return result

    def _save_to_output(self, df: pd.DataFrame, filename: str, fmt: str = "csv") -> str:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        path = os.path.join(OUTPUT_DIR, filename)
        if fmt == "json":
            df.to_json(path, orient="records", indent=2)
        else:
            df.to_csv(path, index=False)
        return path