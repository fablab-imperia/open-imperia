from dataclasses import dataclass, field
from typing import Any


@dataclass
class Dataset:
    name: str
    title: str
    notes: str = ""
    tags: list[dict[str, str]] = field(default_factory=list)
    resources: list[dict[str, Any]] = field(default_factory=list)
    extras: list[dict[str, str]] = field(default_factory=list)
