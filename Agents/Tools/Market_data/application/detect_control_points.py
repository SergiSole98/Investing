import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime
from domain.candle import Candle
from infrastructure.json_repository import load_candles
from infrastructure.poc_repository import save_poc

WINDOW = 2
TOLERANCE = 0.01
MIN_TOUCHES = 2


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


def find_control_points(supports, resistances) -> list[dict]:
    sup_groups = group_prices(supports)
    res_groups = group_prices(resistances)

    control_points = []

    for sg in sup_groups:
        if len(sg) < MIN_TOUCHES:
            continue
        sg_center = sum(p for p, _ in sg) / len(sg)

        for rg in res_groups:
            if len(rg) < MIN_TOUCHES:
                continue
            rg_center = sum(p for p, _ in rg) / len(rg)

            if abs(sg_center - rg_center) / sg_center <= TOLERANCE:
                zone_center = (sg_center + rg_center) / 2
                all_prices = [p for p, _ in sg + rg]
                last_sup = max(dt for _, dt in sg)
                last_res = max(dt for _, dt in rg)

                control_points.append({
                    "price_center": round(zone_center, 4),
                    "price_range": {
                        "min": round(min(all_prices), 4),
                        "max": round(max(all_prices), 4),
                    },
                    "support_touches": len(sg),
                    "last_support": last_sup.strftime("%Y-%m-%d %H:%M:%S"),
                    "resistance_touches": len(rg),
                    "last_resistance": last_res.strftime("%Y-%m-%d %H:%M:%S"),
                    "last_touch": max(last_sup, last_res).strftime("%Y-%m-%d %H:%M:%S"),
                })

    return sorted(control_points, key=lambda x: x["price_center"])


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
            "total_control_points": len(control_points),
            "period_start": period_start,
            "period_end": period_end,
        },
        "supports": [
            {
                "price": cp["price_center"],
                "price_range": cp["price_range"],
                "times_touched": cp["support_touches"],
                "last_touch": cp["last_support"],
            }
            for cp in control_points
        ],
        "resistances": [
            {
                "price": cp["price_center"],
                "price_range": cp["price_range"],
                "times_touched": cp["resistance_touches"],
                "last_touch": cp["last_resistance"],
            }
            for cp in control_points
        ],
    }

    save_poc(symbol, output)
    print(f"Found {len(control_points)} control points.")
    print(f"Period: {period_start} → {period_end}")


if __name__ == "__main__":
    main()
