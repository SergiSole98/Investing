import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime
from domain.candle import Candle
from infrastructure.json_repository import load_candles
from infrastructure.poc_repository import save_poc

WINDOW = 2
TOLERANCE = 0.01
MIN_TOUCHES = 3


def detect_supports(candles: list[Candle]) -> list[tuple[float, datetime]]:
    result = []
    for i in range(WINDOW, len(candles) - WINDOW):
        c = candles[i]
        prev = candles[i - WINDOW:i]
        nxt = candles[i + 1:i + WINDOW + 1]
        if all(c.low < p.low for p in prev) and all(c.low < n.low for n in nxt):
            result.append((c.low, c.datetime))
    return result


def detect_resistances(candles: list[Candle]) -> list[tuple[float, datetime]]:
    result = []
    for i in range(WINDOW, len(candles) - WINDOW):
        c = candles[i]
        prev = candles[i - WINDOW:i]
        nxt = candles[i + 1:i + WINDOW + 1]
        if all(c.high > p.high for p in prev) and all(c.high > n.high for n in nxt):
            result.append((c.high, c.datetime))
    return result


def group_prices(prices: list[tuple[float, datetime]]) -> list[list[tuple[float, datetime]]]:
    if not prices:
        return []
    sorted_prices = sorted(prices, key=lambda x: x[0])
    groups = [[sorted_prices[0]]]
    for price, dt in sorted_prices[1:]:
        center = sum(p for p, _ in groups[-1]) / len(groups[-1])
        if abs(price - center) / center <= TOLERANCE:
            groups[-1].append((price, dt))
        else:
            groups.append([(price, dt)])
    return groups


def find_control_points(supports, resistances) -> dict:
    sup_groups = group_prices(supports)
    res_groups = group_prices(resistances)

    support_points = []
    resistance_points = []

    for sg in sup_groups:
        if len(sg) < MIN_TOUCHES:
            continue
        sg_center = sum(p for p, _ in sg) / len(sg)
        all_prices = [p for p, _ in sg]
        last_touch = max(dt for _, dt in sg)
        support_points.append({
            "price_center": round(sg_center, 4),
            "price_range": {
                "min": round(min(all_prices), 4),
                "max": round(max(all_prices), 4),
            },
            "touches": len(sg),
            "last_touch": last_touch.strftime("%Y-%m-%d %H:%M:%S"),
        })

    for rg in res_groups:
        if len(rg) < MIN_TOUCHES:
            continue
        rg_center = sum(p for p, _ in rg) / len(rg)
        all_prices = [p for p, _ in rg]
        last_touch = max(dt for _, dt in rg)
        resistance_points.append({
            "price_center": round(rg_center, 4),
            "price_range": {
                "min": round(min(all_prices), 4),
                "max": round(max(all_prices), 4),
            },
            "touches": len(rg),
            "last_touch": last_touch.strftime("%Y-%m-%d %H:%M:%S"),
        })

    return {
        "supports": sorted(support_points, key=lambda x: x["price_center"]),
        "resistances": sorted(resistance_points, key=lambda x: x["price_center"]),
    }


def main(symbol: str = "TSLA"):
    candles = load_candles(symbol)
    if not candles:
        print("No data found. Run fetch_historical_data.py first.")
        return

    supports = detect_supports(candles)
    resistances = detect_resistances(candles)
    control_points = find_control_points(supports, resistances)

    period_start = candles[0].datetime.strftime("%Y-%m-%d")
    period_end = candles[-1].datetime.strftime("%Y-%m-%d")

    output = {
        "summary": {
            "total_supports": len(control_points["supports"]),
            "total_resistances": len(control_points["resistances"]),
            "period_start": period_start,
            "period_end": period_end,
        },
        "supports": control_points["supports"],
        "resistances": control_points["resistances"],
    }

    save_poc(symbol, output)
    print(f"Found {len(control_points['supports'])} supports and {len(control_points['resistances'])} resistances.")
    print(f"Period: {period_start} → {period_end}")


if __name__ == "__main__":
    main()
