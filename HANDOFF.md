# Volan Premium Transfers: project handoff (22 Nov 2026)

## The business
- Owner runs two transfer brands in Cyprus:
  - **volanminibus.com**: older main brand for everyday transfers. Hosted on Hostinger and built by the owner. Performs well, including in ChatGPT. **Do not combine it with this site or redirect it.**
  - **volanpremiumtransfers.com** (this repo): VIP brand with luxury minibuses and top-tier drivers. Hosted on **Vercel** (auto-deploys from `main` on GitHub `xaris619/volan-premium-transfers`).
- Phone/WhatsApp +357 99 335570 · email info@volanminibus.com · 24/7 · Larnaca (LCA) and Paphos (PFO) airports, island-wide.
- Fleet (owner confirmed): minibuses for **8, 13, 17, 21 and 30 passengers**. Several vehicles are combined, so **any group size**. **No coaches.**
- Owner decisions: **no prices on the site.** Don't state a maximum group size.

## What was done (all live on the site)
- Full SEO audit. Report: https://claude.ai/artifact/6jT93nj31qun9TGcY1aFmB
- Rebuilt the site as static HTML:
  - Pages: `/`, `/larnaca-airport-transfers/`, `/paphos-airport-transfers/`, `/ayia-napa-protaras-transfers/`, `/limassol-transfers/`, `/private-tours-cyprus/`, `/group-bus-hire-cyprus/`, plus `404.html`
  - Shared files: `assets/css/site.css`, `assets/js/site.js` (mobile menu, WhatsApp quote form, GA4 events `whatsapp_click` / `phone_click` / `email_click` / `generate_lead`), `assets/img/*` (WebP/JPEG)
- Removed hidden font-size-0 multilingual keyword text, which Google treats as spam.
- Replaced the Tailwind CDN script with a local stylesheet. Images went from 2.7 MB to under 110 KB.
- Live mobile Lighthouse: performance 74 → 99, LCP 14.8 s → 1.2 s, SEO 100.
- Structured data:
  - LocalBusiness `@graph` (`#business`)
  - Service, BreadcrumbList and FAQPage on every page
- Search and crawler files:
  - `sitemap.xml` fixed (correct namespace, 7 URLs)
  - `robots.txt` allows AI crawlers
  - `llms.txt` site summary for AI assistants
- `vercel.json`:
  - www → apex 308 redirect, `cleanUrls`, `trailingSlash`
  - 30-day cache on `/assets/`. **CSS/JS links carry `?v=<hash>` so updates load immediately; keep this.**
- Phone fixes from owner feedback:
  - Full hero photo on mobile
  - Aligned ticks
  - Section labels on their own line, with no decorative line before them
- Fleet section showing the real 8/13/17/21/30 sizes. All "1–55", "up to 14" and coach wording removed.

## How pages are built
- `scripts/build.py` generates every HTML page, `404.html` and `sitemap.xml`. Run it with `python3 scripts/build.py .` from the repo root.
- Edit content in `build.py` and re-run it. Editing the HTML directly works too, but the next build run overwrites it.
- Styles are in `assets/css/site.css`. After a CSS/JS change, re-run the build so the `?v=` hash updates.

## Done outside the site
- **Google Search Console:** property `https://volanpremiumtransfers.com/` verified via GA4 (G-36GFT8VNKB). Sitemap submitted. Indexing requested for all 7 pages.
  - Only the homepage was indexed at the time. GSC also still showed an old cached sitemap, but the live sitemap has all 7 URLs.
- **Bing Webmaster Tools:** owner signed in with Google. The GSC import failed once, then the owner reports it done. Check that volanpremiumtransfers.com and its sitemap are listed.

## Open / next steps
1. **Reposition this site as the VIP brand** so it doesn't duplicate volanminibus.com. Waiting on these answers from the owner:
   - Which luxury vehicles (model and passengers)
   - VIP extras (refreshments, Wi-Fi, suit-wearing driver, extra waiting time…)
   - Target customers (business, luxury hotels and villas, weddings, yacht/jet clients…)
   - Whether Volan Minibus has a Google Business Profile
   - Whether the two sites should link to each other

   Then rewrite the copy, titles and schema so the two sites target different searches and contain no duplicate text.
2. Review **volanminibus.com**, to compare it with this site and check it has its own sitemap in GSC and Bing.
3. **Google Business Profile.** Probably one profile for the business. Avoid two profiles for the same company unless they are genuinely separate businesses.
4. **Reviews:** ask customers for Google reviews after every trip.
5. Use real vehicle photos. Current images look AI-generated, and the logo shows a different white van.
6. Later:
   - Translated pages (Russian, Hebrew, German, Polish) with hreflang
   - More route pages (Nicosia, Larnaca→Paphos, Troodos, cruise port)
   - Guide articles
