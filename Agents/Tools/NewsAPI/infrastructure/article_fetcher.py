from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from curl_cffi import requests as cffi_requests


FetchMethod = Literal["curl_cffi", "patchright", "scrapingbee"]
FetchStatus = Literal["ok", "blocked", "error"]


@dataclass(frozen=True)
class FetchResult:
    url: str
    status: FetchStatus
    method: FetchMethod | None
    http_status: int | None
    html: str | None
    error: str | None


# Markers that indicate DataDome / generic anti-bot challenge pages even on HTTP 200.
_BLOCK_MARKERS = (
    "captcha-delivery.com",
    "Please enable JS and disable any ad blocker",
    "Pardon Our Interruption",
    "px-captcha",
    "Access to this page has been denied",
)


def _looks_blocked(html: str, http_status: int) -> bool:
    if http_status in (401, 403, 429):
        return True
    if len(html) < 2000:
        return any(marker in html for marker in _BLOCK_MARKERS)
    return any(marker in html[:4000] for marker in _BLOCK_MARKERS)


class ArticleFetcher:
    """Fetches article HTML with curl_cffi first, falling back to patchright."""

    def __init__(
        self,
        timeout_seconds: int = 30,
        impersonate: str = "chrome131",
        enable_browser_fallback: bool = True,
        browser_wait_ms: int = 4000,
        scrapingbee_api_key: str | None = None,
        scrapingbee_stealth: bool = True,
        scrapingbee_render_js: bool = True,
    ) -> None:
        self.timeout_seconds = timeout_seconds
        self.impersonate = impersonate
        self.enable_browser_fallback = enable_browser_fallback
        self.browser_wait_ms = browser_wait_ms
        self.scrapingbee_api_key = scrapingbee_api_key
        self.scrapingbee_stealth = scrapingbee_stealth
        self.scrapingbee_render_js = scrapingbee_render_js

    def fetch(self, url: str) -> FetchResult:
        last_result = self._try_curl_cffi(url)
        if last_result.status == "ok":
            return last_result

        if self.enable_browser_fallback:
            browser_result = self._try_patchright(url)
            if browser_result.status == "ok":
                return browser_result
            if browser_result.html or browser_result.error:
                last_result = browser_result

        if self.scrapingbee_api_key:
            sb_result = self._try_scrapingbee(url)
            if sb_result.status == "ok":
                return sb_result
            return sb_result

        return last_result

    def _try_curl_cffi(self, url: str) -> FetchResult:
        try:
            response = cffi_requests.get(
                url,
                impersonate=self.impersonate,
                timeout=self.timeout_seconds,
                allow_redirects=True,
            )
        except Exception as exc:
            return FetchResult(
                url=url,
                status="error",
                method="curl_cffi",
                http_status=None,
                html=None,
                error=f"curl_cffi: {exc}",
            )

        html = response.text or ""
        if response.status_code == 200 and not _looks_blocked(html, response.status_code):
            return FetchResult(
                url=url,
                status="ok",
                method="curl_cffi",
                http_status=response.status_code,
                html=html,
                error=None,
            )

        return FetchResult(
            url=url,
            status="blocked",
            method="curl_cffi",
            http_status=response.status_code,
            html=html or None,
            error=None,
        )

    def _try_patchright(self, url: str) -> FetchResult:
        try:
            from patchright.sync_api import sync_playwright
        except ImportError as exc:
            return FetchResult(
                url=url,
                status="error",
                method="patchright",
                http_status=None,
                html=None,
                error=f"patchright import: {exc}",
            )

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    locale="en-US",
                    viewport={"width": 1366, "height": 900},
                )
                page = context.new_page()
                response = page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=self.timeout_seconds * 1000,
                )
                page.wait_for_timeout(self.browser_wait_ms)
                html = page.content()
                http_status = response.status if response else None
                context.close()
                browser.close()
        except Exception as exc:
            return FetchResult(
                url=url,
                status="error",
                method="patchright",
                http_status=None,
                html=None,
                error=f"patchright: {exc}",
            )

        if http_status and http_status >= 400:
            return FetchResult(
                url=url,
                status="blocked",
                method="patchright",
                http_status=http_status,
                html=html or None,
                error=None,
            )

        if _looks_blocked(html, http_status or 200):
            return FetchResult(
                url=url,
                status="blocked",
                method="patchright",
                http_status=http_status,
                html=html or None,
                error=None,
            )

        return FetchResult(
            url=url,
            status="ok",
            method="patchright",
            http_status=http_status,
            html=html,
            error=None,
        )

    def _try_scrapingbee(self, url: str) -> FetchResult:
        params = {
            "api_key": self.scrapingbee_api_key,
            "url": url,
            "render_js": "true" if self.scrapingbee_render_js else "false",
        }
        if self.scrapingbee_stealth:
            params["stealth_proxy"] = "true"

        try:
            response = cffi_requests.get(
                "https://app.scrapingbee.com/api/v1/",
                params=params,
                timeout=max(self.timeout_seconds * 4, 90),
                impersonate=self.impersonate,
            )
        except Exception as exc:
            return FetchResult(
                url=url,
                status="error",
                method="scrapingbee",
                http_status=None,
                html=None,
                error=f"scrapingbee: {exc}",
            )

        html = response.text or ""
        if response.status_code == 200 and html and not _looks_blocked(html, 200):
            return FetchResult(
                url=url,
                status="ok",
                method="scrapingbee",
                http_status=200,
                html=html,
                error=None,
            )

        snippet = html[:300] if html else ""
        if response.status_code in (401, 403):
            error = f"scrapingbee auth/quota error {response.status_code}: {snippet}"
            status: FetchStatus = "error"
        elif response.status_code >= 500:
            error = f"scrapingbee upstream {response.status_code}: {snippet}"
            status = "blocked"
        else:
            error = f"scrapingbee http {response.status_code}: {snippet}" or None
            status = "blocked"

        return FetchResult(
            url=url,
            status=status,
            method="scrapingbee",
            http_status=response.status_code,
            html=html or None,
            error=error,
        )
