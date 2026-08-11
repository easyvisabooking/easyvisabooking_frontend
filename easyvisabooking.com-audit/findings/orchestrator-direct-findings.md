# Orchestrator Direct Findings — easyvisabooking.com

Verified first-hand by the audit orchestrator on 2026-08-11 (not delegated).
Every item below was confirmed by direct HTTP request.

---

## CRITICAL — Broken service hub: 3 of 5 location links are 404 AND robots-blocked

**Evidence.** `/services/` (the location hub) contains these outbound links:

```
/services/us-visa-appointment-canada/     -> 200 OK
/services/us-visa-appointment-toronto/    -> 200 OK
/services/us-visa-appointment-dubai/      -> 404 Not Found
/services/us-visa-appointment-uae/        -> 404 Not Found
/services/us-visa-appointment-australia/  -> 404 Not Found
```

All three 404 URLs return `<title>Page Not Found | Easy Visa Booking</title>`.

Compounding this, `robots.txt` explicitly disallows the same three paths:

```
User-agent: *
Allow: /
Disallow: /services/us-visa-appointment-dubai/
Disallow: /services/us-visa-appointment-uae/
Disallow: /services/us-visa-appointment-australia/

Sitemap: https://www.easyvisabooking.com/sitemap.xml
```

And the `/services/` meta description actively advertises those destinations:

> "Browse US visa appointment booking services by country. We help applicants in
> Canada, Dubai, UAE, Australia and more secure faster visa slots."

**Why this is Critical.** Three failures compound on the single page whose entire
job is routing users to location services:

1. A user who clicks "Dubai" from the services hub hits a 404. In a category where
   users are already scanning for signs the operator is not legitimate, a dead link
   on the core service page is a direct conversion and trust loss.
2. Googlebot cannot even see the 404, because robots.txt blocks the path. Blocked
   URLs cannot return a status code to Google, so these will sit as
   "Indexed, though blocked by robots.txt" or as unresolved discovered URLs rather
   than being cleanly dropped. Robots.txt disallow is the wrong instrument for
   removing a page — it prevents Google from learning the page is gone.
3. The site markets Dubai/UAE/Australia in metadata and has a Dubai *blog post*
   ranking (`/blog/us-visa-appointment-dubai-fast-2026/`, 4 impressions, position
   33.8) with no service page to convert that intent into a booking.

**Fix (choose one path per location, do not mix):**

- *If the pages are coming soon:* remove the three `Disallow` lines from robots.txt,
  build the pages, return 200, and add them to `sitemap.xml`. This is the
  recommended path — Dubai already has ranking blog content to internally link into.
- *If the pages are abandoned:* remove the three links from `/services/`, remove the
  three `Disallow` lines from robots.txt (so Google can crawl and process them),
  and serve either a 410 Gone or a 301 to `/services/`. Then correct the `/services/`
  meta description so it stops advertising unavailable locations.

**Falsifiability check.** After the fix, request each of the three URLs and confirm
the intended status code (200 or 301/410, never 404-behind-a-disallow). In GSC Page
Indexing, confirm zero URLs remain under "Indexed, though blocked by robots.txt" and
that no `/services/*` URL sits in "Not found (404)". Re-crawl `/services/` and
confirm every outbound service link resolves 200.

**Leading indicator.** GSC "Discovered – currently not indexed" count for `/services/*`
should fall to zero within two crawl cycles.

---

## HIGH — Redirect chain on /for-agents

**Evidence.**
```
https://www.easyvisabooking.com/for-agents   -> 308 -> /for-agents/ -> 308 -> /services/ -> 200
https://www.easyvisabooking.com/for-agents/  -> 308 -> /services/ -> 200
```

The page still earns GSC impressions (6 impressions, average position 11.2 over 90
days), meaning Google has not finished reprocessing the redirect.

**Note on business impact.** Retiring `/for-agents/` removed the only page addressing
the B2B / travel-agent / corporate-mobility audience, and folded it into a `/services/`
page of only ~507 words that is not written for that audience. Position 11.2 on a
retired page suggests the B2B intent had traction worth preserving.

**Fix.** Collapse the chain so `/for-agents` redirects to `/services/` in a single
hop. Separately, decide deliberately whether the B2B audience deserves a real page
again rather than losing it by attrition.

**Falsifiability check.** `curl -sIL /for-agents` shows exactly one 308 before the
200. If `/for-agents/` impressions persist past ~60 days, Google has not consolidated
the signal and the redirect target may be considered a soft-404 mismatch.

---

## HIGH — Security headers almost entirely absent

**Evidence.** Full security-header response from `https://www.easyvisabooking.com/`:

```
Strict-Transport-Security: max-age=63072000
```

That is the only one present. Missing: `Content-Security-Policy`,
`X-Content-Type-Options`, `X-Frame-Options` (or CSP `frame-ancestors`),
`Referrer-Policy`, `Permissions-Policy`.

**Why it matters here specifically.** These are not direct ranking factors, and should
not be sold as such. They matter because this site handles passport numbers, personal
data, and payment intent in a scam-adjacent category. `X-Content-Type-Options: nosniff`
and a `frame-ancestors` policy are baseline defenses against clickjacking and MIME
confusion — meaningful for a site whose entire value proposition is "we are the
trustworthy operator." HSTS at 2 years is correctly configured; note it lacks
`includeSubDomains` and `preload`.

**Fix.** Add via `vercel.json` headers config:
```json
{ "headers": [{ "source": "/(.*)", "headers": [
  { "key": "X-Content-Type-Options", "value": "nosniff" },
  { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
  { "key": "X-Frame-Options", "value": "SAMEORIGIN" },
  { "key": "Permissions-Policy", "value": "geolocation=(), microphone=(), camera=()" }
]}]}
```
Add CSP only after auditing the third-party scripts (gtag.js, analytics.ahrefs.com) —
a careless CSP will break analytics.

**Falsifiability check.** `curl -sI` returns all five headers; securityheaders.com
grade improves from F/D to at least B; GA4 and Ahrefs analytics still record hits
after deployment (this is the check people skip and regret).

---

## HIGH — Google is working from a stale, smaller sitemap (10 URLs, not 14)

**Evidence.** GSC Sitemaps API for `sc-domain:easyvisabooking.com`:

```json
{
  "path": "https://www.easyvisabooking.com/sitemap.xml",
  "last_submitted": "2026-06-23T04:30:36.716Z",
  "is_pending": false,
  "warnings": "0",
  "errors": "0",
  "contents": [{ "type": "web", "submitted": "10" }]
}
```

The live sitemap contains **14 URLs**. Google's last processed copy contained **10**.
The sitemap's own `lastmod` values all claim **2026-08-07**, and the homepage
`Last-Modified` header reads **2026-08-11** — so the site has changed at least twice
since Google last took the sitemap on **2026-06-23**, roughly seven weeks ago.

**Interpretation.** Zero errors and zero warnings, so nothing is malformed — Google
simply has not re-fetched. Four URLs are therefore not being surfaced through the
sitemap discovery path at all. On a 14-page site with almost no inbound links,
the sitemap is a disproportionately important discovery channel, because there is
little external crawl demand pulling Googlebot through the site.

**Contributing cause worth noting.** Every URL carries an identical `lastmod` of
`2026-08-07`. Uniform, obviously-templated `lastmod` values are a known trigger for
Google discounting the field entirely — if every page claims to change on the same
day, the signal carries no information, and Google falls back to its own crawl
scheduling. That plausibly contributes to the seven-week gap.

**Fix.**
1. Resubmit `sitemap.xml` in GSC (Sitemaps → enter `sitemap.xml` → Submit) to force a re-fetch.
2. Make `lastmod` reflect each page's genuine last content-modification date, not a
   build timestamp applied uniformly. If the generator cannot do per-page dates
   accurately, it is better to omit `lastmod` than to publish uniform fake values.
3. Drop `priority` and `changefreq` — Google ignores both. Harmless, but they add
   noise and imply a control that does not exist.

**Falsifiability check.** After resubmission, GSC Sitemaps should report
`submitted: 14` and a `last_submitted` date after 2026-08-11. If it still reads 10
after 14 days, the sitemap is not being re-read and the cause is elsewhere (check
for a cached/stale CDN copy of `sitemap.xml` — the site is on Vercel with edge caching,
and `Cache-Control: public, max-age=0, must-revalidate` on HTML does not guarantee the
same policy on the XML).

**Leading indicator.** Watch the GSC Sitemaps "discovered URLs" count move from 10 → 14
without needing to re-run this audit.

---

## MEDIUM — No llms.txt (low priority, do not over-invest)

`https://www.easyvisabooking.com/llms.txt` returns **404**.

Stated honestly: llms.txt is **not used by Google**, and adoption by major AI engines
is unconfirmed. This is a cheap, optional addition with speculative benefit. It should
sit near the bottom of the backlog and must not displace trust/authority work, which
is the actual binding constraint on this domain.

---

## On-page inventory (verified)

All main pages return 200 with a **self-referencing canonical** to the www host, and
**all have meta descriptions** (present, specific, and well-written — a genuine
strength on this site).

| Page | Title len | Meta len | Raw words |
|---|---|---|---|
| / | 65 | 167 | ~2968 |
| /services/ | 59 | 142 | ~507 |
| /services/us-visa-appointment-canada/ | 65 | 181 | ~2795 |
| /services/us-visa-appointment-toronto/ | 72 | 216 | ~3573 |
| /how-it-works/ | 54 | 158 | ~1064 |
| /about/ | 61 | 165 | ~1201 |
| /contact/ | 52 | 187 | ~552 |
| /blog/ | 62 | 176 | ~735 |

(Word counts are raw HTML including markup; true body copy is lower.)

### LOW — Title truncation risk (>60 chars)
- `/services/us-visa-appointment-toronto/` — 72 chars
- `/` — 65 chars
- `/services/us-visa-appointment-canada/` — 65 chars

### LOW — Meta description truncation (>~160 chars rendered)
Toronto 216, Dubai blog 231, /contact/ 187, Canada service 181, /blog/ 176,
World Cup blog 174, /about/ 165, / 167.

These are not errors — Google rewrites descriptions often — but the front-loaded
value proposition should survive truncation. Toronto and the Dubai blog post lose
their differentiating clause ("Pay only on success", "why client satisfaction is
what separates good booking services from great ones") to the cut.

### MEDIUM — Incomplete social/Open Graph markup
Homepage has `og:title`, `og:type`, `og:url`, `og:image` but **no `og:description`**
and **no `twitter:card` / `twitter:title`**. Without `twitter:card`, links shared to
X/Twitter render without a rich preview; without `og:description`, platforms fall back
to arbitrary page text. For a service sold substantially through WhatsApp/Telegram
sharing (both listed as contact channels), link previews are a direct acquisition
surface.

**Falsifiability check.** Validate with a card validator; confirm a shared link to
WhatsApp/Telegram/X renders title, description, and image.

---

## Confirmed strengths (do not "fix" these)

- Apex correctly 301-redirects to www; canonical host is consistent.
- Every page carries a correct self-referencing canonical.
- Every page has a specific, human-written meta description. Many audited sites fail this.
- Static HTML, not an SPA — no JS-rendering dependency for indexing.
- Vercel edge cache (`X-Vercel-Cache: HIT`) — TTFB should be strong.
- Homepage JSON-LD: 4 blocks, all parse-valid.
- `sitemap.xml` is declared in robots.txt, returns 200, and is a valid urlset.
- HSTS present with a 2-year max-age.

---

## Note on the homepage FAQPage block

The homepage carries a valid `FAQPage` block (3778 bytes). Google **retired FAQ rich
results for all sites on 2026-05-07**, so this no longer produces a SERP feature.

Recorded at **Info** severity only. Do **not** remove it — it is harmless, it remains
valid structured data, and removal costs effort for no gain. Do not add new FAQPage
markup expecting Google SERP benefit, and do not assume a confirmed AI-citation
benefit, which is unproven.
