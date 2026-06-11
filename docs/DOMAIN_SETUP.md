# Domain Setup Guide

## Current Production Domain

The project currently uses the Cloudflare Pages domain:

```text
https://what-should-i-eat-hk.pages.dev
```

This appears in:

- `sitemap.xml`
- `robots.txt`
- District page canonical URLs
- District page Open Graph URLs

This domain is valid for production use until a custom domain is connected.

## After Domain Is Chosen

Search the project for:

```text
https://what-should-i-eat-hk.pages.dev
```

Replace every occurrence with the real domain.

Example:

```text
https://whatshouldieathk.com
```

## Files to Check

- `sitemap.xml`
- `robots.txt`
- `regions/quarry-bay.html`
- `regions/central.html`
- `regions/kwun-tong.html`

After replacement, confirm that all URLs use HTTPS, contain the intended hostname, and load successfully.

## Important Rule

If submitting the Pages domain to Google Search Console, use its current sitemap. After connecting a custom domain, replace every Pages-domain URL and submit the custom-domain sitemap instead.
