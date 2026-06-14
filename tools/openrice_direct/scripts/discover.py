#!/usr/bin/env python3
"""Discover minimal OpenRice restaurant candidates from district listing pages."""

from __future__ import annotations

import argparse
from datetime import datetime
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG = REPO_ROOT / "tools" / "openrice_direct" / "config" / "districts.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "tools" / "openrice_apify" / "raw"
BASE_URL = "https://www.openrice.com/en/hongkong/restaurants"
RESTAURANT_ID_PATTERN = re.compile(r"(?:^|[-/])r(\d+)(?:$|/)", re.IGNORECASE)
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
)
SECURITY_PAGE_MARKERS = (
    "Security Check in Progress",
    "BytePlus",
    "_wafchallengeid",
)


class ListingParser(HTMLParser):
    """Collect links and readable anchor text without storing raw HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []
        self._anchor_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a" and self._href is None:
            self._href = dict(attrs).get("href")
            self._text = []
            self._anchor_depth = 1
        elif self._href is not None:
            self._anchor_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if self._href is None:
            return
        self._anchor_depth -= 1
        if tag.lower() == "a" or self._anchor_depth <= 0:
            text = " ".join(" ".join(self._text).split())
            if self._href:
                self.links.append((self._href, text))
            self._href = None
            self._text = []
            self._anchor_depth = 0

    def handle_data(self, data: str) -> None:
        if self._href is not None and data.strip():
            self._text.append(data.strip())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Discover minimal OpenRice candidates from district listing pages."
    )
    parser.add_argument(
        "--district",
        required=True,
        help="District config key or 'all'",
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-items", type=int, default=50)
    parser.add_argument("--delay-seconds", type=float, default=3)
    parser.add_argument("--timeout-seconds", type=float, default=20)
    parser.add_argument("--pages", type=int, default=3)
    local_input = parser.add_mutually_exclusive_group()
    local_input.add_argument("--html-file", type=Path)
    local_input.add_argument("--html-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def load_districts(path: Path) -> dict[str, dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"district config is invalid JSON: {error.msg}") from error
    if not isinstance(data, dict):
        raise ValueError("district config must be a JSON object")
    required = {"label", "districtId", "district", "outputSlug"}
    for key, value in data.items():
        if not isinstance(value, dict) or not required <= set(value):
            raise ValueError(f"district config entry '{key}' is missing required fields")
    return data


def build_listing_url(district_id: int) -> str:
    return f"{BASE_URL}?{urlencode({'regionId': 0, 'districtId': district_id, 'tabIndex': 0})}"


def is_openrice_url(url: str) -> bool:
    parsed = urlparse(url)
    hostname = (parsed.hostname or "").lower()
    return parsed.scheme in {"http", "https"} and (
        hostname == "openrice.com" or hostname.endswith(".openrice.com")
    )


def canonical_url(url: str) -> str:
    parsed = urlparse(url)
    return urlunparse(("https", parsed.netloc.lower(), parsed.path, "", "", ""))


def restaurant_id_from_url(url: str) -> int | None:
    match = RESTAURANT_ID_PATTERN.search(urlparse(url).path)
    return int(match.group(1)) if match else None


def is_same_district_listing(url: str, district_id: int) -> bool:
    if not is_openrice_url(url):
        return False
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    return (
        parsed.path.rstrip("/").endswith("/restaurants")
        and query.get("districtId") == [str(district_id)]
    )


def parse_listing(
    html: str,
    page_url: str,
    district: str,
    district_id: int,
    fetched_at: str,
) -> tuple[list[dict[str, Any]], list[str]]:
    parser = ListingParser()
    parser.feed(html)
    candidates: list[dict[str, Any]] = []
    pagination: list[str] = []

    for href, text in parser.links:
        absolute = urljoin(page_url, href)
        if not is_openrice_url(absolute):
            continue
        if is_same_district_listing(absolute, district_id):
            pagination.append(absolute)
            continue
        restaurant_id = restaurant_id_from_url(absolute)
        if restaurant_id is None or not text:
            continue
        candidates.append(
            {
                "restaurant_id": restaurant_id,
                "name": text,
                "district": district,
                "address": "",
                "latitude": None,
                "longitude": None,
                "price_range_id": None,
                "rating_overall": None,
                "categories": [],
                "opening_hours": {},
                "popular_dishes": [],
                "source_url": canonical_url(absolute),
                "source_name": "openrice_direct",
                "fetched_at": fetched_at,
            }
        )
    return candidates, pagination


def fetch_html(url: str, timeout_seconds: float) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-HK,en;q=0.9,zh-HK;q=0.8",
        },
    )
    with urlopen(request, timeout=timeout_seconds) as response:
        content_type = response.headers.get_content_charset() or "utf-8"
        html = response.read().decode(content_type, errors="replace")
    validate_listing_html(html, "OpenRice response")
    return html


def validate_listing_html(html: str, source: str) -> None:
    if any(marker in html for marker in SECURITY_PAGE_MARKERS):
        raise ValueError(
            f"{source} appears to be a security-check page, not a listing page; "
            "discovery stopped without attempting to bypass it"
        )


def local_html_files(html_file: Path | None, html_dir: Path | None) -> list[Path]:
    if html_file is not None:
        if not html_file.is_file():
            raise ValueError(f"local HTML file does not exist: {html_file}")
        return [html_file]
    if html_dir is None:
        return []
    if not html_dir.is_dir():
        raise ValueError(f"local HTML directory does not exist: {html_dir}")
    files = sorted(
        path
        for path in html_dir.iterdir()
        if path.is_file() and path.suffix.casefold() in {".html", ".htm"}
    )
    if not files:
        raise ValueError(f"no .html or .htm files found under: {html_dir}")
    return files


def discover_district(
    config: dict[str, Any],
    max_items: int,
    pages: int,
    delay_seconds: float,
    timeout_seconds: float,
) -> tuple[list[dict[str, Any]], int, int, bool]:
    district_id = int(config["districtId"])
    queue = [build_listing_url(district_id)]
    visited: set[str] = set()
    candidates: list[dict[str, Any]] = []
    seen: set[str] = set()
    skipped_duplicates = 0
    pagination_found = False
    fetched_at = datetime.now().astimezone().isoformat(timespec="seconds")

    while queue and len(visited) < pages and len(candidates) < max_items:
        page_url = queue.pop(0)
        page_key = canonical_url(page_url) + "?" + urlparse(page_url).query
        if page_key in visited:
            continue
        if visited and delay_seconds:
            time.sleep(delay_seconds)
        html = fetch_html(page_url, timeout_seconds)
        visited.add(page_key)
        page_candidates, pagination = parse_listing(
            html,
            page_url,
            str(config["district"]),
            district_id,
            fetched_at,
        )
        pagination_found = pagination_found or bool(pagination)
        for candidate in page_candidates:
            key = str(candidate["restaurant_id"] or candidate["source_url"])
            if key in seen:
                skipped_duplicates += 1
                continue
            seen.add(key)
            candidates.append(candidate)
            if len(candidates) >= max_items:
                break
        for url in pagination:
            key = canonical_url(url) + "?" + urlparse(url).query
            if key not in visited and url not in queue:
                queue.append(url)

    return candidates, len(visited), skipped_duplicates, pagination_found


def discover_local_html(
    config: dict[str, Any],
    files: list[Path],
    max_items: int,
) -> tuple[list[dict[str, Any]], int, int]:
    district_id = int(config["districtId"])
    page_url = build_listing_url(district_id)
    candidates: list[dict[str, Any]] = []
    seen: set[str] = set()
    skipped_duplicates = 0
    fetched_at = datetime.now().astimezone().isoformat(timespec="seconds")
    files_read = 0

    for path in files:
        html = path.read_text(encoding="utf-8", errors="replace")
        validate_listing_html(html, f"saved HTML file {path}")
        files_read += 1
        page_candidates, _ = parse_listing(
            html,
            page_url,
            str(config["district"]),
            district_id,
            fetched_at,
        )
        for candidate in page_candidates:
            key = str(candidate["restaurant_id"] or candidate["source_url"])
            if key in seen:
                skipped_duplicates += 1
                continue
            seen.add(key)
            candidates.append(candidate)
            if len(candidates) >= max_items:
                return candidates, files_read, skipped_duplicates
    return candidates, files_read, skipped_duplicates


def output_path(output_dir: Path, output_slug: str) -> Path:
    date = datetime.now().astimezone().date().isoformat()
    return output_dir / f"openrice_direct_{output_slug}_{date}.json"


def validate_args(args: argparse.Namespace) -> None:
    if args.max_items < 1:
        raise ValueError("--max-items must be at least 1")
    if args.pages < 1:
        raise ValueError("--pages must be at least 1")
    if args.delay_seconds < 0:
        raise ValueError("--delay-seconds must not be negative")
    if args.timeout_seconds <= 0:
        raise ValueError("--timeout-seconds must be greater than zero")
    if (args.html_file is not None or args.html_dir is not None) and args.district == "all":
        raise ValueError(
            "local HTML mode requires one district key; run each district separately"
        )


def main() -> int:
    args = parse_args()
    try:
        validate_args(args)
        districts = load_districts(args.config)
        if args.district == "all":
            selected = list(districts.items())
        elif args.district in districts:
            selected = [(args.district, districts[args.district])]
        else:
            raise ValueError(
                f"unknown district '{args.district}'; choose one of: "
                f"{', '.join(sorted(districts))}, all"
            )

        for key, config in selected:
            files = local_html_files(args.html_file, args.html_dir)
            if files:
                candidates, pages_fetched, skipped = discover_local_html(
                    config,
                    files,
                    args.max_items,
                )
                pagination_found = True
            else:
                candidates, pages_fetched, skipped, pagination_found = discover_district(
                    config,
                    args.max_items,
                    args.pages,
                    args.delay_seconds,
                    args.timeout_seconds,
                )
            if not candidates:
                raise ValueError(
                    f"no candidates found for {key}; no output file was written. "
                    "Confirm the saved HTML is a rendered/listing page source and "
                    "contains restaurant links with IDs, or try saving a different "
                    "page view."
                )
            path = output_path(args.output_dir, str(config["outputSlug"]))
            if not args.dry_run:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    json.dumps(candidates, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
            print(f"District key: {key}")
            print(f"Label: {config['label']}")
            print(f"District ID: {config['districtId']}")
            print(f"Pages fetched: {pages_fetched}")
            print(f"Candidates extracted: {len(candidates)}")
            print(f"Output path: {path if not args.dry_run else 'dry-run; not written'}")
            print(f"Skipped duplicates: {skipped}")
            print(f"Input mode: {'local HTML' if files else 'URL fetch'}")
            if not pagination_found:
                print("Pagination was not expanded because no reliable listing links were found.")
    except (HTTPError, URLError, TimeoutError, OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
