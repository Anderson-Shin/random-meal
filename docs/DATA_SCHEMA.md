# Restaurant Data Schema

The future restaurant dataset will live at:

```text
assets/data/restaurants.json
```

The file will contain a JSON array of restaurant objects. Do not create the dataset until the relevant roadmap task begins.

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
  "sourceNote": "Manually curated. No reviews, ratings, photos, or menu text copied."
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

## Data Rules

- Do not scrape restaurant websites, platforms, or directories.
- Do not copy reviews.
- Do not copy ratings.
- Do not copy photos.
- Do not copy menu text.
- Use manually written descriptions and recommendations.
- Use public factual information only.
- Keep category labels and capitalization consistent.
- Keep descriptions concise, useful, and free from unverifiable claims.
- Review entries for accuracy before release and periodically after release.
- Remove or update closed, renamed, or materially changed restaurants.
- Store valid UTF-8 JSON with no comments or trailing commas.
