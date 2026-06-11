#!/usr/bin/env python3
"""Normalize local candidate JSON without network access or database writes."""

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any


UNSAFE_FIELDS = (
    "price",
    "smiles",
    "frowns",
    "ratings",
    "reviews",
    "rankings",
    "photos",
    "photoUrls",
    "menuText",
    "promotionalCopy",
    "rawHtml",
    "description",
    "reviewText",
    "ratingScore",
    "popularityRank",
)

NEXT_ACTION = (
    "Cross-check with official website, mall directory, building directory, "
    "or another stronger source."
)

NOTES = "Local candidate only. Do not import directly into restaurants.json."
DISCOVERY_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize fake or local candidate JSON into local review data."
    )
    parser.add_argument("--input", required=True, type=Path, help="Local input JSON file")
    parser.add_argument("--output", required=True, type=Path, help="Local output JSON file")
    return parser.parse_args()


def is_restaurants_path(path: Path) -> bool:
    parts = path.resolve().parts
    return len(parts) >= 3 and parts[-3:] == ("assets", "data", "restaurants.json")


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def safe_string(value: Any, fallback: str = "") -> str:
    return value if isinstance(value, str) else fallback


def safe_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def area_slug(area: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", area.lower()).strip("-")
    return slug or "unknown-area"


def normalize_candidates(raw_candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    area_counts: dict[str, int] = {}
    normalized: list[dict[str, Any]] = []

    for raw in raw_candidates:
        area = safe_string(raw.get("area"))
        slug = area_slug(area)
        area_counts[slug] = area_counts.get(slug, 0) + 1

        source_type = safe_string(raw.get("sourceType"), "local_research")
        if not source_type:
            source_type = "local_research"

        discarded = [field for field in UNSAFE_FIELDS if field in raw]

        normalized.append(
            {
                "candidateId": f"sample-{slug}-{area_counts[slug]:03d}",
                "candidateName": safe_string(raw.get("name")),
                "candidateArea": area,
                "candidateDistrict": safe_string(raw.get("district")),
                "candidateAddressHint": safe_string(raw.get("address")),
                "candidateCuisineHint": safe_string(raw.get("cuisine")),
                "candidateBudgetHint": safe_string(raw.get("budget")),
                "candidateMealTypeHints": safe_string_list(raw.get("mealTypes")),
                "candidateSituationHints": safe_string_list(raw.get("situations")),
                "candidateSpeedHint": safe_string(raw.get("speed")),
                "discoverySource": source_type,
                "sourceUrl": safe_string(raw.get("sourceUrl")),
                "sourceUsage": "discovery",
                "sourceConfidence": "low",
                "dataOrigin": "discovery_source_only",
                "discardedFields": discarded,
                "readyForPublicDb": False,
                "reviewStatus": "not_reviewed",
                "nextAction": NEXT_ACTION,
                "notes": NOTES,
            }
        )

    return normalized


def load_input(path: Path) -> list[dict[str, Any]]:
    if is_restaurants_path(path):
        raise ValueError("assets/data/restaurants.json cannot be used as input")
    if not path.exists():
        raise ValueError(f"input path does not exist: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"input is not valid JSON: {error.msg}") from error

    if not isinstance(data, list):
        raise ValueError("input JSON must be an array")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("every input array item must be an object")

    return data


def write_output(path: Path, candidates: list[dict[str, Any]]) -> None:
    if is_restaurants_path(path):
        raise ValueError("assets/data/restaurants.json cannot be used as output")
    if not is_within(path, DISCOVERY_ROOT):
        raise ValueError("output path must remain under tools/discovery")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(candidates, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()

    try:
        raw_candidates = load_input(args.input)
        normalized = normalize_candidates(raw_candidates)
        write_output(args.output, normalized)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Raw candidates: {len(raw_candidates)}")
    print(f"Normalized candidates: {len(normalized)}")
    print(f"Output path: {args.output}")
    print("Reminder: output is local-only candidate data, not public database data.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
