# OpenRice Direct Discovery

## Purpose

This local-only tool discovers minimal restaurant candidate hints from public OpenRice district listing pages. It is the active data acquisition path while Apify actor execution is paused/fallback.

The tool writes snake_case raw JSON compatible with the shared pipeline under `tools/openrice_apify/`. It does not update `assets/data/restaurants.json`, approve candidates, or make candidates public.

## Initial Districts

- Central (`districtId: 1003`)
- Quarry Bay (`districtId: 1014`)
- Kwun Tong (`districtId: 2026`)

District definitions live in `config/districts.json`. Add or remove a config entry to change the available district keys.

## Safety Limits

- Local candidate discovery only
- Public listing pages only
- No browser automation, login, proxy rotation, or captcha bypass
- Stop without writing output if OpenRice returns a security-check page
- No review bodies, photos, user comments, or raw HTML storage
- Conservative same-site pagination only
- No direct database updates

## Usage

From the repository root:

```bash
python tools/openrice_direct/scripts/discover.py \
  --district central \
  --max-items 50
```

Discover all configured districts:

```bash
python tools/openrice_direct/scripts/discover.py \
  --district all \
  --max-items 50
```

Adjust conservative request limits:

```bash
python tools/openrice_direct/scripts/discover.py \
  --district kwun_tong \
  --max-items 40 \
  --pages 2 \
  --delay-seconds 5
```

Use `--dry-run` to fetch and parse without writing raw JSON.

Generated raw files are written to `tools/openrice_apify/raw/` with names such as:

```text
openrice_direct_central_YYYY-MM-DD.json
```

Do not commit generated raw JSON.

## Output

The parser intentionally keeps minimal factual candidate hints:

- Restaurant ID and name
- Configured district label
- Restaurant source URL
- Empty or null placeholders for fields unavailable on the listing page

The parser returns a nonzero exit code and does not write an empty file when no candidates are found.

## Downstream Pipeline

After inspecting raw discovery output:

```bash
python tools/openrice_apify/scripts/normalize_openrice.py
python tools/openrice_apify/scripts/transform_candidates.py

python tools/openrice_apify/scripts/merge_candidates.py \
  --input tools/openrice_apify/processed/openrice_transformed_candidates.json \
  --refresh-existing
```

Inspect the merge dry run first. Use `--write` only after confirming that new and refreshed entries remain hidden and safe.
