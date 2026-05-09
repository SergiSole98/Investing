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
        repo_dir = self.base_dir / "data" / source_slug
        repo_dir.mkdir(parents=True, exist_ok=True)
        repo_path = repo_dir / f"{source_slug}-news.json"

        existing = self._read(repo_path)
        existing_by_url = {
            item["url"]: item
            for item in existing.get("items", [])
            if item.get("url")
        }

        today_prefix = datetime.now(timezone.utc).strftime("%d%m%Y")
        next_seq = self._next_seq_for_prefix(existing_by_url.values(), today_prefix)

        by_url = {}
        created = 0
        for item in items:
            existing_item = existing_by_url.get(item.url)
            data = {**existing_item, **asdict(item)} if existing_item else asdict(item)
            data["stored_at_utc"] = datetime.now(timezone.utc).isoformat().replace(
                "+00:00",
                "Z",
            )
            if data["url"] not in existing_by_url:
                created += 1
                data = {"id": f"{today_prefix}-{next_seq}", **data}
                next_seq += 1
            else:
                existing_id = existing_by_url[data["url"]].get("id")
                if existing_id:
                    data = {"id": existing_id, **data}
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

    @staticmethod
    def _next_seq_for_prefix(items, prefix: str) -> int:
        max_seq = 0
        for item in items:
            existing_id = item.get("id")
            if not isinstance(existing_id, str) or not existing_id.startswith(f"{prefix}-"):
                continue
            try:
                seq = int(existing_id.split("-", 1)[1])
            except ValueError:
                continue
            if seq > max_seq:
                max_seq = seq
        return max_seq + 1
