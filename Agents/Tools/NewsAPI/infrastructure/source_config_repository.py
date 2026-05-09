from __future__ import annotations

import json
from pathlib import Path

from domain import SourceConfig


class SourceConfigRepository:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir

    def load(self, source: str, explicit_config_path: str | None = None) -> SourceConfig:
        config_path = (
            Path(explicit_config_path)
            if explicit_config_path
            else self.base_dir / source / "config.json"
        )
        raw = json.loads(config_path.read_text(encoding="utf-8"))

        return SourceConfig(
            name=raw["name"],
            robots_url=raw.get("robots_url"),
            sitemap_index_url=raw.get("sitemap_index_url"),
            sitemap_url_contains=raw.get("sitemap_url_contains"),
            user_agent=raw.get(
                "user_agent",
                "Mozilla/5.0 (compatible; investing-sitemap-probe/1.0)",
            ),
            stop_when_page_older_than_window=bool(
                raw.get("stop_when_page_older_than_window", True)
            ),
        )
