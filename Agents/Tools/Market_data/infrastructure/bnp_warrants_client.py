import time
import uuid
from typing import Any

import requests


BASE_URL = "https://productoscotizados.com"
API_BASE_URL = f"{BASE_URL}/apiv2/api/v1"
PRODUCT_LIST_URL = f"{API_BASE_URL}/productlist/"
PRODUCT_GROUP_WARRANTS = 13
CLIENT_ID = 3
LANGUAGE_ID = "es"


def _headers() -> dict[str, str]:
    return {
        "Content-Type": "application/json",
        "clientid": str(CLIENT_ID),
        "countryid": "",
        "languageid": LANGUAGE_ID,
        "traceSessionId": str(uuid.uuid4()),
    }


def _payload(offset: int, limit: int) -> dict[str, Any]:
    return {
        "clientId": CLIENT_ID,
        "languageId": LANGUAGE_ID,
        "countryId": "",
        "sortPreference": [],
        "filterSelections": [],
        "deeplinkParameters": None,
        "oldDeepLinkString": None,
        "firstUnderlyingIsin": None,
        "isBNL": None,
        "isDB": None,
        "responsetype": 0,
        "productFlagFilter": "Default",
        "isDirectionFilterCanBeDisabled": False,
        "derivativeTypeIds": [],
        "productSetIds": [],
        "productSubGroupIds": [],
        "productGroupIds": [PRODUCT_GROUP_WARRANTS],
        "offset": offset,
        "limit": limit,
        "resolveSubPreset": None,
        "resolveOnlySelectedPresets": False,
        "allowLeverageGrouping": False,
    }


def fetch_warrants(page_size: int = 1000, pause_seconds: float = 0.1) -> list[dict[str, Any]]:
    warrants: list[dict[str, Any]] = []
    total: int | None = None
    offset = 0

    while total is None or offset < total:
        response = requests.post(
            PRODUCT_LIST_URL,
            headers=_headers(),
            json=_payload(offset=offset, limit=page_size),
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        batch = data.get("result", [])
        if total is None:
            total = int(data.get("total", 0))
        if not batch:
            break

        warrants.extend(batch)
        offset += len(batch)
        print(f"Fetched {len(warrants)}/{total} BNP warrants")

        if offset < total and pause_seconds > 0:
            time.sleep(pause_seconds)

    return warrants

