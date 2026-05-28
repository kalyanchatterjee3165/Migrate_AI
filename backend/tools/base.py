from abc import ABC, abstractmethod


class BaseTool(ABC):
    """Minimal interface every migration tool must satisfy."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique snake_case tool name matching the registry key."""

    @abstractmethod
    def run(self, **kwargs) -> dict:
        """Execute the tool and return a result dict with at minimum: rows_processed."""