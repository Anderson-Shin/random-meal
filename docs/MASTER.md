# What Should I Eat HK? - Master Brief

## Product Mission

What Should I Eat HK? helps people in Hong Kong decide what to eat quickly. It combines curated restaurant data, simple filters, a random picker, a roulette-style decision tool, multilingual content, and SEO-friendly district pages.

The product should reduce decision fatigue without requiring users to create accounts, install an app, or study long restaurant reviews.

## Target Users

- Hong Kong office workers choosing lunch or dinner
- Residents looking for a quick nearby recommendation
- Visitors who need clear, multilingual restaurant guidance
- Groups that want a simple way to settle on a restaurant

## MVP Scope

- A static, mobile-friendly website
- Manually curated restaurant data
- Filters for area, cuisine, budget, meal type, situation, and speed
- Random restaurant picker
- Roulette-style decision tool
- English, Traditional Chinese, and Simplified Chinese UI
- SEO-friendly pages for the initial districts

## Non-MVP Features

- User accounts, login, and cloud-synced preferences
- User reviews, ratings, comments, or restaurant submissions
- Backend services or databases
- Paid APIs, AI recommendations, or personalized ranking
- Google Maps integration
- Restaurant booking, ordering, or delivery integrations
- Native mobile applications

These features must not be implemented early. They require separate product validation and roadmap approval.

## Tech Stack

- HTML
- CSS
- Vanilla JavaScript
- JSON
- Static hosting on Cloudflare Pages

The project does not use React, Node.js, npm, build tools, a backend, or runtime API dependencies in the MVP.

## Initial Districts

- Quarry Bay
- Central
- Kwun Tong

District coverage should grow only after the initial data is useful, accurate, and maintainable.

## Language Support

- English (`en`)
- Traditional Chinese (`zh-Hant`)
- Simplified Chinese (`zh-Hans`)

Navigation and core decision flows must remain usable in all supported languages. Restaurant descriptions and recommendations should be manually written or reviewed for each language.

## Restaurant Data Policy

Restaurant data must be manually curated from public factual information. Every entry should be useful for making a quick dining decision and must follow the schema in [DATA_SCHEMA.md](DATA_SCHEMA.md).

Do not scrape websites or copy reviews, ratings, photos, or menu text. Descriptions and recommendations must be original, concise, and factual. Entries should be reviewed periodically for accuracy.

## SEO Principles

- Give each district page a clear purpose and unique, useful copy.
- Use semantic HTML and descriptive headings.
- Provide accurate page titles, descriptions, canonical URLs, and Open Graph metadata.
- Keep pages fast, mobile-friendly, and crawlable without JavaScript.
- Use clear internal links between the homepage and district pages.
- Avoid thin, duplicated, or automatically generated content.

SEO usefulness takes priority over decorative animation.

## Monetization Direction

Monetization may begin after the product has useful content, stable traffic, and required policy pages. The first direction is lightweight advertising, such as Google AdSense, with placements that do not obstruct the decision flow.

Future monetization experiments may include clearly labeled sponsored placements or affiliate partnerships. Paid influence must never be presented as an organic recommendation.

## Long-Term Vision

Build the simplest trusted answer to "What should I eat?" across Hong Kong. Over time, the project can expand district coverage, improve data quality, and add small local-first conveniences while remaining fast, transparent, inexpensive, and easy for beginners to maintain.
