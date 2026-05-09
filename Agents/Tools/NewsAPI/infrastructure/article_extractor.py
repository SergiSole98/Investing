from __future__ import annotations

from dataclasses import dataclass

import trafilatura


@dataclass(frozen=True)
class ExtractedArticle:
    text: str | None
    char_count: int


class ArticleExtractor:
    def __init__(self, min_chars: int = 250) -> None:
        self.min_chars = min_chars

    def extract(self, html: str, url: str | None = None) -> ExtractedArticle:
        text = trafilatura.extract(
            html,
            url=url,
            include_comments=False,
            include_tables=False,
            favor_recall=True,
        )
        if text is None:
            return ExtractedArticle(text=None, char_count=0)

        cleaned = text.strip()
        if len(cleaned) < self.min_chars:
            return ExtractedArticle(text=None, char_count=len(cleaned))

        return ExtractedArticle(text=cleaned, char_count=len(cleaned))
