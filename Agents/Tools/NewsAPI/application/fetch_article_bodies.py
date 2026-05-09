from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from infrastructure.article_extractor import ArticleExtractor
from infrastructure.article_fetcher import ArticleFetcher


class FetchArticleBodies:
    """Reads <source>-news.json for a source, fills missing article bodies in place."""

    def __init__(
        self,
        base_dir: Path,
        fetcher: ArticleFetcher,
        extractor: ArticleExtractor,
    ) -> None:
        self.base_dir = base_dir
        self.fetcher = fetcher
        self.extractor = extractor

    def execute(
        self,
        source_slug: str,
        limit: int | None = None,
        retry_failed: bool = False,
        only_urls: Iterable[str] | None = None,
    ) -> dict:
        repo_path = self._repo_path(source_slug)
        if not repo_path.exists():
            raise FileNotFoundError(f"{source_slug}-news.json not found at {repo_path}")

        data = json.loads(repo_path.read_text(encoding="utf-8"))
        items = data.get("items", [])
        target_urls = set(only_urls) if only_urls else None

        ok = 0
        blocked = 0
        errored = 0
        attempted = 0

        for item in items:
            url = item.get("url")
            if not url:
                continue
            if target_urls is not None and url not in target_urls:
                continue
            if not self._needs_fetch(item, retry_failed):
                continue
            if limit is not None and attempted >= limit:
                break

            attempted += 1
            print(f"[{attempted}] fetching {url}")
            result = self.fetcher.fetch(url)
            now_iso = self._now_iso()

            item["body_fetch_attempted_at_utc"] = now_iso
            item["body_fetch_method"] = result.method
            item["body_fetch_http_status"] = result.http_status

            if result.status == "ok" and result.html:
                extracted = self.extractor.extract(result.html, url=url)
                if extracted.text:
                    item["body_text"] = extracted.text
                    item["body_char_count"] = extracted.char_count
                    item["body_fetch_status"] = "ok"
                    item["body_fetch_error"] = None
                    ok += 1
                    print(f"    ok via {result.method} ({extracted.char_count} chars)")
                else:
                    item["body_fetch_status"] = "extract_empty"
                    item["body_fetch_error"] = (
                        f"trafilatura returned <{self.extractor.min_chars} chars"
                    )
                    item["body_text"] = None
                    item["body_char_count"] = extracted.char_count
                    errored += 1
                    print(f"    extract_empty via {result.method}")
            elif result.status == "blocked":
                item["body_fetch_status"] = "blocked"
                item["body_fetch_error"] = None
                item["body_text"] = None
                blocked += 1
                print(f"    blocked via {result.method} (http={result.http_status})")
            else:
                item["body_fetch_status"] = "error"
                item["body_fetch_error"] = result.error
                item["body_text"] = None
                errored += 1
                print(f"    error via {result.method}: {result.error}")

        data["updated_at_utc"] = self._now_iso()
        data["count"] = len(items)
        data["items"] = items
        repo_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

        return {
            "repo_path": str(repo_path),
            "attempted": attempted,
            "ok": ok,
            "blocked": blocked,
            "errored": errored,
            "total_items": len(items),
        }

    def _repo_path(self, source_slug: str) -> Path:
        return self.base_dir / "data" / source_slug / f"{source_slug}-news.json"

    @staticmethod
    def _needs_fetch(item: dict, retry_failed: bool) -> bool:
        status = item.get("body_fetch_status")
        if status is None:
            return True
        if status == "ok":
            return False
        return retry_failed

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
