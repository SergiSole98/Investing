from infrastructure.twelve_data_client import fetch_candles
from infrastructure.csv_repository import save_candles


def fetch_and_store(symbol: str = "TSLA", interval: str = "4h", outputsize: int = 100) -> None:
    candles = fetch_candles(symbol=symbol, interval=interval, outputsize=outputsize)
    save_candles(candles)
