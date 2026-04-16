import sys
import os

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


def main():
    print("=== Market Data Workflow ===")
    symbol = pick_symbol()
    print(f"\n→ Symbol: {symbol}")

    print("\n[1/2] Fetching historical data...")
    candles = get_data(symbol)
    print(f"    Done — {len(candles)} candles loaded.")

    print("\n[2/2] Detecting control points...")
    run_poc(symbol)

    print(f"\n✓ Workflow complete for {symbol}")
    print(f"  Data:   {symbol}/historical_data.json")
    print(f"  POC:    {symbol}/POC/poc.json")


if __name__ == "__main__":
    main()
