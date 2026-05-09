#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from application import FetchArticleBodies
from infrastructure import ArticleExtractor, ArticleFetcher


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fill article bodies in <source>-news.json using curl_cffi -> patchright fallback."
    )
    parser.add_argument("--source", default="reuters", help="Source slug. Default: reuters.")
    parser.add_argument("--limit", type=int, default=None, help="Max URLs to fetch this run.")
    parser.add_argument(
        "--retry-failed",
        action="store_true",
        help="Re-attempt items previously marked blocked/error. By default only items without body are tried.",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Skip patchright fallback (curl_cffi only).",
    )
    parser.add_argument(
        "--url",
        action="append",
        default=None,
        help="Restrict to one specific URL. Can be repeated.",
    )
    parser.add_argument(
        "--min-chars",
        type=int,
        default=250,
        help="Minimum extracted chars to consider extraction successful.",
    )
    parser.add_argument(
        "--browser-wait-ms",
        type=int,
        default=4000,
        help="Idle wait after page load in patchright before reading content.",
    )
    parser.add_argument(
        "--scrapingbee-key",
        default=os.environ.get("SCRAPINGBEE_API_KEY"),
        help="ScrapingBee API key. Defaults to SCRAPINGBEE_API_KEY env var. "
        "When set, used as third fallback after curl_cffi and patchright.",
    )
    parser.add_argument(
        "--no-scrapingbee-stealth",
        action="store_true",
        help="Disable ScrapingBee stealth_proxy (cheaper but does not bypass DataDome).",
    )
    parser.add_argument(
        "--no-scrapingbee-js",
        action="store_true",
        help="Disable ScrapingBee JS rendering (cheaper, may break SPA-rendered articles).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_dir = Path(__file__).resolve().parent
    fetcher = ArticleFetcher(
        enable_browser_fallback=not args.no_browser,
        browser_wait_ms=args.browser_wait_ms,
        scrapingbee_api_key=args.scrapingbee_key,
        scrapingbee_stealth=not args.no_scrapingbee_stealth,
        scrapingbee_render_js=not args.no_scrapingbee_js,
    )
    extractor = ArticleExtractor(min_chars=args.min_chars)
    use_case = FetchArticleBodies(base_dir, fetcher, extractor)

    try:
        summary = use_case.execute(
            source_slug=args.source,
            limit=args.limit,
            retry_failed=args.retry_failed,
            only_urls=args.url,
        )
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print()
    print(
        "summary: attempted={attempted} ok={ok} blocked={blocked} "
        "errored={errored} total_items={total_items}".format(**summary)
    )
    print(f"repo={summary['repo_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
