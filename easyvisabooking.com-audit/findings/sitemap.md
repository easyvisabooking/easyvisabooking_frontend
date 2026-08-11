# Sitemap Audit — easyvisabooking.com

Sitemap: `https://www.easyvisabooking.com/sitemap.xml` (declared in robots.txt)
Audit date: 2026-08-11 | 14 URLs, 2,699 bytes uncompressed

## Score: 90/100

The sitemap itself is clean and correctly scoped: valid XML, every listed URL is a live,
self-canonical 200 with no noindex, and the site correctly *excludes* both a redirected
legacy URL and three not-yet-launched location pages that are 404 + robots.txt-disallowed.
The only real defects are informational/low-severity: fabricated-looking uniform `lastmod`
values and the presence of ignored `priority`/`changefreq` tags. The highest-value output
of this audit is forward-looking: the site's markup already reveals a plan to scale
location pages worldwide, which is a programmatic-SEO risk worth gating now, before it exists.

---

## 1. XML Validity & Schema Conformance — PASS (Info)

**Evidence:** Parsed with `xml.etree.ElementTree` — well-formed, root element
`{http://www.sitemaps.org/schemas/sitemap/0.9}urlset`, 14 `<url>` children, each with
`<loc>`, `<lastmod>`, `<changefreq>`, `<priority>`. No parse errors.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
```

**Severity:** Info (pass). **Fix:** None needed.
**Falsifiability:** Re-fetch `https://www.easyvisabooking.com/sitemap.xml` and parse with any
standard XML parser; should succeed with 14 `<url>` elements under the sitemaps 0.9 namespace.

---

## 2. Size / URL-Count Limits — PASS (Info)

**Evidence:** 14 URLs, 2,699 bytes. Sitemaps protocol caps: ≤50,000 URLs AND ≤50MB
uncompressed (whichever first); ≤1,000 for `news:` sitemaps (n/a here — no `news:` namespace
present). Current file uses 0.03% of the URL limit and 0.005% of the size limit.

**Severity:** Info. **Fix:** None. Revisit only once URL count approaches ~40,000 or file
approaches ~40MB.
**Falsifiability:** `curl -s -o sitemap.xml .../sitemap.xml && wc -c sitemap.xml` and count
`<url>` tags — should be well under both caps.

---

## 3. URL Health: 200 status, self-canonical, indexable — PASS for all 14 (Info/Low)

**Evidence:** All 14 sitemap URLs verified with `curl -D -` (custom UA) — every one returned
`HTTP/1.1 200 OK` with no redirect. Spot-checked HTML `<head>` for canonical + robots meta on
all 14, including the blog posts and the three policy pages that are easy to overlook:

| URL | Status | Canonical matches loc | Robots meta |
|---|---|---|---|
| `/` | 200 | yes | `index, follow` |
| `/services/` | 200 | yes | `index, follow` |
| `/services/us-visa-appointment-canada/` | 200 | yes | `index, follow` |
| `/services/us-visa-appointment-toronto/` | 200 | yes | `index, follow` |
| `/how-it-works/` | 200 | yes | `index, follow` |
| `/about/` | 200 | yes | `index, follow` |
| `/contact/` | 200 | yes | `index, follow` |
| `/blog/` | 200 | yes | `index, follow` |
| `/blog/us-visa-appointment-world-cup-2026-guide/` | 200 | yes | `index, follow` |
| `/blog/us-visa-appointment-canada-guide-2026/` | 200 | yes | `index, follow` |
| `/blog/us-visa-appointment-dubai-fast-2026/` | 200 | yes | `index, follow` |
| `/terms/` | 200 | yes | `index, follow` |
| `/privacy/` | 200 | yes | `index, follow` |
| `/refund-policy/` | 200 | yes | `index, follow` |

No 404s, no redirects, no noindex among the 14 listed URLs.

**Severity:** Info (pass). **Fix:** None needed; keep this in the release checklist so a
future redirect/noindex doesn't silently sit in the sitemap.
**Falsifiability:** `curl -sI -A "Mozilla/5.0" <url>` for each of the 14 URLs should return
`HTTP/1.1 200`, and `curl -s <url> | grep -E 'canonical|name="robots"'` should show a
self-referencing canonical and no `noindex`.

---

## 4. `lastmod` Accuracy — FAIL (Low-Medium)

**Evidence:** Every one of the 14 `<lastmod>` values in the sitemap is identical:
`2026-08-07`. The date format itself is valid W3C Datetime (`YYYY-MM-DD`), so this is not a
syntax defect — it's a trust/signal defect.

Cross-checked against live server `Last-Modified` response headers on 2026-08-11:

```
/                                        Last-Modified: Tue, 11 Aug 2026 05:37:11 GMT
/services/                               Last-Modified: Tue, 11 Aug 2026 16:11:47 GMT
/services/us-visa-appointment-canada/    Last-Modified: Tue, 11 Aug 2026 16:43:24 GMT
/contact/                                Last-Modified: Tue, 11 Aug 2026 16:10:38 GMT
/refund-policy/                          Last-Modified: Tue, 11 Aug 2026 16:43:42 GMT
```

Two problems, both falsifiable from the data above:
1. **Every server `Last-Modified` is 2026-08-11 (today, audit day)** — not 2026-08-07 as the
   sitemap claims. The sitemap's date is stale/wrong relative to the server's own header.
2. **The `Last-Modified` timestamps also differ from each other by minutes across pages on
   the same day** (05:37 vs 16:10 vs 16:43), which is consistent with a full-site redeploy
   (Vercel static rebuild), not per-page content edits. This means neither the sitemap's
   `2026-08-07` nor the server's `Last-Modified` can currently be trusted as "date of last
   *significant* content change" — both look infrastructure-driven (build/deploy time), not
   content-driven.

Per Google's own guidance, `lastmod` is only useful when it reflects genuine content changes;
uniform or deploy-driven dates are commonly ignored/distrusted by crawlers, which defeats the
purpose of including the tag at all.

**Severity:** Low-Medium (matches "All identical lastmod → Low" in the standard checklist,
elevated slightly here because the value also mismatches the server's own header, suggesting
it's hardcoded in the sitemap generator rather than derived from any real timestamp).
**Fix:** Generate `lastmod` from the CMS/build pipeline's actual "content updated at" field
(not deploy time, not a hardcoded constant). If no CMS field exists yet, it is safer to *omit*
`lastmod` entirely than to publish a value indistinguishable from a fabricated one.
**Falsifiability:** Diff the sitemap XML against itself on two different days after a genuine
content edit to only one page — a correct implementation should show `lastmod` change for
that one URL only, not all 14.

---

## 5. `changefreq` / `priority` — Info, no action required, low value

**Evidence:** Sitemap sets `<changefreq>` (weekly/monthly/yearly) and `<priority>` (1.0 down
to 0.4) on every URL, e.g.:
```xml
<changefreq>weekly</changefreq>
<priority>1.0</priority>
```
Google has publicly stated both tags are ignored for crawling/ranking purposes and have been
for years; Bing's usage is also minimal/undocumented. They are inert metadata here — not
harmful, but not delivering any measurable crawl-budget or ranking benefit either.

**Severity:** Info. **Fix:** Optional cleanup only — removing them shrinks the file slightly
and removes false signal of control the team doesn't actually have over crawl behavior. Do
not spend engineering time here ahead of higher-impact items; do not expect any ranking or
crawl-frequency change from touching these tags.
**Falsifiability:** No test will show a ranking/crawl delta from adding, removing, or changing
these values — that absence of measurable effect is itself the confirming check.

---

## 6. Coverage Gap Analysis — no real gaps found; two false-positive candidates explained

Crawled internal links across all 14 sitemap pages (homepage, services, both live location
pages, how-it-works, about, contact, blog index + 3 posts, terms, privacy, refund-policy) and
cross-checked every internal `href` found against the sitemap and live HTTP status.

### 6a. `/for-agents/` — correctly excluded (not a gap)
**Evidence:**
```
curl -D- https://www.easyvisabooking.com/for-agents/
HTTP/1.1 308 Permanent Redirect
Location: /services/
```
```
curl -D- https://www.easyvisabooking.com/for-agents   (no trailing slash)
HTTP/1.1 308 Permanent Redirect
Location: /for-agents/
```
So `/for-agents` is a **2-hop redirect chain** (`/for-agents` → `/for-agents/` → `/services/`)
that ultimately lands on 200. A URL that redirects must never be listed in a sitemap — its
absence here is correct sitemap hygiene, not a coverage gap.

GSC URL Inspection confirms this is a *transient* state, not a defect: Google's last crawl of
`/for-agents/` was **2026-06-24**, when the page still returned 200 and was
"Submitted and indexed." The 308 redirect was introduced sometime after that crawl. The 6
impressions / avg. position 11.2 seen in the 90-day GSC window reflect Google still serving
that stale index entry — this will self-correct once Google recrawls and processes the
redirect; it does not require a sitemap change.

**Severity:** Info (no fix needed for the sitemap). **Secondary note (Low, not a sitemap
defect):** the 2-hop chain (`/for-agents` → `/for-agents/` → `/services/`) could be collapsed
to a single 308 straight to `/services/` to save one round-trip for crawlers/users, but this is
a redirect-map cleanup item, not a sitemap issue.
**Falsifiability:** `curl -sI -A Googlebot https://www.easyvisabooking.com/for-agents/` should
show `308` → `Location: /services/`; GSC URL Inspection on the same URL should show
`last_crawl_time` predating the redirect's introduction.

### 6b. Three unlaunched location pages — correctly excluded (not a gap, evidence of a roadmap)
Link-crawling every sitemap page turned up three additional internal hrefs not in the sitemap:
`/services/us-visa-appointment-australia/`, `/services/us-visa-appointment-dubai/`,
`/services/us-visa-appointment-uae/`. These are **not** a coverage gap:

**Evidence — all three 404:**
```
curl -D- https://www.easyvisabooking.com/services/us-visa-appointment-dubai/
HTTP/1.1 404 Not Found
```
**Evidence — all three explicitly blocked in robots.txt:**
```
User-agent: *
Allow: /
Disallow: /services/us-visa-appointment-dubai/
Disallow: /services/us-visa-appointment-uae/
Disallow: /services/us-visa-appointment-australia/

Sitemap: https://www.easyvisabooking.com/sitemap.xml
```
So these are pages the team has scaffolded links for (likely in a site-wide "browse
locations" component, since the hrefs appear on nearly every crawled page) but hasn't
launched yet — correctly kept out of both the crawl path (robots.txt) and the sitemap.

**Severity:** Low, secondary finding (not a sitemap defect, but a linked-but-404 internal-link
hygiene issue worth flagging to the site team): a live page currently links to three URLs that
404. This wastes a small amount of crawl budget on 404s despite the robots.txt block (robots.txt
disallow prevents crawling, but doesn't remove the broken `<a href>` from the user-facing HTML)
and is a minor UX papercut if a visitor clicks one.
**Fix:** Either (a) remove/hide these three links from the "browse locations" component until
the pages ship, or (b) if they're intentionally shown as a "coming soon" roadmap, mark them
non-clickable / with a "coming soon" badge rather than a live `<a href>` to a 404.
**Falsifiability:** `curl -sI <url>` on each of the three should currently return 404; once
launched, they should return 200 and only then be added to both robots.txt (removing the
Disallow) and sitemap.xml.

### 6c. No other gaps
No other internal `href` values were found across the crawl that (a) return 200, (b) are
indexable, and (c) are absent from the sitemap. Coverage of the 14 live, indexable pages is
complete.

**Falsifiability:** Re-run a link crawl from all sitemap URLs plus the homepage; any newly
discovered internal link returning 200 with `index,follow` and not in `sitemap.xml` would be a
genuine gap requiring re-audit.

---

## 7. Location Page Quality Gates — forward-looking risk flag (Medium, pre-emptive)

**Current state:** 2 location pages in the sitemap — `/services/us-visa-appointment-canada/`
and `/services/us-visa-appointment-toronto/`. This is far under the 30-page warning threshold
and the 50-page hard stop. **No gate is triggered today.**

**Why this needs to be said now anyway:** Every piece of evidence gathered in this audit
points to imminent scaling of this exact page type:
- Business context: "Global service business with location-targeted pages (Canada, Toronto,
  Dubai)" — Dubai is already named as a target market.
- The site already has a reusable "browse locations" internal-linking component (found on
  nearly every page) pre-wired with three more cities/countries
  (`us-visa-appointment-dubai`, `-uae`, `-australia`) that 404 today.
- `robots.txt` has pre-emptive `Disallow` rules for those same three URLs — someone is actively
  managing this rollout, not just prototyping.
- The blog already has a Dubai-specific guide (`/blog/us-visa-appointment-dubai-fast-2026/`)
  priming that market ahead of the location page's launch.

This is a textbook setup for **programmatic location-page scaling** — the highest-risk pattern
for Google's doorway-page / thin-content algorithms when done by swapping only the city name.

**Baseline quality check on the 2 existing pages (for future comparison):** word-count and
text-similarity diff between `/services/us-visa-appointment-canada/` (1,905 words) and
`/services/us-visa-appointment-toronto/` (2,324 words) — character-level `difflib` similarity
ratio ≈ 0.35 (i.e., roughly 65% non-matching text), word-level Jaccard overlap ≈ 0.56. Both
pages are substantive (not thin) and reasonably differentiated today. **This baseline must be
maintained or improved as more pages are added** — it is not itself a pass/fail gate, just the
current reference point.

**Explicit forward guidance (apply before, not after, scaling):**
- **At 30+ location pages:** each page must carry **60%+ genuinely unique content** — unique
  local logistics (actual consulate address, appointment-slot availability patterns specific
  to that post, local document/photo requirements, region-specific processing-time data,
  genuine local reviews/testimonials), not just city-name find/replace over a shared template.
  Recommend measuring this the same way this audit just did — pairwise text-similarity diffs
  across every new page pair before publishing — and rejecting any page pair whose unique-text
  ratio falls under 60%.
- **At 50+ location pages:** treat this as a **hard stop** requiring explicit, documented
  business justification before publishing more — not an automatic engineering task. Google's
  doorway-page algorithm specifically targets exactly this pattern: large numbers of
  near-duplicate location pages built to rank for "[service] in [city]" without proportionally
  unique value.
- **Practical recommendation:** build a per-consulate content checklist now (real address/hours,
  actual local appointment-wait-time data, country-specific visa document nuances, at minimum
  one locally-sourced testimonial or case reference) so that page #3 through #29 are held to the
  same bar as page #30+ from day one, rather than retrofitting quality after a doorway-page
  pattern is already live and indexed.

**Severity:** Medium (pre-emptive/advisory — no violation exists today, but the infrastructure
for the violation is already partially built).
**Fix:** Adopt the 60%-unique-content bar and the 50-page justification gate as a written
publishing rule before the Dubai/UAE/Australia pages (or any further cities) go live.
**Falsifiability:** Count location pages in `sitemap.xml` matching pattern
`/services/us-visa-appointment-*/` at any future audit date; if count ≥ 30, re-run the
pairwise text-similarity check used above on all pages and require ≥60% unique ratio per page;
if count ≥ 50, confirm a documented business justification exists.

---

## 8. Image Sitemap / News Sitemap — not warranted (Info, justified)

**Image sitemap:** Not recommended. The site is a service/booking business (visa appointment
booking), not an image-led vertical (e.g., stock photography, real estate, recipes). No page
crawled during this audit depends on image search traffic as a plausible acquisition channel,
and standard `<img>` tags with proper `alt` text are already sufficient for Google Images
indexing without a dedicated image sitemap — the image sitemap protocol mainly helps when
images are loaded via JS/lazy-load patterns that hide them from a normal crawl, or when
driving meaningful Image Search traffic is a stated goal. Neither applies here.

**News sitemap:** Not recommended, and would likely be rejected by Google if submitted. News
sitemaps require the publisher to be accepted into Google News, with strict recency
requirements (articles must be added within the last 2 days to remain eligible) and content
must be genuinely news-style journalism. This site's `/blog/` contains evergreen how-to/guide
content (world cup 2026 visa guide, Canada guide, Dubai guide) published on an infrequent
cadence — not a newsroom. A `news:` sitemap here would add maintenance overhead (1,000-URL
cap, 2-day freshness requirement) with no realistic approval path or traffic upside.

**Severity:** Info. **Fix:** None — do not build either.
**Falsifiability:** Check Google Search Console's Sitemaps and News reports after any future
`news:` submission attempt — expect a rejection or "not eligible" status given the current
content type and publishing cadence, confirming this recommendation.

---

## 9. Sitemap Structure Recommendation if Scaling to Many Consulate/City Pages

**Current state:** A single flat `sitemap.xml` (14 URLs) is correct and sufficient today — no
index file is needed at this scale, and none currently exists (`sitemap_index.xml` and
`sitemap-index.xml` both 404, confirmed via automated discovery).

**Forward recommendation, to implement *before* URL count becomes unwieldy (not urgent today,**
**but plan the pattern now given the location-page roadmap in Section 7):**

- Split into a **sitemap index** (`sitemap_index.xml` at the root, referencing child sitemaps)
  once the combined URL count starts approaching a few hundred to a few thousand URLs, or
  earlier for operational clarity even before hitting the 50k technical cap. Practical trigger:
  when location pages alone would push the single file past ~500 URLs, or as soon as location
  pages are versioned/updated on a different cadence than the rest of the site.
- Suggested child sitemap split by content type/update cadence, which also makes the `lastmod`
  problem in Section 4 easier to fix correctly (each generator only needs to track change dates
  for its own content type):
  - `sitemap-core.xml` — homepage, services hub, how-it-works, about, contact, legal pages
    (low change frequency)
  - `sitemap-locations.xml` — all `/services/us-visa-appointment-*/` consulate/city pages
    (this is the set that will grow fastest and is the one to watch against the 30/50-page
    quality gates in Section 7)
  - `sitemap-blog.xml` — blog posts (highest change frequency, easiest to keep `lastmod`
    accurate since CMS posts typically have real `updated_at` fields)
- Each child sitemap stays under the 50,000 URL / 50MB caps independently; the index file
  simply lists child sitemap locations and their own `lastmod`.
- This structure also gives Search Console per-sitemap coverage stats broken out by content
  type — directly useful for monitoring the location-page rollout's indexation health without
  it being diluted by the rest of the site's URLs.

**Severity:** Info (proactive infrastructure recommendation, not a current defect).
**Fix:** Build the index + child-sitemap generator now as part of whatever pipeline will
generate the new consulate/city pages, so the split happens automatically as pages are added
rather than as a manual migration later.
**Falsifiability:** At any future audit, check whether `sitemap.xml` URL count exceeds ~500
before an index+child structure exists — if so, this recommendation was under-actioned; if
child sitemaps exist and each stays under the technical caps with content-type-appropriate
`lastmod` values, this recommendation was correctly implemented.

---

## Summary Table

| # | Check | Status | Severity |
|---|---|---|---|
| 1 | XML validity | Pass | Info |
| 2 | Size/URL-count limits | Pass (14 URLs, 2.7KB) | Info |
| 3 | 200 + self-canonical + indexable, all 14 URLs | Pass | Info |
| 4 | `lastmod` accuracy | Fail — uniform, mismatches server headers | Low-Medium |
| 5 | `changefreq`/`priority` present | Ignored by Google, harmless | Info |
| 6a | `/for-agents/` "gap" | False positive — correctly excluded (308 redirect) | Info |
| 6b | 3 unlaunched location pages linked but 404 | Not a sitemap gap; broken internal links | Low |
| 6c | Other coverage gaps | None found | Info |
| 7 | Location-page quality gates | Not triggered yet (2 pages); high scaling risk flagged | Medium (pre-emptive) |
| 8 | Image/news sitemap | Not warranted | Info |
| 9 | Sitemap index structure | Not needed yet; plan now for location-page rollout | Info |

## Top Issues (ranked)
1. **[Medium, pre-emptive] Location-page scaling risk** — infrastructure (linking component,
   robots.txt rules, blog priming) already points to imminent multi-city rollout; adopt the
   60%-unique-content rule and 50-page hard-stop justification gate before Dubai/UAE/Australia
   pages launch, not after.
2. **[Low-Medium] Uniform, server-mismatched `lastmod`** — all 14 URLs claim `2026-08-07` while
   live server `Last-Modified` headers show `2026-08-11`; fix by sourcing `lastmod` from actual
   CMS content-update timestamps or omit the tag.
3. **[Low] Three internal links to 404 location pages** — `/services/us-visa-appointment-{dubai,uae,australia}/` are linked site-wide but return 404 (correctly excluded from sitemap and blocked via robots.txt, but still a live broken-link/crawl-budget item).
4. **[Info]** `priority`/`changefreq` present but ignored by Google — optional cleanup only, no measurable impact either way.
