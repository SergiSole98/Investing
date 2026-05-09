import json
import os
from datetime import datetime


def get_path(symbol: str) -> str:
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    folder = os.path.join(base, symbol)
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "current_quote.json")


def save_quote(symbol: str, quote: dict) -> None:
    path = get_path(symbol)
    payload = {
        "fetched_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        **quote,
    }
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"Saved quote to {path}")


def load_quote(symbol: str) -> dict | None:
    path = get_path(symbol)
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)
