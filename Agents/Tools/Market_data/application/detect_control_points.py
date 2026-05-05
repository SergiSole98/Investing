import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dataclasses import dataclass
from datetime import datetime
from domain.candle import Candle
from infrastructure.json_repository import load_candles
from infrastructure.poc_repository import save_poc

LOOKBACK_PIVOT = 2
ATR_PERIOD = 14
MIN_ZONE_TOLERANCE_PCT = 0.005
ATR_ZONE_MULTIPLIER = 0.5
MIN_VALID_TOUCHES = 2
MAX_ZONES_PER_SIDE = 5


@dataclass(frozen=True)
class PriceTouch:
    price: float
    datetime: datetime
    index: int
    tolerance_pct: float


def calculate_atr_values(candles: list[Candle], period: int = ATR_PERIOD) -> list[float]:
    if not candles:
        return []

    true_ranges = []
    for i, candle in enumerate(candles):
        if i == 0:
            true_ranges.append(candle.high - candle.low)
            continue

        prev_close = candles[i - 1].close
        true_ranges.append(max(
            candle.high - candle.low,
            abs(candle.high - prev_close),
            abs(candle.low - prev_close),
        ))

    atr_values = []
    for i in range(len(true_ranges)):
        start = max(0, i - period + 1)
        window = true_ranges[start:i + 1]
        atr_values.append(sum(window) / len(window))
    return atr_values


def dynamic_zone_tolerance_pct(price: float, atr: float) -> float:
    if price <= 0:
        return MIN_ZONE_TOLERANCE_PCT
    atr_pct = atr / price
    return max(MIN_ZONE_TOLERANCE_PCT, ATR_ZONE_MULTIPLIER * atr_pct)


def is_pivot_low(candles: list[Candle], index: int) -> bool:
    current_low = candles[index].low
    prev = candles[index - LOOKBACK_PIVOT:index]
    nxt = candles[index + 1:index + LOOKBACK_PIVOT + 1]
    return all(current_low < candle.low for candle in prev + nxt)


def is_pivot_high(candles: list[Candle], index: int) -> bool:
    current_high = candles[index].high
    prev = candles[index - LOOKBACK_PIVOT:index]
    nxt = candles[index + 1:index + LOOKBACK_PIVOT + 1]
    return all(current_high > candle.high for candle in prev + nxt)


def detect_supports(candles: list[Candle], atr_values: list[float]) -> list[PriceTouch]:
    result = []
    end = len(candles) - LOOKBACK_PIVOT
    for i in range(LOOKBACK_PIVOT, end):
        c = candles[i]
        price = c.low
        tolerance_pct = dynamic_zone_tolerance_pct(price, atr_values[i])

        if not is_pivot_low(candles, i):
            continue

        result.append(PriceTouch(price, c.datetime, i, tolerance_pct))
    return result


def detect_resistances(candles: list[Candle], atr_values: list[float]) -> list[PriceTouch]:
    result = []
    end = len(candles) - LOOKBACK_PIVOT
    for i in range(LOOKBACK_PIVOT, end):
        c = candles[i]
        price = c.high
        tolerance_pct = dynamic_zone_tolerance_pct(price, atr_values[i])

        if not is_pivot_high(candles, i):
            continue

        result.append(PriceTouch(price, c.datetime, i, tolerance_pct))
    return result


def group_prices(touches: list[PriceTouch]) -> list[list[PriceTouch]]:
    if not touches:
        return []
    sorted_touches = sorted(touches, key=lambda x: x.price)
    groups = [[sorted_touches[0]]]
    for touch in sorted_touches[1:]:
        center = sum(t.price for t in groups[-1]) / len(groups[-1])
        group_tolerance = max(t.tolerance_pct for t in groups[-1])
        tolerance = max(group_tolerance, touch.tolerance_pct)
        if abs(touch.price - center) / center <= tolerance:
            groups[-1].append(touch)
        else:
            groups.append([touch])
    return groups


def build_level(group: list[PriceTouch]) -> dict:
    center = sum(t.price for t in group) / len(group)
    all_prices = [t.price for t in group]
    tolerance_pct = max(t.tolerance_pct for t in group)
    last_touch = max(t.datetime for t in group)
    return {
        "price_center": round(center, 4),
        "price_range": {
            "min": round(min(all_prices), 4),
            "max": round(max(all_prices), 4),
        },
        "touches": len(group),
        "tolerance_pct": round(tolerance_pct, 4),
        "last_touch": last_touch.strftime("%Y-%m-%d %H:%M:%S"),
    }


def find_control_points(
    supports: list[PriceTouch],
    resistances: list[PriceTouch],
    current_price: float,
) -> dict:
    sup_groups = group_prices(supports)
    res_groups = group_prices(resistances)

    support_points = []
    resistance_points = []

    for sg in sup_groups:
        if len(sg) < MIN_VALID_TOUCHES:
            continue
        level = build_level(sg)
        if level["price_center"] < current_price:
            support_points.append(level)

    for rg in res_groups:
        if len(rg) < MIN_VALID_TOUCHES:
            continue
        level = build_level(rg)
        if level["price_center"] > current_price:
            resistance_points.append(level)

    support_points = sorted(
        support_points,
        key=lambda x: current_price - x["price_center"],
    )[:MAX_ZONES_PER_SIDE]
    resistance_points = sorted(
        resistance_points,
        key=lambda x: x["price_center"] - current_price,
    )[:MAX_ZONES_PER_SIDE]

    return {
        "supports": sorted(support_points, key=lambda x: x["price_center"]),
        "resistances": sorted(resistance_points, key=lambda x: x["price_center"]),
    }


def main(symbol: str = "TSLA"):
    candles = load_candles(symbol)
    if not candles:
        print("No data found. Run fetch_historical_data.py first.")
        return

    atr_values = calculate_atr_values(candles)
    current_price = candles[-1].close
    supports = detect_supports(candles, atr_values)
    resistances = detect_resistances(candles, atr_values)
    control_points = find_control_points(supports, resistances, current_price)

    period_start = candles[0].datetime.strftime("%Y-%m-%d")
    period_end = candles[-1].datetime.strftime("%Y-%m-%d")

    output = {
        "summary": {
            "total_supports": len(control_points["supports"]),
            "total_resistances": len(control_points["resistances"]),
            "period_start": period_start,
            "period_end": period_end,
            "current_price": round(current_price, 4),
            "params": {
                "lookback_pivot": LOOKBACK_PIVOT,
                "atr_period": ATR_PERIOD,
                "zone_tolerance": "max(0.5%, 0.5 * ATR%)",
                "min_valid_touches": MIN_VALID_TOUCHES,
                "max_zones_per_side": MAX_ZONES_PER_SIDE,
            },
        },
        "supports": control_points["supports"],
        "resistances": control_points["resistances"],
    }

    save_poc(symbol, output)
    print(f"Found {len(control_points['supports'])} supports and {len(control_points['resistances'])} resistances.")
    print(f"Period: {period_start} → {period_end}")


if __name__ == "__main__":
    main()
