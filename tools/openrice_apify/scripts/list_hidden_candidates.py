#!/usr/bin/env python3
"""List hidden OpenRice Apify candidates without modifying any files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_TARGET = REPO_ROOT / "assets" / "data" / "restaurants.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="List hidden OpenRice Apify candidates from the public database."
    )
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    parser.add_argument("--format", choices=("table", "json"), default="table")
    return parser.parse_args()


def load_restaurants(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise ValueError(f"target path does not exist: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"target is not valid JSON: {error.msg}") from error
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError("target must be a JSON array of restaurant objects")
    return data


def text_or_default(value: Any, default: str = "") -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    if value is not None and not isinstance(value, (dict, list)):
        return str(value)
    return default


def list_or_empty(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def summarize(candidate: dict[str, Any]) -> dict[str, Any]:
    transformed = any(
        key in candidate
        for key in ("sourceCategories", "tags_en", "cuisine_en", "area_zhHant")
    )
    tag_values = candidate.get("tags") if transformed else (
        candidate.get("tags") or candidate.get("categories")
    )
    tags = [
        text_or_default(item)
        for item in list_or_empty(tag_values)
        if text_or_default(item)
    ]
    source_categories = [
        text_or_default(item)
        for item in list_or_empty(
            candidate.get("sourceCategories") or candidate.get("categories")
        )
        if text_or_default(item)
    ]
    return {
        "id": text_or_default(candidate.get("id")),
        "name": text_or_default(candidate.get("name")),
        "area": text_or_default(candidate.get("area")),
        "district": text_or_default(candidate.get("district")),
        "cuisine": text_or_default(candidate.get("cuisine")),
        "budget": text_or_default(candidate.get("budget")),
        "priceBand": text_or_default(candidate.get("priceBand")),
        "ratingOverall": candidate.get("ratingOverall"),
        "tags": tags,
        "sourceCategories": source_categories,
        "popularDishesCount": len(list_or_empty(candidate.get("popularDishes"))),
        "hasOpeningHours": bool(candidate.get("openingHours")),
        "needsReview": candidate.get("needsReview"),
        "verificationStatus": text_or_default(candidate.get("verificationStatus")),
    }


def hidden_openrice_candidates(
    restaurants: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        summarize(item)
        for item in restaurants
        if item.get("dataOrigin") == "openrice_apify"
        and item.get("publicDisplay") is False
    ]


def display(value: Any) -> str:
    if value is None or value == "":
        return "-"
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def print_table(candidates: list[dict[str, Any]]) -> None:
    print(f"Found {len(candidates)} hidden OpenRice candidates.")
    for index, candidate in enumerate(candidates, start=1):
        tags = ", ".join(candidate["tags"]) or "-"
        source_categories = ", ".join(candidate["sourceCategories"]) or "-"
        print()
        print(f"{index}. {display(candidate['id'])}")
        print(f"   Name: {display(candidate['name'])}")
        print(f"   Area: {display(candidate['area'])}")
        print(f"   District: {display(candidate['district'])}")
        print(f"   Cuisine: {display(candidate['cuisine'])}")
        print(f"   Budget: {display(candidate['budget'])}")
        print(f"   Price Band: {display(candidate['priceBand'])}")
        print(f"   Rating Overall: {display(candidate['ratingOverall'])}")
        print(f"   Tags: {tags}")
        print(f"   Source Categories: {source_categories}")
        print(f"   Popular Dishes: {candidate['popularDishesCount']}")
        print(f"   Has Opening Hours: {display(candidate['hasOpeningHours'])}")
        print(f"   Needs Review: {display(candidate['needsReview'])}")
        print(f"   Verification Status: {display(candidate['verificationStatus'])}")


def main() -> int:
    args = parse_args()
    try:
        restaurants = load_restaurants(args.target)
        candidates = hidden_openrice_candidates(restaurants)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(candidates, ensure_ascii=False, indent=2))
    else:
        print_table(candidates)
    return 0


if __name__ == "__main__":
    sys.exit(main())
