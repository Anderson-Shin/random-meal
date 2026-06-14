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

## Local HTML Input Mode

Use local HTML mode when URL fetch mode receives an OpenRice security-check page:

1. Open the OpenRice district listing page in Atlas or another browser.
2. Confirm the real restaurant listing page is visible.
3. View or save the page source.
4. Save the files locally, for example:

```text
tools/openrice_direct/html/central/page1.html
tools/openrice_direct/html/quarry_bay/page1.html
tools/openrice_direct/html/kwun_tong/page1.html
```

5. Parse one district at a time:

```bash
python tools/openrice_direct/scripts/discover.py \
  --district central \
  --html-dir tools/openrice_direct/html/central \
  --max-items 50
```

Parse one saved file:

```bash
python tools/openrice_direct/scripts/discover.py \
  --district central \
  --html-file tools/openrice_direct/html/central/page1.html \
  --max-items 50
```

Run all three local district folders separately:

```bash
python tools/openrice_direct/scripts/discover.py --district central --html-dir tools/openrice_direct/html/central --max-items 50
python tools/openrice_direct/scripts/discover.py --district quarry_bay --html-dir tools/openrice_direct/html/quarry_bay --max-items 50
python tools/openrice_direct/scripts/discover.py --district kwun_tong --html-dir tools/openrice_direct/html/kwun_tong --max-items 50
```

Local HTML mode makes no network requests. Saved HTML under `tools/openrice_direct/html/` is ignored by git and must not be committed. This mode only writes local raw candidate JSON and does not update `restaurants.json` directly.

Inspect generated raw JSON, then continue with the downstream workflow:

```bash
python tools/openrice_apify/scripts/normalize_openrice.py
python tools/openrice_apify/scripts/transform_candidates.py
python tools/openrice_apify/scripts/merge_candidates.py \
  --input tools/openrice_apify/processed/openrice_transformed_candidates.json \
  --refresh-existing
```

The merge command is a dry run unless `--write` is explicitly provided. Inspect the dry-run summary before any write.

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
