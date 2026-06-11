# Deployment Guide

## Deployment Target

Cloudflare Pages

## Project Type

Static HTML, CSS, JavaScript, and JSON site.

## Build Settings

Use these recommended Cloudflare Pages settings:

| Setting | Value |
| --- | --- |
| Framework preset | None |
| Build command | Leave empty |
| Build output directory | `/` |
| Root directory | `/` |
| Node.js version | Not required |

This project has:

- No build process
- No `npm install`
- No backend
- No environment variables required for the MVP

Cloudflare Pages should publish the repository root exactly as committed.

## Deployment Steps

1. Push the latest project changes to GitHub.
2. Open the Cloudflare Dashboard.
3. Go to **Workers & Pages**.
4. Select **Create application**.
5. Select **Pages**.
6. Connect the GitHub account that owns the repository.
7. Select `Anderson-Shin/random-meal`.
8. Configure the build settings shown above.
9. Deploy the project.
10. Open the generated Cloudflare Pages URL.

Do not add a build command, dependency-install step, or environment variable for the MVP.

## After Deployment

Test the generated Cloudflare Pages URL:

- Homepage
- Filters and reset button
- Random picker
- Roulette
- Language switcher
- Quarry Bay, Central, and Kwun Tong pages
- `sitemap.xml`
- `robots.txt`
- Mobile layout

Use [QA_CHECKLIST.md](QA_CHECKLIST.md) for the complete test pass.

## Production Domain Update

Do not change the placeholder before the production domain is finalized.

After connecting a production domain, search the project for:

```text
https://example.com
```

Replace it with:

```text
https://your-domain.com
```

Check these files:

- `sitemap.xml`
- `robots.txt`
- `regions/quarry-bay.html`
- `regions/central.html`
- `regions/kwun-tong.html`

Then re-test the sitemap, robots file, canonical URLs, and Open Graph URLs on the deployed site.
