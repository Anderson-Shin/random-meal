# Codex Instructions

This file gives Codex a compact repository-level context for working on **What Should I Eat HK?**.

Use this file before starting any new task.

## Project Summary

What Should I Eat HK? is a multilingual, static-first Hong Kong restaurant decision website.

The site helps users choose lunch or dinner options using:

- District filters
- Meal filters
- Cuisine filters
- Budget filters
- Situation filters
- Speed filters
- Random picker
- Roulette picker
- District SEO pages

The current production site is deployed on Cloudflare Pages:

```text
https://what-should-i-eat-hk.pages.dev
```

## Required Reading Before Each Task

Before making changes, read these files:

- `README.md`
- `docs/MASTER.md`
- `docs/PM_RULES.md`
- `docs/ROADMAP.md`
- `docs/DATA_SCHEMA.md`
- `docs/DATA_VERIFICATION.md`
- `docs/DATA_SOURCE_STRATEGY.md`
- `docs/LOCAL_DISCOVERY_WORKFLOW.md`
- `docs/LOCAL_DISCOVERY_PROTOTYPE_PLAN.md`
- `docs/QA_CHECKLIST.md`
- `docs/LAUNCH_CHECKLIST.md`
- `docs/DOMAIN_SETUP.md`

For deployment-related tasks, also read:

- `docs/DEPLOYMENT.md`

For restaurant data tasks, also inspect:

- `assets/data/restaurants.json`
- `assets/js/app.js`
- `docs/DATA_SOURCE_STRATEGY.md`
- `docs/LOCAL_DISCOVERY_WORKFLOW.md`

## Non-Negotiable Project Rules

Keep the project:

- Static-first
- SEO-friendly
- Beginner-editable
- Low-cost
- Cloudflare Pages compatible
- Easy to maintain

Do not add unless explicitly requested:

- React
- Node.js
- npm dependencies
- Build tools
- Backend
- Database
- Login or user accounts
- AI recommendation
- Google Maps
- Paid APIs
- Real AdSense code
- Analytics trackers
- Reviews
- Ratings
- Third-party photos
- Copied menu text

Do not introduce environment variables for MVP work.

Do not add external scripts unless the task explicitly requires them.

## Development Rules

Prefer:

- Simple HTML
- Simple CSS
- Vanilla JavaScript
- JSON data
- Small focused changes
- Clear documentation updates

Avoid:

- Large refactors
- Clever abstractions
- Premature features
- Changing unrelated files
- Changing copy or data without a clear reason

If a task can be completed by updating documentation only, do not change the app code.

## Restaurant Data Rules

Restaurant data lives in:

```text
assets/data/restaurants.json
```

Each restaurant must follow `docs/DATA_SCHEMA.md`.

Each restaurant must include verification metadata:

- `verificationStatus`
- `verified`
- `lastChecked`
- `needsReview`
- `publicDisplay`
- `reviewNotes`

Each restaurant must also include source metadata:

- `sourceLinks`
- `sourceConfidence`
- `dataOrigin`

Do not remove these fields. Source metadata does not mean the restaurant is verified. Do not set `sourceConfidence: high` based only on OpenRice.

Allowed `verificationStatus` values:

- `unverified`
- `verified`
- `needs_update`
- `remove_candidate`

Use `publicDisplay: false` only when a restaurant should be hidden from public recommendations.

The app should only hide entries where:

```js
restaurant.publicDisplay === false
```

Do not copy third-party reviews, ratings, photos, menu text, or marketing copy.

Use external sources only for factual confirmation.

New candidate entries from weak discovery sources should default to:

```json
{
  "sourceConfidence": "low",
  "dataOrigin": "discovery_source_only",
  "verificationStatus": "unverified",
  "verified": false,
  "needsReview": true,
  "publicDisplay": false
}
```

Do not add OpenRice scraper code unless a later local-only prototype task explicitly approves it.

## Local Discovery Artifact Rules

- Candidate files under `tools/discovery/` are local and private artifacts.
- Candidate files are not production data.
- Candidate files must not be imported automatically into `assets/data/restaurants.json`.
- `tools/discovery/sample-candidates.json` must use fake sample data only unless a future task explicitly approves real local candidates.
- `tools/discovery/manual-review-worksheet.md` must be used before drafting real candidates into `assets/data/restaurants.json`.
- Do not connect `tools/discovery/` to frontend JavaScript or Cloudflare Pages.
- Do not add scraper code or dependencies unless a future local-only prototype task explicitly approves them.
- Read `docs/LOCAL_DISCOVERY_PROTOTYPE_PLAN.md` before any discovery tool implementation task.
- Prefer file-only local normalization as the first prototype implementation.
- Do not implement URL fetching or fetch OpenRice URLs.
- Any future discovery tool output must remain under `tools/discovery/`.
- Any future discovery tool must not modify `assets/data/restaurants.json`.
- Any future discovery tool must not connect to frontend JavaScript or Cloudflare Pages.
- The only currently approved discovery implementation is file-only local normalization.
- `tools/discovery/local_tools/normalize_candidates.py` must not be changed to fetch URLs unless a later task explicitly approves it.
- The normalizer must not import network or scraping libraries.
- The normalizer must not read or write `assets/data/restaurants.json`.
- Generated candidate outputs must remain under `tools/discovery/`.
- Generated candidate outputs must go through `tools/discovery/manual-review-worksheet.md` before any database draft.

## Restaurant Data Source Strategy Rules

- Read `docs/DATA_SOURCE_STRATEGY.md` before any restaurant data expansion, API, scraping, import, or verification task.
- Do not add OpenRice API wrappers, scraping code, crawler code, or external data dependencies unless explicitly approved in a later task.
- Do not copy reviews, ratings, rankings, photos, menu text, or promotional copy from OpenRice or any third-party platform.
- Use third-party sources for factual confirmation only.
- Keep all public-facing descriptions original.
- Treat unofficial OpenRice API repositories as risky and not production-approved.
- If a future task proposes data import, keep it local and private first. Do not integrate it into Cloudflare Pages or frontend code.

## OpenRice Repository Policy

- The reviewed `cal65/Open-Rice` repository is classified as an unofficial HTML scraper.
- Do not integrate it into production.
- Do not add it to Cloudflare Pages.
- Do not add it to frontend JavaScript.
- Do not add Python scraping scripts or dependencies unless a future task explicitly approves a local-only prototype.
- Do not store or display smiles, frowns, OpenRice ratings, reviews, rankings, photos, menu text, promotional copy, or raw HTML.
- Treat `restaurant_name`, `address`, `region`, and cuisine/type fields only as temporary discovery hints.
- Cross-check any candidate restaurant discovered from this source with stronger sources before public display.

## Data Verification Workflow

Verify restaurants district by district:

1. Quarry Bay
2. Central
3. Kwun Tong

For each restaurant, check:

- Restaurant still exists
- Restaurant appears currently operating
- District is correct
- Cuisine category is reasonable
- Budget category is reasonable
- Meal types are reasonable
- Situations are reasonable
- Speed category is reasonable
- Descriptions are original
- No copied reviews, ratings, photos, or menu text

After verification, update the metadata.

Example verified metadata:

```json
{
  "verificationStatus": "verified",
  "verified": true,
  "lastChecked": "2026-06-11",
  "needsReview": false,
  "publicDisplay": true,
  "reviewNotes": "Verified restaurant name, district, cuisine, and general suitability."
}
```

If uncertain, use `needs_update` or `remove_candidate` and explain why in `reviewNotes`.

## SEO and Domain Rules

Current canonical, sitemap, robots, and Open Graph URLs use:

```text
https://what-should-i-eat-hk.pages.dev
```

Do not replace this unless a custom domain is connected.

After a custom domain is connected, update all occurrences of the Pages domain in:

- `sitemap.xml`
- `robots.txt`
- District page canonical URLs
- District page Open Graph URLs
- Documentation that mentions the production domain

## Roadmap Discipline

Before starting, check `docs/ROADMAP.md`.

Implement only the requested task or the next clearly appropriate task.

After finishing, update `docs/ROADMAP.md` when task status changes.

Update `README.md` only when the current status, project scope, deployment state, or documentation links change.

## QA Requirements

After changes, check what is relevant:

- JSON remains valid
- JavaScript syntax remains valid
- Homepage still loads
- Filters still work
- Random picker still works
- Roulette still works
- Language switcher still works
- District pages still load
- Sitemap and robots remain valid
- No console errors are introduced
- Cloudflare Pages compatibility is preserved

For restaurant data changes, confirm:

- The total number of entries is expected
- District counts are expected
- Required schema fields exist
- `publicDisplay: false` entries are intentionally hidden

## Response Format After Each Task

When finished, summarize:

1. Files created
2. Files modified
3. What changed
4. Validation performed
5. Any manual verification still required
6. Recommended next task

## Current Recommended Next Task

Proceed with:

```text
Task 8A: Review normalized fake candidate output and decide whether to allow real local candidate input
```

Do not mark restaurants as `verified` unless factual verification was actually performed.
