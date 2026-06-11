# Local Discovery Folder

## Purpose

This folder is for local and private restaurant candidate discovery artifacts.

- Candidate files are not public restaurant data.
- Candidate files are not verified data.
- Candidate files are not automatically used by the website.
- This folder is not production code.
- This folder must not be imported by frontend JavaScript or deployed as an active data pipeline.
- Candidate files must not automatically write to `assets/data/restaurants.json`.

## Non-Negotiable Rules

- Do not add scraper code here unless a future task explicitly approves a local-only prototype.
- Do not add OpenRice scraper dependencies in this task.
- Do not run scraping from the website.
- Do not connect this folder to Cloudflare Pages.
- Do not connect this folder to frontend JavaScript.
- Do not automatically import candidates into `assets/data/restaurants.json`.
- Do not store reviews, ratings, rankings, photos, menu text, promotional copy, smiles, frowns, or raw HTML.

## Files

- `sample-candidates.json` - Example candidate format with fake placeholder data only.
- `manual-review-worksheet.md` - Manual review checklist for candidates before database entry.

Allowed `reviewStatus` values:

- `not_reviewed`
- `needs_more_sources`
- `ready_for_database_draft`
- `rejected`

## Candidate Lifecycle

1. Candidate discovered locally.
2. Unsafe fields discarded.
3. Candidate recorded in the local candidate template.
4. Candidate manually reviewed.
5. Stronger sources cross-checked.
6. Original descriptions written.
7. Only then can a candidate be considered for `assets/data/restaurants.json`.
8. Weak candidates should start with `publicDisplay: false`.

## OpenRice Handling

- `cal65/Open-Rice` is classified as an unofficial OpenRice HTML scraper.
- It is not production-approved.
- It is not frontend-approved.
- It may only be considered for future local and private discovery if explicitly approved.
- OpenRice alone must not produce `sourceConfidence: high`.
- OpenRice-derived reviews, ratings, rankings, photos, menu text, promotional copy, smiles, frowns, and raw HTML must be discarded.

## Prototype Plan

See [`../../docs/LOCAL_DISCOVERY_PROTOTYPE_PLAN.md`](../../docs/LOCAL_DISCOVERY_PROTOTYPE_PLAN.md).

- The first future implementation should be file-only local normalization.
- This folder must not contain direct URL scraping unless a later task explicitly approves it.
- Candidate outputs must remain local and private until manually reviewed.
