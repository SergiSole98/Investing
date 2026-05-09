from __future__ import annotations

import ssl
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    import certifi
except ImportError:  # pragma: no cover - optional local dependency
    certifi = None


class HttpClient:
    def __init__(self, timeout_seconds: int = 30) -> None:
        self.timeout_seconds = timeout_seconds

    def fetch_text(self, url: str, user_agent: str) -> str:
        request = Request(url, headers={"User-Agent": user_agent})
        try:
            with urlopen(
                request,
                timeout=self.timeout_seconds,
                context=self._ssl_context(),
            ) as response:
                return response.read().decode("utf-8")
        except HTTPError as exc:
            raise RuntimeError(f"HTTP {exc.code} while fetching {url}") from exc
        except URLError as exc:
            raise RuntimeError(f"Network error while fetching {url}: {exc}") from exc

    def _ssl_context(self) -> ssl.SSLContext | None:
        if certifi is None:
            return None
        return ssl.create_default_context(cafile=certifi.where())
