# Google API Findings — easyvisabooking.com

Data source: Google Search Console API (URL Inspection, Search Analytics, Sitemaps), PageSpeed/CrUX History. Tier 1 credentials (service account `claude-skills@claude-skills-505118.iam.gserviceaccount.com`, siteFullUser on `sc-domain:easyvisabooking.com`). GA4 is NOT configured — see Gap section.

Freshness notes: GSC data has a 2–3 day lag (query data through 2026-08-08; today is 2026-08-11). URL Inspection reflects Google's *last crawl*, not live-site state — this matters below (/for-agents/).

Raw data: `easyvisabooking.com-audit/raw/gsc_url_inspection.json` (15 URLs, this agent's run), `raw/inspection.json` (14 sitemap URLs, coordinator's run — both agree), `raw/gsc_sitemaps.json`, `raw/crux_history.json`, `raw/gsc_query_page_90d.json`, `raw/gsc_country_device_90d.json`, `raw/gsc_trend_28d_vs_prior28d.json`.

---

## 1. URL Inspection — full per-URL table (14 sitemap URLs + /for-agents/)

| URL | Coverage state | Verdict | Last crawl | Crawled as | Robots.txt | Google canonical vs user canonical |
|---|---|---|---|---|---|---|
| `/` | Submitted and indexed | PASS | 2026-08-04 | MOBILE | ALLOWED | Match (self) |
| `/how-it-works/` | Submitted and indexed | PASS | 2026-06-28 | MOBILE | ALLOWED | Match (self) |
| `/contact/` | Submitted and indexed | PASS | 2026-06-25 | MOBILE | ALLOWED | Match (self) |
| `/blog/` | Submitted and indexed | PASS | 2026-07-26 | MOBILE | ALLOWED | Match (self) |
| `/blog/us-visa-appointment-world-cup-2026-guide/` | Submitted and indexed | PASS | 2026-07-29 | MOBILE | ALLOWED | Match (self) |
| `/blog/us-visa-appointment-canada-guide-2026/` | Submitted and indexed | PASS | 2026-07-20 | MOBILE | ALLOWED | Match (self) |
| `/blog/us-visa-appointment-dubai-fast-2026/` | Submitted and indexed | PASS | 2026-06-24 | MOBILE | ALLOWED | Match (self) |
| `/for-agents/` (not in sitemap) | Submitted and indexed | PASS | 2026-06-24 | MOBILE | ALLOWED | Match (self) — **stale, see finding G-2** |
| `/services/` | URL is unknown to Google | NEUTRAL | never crawled | — | unspecified | n/a |
| `/services/us-visa-appointment-canada/` | URL is unknown to Google | NEUTRAL | never crawled | — | unspecified | n/a |
| `/services/us-visa-appointment-toronto/` | URL is unknown to Google | NEUTRAL | never crawled | — | unspecified | n/a |
| `/about/` | URL is unknown to Google | NEUTRAL | never crawled | — | unspecified | n/a |
| `/terms/` | URL is unknown to Google | NEUTRAL | never crawled | — | unspecified | n/a |
| `/privacy/` | URL is unknown to Google | NEUTRAL | never crawled | — | unspecified | n/a |
| `/refund-policy/` | URL is unknown to Google | NEUTRAL | never crawled | — | unspecified | n/a |

Summary: **8 of 15 inspected URLs indexed, 7 unknown to Google, 0 failed, 0 canonical mismatches, 0 robots-blocked, 0 mobile-usability issues** (mobile-usability verdict came back `VERDICT_UNSPECIFIED` for every URL — Google retired the standalone Mobile-Friendly Test in Dec 2023, so an empty verdict is expected/normal here, not a data gap).

"URL is unknown to Google" (`coverage_state`) is a stronger negative signal than "Discovered — not indexed" or "Crawled — not indexed": it means these 7 URLs have **no record at all** in Google's URL database — not queued, not deprioritized, simply never seen. `robots_txt_state`, `indexing_state`, and `page_fetch_state` all return `*_UNSPECIFIED` for these because Google has nothing to report a state on.

---

## 2. Finding G-1 (Critical): The entire commercial/trust path is unindexed — and it is a crawl-demand + stale-sitemap problem, not a linking problem

**Evidence:**
- Unindexed: `/services/` (root service hub), both location service pages (`/services/us-visa-appointment-canada/`, `/services/us-visa-appointment-toronto/`), `/about/`, and all 3 policy pages (`/terms/`, `/privacy/`, `/refund-policy/`) — 7 of 8 non-blog pages on the site.
- Indexed: only `/`, `/how-it-works/`, `/contact/`, and blog content.
- The homepage — Google's own most-recently-crawled page (2026-08-04) — contains 8 links to `/services/`, 3 to `/about/`, 3 to `/refund-policy/`, 2 to `/terms/`, 1 to `/privacy/`, plus 2 each to the Canada and Toronto service pages. Despite that internal-link density, `/services/` still shows `referring_urls: []` and zero index footprint.
- Counter-evidence against "it's a linking problem": `/blog/` **is** indexed even though it has no homepage nav link (confirmed in DOM analysis) — a more weakly linked page got crawled and indexed while a heavily linked page (`/services/`) did not.
- Sitemap (GSC Sitemaps API, see G-3) still tells Google there are only 10 URLs on the site, last downloaded 2026-06-23, while the live sitemap.xml has 14. This is real: Google has not re-read the sitemap in ~7 weeks and may not even be aware some of these unindexed URLs are sitemap members.

**Diagnosis:** This is a **crawl budget / demand problem on a very low-authority, near-zero-traffic site**, compounded by a **stale sitemap submission**, not a discoverability/internal-linking defect. Google has already proven it can find and crawl `/services/` (it's linked 8x from a page Google visits regularly) — it is choosing not to prioritize crawling or indexing it, most plausibly because the site has almost no external signals (backlinks/traffic — see 90-day totals: 9 clicks, 382 impressions site-wide) to justify spending crawl budget on secondary pages. Adding more internal links will not fix this; the fix is (a) get Google to re-read the sitemap and (b) explicitly request indexing per page, while the underlying authority problem (near-zero backlinks/traffic) is addressed elsewhere in the audit.

**Business consequence:** Every page a prospective customer would need to convert (service description, location-specific service pages, trust/policy pages, about) is invisible in Google Search. Only the homepage, contact page, and blog content can currently drive any organic traffic. A visitor who searches a Canada- or Toronto-specific query cannot land directly on the matching service page from Google — only on the homepage or a blog post.

**Fix:**
1. Resubmit `sitemap.xml` in GSC (Sitemaps → remove and re-add, or ping `https://www.easyvisabooking.com/sitemap.xml`) to force Google to re-read the current 14-URL version.
2. Use GSC's UI "Request Indexing" (URL Inspection tool, one URL at a time — this is a manual UI action, not part of the read-only API surface exposed here) for the 7 unindexed URLs, prioritizing `/services/` and the 2 location pages first (highest commercial value).
3. Check/normalize `lastmod` values in sitemap.xml — if every URL carries an identical or missing `lastmod`, Google has less reason to trust it as a freshness signal; per-page accurate `lastmod` can improve re-crawl priority.
4. This is necessary but not sufficient — with 9 clicks and 382 impressions total over 90 days, the site's fundamental authority/backlink/traffic problem (covered elsewhere in this audit) is the deeper cause of low crawl demand and should be treated as the priority fix, not just as a corollary.

**Falsifiability check:** Re-run URL Inspection on these 7 URLs after resubmitting the sitemap and requesting indexing; if `coverage_state` moves to "Discovered — not indexed" or "Submitted and indexed" within 1-2 weeks, this diagnosis is confirmed. If they remain "unknown to Google" despite resubmission and manual indexing requests, the authority-deficit explanation strengthens further (Google is actively declining to index despite explicit requests).

---

## 3. Finding G-2 (High): `/for-agents/` has a stale, pre-redirect index entry

**Evidence:**
- URL Inspection (last crawl 2026-06-24): `/for-agents/` returns `coverage_state: "Submitted and indexed"`, `page_fetch_state: SUCCESSFUL`, self-canonical (`google_canonical == user_canonical == https://www.easyvisabooking.com/for-agents/`).
- Live HTTP check performed independently by this agent just now (2026-08-11):
  ```
  curl -I https://www.easyvisabooking.com/for-agents/
  HTTP/1.1 308 Permanent Redirect
  Location: /services/
  ```
- GSC query data confirms `/for-agents/` is still receiving impressions from live search results as recently as the last 28 days (2 impressions, position 28.0, 2026-07-12 to 2026-08-08) and 3 impressions in the prior 28-day window (position 2.3) — meaning Google is still actively surfacing this URL in the SERP using its stale, pre-redirect index record.
- `/for-agents/` is also confirmed absent from `sitemap.xml` (matches CONTEXT.md's known gap).

**Diagnosis:** Sometime between 2026-06-24 (last Google crawl) and 2026-08-11 (today), the page was changed from a live, self-canonical page to a 308 redirect to `/services/`. Google has not re-crawled it since, so its index still reflects the old content/canonical, and it is still being shown in search results pointing to a URL that immediately bounces visitors to `/services/`. This is not a canonical-tag mismatch (Google's crawl-time canonical *did* match the user declaration at the time) — it is simply an out-of-date crawl.

**Business consequence:** Any searcher who clicks a `/for-agents/` result gets redirected to `/services/`, which is itself unindexed and has essentially zero organic visibility per G-1 — so this traffic path currently leads into a page that Google doesn't otherwise send anyone to. It also means the "agents" audience segment (if intentional) has no addressable, indexed landing page at all right now.

**Fix:** Decide intent first: if `/for-agents/` should still exist as a distinct page, un-redirect it, add it to `sitemap.xml`, and request indexing. If the redirect to `/services/` is intentional (retiring the page), request re-indexing of `/for-agents/` via URL Inspection so Google picks up the 308 and consolidates signals into `/services/` — but note `/services/` itself is currently not indexed (G-1), so this redirect currently sends both users and equity into a black hole until G-1 is fixed.

**Falsifiability check:** Re-inspect `/for-agents/` after requesting indexing; `last_crawl_time` should advance past 2026-08-11 and `coverage_state`/canonical should reflect the 308 (i.e., Google should start treating `/services/` as canonical, or drop `/for-agents/` from the index if it treats the redirect as a removal signal).

---

## 4. Finding G-3 (Medium): Sitemap under-reports URL count and hasn't been re-read in ~7 weeks

**Evidence:** GSC Sitemaps API (`raw/gsc_sitemaps.json`):
```
path: https://www.easyvisabooking.com/sitemap.xml
last_submitted: 2026-06-23T04:30:36Z
is_pending: false | errors: 0 | warnings: 0
contents: [{type: web, submitted: 10}]
```
The live sitemap.xml (per CONTEXT.md) currently lists 14 URLs. Google's own record says 10. Zero errors/warnings means Google successfully read a version of the sitemap — just an outdated, smaller one.

**Diagnosis:** Either 4 URLs were added to the sitemap after 2026-06-23 and the change hasn't propagated, or Google simply hasn't re-fetched since then (sitemaps aren't always re-crawled automatically on a fixed schedule). No sitemap errors exist, so this is a freshness problem, not a validity problem.

**Fix:** Manually resubmit the sitemap in GSC (Sitemaps report → remove and re-add) to force an immediate re-read.

**Falsifiability check:** After resubmission, re-run `gsc_query.py sitemaps` — `last_submitted` should update to today's date and `contents[].submitted` should read 14.

---

## 5. Finding G-4 (Low/Info): robots.txt disallows 3 location-page URLs that don't exist (404)

**Evidence:**
```
User-agent: *
Allow: /
Disallow: /services/us-visa-appointment-dubai/
Disallow: /services/us-visa-appointment-uae/
Disallow: /services/us-visa-appointment-australia/
Sitemap: https://www.easyvisabooking.com/sitemap.xml
```
Independently verified via curl: all three disallowed URLs return `404`.

**Diagnosis:** These are not live, blocked pages (which would be a real problem) — they are either (a) placeholders reserved for future location-specific service pages that were never built, or (b) leftovers from removed pages. The business already has a Dubai-targeted blog post (`/blog/us-visa-appointment-dubai-fast-2026/`) and CONTEXT.md's business summary explicitly lists Dubai/UAE as a target market, but there is no dedicated `/services/us-visa-appointment-dubai/` landing page mirroring the Canada/Toronto pattern — this robots.txt entry is a breadcrumb suggesting that build-out was planned but not completed.

**Fix:** No urgent action (the disallow is currently inert since the URLs 404). If Dubai/UAE/Australia location pages are on the roadmap, build them to mirror `/services/us-visa-appointment-canada/` and `/services/us-visa-appointment-toronto/`, then remove the corresponding robots.txt disallow lines before launch (a disallow left in place on launch day would block them from being crawled).

**Falsifiability check:** Anyone can `curl -I` the three URLs and confirm 404 status; anyone can view `/robots.txt` directly to confirm the disallow lines.

---

## 6. Query-level data (90 days, `dimensions=query,page`, limit 200, 83 rows returned)

**Evidence:** 78 of the 83 query×page rows are attributed to a single page, `/blog/us-visa-appointment-canada-guide-2026/`, almost entirely long-tail Canada-visa-appointment variants at **positions 41–97, all with 0 clicks**. Two rows attach to `/` (branded/misc terms, positions 49–85, 0 clicks), one to `/contact/` (0 clicks), one to `/blog/us-visa-appointment-dubai-fast-2026/` (0 clicks).

**Critical honesty check on striking-distance queries flagged by the coordinator:** `/how-it-works/` (pos 4.0), `/services/` (pos 1.0), `/blog/` (pos 5.0), and `/for-agents/` (pos 11.2) from the page-level 90-day table **do not appear anywhere in the query×page breakdown** — meaning the individual queries driving those positions are below GSC's disclosure threshold (Google anonymizes queries with very low, privacy-sensitive impression counts) and are being aggregated into the page-level average from only 1–6 total impressions each.

**Diagnosis — these are NOT real striking-distance opportunities.** A "position 1.0" or "position 4.0" built from 1–4 impressions total over 90 days is not a stable ranking; it's a single ephemeral SERP appearance (e.g., a personalized/branded query, a low-competition long-tail phrase, or a one-off ranking fluctuation). This is further confirmed by the 28-day-window comparison (Section 7): `/services/` appears with 1 impression at position 1.0 in the *prior* 28-day window and **does not appear at all** in the most recent 28-day window — it isn't a persistent, improvable ranking, it's noise that already stopped recurring. Similarly `/how-it-works/` swung from position 2.5 (2 impressions, prior period) to position 6 (1 impression, latest period) — a volatility pattern consistent with near-zero sample size, not a genuine SERP position to optimize toward. Recommending CTR/content fixes on these based on position alone would be acting on statistical noise. Do not prioritize them.

The one real, non-noise pattern in the query data: `/blog/us-visa-appointment-canada-guide-2026/` is accumulating real query-level volume (dozens of distinct long-tail Canada-visa queries) but sitting at positions 41–97 — too far down to be "striking distance" (typically defined as positions 5–20); this page needs substantial ranking improvement (content depth, backlinks, on-page relevance), not a CTR/snippet fix.

---

## 7. Trend: last 28 days vs prior 28 days

| Period | Clicks | Impressions | CTR | Avg position |
|---|---|---|---|---|
| Prior 28d (2026-06-14 → 2026-07-11) | 3 | 92 | 3.26% | 44.4 |
| Last 28d (2026-07-12 → 2026-08-08) | 4 | 272 | 1.47% | 45.7 |
| Δ | +1 | +180 (+196%) | −1.79pp | −1.3 (slightly worse) |

**Evidence:** Nearly all impression growth (64 → 236, +269%) is concentrated in `/blog/us-visa-appointment-canada-guide-2026/`, ranking around position 50–53 for dozens of long-tail queries. Clicks grew only marginally (+1) while impressions nearly tripled, which mechanically drove CTR down — the site is being shown more often for queries it ranks too low on to actually get clicked.

**Diagnosis:** This is a page gaining topical/query breadth (Google is testing it against more query variants) without gaining rank. It is a leading indicator worth monitoring — if position improves on this page, the impression base is already there to convert into clicks — but is not yet a traffic win.

---

## 8. Geographic and device split (90 days)

| Country | Clicks | Impressions | CTR | Position |
|---|---|---|---|---|
| Canada (CAN) | 3 | 172 | 1.74% | 50.4 |
| USA | 1 | 71 | 1.41% | 53.9 |
| India (IND) | 3 | 20 | 15.0% | 15.1 |
| Vietnam (VNM) | 0 | 29 | 0% | 41.2 |
| Morocco (MAR) | 0 | 15 | 0% | 41.3 |
| Singapore, Turkey, +~25 others | ≤1 each | 1–9 each | mixed | mixed |

**Note on business fit:** CONTEXT.md describes the business as targeting Canada/UAE/worldwide. Canada dominates impressions (172/382 = 45%) as expected. UAE ("ARE") shows only 1 impression at position 81 over 90 days — essentially no visibility yet for the UAE market despite the Dubai blog post and business intent, consistent with G-4 (no dedicated UAE/Dubai service page exists to rank). India, oddly, has the best CTR (15%) and best position (15.1) of any country with meaningful volume — worth a closer look at what's driving that (could be a single high-intent branded query) but the volume (20 impressions) is too small to draw a strategic conclusion.

| Device | Clicks | Impressions | CTR | Position |
|---|---|---|---|---|
| Desktop | 5 | 354 (93%) | 1.41% | 47.1 |
| Mobile | 4 | 28 (7%) | 14.29% | 20.6 |

Desktop dominates impression share, but mobile has a much better average position and 10x the CTR — again on a very small sample (28 impressions), so directional only, not a basis for a device-specific strategy at this traffic level.

---

## 9. CrUX field data — unavailable

**Evidence:**
```
"error": "No CrUX history data for this origin. Insufficient Chrome traffic volume for eligibility."
```
CrUX requires a meaningful volume of real Chrome user sessions per origin (roughly on the order of thousands of qualifying page loads per 28-day period) before Google will publish aggregated field data. At 9 clicks/382 impressions over 90 days, easyvisabooking.com is far below that threshold. Report this plainly rather than substituting a misleading number — Core Web Vitals for this site should be evaluated from PSI **lab data** only (covered in whichever performance/CWV finding file owns that pull), not field data.

---

## 10. Indexing API — availability and correct scope (not used)

**Evidence:** `google_auth.py --check` reports Indexing API v3 is available under the same service account (`claude-skills@claude-skills-505118.iam.gserviceaccount.com`).

**Correct guidance:** Google's Indexing API is officially documented as supporting only pages marked up with `JobPosting` or `BroadcastEvent` structured data. easyvisabooking.com's pages carry `Organization`, `Service`/`Offer`, `WebSite`, and `FAQPage` structured data — none of which qualify. **Do not use the Indexing API to push indexing for `/services/`, `/about/`, the policy pages, or any other page on this site.** The correct mechanism for the unindexed pages is sitemap resubmission plus manual "Request Indexing" via the GSC UI (G-1/G-3), which this agent has not executed — only reported as available and appropriate.

---

## 11. Credential/data gaps

- **GA4: not configured.** `google_auth.py --check` returns `"ga4": {"available": false, "error": "Credentials found but no GA4 property ID configured. Set GA4_PROPERTY_ID or add 'ga4_property_id' to C:\\Users\\MEGH/.config/claude-seo/google-api.json"}`. Exact fix: add a `"ga4_property_id"` key (the GA4 property's numeric ID, e.g. from Admin → Property Settings for property tied to measurement ID G-3MTBDM446M per CONTEXT.md) to `~/.config/claude-seo/google-api.json`, then re-run `google_auth.py --check` to confirm tier upgrades to 2. Until then, organic-traffic-by-landing-page and conversion data cannot be cross-checked against GSC's click counts.
- Two URL Inspection runs exist for this audit: this agent's (`raw/gsc_url_inspection.json`, 15 URLs including `/for-agents/`) and the coordinator's (`raw/inspection.json`, 14 sitemap URLs). Both agree exactly on all 14 overlapping URLs (same coverage states, same last-crawl dates) — cross-validated, not a discrepancy.

---

## Severity summary

| ID | Finding | Severity |
|---|---|---|
| G-1 | 7 of 8 non-blog pages (entire commercial/trust path) unindexed; crawl-demand + stale-sitemap cause, not a linking defect | Critical |
| G-2 | `/for-agents/` indexed under stale pre-redirect state; live page now 308s to unindexed `/services/` | High |
| G-3 | Sitemap last read 2026-06-23, reports 10 URLs vs live 14 | Medium |
| G-4 | robots.txt disallows 3 non-existent Dubai/UAE/Australia service URLs (all 404, currently inert) | Low/Info |
| G-5 | "Striking-distance" positions on `/how-it-works/`, `/services/`, `/blog/`, `/for-agents/` are 1-6 impression noise, not real opportunities | Info (correction of a hypothesis) |
| G-6 | CrUX field data unavailable — insufficient Chrome traffic | Info |
| G-7 | GA4 not configured | Info/Gap |
