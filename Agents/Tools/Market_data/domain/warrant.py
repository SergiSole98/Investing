from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Warrant:
    source: str
    issuer: str
    isin: str
    wkn: str | None
    name: str | None
    derivative_type: str | None
    derivative_type_id: int | None
    market: str | None
    currency: str | None
    underlying_name: str | None
    underlying_isin: str | None
    underlying_asset_class: str | None
    underlying_country: str | None
    strike: float | None
    strike_currency: str | None
    ratio: float | None
    issue_date: str | None
    maturity_date: str | None
    bid: float | None
    ask: float | None
    previous_day_bid: float | None
    change_percent: float | None
    leverage: float | None
    omega: float | None
    delta: float | None
    implied_volatility: float | None
    break_even: float | None
    intrinsic_value: float | None
    moneyness: float | None
    moneyness_text: str | None
    spread_homogeneous: float | None
    underlying_price: float | None
    underlying_price_date: str | None
    is_public_tradable: bool | None
    is_bid_only: bool | None
    is_matured: bool | None
    is_knocked_out: bool | None
    last_update: str | None
    product_url: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

