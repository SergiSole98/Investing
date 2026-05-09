from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SitemapFilter:
    include_sections: tuple[str, ...] = ()
    exclude_sections: tuple[str, ...] = ()
    query: str | None = None
    only_with_tickers: bool = False
    exclude_non_english: bool = False
