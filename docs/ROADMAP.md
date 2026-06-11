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

## v0.4.2 Verification Workspace

- [x] Create Quarry Bay verification worksheet
- [ ] Complete Quarry Bay manual verification
- [ ] Apply Quarry Bay verification results to restaurants.json

## v0.4.3 Data Source Strategy

- [x] Create DATA_SOURCE_STRATEGY.md
- [x] Update CODEX_INSTRUCTIONS.md with data source strategy rules
- [x] Pause branch-level manual verification until data source strategy is finalized
- [x] Decide whether unofficial OpenRice API repositories should be avoided or tested locally only
- [x] Classify cal65/Open-Rice as an unofficial scraper, not a production API
- [x] Document field-level treatment for OpenRice scraper output
- [x] Design proposed restaurant source metadata fields
- [x] Decide whether to add proposed source metadata fields to restaurants.json
- [ ] Create local-only data discovery prototype, if approved

## v0.4.4 Source Metadata Activation and Local Discovery Workflow

- [x] Promote source metadata fields to active schema
- [x] Add default source metadata to existing restaurant entries
- [x] Create LOCAL_DISCOVERY_WORKFLOW.md
- [x] Document local-only discovery workflow
- [x] Confirm OpenRice scraper remains production-disallowed
- [ ] Create local-only candidate template
- [ ] Create manual candidate review worksheet
- [ ] Decide whether to test cal65/Open-Rice locally

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

1. Review activated source metadata fields.
2. Create a local-only candidate template and manual review worksheet.
3. Decide whether to test cal65/Open-Rice locally.
4. Do not run scraping or expand the public database until the candidate workflow is finalized.

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
