# Data Verification Guide

## Purpose

This guide defines how to manually check restaurant data before public launch, wider SEO promotion, or an AdSense application. Verification should confirm factual suitability without copying third-party content.

## Current Dataset

- 45 restaurant entries
- 3 districts: Quarry Bay, Central, and Kwun Tong
- First-pass curated MVP data
- All entries start as unverified
- All entries remain publicly displayed while the first verification round is in progress

## Verification Status Values

| Status | Meaning |
| --- | --- |
| `unverified` | First-pass entry that has not been manually checked yet. |
| `verified` | Manually checked and accepted for public launch. |
| `needs_update` | Likely valid, but one or more data fields need correction. |
| `remove_candidate` | Should be removed or replaced before launch. |

## Manual Verification Checklist

For each restaurant, check:

- Restaurant still exists
- Restaurant is currently operating
- District is correct
- Cuisine category is appropriate
- Budget category is reasonable
- Meal types are reasonable
- Situations are reasonable
- Speed category is reasonable
- Descriptions are original and not copied
- No ratings are copied
- No reviews are copied
- No menu text is copied
- No third-party photos are copied

## Suggested Verification Sources

Use sources for factual confirmation only. Do not scrape.

- Restaurant official website
- Official social media page
- Google search result snippets
- OpenRice listing page for factual confirmation only
- Shopping mall directory
- Building directory
- Manual visit or user feedback

Do not copy reviews, ratings, menu text, or photos.

## How To Update A Restaurant After Verification

Update the factual fields that were checked, then change the verification metadata:

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

Use an ISO date in `YYYY-MM-DD` format for `lastChecked`.

## When To Use `needs_update`

Use `needs_update` when:

- District is probably right but location needs confirmation
- Cuisine category seems too broad
- Budget may be wrong
- Description should be rewritten
- Restaurant has moved
- Restaurant still exists but data needs correction

Set `needsReview` to `true` and explain the required correction in `reviewNotes`.

## When To Use `remove_candidate`

Use `remove_candidate` when:

- Restaurant appears closed
- Restaurant is outside the target district
- Restaurant name is wrong
- Entry is too uncertain
- Restaurant is unsuitable for the site

Set `publicDisplay` to `false` when an uncertain entry should no longer appear in public recommendations.

## Replacement Rule

If removing an entry:

- Keep 15 restaurants per district if possible
- Replace it with another manually verified restaurant
- Do not scrape
- Do not copy reviews, ratings, photos, or menu text

## Public Launch Rule

Before public launch:

- Prefer all entries to be verified
- At minimum, no entry should remain `remove_candidate`
- Any `needs_update` entry should be reviewed before submitting to AdSense
- Every publicly displayed entry should be suitable for recommendation
