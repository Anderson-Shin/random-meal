# QA Checklist

Run this checklist locally and again on the deployed Cloudflare Pages URL.

## Homepage

- [ ] Homepage loads without console errors
- [ ] CSS loads correctly
- [ ] Restaurant data loads
- [ ] Result count appears
- [ ] Ad placeholders appear
- [ ] Footer appears

## Filters

- [ ] District filter works
- [ ] Meal filter works
- [ ] Cuisine filter works
- [ ] Budget filter works
- [ ] Situation filter works
- [ ] Speed filter works
- [ ] Reset button works
- [ ] Empty state appears when no result matches

## Restaurant Cards

- [ ] Restaurant cards show name
- [ ] Restaurant cards show district
- [ ] Restaurant cards show cuisine
- [ ] Restaurant cards show budget
- [ ] Restaurant cards show tags
- [ ] Restaurant cards show description
- [ ] Restaurant cards show recommended-for text

## Random Picker

- [ ] Pick For Me works with all restaurants
- [ ] Pick For Me respects filters
- [ ] Empty state works if no candidates exist

## Roulette

- [ ] Spin Roulette works with all restaurants
- [ ] Spin Roulette respects filters
- [ ] Button disables while spinning
- [ ] Result appears after spin
- [ ] Empty state works if no candidates exist

## Language Switcher

- [ ] English works
- [ ] Traditional Chinese works
- [ ] Simplified Chinese works
- [ ] Filter labels update
- [ ] Button labels update
- [ ] Restaurant descriptions update
- [ ] Recommended-for text updates

## District Pages

- [ ] Quarry Bay page loads
- [ ] Central page loads
- [ ] Kwun Tong page loads
- [ ] District pages use the correct CSS path
- [ ] District pages link back to the homepage
- [ ] District pages link to the other district pages
- [ ] CTA links go to homepage filters

## SEO

- [ ] Homepage title exists
- [ ] Homepage meta description exists
- [ ] District page titles exist
- [ ] District page meta descriptions exist
- [ ] Open Graph tags exist
- [ ] Canonical links exist
- [ ] `sitemap.xml` loads
- [ ] `robots.txt` loads
- [ ] Placeholder domain is documented

## Responsive Design

- [ ] Mobile layout works
- [ ] Tablet layout works
- [ ] Desktop layout works
- [ ] Buttons are easy to tap
- [ ] Cards do not overflow
- [ ] Filters remain usable on small screens

## Accessibility Basics

- [ ] Form labels exist
- [ ] Buttons are keyboard accessible
- [ ] Links are descriptive
- [ ] Text contrast is readable
- [ ] No critical content depends only on color

## Data Quality

- [ ] 45 restaurant entries exist
- [ ] Each entry has required schema fields
- [ ] No copied reviews
- [ ] No ratings
- [ ] No menu text
- [ ] No photos
- [ ] Restaurant operation status still requires manual verification
- [ ] Each restaurant has `verificationStatus`
- [ ] Each restaurant has `verified`
- [ ] Each restaurant has `lastChecked`
- [ ] Each restaurant has `needsReview`
- [ ] Each restaurant has `publicDisplay`
- [ ] Each restaurant has `reviewNotes`
- [ ] No restaurant is marked `remove_candidate` before launch
- [ ] Any `needs_update` entries are reviewed before launch
