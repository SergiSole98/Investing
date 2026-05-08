import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(__file__))

from application.fetch_historical_data import get_data
from application.detect_control_points import main as run_poc
from infrastructure.json_repository import save_candles


def list_available_symbols() -> list[str]:
    base = os.path.dirname(__file__)
    excluded = {"application", "domain", "infrastructure", "__pycache__"}
    return [
        d for d in os.listdir(base)
        if os.path.isdir(os.path.join(base, d)) and d not in excluded
    ]


def pick_symbol() -> str:
    available = list_available_symbols()

    if available:
        print("\nSymbols with existing data:")
        for i, s in enumerate(available, 1):
            print(f"  {i}. {s}")
        print("  0. Enter a new ticker")

        choice = input("\nSelect an option: ").strip()
        if choice.isdigit() and 0 < int(choice) <= len(available):
            return available[int(choice) - 1]

    ticker = input("Enter ticker symbol (e.g. TSLA): ").strip().upper()
    if not ticker:
        print("No ticker provided. Exiting.")
        sys.exit(1)
    return ticker


def pick_years(default: int = 1) -> int:
    raw = input(f"\nHow many years of data? (default: {default}): ").strip()
    if not raw:
        return default
    if raw.isdigit() and int(raw) > 0:
        return int(raw)
    print(f"Invalid input, using default ({default} year).")
    return default


def main():
    parser = argparse.ArgumentParser(description="Market Data Workflow")
    parser.add_argument("--symbol", "-s", type=str, help="Ticker symbol (e.g. TSLA)")
    parser.add_argument("--years", "-y", type=int, default=None, help="Years of historical data to fetch (default: 1)")
    args = parser.parse_args()

    print("=== Market Data Workflow ===")

    symbol = args.symbol.upper() if args.symbol else pick_symbol()
    print(f"\n→ Symbol: {symbol}")

    years = args.years if args.years is not None else pick_years()
    print(f"→ Years:  {years}")

    print("\n[1/2] Fetching historical data...")
    candles = get_data(symbol, years=years)
    print(f"    Done — {len(candles)} candles loaded.")

    print("\n[2/2] Detecting control points...")
    run_poc(symbol)

    print(f"\n✓ Workflow complete for {symbol}")
    print(f"  Data:   {symbol}/historical_data.json")
    print(f"  POC:    {symbol}/POC/poc.json")


if __name__ == "__main__":
    main()
