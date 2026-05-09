from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceConfig:
    name: str
    robots_url: str | None
    sitemap_index_url: str | None
    sitemap_url_contains: str | None
    user_agent: str
    stop_when_page_older_than_window: bool
