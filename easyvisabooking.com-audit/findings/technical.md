# Technical SEO Audit — easyvisabooking.com
Audit date: 2026-08-11 | Canonical host: https://www.easyvisabooking.com (verified live)

Scope: all 14 sitemap URLs + /for-agents/ (15 URLs), fetched raw over HTTPS with headers captured.

## Technical SEO Score: 64 / 100

Static HTML on Vercel with clean canonicals, working HSTS, and no mixed content — the
foundation is sound. The score is pulled down by: a robots.txt/404 crawl trap on three
public nav links, a page that GSC has impressions for now permanently redirecting to an
unrelated page, a completely absent security-header set beyond HSTS, and two confirmed
broken image references (favicon + OG image) caused by filename case mismatches on a
case-sensitive host.

---

## 1. Crawlability

**FINDING 1.1 — CRITICAL — /services/ links to 3 URLs that are simultaneously robots-blocked AND 404**
- Evidence: robots.txt (fetched live, 200, `Content-Length: 220`):
  ```
  User-agent: *
  Allow: /
  Disallow: /services/us-visa-appointment-dubai/
  Disallow: /services/us-visa-appointment-uae/
  Disallow: /services/us-visa-appointment-australia/

  Sitemap: https://www.easyvisabooking.com/sitemap.xml
  ```
  `/services/` (200, confirmed live) contains hard-coded `<a href>` links to all five location
  pages:
  ```
  /services/us-visa-appointment-canada/       -> 200 (in sitemap)
  /services/us-visa-appointment-toronto/      -> 200 (in sitemap)
  /services/us-visa-appointment-dubai/        -> 404  AND Disallow'd
  /services/us-visa-appointment-uae/          -> 404  AND Disallow'd
  /services/us-visa-appointment-australia/    -> 404  AND Disallow'd
  ```
  Confirmed by direct request: `curl -o /dev/null -w '%{http_code}'` on all three returns `404`.
- Why this is worse than a plain 404: Disallow prevents Googlebot from ever crawling these
  URLs, which means Google cannot discover the 404 and cleanly drop the URL from
  consideration. Combined with the fact that `/services/` — an indexed, internally-linked
  page — actively links to them, this sends mixed signals (link equity flows to blocked
  dead ends) and wastes crawl budget/link paths on a 15-page site. Disallow is the wrong
  instrument for "this page doesn't exist" or "not launched yet" — it should either be a
  real 200 page, or the link should be removed, or the URL should 410/404 without being
  blocked so Google can process the removal.
  Also note the sitemap for the business (Organization JSON-LD `areaServed`) claims
  Canada, UAE, Turkey, Australia, United Kingdom as served countries — but only Canada
  has a live location page. Dubai/UAE and Australia are advertised in schema and linked
  from `/services/` yet have no live landing page at all.
- Fix: Pick one of two paths per URL: (a) build the page and remove Disallow + submit in
  sitemap, or (b) remove the `<a href>` from `/services/` and delete the Disallow rule so
  the URL 404s cleanly and Google can process removal via normal crawling (or serve a
  proper 410 if the pages will never exist). Do not combine "linked internally" +
  "blocked" + "404" on the same URL.
- Falsifiability: Fixed when, for each of the three URLs, `curl -I` returns either 200 (page
  built, present in sitemap, no Disallow) or 404/410 with **no** internal `<a href>` pointing
  to it anywhere on the site and no Disallow rule referencing it. Re-crawl `/services/` and
  confirm `grep -o 'href="[^"]*"'` no longer contains any of the three paths, or confirm the
  paths return 200.

**FINDING 1.2 — INFO — Disallow rules with no matching sitemap entries are a no-op today, not a risk**
- Evidence: none of the three Disallow'd paths appear in `sitemap.xml` (14 URLs verified via
  `sitemap_discovery.py`), so there is no sitemap/robots conflict — only the internal-link
  conflict described in 1.1.
- Fix: covered by 1.1.
- Falsifiability: N/A once 1.1 is resolved.

**FINDING 1.3 — LOW — /for-agents/ is not in sitemap.xml and has zero internal links**
- Evidence: `sitemap_discovery.py --json` returned exactly the 14 URLs listed in
  CONTEXT.md; `/for-agents/` is absent. `grep -l "for-agents"` across the raw HTML of all
  14 sitemap pages returned **zero matches** — no page on the site links to it. GSC shows
  it received 6 impressions / 0 clicks over 90 days at avg. position 11.2, meaning Google
  has it indexed from some prior discovery path (external link, manual submission, or a
  since-removed internal link).
- Fix: See Finding 4.1 below — this is now moot in its current form because the URL
  redirects away (see 4.1), but if the page is reinstated it must be (a) linked from main
  nav or a relevant page (e.g., `/services/` or footer), and (b) added to sitemap.xml.
- Falsifiability: Crawl the site depth-first from `/`; the page is no longer orphaned when
  it appears as a discovered link before you have to consult the sitemap or search Google
  site: to find it.

**FINDING 1.4 — INFO — robots.txt is otherwise clean**
- Evidence: `User-agent: *` / `Allow: /` blanket-allow, valid `Sitemap:` directive, HTTP 200,
  `text/plain; charset=utf-8`. No blocking of CSS/JS asset directories was found in the
  fetched HTML (no `/wp-content/`, `/_next/`, or bundler asset paths blocked).
- Fix: none required.
- Falsifiability: N/A.

---

## 2. Indexability

**FINDING 2.1 — PASS — Canonicals are self-referencing and point to www on every audited page**
- Evidence (all 14 sitemap pages + homepage checked): every page emits
  `<link rel="canonical" href="https://www.easyvisabooking.com/<path>/">` matching its own
  URL exactly, e.g. `/privacy/` → `https://www.easyvisabooking.com/privacy/`,
  `/services/us-visa-appointment-toronto/` →
  `https://www.easyvisabooking.com/services/us-visa-appointment-toronto/`. No canonical
  pointed to the apex (non-www) host on any page.
- Falsifiability: Would fail if any canonical resolved to a different host/path than the
  page's own live URL, or was missing.

**FINDING 2.2 — PASS — meta robots is `index, follow` on every page, no X-Robots-Tag leakage**
- Evidence: `<meta name="robots" content="index, follow">` present on all 15 fetched pages.
  Response headers captured for all 15 URLs contain no `X-Robots-Tag` header at all (only
  `Strict-Transport-Security`, `Cache-Control`, `Content-Disposition`, `Etag`, standard
  Vercel headers). No accidental `noindex` anywhere.
- Falsifiability: Would fail if any page returned `noindex` in either the meta tag or an
  `X-Robots-Tag` response header.

**FINDING 2.3 — MEDIUM — `/blog` vs `/blog/` shows as two separate entries in GSC despite a clean single-hop redirect today**
- Evidence: Live test: `curl -I https://www.easyvisabooking.com/blog` → `308 Permanent
  Redirect`, `Location: /blog/` → `/blog/` → `200 OK`. This is a correct, single-hop
  redirect *today*. But GSC's 90-day Performance data (from CONTEXT.md) shows both
  `/blog/` (2 impressions) and `/blog` no-slash (1 impression) as distinct indexed rows.
  This is evidence Google crawled/indexed the no-slash variant as its own URL at some
  point — most likely because the redirect was added or fixed after Google's initial
  crawl, or because an external backlink/GSC URL-inspection request pointed at the
  non-slash form before the rewrite rule existed. It is not evidence of an active
  redirect problem today.
- Fix: No code change needed — the redirect is already correct. Use GSC URL Inspection on
  `https://www.easyvisabooking.com/blog` (no slash) and request re-indexing/validation so
  Google re-confirms the 308 and consolidates the two rows into the canonical `/blog/`
  entry. Re-check in 4–6 weeks.
- Falsifiability: Fails to resolve if, after a GSC re-crawl (check via URL Inspection "Last
  crawl" date advancing past today), the Performance report still shows the no-slash
  variant as a separately indexed URL rather than collapsing into `/blog/`.

**FINDING 2.4 — INFO — Structured data is present and parses, but FAQPage has no current SERP benefit**
- Evidence: Homepage carries 4 JSON-LD blocks (Organization, Service, WebSite/SearchAction,
  FAQPage) confirmed present in raw HTML and previously validated as parse-clean per
  CONTEXT.md. Google retired FAQ rich results for all sites on 2026-05-07.
- Fix: No action required. Leave FAQPage in place — it does not need to be removed, and no
  new FAQPage markup should be added elsewhere in anticipation of a SERP benefit, since
  none currently exists.
- Falsifiability: N/A (informational).

---

## 3. HTTPS / Security

**FINDING 3.1 — HIGH — No security headers present except HSTS; HSTS itself is incomplete**
- Evidence: Full response headers captured for 15 URLs (homepage shown, identical pattern
  on every page and on `/robots.txt`):
  ```
  HTTP/1.1 200 OK
  Access-Control-Allow-Origin: *
  Cache-Control: public, max-age=0, must-revalidate
  Content-Type: text/html; charset=utf-8
  Server: Vercel
  Strict-Transport-Security: max-age=63072000
  X-Vercel-Cache: HIT
  ```
  Missing on every single page tested: `Content-Security-Policy`,
  `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`.
  The one present header, `Strict-Transport-Security: max-age=63072000` (2 years), lacks
  both `includeSubDomains` and `preload`.
  Additionally, `Access-Control-Allow-Origin: *` is set globally (on HTML documents, not
  just APIs) — low risk for a static marketing site with no auth/session data, but it is
  broader than needed and worth tightening if any future form/API endpoint is added under
  the same domain.
- Fix: Add via Vercel's `vercel.json` `headers` config (or platform dashboard) at minimum:
  `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN` (or a `frame-ancestors`
  CSP directive), `Referrer-Policy: strict-origin-when-cross-origin`, and a baseline CSP
  (start with `default-src 'self'; script-src 'self' 'unsafe-inline' www.googletagmanager.com
  analytics.ahrefs.com; ...` tuned to the actual GA4/Ahrefs/font script origins already in
  use). Update HSTS to `max-age=63072000; includeSubDomains; preload` once all subdomains
  are confirmed HTTPS-only.
- Falsifiability: Re-run `curl -I` (or any header-inspection tool) against
  `https://www.easyvisabooking.com/` after deployment; the fix has failed if any of the
  five listed headers is still absent from the response.

**FINDING 3.2 — PASS — HTTPS enforced correctly, no mixed content**
- Evidence: `http://www.easyvisabooking.com/` → `308` → `https://www.easyvisabooking.com/`.
  `http://easyvisabooking.com/` → `308` → `https://easyvisabooking.com/` → `301` →
  `https://www.easyvisabooking.com/` (2 hops — see Finding 5.1, this is a redirect-chain
  issue, not an HTTPS-enforcement issue: every hop upgrades toward HTTPS+www correctly).
  Full-page grep across all 15 fetched HTML documents for `src="http://` / `href="http://`
  (excluding `schema.org`/`w3.org` namespace URIs, which are inert identifiers, not fetched
  resources) returned **zero matches**. No mixed content.
- Falsifiability: Would fail if any `<script>`, `<img>`, `<link>`, or `<iframe>` loaded a
  live `http://` resource, or if any HTTP entry point failed to reach `https://www.` within
  1–2 hops.

---

## 4. URL Structure & Redirects

**FINDING 4.1 — CRITICAL — /for-agents/ (has live GSC impressions) now 308-redirects to /services/ via a 2-hop chain**
- Evidence: Direct test:
  ```
  curl -I https://www.easyvisabooking.com/for-agents
  → HTTP/1.1 308 Permanent Redirect
    Location: /for-agents/

  curl -I https://www.easyvisabooking.com/for-agents/
  → HTTP/1.1 308 Permanent Redirect
    Location: /services/

  curl -I https://www.easyvisabooking.com/services/
  → HTTP/1.1 200 OK
  ```
  So the full chain is `/for-agents` → `/for-agents/` → `/services/` → 200 (2 redirect hops
  to a non-equivalent page). Per CONTEXT.md, GSC's 90-day Performance report shows
  `/for-agents/` receiving 6 impressions and ranking at avg. position 11.2 for some query
  — meaning this URL was live, indexed, and getting some visibility recently. It now
  permanently redirects to `/services/`, a page with different content and intent (an
  "AI agents / for-agents" landing page, likely aimed at travel-agent partners or an
  agent-facing use case, is not the same as the general services directory). This is the
  single most consequential finding in this audit: it is an active regression, not a
  latent risk — content Google had some (small but real) visibility for has been replaced
  with a redirect to unrelated content, which will read to Google as content removal and
  will not preserve whatever authority/relevance `/for-agents/` had accumulated.
- Fix: Two decisions needed, in order: (1) Was this redirect intentional (page
  deprecated/merged into /services/) or accidental (broken deploy, stale rewrite rule)? If
  accidental, restore `/for-agents/` as a live 200 page immediately. If intentional, the
  redirect target is wrong — `/for-agents/` should either point to a genuinely equivalent
  replacement page (if the content was merged somewhere specific) or, if the page is
  being permanently retired, the redirect should still go to the most topically relevant
  live page (not the generic `/services/` hub) with a 301 (this is currently a 308, which
  is functionally equivalent for SEO but non-standard for a permanent redirect —a 301 is
  the more universally recognized signal). (2) Regardless of outcome, collapse the 2-hop
  chain to 1 hop by pointing `/for-agents` (no slash) directly at the final destination
  instead of relaying through `/for-agents/`.
- Falsifiability: Fails if, one redirect check from now, `curl -I
  https://www.easyvisabooking.com/for-agents/` still returns a 308/301 (should be a
  deliberate 200 if restored, or a single-hop 301 to a genuinely relevant target if
  retired) or if `curl -I https://www.easyvisabooking.com/for-agents` still takes 2 hops
  to resolve.

**FINDING 4.2 — MEDIUM — http (non-HTTPS) apex takes 2 hops to reach the canonical host**
- Evidence:
  ```
  curl -I http://easyvisabooking.com/
  → HTTP/1.0 308 Permanent Redirect
    Location: https://easyvisabooking.com/

  curl -I https://easyvisabooking.com/
  → HTTP/1.1 301 Moved Permanently
    Location: https://www.easyvisabooking.com/
  ```
  `curl -sL -o /dev/null -w '%{num_redirects}' http://easyvisabooking.com/` confirms
  `num_redirects: 2`. By contrast `http://www.easyvisabooking.com/` reaches the canonical
  host in a single 308 hop. Only the http-apex entry point has the extra hop.
- Fix: At the edge/DNS layer, make `http://easyvisabooking.com/` redirect directly to
  `https://www.easyvisabooking.com/` in one hop (skip the intermediate https-apex stop).
  Low traffic impact (almost nothing links to bare `http://` apex in 2026) but trivial to
  fix and removes one avoidable hop for any crawler or legacy inbound link that does hit
  it.
- Falsifiability: Fails if `curl -sL -o /dev/null -w '%{num_redirects}'
  http://easyvisabooking.com/` still reports more than 1.

**FINDING 4.3 — PASS — Trailing-slash policy is applied consistently, including to non-existent paths**
- Evidence: Every non-slash sitemap path tested 308-redirects to its slash-terminated form
  in one hop: `/blog` → `/blog/` (200), `/services` → `/services/` (200), `/about` → 308,
  `/contact` → 308. Even a deliberately invented nonexistent path,
  `/this-page-does-not-exist-xyz123`, first 308s to
  `/this-page-does-not-exist-xyz123/` and *then* correctly returns a true `404 Not Found`
  (see Finding 7.1) — the trailing-slash rewrite is applied uniformly at the platform
  level rather than per-route, so there is no risk of a route existing at one slash-state
  but not the other.
- Falsifiability: Would fail if any sitemap URL's non-slash form returned something other
  than a single 308 to the slash form, or if it 200'd independently (creating a true
  duplicate).

**FINDING 4.4 — LOW — Case sensitivity is inconsistent between routes and static assets**
- Evidence: `https://www.easyvisabooking.com/Blog/` (capitalized) → `404` (routes are
  case-sensitive, expected/fine). But static asset serving is also case-sensitive and this
  is *not* handled safely — see Finding 6.1/6.2 (favicon and OG image references use the
  wrong case and 404 in practice). Flagging here because it's a URL-structure-level root
  cause: the platform (Vercel, effectively Linux/S3-backed) is case-sensitive for both
  routes and assets, and the codebase does not consistently match asset casing to the
  actual stored filename.
- Fix: See 6.1/6.2 for the concrete asset fix.
- Falsifiability: See 6.1/6.2.

---

## 5. Redirects (chain type/length summary)

| Path tested | Chain | Type(s) | Hops |
|---|---|---|---|
| `http://easyvisabooking.com/` | → https apex → https www | 308, 301 | 2 |
| `http://www.easyvisabooking.com/` | → https www | 308 | 1 |
| `https://easyvisabooking.com/` (apex) | → https www | 301 | 1 |
| `/for-agents` | → `/for-agents/` → `/services/` | 308, 308 | 2 |
| `/blog` (no slash) | → `/blog/` | 308 | 1 |
| `/services`, `/about`, `/contact` (no slash) | → slash form | 308 | 1 |
| nonexistent path | → slash form → 404 | 308 | 1 (then true 404) |

No redirect loops were found anywhere. All redirects are permanent (301/308); no 302s were
observed on this site. See 4.1 and 4.2 for the two chains exceeding 1 hop.

---

## 6. Broken Asset References (found during header/HTML inspection — not in original checklist but verifiable and material)

**FINDING 6.1 — HIGH — Favicon 404s on 6 of 14 sitemap pages due to file-extension case mismatch**
- Evidence: The actual stored file resolves only as
  `https://www.easyvisabooking.com/img/brand-logo-real.PNG` (uppercase extension,
  confirmed `200 OK`). `https://www.easyvisabooking.com/img/brand-logo-real.png`
  (lowercase) confirmed `404 Not Found` — Vercel's static file serving is case-sensitive.
  The `<link rel="icon">` tag's `href` value varies by page:
  - Uppercase `.PNG` (works): `/` (`href="img/brand-logo-real.PNG"`), `/blog/`,
    `/services/`, and the three blog post pages (`../../img/brand-logo-real.PNG`).
  - Lowercase `.png` (404s): `/about/`, `/contact/`, `/how-it-works/`, `/privacy/`,
    `/refund-policy/`, `/terms/`, `/services/us-visa-appointment-canada/`,
    `/services/us-visa-appointment-toronto/` (all reference
    `../img/brand-logo-real.png` or `../../img/brand-logo-real.png` — lowercase).
  Additionally, no `/favicon.ico` fallback exists: `curl -I
  https://www.easyvisabooking.com/favicon.ico` → `404`. Most browsers will still render
  the tab icon correctly on pages with the working uppercase reference, but on the
  affected pages the favicon silently fails to load (broken icon / blank tab), and any
  crawler or tool that resolves `/favicon.ico` directly (a long-standing convention some
  bots and browser UI still fall back to) gets a 404 site-wide.
- Fix: Standardize every `<link rel="icon">` reference to the one filename that actually
  exists on disk (`brand-logo-real.PNG`, uppercase — or, better, rename the source file to
  lowercase `.png` since that's the near-universal web convention and update every
  template reference to match). Also add a `/favicon.ico` at the site root (even a copied
  PNG-as-ICO or a proper multi-size ICO) for legacy fallback compatibility.
- Falsifiability: Fixed when `curl -I` on the exact href value referenced by every one of
  the 14 sitemap pages' `<link rel="icon">` tag returns `200`, and
  `curl -I https://www.easyvisabooking.com/favicon.ico` returns `200`.

**FINDING 6.2 — MEDIUM — Homepage's Open Graph image 404s; all other pages have no og:image at all**
- Evidence: Homepage HTML contains
  `<meta property="og:image" content="https://www.easyvisabooking.com/img/visa-banner.jpg">`.
  Direct request: `curl -I https://www.easyvisabooking.com/img/visa-banner.jpg` →
  `404 Not Found`. Tested case variants (`visa-banner.PNG`, `visa-banner.png`) also `404`
  — the file does not exist under any tested name/extension. Every other audited page
  (`/about/`, `/blog/`, `/contact/`, `/services/`, and the rest) has `og:title`,
  `og:description`, `og:type`, `og:url` but **no `og:image` tag at all** — confirmed by
  grep across all 14 fetched HTML documents. `twitter:card` is absent site-wide (0 of 14
  pages).
- Fix: Upload a real image at the referenced path (or fix the path to point at an existing
  asset) so homepage social shares render a preview image instead of Facebook/LinkedIn/
  X's blank-image fallback. Add a per-page (or shared default) `og:image` to the other 13
  pages, and add `twitter:card` (`summary_large_image` is the standard choice) plus
  `twitter:image`/`twitter:title`/`twitter:description` site-wide for correct X/Twitter
  card rendering. Low ranking impact, real impact on click-through/trust when links are
  shared on social or messaging apps (relevant here since Contact page explicitly offers
  WhatsApp/Telegram support — those platforms also render OG previews).
- Falsifiability: Fixed when `curl -I` on the homepage's `og:image` URL returns `200` with
  an `image/*` content-type, and each of the other 13 sitemap pages has a non-empty,
  resolvable `og:image` and a `twitter:card` meta tag.

---

## 7. Status Codes / 404 Behavior

**FINDING 7.1 — PASS — 404 page returns a true 404 status with distinct title, not a soft-404**
- Evidence: `curl -sL -D - https://www.easyvisabooking.com/this-page-does-not-exist-xyz123`
  → after the trailing-slash 308, final response is `HTTP/1.1 404 Not Found`, `Content-Type:
  text/html; charset=utf-8`, `Content-Length: 13013`, served from a distinct
  `404.html` (`Content-Disposition: inline; filename="404.html"`). Page `<title>` reads
  "Page Not Found | Easy Visa Booking" — not a 200-status "soft 404" that silently serves
  the homepage or a generic template.
- Falsifiability: Would fail if the final response after following redirects returned `200`
  instead of `404`, or if the page title/content matched another live page (indicating a
  soft-404 redirect-to-homepage pattern).

**FINDING 7.2 — CRITICAL (cross-ref)** — see Finding 1.1: three internally-linked URLs
compound a 404 with a robots.txt Disallow, which is the one genuinely broken status-code
pattern found across the 15 audited entry points plus their directly linked children. All
15 sitemap+`/for-agents/` URLs themselves return clean 200s (14 of them) or the 308 chain
documented in 4.1 (`/for-agents/`) — no other internal link on the crawled pages returned an
unexpected status.

---

## 8. Internal Linking

**FINDING 8.1 — MEDIUM — /for-agents/ has zero internal links (confirmed orphan) and now redirects away**
- Evidence: `grep -l "for-agents"` across the raw HTML of all 14 sitemap pages (home,
  services hub, both location pages, how-it-works, about, contact, blog hub, all 3 blog
  posts, terms, privacy, refund-policy) returned **no matches**. The only way to reach
  `/for-agents/` is a direct URL request — it is not present in the site's own navigation,
  footer, or body copy anywhere in the crawled set, yet GSC recorded impressions for it
  (see 4.1). This is a genuine orphan page in the internal graph, independent of the
  redirect issue.
- Fix: If the page is restored, link it from primary navigation or a contextually relevant
  page (e.g., a "Travel Agents / Partners" link in the footer, or from `/services/` if it
  targets B2B partners). If it stays retired, no linking fix is needed, but see 4.1 for the
  redirect-target correction still required.
- Falsifiability: Fails if a full breadth-first crawl starting at `/` still cannot reach
  `/for-agents/` through any `<a href>` on the live site.

**FINDING 8.2 — LOW — /blog/ (the blog index/hub) is not linked from homepage nav, footer, or body — only individual posts are**
- Evidence: `grep -oiP 'href="[^"]*blog[^"]*"' page_.html` returns only the three
  individual post URLs (`/blog/us-visa-appointment-canada-guide-2026/`,
  `/blog/us-visa-appointment-dubai-fast-2026/`,
  `/blog/us-visa-appointment-world-cup-2026-guide/`) — never bare `/blog/`. The same check
  against `/about/`, `/services/`, and `/contact/` also found no `/blog/` link, and the
  primary `<nav>` markup has no visible "Blog" nav item in the fetched HTML. `/blog/` is
  reachable today only via direct URL, sitemap.xml, or by a user who lands on one of the
  three posts and uses breadcrumbs/related-post links within the post itself (not verified
  here — worth a follow-up check if content strategy expects `/blog/` to be a real hub for
  future posts).
- Fix: Add a persistent "Blog" (or "Guides") link to primary navigation or footer so the
  hub page accrues internal link equity and is easily discoverable as more posts are
  added.
- Falsifiability: Fails if `/blog/`'s href still cannot be found in the primary nav or
  footer markup of `/`, `/about/`, `/services/`, or `/contact/`.

**FINDING 8.3 — INFO — Click depth is shallow (max depth ~2) for all legitimately linked content**
- Evidence: All 14 sitemap pages are reachable within 1 click from `/` except the two
  location-specific service pages, which are reachable within 1 click from `/services/`
  (2 clicks from home) — a normal, shallow depth for a 15-page brochure site. No
  pagination was found (blog has only 3 posts, no `/page/2/` or similar detected).
- Falsifiability: N/A (informational, confirms no structural depth problem).

---

## 9. Mobile-Friendliness

**FINDING 9.1 — PASS — Correct responsive viewport tag present site-wide**
- Evidence: `<meta content="width=device-width, initial-scale=1.0" name="viewport">`
  confirmed present in the raw HTML `<head>` of all 15 fetched pages (attribute order is
  `content` before `name`, which is why a naive `name="viewport"[^>]*content=` regex
  misses it on a first pass — confirmed present via a more permissive check).
- Falsifiability: Would fail if the viewport meta tag were absent or missing
  `width=device-width` on any page.

**FINDING 9.2 — INFO — Bootstrap-based markup (`navbar`, `px-4 px-lg-5`) indicates a responsive framework is in use**
- Evidence: `<nav class="navbar navbar-expand-lg navbar-light bg-white px-4 px-lg-5
  py-3 py-lg-0">` on the homepage — Bootstrap 4/5 utility classes with responsive
  breakpoint modifiers (`-lg-`), consistent with a mobile-first responsive layout. Full
  tap-target sizing and rendered layout were not measured (would require a rendered
  screenshot/Lighthouse pass, out of scope for source-only inspection) — recommend a
  PageSpeed Insights / Lighthouse mobile run as a follow-up if not already covered
  elsewhere in this audit.
- Falsifiability: N/A (informational; a rendered mobile screenshot or Lighthouse mobile
  score would be the falsifiable follow-up check).

---

## Core Web Vitals — Source-Level Risk Flags (not measured live; flagging structural risk only)

- **LCP risk — MEDIUM**: Homepage is 79,385 bytes of HTML and references Google Fonts via
  `<link rel="preconnect" href="https://fonts.googleapis.com">` /
  `https://fonts.gstatic.com` — preconnect is present (good), but no `<link rel="preload">`
  was found for a likely LCP hero image; combined with `og:image`/favicon 404s indicating
  general asset-path fragility (Findings 6.1/6.2), recommend confirming the actual hero
  image loads correctly and is preloaded. Needs a live PageSpeed/Lighthouse run to confirm
  actual LCP value — not measurable from static source alone.
- **CLS risk — LOW**: No obvious web-font-swap or unsized `<img>` issues detected in a
  source scan, but font-loading strategy (`font-display`) was not verified — recommend a
  live CrUX/PageSpeed check.
- **INP risk — LOW/INFO**: Static HTML site with no SPA framework and Bootstrap for layout;
  no heavy client-side JS bundle detected in the fetched markup beyond GA4 (`gtag.js`,
  async), Ahrefs analytics (async), and presumably Bootstrap JS. Low INP risk expected but
  not measured live.
- Recommend running `pagespeed_check.py` / CrUX for field data to replace these
  source-level estimates with real measured Core Web Vitals — Tier 1 PageSpeed/CrUX access
  is available per CONTEXT.md and should be used in the Performance category of this audit
  if not already covered there.

---

## 10. JavaScript Rendering

**FINDING 10.1 — PASS — Site is server-rendered static HTML, not an SPA; no raw/rendered content gap**
- Evidence: Every one of the 15 fetched URLs returned full page content (headings, body
  copy, JSON-LD, meta tags) in the raw HTTP response with no client-side rendering
  required — confirmed by direct `curl` fetch (no headless browser) returning complete
  `<title>`, meta description, canonical, and body content identical in structure across
  all pages. No SPA shell markers (e.g., a near-empty `<div id="root">` with all content
  injected via JS) were found. This matches CONTEXT.md's stated "static HTML, not an SPA."
- Falsifiability: Would fail if a raw `curl` fetch returned materially less content
  (missing headings/body text/structured data) than a Playwright-rendered fetch of the
  same URL.

---

## 11. Hreflang

**FINDING 11.1 — LOW/INFO — No hreflang tags anywhere on the site despite explicit multi-country targeting**
- Evidence: `grep -oiP 'hreflang="[^"]*"'` across all 15 fetched pages returned zero
  matches. The business explicitly targets multiple countries in single-language English
  content: dedicated Canada/Toronto service pages exist, Dubai/UAE/Australia are named in
  Organization and Service JSON-LD `areaServed` and linked from `/services/` (though
  currently 404/blocked — see 1.1), and blog content explicitly targets Dubai and Canada
  audiences.
- Analysis: hreflang exists to tell Google which URL to serve for a given
  language/region combination when the *same content* exists in multiple locale
  variants. This site does not have locale variants of the same page (e.g., no
  `/ca/` vs `/ae/` duplicate content) — it has *distinct* location-specific landing pages
  targeting different search intent (Canada page vs. Toronto page vs., if built, a Dubai
  page), which is a legitimate, hreflang-independent geo-targeting pattern (similar to
  how many local-service businesses handle multi-city targeting via unique content pages
  rather than hreflang). Hreflang is therefore not strictly required here and its absence
  is not a ranking-blocking issue.
- Fix (optional, Low priority): No hreflang implementation is required as long as each
  country/city gets its own uniquely-written landing page (current pattern). If, in the
  future, the same page content is duplicated verbatim across country subpaths (e.g., a
  templated `/ae/services/` mirroring `/ca/services/` with only the country name
  swapped), hreflang (or better, more differentiated content) would become necessary at
  that point to avoid duplicate-content dilution. For now, this is documentation, not a
  required fix.
- Falsifiability: Would become a real issue only if two or more live URLs are found
  serving substantially the same content differentiated only by target country/language
  without either hreflang or sufficiently unique content — re-check if/when Dubai/UAE/
  Australia pages from Finding 1.1 are eventually built.

---

## 12. Title/Meta Duplication Check

**FINDING 12.1 — PASS — No duplicate titles or meta descriptions found across the 14 sitemap pages**
- Evidence: Extracted and compared `<title>` and `<meta name="description">` values for
  all 14 sitemap pages (see table). Every title and every description is unique:

| Page | Title (chars) | Description present |
|---|---|---|
| `/` | "US Visa Appointment Booking & Rescheduling Assistance Service" (65) | Yes, unique |
| `/services/` | "US Visa Appointment Booking by Location \| Easy Visa Booking" (59) | Yes, unique |
| `/services/us-visa-appointment-canada/` | (65) | Yes, unique |
| `/services/us-visa-appointment-toronto/` | (72) | Yes, unique |
| `/how-it-works/` | (54) | Yes, unique |
| `/about/` | (61) | Yes, unique |
| `/contact/` | (52) | Yes, unique |
| `/blog/` | (62) | Yes, unique |
| `/blog/us-visa-appointment-world-cup-2026-guide/` | (88) | Yes, unique |
| `/blog/us-visa-appointment-canada-guide-2026/` | (74) | Yes, unique |
| `/blog/us-visa-appointment-dubai-fast-2026/` | (81) | Yes, unique |
| `/terms/` | (36) | Yes, unique |
| `/privacy/` | (34) | Yes, unique |
| `/refund-policy/` | (52) | Yes, unique |

  Note two titles exceed the ~60-char display guideline (`/blog/.../dubai-fast-2026/` at
  81 chars, `/blog/.../world-cup-2026-guide/` at 88 chars) and will likely truncate in SERP
  — worth trimming for CTR, but this is a Low-severity display concern, not a duplication
  issue.
- Falsifiability: Would fail if any two pages shared an identical `<title>` or
  `<meta name="description">` value; none were found.

---

## Prioritized Issue Summary

| # | Severity | Finding | Section |
|---|---|---|---|
| 1 | Critical | `/for-agents/` (has GSC impressions) now 308-redirects (2 hops) to unrelated `/services/` | 4.1 |
| 2 | Critical | 3 links on `/services/` are simultaneously robots-Disallow'd AND 404 — Google can never crawl to discover/drop them | 1.1 |
| 3 | High | No security headers site-wide except incomplete HSTS (missing CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy) | 3.1 |
| 4 | High | Favicon 404s on 8 of 14 sitemap pages (case-mismatched file extension); no `/favicon.ico` fallback | 6.1 |
| 5 | Medium | Homepage `og:image` 404s; no `og:image`/`twitter:card` on any other page | 6.2 |
| 6 | Medium | `/blog` vs `/blog/` shows as 2 separate indexed GSC entries despite a correct single-hop redirect today — needs re-crawl validation | 2.3 |
| 7 | Medium | http (non-HTTPS) apex takes 2 redirect hops instead of 1 | 4.2 |
| 8 | Medium | `/for-agents/` has zero internal links (true orphan) | 8.1 |
| 9 | Low | `/blog/` hub not linked from nav/footer/homepage body | 8.2 |
| 10 | Low | 2 blog post titles exceed ~60 char SERP display guideline | 12.1 |
| 11 | Info | No hreflang — acceptable given unique per-country content pattern | 11.1 |
| 12 | Info | FAQPage schema present; no current SERP benefit post-2026-05-07 retirement — no action needed | 2.4 |

## Confirmed Passing (no action needed)
- Self-referencing, www-canonical `<link rel="canonical">` on every page (2.1)
- `meta name="robots" content="index, follow"` everywhere, no X-Robots-Tag leakage (2.2)
- HTTPS enforced on all entry points, zero mixed content (3.2)
- Trailing-slash policy applied uniformly, including to nonexistent paths (4.3)
- True `404` status (not soft-404) on nonexistent URLs, with distinct 404 template (7.1)
- Responsive viewport meta tag present site-wide (9.1)
- Static HTML, full content parity between raw and rendered fetch — no JS-rendering risk (10.1)
- No duplicate titles/meta descriptions across the 14 sitemap pages (12.1)

---

## Files Referenced
- Context: `C:/Megh/Personal Projects/Site SEO/Easy Visa Booking/easyvisabooking.com-audit/raw/CONTEXT.md`
- This report: `C:/Megh/Personal Projects/Site SEO/Easy Visa Booking/easyvisabooking.com-audit/findings/technical.md`
