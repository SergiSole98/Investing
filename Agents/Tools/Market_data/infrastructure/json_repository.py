import os
import json
from datetime import datetime
from domain.candle import Candle

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_path(symbol: str) -> str:
    base = os.path.dirname(os.path.dirname(__file__))
    folder = os.path.join(base, symbol)
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "historical_data.json")


def save_candles(symbol: str, candles: list[Candle]) -> None:
    path = get_path(symbol)
    data = [
        {
            "datetime": c.datetime.strftime(DATE_FORMAT),
            "open": c.open,
            "high": c.high,
            "low": c.low,
            "close": c.close,
            "volume": c.volume,
        }
        for c in candles
    ]
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(data)} candles to {path}")


def load_candles(symbol: str) -> list[Candle] | None:
    path = get_path(symbol)
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        data = json.load(f)
    return [
        Candle(
            datetime=datetime.strptime(item["datetime"], DATE_FORMAT),
            open=item["open"],
            high=item["high"],
            low=item["low"],
            close=item["close"],
            volume=item["volume"],
        )
        for item in data
    ]
