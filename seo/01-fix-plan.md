# Fix Plan — raising the score from 55

**Last updated:** 2026-08-11
**Baseline:** 55/100 (audit 2026-08-11) · **Projected on completion:** ~78/100 · **Ceiling:** ~82–84 (see accepted risks in [`README.md`](README.md))

Ordered by **dependency, not severity**. Items early in the list unblock later ones. Doing them out
of order wastes effort.

**The through-line:** you cannot rank pages Google has not indexed, and you cannot earn links to
pages that do not resolve. Stages 1 and 2 exist to make Stages 3–5 worth doing at all.

Legend: 🔴 blocking · 🟠 high · 🟡 medium · ⚪ low · ✅ done · 🙋 needs you (I can't do it)

---

## Where the 23 points come from

| Category | Now | Target | Weight | Gain | Driven by |
|---|---|---|---|---|---|
| Technical SEO | 50 | 85 | 22% | **+7.7** | Stage 1 + 2 |
| On-Page SEO | 62 | 85 | 20% | **+4.6** | Stage 3 |
| Schema | 58 | 90 | 10% | **+3.2** | Stage 4 |
| Images | 45 | 85 | 5% | **+2.0** | Stage 5 |
| Performance | 60 | 80 | 10% | **+2.0** | Stage 5 |
| AI Search Readiness | 48 | 68 | 10% | **+2.0** | Stage 4 (capped by authority) |
| Content Quality | 54 | 62 | 23% | **+1.8** | Stage 6 (capped by declined trust items) |
| | | | | **≈ +23** | **55 → 78** |

Content Quality is the heaviest category at 23% and gains the least. That is the direct, measurable
price of declining testimonials and legal-entity publication. It is a deliberate trade, not an oversight.

---

## Stage 1 — Get the money pages into Google

*Seven of 14 pages have **never been crawled**: `page_fetch_state: UNSPECIFIED`, no `last_crawl_time`,
zero referring URLs. That includes every commercial service page, `/about/`, and all three policy
pages. Nothing else in this plan matters until this moves.*

Critically: **the two service pages that Google has never seen are the only two pages carrying your
confirmation screenshots** (`img/canada-proof-1..5.jpg`, `img/toronto-proof-1..3.png`, used in
`services/us-visa-appointment-canada/index.html` and `services/us-visa-appointment-toronto/index.html`).
Your single strongest existing trust asset is invisible to search. That alone justifies Stage 1's priority.

### ✅ 1.1 🔴🙋 Resubmit the sitemap in GSC
Google's copy was last processed **2026-06-23** with **10 URLs**; the live file has 14. Zero errors —
it simply has not been re-fetched in ~7 weeks.

- GSC → Sitemaps → enter `sitemap.xml` → Submit.
- **Verify:** GSC Sitemaps reports `submitted: 14` and `last_submitted` after 2026-08-11.
- **If still 10 after 14 days:** check for a stale edge-cached `sitemap.xml` on Vercel.

### ✅ 1.2 🔴🙋 Request indexing for the 7 unknown URLs
GSC → URL Inspection → each → Request Indexing:

```
/services/
/services/us-visa-appointment-canada/
/services/us-visa-appointment-toronto/
/about/
/terms/
/privacy/
/refund-policy/
```

- **Verify:** re-inspect in 14 days; state should move off "URL is unknown to Google."
- **Do NOT use the Indexing API** — it officially supports only `JobPosting` and `BroadcastEvent`.
- **Escalation if still unknown after 14 days:** the cause is not crawl scheduling. Check for a
  Vercel edge rule serving different content to Googlebot, then compare
  `curl -A "Googlebot" https://www.easyvisabooking.com/services/` against a normal fetch.

### ✅ 1.3 🟠 Fix `lastmod`, drop `priority` and `changefreq` — `sitemap.xml`
Every one of the 14 URLs claims the identical `2026-08-07`. Uniform templated `lastmod` is a known
trigger for Google discounting the field entirely. `priority` and `changefreq` are ignored outright.

Emit true per-page dates, or omit `lastmod` — **omitting beats faking**.

### ✅ 1.4 🟠 Remove the three `Disallow` lines — `robots.txt`
```
Disallow: /services/us-visa-appointment-dubai/
Disallow: /services/us-visa-appointment-uae/
Disallow: /services/us-visa-appointment-australia/
```
`Disallow` is the wrong instrument for removing pages. A blocked URL cannot be crawled, so Google can
never observe the 404 and can never cleanly drop it — the block *preserves* the dead URL instead of
retiring it. Removing the lines is a prerequisite for 1.5.

### ✅ 1.5 🟠 Serve **410 Gone** on the three dead location URLs — `vercel.json`
**Decision (2026-08-11): kill all three.** Dubai, UAE, and Australia will not be built.

- Add explicit 410 responses so Google retires them permanently rather than re-queueing 404s.
- Correction to the audit: the links to these pages are **already commented out** in the HTML on
  every page, so they are not live crawlable links. The audit's "`/services/` links to 3 pages that
  are 404" is stale. What *is* still real: the 404s, the robots block, and 1.6.

### ✅ 1.6 🟠 Stop advertising the three dead locations — `services/index.html`
Three tags still name locations that will not exist:
- L19–20 `meta name="description"` — *"We help applicants in Canada, Dubai, UAE, Australia and more…"*
- L21–22 `meta name="keywords"` — Dubai/UAE/Australia terms
- L24–25 `og:description` — *"Canada, Dubai, UAE, Australia and more."*

Rewrite to match reality. Also delete the malformed commented-out footer link block at
`services/index.html:248-253` — it contains a nested `<!-- <!--` and a stray trailing `-->`.
Same dead block exists in 8 other files; remove it everywhere while in there.

### ✅ 1.7 🟠 Fix the favicon case bug — 8 files
Git tracks the file as **`img/brand-logo-real.PNG`** (uppercase). Verified live:
`img/brand-logo-real.PNG` → **200**, `img/brand-logo-real.png` → **404**. Vercel is case-sensitive;
your local Windows checkout is not (`core.ignorecase=true`), which is why this is invisible in dev.

Eight files reference the lowercase path and 404 their favicon:

| File | Line |
|---|---|
| `404.html` | 22 |
| `terms/index.html` | 50 |
| `about/index.html` | 82 |
| `privacy/index.html` | 50 |
| `refund-policy/index.html` | 50 |
| `contact/index.html` | 34 |
| `how-it-works/index.html` | 30 |

Also: **no `/favicon.ico` exists** (404) — browsers and crawlers request it by default. Add one.

**Leading indicator for Stage 1:** GSC "Pages" indexed count climbs from 7 toward 14. Watch weekly.
No re-audit needed.

---

## Stage 2 — Security and infrastructure

### ✅ 2.1 🟠 Add security headers — `vercel.json`
Verified live: the **only** header present sitewide is `Strict-Transport-Security: max-age=63072000`
(missing `includeSubDomains` and `preload`). Absent: CSP, `X-Content-Type-Options`, `X-Frame-Options`,
`Referrer-Policy`, `Permissions-Policy`.

**These are not ranking factors and should never be sold as such.** They matter because this site
handles passport details and payment intent in a scam-adjacent category, and because Stripe's
underwriting review will look at the site.

Add the four cheap ones now. **Add CSP only after auditing `gtag.js` and `analytics.ahrefs.com` —
and then confirm analytics still fires.** That verification step is the one people skip and regret.

### 2.2 🟡 Collapse the `/for-agents/` redirect chain — `vercel.json`
`/for-agents` → 308 → `/for-agents/` → 308 → `/services/`. Two hops; should be one.

Note: this page still draws impressions at **average position 11.2** — the best on the site — from
stale pre-redirect index data. Per the constraints in `README.md`, the audience is **not** being
reinstated. Collapse the chain and let the impressions decay.

**❌ Closed as not-fixable (2026-08-12).** `vercel.json` already declares
`/for-agents` → `/services/` directly, and the chain persists anyway. Verified live: Vercel applies
`trailingSlash: true` normalization **before** config `redirects`, so the platform emits the first
308 and our rule never sees the un-slashed path. The only way to collapse it is to drop
`trailingSlash`, which would restructure every canonical URL on the site — vastly disproportionate.
The same 2-hop pattern applies to `/office`, `/testimonial` and every other un-slashed `source` in
the file; those rules are dead code but harmless, and would become live if `trailingSlash` ever
changed. Impact accepted: Google follows chains up to 5 hops, and the target is a page whose
impressions we *want* to decay.

---

## Stage 3 — On-page

### ✅ partial 3.1 🟠 Fix the broken `og:image` — `index.html:29`
Points to `https://www.easyvisabooking.com/img/visa-banner.jpg` — verified **404**. No other page on
the site has an `og:image` at all.

You promote through WhatsApp and Telegram. Every link shared in those channels currently renders as a
bare grey box. This is a direct acquisition surface, not a vanity item.

- ~~Create a real 1200×630 OG image.~~ **Still open.** Every page currently points at
  `img/carousel-1.jpg` (1920×1080 — 16:9, not the 1.91:1 OG ratio; 120 KB generic stock). It renders, which is the
  whole point of closing the 404, but it is a placeholder: no logo, no proposition, identical on all
  14 pages. A purpose-built 1200×630 card — and per-page variants for the two service pages and the
  blog — is a Stage 5 follow-up.
- ✅ `og:image`, `og:image:width`, `og:image:height`, `og:type`, `og:site_name` now present sitewide.

### ✅ 3.2 🟠 Add `twitter:card` sitewide — all pages
Absent everywhere. `summary_large_image` + `twitter:title` + `twitter:description` + `twitter:image`.
WhatsApp and Telegram both fall back to Twitter Card tags when OG is incomplete.

### ✅ 3.3 🟡 Trim over-length meta descriptions
Render limit is ~155 chars. Over-length entries lose their differentiating clause to truncation —
"Pay only on success" is exactly the phrase getting cut.

| Page | Now | Action |
|---|---|---|
| `services/us-visa-appointment-toronto/` | 216 | Trim to ≤155, keep "pay only on success" |
| `blog/us-visa-appointment-dubai-fast-2026/` | 231 | Trim to ≤155 |
| Others 162–170 | 162–170 | Trim to ≤155 |

### ✅ 3.4 🟡 Trim over-length titles
Toronto (72 chars), `/` (65), Canada service (65). Target ≤60.

### ✅ 3.5 🟡 Link `/blog/` from header nav and footer
`/blog/` appears in **no** navigation anywhere on the site. It is indexed regardless — which is why
the audit correctly rejects "add internal links" as the fix for the indexation problem — but it
receives no internal link equity, and it is about to become the site's primary growth engine
(8+ posts/month). Add it to the main nav and footer before Stage 6 volume starts landing.

### 3.6 🟡 Deepen `/services/` — currently 495 words
Verified: 495 words, thinner than both of its own children (Canada 2,795w, Toronto 3,573w). A hub
smaller than its spokes cannot carry hub duty. Rebuild as part of Stage 6.

---

## Stage 4 — Schema and entity clarity

Seven ready-to-paste JSON-LD files already exist in
[`../easyvisabooking.com-audit/findings/schema-generated/`](../easyvisabooking.com-audit/findings/schema-generated/).
This stage is mostly application, not authoring.

### ✅ 4.1 🔴 Placeholder text live in production — `index.html:50`
`Organization.sameAs` contains the literal unfilled placeholder:
```
"https://t.me/YourTelegramChannel"
```
Your real channel — already live in the footer — is `https://t.me/earlyusvisabooking`.
**Two-minute fix. Highest embarrassment-to-effort ratio on the site.**

### 4.2 🔴 `/contact/` ships zero JSON-LD
The page most needing a machine-readable `ContactPoint` has none, despite email, WhatsApp, and
Telegram all being live on it. Use `05-contact-page.jsonld`.

### 4.3 🔴 `image` missing from all 3 `BlogPosting` blocks
Google's most consistently required `Article` property for rich-result eligibility. Use
`02-blogposting-template.jsonld`.

### 4.4 🟠 Consolidate the Organization entity with `@id`
`Organization` is currently declared as **7+ disconnected anonymous islands** — twice on the homepage
alone (top-level, and nested in `Service.provider`), plus stub copies on `/about/`, both service
pages, and all three blog posts. None carry `@id`, so nothing links.

Adopt one canonical `@id` (`https://www.easyvisabooking.com/#organization`) and reference it
everywhere else. Entity clarity is the single dimension this site scores worst on (18/100) and the
one AI answer engines depend on most. Use `01-homepage-organization-website-service-graph.jsonld`.

### ✅ partial 4.5 🟠 Reconcile the contradictory country lists
**Up to six mutually inconsistent lists** of which countries you serve exist across: `Organization`
description, `Organization.areaServed`, `Service.areaServed`, `/about/` schema, visible FAQ text, and
a homepage subheading. Pick one authoritative list. See `02-growth-plan.md` § Geographic scope for
the decision.

### 4.6 🟠 Make homepage schema describe the visible page — `index.html`
The homepage `FAQPage` JSON-LD and the visible FAQ accordion contain **entirely different questions
and answers**. Worse, the only stated price (**$100 starting fee**) exists *solely inside JSON-LD and
never in visible text* — that is a structured-data policy violation, not just an inconsistency.

Two options, both acceptable:
- Put the price in visible copy (recommended — "no upfront fee / pay only on success" is a genuine
  competitive advantage currently hidden), **or**
- Remove `offers` from schema.

Do not leave it as-is.

### 4.7 🟡 Add `BreadcrumbList` (absent on 6 pages) and `Service.offers`
Use `03-breadcrumblist-missing-pages.jsonld`, `04-service-location-pages-offers.jsonld`,
`06-services-hub-collectionpage.jsonld`, `07-how-it-works-and-for-agents-webpage.jsonld`.

### ⚠️ Leave the existing `FAQPage` blocks alone
Google retired FAQ rich results for **all** sites on 2026-05-07. The four existing blocks no longer
produce a SERP feature, but they are valid, harmless, and removing them is pure cost. Just do not add
new `FAQPage` expecting SERP benefit.

---

## Stage 5 — Performance and images

**Calibration first.** CrUX field data is confirmed **unavailable** for this domain ("Insufficient
Chrome traffic volume"), and every PSI response returned empty `field_metrics`. Google's CWV ranking
assessment uses 75th-percentile *field* data. **It therefore cannot currently compute a CWV signal
for this site at all — CWV is a weak ranking lever here.** Do this because the images are genuinely
bad and cheap to fix, not because it will move rankings.

TTFB is already strong (222ms, `X-Vercel-Cache: HIT`). The LCP problem is entirely resource weight.

### 5.1 🟠 Compress the four oversized images
Verified on disk:

| File | Size | Note |
|---|---|---|
| `img/canada-visa-hero-banner.png` | **852 KB** | 94% wasted; direct cause of 11.7s mobile LCP |
| `img/toronto-proof-1.png` | **760 KB** | Trust asset — compress, do not remove |
| `img/toronto-proof-2.png` | **624 KB** | " |
| `img/toronto-proof-3.png` | **580 KB** | " |
| `img/breadcrumb.png` | **412 KB** | 31% wasted |
| `img/us-visa-appointment-canada-system.png` | 328 KB | |
| `img/us-visa-appointment-canada-hero.png` | 328 KB | |

Zero WebP/AVIF adoption sitewide. Convert all of these; keep PNG/JPG fallbacks via `<picture>`.
Expected: mobile LCP from 7.2–11.7s down substantially.

### 5.2 🟠 Add `width` and `height` to every image
**100% of images currently lack them**, including the hero carousel image (likely the LCP element).
Real CLS risk, and free to fix.

### 5.3 🟠 Add `fetchpriority="high"` + preload to the LCP image
Not present on any page.

### 5.4 🟡 Investigate desktop CLS
1.039 on home, 0.501 on blog (mobile CLS is 0 everywhere). Prime suspect: the `#spinner` full-viewport
overlay. Note it is correctly `visibility:hidden; opacity:0` post-load — so this is a layout shift
during load, not an interstitial problem.

### ⚪ Do not bother with
- **Ahrefs analytics** — 3.7 KB, ~4ms. Irrelevant.
- `gtag.js` costs up to 656ms main-thread and is the real third-party cost, but removing analytics
  to chase a lab metric with no field data is a bad trade. Leave it.

---

## Stage 6 — Content structure

*Everything here overlaps with [`02-growth-plan.md`](02-growth-plan.md). Listed here only where it
affects the audit score.*

### 6.1 🟠 Resolve the Canada/Toronto duplication
The two location pages share **65–75% verbatim text** (8-word shingle overlap coefficient 65.4%).
Toronto is a city inside Canada, so they compete directly for the same intent. This is the
doorway-page pattern — and it is the template that would be replicated if location pages scale.

Either differentiate genuinely (consulate-specific wait times — Toronto is at 14.5 months vs
Vancouver 12.5, which is real differentiating substance) or consolidate to one.

**Quality gate before scaling locations:** 60%+ unique content per page at 30+ pages. Stop and
justify at 50+. On the current template you would breach both.

### 6.2 🟠 Add author bylines with credentials to all blog posts
Zero bylines across all three posts. For YMYL content explaining consulate and AIS mechanics, a named
author with stated relevant experience is a direct Expertise signal — and it is one of the few
E-E-A-T levers still open given the declined trust items.

### 6.3 🟡 Split the three-way cannibalization on "US visa appointment Canada"
The Canada blog guide and both service pages target the same cluster. Currently masked because the
service pages are unindexed — **Stage 1 will unmask it.** Assign distinct intent before Stage 1
lands, or you create an active problem while fixing another.

- Blog guide → informational ("how the process works")
- `/services/us-visa-appointment-canada/` → commercial ("get help with it")

---

## What NOT to do

| Don't | Why |
|---|---|
| Rewrite the Canada blog guide to chase CTR | 300 impressions / 0 clicks at position 50.3 is *statistically expected* — under 1 click. It is a position problem, not a snippet problem. The page is 2,745 words and scored 84/100 |
| Add internal links to fix indexation | The unindexed pages already have up to 8 homepage links each; `/blog/` is indexed with **zero** nav links. Internal linking demonstrably does not explain the split |
| Chase the "striking distance" positions | `/services/` pos 1.0, `/how-it-works/` pos 4.0, `/blog/` pos 5.0 are each built from 1–4 impressions and vanish between periods. `/services/` is not even indexed. Noise, not opportunity |
| Read rising impressions as progress | Impressions rose 196% while CTR fell 3.26% → 1.47%. More visibility at position 41–97 earns nothing |
| Remove existing `FAQPage` schema | Valid and harmless; removal is pure cost |
| Add new `FAQPage` for SERP benefit | Google retired FAQ rich results for all sites 2026-05-07 |
| Add `HowTo` schema to `/how-it-works/` | Deprecated September 2023 |
| Add `Review`/`AggregateRating` schema | No genuine on-page reviews exist; self-serve markup violates Google policy |
| Prioritize Core Web Vitals | No field data exists, so Google cannot compute the signal for you |
| Chase head terms like "us visa appointment" | Owned by `ais.usvisa-info.com` — the actual government booking portal |
| Buy links or guest post at scale | Elevated penalty risk in this specific niche |
| Reinstate `/for-agents/` | Rejected on Stripe grounds — see `README.md` constraints |

---

## Sequencing

```
Now        Stage 1  → indexation          (unblocks everything)
Now        Stage 2  → security/infra      (Stripe review looks at this too)
Week 1     Stage 3  → on-page             (cheap, mechanical)
Week 1-2   Stage 4  → schema + entity     (files already written)
Week 2     Stage 5  → images/performance  (cheap, do not over-prioritize)
Week 2-4   Stage 6  → content structure   (merges into 02-growth-plan.md)
```

**If only three things get done:** 1.1 + 1.2 (sitemap + request indexing), 4.1 (the live placeholder),
and 3.1 (the broken `og:image` — because WhatsApp and Telegram are your actual distribution channels).
