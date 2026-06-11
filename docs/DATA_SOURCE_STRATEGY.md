# Restaurant Data Source Strategy

## Purpose

This document defines how the project may safely discover, confirm, and expand restaurant data. The goal is to build a useful Hong Kong restaurant database while avoiding copyright, terms-of-service, and reliability risks.

## Why Task 7A Is Paused

Branch-level manual verification remains useful, but it is paused while the project owner considers a broader database expansion strategy.

Before verifying entries one by one, the project should first decide:

- Which sources are allowed
- What data can be stored
- What data must not be copied
- Whether unofficial OpenRice API repositories are acceptable
- How to handle restaurant discovery versus public display

## Core Principle

Use third-party platforms only for factual discovery and confirmation.

All public-facing descriptions, recommendations, tags, and summaries must be written originally by this project.

## Allowed Data Types

- Restaurant name
- District or area
- General location hint, such as mall, building, or neighborhood
- Cuisine category written or normalized by us
- Budget category written or normalized by us
- Meal type tags written by us
- Situation tags written by us
- Speed tags written by us
- Original descriptions written by us
- Original recommended-for text written by us
- Source URL for factual confirmation
- Source type
- Last checked date
- Verification status
- Internal review notes
- Public display flag

## Disallowed Data Types

- Copied reviews
- Copied user comments
- Copied ratings
- Copied OpenRice rankings
- Copied menu text
- Copied promotional copy
- Copied third-party photos
- Third-party photo URLs used for display
- Scraped copyrighted descriptions
- Any data that violates source terms
- Any sensitive user data

## OpenRice Usage Policy

- OpenRice may be used for restaurant discovery and factual confirmation only.
- Do not copy reviews, ratings, rankings, photos, menu text, or promotional text from OpenRice.
- Do not reproduce OpenRice content on public pages.
- Do not present OpenRice-derived ratings or reviews as site content.
- Do not rely on OpenRice as the only source when marking a restaurant as verified.
- Store only source links and internal notes where appropriate.

## Unofficial OpenRice API Repository Policy

GitHub repositories claiming to provide an OpenRice API may be unofficial wrappers, scrapers, reverse-engineered endpoints, or unstable tools.

They may:

- Violate source platform terms
- Break without warning
- Return incomplete or stale data
- Create legal or compliance risk
- Be unsuitable for a public AdSense-supported production site

Policy:

- Do not integrate unofficial OpenRice API wrappers into production at this stage.
- Do not add them to frontend code.
- Do not add them to Cloudflare Pages.
- Do not add dependencies for them.
- If tested later, test only locally and privately for research.
- Any future use requires a separate technical and legal risk review document.

## Safe Source Hierarchy

Use this hierarchy for future restaurant confirmation:

1. Restaurant official website
2. Official restaurant social media
3. Shopping mall directory
4. Building directory
5. Restaurant group official branch list
6. Google Business Profile snippets for factual confirmation only
7. OpenRice listing for factual confirmation only
8. Manual visit or trusted user feedback

Prefer stronger sources before marking an entry as verified.

## Restaurant Discovery vs Public Display

### Discovery

A restaurant may be discovered from many public sources. Discovery does not mean the restaurant should be publicly displayed immediately.

### Public Display

A restaurant should only be displayed if it has enough factual confidence and does not rely on copied third-party content.

Use `publicDisplay: false` for uncertain or unsuitable entries.

## Proposed Future Source Fields

The following fields are proposed for a future schema task:

```json
{
  "sourceLinks": [
    {
      "type": "official",
      "url": "https://example.com",
      "checkedAt": "2026-06-11",
      "note": "Official branch page confirms district and current listing."
    }
  ],
  "sourceConfidence": "medium",
  "dataOrigin": "manual_curation"
}
```

Allowed `sourceConfidence` values:

- `low`
- `medium`
- `high`

Allowed `dataOrigin` values:

- `manual_curation`
- `official_source`
- `mall_directory`
- `user_suggestion`
- `discovery_source_only`

These are proposed fields only. Do not add them to `assets/data/restaurants.json` in this task.

## Review and Rating Policy

- Do not store or display third-party review text.
- Do not store or display third-party rating scores.
- Do not summarize reviews in a way that copies their substance.
- Site recommendations should be based on our own categories and original descriptions.

## Photo and Menu Policy

- Do not use third-party photos unless explicit permission or a safe license is confirmed.
- Do not copy menu item text or menu descriptions.
- Future image support should use original photos, licensed assets, or no photos.

## Source Attribution Policy

- For internal verification, source URLs may be stored as references.
- Public-facing attribution should not imply partnership with OpenRice, Google, or any restaurant unless officially confirmed.
- Avoid using third-party brand names in a way that suggests endorsement.

## Future Database Expansion Workflow

1. Collect candidate restaurants from safe discovery sources.
2. Remove duplicates.
3. Normalize district, cuisine, budget, meal type, situation, and speed fields.
4. Write original descriptions.
5. Add verification metadata.
6. Add source references internally.
7. Mark uncertain entries as `needs_update`.
8. Set `publicDisplay: false` for entries that should not appear publicly.
9. Review district counts and SEO page coverage.
10. Only then publish.

## Recommended Next Steps

1. Decide whether unofficial OpenRice API repositories should be avoided entirely or tested locally only.
2. Design future source metadata fields.
3. Create a local-only data import prototype if needed.
4. Expand restaurant coverage district by district.
5. Resume branch-level verification after the source strategy is accepted.
