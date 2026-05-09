from __future__ import annotations

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from domain import SitemapFilter, SitemapItem, SourceConfig
from infrastructure.sitemap_gateway import SitemapGateway, parse_datetime


class ListRecentSitemapItems:
    def __init__(self, sitemap_gateway: SitemapGateway) -> None:
        self.sitemap_gateway = sitemap_gateway

    def execute(
        self,
        config: SourceConfig,
        hours: float,
        local_tz: ZoneInfo,
        max_pages: int | None,
        include_undated: bool,
        item_filter: SitemapFilter | None = None,
    ) -> list[SitemapItem]:
        item_filter = item_filter or SitemapFilter()
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        entry_url = self.sitemap_gateway.entry_sitemap_url(config)
        items: list[SitemapItem] = []

        for page_url in self.sitemap_gateway.child_sitemap_pages(
            entry_url,
            config,
            max_pages,
        ):
            page_items = self.sitemap_gateway.items_from_page(page_url, config, local_tz)
            page_dates = [
                published_dt
                for published_dt in (
                    parse_datetime(item.published_utc) for item in page_items
                )
                if published_dt is not None
            ]

            for item in page_items:
                item_dt = parse_datetime(item.published_utc)
                if item_dt is not None:
                    if item_dt >= cutoff and matches_filter(item, item_filter):
                        items.append(item)
                elif include_undated and matches_filter(item, item_filter):
                    items.append(item)

            if (
                config.stop_when_page_older_than_window
                and page_dates
                and max(page_dates) < cutoff
            ):
                break

        items.sort(key=lambda item: item.published_utc or "", reverse=True)
        return items


def matches_filter(item: SitemapItem, item_filter: SitemapFilter) -> bool:
    section = item.category or url_section(item.url)

    if item_filter.include_sections and section not in item_filter.include_sections:
        return False

    if item_filter.exclude_sections and section in item_filter.exclude_sections:
        return False

    if item_filter.only_with_tickers and not item.stock_tickers:
        return False

    if item_filter.exclude_non_english and is_non_english_path(item.url):
        return False

    if item_filter.query and item_filter.query.lower() not in searchable_text(item):
        return False

    return True


def url_section(url: str) -> str:
    path = url.split("://", 1)[-1].split("/", 1)
    if len(path) < 2:
        return ""
    first_segment = path[1].split("/", 1)[0].lower()
    return first_segment


def is_non_english_path(url: str) -> bool:
    return url_section(url) in {"es", "fr", "pt", "de", "it"}


def searchable_text(item: SitemapItem) -> str:
    return " ".join(
        value
        for value in [
            item.title,
            item.url,
            item.stock_tickers,
            item.publisher,
            item.language,
        ]
        if value
    ).lower()
