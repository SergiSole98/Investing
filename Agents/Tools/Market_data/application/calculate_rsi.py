import sys
import os
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from domain.candle import Candle

PERIOD = 14


def calculate_rsi(candles: list[Candle]) -> list[Optional[float]]:
    closes = [c.close for c in candles]
    rsi_values: list[float | None] = [None] * len(closes)

    for i in range(PERIOD, len(closes)):
        window = closes[i - PERIOD:i]
        diffs = [window[j] - window[j - 1] for j in range(1, len(window))]

        gains = [d for d in diffs if d > 0]
        losses = [-d for d in diffs if d < 0]

        avg_gain = sum(gains) / PERIOD if gains else 0.0
        avg_loss = sum(losses) / PERIOD if losses else 0.0

        if avg_loss == 0:
            rsi_values[i] = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi_values[i] = round(100 - (100 / (1 + rs)), 2)

    return rsi_values
