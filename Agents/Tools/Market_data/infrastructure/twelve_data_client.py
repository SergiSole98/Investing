import os
import time
import requests
from collections import deque
from datetime import datetime
from dotenv import load_dotenv

from domain.candle import Candle

load_dotenv()

BASE_URL = "https://api.twelvedata.com/time_series"
MAX_REQUESTS_PER_MINUTE = 8

_request_times: deque = deque()


def _wait_if_needed() -> None:
    now = time.time()
    while _request_times and now - _request_times[0] >= 60:
        _request_times.popleft()
    if len(_request_times) >= MAX_REQUESTS_PER_MINUTE:
        wait = 60 - (now - _request_times[0])
        print(f"Rate limit: waiting {wait:.1f}s...")
        time.sleep(wait)
        _request_times.popleft()
    _request_times.append(time.time())


def _fetch_raw(symbol: str, interval: str, outputsize: int, end_date: str = None, start_date: str = None) -> dict:
    api_key = os.getenv("TWELVE_DATA_API_KEY")
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": api_key,
    }
    if end_date:
        params["end_date"] = end_date
    if start_date:
        params["start_date"] = start_date

    _wait_if_needed()
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()

    if "code" in data:
        if data["code"] == 401:
            raise ValueError(f"Invalid API key: {data.get('message')}")
        if data["code"] == 429:
            raise RuntimeError(f"Unexpected rate limit: {data.get('message')}")
        raise RuntimeError(f"API error {data['code']}: {data.get('message')}")

    if "values" not in data or not data["values"]:
        raise ValueError("Empty response: no values returned.")

    return data


def fetch_candles(symbol: str, interval: str, outputsize: int) -> list[Candle]:
    data = _fetch_raw(symbol, interval, outputsize)
    return [
        Candle(
            datetime=datetime.strptime(item["datetime"], "%Y-%m-%d %H:%M:%S"),
            open=float(item["open"]),
            high=float(item["high"]),
            low=float(item["low"]),
            close=float(item["close"]),
            volume=float(item["volume"]),
        )
        for item in data["values"]
    ]


def fetch_raw_page(symbol: str, interval: str, outputsize: int, end_date: str = None, start_date: str = None) -> dict:
    return _fetch_raw(symbol, interval, outputsize, end_date, start_date)
