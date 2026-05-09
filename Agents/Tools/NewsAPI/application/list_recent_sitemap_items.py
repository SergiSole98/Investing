from __future__ import annotations

import dataclasses
import re
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
        items_by_url: dict[str, SitemapItem] = {}

        for entry_url in self.sitemap_gateway.entry_sitemap_urls(config):
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
                    existing = items_by_url.get(item.url)
                    items_by_url[item.url] = (
                        merge_items(existing, item) if existing else item
                    )

                if (
                    config.stop_when_page_older_than_window
                    and page_dates
                    and max(page_dates) < cutoff
                ):
                    break

        items: list[SitemapItem] = []
        for item in items_by_url.values():
            item_dt = parse_datetime(item.published_utc)
            if item_dt is not None:
                if item_dt >= cutoff and matches_filter(item, item_filter):
                    items.append(item)
            elif include_undated and matches_filter(item, item_filter):
                items.append(item)

        items.sort(key=lambda item: item.published_utc or "", reverse=True)
        return items


def merge_items(existing: SitemapItem, new: SitemapItem) -> SitemapItem:
    merged = {
        field.name: getattr(existing, field.name) or getattr(new, field.name)
        for field in dataclasses.fields(SitemapItem)
    }
    return SitemapItem(**merged)


def matches_filter(item: SitemapItem, item_filter: SitemapFilter) -> bool:
    section = item.category or url_section(item.url)

    if not section:
        return False

    if not is_dated_article_url(item.url):
        return False

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


def is_dated_article_url(url: str) -> bool:
    return re.search(r"-20\d{2}-\d{2}-\d{2}/?$", url) is not None


def searchable_text(item: SitemapItem) -> str:
    return " ".join(
        value
        for value in [
            item.title,
            item.url,
            item.stock_tickers,
            item.publisher,
        ]
        if value
    ).lower()
