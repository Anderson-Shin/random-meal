# Restaurant Data Schema

The restaurant dataset lives at:

```text
assets/data/restaurants.json
```

The file contains a JSON array of restaurant objects.

## Example Object

```json
{
  "id": "quarry-bay-japanese-001",
  "name": "Restaurant Name",
  "area": "Quarry Bay",
  "district": "Eastern Hong Kong",
  "cuisine": "Japanese",
  "budget": "$$",
  "mealTypes": ["lunch", "dinner"],
  "situations": ["solo", "friends", "team lunch"],
  "speed": "quick",
  "tags": ["quick lunch", "office worker friendly"],
  "description_en": "Short manually written description.",
  "description_zhHant": "Traditional Chinese description.",
  "description_zhHans": "Simplified Chinese description.",
  "recommendedFor_en": "Quick solo lunch or casual team lunch.",
  "recommendedFor_zhHant": "Traditional Chinese recommendation.",
  "recommendedFor_zhHans": "Simplified Chinese recommendation.",
  "sourceNote": "Manually curated. No reviews, ratings, photos, or menu text copied.",
  "verificationStatus": "unverified",
  "verified": false,
  "lastChecked": null,
  "needsReview": true,
  "publicDisplay": true,
  "reviewNotes": "First-pass MVP entry. Verify current operation, district accuracy, cuisine category, and suitability before public launch.",
  "sourceLinks": [],
  "sourceConfidence": "low",
  "dataOrigin": "manual_curation"
}
```

## Field Definitions

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Unique, stable, lowercase kebab-case identifier. Use the pattern `area-cuisine-number`. |
| `name` | string | Public factual restaurant name. |
| `area` | string | User-facing neighborhood or area, such as `Quarry Bay`. |
| `district` | string | Broader Hong Kong district used for grouping. |
| `cuisine` | string | Primary cuisine category using an approved consistent label. |
| `budget` | string | Relative price category: `$`, `$$`, `$$$`, or `$$$$`. |
| `mealTypes` | string[] | Supported meal occasions, such as `breakfast`, `lunch`, `dinner`, or `late night`. |
| `situations` | string[] | Useful dining contexts, such as `solo`, `friends`, `date`, or `team lunch`. |
| `speed` | string | Expected meal pace category, such as `quick`, `regular`, or `leisurely`. |
| `tags` | string[] | Short normalized discovery labels that add useful filtering context. |
| `description_en` | string | Short, original English description based on public facts. |
| `description_zhHant` | string | Short, original Traditional Chinese description. |
| `description_zhHans` | string | Short, original Simplified Chinese description. |
| `recommendedFor_en` | string | Original English summary of suitable dining situations. |
| `recommendedFor_zhHant` | string | Original Traditional Chinese recommendation summary. |
| `recommendedFor_zhHans` | string | Original Simplified Chinese recommendation summary. |
| `sourceNote` | string | Internal provenance note confirming how the entry was curated. |

## Optional OpenRice Apify Candidate Fields

These optional fields may come from the local OpenRice Apify candidate pipeline:

| Field | Type | Description |
| --- | --- | --- |
| `sourceRestaurantId` | integer or null | Source restaurant identifier used for local deduplication and traceability. |
| `sourceName` | string | Local pipeline source name, such as `openrice_apify`. |
| `address` | string | Candidate address hint requiring manual review. |
| `latitude` | number or null | Candidate latitude requiring manual review. |
| `longitude` | number or null | Candidate longitude requiring manual review. |
| `priceRangeId` | integer or null | Source price-range identifier. |
| `priceBand` | string | Locally mapped price band. |
| `ratingOverall` | number or null | Source rating hint retained for internal candidate review only. |
| `openingHours` | object | Source opening-hours hint requiring manual verification. |
| `popularDishes` | string[] | Source popular-dish hints retained for internal review only. |

`assets/data/restaurants.json` remains the public static source of truth. OpenRice-derived entries must remain hidden until manually reviewed and should start with:

```json
{
  "verificationStatus": "unverified",
  "verified": false,
  "needsReview": true,
  "publicDisplay": false,
  "sourceConfidence": "low",
  "dataOrigin": "openrice_apify"
}
```

Optional OpenRice Apify fields do not mean an entry is verified or approved for public display.

## Verification Fields

| Field | Type | Description |
| --- | --- | --- |
| `verificationStatus` | string | Manual review state. Allowed values: `unverified`, `verified`, `needs_update`, or `remove_candidate`. |
| `verified` | boolean | `true` only after a manual check accepts the entry for public launch. |
| `lastChecked` | string or null | Date of the latest manual check in `YYYY-MM-DD` format, or `null` when not checked. |
| `needsReview` | boolean | Whether the entry still requires manual attention. |
| `publicDisplay` | boolean | Whether the entry may appear in public recommendations. Entries with `false` are hidden by the homepage app. |
| `reviewNotes` | string | Short note explaining the verification result or remaining work. |

## Source Metadata Fields

| Field | Type | Description |
| --- | --- | --- |
| `sourceLinks` | array | Internal list of source references used for discovery, verification, or cross-checking. An empty array is allowed for first-pass manually curated entries. |
| `sourceConfidence` | string | Current confidence level of the entry's source support. Allowed values: `low`, `medium`, or `high`. |
| `dataOrigin` | string | How the entry originally entered the database. Allowed values: `manual_curation`, `official_source`, `mall_directory`, `user_suggestion`, `local_research`, `discovery_source_only`, or `openrice_apify`. |

Each `sourceLinks` object uses this format:

```json
{
  "type": "official_website",
  "url": "https://example.com",
  "checkedAt": "2026-06-11",
  "usage": "verification",
  "note": "Official source confirms location and current listing."
}
```

Allowed `sourceLinks[].type` values:

- `official_website`
- `official_social`
- `mall_directory`
- `building_directory`
- `google_business_profile`
- `openrice_listing`
- `local_research`
- `user_suggestion`

Allowed `sourceLinks[].usage` values:

- `discovery`
- `verification`
- `cross_check`
- `do_not_publish`

Allowed `sourceConfidence` values:

- `low`
- `medium`
- `high`

Allowed `dataOrigin` values:

- `manual_curation`
- `official_source`
- `mall_directory`
- `user_suggestion`
- `local_research`
- `discovery_source_only`
- `openrice_apify`

Default source metadata for first-pass entries:

```json
{
  "sourceLinks": [],
  "sourceConfidence": "low",
  "dataOrigin": "manual_curation"
}
```

Rules:

- `sourceConfidence: high` requires stronger confirmation than OpenRice alone.
- `openrice_listing` may only be used as an internal source reference.
- OpenRice-derived reviews, rankings, photos, menu text, promotional copy, smiles, frowns, and raw HTML must never be stored. `ratingOverall` may be retained only as an optional hidden candidate-review hint for `openrice_apify` entries.
- Empty `sourceLinks` means the entry is not yet source-documented.
- Source metadata does not mean the restaurant is verified.
- Verification still depends on `verificationStatus`, `verified`, `lastChecked`, `needsReview`, and `reviewNotes`.

New first-pass entries should use:

```json
{
  "verificationStatus": "unverified",
  "verified": false,
  "lastChecked": null,
  "needsReview": true,
  "publicDisplay": true,
  "reviewNotes": "First-pass MVP entry. Verify current operation, district accuracy, cuisine category, and suitability before public launch."
}
```

After a successful manual check, use:

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

## Data Rules

- Do not scrape restaurant websites, platforms, or directories.
- Do not copy reviews.
- Do not use third-party ratings in public-facing content. Optional `ratingOverall` values from hidden `openrice_apify` candidates are internal review hints only.
- Do not copy photos.
- Do not copy menu text.
- Use manually written descriptions and recommendations.
- Use public factual information only.
- Keep category labels and capitalization consistent.
- Keep descriptions concise, useful, and free from unverifiable claims.
- Review entries for accuracy before release and periodically after release.
- Remove or update closed, renamed, or materially changed restaurants.
- Store valid UTF-8 JSON with no comments or trailing commas.
- Keep verification metadata accurate whenever restaurant data changes.
