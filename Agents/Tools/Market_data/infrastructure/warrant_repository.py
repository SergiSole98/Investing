import csv
import json
import os
from datetime import datetime
from typing import Any

from domain.warrant import Warrant


BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def get_bnp_warrants_dir() -> str:
    path = os.path.join(BASE_DIR, "Warrants", "BNP_Paribas")
    os.makedirs(path, exist_ok=True)
    return path


def save_bnp_warrants(
    raw_warrants: list[dict[str, Any]],
    warrants: list[Warrant],
    type_counts: dict[str | None, int] | None = None,
) -> dict[str, Any]:
    output_dir = get_bnp_warrants_dir()
    saved_at = datetime.now().astimezone().isoformat(timespec="seconds")
    normalized = [w.to_dict() for w in warrants]

    raw_path = os.path.join(output_dir, "raw_warrants.json")
    normalized_path = os.path.join(output_dir, "warrants.json")
    csv_path = os.path.join(output_dir, "warrants.csv")
    metadata_path = os.path.join(output_dir, "metadata.json")

    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(raw_warrants, f, ensure_ascii=False, indent=2)

    with open(normalized_path, "w", encoding="utf-8") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)

    if normalized:
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(normalized[0].keys()))
            writer.writeheader()
            writer.writerows(normalized)

    metadata = {
        "source": "BNP Paribas Productos Cotizados",
        "url": "https://productoscotizados.com/warrants/",
        "saved_at": saved_at,
        "count": len(warrants),
        "raw_path": raw_path,
        "normalized_path": normalized_path,
        "csv_path": csv_path,
        "type_counts": type_counts or {},
    }
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    return metadata
