from dataclasses import dataclass, field


@dataclass
class MigrationState:
    """
    Holds per-conversation state for a single migration session.
    Gradio creates one instance per user session and passes it around.
    """
    source_type:    str  = ""
    dest_type:      str  = ""
    source_config:  dict = field(default_factory=dict)
    dest_config:    dict = field(default_factory=dict)
    confirmed:      bool = False
    completed:      bool = False

    def reset(self):
        self.source_type   = ""
        self.dest_type     = ""
        self.source_config = {}
        self.dest_config   = {}
        self.confirmed     = False
        self.completed     = False

    def summary(self) -> str:
        return (
            f"Source: {self.source_type or 'unknown'} | "
            f"Dest: {self.dest_type or 'unknown'} | "
            f"Confirmed: {self.confirmed} | "
            f"Done: {self.completed}"
        )