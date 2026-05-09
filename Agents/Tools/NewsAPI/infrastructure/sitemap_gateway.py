from __future__ import annotations

from datetime import datetime
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

from domain import SitemapItem, SourceConfig
from infrastructure.http_client import HttpClient


XML_NS = {
    "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "news": "http://www.google.com/schemas/sitemap-news/0.9",
}


class SitemapGateway:
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    def entry_sitemap_urls(self, config: SourceConfig) -> list[str]:
        if config.sitemap_index_url:
            return [config.sitemap_index_url]

        sitemap_urls = self._robots_sitemaps(config)
        if config.sitemap_url_contains:
            sitemap_urls = [
                url for url in sitemap_urls if config.sitemap_url_contains in url
            ]

        if sitemap_urls:
            return sitemap_urls

        if config.robots_url:
            parsed = urlparse(config.robots_url)
            return [urljoin(f"{parsed.scheme}://{parsed.netloc}", "/sitemap.xml")]

        raise ValueError("Source config must define sitemap_index_url or robots_url")

    def child_sitemap_pages(
        self,
        entry_url: str,
        config: SourceConfig,
        max_pages: int | None,
    ) -> list[str]:
        root = self._fetch_xml(entry_url, config)
        if root.tag.endswith("sitemapindex"):
            pages = [
                loc.text.strip()
                for loc in root.findall(".//sm:loc", XML_NS)
                if loc.text and loc.text.strip()
            ]
        else:
            pages = [entry_url]

        if max_pages is not None:
            return pages[: max(0, max_pages)]
        return pages

    def items_from_page(
        self,
        page_url: str,
        config: SourceConfig,
        local_tz: ZoneInfo,
    ) -> list[SitemapItem]:
        root = self._fetch_xml(page_url, config)
        items = []
        for url_el in root.findall("sm:url", XML_NS):
            item = self._parse_item(url_el, config.name, local_tz)
            if item is not None:
                items.append(item)
        return items

    def _robots_sitemaps(self, config: SourceConfig) -> list[str]:
        if not config.robots_url:
            return []

        robots_txt = self.http_client.fetch_text(config.robots_url, config.user_agent)
        urls = []
        for line in robots_txt.splitlines():
            key, _, value = line.partition(":")
            if key.strip().lower() == "sitemap":
                url = value.strip()
                if url:
                    urls.append(url)
        return urls

    def _fetch_xml(self, url: str, config: SourceConfig) -> ET.Element:
        xml_text = self.http_client.fetch_text(url, config.user_agent)
        return ET.fromstring(xml_text.encode("utf-8"))

    def _parse_item(
        self,
        url_el: ET.Element,
        source: str,
        local_tz: ZoneInfo,
    ) -> SitemapItem | None:
        url = url_el.findtext("sm:loc", default="", namespaces=XML_NS).strip()
        if not url:
            return None

        published_raw = self._first_text(
            url_el,
            ["news:news/news:publication_date", "sm:lastmod"],
        )
        published_dt = parse_datetime(published_raw)
        lastmod_dt = parse_datetime(self._first_text(url_el, ["sm:lastmod"]))

        return SitemapItem(
            source=source,
            category=url_section(url),
            published_utc=format_utc(published_dt),
            published_local=published_dt.astimezone(local_tz).isoformat()
            if published_dt
            else None,
            lastmod_utc=format_utc(lastmod_dt),
            changefreq=self._first_text(url_el, ["sm:changefreq"]),
            priority=self._first_text(url_el, ["sm:priority"]),
            title=self._first_text(url_el, ["news:news/news:title"]),
            url=url,
            publisher=self._first_text(url_el, ["news:news/news:publication/news:name"]),
            keywords=self._first_text(url_el, ["news:news/news:keywords"]),
            stock_tickers=self._first_text(url_el, ["news:news/news:stock_tickers"]),
        )

    def _first_text(self, url_el: ET.Element, paths: list[str]) -> str | None:
        for path in paths:
            value = url_el.findtext(path, default="", namespaces=XML_NS).strip()
            if value:
                return value
        return None


def parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def format_utc(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat().replace("+00:00", "Z")


def url_section(url: str) -> str | None:
    path = url.split("://", 1)[-1].split("/", 1)
    if len(path) < 2:
        return None
    section = path[1].split("/", 1)[0].lower()
    return section or None
