import pandas as pd
from domain.candle import Candle


def save_candles(candles: list[Candle], path: str = "market_data.csv") -> None:
    df = pd.DataFrame([c.__dict__ for c in candles]).set_index("datetime")
    df.to_csv(path)
    print(f"Saved {len(df)} rows to {path}")
