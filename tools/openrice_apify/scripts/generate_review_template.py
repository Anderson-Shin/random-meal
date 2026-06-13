#!/usr/bin/env python3
"""Generate a manual review template for hidden OpenRice Apify candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_TARGET = REPO_ROOT / "assets" / "data" / "restaurants.json"
DEFAULT_OUTPUT = (
    REPO_ROOT
    / "tools"
    / "openrice_apify"
    / "processed"
    / "openrice_review_template.json"
)
REVIEW_WARNING = (
    "Do not approve unless facts were manually checked and public descriptions "
    "are original."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a review template for hidden OpenRice Apify candidates."
    )
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def load_array(path: Path, label: str) -> list[dict[str, Any]]:
    if not path.exists():
        raise ValueError(f"{label} path does not exist: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"{label} is not valid JSON: {error.msg}") from error
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError(f"{label} must be a JSON array of objects")
    return data


def text_or_default(value: Any, default: str = "") -> str:
    return value.strip() if isinstance(value, str) and value.strip() else default


def list_or_empty(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def object_or_empty(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def review_object(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": text_or_default(candidate.get("id")),
        "name": text_or_default(candidate.get("name")),
        "name_en": text_or_default(candidate.get("name_en")),
        "name_zhHant": text_or_default(candidate.get("name_zhHant")),
        "name_zhHans": text_or_default(candidate.get("name_zhHans")),
        "area": text_or_default(candidate.get("area")),
        "area_zhHant": text_or_default(candidate.get("area_zhHant")),
        "area_zhHans": text_or_default(candidate.get("area_zhHans")),
        "district": text_or_default(candidate.get("district")),
        "address": text_or_default(candidate.get("address")),
        "cuisine": text_or_default(candidate.get("cuisine")),
        "cuisine_en": text_or_default(candidate.get("cuisine_en")),
        "cuisine_zhHant": text_or_default(candidate.get("cuisine_zhHant")),
        "cuisine_zhHans": text_or_default(candidate.get("cuisine_zhHans")),
        "budget": text_or_default(candidate.get("budget")),
        "priceBand": text_or_default(candidate.get("priceBand")),
        "ratingOverall": candidate.get("ratingOverall"),
        "tags": list_or_empty(candidate.get("tags")),
        "tags_en": list_or_empty(candidate.get("tags_en")),
        "tags_zhHant": list_or_empty(candidate.get("tags_zhHant")),
        "tags_zhHans": list_or_empty(candidate.get("tags_zhHans")),
        "sourceCategories": list_or_empty(
            candidate.get("sourceCategories") or candidate.get("categories")
        ),
        "popularDishes": list_or_empty(candidate.get("popularDishes")),
        "openingHours": object_or_empty(candidate.get("openingHours")),
        "reviewDecision": "pending",
        "approvedForPublicDisplay": False,
        "reviewer": "",
        "reviewDate": "",
        "reviewNotes": "",
        "finalCuisine": text_or_default(candidate.get("cuisine")),
        "finalBudget": text_or_default(candidate.get("budget")),
        "finalMealTypes": [],
        "finalSituations": [],
        "finalSpeed": text_or_default(candidate.get("speed"), "normal"),
        "finalTags": list_or_empty(candidate.get("tags")),
        "description_en": "",
        "description_zhHant": "",
        "description_zhHans": "",
        "recommendedFor_en": "",
        "recommendedFor_zhHant": "",
        "recommendedFor_zhHans": "",
        "sourceLinks": list_or_empty(candidate.get("sourceLinks")),
        "sourceConfidence": text_or_default(candidate.get("sourceConfidence"), "low"),
        "reviewWarning": REVIEW_WARNING,
    }


def main() -> int:
    args = parse_args()
    try:
        if args.output.resolve() == args.target.resolve():
            raise ValueError("output path must not be the restaurant database target")
        restaurants = load_array(args.target, "target")
        reviews = [
            review_object(item)
            for item in restaurants
            if item.get("dataOrigin") == "openrice_apify"
            and item.get("publicDisplay") is False
        ]
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(reviews, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Hidden OpenRice candidates read: {len(reviews)}")
    print(f"Review template: {args.output}")
    print("The restaurant database was not modified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
