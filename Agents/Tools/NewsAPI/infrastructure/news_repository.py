from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from domain import SitemapItem


class NewsRepository:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir

    def upsert_many(self, source_slug: str, items: list[SitemapItem]) -> tuple[Path, int, int]:
        repo_dir = self.base_dir / "domain" / "newsRepo" / source_slug
        repo_dir.mkdir(parents=True, exist_ok=True)
        repo_path = repo_dir / "news.json"

        existing = self._read(repo_path)
        by_url = {
            item["url"]: item
            for item in existing.get("items", [])
            if item.get("url")
        }

        created = 0
        for item in items:
            data = asdict(item)
            data["stored_at_utc"] = datetime.now(timezone.utc).isoformat().replace(
                "+00:00",
                "Z",
            )
            if data["url"] not in by_url:
                created += 1
            by_url[data["url"]] = data

        merged_items = sorted(
            by_url.values(),
            key=lambda data: data.get("published_utc") or "",
            reverse=True,
        )
        output = {
            "source": source_slug,
            "updated_at_utc": datetime.now(timezone.utc).isoformat().replace(
                "+00:00",
                "Z",
            ),
            "count": len(merged_items),
            "items": merged_items,
        }
        repo_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
        return repo_path, created, len(merged_items)

    def _read(self, repo_path: Path) -> dict:
        if not repo_path.exists():
            return {"items": []}
        return json.loads(repo_path.read_text(encoding="utf-8"))
