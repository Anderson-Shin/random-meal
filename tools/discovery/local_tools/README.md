# Local Discovery Tools

## Purpose

This folder contains local-only helper scripts for normalizing fake or local candidate input.

These scripts are not production code or frontend code. They must not connect to Cloudflare Pages or automatically update `assets/data/restaurants.json`.

## Current Tool

```bash
python tools/discovery/local_tools/normalize_candidates.py \
  --input tools/discovery/raw-candidates.example.json \
  --output tools/discovery/local-candidates.example.json
```

- The tool reads local JSON only.
- The tool makes no network requests.
- The tool does not fetch OpenRice URLs.
- The tool does not scrape.
- The tool discards unsafe fields.
- The output still requires manual review.

## Not Allowed

- URL fetching
- OpenRice scraping
- Google scraping
- Automatic import into `restaurants.json`
- Frontend integration
- Cloudflare integration
- Storing reviews, ratings, rankings, photos, menu text, promotional copy, smiles, frowns, or raw HTML
