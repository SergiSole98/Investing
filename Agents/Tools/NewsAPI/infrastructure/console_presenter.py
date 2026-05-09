from __future__ import annotations

import csv
import json
import textwrap
from dataclasses import asdict
from io import StringIO

from domain import SitemapItem


def print_items(items: list[SitemapItem], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps([asdict(item) for item in items], indent=2, ensure_ascii=False))
    elif output_format == "csv":
        print_csv(items)
    else:
        print_table(items)


def print_csv(items: list[SitemapItem]) -> None:
    output = StringIO()
    fieldnames = list(SitemapItem.__dataclass_fields__)
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for item in items:
        writer.writerow(asdict(item))
    print(output.getvalue(), end="")


def print_table(items: list[SitemapItem]) -> None:
    print(f"count={len(items)}")
    print("source | category | published_local | published_utc | title | stock_tickers | url")
    print("-" * 140)
    for item in items:
        title = textwrap.shorten(item.title or "", width=80, placeholder="...")
        print(
            f"{item.source} | {item.category or ''} | {item.published_local or ''} | "
            f"{item.published_utc or ''} | {title} | "
            f"{item.stock_tickers or ''} | {item.url}"
        )
