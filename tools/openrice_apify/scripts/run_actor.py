#!/usr/bin/env python3
"""Explicit local helper for running an approved Apify actor."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

from apify_client import ApifyClient
from dotenv import load_dotenv


TOOL_ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = TOOL_ROOT / "raw"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Explicitly run an approved Apify actor and save raw JSON locally."
    )
    parser.add_argument("--actor", required=True)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        args.output.resolve().relative_to(RAW_ROOT.resolve())
    except ValueError:
        print("Error: output path must remain under tools/openrice_apify/raw", file=sys.stderr)
        return 1

    load_dotenv(TOOL_ROOT / ".env")
    token = os.getenv("APIFY_TOKEN")
    if not token:
        print("Error: APIFY_TOKEN is missing from the local environment", file=sys.stderr)
        return 1

    try:
        actor_input = json.loads(args.input.read_text(encoding="utf-8"))
        client = ApifyClient(token)
        run = client.actor(args.actor).call(run_input=actor_input)
        dataset_id = run.get("defaultDatasetId")
        if not dataset_id:
            raise ValueError("actor run did not return a default dataset ID")
        items = list(client.dataset(dataset_id).iterate_items())
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(items, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Saved {len(items)} raw records to {args.output}")
    print("Raw output remains local and must be normalized and manually reviewed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
