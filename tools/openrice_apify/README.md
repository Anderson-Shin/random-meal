# Local OpenRice Apify Pipeline

## Active Workflow Location

The active OpenRice Apify workflow now lives inside the `random-meal` repository:

```text
/Users/minseong/Desktop/github/random-meal
```

The old standalone workspace at `/Users/minseong/Desktop/github/openrice-apify-workspace` was only a proof-of-concept and is no longer part of the active workflow.

Copy future manually downloaded Apify raw JSON files into:

```text
tools/openrice_apify/raw/
```

Run future commands from the repository root:

```bash
cd /Users/minseong/Desktop/github/random-meal

python tools/openrice_apify/scripts/normalize_openrice.py

python tools/openrice_apify/scripts/transform_candidates.py

python tools/openrice_apify/scripts/export_candidates.py \
  --input tools/openrice_apify/processed/openrice_candidates.json \
  --output tools/openrice_apify/processed/openrice_candidates.export.json

python tools/openrice_apify/scripts/merge_candidates.py \
  --input tools/openrice_apify/processed/openrice_transformed_candidates.json

python tools/openrice_apify/scripts/merge_candidates.py \
  --input tools/openrice_apify/processed/openrice_transformed_candidates.json \
  --write
```

- `normalize_openrice.py` creates normalized candidates from local raw JSON.
- `transform_candidates.py` applies local district, category, price, and multilingual mappings.
- `export_candidates.py` optionally validates normalized candidates before transformation.
- `merge_candidates.py` performs a dry run by default.
- `merge_candidates.py --write` appends non-duplicate hidden candidates to `assets/data/restaurants.json`.
- Merged entries remain hidden with `publicDisplay: false`.
- Manual review is required before making any merged entry public.

## Purpose

This directory contains a separate, local-only pipeline for preparing OpenRice Apify discovery data as review candidates.

It does not modify `assets/data/restaurants.json`, change frontend behavior, or connect to Cloudflare Pages. Candidate output is not approved public restaurant data.

## Pipeline

```text
Manually downloaded OpenRice Apify JSON
  -> normalize_openrice.py
  -> processed/openrice_candidates.json
     -> export_candidates.py (optional normalized-candidate validation)
     -> transform_candidates.py
     -> processed/openrice_transformed_candidates.json
     -> merge_candidates.py
     -> hidden public-database candidates for manual review
```

`run_actor.py` is an optional local helper for an explicitly approved future Apify run. It is never called by the normalizer or exporter.

The normalizer accepts input only from `raw/`, and normalization/export output paths are restricted to `processed/`. This prevents the tools from writing to the public restaurant database.

## Folder Structure

```text
tools/openrice_apify/
  README.md
  review-checklist.md
  requirements.txt
  .env.example
  config/
    price_map.json
    category_map.json
    district_map.json
  raw/
    .gitkeep
  processed/
    .gitkeep
  scripts/
    run_actor.py
    normalize_openrice.py
    mapping_utils.py
    transform_candidates.py
    export_candidates.py
    merge_candidates.py
    list_hidden_candidates.py
    generate_review_template.py
    apply_review_updates.py
```

## Input

Place manually downloaded Apify JSON files under:

```text
tools/openrice_apify/raw/
```

Input files may be JSON arrays or objects containing an `items` array. Raw downloads should be reviewed before use and should not contain credentials.

`config/category_map.json` is intentionally empty because raw category names are preserved without classification in this version.

## Output

The normalizer writes:

```text
tools/openrice_apify/processed/openrice_candidates.json
```

Output candidates keep only the approved factual fields and always include:

```json
{
  "dataOrigin": "openrice_apify",
  "needsReview": true,
  "publicDisplay": false
}
```

The pipeline does not automatically import candidates into the public database.

## Mapping and Transform Layer

The local mapping flow prepares richer random-meal style candidates before merge and review:

```text
Raw Apify JSON
  -> normalize_openrice.py
  -> transform_candidates.py
  -> merge_candidates.py
  -> list_hidden_candidates.py
  -> generate_review_template.py
  -> apply_review_updates.py
```

Run the mapping flow from the repository root:

```bash
python tools/openrice_apify/scripts/normalize_openrice.py

python tools/openrice_apify/scripts/transform_candidates.py

python tools/openrice_apify/scripts/merge_candidates.py \
  --input tools/openrice_apify/processed/openrice_transformed_candidates.json

python tools/openrice_apify/scripts/merge_candidates.py \
  --input tools/openrice_apify/processed/openrice_transformed_candidates.json \
  --write
```

- `district_map.json` controls area and district mapping.
- `category_map.json` controls cuisine, tags, meal types, situations, speed, and multilingual display helpers.
- `price_map.json` controls price-band mapping; the transformer converts the band into the public budget scale.
- Raw OpenRice category labels are preserved separately as `sourceCategories`.
- `tags` contains random-meal service tags. Multilingual display/helper tags are stored in `tags_en`, `tags_zhHant`, and `tags_zhHans`.
- The first expansion targets are Central, Quarry Bay, and Kwun Tong, with roughly 40 to 50 local candidates per area.
- All transformed and newly merged candidates remain hidden until manually reviewed.
- A monthly local database refresh cadence may be used after the workflow is proven.

## Merge Candidates

The merge tool converts normalized or transformed OpenRice candidates into the existing public restaurant schema. It is dry-run only by default:

```bash
python tools/openrice_apify/scripts/merge_candidates.py
```

Review the summary, then explicitly append new hidden candidates with:

```bash
python tools/openrice_apify/scripts/merge_candidates.py --write
```

Optional paths:

```bash
python tools/openrice_apify/scripts/merge_candidates.py \
  --input tools/openrice_apify/processed/openrice_candidates.json \
  --target assets/data/restaurants.json
```

The merge tool skips candidates with a duplicate `sourceRestaurantId` or duplicate normalized name and address. New entries remain `unverified`, require review, and use `publicDisplay: false`.

### Merge Safety Workflow

- The default command is a dry run. It reads candidates and the target database, prints a summary, and does not modify files.
- Passing `--write` explicitly modifies `assets/data/restaurants.json` by appending non-duplicate candidates at the end.
- Merged entries remain hidden by default with `publicDisplay: false`.
- Manual review is still required before public display. Review current operation, district, cuisine, budget, opening hours, descriptions, and general suitability before changing `publicDisplay`.
- Existing restaurant entries are preserved in their current order.
- Candidate fields such as `ratingOverall`, `openingHours`, and `popularDishes` are retained as internal review hints, not automatic approval for public display.

Recommended workflow:

```bash
# 1. Preview only. No files are modified.
python tools/openrice_apify/scripts/merge_candidates.py

# 2. Review the dry-run summary and candidate data manually.

# 3. Explicitly append non-duplicate hidden candidates.
python tools/openrice_apify/scripts/merge_candidates.py --write

# 4. Manually review every appended entry before public display.
```

## Review Hidden Candidates

List OpenRice Apify entries that are hidden with `publicDisplay: false`:

```bash
python tools/openrice_apify/scripts/list_hidden_candidates.py
```

Print the same concise candidate summaries as JSON:

```bash
python tools/openrice_apify/scripts/list_hidden_candidates.py --format json
```

An alternative restaurant database path can be supplied with `--target`. The script is read-only and never modifies files. Candidates remain hidden until they are manually reviewed and edited.

Use [review-checklist.md](review-checklist.md) before changing any candidate's `publicDisplay` value. Public display must only be enabled after a manual factual and content-safety review.

## Manual Approval Workflow

Generate a review template from hidden OpenRice Apify candidates:

```bash
python tools/openrice_apify/scripts/generate_review_template.py
```

Manually edit:

```text
tools/openrice_apify/processed/openrice_review_template.json
```

Fill in original descriptions and recommendations, final cuisine, budget, meal types, situations, speed, tags, reviewer, review date, and review notes. Only after completing manual review, set:

```json
{
  "reviewDecision": "approved",
  "approvedForPublicDisplay": true
}
```

Preview valid approval updates without modifying the database:

```bash
python tools/openrice_apify/scripts/apply_review_updates.py
```

Explicitly write complete approved updates:

```bash
python tools/openrice_apify/scripts/apply_review_updates.py --write
```

The apply script is dry-run by default. It rejects incomplete approvals, skips pending or rejected records, updates only hidden OpenRice Apify entries, and does not remove their source trace fields. Already-public OpenRice entries are skipped for safety. It never modifies non-OpenRice manual entries. Public descriptions must be original.

## Setup

Use a local virtual environment outside the public website runtime:

```bash
cd tools/openrice_apify
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Never commit `.env` or an Apify token.

## How To Run

Normalize manually downloaded JSON:

```bash
python tools/openrice_apify/scripts/normalize_openrice.py
```

Validate and prepare a future-import candidate file:

```bash
python tools/openrice_apify/scripts/export_candidates.py \
  --input tools/openrice_apify/processed/openrice_candidates.json \
  --output tools/openrice_apify/processed/openrice_candidates.export.json
```

Optional explicit Apify actor run:

```bash
python tools/openrice_apify/scripts/run_actor.py \
  --actor your-actor-id \
  --input actor-input.json \
  --output tools/openrice_apify/raw/openrice_download.json
```

The actor helper requires explicit arguments and local credentials. Do not use it without confirming source terms and project approval.

## Future Integration

Before any candidate can be considered for `assets/data/restaurants.json`:

1. Review the normalized candidate manually.
2. Confirm factual accuracy with stronger sources.
3. Write original public-facing descriptions.
4. Map fields into the active restaurant schema.
5. Keep uncertain entries hidden with `publicDisplay: false`.

Ratings, opening hours, popular dishes, coordinates, and other Apify-derived fields are candidate review hints only. Their inclusion here does not approve them for public display.
