# Product Management Rules

These rules govern every product and engineering decision in What Should I Eat HK?.

## Decision Priorities

1. **Simple > Fancy**  
   Prefer the smallest experience that clearly helps users decide.
2. **Working > Perfect**  
   Ship a reliable useful version, then improve it with evidence.
3. **Maintainable > Clever**  
   Choose code and content that a beginner can understand and edit.
4. **SEO > Animation**  
   Never trade crawlability, speed, or useful content for visual effects.
5. **Static > Dynamic**  
   Use static files and browser-native capabilities unless a dynamic system is proven necessary.

## Strict Rules

- Use HTML, CSS, Vanilla JavaScript, and JSON.
- Keep the project compatible with Cloudflare Pages at all times.
- Add no unnecessary dependencies.
- Do not use React, Node.js, npm, build tools, or a backend in the MVP.
- Never put API keys, secrets, or private credentials in frontend code or committed files.
- Do not use paid APIs, AI, Google Maps, login, or user accounts in the MVP.
- Do not implement future features early. Complete and validate the current roadmap version first.
- Update `docs/ROADMAP.md` whenever feature scope or completion status changes.
- Keep core content available to search engines without requiring JavaScript.
- Preserve multilingual usability when changing user-facing content or flows.
- Follow `docs/DATA_SCHEMA.md` for all restaurant data.
- Prefer original, manually curated content over copied or automated content.

## Change Check

Before accepting a feature or dependency, confirm:

- Does it directly improve a current roadmap goal?
- Can a beginner maintain it?
- Does it preserve static hosting and Cloudflare Pages compatibility?
- Does it keep the site fast, accessible, multilingual, and SEO-friendly?
- Is the added complexity justified by clear user value?

If any answer is no, simplify, defer, or reject the change.
