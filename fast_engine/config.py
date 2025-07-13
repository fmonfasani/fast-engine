from dataclasses import dataclass


@dataclass
class Config:
    """Configuration for the engine."""

    name: str = "fast-engine"
