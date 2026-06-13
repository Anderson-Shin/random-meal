#!/usr/bin/env python3
"""Transform normalized OpenRice candidates into richer local review records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any

from mapping_utils import (
    build_multilingual_names,
    load_category_map,
    load_district_map,
    load_json,
    map_categories,
    map_district,
    map_price,
)


TOOL_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_ROOT = TOOL_ROOT / "processed"
DEFAULT_INPUT = PROCESSED_ROOT / "openrice_candidates.json"
DEFAULT_OUTPUT = PROCESSED_ROOT / "openrice_transformed_candidates.json"
DEFAULT_DISTRICT_MAP = TOOL_ROOT / "config" / "district_map.json"
DEFAULT_CATEGORY_MAP = TOOL_ROOT / "config" / "category_map.json"
DEFAULT_PRICE_MAP = TOOL_ROOT / "config" / "price_map.json"
REVIEW_NOTES = "Transformed OpenRice Apify candidate. Requires manual review before public display."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Transform normalized OpenRice candidates.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--district-map", type=Path, default=DEFAULT_DISTRICT_MAP)
    parser.add_argument("--category-map", type=Path, default=DEFAULT_CATEGORY_MAP)
    parser.add_argument("--price-map", type=Path, default=DEFAULT_PRICE_MAP)
    return parser.parse_args()


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def safe_text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def safe_object(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def safe_number(value: Any, *, integer: bool = False) -> int | float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return int(value) if integer else float(value)
    except (TypeError, ValueError):
        return None


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug or "unknown"


def candidate_id(candidate: dict[str, Any]) -> str:
    source_id = safe_number(candidate.get("sourceRestaurantId"), integer=True)
    if source_id is not None:
        return f"openrice-{source_id}"
    return f"openrice-{slugify(safe_text(candidate.get('district')))}-{slugify(safe_text(candidate.get('name')))}"


def transform(
    candidate: dict[str, Any],
    district_map: list[dict[str, Any]],
    category_map: dict[str, dict[str, Any]],
    price_map: dict[str, str],
) -> dict[str, Any]:
    district_fields = map_district(candidate.get("district"), district_map)
    category_fields = map_categories(candidate.get("categories"), category_map)
    price_fields = map_price(candidate.get("priceRangeId"), candidate.get("priceBand"), price_map)
    name_fields = build_multilingual_names(candidate)
    return {
        "id": candidate_id(candidate),
        "sourceRestaurantId": safe_number(candidate.get("sourceRestaurantId"), integer=True),
        "sourceName": "openrice_apify",
        "name": safe_text(candidate.get("name")),
        **name_fields,
        **district_fields,
        "address": safe_text(candidate.get("address")),
        "latitude": safe_number(candidate.get("latitude")),
        "longitude": safe_number(candidate.get("longitude")),
        "categories": safe_list(candidate.get("categories")),
        **category_fields,
        "sourceCategories": (
            safe_list(category_fields.get("sourceCategories"))
            or safe_list(candidate.get("categories"))
        ),
        **price_fields,
        "priceRangeId": safe_number(candidate.get("priceRangeId"), integer=True),
        "ratingOverall": safe_number(candidate.get("ratingOverall")),
        "openingHours": safe_object(candidate.get("openingHours")),
        "popularDishes": safe_list(candidate.get("popularDishes")),
        "description_en": safe_text(candidate.get("description_en")),
        "description_zhHant": safe_text(candidate.get("description_zhHant")),
        "description_zhHans": safe_text(candidate.get("description_zhHans")),
        "recommendedFor_en": safe_text(candidate.get("recommendedFor_en")),
        "recommendedFor_zhHant": safe_text(candidate.get("recommendedFor_zhHant")),
        "recommendedFor_zhHans": safe_text(candidate.get("recommendedFor_zhHans")),
        "dataOrigin": "openrice_apify",
        "verificationStatus": "unverified",
        "verified": False,
        "lastChecked": None,
        "needsReview": True,
        "publicDisplay": False,
        "sourceLinks": safe_list(candidate.get("sourceLinks")),
        "sourceConfidence": safe_text(candidate.get("sourceConfidence")) or "low",
        "reviewNotes": REVIEW_NOTES,
    }


def main() -> int:
    args = parse_args()
    try:
        if not is_within(args.input, PROCESSED_ROOT):
            raise ValueError("input path must remain under tools/openrice_apify/processed")
        if not is_within(args.output, PROCESSED_ROOT):
            raise ValueError("output path must remain under tools/openrice_apify/processed")
        if args.output.resolve() == args.input.resolve():
            raise ValueError("output path must differ from input path")
        candidates = load_json(args.input)
        if not isinstance(candidates, list) or not all(isinstance(item, dict) for item in candidates):
            raise ValueError("input must be a JSON array of candidate objects")
        district_map = load_district_map(args.district_map)
        category_map = load_category_map(args.category_map)
        price_map = load_json(args.price_map)
        if not isinstance(price_map, dict):
            raise ValueError("price map must be a JSON object")
        transformed = [
            transform(candidate, district_map, category_map, price_map)
            for candidate in candidates
        ]
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(transformed, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Transformed candidates: {len(transformed)}")
    print(f"Output: {args.output}")
    print("All transformed candidates remain hidden and require manual review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
