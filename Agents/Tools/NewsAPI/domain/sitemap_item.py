from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SitemapItem:
    source: str
    category: str | None
    published_utc: str | None
    published_local: str | None
    lastmod_utc: str | None
    changefreq: str | None
    priority: str | None
    title: str | None
    url: str
    publisher: str | None
    language: str | None
    keywords: str | None
    stock_tickers: str | None
    image_url: str | None
    image_caption: str | None
