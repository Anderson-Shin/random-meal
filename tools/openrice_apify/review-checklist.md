# OpenRice Candidate Review Checklist

Use this checklist to manually review a hidden OpenRice Apify candidate before deciding whether it may be displayed publicly. Completing the checklist does not automatically publish or verify a candidate.

## Candidate

- Candidate ID:
- Restaurant name:
- Reviewer:
- Review date:

## Factual Review

- [ ] Restaurant still exists.
- [ ] Restaurant is currently operating.
- [ ] District and area are correct.
- [ ] Address is correct.
- [ ] Cuisine label is appropriate.
- [ ] Budget category is reasonable.
- [ ] `ratingOverall` was treated only as a review hint and was not blindly trusted.
- [ ] `openingHours` were manually checked before any public use.
- [ ] `popularDishes` were manually checked before any public use.

## Content Safety

- [ ] Public descriptions are original.
- [ ] No reviews were copied.
- [ ] No ratings or rankings were copied into public-facing content.
- [ ] No photos or photo URLs were copied.
- [ ] No menu text was copied.
- [ ] No promotional copy was copied.
- [ ] No smiles or frowns were copied.

## Public Display Decision

- [ ] Keep hidden with `publicDisplay: false`.
- [ ] Candidate is suitable to change manually to `publicDisplay: true`.

Do not change `publicDisplay` automatically. Only make a candidate public after completing a manual factual and content-safety review.

## Verification Metadata

After review, manually update the appropriate fields:

- [ ] `verificationStatus`
- [ ] `verified`
- [ ] `lastChecked`
- [ ] `needsReview`
- [ ] `reviewNotes`

Reviewer notes:

Source and cross-check notes:

## Apply A Reviewed Decision

After completing this checklist, generate and fill out:

```text
tools/openrice_apify/processed/openrice_review_template.json
```

Then dry-run `apply_review_updates.py` before explicitly using `--write`. The checklist itself does not publish anything, and incomplete or non-approved review records remain hidden.
