# Local-Only Discovery Prototype Plan

## Purpose

The future prototype may help organize restaurant candidate hints from local and private discovery work.

It must not automatically update `assets/data/restaurants.json`, publish data, connect to frontend JavaScript, or connect to Cloudflare Pages. It must not be described as an OpenRice API.

The correct name is:

```text
Local-Only Candidate Discovery Prototype
```

## Decision on cal65/Open-Rice

```text
Decision: Do not implement or run cal65/Open-Rice testing yet.
Status: Conditionally deferred.
```

- The reviewed `cal65/Open-Rice` repository is an unofficial OpenRice HTML scraper.
- It is not an official API.
- It must not be used in production.
- It must not connect to frontend JavaScript or Cloudflare Pages.
- It must not directly populate `assets/data/restaurants.json`.
- It may be reconsidered only after a separate local-only prototype task is approved.
- The project should first design and test a source-agnostic local discovery tool.

## Safer Implementation Direction

The project should not build an "OpenRice API." It may later build a local-only discovery tool that handles candidate hints from multiple source types:

- Official restaurant websites
- Official restaurant social media
- Mall directories
- Building directories
- Google Business Profile snippets for factual cross-checking only
- OpenRice listing pages for discovery or reference only
- User suggestions
- Local manual research

OpenRice is one possible discovery source, not the core of the system.

## Prototype Scope

The future prototype may:

- Read local input files
- Normalize candidate fields
- Drop unsafe fields
- Validate candidate shape
- Write a local candidate output file under `tools/discovery/`
- Mark candidates as `readyForPublicDb: false`
- Mark candidates as `reviewStatus: "not_reviewed"`
- Add `nextAction` instructions for manual review

The future prototype must not:

- Scrape from the public website
- Run inside the frontend
- Run on Cloudflare Pages
- Automatically update `assets/data/restaurants.json`
- Mark candidates as verified
- Set `sourceConfidence: high` based only on OpenRice
- Store or display reviews, ratings, rankings, photos, menu text, promotional copy, smiles, frowns, or raw HTML

## Allowed Candidate Fields

The future prototype output may contain only safe candidate hints:

```json
{
  "candidateId": "sample-quarry-bay-001",
  "candidateName": "Example Restaurant",
  "candidateArea": "Quarry Bay",
  "candidateDistrict": "Eastern Hong Kong",
  "candidateAddressHint": "Example building or neighborhood",
  "candidateCuisineHint": "Japanese",
  "candidateBudgetHint": "$$",
  "candidateMealTypeHints": ["lunch", "dinner"],
  "candidateSituationHints": ["solo", "friends"],
  "candidateSpeedHint": "quick",
  "discoverySource": "openrice_listing",
  "sourceUrl": "https://example.com/not-a-real-source",
  "sourceUsage": "discovery",
  "sourceConfidence": "low",
  "dataOrigin": "discovery_source_only",
  "discardedFields": [
    "price",
    "smiles",
    "frowns",
    "ratings",
    "reviews",
    "rankings",
    "photos",
    "menuText",
    "promotionalCopy",
    "rawHtml"
  ],
  "readyForPublicDb": false,
  "reviewStatus": "not_reviewed",
  "nextAction": "Cross-check with official website, mall directory, building directory, or another stronger source.",
  "notes": "Local candidate only. Do not import directly into restaurants.json."
}
```

This is a candidate format, not public restaurant data. Candidate output must go through [`tools/discovery/manual-review-worksheet.md`](../tools/discovery/manual-review-worksheet.md).

## Discarded Fields

The future prototype must explicitly discard:

- Price
- Smiles
- Frowns
- Ratings
- Reviews
- Rankings
- Photos
- Photo URLs
- Menu text
- Promotional copy
- Raw HTML
- Copied third-party descriptions
- Platform-generated popularity claims

Discarded means these fields must not be written to candidate output files, `assets/data/restaurants.json`, frontend code, documentation examples, or public pages.

## Recommended Prototype Architecture

Recommended future local-only structure:

```text
tools/discovery/
  README.md
  sample-candidates.json
  manual-review-worksheet.md
  local-candidates.example.json
  prototype-plan.md
```

The approved Phase 1 implementation script is placed under:

```text
tools/discovery/local_tools/
```

Current script name:

```text
normalize_candidates.py
```

The Phase 1 implementation uses local file input:

```text
python tools/discovery/local_tools/normalize_candidates.py --input tools/discovery/raw-candidates.example.json --output tools/discovery/local-candidates.example.json
```

This command describes a future file-only interface. It does not fetch OpenRice URLs.

## Input Modes for Future Prototype

### Phase 1: File-only mode

The tool reads a local JSON or CSV file prepared manually. It makes no network requests and performs no scraping. This is the recommended first implementation phase.

### Phase 2: Saved HTML mode, optional

The tool may parse a locally saved HTML file only if separately approved. It makes no network requests and stores no raw HTML in outputs.

### Phase 3: URL-fetch mode, strongly discouraged

Fetching URLs directly should be avoided unless explicitly approved later. If ever approved, it must remain local-only and rate-limited, and must not store raw HTML or unsafe fields.

Phase 3 is not approved.

## Phase 1 Implementation

Phase 1 file-only local normalization is now implemented with:

- [`tools/discovery/local_tools/normalize_candidates.py`](../tools/discovery/local_tools/normalize_candidates.py)
- [`tools/discovery/raw-candidates.example.json`](../tools/discovery/raw-candidates.example.json)
- [`tools/discovery/local-candidates.example.json`](../tools/discovery/local-candidates.example.json)

This implementation is file-only. It makes no network requests, does not fetch OpenRice URLs, does not scrape, and does not update `assets/data/restaurants.json`. It only demonstrates safe candidate normalization with fake or local input.

## Stop Conditions

Stop or reject the future prototype if:

- It requires copying reviews, ratings, rankings, photos, menu text, smiles, frowns, or raw HTML.
- It tries to connect to frontend JavaScript.
- It tries to run on Cloudflare Pages.
- It writes directly to `assets/data/restaurants.json`.
- It produces candidates without manual review fields.
- It encourages large-scale scraping.
- It relies only on OpenRice for high confidence.
- It breaks the static-first project rule.

## Recommended Next Task

```text
Task 8A: Review normalized fake candidate output and decide whether to allow real local candidate input
```

Any future task must continue to prohibit OpenRice URL fetching and scraping unless separately approved.
