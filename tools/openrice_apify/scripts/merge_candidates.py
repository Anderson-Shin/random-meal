#!/usr/bin/env python3
"""Dry-run or explicitly merge local OpenRice candidates into the public schema."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT = REPO_ROOT / "tools" / "openrice_apify" / "processed" / "openrice_candidates.json"
DEFAULT_TARGET = REPO_ROOT / "assets" / "data" / "restaurants.json"

BUDGET_MAP = {
    "budget": "$",
    "affordable": "$$",
    "mid": "$$",
    "upper_mid": "$$$",
    "premium": "$$$$",
    "luxury": "$$$$",
    "unknown": "$$",
}

SOURCE_NOTE = (
    "Imported from local OpenRice Apify candidate pipeline. "
    "Requires review before public display."
)

REVIEW_NOTES = (
    "OpenRice Apify candidate. Verify current operation, district, cuisine, "
    "budget, opening hours, and suitability before public display."
)

REFRESH_FIELDS = (
    "name_en",
    "name_zhHant",
    "name_zhHans",
    "area",
    "area_zhHant",
    "area_zhHans",
    "district",
    "cuisine",
    "cuisine_en",
    "cuisine_zhHant",
    "cuisine_zhHans",
    "budget",
    "priceBand",
    "priceRangeId",
    "tags",
    "tags_en",
    "tags_zhHant",
    "tags_zhHans",
    "sourceCategories",
    "categories",
    "mealTypes",
    "situations",
    "speed",
    "address",
    "latitude",
    "longitude",
    "ratingOverall",
    "openingHours",
    "popularDishes",
    "sourceName",
    "sourceConfidence",
    "reviewNotes",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dry-run or explicitly merge local OpenRice candidates."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    parser.add_argument(
        "--refresh-existing",
        action="store_true",
        help="Refresh safe fields on matching hidden OpenRice entries",
    )
    parser.add_argument("--write", action="store_true", help="Write additions to target JSON")
    return parser.parse_args()


def load_array(path: Path, label: str) -> list[dict[str, Any]]:
    if not path.exists():
        raise ValueError(f"{label} path does not exist: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"{label} is not valid JSON: {error.msg}") from error
    if not isinstance(data, list):
        raise ValueError(f"{label} must be a JSON array")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError(f"every {label} item must be a JSON object")
    return data


def safe_text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def safe_number(value: Any, *, integer: bool = False) -> int | float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return int(value) if integer else float(value)
    except (TypeError, ValueError):
        return None


def safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def safe_object(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "unknown"


def normalized_text(value: Any) -> str:
    return re.sub(r"[\W_]+", "", safe_text(value).casefold(), flags=re.UNICODE)


def candidate_id(candidate: dict[str, Any]) -> str:
    existing_id = safe_text(candidate.get("id"))
    if existing_id:
        return existing_id
    source_id = safe_number(candidate.get("sourceRestaurantId"), integer=True)
    if source_id is not None:
        return f"openrice-{source_id}"
    district = slugify(safe_text(candidate.get("district")))
    name = slugify(safe_text(candidate.get("name")))
    return f"openrice-{district}-{name}"


def to_public_schema(candidate: dict[str, Any]) -> dict[str, Any]:
    categories = [
        item.strip()
        for item in safe_list(candidate.get("categories"))
        if isinstance(item, str) and item.strip()
    ]
    district = safe_text(candidate.get("district"))
    area = safe_text(candidate.get("area")) or district
    price_band = safe_text(candidate.get("priceBand")) or "unknown"
    source_restaurant_id = safe_number(candidate.get("sourceRestaurantId"), integer=True)
    transformed = any(
        key in candidate
        for key in ("sourceCategories", "tags_en", "cuisine_en", "area_zhHant")
    )
    tags = safe_list(candidate.get("tags")) if transformed else (
        safe_list(candidate.get("tags")) or categories
    )
    source_categories = safe_list(candidate.get("sourceCategories")) or categories

    return {
        "id": candidate_id(candidate),
        "name": safe_text(candidate.get("name")),
        "name_en": safe_text(candidate.get("name_en")),
        "name_zhHant": safe_text(candidate.get("name_zhHant")),
        "name_zhHans": safe_text(candidate.get("name_zhHans")),
        "area": area,
        "area_zhHant": safe_text(candidate.get("area_zhHant")),
        "area_zhHans": safe_text(candidate.get("area_zhHans")),
        "district": district,
        "cuisine": safe_text(candidate.get("cuisine")) or (categories[0] if categories else "Unknown"),
        "cuisine_en": safe_text(candidate.get("cuisine_en")),
        "cuisine_zhHant": safe_text(candidate.get("cuisine_zhHant")),
        "cuisine_zhHans": safe_text(candidate.get("cuisine_zhHans")),
        "budget": safe_text(candidate.get("budget")) or BUDGET_MAP.get(price_band, "$$"),
        "mealTypes": safe_list(candidate.get("mealTypes")),
        "situations": safe_list(candidate.get("situations")),
        "speed": safe_text(candidate.get("speed")) or "regular",
        "tags": tags,
        "tags_en": safe_list(candidate.get("tags_en")),
        "tags_zhHant": safe_list(candidate.get("tags_zhHant")),
        "tags_zhHans": safe_list(candidate.get("tags_zhHans")),
        "sourceCategories": source_categories,
        "categories": categories,
        "description_en": safe_text(candidate.get("description_en")),
        "description_zhHant": safe_text(candidate.get("description_zhHant")),
        "description_zhHans": safe_text(candidate.get("description_zhHans")),
        "recommendedFor_en": safe_text(candidate.get("recommendedFor_en")),
        "recommendedFor_zhHant": safe_text(candidate.get("recommendedFor_zhHant")),
        "recommendedFor_zhHans": safe_text(candidate.get("recommendedFor_zhHans")),
        "sourceNote": SOURCE_NOTE,
        "verificationStatus": "unverified",
        "verified": False,
        "lastChecked": None,
        "needsReview": True,
        "publicDisplay": False,
        "reviewNotes": safe_text(candidate.get("reviewNotes")) or REVIEW_NOTES,
        "sourceLinks": safe_list(candidate.get("sourceLinks")),
        "sourceConfidence": safe_text(candidate.get("sourceConfidence")) or "low",
        "dataOrigin": "openrice_apify",
        "sourceRestaurantId": source_restaurant_id,
        "sourceName": safe_text(candidate.get("sourceName")) or "openrice_apify",
        "address": safe_text(candidate.get("address")),
        "latitude": safe_number(candidate.get("latitude")),
        "longitude": safe_number(candidate.get("longitude")),
        "priceRangeId": safe_number(candidate.get("priceRangeId"), integer=True),
        "priceBand": price_band,
        "ratingOverall": safe_number(candidate.get("ratingOverall")),
        "openingHours": safe_object(candidate.get("openingHours")),
        "popularDishes": [
            item.strip()
            for item in safe_list(candidate.get("popularDishes"))
            if isinstance(item, str) and item.strip()
        ],
    }


def source_key(item: dict[str, Any]) -> str:
    source_id = safe_number(item.get("sourceRestaurantId"), integer=True)
    return str(source_id) if source_id is not None else ""


def name_address_key(item: dict[str, Any]) -> tuple[str, str]:
    return (normalized_text(item.get("name")), normalized_text(item.get("address")))


def refresh_values(candidate: dict[str, Any]) -> dict[str, Any]:
    mapped = to_public_schema(candidate)
    return {field: mapped[field] for field in REFRESH_FIELDS if field in mapped}


def plan_merge(
    candidates: list[dict[str, Any]],
    existing: list[dict[str, Any]],
    refresh_existing: bool,
) -> tuple[list[dict[str, Any]], list[tuple[int, dict[str, Any]]], int, int]:
    source_matches = {
        source_key(item): index
        for index, item in enumerate(existing)
        if source_key(item)
    }
    pair_matches = {
        name_address_key(item): index
        for index, item in enumerate(existing)
        if all(name_address_key(item))
    }
    additions: list[dict[str, Any]] = []
    refreshes: list[tuple[int, dict[str, Any]]] = []
    skipped_duplicates = 0
    skipped_unsafe = 0
    planned_source_keys: set[str] = set()
    planned_pairs: set[tuple[str, str]] = set()
    planned_refresh_indices: set[int] = set()

    for candidate in candidates:
        candidate_source_key = source_key(candidate)
        pair = name_address_key(candidate)
        match_index = source_matches.get(candidate_source_key) if candidate_source_key else None
        if match_index is None and all(pair):
            match_index = pair_matches.get(pair)

        if match_index is not None:
            target = existing[match_index]
            if not refresh_existing:
                skipped_duplicates += 1
            elif (
                target.get("dataOrigin") == "openrice_apify"
                and target.get("publicDisplay") is False
            ):
                if match_index in planned_refresh_indices:
                    skipped_duplicates += 1
                else:
                    refreshes.append((match_index, refresh_values(candidate)))
                    planned_refresh_indices.add(match_index)
            else:
                skipped_unsafe += 1
            continue
        if (
            candidate_source_key
            and candidate_source_key in planned_source_keys
        ) or (all(pair) and pair in planned_pairs):
            skipped_duplicates += 1
            continue

        addition = to_public_schema(candidate)
        additions.append(addition)
        if candidate_source_key:
            planned_source_keys.add(candidate_source_key)
        if all(pair):
            planned_pairs.add(pair)

    return additions, refreshes, skipped_duplicates, skipped_unsafe


def main() -> int:
    args = parse_args()
    try:
        candidates = load_array(args.input, "input")
        existing = load_array(args.target, "target")
        additions, refreshes, skipped, skipped_unsafe = plan_merge(
            candidates, existing, args.refresh_existing
        )

        if args.write:
            if args.refresh_existing:
                for index, values in refreshes:
                    existing[index].update(values)
            args.target.parent.mkdir(parents=True, exist_ok=True)
            args.target.write_text(
                json.dumps(existing + additions, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Candidates read: {len(candidates)}")
    print(f"Existing restaurants read: {len(existing)}")
    print(f"New candidates to add: {len(additions)}")
    print(f"Skipped duplicates: {skipped}")
    print(f"Existing hidden OpenRice candidates to refresh: {len(refreshes)}")
    print(f"Skipped unsafe refresh targets: {skipped_unsafe}")
    print(f"Output path: {args.target}")
    print(f"Refresh existing enabled: {str(args.refresh_existing).lower()}")
    print(f"Write mode enabled: {str(args.write).lower()}")
    if not args.write:
        print("Dry run only. No files were modified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
