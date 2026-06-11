# Launch Checklist

## Pre-Deployment

- [ ] Confirm repository is public if required
- [ ] Confirm no API keys are committed
- [ ] Confirm no `.env` files are committed
- [ ] Confirm no real AdSense code is inserted yet
- [ ] Confirm no third-party copyrighted content is copied
- [ ] Confirm restaurant data is first-pass curated only
- [ ] Verify all restaurant entries
- [ ] Confirm no entry has `verificationStatus = remove_candidate`
- [ ] Resolve or replace `needs_update` entries
- [ ] Confirm all `publicDisplay` entries are suitable for public launch

## Cloudflare Pages

- [ ] Connect GitHub repository
- [ ] Set framework preset to None
- [ ] Leave build command empty
- [ ] Set output directory to `/`
- [ ] Deploy
- [ ] Open generated Pages URL

## Post-Deployment QA

- [ ] Run [QA_CHECKLIST.md](QA_CHECKLIST.md) on the Cloudflare Pages URL
- [ ] Test homepage
- [ ] Test filters
- [ ] Test random picker
- [ ] Test roulette
- [ ] Test language switcher
- [ ] Test district pages
- [ ] Test sitemap
- [ ] Test robots.txt

## Domain Setup

- [ ] Choose production domain
- [ ] Connect custom domain to Cloudflare Pages
- [ ] Replace `https://what-should-i-eat-hk.pages.dev`
- [ ] Re-test sitemap
- [ ] Re-test robots.txt
- [ ] Re-test canonical URLs
- [ ] Re-test Open Graph URLs

## Search Console

- [ ] Add domain to Google Search Console
- [ ] Submit sitemap
- [ ] Request indexing for homepage
- [ ] Request indexing for district pages

## AdSense Preparation

Do not apply too early. Before applying:

- [ ] Add privacy policy page
- [ ] Add terms page
- [ ] Add contact page
- [ ] Improve restaurant content quality
- [ ] Verify all restaurant data
- [ ] Add more useful written content
- [ ] Remove or replace weak placeholder text

## Public Launch

- [ ] Final mobile check
- [ ] Final content check
- [ ] Final SEO check
- [ ] Share with small test users
- [ ] Collect feedback
- [ ] Decide v0.4.0 priorities
