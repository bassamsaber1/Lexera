from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JsonStorage:
    """Simple JSON storage helper for file-based persistence."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self, default: Any) -> Any:
        if not self.path.exists():
            return default
        with self.path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, payload: Any) -> None:
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)
