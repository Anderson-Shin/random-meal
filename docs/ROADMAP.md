# Roadmap

The roadmap is version-based. Update it whenever feature scope or completion changes.

## v0.1.0 Documentation Setup

- [x] Create MASTER.md
- [x] Create PM_RULES.md
- [x] Create ROADMAP.md
- [x] Create DATA_SCHEMA.md
- [x] Create README.md
- [x] Create LICENSE
- [x] Create .gitignore

## v0.2.0 Static MVP

- [x] Create index.html
- [x] Create CSS
- [x] Create JavaScript structure
- [x] Create restaurants.json
- [x] Add 45 restaurant entries
- [x] Add filters
- [x] Add random picker
- [x] Add roulette
- [x] Add multilingual UI

## v0.3.0 SEO Pages

- [x] Create Quarry Bay page
- [x] Create Central page
- [x] Create Kwun Tong page
- [x] Create sitemap.xml
- [x] Create robots.txt
- [x] Add Open Graph metadata
- [x] Add internal links

## v0.3.5 Deployment Preparation

- [x] Create DEPLOYMENT.md
- [x] Create QA_CHECKLIST.md
- [x] Create LAUNCH_CHECKLIST.md
- [x] Create DOMAIN_SETUP.md
- [x] Document Cloudflare Pages settings
- [x] Document placeholder domain replacement process
- [x] Document launch QA process

## v0.4.0 Data Quality

- [x] Add verification fields to restaurant data
- [x] Create DATA_VERIFICATION.md
- [x] Update DATA_SCHEMA.md with verification fields
- [ ] Verify restaurant names
- [ ] Verify current operation status
- [ ] Verify district accuracy
- [ ] Improve descriptions
- [ ] Add more tags
- [ ] Add more districts

## v0.4.1 Codex Workflow

- [x] Create CODEX_INSTRUCTIONS.md
- [x] Link CODEX_INSTRUCTIONS.md from README.md
- [x] Document repository-level Codex workflow rules
- [x] Document short future Codex prompt pattern

## v0.5.0 UX Improvements

- [ ] Improve roulette animation
- [ ] Add favorites with localStorage
- [ ] Add recently picked restaurants
- [ ] Add share result button
- [ ] Add dark mode

## v0.6.0 Monetization Preparation

- [ ] Add ad placeholder review
- [ ] Add privacy policy
- [ ] Add terms page
- [ ] Add contact page
- [ ] Prepare AdSense checklist

## v1.0.0 Public Launch

- [ ] Final mobile check
- [ ] Final SEO check
- [x] Deploy to Cloudflare Pages
- [ ] Connect custom domain
- [ ] Submit sitemap to Google Search Console
- [ ] Apply for Google AdSense

## Known Limitations

- Initial restaurant coverage is limited to Quarry Bay, Central, and Kwun Tong.
- Restaurant data is manually curated and may become outdated between reviews.
- The MVP has no maps, live opening hours, booking, ratings, or user submissions.
- Preferences and results do not sync across devices.
- Multilingual content quality depends on manual writing and review.
- `sitemap.xml`, `robots.txt`, canonical URLs, and Open Graph URLs currently use `https://what-should-i-eat-hk.pages.dev` and must be updated after a custom domain is connected.
- Restaurant entries now include verification metadata, but all entries remain unverified until manually checked.

## Release Checklist

- [ ] Confirm the release matches the approved roadmap scope.
- [ ] Check all supported languages.
- [ ] Test mobile and desktop layouts.
- [ ] Test filters, picker, roulette, and links.
- [ ] Validate HTML and inspect browser console errors.
- [ ] Confirm content accuracy and data-schema compliance.
- [ ] Check page titles, descriptions, canonical URLs, and social metadata.
- [ ] Confirm accessibility basics and keyboard usability.
- [ ] Confirm Cloudflare Pages compatibility.
- [ ] Update this roadmap and the README status.

## Next Actions

1. Manually verify Quarry Bay restaurants.
2. Manually verify Central restaurants.
3. Manually verify Kwun Tong restaurants.
4. Replace or update any uncertain entries.
5. Then prepare legal pages for AdSense readiness.

## Short Codex Prompt Pattern

For future tasks, use a short prompt like:

```markdown
Read docs/CODEX_INSTRUCTIONS.md and docs/ROADMAP.md.

Implement the requested task only.

Follow the project rules strictly.

After finishing:
1. Update docs/ROADMAP.md if task status changes.
2. Update README.md if project status or documentation links change.
3. Summarize files changed.
4. Mention anything requiring manual verification.
```
