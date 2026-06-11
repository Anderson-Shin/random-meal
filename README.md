# What Should I Eat HK?

A multilingual, static-first Hong Kong restaurant decision website that helps people quickly choose where to eat.

## Current Status

**v0.4.8 - File-only local candidate normalizer added**

The working static MVP includes filters, decision tools, multilingual core UI, Cloudflare Pages deployment, and 45 first-pass manually curated restaurant entries across Quarry Bay, Central, and Kwun Tong.

## Tech Stack

- HTML
- CSS
- Vanilla JavaScript
- JSON
- Cloudflare Pages

## Documentation

- [Master product and engineering brief](docs/MASTER.md)
- [Product management rules](docs/PM_RULES.md)
- [Version roadmap](docs/ROADMAP.md)
- [Restaurant data schema](docs/DATA_SCHEMA.md)
- [Restaurant data source strategy](docs/DATA_SOURCE_STRATEGY.md)
- [Local discovery workflow](docs/LOCAL_DISCOVERY_WORKFLOW.md)
- [Local discovery prototype plan](docs/LOCAL_DISCOVERY_PROTOTYPE_PLAN.md)
- [Local discovery folder guide](tools/discovery/README.md)
- [Local discovery tools](tools/discovery/local_tools/README.md)
- [Manual candidate review worksheet](tools/discovery/manual-review-worksheet.md)
- [Codex repository instructions](docs/CODEX_INSTRUCTIONS.md)

## Development Philosophy

The project stays static-first, beginner-editable, SEO-friendly, low-cost, and maintainable. Simple, working solutions take priority over fancy or premature features. The MVP uses no framework, build tool, backend, paid API, AI, Google Maps, login, or user accounts.

## Future MVP Direction

The next milestone is reviewing the normalized fake candidate output and deciding whether to allow real local candidate input. Direct OpenRice URL fetching is still not approved.

See [docs/ROADMAP.md](docs/ROADMAP.md) for the full version plan.

## SEO Pages

The project currently includes district SEO pages for:

- Quarry Bay
- Central
- Kwun Tong

The site is deployed at [what-should-i-eat-hk.pages.dev](https://what-should-i-eat-hk.pages.dev). Sitemap, robots, canonical, and Open Graph URLs currently use this Pages domain. Replace it after connecting a custom domain.

## Deployment

This project is designed for Cloudflare Pages as a static site.

- Framework preset: None
- Build command: empty
- Build output directory: `/`
- Environment variables: none required for MVP

See:

- [Deployment Guide](docs/DEPLOYMENT.md)
- [QA Checklist](docs/QA_CHECKLIST.md)
- [Launch Checklist](docs/LAUNCH_CHECKLIST.md)
- [Domain Setup Guide](docs/DOMAIN_SETUP.md)

## Data Verification

Restaurant data is manually curated and now includes verification fields. Entries remain first-pass until manually verified.

All restaurant entries now include source metadata fields for tracking data origin and source confidence.

Local candidate templates are available for private discovery work, but candidates are not automatically imported into the public restaurant database.

Before expanding the database, review the data source strategy to avoid copying third-party reviews, ratings, photos, menu text, or other protected content.

The reviewed `cal65/Open-Rice` repository is treated as an unofficial scraper and is not approved for production or frontend integration.

See:

- [Data Verification Guide](docs/DATA_VERIFICATION.md)

## Codex Workflow

Codex should read [Codex repository instructions](docs/CODEX_INSTRUCTIONS.md) before starting new tasks. This keeps future prompts shorter and helps preserve project rules, roadmap discipline, data verification rules, and Cloudflare Pages compatibility.
