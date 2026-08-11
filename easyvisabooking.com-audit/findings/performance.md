# Performance / Core Web Vitals — easyvisabooking.com

Audit date: 2026-08-11
Method: PageSpeed Insights v5 (Lighthouse 13.x, lab data) for 5 URLs × 2 strategies (10 runs) + CrUX History API (field data attempt) + preload/render-blocking audit + direct `curl` header/timing verification.

## Headline: Lab data only — CrUX field data is UNAVAILABLE

`crux_history.py` on the origin returned:
```
"error": "No CrUX history data for this origin. Insufficient Chrome traffic volume for eligibility."
```
Every one of the 10 PSI runs also returned an **empty `field_metrics: {}`** at the page level. This is consistent with the site's real-world exposure: 382 impressions / 9 clicks over 90 days per GSC (see CONTEXT.md). CrUX requires a minimum rolling-28-day sample of real Chrome users per origin/URL before it publishes data; this site does not have enough traffic to qualify.

**Consequence: Google's actual Core Web Vitals ranking assessment (which uses only field/CrUX data at the 75th percentile) cannot currently be measured for this site, and — more importantly — CrUX cannot be evaluating it as a ranking signal either, because Google itself has no field sample to score.** Everything below is Lighthouse **lab data**: a single simulated run under fixed network/CPU throttling, useful for diagnosing bottlenecks but NOT the number Google uses for ranking. Do not treat any figure below as a field/CrUX value.

**Prioritization call:** given zero field data and near-zero traffic/clicks, Core Web Vitals is currently a **weak lever** for this site relative to its real constraints — indexation, topical authority/trust, and backlinks (see other audit categories). Fixing the lab-flagged issues below is still worthwhile (they are real, measurable waste and will matter once traffic grows and CrUX starts populating), but they should not be prioritized over indexation/content/links issues in the overall audit ranking.

## Lab Metrics Summary (Lighthouse via PSI, single run each)

| Page | Strategy | Perf Score | LCP | TBT (INP lab proxy*) | CLS | FCP | Speed Index |
|---|---|---|---|---|---|---|---|
| Home (/) | Mobile | 62 | 7.2 s | 70 ms | 0 | 4.6 s | 6.1 s |
| Home (/) | Desktop | 71 | 1.3 s | 50 ms | **1.039** | 0.8 s | 1.3 s |
| /services/ | Mobile | 62 | 7.3 s | 90 ms | 0 | 4.3 s | 6.1 s |
| /services/ | Desktop | 65 | 1.9 s | **540 ms** | 0.011 | 0.7 s | 1.9 s |
| /services/us-visa-appointment-canada/ | Mobile | 58 | **11.7 s** | 120 ms | 0 | 4.8 s | 7.5 s |
| /services/us-visa-appointment-canada/ | Desktop | 89 | 2.0 s | 50 ms | 0.062 | 0.7 s | 1.3 s |
| /blog/us-visa-appointment-canada-guide-2026/ | Mobile | 60 | **11.7 s** | 120 ms | 0 | 4.3 s | 6.5 s |
| /blog/us-visa-appointment-canada-guide-2026/ | Desktop | 69 | 1.9 s | 100 ms | **0.501** | 0.7 s | 1.1 s |
| /contact/ | Mobile | 61 | 7.6 s | 120 ms | 0 | 4.3 s | 6.0 s |
| /contact/ | Desktop | 94 | 1.5 s | 80 ms | 0.01 | 0.7 s | 1.0 s |

\* PSI/Lighthouse lab runs do **not** measure INP — INP is a field-only metric derived from real user interactions. **Total Blocking Time (TBT)** is reported here as the standard lab proxy for interactivity risk; it is not on the same scale as INP and the ≤200ms INP threshold does not apply directly to TBT. Treat TBT as a directional signal only. True INP requires CrUX field data, which is unavailable (see above).

**Mobile average Performance score: ~60.6/100. Desktop average: ~77.6/100.** Because Google indexes and ranks mobile-first, the mobile figures are the more representative signal. Headline lab score: **60/100 (mobile)**.

### Against current CWV thresholds (LCP ≤2.5s good, INP ≤200ms good, CLS ≤0.1 good) — lab LCP/CLS only, no INP available:
- **LCP: FAILS "good" on mobile for all 5 pages** (7.2s–11.7s, all in "Poor," >4.0s). Desktop LCP passes "good" on all 5 pages (1.3s–2.0s).
- **CLS: passes on mobile** (0 across all 5 pages tested). **Desktop CLS fails on Home (1.039, Poor) and the blog guide (0.501, Poor)**; other desktop pages pass.
- **INP: cannot be assessed** — no field data exists to compute it.

## Finding 1 — Oversized, unoptimized hero/breadcrumb images driving mobile LCP failure
**Severity: Critical**
**Evidence:**
- `/blog/us-visa-appointment-canada-guide-2026/img/canada-visa-hero-banner.png` — **869,160 bytes**, Lighthouse computes **820,740 bytes (94%) as wasted** (image-delivery-insight audit). This page has the worst mobile LCP measured: **11.7s**.
- `/services/us-visa-appointment-canada/img/breadcrumb.png` — **421,412 bytes**, **132,031 bytes (31%) wasted**. Reused on the Canada service page (also 11.7s mobile LCP) and the blog guide page.
- Home `/img/carousel-1.jpg` — 120,535 bytes, 23,276 bytes (19%) wasted.
- On the Canada service page (mobile), images account for **1,328,065 of 1,986,324 total transfer bytes — 67% of the entire page weight**, for a page whose primary user value is a short informational/booking flow.
- All hero/breadcrumb images are **PNG or JPG — zero WebP/AVIF usage detected** anywhere in the sampled resource summaries.
**Fix:** Convert `canada-visa-hero-banner.png` and `breadcrumb.png` to compressed WebP or AVIF (target <150KB and <80KB respectively at delivered dimensions), serve via `<picture>` with responsive `srcset`/`sizes` so mobile doesn't download desktop-resolution assets, and re-encode `carousel-1.jpg` at a modern format with quality ~75-80.
**Expected impact:** Largest single lever available — these three images alone account for ~980KB of avoidable transfer on the two worst-performing pages and are the direct cause of the 7.2s-11.7s mobile LCP figures.
**Falsifiability:** Re-run `pagespeed_check.py` mobile on the same URLs after re-encoding; LCP display value and the `image-delivery-insight` wastedBytes figure should drop close to zero. If LCP does not improve substantially, the LCP element or discovery path (Finding 2) is the actual bottleneck, not image weight.

## Finding 2 — LCP image not discoverable/preloaded (compounds Finding 1)
**Severity: High**
**Evidence:** The `lcp-discovery-insight` audit **fails on every page tested** ("Optimize LCP by making the LCP image discoverable from the HTML immediately, and avoiding lazy-loading"). `preload_check.py` on the homepage confirms: `"lcp_resource_hints": {"preload_lcp_candidate": false, "fetchpriority_high": 0}`, overall preload score **50/100**.
**Fix:** Add `fetchpriority="high"` to the LCP hero/carousel `<img>` tag on each page, remove any `loading="lazy"` on that specific element, and add `<link rel="preload" as="image" href="...">` in `<head>` for the LCP image on each template.
**Expected impact:** Typically shaves several hundred ms to low seconds off LCP by starting the download during HTML parsing instead of after CSSOM/JS execution — meaningful on mobile where the current gap between FCP (4.3-4.8s) and LCP (7.2-11.7s) is 2.5-6.9s, most of which is the browser discovering and then downloading the oversized image late.
**Falsifiability:** Check `lcp-discovery-insight` passes and `fetchpriority_high` count >0 in a follow-up `preload_check.py` run.

## Finding 3 — Desktop CLS spikes to Poor on Home (1.039) and Blog (0.501)
**Severity: High**
**Evidence:** Lighthouse's `layout-shifts` diagnostic attributes the overwhelming majority of the shift to the `<body>` element itself: Home desktop shows a body-level shift score of **1.0** (of 1.039 total); Blog desktop shows a body-level shift score of **0.484** (of 0.501 total). Home's diagnostics also surfaced a full-viewport `<div id="spinner" class="bg-white position-fixed ... w-100 vh-100 ...">` overlay element in the DOM — a fixed-position loading spinner covering the whole viewport is a plausible cause of a near-1.0 shift score when it is removed after load. Mobile CLS on the same URLs is 0, so this is either a desktop-viewport-specific timing artifact or a real bug that only manifests at desktop viewport width/timing.
**Fix:** Manually verify in Chrome DevTools Performance panel (desktop viewport) whether the `#spinner` overlay or a late web-font swap is the trigger. If it's the spinner: ensure it is removed via CSS `visibility`/`opacity` transition rather than DOM removal/display toggling that triggers reflow of trailing content, or position it as an overlay with `position: fixed` and no impact on document flow. If it's a font swap, see Finding 5.
**Expected impact:** Uncertain until root-caused — but a 1.0 desktop CLS score is unusually large for typical Lighthouse noise and warrants a targeted look; a fix would move desktop CLS solidly into "Good" on both flagged pages.
**Falsifiability:** Re-run PSI desktop after isolating and removing/fixing the spinner; if CLS does not drop, look at the second- and third-ranked shift contributors (font/webfont swap) instead.

## Finding 4 — Third-party script cost: Google Tag Manager/gtag.js is the dominant cost; Ahrefs analytics is negligible
**Severity: Medium (GTM) / Info (Ahrefs)**
**Evidence** (from `third-parties-insight` and `bootup-time` audits):

| Entity | Page/Strategy sampled | Transfer size | Main-thread time |
|---|---|---|---|
| Google Tag Manager (gtag.js, G-3MTBDM446M) | Home mobile | 189,568 B | 144.9 ms |
| Google Tag Manager (gtag.js) | Services desktop | 189,570 B | **656.0 ms** |
| Google Fonts | Home mobile | 143,895 B | 0 ms |
| Google Fonts | Services desktop | 72,707 B | 0 ms |
| FontAwesome CDN | Services desktop | 169,997 B | 0 ms |
| Google CDN (jQuery/ajax.googleapis.com) | Home mobile | 32,115 B | 16.2 ms |
| JSDelivr CDN | Home mobile | 33,319 B | 10.9 ms |
| **ahrefs.com (analytics)** | Home mobile | **3,664 B** | **4.3 ms** |

On `/services/` desktop, `bootup-time` attributes **667.9 ms total JS execution** to `googletagmanager.com/gtag/js?id=G-3MTBDM446M` (311.9ms parse/compile + 348.4ms scripting) — the single largest script cost on any page tested — and `long-tasks` shows two discrete long tasks from that same script (400ms and 224ms), which directly explains the 540ms TBT outlier on that page/strategy.

Ahrefs analytics, by contrast, costs **3.7KB transfer and ~4ms main-thread time** across the entire sample — effectively negligible. It is not a meaningful optimization target.
**Fix:** Load `gtag.js` with `async` (verify it already is — if not, add it), or migrate to server-side GTM/Measurement Protocol if analytics granularity requirements allow, or defer GTM initialization until after first interaction using a facade/consent-gate pattern. Do not spend effort optimizing the ahrefs snippet — the cost/benefit isn't there.
**Expected impact:** Directly addresses the 540ms TBT outlier on `/services/` desktop; more broadly reduces main-thread contention that will matter for INP once real-user (field) interaction data exists.
**Falsifiability:** Re-run `bootup-time`/`long-tasks` audits post-change; gtag.js scripting time and its long-task count should drop. If TBT doesn't improve, the long tasks have shifted to another script (check `long-tasks` again for the new top contributor).

## Finding 5 — Render-blocking CSS and FOIT web fonts
**Severity: Medium**
**Evidence:**
- `render-blocking-insight` (Home): `css/style.css`, 5,211 bytes, **219ms wasted** — the only render-blocking resource found, small in bytes but still delays first paint by parsing before it can start.
- `font-display-insight` (Home): FontAwesome `fa-solid-900.woff2` wastes **380ms**, `fa-brands-400.woff2` wastes **235ms** — indicates these fonts lack `font-display: swap` (or equivalent), causing FOIT (flash of invisible text) while they block.
- FontAwesome alone is **169,997 bytes** transferred (Services desktop) for what is typically a handful of icons — a full icon-font kit for a small icon set is disproportionate.
**Fix:** Add `font-display: swap` to all `@font-face` declarations (Google Fonts and FontAwesome), preload the woff2 files actually used above the fold, and replace the FontAwesome kit with inline SVG icons or a subsetted icon font containing only the icons actually used on the page (likely a handful — nav/social/contact icons).
**Expected impact:** Removes the render-blocking 219ms CSS delay and the 380ms+235ms FOIT windows; subsetting FontAwesome could cut ~150KB+ from every page load.
**Falsifiability:** Re-run and confirm `render-blocking-insight` and `font-display-insight` no longer appear in `failed_audits`.

## Finding 6 — TTFB is genuinely strong (Vercel edge cache confirmed, not assumed)
**Severity: Info / Pass**
**Evidence:** Verified directly rather than assumed:
```
curl -D - https://www.easyvisabooking.com/
X-Vercel-Cache: HIT
Age: 40463
Server: Vercel
curl -w "TTFB: %{time_starttransfer}s  Total: %{time_total}s"
TTFB: 0.222s   Total: 0.317s
```
Lighthouse's `server-response-time` audit independently reports the response as "short" (1-3ms measured from Google's test infrastructure, which is likely co-located near the Vercel edge). Both measurements are well under the 800ms LCP-subpart TTFB target and the legacy 200ms TTFB guidance.
**Conclusion:** TTFB is **not** a bottleneck for this site. The static-HTML-on-Vercel-with-cache-HIT architecture is doing its job. The LCP problem (Finding 1) is entirely in resource load delay/duration and render delay, not server response.
**Note:** `lcp_subparts.py`, which would formally break LCP into TTFB/load-delay/load-time/render-delay percentages, depends on the CrUX API and returned the same 404 as `crux_history.py` for the same reason (insufficient field traffic) — so a field-verified subpart breakdown isn't available. The curl+Lighthouse evidence above substitutes for it directionally: TTFB is fast; the remaining ~4-9 seconds of mobile LCP time is resource load delay/duration (large unoptimized images, Finding 1) and element render delay (missing fetchpriority/preload, Finding 2).

## Finding 7 — Logo image should be SVG, not PNG
**Severity: Low**
**Evidence:** `/img/brand-logo-real.PNG` is 6,911 bytes for a 54×45px rendered logo, with Lighthouse flagging 6,296-6,710 bytes (91-97%) as wasted across multiple pages.
**Fix:** Replace with an SVG (typically <2KB for a simple logo) or a properly-sized WebP.
**Expected impact:** Minor in isolation (~6KB/page) but appears on every page template, so it's a small compounding fix, not a priority item.
**Falsifiability:** Confirm `image-delivery-insight` no longer lists the logo after the swap.

## What is NOT a problem (avoid over-fixing)
- **TTFB** — confirmed fast (Finding 6). Do not spend effort here.
- **Ahrefs analytics script** — 3.7KB/4ms, immaterial (Finding 4). Do not spend effort here.
- **Mobile CLS** — 0 across all 5 pages tested. No action needed.
- **Desktop LCP** — passes "good" (1.3s-2.0s) on all 5 pages. The LCP problem is mobile-specific.
- **Best Practices score**: 100/100 on every page sampled (from `lighthouse_scores`). No findings there.

## Data Gaps / Falsifiability Notes
- **CrUX field data (origin + all 5 pages): unavailable.** Confirmed via `crux_history.py` (404, "Insufficient Chrome traffic volume for eligibility") and empty `field_metrics: {}` on every PSI page response. This is expected and consistent with the 382-impression/90-day GSC volume documented in CONTEXT.md. Re-check once organic traffic grows — CrUX needs a rolling 28-day sample before it will populate.
- **`lcp_subparts.py`**: failed for the same CrUX-dependency reason; substituted with curl timing + Lighthouse `server-response-time` (Finding 6).
- **INP**: cannot be measured at all today (lab tools don't produce it, field data doesn't exist). TBT was reported as the closest lab proxy, with the caveat stated in the metrics table footnote.
- All Lighthouse figures are **single-run lab measurements**, not averaged — normal run-to-run variance of low double-digit percent should be expected on LCP/TBT if re-tested.
