# Full SEO Audit — easyvisabooking.com

**Audit date:** 2026-08-11
**Property:** `sc-domain:easyvisabooking.com` (Google Search Console access verified, `siteFullUser`)
**Business type:** Service business — paid intermediary booking US visa (AIS/CGI) interview appointments
**Pages analyzed:** 14 sitemap URLs + 4 non-sitemap URLs
**Data sources:** GSC Search Analytics, GSC URL Inspection API, GSC Sitemaps API, PageSpeed Insights v5, CrUX (unavailable), Common Crawl web graph, Playwright rendering, live SERP checks

---

# SEO Health Score: 55 / 100

| Category | Score | Weight | Contribution |
|---|---|---|---|
| Technical SEO | 50 | 22% | 11.0 |
| Content Quality | 54 | 23% | 12.4 |
| On-Page SEO | 62 | 20% | 12.4 |
| Schema / Structured Data | 58 | 10% | 5.8 |
| Performance (CWV) | 60 | 10% | 6.0 |
| AI Search Readiness | 48 | 10% | 4.8 |
| Images | 45 | 5% | 2.3 |
| **Total** | | | **54.7 → 55** |

---

# Executive Summary

The site is better built than its search performance suggests. The writing is genuinely
good (per-page content quality scored 84–96/100 with no filler patterns), every page has a
hand-written meta description, canonicals are clean, the HTML is static and fully parseable,
and the disclaimer and pricing-honesty language is unusually responsible for this category.

None of that is currently reaching Google, because of one dominant problem.

## The finding that outranks everything else

**Half the site does not exist as far as Google is concerned — and it is the half that
makes money.**

GSC URL Inspection on all 14 sitemap URLs returns:

| Status | Count | URLs |
|---|---|---|
| Submitted and indexed | 7 | `/`, `/how-it-works/`, `/contact/`, `/blog/`, and all 3 blog posts |
| **URL is unknown to Google** | **7** | **`/services/`, `/services/us-visa-appointment-canada/`, `/services/us-visa-appointment-toronto/`, `/about/`, `/terms/`, `/privacy/`, `/refund-policy/`** |

"Unknown to Google" is not "crawled and rejected." It is *never crawled, never discovered,
not in the index, not in the queue* — `page_fetch_state: PAGE_FETCH_STATE_UNSPECIFIED`,
`referring_urls: []`, no `last_crawl_time` at all.

What is missing is precisely:

- **Every commercial service page.** The pages that sell the service and convert visitors.
- **`/about/`** — the single most important E-E-A-T page on a YMYL site.
- **All three trust/policy pages** — terms, privacy, refund policy.

What *is* indexed is the blog. So the site's entire measured search presence (382
impressions in 90 days, 79% of it on one blog post) comes from informational content,
while the conversion path is invisible.

### The cause is not what it looks like

The obvious diagnosis — "these pages must be poorly linked" — is wrong, and acting on it
would waste effort. The homepage is indexed and was crawled on 2026-08-04, and it links to:

```
/services/                8 links
/about/                   3 links
/refund-policy/           3 links
/terms/                   2 links
/services/...-toronto/    2 links
/services/...-canada/     2 links
/privacy/                 1 link
```

Google crawled a page linking to `/services/` eight times and still reports `/services/`
as unknown with zero referring URLs. Conversely, `/blog/` **is** indexed despite having no
header or footer nav link anywhere on the site. Internal linking does not explain the split.

Two things do:

1. **Google is working from a stale, smaller sitemap.** The GSC Sitemaps API reports the
   sitemap was last processed on **2026-06-23** containing **10 URLs**. The live sitemap
   has **14**. Zero errors, zero warnings — Google simply has not re-fetched in ~7 weeks.
   Every `lastmod` in the file is the identical value `2026-08-07`, and uniform templated
   `lastmod` values are a known trigger for Google discounting the field entirely.

2. **Crawl demand is near zero.** The domain sits at the bottom of the Common Crawl
   authority distribution (PageRank rank ~1.2M, harmonic centrality rank ~377K) with no
   discoverable referring domains. Google allocates crawl budget by demand; a site with no
   external signals gets its homepage crawled and little else.

## The second-order finding

Fixing indexation will expose, not solve, the deeper constraint. Live SERP checks confirm
that the broad commercial queries this site targets — "canada us visa appointment" and
similar — are owned by `ais.usvisa-info.com` (the official booking portal itself),
`travel.state.gov`, and `ca.usembassy.gov`. No commercial content page displaces a
government portal on those terms. The site is currently ranked 45–80 for a query class it
cannot win.

The winnable class is different and adjacent: **rescheduling mechanics, slot-release
timing, service legitimacy, and cost transparency** — query clusters where SERPs are
dominated by blogs and forums with near-zero government presence.

## Reading the flagship page correctly

`/blog/us-visa-appointment-canada-guide-2026/` carries 300 impressions (79% of the site's
total) and **zero clicks** at average position 50.3. This looks alarming and is widely
misdiagnosed. Two independent analyses agree: at position 50, expected clicks from 300
impressions is **under 1**. Zero is statistically unremarkable. The page is 2,745 words,
well-structured, and scored 84/100 on content quality; its queries map cleanly onto its
content.

**This is a position problem, not a snippet or format problem.** Rewriting the title and
meta description would be effort spent on the wrong variable. The position is low because
the domain has no authority and the page targets the unwinnable query cluster.

Period-over-period, this page shows the site's one real ranking pattern: **query breadth
growing without rank improving.** Impressions nearly tripled (64 → 236) across dozens of
long-tail Canada queries, but every one sits at position 41–97. That is why sitewide CTR
*fell* from 3.26% to 1.47% while impressions rose 196% — the site is being shown for more
queries, all of them too deep to earn a click. More impressions at position 50 is not
progress; it is the same problem at greater scale.

## A trap worth naming: the "striking distance" mirage

GSC shows tempting-looking average positions — `/services/` at 1.0, `/how-it-works/` at 4.0,
`/blog/` at 5.0, `/for-agents/` at 11.2. These are **statistical noise, not opportunities.**
Each is built from 1–4 total impressions, none appear in the query × page breakdown (their
queries fall below GSC's anonymization threshold), and `/services/`'s "position 1.0" appeared
once in the prior 28-day window then vanished entirely from the latest one. `/services/` is
not even indexed.

Chasing CTR or content fixes on these would be optimizing noise. They are listed here
specifically so they do not get mistaken for quick wins.

## A compounding detail

`/for-agents/` is indexed on **stale, pre-redirect data** — GSC's last crawl (2026-06-24)
recorded it as a live self-canonical page, and it still draws impressions. So a searcher who
clicks that result today gets 308-bounced into `/services/` — which is itself unindexed and
whose three of five location links are 404s. The one page with the site's best average
position leads to a broken destination.

---

# Findings by Category

## Technical SEO — 50/100

### CRITICAL · Seven URLs unknown to Google
Covered in the executive summary. This is the audit's top finding.
**Falsifiability:** re-inspect the 7 URLs in 14 days; any still reporting "URL is unknown
to Google" after sitemap resubmission and manual indexing requests means the cause is
deeper than crawl scheduling and warrants checking for a CDN/edge rule serving different
content to Googlebot.

### CRITICAL · `/services/` links to 3 pages that are 404 *and* robots-blocked
```
/services/us-visa-appointment-canada/     -> 200
/services/us-visa-appointment-toronto/    -> 200
/services/us-visa-appointment-dubai/      -> 404   (and Disallow'd in robots.txt)
/services/us-visa-appointment-uae/        -> 404   (and Disallow'd in robots.txt)
/services/us-visa-appointment-australia/  -> 404   (and Disallow'd in robots.txt)
```
Three of the five location links on the service hub are dead, and the homepage links to
them too. The `/services/` meta description actively advertises them: *"We help applicants
in Canada, Dubai, UAE, Australia and more."*

The robots.txt `Disallow` makes this worse rather than better. A disallowed URL cannot be
crawled, so Google can never observe the 404 and can never cleanly drop the URL. Disallow
is the wrong instrument for removing pages.

A user clicking "Dubai" from the service hub lands on a 404 — in a category where visitors
are actively scanning for signs the operator is not legitimate.

**Fix — pick one path per location, do not mix:**
- *Building them:* remove the three `Disallow` lines, ship the pages at 200, add to sitemap.
  Recommended for Dubai, which already has a ranking blog post to link into.
- *Abandoning them:* remove the links from `/services/` and the homepage, remove the
  `Disallow` lines so Google can process the removal, serve 410 Gone, and correct the
  `/services/` meta description.

**Falsifiability:** every outbound service link on `/services/` resolves 200; GSC Page
Indexing shows zero URLs under "Indexed, though blocked by robots.txt."

### HIGH · Google is working from a stale 10-URL sitemap
Detailed above. **Fix:** resubmit in GSC; make `lastmod` per-page and truthful (omit it
entirely rather than publish uniform fake dates); drop `priority` and `changefreq`, which
Google ignores.
**Falsifiability:** GSC Sitemaps reports `submitted: 14` and a `last_submitted` after
2026-08-11. If it still reads 10 after 14 days, check for a stale edge-cached copy of
`sitemap.xml` on Vercel.

### HIGH · Favicon 404s on 8 of 14 pages (case-sensitivity bug)
`brand-logo-real.PNG` returns 200; `brand-logo-real.png` returns 404. Vercel static hosting
is case-sensitive. Eight pages reference the lowercase path. No `/favicon.ico` fallback
exists either.

### HIGH · Security headers effectively absent
The only security header present sitewide is `Strict-Transport-Security: max-age=63072000`
(missing `includeSubDomains` and `preload`). Absent: CSP, `X-Content-Type-Options`,
`X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`.

These are not ranking factors and should not be sold as such. They matter because this site
collects passport details and payment intent in a scam-adjacent category. Add via
`vercel.json`; add CSP only after auditing gtag.js and analytics.ahrefs.com, and verify
analytics still fires afterwards.

### CRITICAL (business) · `/for-agents/` silently deleted
`/for-agents` → 308 → `/for-agents/` → 308 → `/services/` → 200 (two hops). It still earns
6 impressions at **average position 11.2** — the best average position on the entire site.

It was folded into `/services/`, a ~507-word consumer location directory with **zero**
mention of agents, B2B, or bulk booking. A distinct, higher-intent audience was dropped by
attrition. Collapse the chain to one hop, and treat reinstating a real B2B page as a
deliberate decision rather than an accident.

### Confirmed healthy — do not "fix" these
Apex 301s to www; all pages self-canonical; correct `index, follow` meta robots; no mixed
content; static HTML with full raw/rendered parity; true 404 status codes; no duplicate
titles or descriptions; sitemap valid and declared in robots.txt.

---

## Content Quality — 54/100

Raw writing quality is a genuine strength: 84–96/100 per page, zero filler/AI-slop pattern
matches. The score reflects structural E-E-A-T and trust gaps, not prose.

### HIGH · No verifiable legal entity
`/terms/` states *"Our registered details are set out at the top of this page and on our
About page"* — but the actual content shows only "Operated by: Easy Visa Booking" (a
trading name) and a founder's personal name. No company number, no registered address, no
jurisdiction. A page that promises registration details and does not deliver them is worse
than one that never promised. Material YMYL trust risk.

### HIGH · Zero social proof anywhere
No testimonials, reviews, case studies, or third-party validation. The homepage HTML
contains the literal comment `<!-- Testimonial section removed -->`. Claimed confirmation
screenshots are "available on request" rather than shown. In a scam-heavy niche this is the
single largest conversion gap.

### HIGH · 65–75% verbatim duplication between the two location pages
`/services/us-visa-appointment-canada/` and `/services/us-visa-appointment-toronto/` share
75% of the Canada page's text verbatim (8-word shingle overlap coefficient 65.4%). Toronto
is a city inside Canada, so these compete directly. This is the doorway-page pattern, and
it is the template that would be replicated if location pages scale.

### HIGH · No author bylines or credentials on any blog post
Zero bylines across all three posts. For YMYL content explaining consulate and AIS
mechanics, this is a direct Expertise gap.

### MEDIUM · Three-way cannibalization on "US visa appointment Canada"
The blog guide plus both service pages target the same cluster. GSC shows the blog post
absorbing all 300 impressions while the service pages get none — though note the service
pages are also unindexed, so this is currently masked. Split intent explicitly before
fixing indexation, or the cannibalization becomes active.

### Genuine strengths
Pricing honesty ("no upfront fee", "pay only on success"), explicit "we cannot guarantee a
date" language, and a well-structured anchor-linked refund policy. These are better than
most sites in this category and should be made *more* prominent, not changed.

---

## On-Page SEO — 62/100

All pages carry hand-written, specific meta descriptions — a real strength. Titles are
descriptive and keyword-aligned. H1s present.

| Issue | Severity | Detail |
|---|---|---|
| Meta descriptions exceed render limit | Low | 162–231 chars vs ~155 safe. Toronto (216) and Dubai blog (231) lose their differentiating clause ("Pay only on success") to truncation |
| Titles over 60 chars | Low | Toronto (72), `/` (65), Canada service (65) |
| No `og:description`, no `twitter:card` sitewide | Medium | Links shared to WhatsApp/Telegram — both advertised contact channels — render without rich previews |
| Homepage `og:image` 404s | Medium | `/img/visa-banner.jpg` does not exist; no other page has `og:image` at all |
| `/blog/` unlinked from nav and footer | Medium | Indexed anyway, but no equity flows to it |
| `/services/` thin at ~507 words | Medium | Thinner than its own children (Toronto 3,573w, Canada 2,795w) — cannot carry hub duty |

---

## Schema / Structured Data — 58/100

All existing JSON-LD parses valid; no deprecated types; dates are correct ISO 8601; no
fabricated reviews.

### CRITICAL · Placeholder text live in production
Homepage `Organization.sameAs` contains the literal unfilled placeholder
`"https://t.me/YourTelegramChannel"`. The real channel, live in the footer, is
`https://t.me/earlyusvisabooking`.

### CRITICAL · `/contact/` ships zero JSON-LD
The page most needing machine-readable `ContactPoint` has none, despite email, phone
(+91-8849146234), and WhatsApp all being live on it.

### CRITICAL · `image` missing from all 3 `BlogPosting` blocks
Google's most consistently required Article property for rich-result eligibility.

### HIGH · No `@id` entity linking; Organization duplicated as 7+ anonymous islands
The homepage declares `Organization` twice (top-level and nested in `Service.provider`)
with no `@id`. `/about/`, both service pages, and all three blog posts each add
disconnected stub copies. This fragments entity consolidation for both Google and AI
crawlers — and entity clarity is exactly what this site needs most.

### HIGH · `BreadcrumbList` absent on 6 pages; `offers` missing from both `Service` blocks

### Info · Existing `FAQPage` blocks
Four `FAQPage` blocks exist. Google retired FAQ rich results for all sites on 2026-05-07,
so these no longer produce a SERP feature. **Recorded at Info only — do not remove them.**
They remain valid structured data and removal costs effort for no gain. Do not add new
FAQPage expecting SERP benefit.

Corrected, ready-to-paste JSON-LD for every gap above is in
`findings/schema-generated/` (7 files).

---

## Performance — 60/100 (mobile lab) / 78 (desktop lab)

**CrUX field data is confirmed unavailable** — `crux_history.py` returned 404 "Insufficient
Chrome traffic volume for eligibility," and every PSI response returned empty
`field_metrics: {}`. This is consistent with 382 impressions in 90 days.

**All numbers below are Lighthouse lab data.** Google's actual Core Web Vitals ranking
assessment uses 75th-percentile *field* data, which cannot be computed for this site.
**CWV is therefore a weak ranking lever here** relative to indexation, trust, and links —
do not prioritize it above those.

| Metric | Value | Type | Status |
|---|---|---|---|
| LCP mobile | 7.2s – 11.7s | Lab | Fails on every page |
| LCP desktop | 1.3s – 2.0s | Lab | Good |
| INP | Not measurable (no field data) | — | Cannot be assessed |
| TBT (lab proxy, *not* INP) | 50ms – 540ms | Lab | Directional only |
| CLS mobile | 0 on all 5 pages | Lab | Good |
| CLS desktop | 1.039 (home), 0.501 (blog) | Lab | Poor on 2 of 5 |

- **Critical:** `canada-visa-hero-banner.png` is 869KB (94% wasted) and `breadcrumb.png` is
  421KB (31% wasted) — the direct cause of 11.7s mobile LCP. Zero WebP/AVIF adoption sitewide.
- **High:** LCP image not preloaded or `fetchpriority="high"` on any page.
- **High:** Desktop CLS 1.039 traced to a body-level shift, plausibly the `#spinner` overlay.
- **Medium:** gtag.js dominates third-party cost (up to 656ms main-thread). Ahrefs analytics
  is negligible (3.7KB, ~4ms) — not worth touching.
- **Pass:** TTFB is genuinely strong — 222ms, `X-Vercel-Cache: HIT`. The LCP problem is
  entirely resource weight and discovery, not server response.

---

## AI Search Readiness — 48/100

- **AI crawler access is fully open.** GPTBot, OAI-SearchBot, ClaudeBot, Claude-User,
  Claude-SearchBot, PerplexityBot, Applebot-Extended, CCBot, meta-externalagent, Bingbot,
  and Google-Extended are all unblocked. (Note: Google-Extended governs Gemini/Vertex
  training and grounding only — it does **not** gate AI Overviews or classic Search
  inclusion, which run off ordinary Googlebot.)
- **HIGH · The homepage's FAQPage JSON-LD and its visible FAQ accordion are completely
  different content** — different questions, different answers. The only stated price
  ($100 starting fee) exists **solely in schema and never in visible text**. Structured data
  must describe what is on the page.
- **HIGH · Entity signals are the weakest dimension (18/100).** The `sameAs` placeholder bug,
  plus **up to six different, mutually contradictory lists** of which countries the service
  covers across Organization description, Organization `areaServed`, Service `areaServed`,
  the About page schema, visible FAQ text, and a homepage subheading. Only Canada has an
  actual indexable location page.
- **llms.txt absent (404).** Stated honestly: llms.txt is not used by Google and no major AI
  vendor has confirmed production use. Low priority; do not let it displace trust work.
- **Realism.** With 9 clicks and average position 45.2, this domain is not in the candidate
  pool most AI answer engines draw from. In a YMYL commercial-intermediary category with
  heavy scam activity, formatting alone cannot produce citations. Trust and authority are
  the binding constraint.

---

## Images — 45/100

- 869KB and 421KB PNGs shipped uncompressed; zero WebP/AVIF adoption.
- 100% of images lack explicit `width`/`height` attributes, including the hero carousel
  image (likely the LCP element) — real CLS risk.
- Homepage `og:image` points to a 404.
- **Strength:** 100% alt-text coverage across all analyzed pages.

---

## Visual / Mobile UX — 54/100

- **High:** No government-affiliation disclaimer visible without scrolling on any page. The
  disclaimer exists and is well-worded — but sits in the global footer, roughly 9,000px down
  the homepage. In this category that sentence is a conversion asset, not a legal footnote.
- **High:** Zero third-party trust signals; no `tel:` link anywhere on the site (email,
  WhatsApp, Telegram only) despite schema and a homepage trust badge promising phone support.
- **Medium-High:** `/services/` has ~1,200–1,500px of dead space and an empty styled box
  between the location cards and footer, on both desktop and mobile.
- **Medium:** Confirmed mobile horizontal overflow — 48px on home, 22px on services-canada.
- **Medium:** Fixed WhatsApp button overlaps body copy on `/contact/` mobile.
- **Cleared:** viewport meta correct, 16px base font, no intrusive interstitials (the
  full-viewport `#spinner` is `visibility:hidden; opacity:0` post-load), hamburger works.

---

## Backlinks / Authority — no score (insufficient data, by design)

Backlink tier is 0: Common Crawl and the verification crawler only. Moz and Bing Webmaster
keys are not configured. **No numeric score is reported, because only 1 of 7 scoring factors
has any data source — producing a number here would be fabrication.**

What is known: the domain **is** present in Common Crawl's Jan–Mar 2026 web graph and clears
its ranking threshold, but sits at the bottom of the authority distribution (PageRank rank
~1.2M, harmonic centrality rank ~377K). Confidence: 0.50. No candidate backlink URLs surfaced
anywhere in this audit, so nothing could be verified.

**Assessment:** cross-referencing near-zero Common Crawl authority against GSC position
45–80 on commercial head terms supports a blunt conclusion — **link acquisition is very
likely the binding constraint on this site**, more binding than any remaining on-page or
technical work.

Highest-leverage next step: configure the **free Moz API tier** (2,500 rows/month,
https://moz.com/products/api). It is the only free source that would return a referring-domain
count and spam score, both currently blank. **Bing Webmaster Tools** (free,
https://www.bing.com/webmasters) is a reasonable second — and it also feeds Microsoft Copilot
citations.

**Avoid** the tactics endemic to this niche: PBNs, paid link networks, mass guest posting,
comment and forum spam. Flagged Critical risk given elevated Google scrutiny here and the
site's lack of an established track record.

---

# Content Strategy (from SERP-based clustering)

**Unwinnable — do not anchor strategy here.** "us visa appointment", "us visa interview slot",
"us visa wait times" return SERPs 40–70% dominated by travel.state.gov, ais.usvisa-info.com,
and ustraveldocs.com, plus funded incumbents (Atlys, VisaGrader, CheckVisaSlots).

**Genuinely winnable.** Rescheduling mechanics, slot-release timing, service legitimacy and
trust, cost transparency, and location comparisons — SERPs here are blog- and forum-dominated
with near-zero government presence.

**Hub decision.** `/services/` at ~507 words is too thin to serve as pillar — it is smaller
than both of its own children. Recommendation: build a new informational guide pillar
(`/blog/us-visa-appointment-guide/`) for topical authority, and separately rebuild `/services/`.

**Four clusters designed** with a full internal link matrix: Location/Wait-Times;
Rescheduling & Slot Timing; Trust/Legitimacy/Cost; B2B/Agent Booking.

**B2B note:** SERP data for "us visa appointment for travel agents" shows near-zero government
competition and real dedicated competitors already ranking (usvisaagents.com, path2usa.com,
giecglobal.com). Combined with `/for-agents/`'s position 11.2, reinstating a dedicated B2B
page looks justified — flagged as a decision point, not a default.

**Defensible angles a government portal cannot cover:** real slot-release timing patterns,
consulate-by-consulate wait-time comparisons, what actually happens during a reschedule, and
first-hand process documentation.

---

# Method Note

Findings were synthesized through PERCEIVE → ANALYZE → VALIDATE → ACT. The priority buckets
below are the *output* of validation, not a substitute for it. Two conclusions were
explicitly revised during the audit when evidence contradicted the initial reading:

1. `/for-agents/` was initially framed as an orphan page missing from the sitemap. It is a
   308 redirect, correctly excluded. Framing corrected mid-audit.
2. Meta descriptions were initially read as missing sitewide. That was a faulty grep pattern;
   they are present and well-written. Corrected before it reached any conclusion.

Every recommendation carries an explicit falsifiability check, so each can be independently
verified or refuted without re-running the audit.
