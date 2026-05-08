import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime, timedelta
from domain.candle import Candle
from infrastructure.twelve_data_client import fetch_raw_page
from infrastructure.json_repository import save_candles, load_candles

INTERVAL = "4h"
OUTPUTSIZE = 800


def get_data(symbol: str = "TSLA", years: int = 1) -> list[Candle]:
    start_date = datetime.now() - timedelta(days=365 * years)
    cached = load_candles(symbol)

    if cached:
        cached = [c for c in cached if c.datetime >= start_date]
        oldest = cached[0].datetime
        newest = cached[-1].datetime

        missing_past = oldest > start_date + timedelta(hours=4)
        missing_recent = newest < datetime.now() - timedelta(hours=4)

        if not missing_past and not missing_recent:
            print(f"Cache up to date ({len(cached)} candles). Skipping API call.")
            return cached

        if missing_past:
            print(f"Fetching missing history from {start_date} to {oldest}...")
            old_candles = _fetch_range_backwards(symbol, start_date, end_date=oldest)
            old_candles = [c for c in old_candles if c.datetime < oldest]
            cached = sorted(old_candles + cached, key=lambda c: c.datetime)

        if missing_recent:
            print(f"Fetching missing candles from {newest} to now...")
            raw = fetch_raw_page(symbol, INTERVAL, OUTPUTSIZE, start_date=newest.strftime("%Y-%m-%d %H:%M:%S"))
            new_batch = [c for c in parse_data(raw) if c.datetime > newest]
            cached = sorted(cached + new_batch, key=lambda c: c.datetime)

        save_candles(symbol, cached)
        return cached

    print(f"No cache found. Fetching {years} year(s) of data from API...")
    all_candles = _fetch_range_backwards(symbol, start_date)
    save_candles(symbol, all_candles)
    return all_candles


def _fetch_range_backwards(symbol: str, start_date: datetime, end_date: datetime = None) -> list[Candle]:
    all_candles: list[Candle] = []
    end_date_str = end_date.strftime("%Y-%m-%d %H:%M:%S") if end_date else None

    while True:
        raw = fetch_raw_page(symbol, INTERVAL, OUTPUTSIZE, end_date=end_date_str)
        batch = parse_data(raw)

        if not batch:
            break

        if all_candles:
            batch = [c for c in batch if c.datetime < all_candles[0].datetime]

        all_candles = sorted(batch + all_candles, key=lambda c: c.datetime)
        partial = [c for c in all_candles if c.datetime >= start_date]
        save_candles(symbol, partial)
        print(f"Saved {len(partial)} candles so far (oldest: {partial[0].datetime})")

        oldest = all_candles[0].datetime
        if oldest <= start_date:
            break

        end_date_str = oldest.strftime("%Y-%m-%d %H:%M:%S")

    return [c for c in all_candles if c.datetime >= start_date]


def parse_data(raw: dict) -> list[Candle]:
    return [
        Candle(
            datetime=datetime.strptime(item["datetime"], "%Y-%m-%d %H:%M:%S"),
            open=float(item["open"]),
            high=float(item["high"]),
            low=float(item["low"]),
            close=float(item["close"]),
            volume=float(item.get("volume", 0)),
        )
        for item in raw.get("values", [])
    ]


def main():
    symbol = "TSLA"
    candles = get_data(symbol)
    print(f"\nTotal candles: {len(candles)}")
    print("\nFirst 5:")
    for c in candles[:5]:
        print(c)
    print("\nLast 5:")
    for c in candles[-5:]:
        print(c)


if __name__ == "__main__":
    main()
