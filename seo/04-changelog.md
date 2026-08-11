# SEO Changelog

Running log of what shipped, what moved, and every new finding as it surfaces. Newest first.
Superseded reasoning is struck through, never deleted — the reasoning is worth more than the tidiness.

---

## 2026-08-12 — Stage 3 (on-page) + Stage 1 leftover

### Shipped — awaiting deploy verification

All 15 HTML pages touched. Nothing here is verified live yet; see the verification block below.

**§3.2 — social cards sitewide.** `og:image`, `og:image:width/height`, `og:type`, `og:site_name`
and the full `twitter:*` set are now on all 14 indexable pages (404 deliberately excluded — it is
`noindex` and there is nothing to share). Before this, only `/` and `/services/` had any OG image at
all and only those two had a Twitter Card. Every link pasted into WhatsApp or Telegram from the
other 12 pages rendered as a bare grey box, which matters because those are the actual acquisition
channels.

**§3.3 — meta descriptions.** 11 pages were over the ~155-char render limit (worst: Toronto 212,
Dubai blog 231). All 14 now sit between 121 and 143. "Pay only on success" — the differentiating
clause that was being truncated away — is preserved in every commercial description.

**§3.4 — titles.** 7 pages were over 60 chars (worst: World Cup blog 88). All now ≤ 59.

**§3.5 — `/blog/` in nav and footer.** Added to the header nav (between Services and About) and to
the footer's first column on all 15 pages, with `active` state on the four blog pages. `/blog/`
previously had **zero** internal links sitewide despite being indexed, and is about to become the
primary growth engine at 8–10 posts/month.

**§1.5 — 410 Gone on the three dead location URLs.** New `api/gone.js` + three `rewrites` in
`vercel.json`. Needed a serverless function: `vercel.json` can express 3xx and rewrites but not a
410 status, and this is otherwise a fully static deploy. Reverting is deleting one file and three
rewrite entries; the URLs fall back to plain 404s.

### Closes
- `01-fix-plan.md` §1.5, §3.2, §3.3, §3.4, §3.5 ✅
- `01-fix-plan.md` §2.2 — closed as **not fixable**, see below

### ❌ §2.2 closed as not-fixable
`vercel.json` already redirects `/for-agents` → `/services/` directly, and the 2-hop chain persists
anyway. Verified live: Vercel applies `trailingSlash: true` normalization *before* config
`redirects`, so the platform emits the first 308 and our rule never sees the un-slashed path.
Collapsing it means dropping `trailingSlash`, which would restructure every canonical URL on the
site. Disproportionate. Google follows chains to 5 hops and the destination is a page whose
impressions we want to decay regardless.

Corollary worth knowing: every un-slashed `source` in `vercel.json` (`/office`, `/testimonial`,
`/contact`, …) is dead code for the same reason. Harmless, and live again if `trailingSlash` changes.

### ⏰ Verify after deploy
```
curl -sI https://www.easyvisabooking.com/services/us-visa-appointment-dubai/   -> expect 410
curl -sI https://www.easyvisabooking.com/services/us-visa-appointment-uae/     -> expect 410
curl -sI https://www.easyvisabooking.com/api/gone                              -> expect 410
```
The 410 is the only item here that can fail at deploy rather than at edit time — it introduces the
first serverless function on a project with no `package.json`. If the Vercel build errors or the
URLs still return 404, delete `api/gone.js` and its three rewrite entries and the previous 404
behaviour returns unchanged.

Then re-share one page per template in WhatsApp to confirm the card renders, and re-run the
title/description length check.

### Still open in Stage 3
- **§3.1 — a real OG image.** Every page now points at `img/carousel-1.jpg`: 1920×1080 (16:9, not
  the 1.91:1 OG ratio), generic stock, no logo, no proposition, identical across all 14 pages. The
  404 is fixed and previews render, but this is a placeholder standing in for a designed card.
- **§3.6 — deepen `/services/`** (460 words). Content work, merges into Stage 6.

### Judgment call worth flagging
The Canada blog guide and `/services/us-visa-appointment-canada/` had near-identical titles. Since
both had to be trimmed under §3.4 anyway, the rewrites were pointed at different intents — blog to
informational ("Wait Times & AIS Guide"), service page to commercial ("Get an Earlier Date") — which
is the first move of §6.3. **§6.3 is not closed**: the body copy still overlaps 65–75% and Stage 1
will unmask the cannibalization once the service pages get indexed.

---

## 2026-08-12

### Shipped and verified live
Commits `6aab71e` + `6e925f9` deployed. Verified against production:

```
Permissions-Policy, Referrer-Policy, X-Content-Type-Options, X-Frame-Options   now present
robots.txt                       no Disallow lines remain
sitemap.xml                      14 <loc>, zero lastmod/priority/changefreq
/favicon.ico                     404 -> 200 (rewrite to brand-logo-real.PNG)
brand-logo-real.png (lowercase)  0 references remain on any live page
og:image                         now /img/carousel-1.jpg (was a 404)
twitter:card                     summary_large_image now live
Organization.sameAs              placeholder gone, real Telegram channel live
```

**`.vercelignore` confirmed working** — `seo/`, the audit folder, and `README.md` all return 404
on the live domain while remaining in git. This was the load-bearing assumption behind committing
the audit at all, and it holds.

### Closes
- `01-fix-plan.md` §1.1 — sitemap resubmitted in GSC ✅
- `01-fix-plan.md` §1.2 — indexing requested for all 7 unknown URLs ✅
- `01-fix-plan.md` §1.3, §1.4, §1.6, §1.7, §2.1, §3.1, §3.2 (homepage + `/services/`), §4.1, §4.5 (partial)

### ⏰ Verification due 2026-08-26 (14 days)
Re-inspect the 7 URLs in GSC. Expected: coverage state moves off "URL is unknown to Google."
**If any are still unknown, the cause is not crawl scheduling** — check for a Vercel edge rule
serving different content to Googlebot:
`curl -A "Googlebot" https://www.easyvisabooking.com/services/` vs a normal fetch.
Also confirm GSC Sitemaps now reports `submitted: 14` rather than 10.

### New finding — missed on the first pass
`/services/` carried three visible **"Coming Soon" cards** for Dubai, UAE and Australia (body
content, not links — which is why the link-level greps did not surface them). With those pages
now permanently killed, "Coming Soon" was a false promise on a commercial page, in a category
where visitors actively scan for reasons to distrust the operator. Removed.

The "Don't See Your Location? We serve applicants worldwide" CTA directly beneath them already
handles global coverage honestly, and matches the geographic-scope decision in
`02-growth-plan.md` §4. Removing the cards also cuts into the ~1,200–1,500px of dead space the
audit flagged on this page.

Side effect: `/services/` is now **460 words**, down from 495. It was already thinner than both of
its own children (Canada 2,795w, Toronto 3,573w). This makes the rebuild in `01-fix-plan.md` §3.6
more urgent, not less — but publishing accurate thin content beats publishing inaccurate content.

---

## 2026-08-11

### Plans created
- Established `seo/` as the single home for SEO planning.
- `01-fix-plan.md` — 6-stage fix plan, 55 → ~78 projected, with per-category point attribution.
- `02-growth-plan.md` — 5-cluster keyword architecture, new pages, backlink workstream, measurement.
- `03-content-queue.md` — 28 posts across 3 months plus backlog, deduplicated against cannibalization.
- Moved `blog-topics-us-early-visa-appointment-date.pdf` → `seo/research/`.

### Decisions taken
- **Dead location pages: kill all three.** Dubai, UAE, Australia will not be built. 410 Gone,
  robots `Disallow` lines removed, meta descriptions corrected.
- **Trust items remain declined.** No legal entity details, no testimonials, no `tel:` link.
  Recorded as accepted risks costing ~6–8 points of the 100. Score ceiling is ~82–84, not 90+.
- **Audit's B2B/Agent recommendations rejected outright** (Phase 3.6 + the B2B content cluster) on
  Stripe underwriting grounds. Not deferred — rejected. Do not resurface.
- **Content: 8–10 posts/month**, written in-house, plus new pages.
- **Git: audit reports and plans are committed; screenshots and raw GSC exports are not.** A
  `.vercelignore` keeps the entire SEO folder out of the deployment, because the repo deploys as
  static files and anything committed would otherwise be publicly fetchable at the domain.

### New findings — not in the audit

- 🔥 **The State Department launched a $750 expedited-interview pilot on 2026-07-01**, running
  through 2026-12-31. B-1/B-2 applicants can secure an interview within ten business days at select
  posts. Six weeks old, SERP unsettled, hard deadline, exactly our customer's intent. Promoted to
  first position in the content queue as Cluster 3.
  *Source: travel.state.gov NIV expedited appointment pilot program; Ogletree 2026-06.*

- 📊 **The longest B1/B2 waits are no longer in Africa or South Asia — they are in Canada and
  Australia.** Toronto 14.5 months, Sydney 15 months, Vancouver 12.5 months. India 2–10 months,
  Brazil 6–12, many European posts within days. Counter-intuitive, therefore linkable, and the
  existing Canada/Toronto service pages sit directly on top of it.
  *Source: SERP research 2026-08-11; travel.state.gov global visa wait times.*

- ⚠️ **Excessive refreshing of the appointment portal triggers 24–72 hour temporary bans.** Almost
  nothing currently ranking states this plainly. It is the exact mistake customers make before
  finding us, so it is both genuine information gain and a natural service justification.

- 🎯 **Competitor set identified for the winnable clusters:** `visaslotwatch.com`,
  `visafortheunitedstates.com`, `beyondborderglobal.com`, `redbus2us.com`, `leso.co.in`, plus raw
  Reddit/Quora/Teamblind threads. These are ordinary content sites, not government portals —
  out-executable.

- 🚨 **The fraud in this niche is worse than assumed.** Documented: advance-fee theft, Telegram
  operators, blackmail using applicants' SSN and location data, and real visa-denial risk where
  appointments are hoarded. The US Embassy in India explicitly warns that no agent can guarantee a
  visa or a slot. Strengthens the case for leading with the existing "we cannot guarantee a date"
  and "pay only on success" language — with testimonials off the table, stated honesty is the
  substitute trust signal.

### Corrections to the audit

- **"`/services/` links to 3 pages that are 404" — stale.** All Dubai/UAE/Australia links are already
  commented out in the HTML across all 9 files, and live fetches of `/services/` and `/` confirm no
  crawlable link exists. Still real and still worth fixing: the 404s themselves, the robots
  `Disallow` lines, and the `/services/` meta description + keywords + `og:description`, which all
  still advertise the three dead locations.

- **Favicon casing confirmed, cause identified.** Git tracks `img/brand-logo-real.PNG` (uppercase).
  Live: `.PNG` → 200, `.png` → 404. It is invisible locally because the Windows checkout has
  `core.ignorecase=true`. Seven files reference the lowercase path. No `/favicon.ico` exists either.

- **The confirmation screenshots the audit called "available on request" do exist and are already
  published** — `img/canada-proof-1..5.jpg` and `img/toronto-proof-1..3.png`, live on the Canada and
  Toronto service pages. The problem is that **those are exactly the two pages Google has never
  crawled.** The site's strongest existing trust asset is invisible to search, which raises the
  priority of the indexation work rather than lowering it.

- **`/services/` measured at 495 words** (audit said ~507). Immaterial, but it is thinner than both
  of its own children and cannot carry hub duty either way.

### Verified live at time of writing
```
200  /sitemap.xml
200  /img/brand-logo-real.PNG
404  /img/brand-logo-real.png       ← 7 pages reference this
404  /favicon.ico
404  /img/visa-banner.jpg           ← homepage og:image
404  /services/us-visa-appointment-dubai/
404  /services/us-visa-appointment-uae/
404  /services/us-visa-appointment-australia/

Security headers: Strict-Transport-Security only. No CSP, X-Content-Type-Options,
X-Frame-Options, Referrer-Policy, or Permissions-Policy.
```

---

## Template for future entries

```
## YYYY-MM-DD

### Shipped
- What changed, which file, which plan item it closes.

### New findings
- Finding. Source. Which plan section it amends.

### Measurements
- GSC indexed count: N/14 · referring domains: N · avg position on target cluster: N
```
