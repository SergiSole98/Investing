import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from infrastructure.quote_repository import save_quote
from infrastructure.twelve_data_client import fetch_quote


def fetch_and_store_extended_quote(symbol: str, exchange: str = None) -> dict:
    quote = fetch_quote(symbol=symbol, exchange=exchange, prepost=True)
    save_quote(symbol, quote)
    return quote


def print_quote_summary(quote: dict) -> None:
    symbol = quote.get("symbol", "UNKNOWN")
    exchange = quote.get("exchange", "")
    extended_price = quote.get("extended_price")
    price = extended_price or quote.get("close") or quote.get("price")
    previous_close = quote.get("previous_close")
    change = quote.get("extended_change") if extended_price is not None else quote.get("change")
    percent_change = (
        quote.get("extended_percent_change")
        if extended_price is not None
        else quote.get("percent_change")
    )
    is_extended = quote.get("is_extended_hours")
    quote_time = quote.get("extended_timestamp") or quote.get("datetime")
    if isinstance(quote_time, int):
        quote_time = datetime.fromtimestamp(quote_time).astimezone().isoformat(timespec="seconds")

    session = "extended hours" if is_extended or extended_price is not None else "regular session"
    print(f"{symbol} {exchange} @ {quote_time}: {price} ({session})")
    if previous_close is not None:
        print(f"Previous close: {previous_close}")
    if change is not None and percent_change is not None:
        print(f"Change: {change} ({percent_change}%)")


def main() -> None:
    symbol = sys.argv[1].upper() if len(sys.argv) > 1 else "AAPL"
    quote = fetch_and_store_extended_quote(symbol)
    print_quote_summary(quote)


if __name__ == "__main__":
    main()
