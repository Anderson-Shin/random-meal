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
- `docs/QA_CHECKLIST.md`
- `docs/LAUNCH_CHECKLIST.md`
- `docs/DOMAIN_SETUP.md`

For deployment-related tasks, also read:

- `docs/DEPLOYMENT.md`

For restaurant data tasks, also inspect:

- `assets/data/restaurants.json`
- `assets/js/app.js`

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
Task 7A: Manually verify Quarry Bay restaurants
```

Do not mark restaurants as `verified` unless factual verification was actually performed.
