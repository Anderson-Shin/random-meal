#!/usr/bin/env python3
"""Validate normalized candidates and copy them to a future-import review file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


TOOL_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_ROOT = TOOL_ROOT / "processed"

REQUIRED_KEYS = {
    "sourceRestaurantId",
    "name",
    "district",
    "address",
    "latitude",
    "longitude",
    "priceRangeId",
    "priceBand",
    "ratingOverall",
    "categories",
    "openingHours",
    "popularDishes",
    "dataOrigin",
    "needsReview",
    "publicDisplay",
}


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate local OpenRice candidates for future manual import review."
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def validate(data: Any) -> list[dict[str, Any]]:
    if not isinstance(data, list):
        raise ValueError("input must be a JSON array")
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"candidate {index} must be a JSON object")
        if set(item) != REQUIRED_KEYS:
            raise ValueError(f"candidate {index} does not match the approved candidate schema")
        if item["dataOrigin"] != "openrice_apify":
            raise ValueError(f"candidate {index} has an invalid dataOrigin")
        if item["needsReview"] is not True or item["publicDisplay"] is not False:
            raise ValueError(f"candidate {index} must require review and remain hidden")
    return data


def main() -> int:
    args = parse_args()
    try:
        if not is_within(args.input, PROCESSED_ROOT):
            raise ValueError("input path must remain under tools/openrice_apify/processed")
        if not is_within(args.output, PROCESSED_ROOT):
            raise ValueError("output path must remain under tools/openrice_apify/processed")
        data = json.loads(args.input.read_text(encoding="utf-8"))
        candidates = validate(data)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(candidates, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Prepared {len(candidates)} candidates for future manual import review.")
    print(f"Output: {args.output}")
    print("No public restaurant database files were modified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
