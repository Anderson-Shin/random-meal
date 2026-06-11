# Manual Candidate Review Worksheet

## Purpose

This worksheet is used to decide whether a local candidate is safe and useful enough to become a restaurant database draft.

It does not verify a restaurant automatically. It does not approve public display automatically.

## Candidate Basic Info

## Candidate: [Candidate Name]

- Candidate ID:
- Candidate area:
- Candidate district:
- Candidate address hint:
- Candidate cuisine hint:
- Discovery source:
- Source URL:
- Source usage:
- Data origin:
- Source confidence:
- Review status:

Allowed review status values:

- `not_reviewed`
- `needs_more_sources`
- `ready_for_database_draft`
- `rejected`

## Safety Checklist

- [ ] No reviews copied
- [ ] No ratings copied
- [ ] No rankings copied
- [ ] No photos copied
- [ ] No menu text copied
- [ ] No promotional copy copied
- [ ] No smiles/frowns stored
- [ ] No raw HTML stored
- [ ] No third-party text reused in public descriptions
- [ ] Candidate is not automatically imported into `restaurants.json`

## Source Strength Checklist

- [ ] Official website checked
- [ ] Official social media checked
- [ ] Mall directory checked
- [ ] Building directory checked
- [ ] Google Business Profile used only for factual cross-check
- [ ] OpenRice listing used only as discovery/reference
- [ ] More than one source reviewed, if possible
- [ ] OpenRice alone is not treated as high confidence

## Restaurant Suitability Checklist

- [ ] Restaurant appears relevant to the target area
- [ ] District appears correct
- [ ] Cuisine category can be normalized
- [ ] Budget category can be estimated without copying platform rating data
- [ ] Meal types are reasonable
- [ ] Situations are reasonable
- [ ] Speed category is reasonable
- [ ] Duplicate restaurant ID checked
- [ ] Existing database duplicates checked

## Public Database Draft Decision

### Decision

Choose one:

- [ ] Reject candidate
- [ ] Keep candidate for more research
- [ ] Draft candidate with `publicDisplay: false`
- [ ] Draft candidate with `publicDisplay: true` only if source support is strong and descriptions are original

## Recommended Metadata by Decision

For weak discovery-source candidates:

```json
{
  "sourceConfidence": "low",
  "dataOrigin": "discovery_source_only",
  "verificationStatus": "unverified",
  "verified": false,
  "lastChecked": null,
  "needsReview": true,
  "publicDisplay": false
}
```

For manually curated first-pass candidates:

```json
{
  "sourceLinks": [],
  "sourceConfidence": "low",
  "dataOrigin": "manual_curation",
  "verificationStatus": "unverified",
  "verified": false,
  "lastChecked": null,
  "needsReview": true,
  "publicDisplay": true
}
```

For source-supported but not fully verified candidates:

```json
{
  "sourceConfidence": "medium",
  "verificationStatus": "needs_update",
  "verified": false,
  "needsReview": true
}
```

- Source confidence does not equal verified.
- `verified: true` requires manual factual verification.
- OpenRice alone must not justify `sourceConfidence: high`.

## Draft Description Rules

- Public descriptions must be original.
- Do not paraphrase reviews.
- Do not summarize user comments.
- Do not copy menu or promotional copy.
- Use neutral factual language.
- Avoid claims like "best," "top-rated," "famous," or "popular" unless independently supported and safe to use.
