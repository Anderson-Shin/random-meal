#!/usr/bin/env python3
"""Dry-run or explicitly apply complete OpenRice candidate review approvals."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_REVIEW_FILE = (
    REPO_ROOT
    / "tools"
    / "openrice_apify"
    / "processed"
    / "openrice_review_template.json"
)
DEFAULT_TARGET = REPO_ROOT / "assets" / "data" / "restaurants.json"

REQUIRED_TEXT_FIELDS = (
    "reviewer",
    "reviewDate",
    "reviewNotes",
    "finalCuisine",
    "finalBudget",
    "finalSpeed",
    "description_en",
    "description_zhHant",
    "description_zhHans",
    "recommendedFor_en",
    "recommendedFor_zhHant",
    "recommendedFor_zhHans",
)
REQUIRED_LIST_FIELDS = ("finalMealTypes", "finalSituations", "finalTags")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dry-run or explicitly apply reviewed OpenRice candidate approvals."
    )
    parser.add_argument("--review-file", type=Path, default=DEFAULT_REVIEW_FILE)
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    parser.add_argument("--write", action="store_true", help="Write valid approvals to target")
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


def nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value)


def approval_errors(review: dict[str, Any]) -> list[str]:
    errors = [
        field for field in REQUIRED_TEXT_FIELDS if not nonempty_text(review.get(field))
    ]
    errors.extend(
        field for field in REQUIRED_LIST_FIELDS if not nonempty_list(review.get(field))
    )
    return errors


def approved(review: dict[str, Any]) -> bool:
    return (
        review.get("reviewDecision") == "approved"
        and review.get("approvedForPublicDisplay") is True
    )


def update_values(review: dict[str, Any]) -> dict[str, Any]:
    source_links = review.get("sourceLinks")
    source_confidence = review.get("sourceConfidence")
    return {
        "cuisine": review["finalCuisine"].strip(),
        "budget": review["finalBudget"].strip(),
        "mealTypes": review["finalMealTypes"],
        "situations": review["finalSituations"],
        "speed": review["finalSpeed"].strip(),
        "tags": review["finalTags"],
        "description_en": review["description_en"].strip(),
        "description_zhHant": review["description_zhHant"].strip(),
        "description_zhHans": review["description_zhHans"].strip(),
        "recommendedFor_en": review["recommendedFor_en"].strip(),
        "recommendedFor_zhHant": review["recommendedFor_zhHant"].strip(),
        "recommendedFor_zhHans": review["recommendedFor_zhHans"].strip(),
        "sourceLinks": source_links if isinstance(source_links, list) else [],
        "sourceConfidence": (
            source_confidence.strip()
            if nonempty_text(source_confidence)
            else "low"
        ),
        "reviewNotes": review["reviewNotes"].strip(),
        "lastChecked": review["reviewDate"].strip(),
        "verificationStatus": "reviewed",
        "verified": True,
        "needsReview": False,
        "publicDisplay": True,
    }


def main() -> int:
    args = parse_args()
    try:
        reviews = load_array(args.review_file, "review file")
        restaurants = load_array(args.target, "target")
        hidden_openrice_by_id = {
            item.get("id"): item
            for item in restaurants
            if nonempty_text(item.get("id"))
            and item.get("dataOrigin") == "openrice_apify"
            and item.get("publicDisplay") is False
        }
        public_openrice_ids = {
            item.get("id")
            for item in restaurants
            if nonempty_text(item.get("id"))
            and item.get("dataOrigin") == "openrice_apify"
            and item.get("publicDisplay") is True
        }

        valid_updates = 0
        skipped = 0
        invalid = 0
        missing = 0
        skipped_already_public = 0

        for review in reviews:
            review_id = review.get("id")
            target = hidden_openrice_by_id.get(review_id)
            if target is None:
                if review_id in public_openrice_ids:
                    skipped_already_public += 1
                    print(
                        f"Skipped already-public OpenRice record: {review_id}",
                        file=sys.stderr,
                    )
                    continue
                missing += 1
                print(f"Missing target id: {review_id or '-'}", file=sys.stderr)
                continue
            if not approved(review):
                skipped += 1
                continue
            errors = approval_errors(review)
            if errors:
                invalid += 1
                print(
                    f"Invalid approval {review_id}: missing or empty {', '.join(errors)}",
                    file=sys.stderr,
                )
                continue
            target.update(update_values(review))
            valid_updates += 1

        if args.write:
            args.target.write_text(
                json.dumps(restaurants, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Review records read: {len(reviews)}")
    print(f"Target restaurants read: {len(restaurants)}")
    print(f"Approved valid updates: {valid_updates}")
    print(f"Skipped pending/rejected records: {skipped}")
    print(f"Invalid approval records: {invalid}")
    print(f"Missing target ids: {missing}")
    print(f"Skipped already-public OpenRice records: {skipped_already_public}")
    print(f"Write mode enabled: {args.write}")
    if not args.write:
        print("Dry run only. No files were modified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
