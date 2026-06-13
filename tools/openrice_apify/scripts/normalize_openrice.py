#!/usr/bin/env python3
"""Normalize manually downloaded OpenRice Apify JSON into review candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


TOOL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RAW_DIR = TOOL_ROOT / "raw"
DEFAULT_OUTPUT = TOOL_ROOT / "processed" / "openrice_candidates.json"
DEFAULT_PRICE_MAP = TOOL_ROOT / "config" / "price_map.json"


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize local OpenRice Apify JSON files into review candidates."
    )
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--price-map", type=Path, default=DEFAULT_PRICE_MAP)
    return parser.parse_args()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"{path}: invalid JSON: {error.msg}") from error


def rows_from_payload(payload: Any, path: Path) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("items"), list):
        payload = payload["items"]
    if not isinstance(payload, list):
        raise ValueError(f"{path}: expected a JSON array or an object with an items array")
    if not all(isinstance(item, dict) for item in payload):
        raise ValueError(f"{path}: every candidate item must be a JSON object")
    return payload


def safe_number(value: Any, *, integer: bool = False) -> int | float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return int(value) if integer else float(value)
    except (TypeError, ValueError):
        return None


def safe_text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def safe_object(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def normalize_categories(value: Any) -> list[str]:
    categories: list[str] = []
    for item in safe_list(value):
        if isinstance(item, str) and item.strip():
            categories.append(item.strip())
        elif isinstance(item, dict):
            name = item.get("name")
            if isinstance(name, str) and name.strip():
                categories.append(name.strip())
    return categories


def normalize_popular_dishes(value: Any) -> list[str]:
    dishes: list[str] = []
    for item in safe_list(value):
        if isinstance(item, str) and item.strip():
            dishes.append(item.strip())
        elif isinstance(item, dict):
            name = item.get("name") or item.get("dish_name")
            if isinstance(name, str) and name.strip():
                dishes.append(name.strip())
    return dishes


def normalize_row(row: dict[str, Any], price_map: dict[str, str]) -> dict[str, Any]:
    price_range_id = safe_number(row.get("price_range_id"), integer=True)
    return {
        "sourceRestaurantId": safe_number(row.get("restaurant_id"), integer=True),
        "name": safe_text(row.get("name")),
        "district": safe_text(row.get("district")),
        "address": safe_text(row.get("address")),
        "latitude": safe_number(row.get("latitude")),
        "longitude": safe_number(row.get("longitude")),
        "priceRangeId": price_range_id,
        "priceBand": price_map.get(str(price_range_id), "unknown"),
        "ratingOverall": safe_number(row.get("rating_overall")),
        "categories": normalize_categories(row.get("categories")),
        "openingHours": safe_object(row.get("opening_hours")),
        "popularDishes": normalize_popular_dishes(row.get("popular_dishes")),
        "dataOrigin": "openrice_apify",
        "needsReview": True,
        "publicDisplay": False,
    }


def main() -> int:
    args = parse_args()
    try:
        if not is_within(args.input_dir, DEFAULT_RAW_DIR):
            raise ValueError("input directory must remain under tools/openrice_apify/raw")
        if not is_within(args.output, DEFAULT_OUTPUT.parent):
            raise ValueError("output path must remain under tools/openrice_apify/processed")
        if not args.input_dir.is_dir():
            raise ValueError(f"input directory does not exist: {args.input_dir}")
        price_map = load_json(args.price_map)
        if not isinstance(price_map, dict):
            raise ValueError("price map must be a JSON object")

        input_files = sorted(args.input_dir.glob("*.json"))
        if not input_files:
            raise ValueError(f"no JSON files found under: {args.input_dir}")

        rows: list[dict[str, Any]] = []
        for path in input_files:
            rows.extend(rows_from_payload(load_json(path), path))

        candidates = [normalize_row(row, price_map) for row in rows]
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(candidates, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Normalized {len(candidates)} candidates from {len(input_files)} local JSON files.")
    print(f"Output: {args.output}")
    print("Reminder: candidates require review and are not public database data.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
