import time
import pandas as pd
from abc import ABC, abstractmethod

class BaseSource(ABC):

    source_type: str = "base"

    def connect(self, **kwargs) -> None:
        time.sleep(0.3)
        print(f"[{self.source_type}] Connected (simulated)")

    def disconnect(self) -> None:
        time.sleep(0.1)
        print(f"[{self.source_type}] Disconnected (simulated)")

    @abstractmethod
    def read(self, **kwargs) -> pd.DataFrame:
        ...

    def fetch(self, **kwargs) -> pd.DataFrame:
        self.connect(**kwargs)
        try:
            df = self.read(**kwargs)
        finally:
            self.disconnect()
        return df