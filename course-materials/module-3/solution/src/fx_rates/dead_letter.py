"""In-memory dead-letter tracking for failed currency pair resolutions."""

from dataclasses import dataclass, field


@dataclass
class DeadLetter:
    """Stores failed items and their error causes without crashing the pipeline."""

    entries: list[dict[str, str]] = field(default_factory=list)

    def add(self, identifier: str, reason: str) -> None:
        self.entries.append({"identifier": identifier, "reason": reason})

    def __len__(self) -> int:
        return len(self.entries)