#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

from application import ListRecentSitemapItems
from domain import SitemapFilter
from infrastructure import (
    HttpClient,
    NewsRepository,
    SitemapGateway,
    SourceConfigRepository,
    print_items,
)


DEFAULT_EXCLUDED_SECTIONS = ("sports", "lifestyle")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="List recent URLs from a sitemap source.")
    parser.add_argument(
        "--source",
        default="reuters",
        help="Source folder next to main.py. Default: reuters.",
    )
    parser.add_argument(
        "--config",
        help="Explicit source config JSON path. Overrides --source.",
    )
    parser.add_argument(
        "--hours",
        type=float,
        default=12,
        help="Lookback window in hours. Default: 12.",
    )
    parser.add_argument(
        "--timezone",
        default="Europe/Madrid",
        help="Local timezone for display. Default: Europe/Madrid.",
    )
    parser.add_argument(
        "--format",
        choices=("table", "json", "csv"),
        default="table",
        help="Output format. Default: table.",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Optional limit for sitemap pages read from the sitemap index.",
    )
    parser.add_argument(
        "--include-undated",
        action="store_true",
        help="Include URLs without publication/lastmod date.",
    )
    parser.add_argument(
        "--include-sections",
        help="Comma-separated URL sections to keep, e.g. business,world,technology.",
    )
    parser.add_argument(
        "--exclude-sections",
        help=(
            "Comma-separated URL sections to drop. "
            "Default: sports,lifestyle."
        ),
    )
    parser.add_argument(
        "--query",
        help="Case-insensitive text filter over title, URL, tickers, publisher and language.",
    )
    parser.add_argument(
        "--only-with-tickers",
        action="store_true",
        help="Keep only items that include stock_tickers.",
    )
    parser.add_argument(
        "--include-non-english",
        action="store_true",
        help="Include common non-English URL prefixes such as /es/, /fr/, /pt/, /de/, /it/. Default: English only.",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Do not upsert fetched items into domain/newsRepo/<source>/news.json.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        source_repository = SourceConfigRepository(Path(__file__).resolve().parent)
        config = source_repository.load(args.source, args.config)
        use_case = ListRecentSitemapItems(SitemapGateway(HttpClient()))
        items = use_case.execute(
            config=config,
            hours=args.hours,
            local_tz=ZoneInfo(args.timezone),
            max_pages=args.max_pages,
            include_undated=args.include_undated,
            item_filter=SitemapFilter(
                include_sections=parse_csv_arg(args.include_sections),
                exclude_sections=parse_excluded_sections(args.exclude_sections),
                query=args.query,
                only_with_tickers=args.only_with_tickers,
                exclude_non_english=not args.include_non_english,
            ),
        )
        if not args.no_save:
            repo_path, created, total = NewsRepository(
                Path(__file__).resolve().parent
            ).upsert_many(args.source, items)
            print(f"repo={repo_path} new={created} total={total}")
        print_items(items, args.format)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


def parse_csv_arg(value: str | None) -> tuple[str, ...]:
    if not value:
        return ()
    return tuple(part.strip().lower() for part in value.split(",") if part.strip())


def parse_excluded_sections(value: str | None) -> tuple[str, ...]:
    if value is None:
        return DEFAULT_EXCLUDED_SECTIONS
    return parse_csv_arg(value)


if __name__ == "__main__":
    raise SystemExit(main())
