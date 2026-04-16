import os
import json


def save_poc(symbol: str, data: dict) -> None:
    base = os.path.dirname(os.path.dirname(__file__))
    folder = os.path.join(base, symbol, "POC")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "poc.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved POC to {path}")
