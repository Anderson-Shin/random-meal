# Local Discovery Workflow

## Purpose

This workflow is for local and private restaurant candidate discovery only. It is not a production data pipeline and does not connect to Cloudflare Pages or frontend code.

## Non-Negotiable Rules

- Do not integrate scrapers into production.
- Do not run scraping from the public website.
- Do not add scraper code to frontend JavaScript.
- Do not add scraping dependencies unless a future local-only prototype task explicitly approves them.
- Do not store or display reviews, ratings, rankings, photos, menu text, promotional copy, smiles, frowns, or raw HTML.
- Do not automatically write scraped data into `assets/data/restaurants.json`.
- Every candidate must be manually reviewed before public display.

## Candidate Discovery Stage

Candidate restaurants may be discovered from:

- Official restaurant websites
- Official restaurant social media
- Mall directories
- Building directories
- Google Business Profile snippets for factual confirmation only
- OpenRice listing pages for factual discovery only
- Local and private research tools, if separately approved

Discovery does not mean verification. Discovery does not mean public display.

## Candidate File Format

A local-only candidate file may use this format:

```json
[
  {
    "candidateName": "Example Restaurant",
    "candidateArea": "Quarry Bay",
    "candidateAddressHint": "Taikoo Place",
    "candidateCuisineHint": "Japanese",
    "discoverySource": "openrice_listing",
    "sourceUrl": "https://example.com",
    "sourceUsage": "discovery",
    "discardedFields": [
      "smiles",
      "frowns",
      "ratings",
      "reviews",
      "photos",
      "menuText",
      "rawHtml"
    ],
    "readyForPublicDb": false,
    "nextAction": "Cross-check with official website, mall directory, or building directory."
  }
]
```

## Local Discovery Artifacts

- [`tools/discovery/sample-candidates.json`](../tools/discovery/sample-candidates.json) is a format example only and contains fake placeholder data.
- [`tools/discovery/manual-review-worksheet.md`](../tools/discovery/manual-review-worksheet.md) must be used before any candidate is drafted into `assets/data/restaurants.json`.

## OpenRice Scraper Handling

The reviewed `cal65/Open-Rice` repository is classified as:

```text
Type: unofficial OpenRice HTML scraper
Allowed use: local/private discovery only, if separately approved
Production use: not allowed
Frontend use: not allowed
Direct public DB import: not allowed
```

Allowed only as temporary hints:

- Restaurant name
- Address hint
- Region hint
- Cuisine or type hint

Always discard:

- Price
- Smiles
- Frowns
- Ratings
- Reviews
- Rankings
- Photos
- Menu text
- Promotional copy
- Raw HTML

## Candidate Review Stage

Before a candidate can enter `assets/data/restaurants.json`, check:

- Duplicate restaurant ID
- District accuracy
- Current operation likelihood
- Source strength
- Cuisine category
- Budget category
- Meal type fit
- Situation tags
- Speed category
- Original descriptions
- No copied third-party content

## Public Database Entry Stage

When a candidate is accepted into `assets/data/restaurants.json`, weak discovery-source metadata should start like this:

```json
{
  "sourceLinks": [
    {
      "type": "openrice_listing",
      "url": "https://example.com",
      "checkedAt": "2026-06-11",
      "usage": "discovery",
      "note": "Used only as a discovery hint. Not used as sole verification source."
    }
  ],
  "sourceConfidence": "low",
  "dataOrigin": "discovery_source_only",
  "verificationStatus": "unverified",
  "verified": false,
  "lastChecked": null,
  "needsReview": true,
  "publicDisplay": false
}
```

New candidate entries from weak discovery sources should usually start with `publicDisplay: false`. They can become public only after stronger cross-checking and original descriptions are added. OpenRice alone must not create `sourceConfidence: high`.

## Recommended Future Tasks

1. Review the local candidate template.
2. Review the manual candidate worksheet.
3. Decide whether to test `cal65/Open-Rice` locally.
4. If approved, create a separate local-only prototype task.
5. Do not run scraping or expand the public database until explicitly approved.
