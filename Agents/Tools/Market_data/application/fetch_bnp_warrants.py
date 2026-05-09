import sys
import os
from collections import Counter
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from domain.warrant import Warrant
from infrastructure.bnp_warrants_client import BASE_URL, fetch_warrants
from infrastructure.warrant_repository import save_bnp_warrants


ISSUER = "BNP Paribas"
SOURCE = "productoscotizados.com"


def _first_not_none(*values: Any) -> Any:
    for value in values:
        if value is not None:
            return value
    return None


def _date(value: str | None) -> str | None:
    return value[:10] if value else None


def _currency_iso(value: Any) -> str | None:
    return value.get("isoCode") if isinstance(value, dict) else None


def normalize_warrant(item: dict[str, Any]) -> Warrant:
    key_figures = item.get("keyFigures") or {}
    config = item.get("config") or {}
    first = item.get("first") or {}
    currency = _currency_iso(item.get("currency"))
    isin = item.get("isin", "")

    return Warrant(
        source=SOURCE,
        issuer=ISSUER,
        isin=isin,
        wkn=item.get("wkn"),
        name=item.get("productName") or item.get("name"),
        derivative_type=item.get("derivativeTypeName"),
        derivative_type_id=item.get("derivativeTypeId"),
        market=item.get("market"),
        currency=currency,
        underlying_name=item.get("firstUnderlyingName") or first.get("underlyingName"),
        underlying_isin=item.get("firstUnderlyingISIN") or first.get("underlyingISIN"),
        underlying_asset_class=item.get("firstAssetClassName") or first.get("assetClassName"),
        underlying_country=item.get("firstUnderlyingCountryIsoCode"),
        strike=first.get("strikeAbsolute"),
        strike_currency=first.get("strikeCurrencyIsoCode"),
        ratio=first.get("ratio"),
        issue_date=_date(item.get("issueDate") or key_figures.get("issueDate")),
        maturity_date=_date(item.get("maturityDate") or key_figures.get("maturityDate")),
        bid=item.get("bid"),
        ask=item.get("ask"),
        previous_day_bid=item.get("previousDayBid"),
        change_percent=_first_not_none(item.get("changePercent"), key_figures.get("changePercent")),
        leverage=_first_not_none(item.get("leverage"), key_figures.get("leverage")),
        omega=_first_not_none(item.get("omega"), key_figures.get("omega")),
        delta=_first_not_none(item.get("delta"), key_figures.get("delta")),
        implied_volatility=_first_not_none(item.get("volatilityImplied"), key_figures.get("volatilityImplied")),
        break_even=_first_not_none(item.get("breakEven"), key_figures.get("breakEven")),
        intrinsic_value=_first_not_none(item.get("intrinsicValue"), key_figures.get("intrinsicValue")),
        moneyness=_first_not_none(item.get("moneyness"), key_figures.get("moneyness")),
        moneyness_text=_first_not_none(item.get("moneynessText"), key_figures.get("moneynessText")),
        spread_homogeneous=_first_not_none(item.get("spreadHomogeneous"), key_figures.get("spreadHomogeneous")),
        underlying_price=_first_not_none(first.get("price"), key_figures.get("underlyingQuotation")),
        underlying_price_date=_date(first.get("priceDate") or key_figures.get("underlyingQuotationDate")),
        is_public_tradable=config.get("isPublicTradable"),
        is_bid_only=config.get("isBidOnly"),
        is_matured=config.get("isMatured"),
        is_knocked_out=config.get("isKnockedOut"),
        last_update=key_figures.get("lastUpdate") or item.get("timestamp"),
        product_url=f"{BASE_URL}/product-details/{isin}/" if isin else "",
    )


def fetch_and_store_bnp_warrants(page_size: int = 1000) -> dict[str, Any]:
    raw_warrants = fetch_warrants(page_size=page_size)
    warrants = [normalize_warrant(item) for item in raw_warrants]
    type_counts = Counter(w.derivative_type for w in warrants)
    metadata = save_bnp_warrants(raw_warrants, warrants, type_counts=dict(type_counts))
    return metadata


def main() -> None:
    metadata = fetch_and_store_bnp_warrants()
    print(f"Saved {metadata['count']} BNP warrants")
    print(f"JSON: {metadata['normalized_path']}")
    print(f"CSV:  {metadata['csv_path']}")


if __name__ == "__main__":
    main()
