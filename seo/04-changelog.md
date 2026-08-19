# SEO Changelog

Running log of what shipped, what moved, and every new finding as it surfaces. Newest first.
Superseded reasoning is struck through, never deleted — the reasoning is worth more than the tidiness.

---

## 2026-08-19 — Mission Canada joins the $750 pilot: new post shipped same week, F1 corrected

**What happened.** On 2026-08-18 the State Department designated **Mission Canada** (Embassy Ottawa
and every US consulate in Canada) as a participating post in the nonimmigrant visa expedited
appointment pilot. It is the second mission ever designated, after Mission Mexico on 2026-07-22, and
the first with a visitor visa queue measured in years (Toronto 21 months as of 2026-06-18).

**Shipped.** `/blog/us-visa-paid-expedite-canada/` (queue item 6b, C3, 3,770 words), featured on the
hub, in the sitemap, and in the hub `Blog` JSON-LD. Three info-gain angles no competing page carried
on the day of writing:

- **Canadian citizens do not need a B-1/B-2 visa at all.** The Canadian queue is therefore almost
  entirely PRs, work and study permit holders and other foreign nationals resident in Canada. That
  reframes who the news is even for, and nothing else in the SERP said it.
- **The ~25,000 request cap is worldwide and shared**, not allocated per mission. Canada joined seven
  weeks into a capped pilot, with the deepest queues of the two participating missions.
- **The fly-to-Toronto plan does not work.** The country-of-residence guidance of 2025-09-06 (updated
  2025-10-10) plus a non-refundable $750 makes third-country expedite shopping an expensive mistake.

**F1 corrected, not left to rot.** `/blog/us-visa-expedited-appointment-750/` asserted in eleven
places that Mexico was the only participating mission. All of them now read Mexico *and* Canada, the
FAQ pair was rewritten on both sides (visible text and `FAQPage` schema kept word for word), the
`#not-in-mexico` section was retitled "What to do if the pilot is closed to you" with the anchor
preserved, `dateModified` moved to 2026-08-19, the official pilot page was added as source 1, and the
cover SVG was regenerated. Publishing 6b while F1 still said "you cannot pay this fee in Canada"
would have put the site in direct contradiction with itself on the same query.

**Cadence note.** Published on the day rather than spaced, and that is deliberate: this is the only
item in the queue with a government deadline attached (pilot ends 2026-12-31) and a designation that
is news for roughly a week. Queue item 13 ("Which Embassies Offer the $750 Expedited Interview?") is
now flagged to be folded into F1 rather than written as a third page on the same intent.

---

## 2026-08-13 — Held posts were reachable: scheduling hardened, guard added to CI

**Symptom.** URL Inspection on `/blog/reschedule-us-visa-appointment-earlier/` returned *"URL is not
available to Google — Excluded by 'noindex' tag."* Crawl allowed, fetch successful, canonical
self-referencing, `Indexing allowed? No`.

**Diagnosis: working as designed, designed wrong.** The post was a scheduled post held until
2026-08-19, so the `noindex` was correct. Nothing else on the site was affected — one `noindex` page
sitewide, sitemap clean at 14 self-canonical URLs, `robots.txt` blocking nothing, `blog/_template/`
already out of the deploy via `.vercelignore`. The automation was sound: dry-run against the due date
matched every anchor.

The design flaw was that the hold covered the post but not the **paths to** it. It was linked from
six live indexable pages — related-post cards and the footer "Popular Guides" column in the Canada,
Dubai, World Cup, $750 and legit posts, plus the hub — and listed in the hub's `Blog` JSON-LD
`blogPost[]`. So Googlebot followed a link, hit the `noindex`, and filed the URL as excluded. Benign
in itself, self-resolving on the publish date, and guaranteed to recur for **every** future scheduled
post.

**Fixed.** Published the post immediately (`--slug`, dated 2026-08-12) and hardened the mechanism:

- ~~Three markers~~ **five markers.** Added: every inbound link from a live page is held, and the
  post has no hub `blogPost[]` schema entry while held (the script now *inserts* that entry on
  publish, reading headline and image from the post's own `BlogPosting` schema).
- **`--hold <slug>`** applies marker 4 automatically. A related-post `<article class="post-card">` or
  a standalone footer anchor is wrapped in `<!-- SCHEDULED LINK date slug … -->`. A link *mid-sentence*
  is instead demoted to `<span data-scheduled-link="slug">`, keeping the visible text and dropping
  the URL — commenting that out would have eaten the prose. Both revert to live `<a>` on publish.
- **`--check`** strips comments and `<template data-scheduled>` blocks from every file `.vercelignore`
  does not exclude, then fails if a scheduled post's URL survives anywhere. Runs on every push via
  `.github/workflows/check-scheduled-holds.yml`. A held post can no longer reach production
  discoverable. The post's own canonical/`og:url`/self-link are exempt — they sit on the `noindex`
  page itself and are not a discovery path.

**Verified by round trip**, not by inspection: restored the pre-publish held state, ran
`--hold` → `--check` → publish, and diffed against the live site. All five linking pages came back
**byte-identical**, including the demoted inline link in the $750 post. Two bugs were caught this way
and fixed — a first cut at `--hold` matched bare `<article>` and commented out a 530-line post body,
and the publish path wrote the hub file twice, silently discarding its own link reveal.

Also pinned all script writes to LF. A publish run now rewrites every page linking to the post, and
Python's default would have flipped each to CRLF on a Windows run, turning a ten-line publish into a
whole-file diff.

**Standing rule:** a held post returns 200 with `noindex`, and that is safe *only* while nothing
crawlable points at it.

---

## 2026-08-13 — Competitor naming reworked + `.why-us` block added to every post

Owner decision, applied across all six posts and the template.

**Atlys removed entirely.** Every "All-in-one visa apps — e.g. Atlys" table row, the naming in
`is-us-visa-slot-booking-legit` prose, and the Atlys citation in the
`reschedule-us-visa-appointment-earlier` sources list. The category survives as **All-in-one visa
platforms** with no brand attached. The reschedule post's per-country claim still stands on the
RedBus2US source, which already covered it; no claim lost its evidence.

**Third parties are websites, never extensions.** CheckVisaSlots and VisaGrader are described as
slot-availability websites. Dropped with the extension framing: the Chrome Web Store citation, the
~80,000 users / 4.6 rating figures, and the "check what permissions it requests" advice in the
"Are free visa slot checking tools safe to use?" FAQ (rewritten in both the visible `<details>` and
the `FAQPage` schema, verified word-for-word identical across all 7 Q&As).

**Named competitors dropped from four posts to two.** They now appear only where the post is
genuinely about choosing between providers: `is-us-visa-slot-booking-legit` and
`reschedule-us-visa-appointment-earlier`. The Canada, Dubai, World Cup and $750 posts compare
*categories* only. Naming a competitor in a location guide bought us nothing and handed them the
brand impression on our page.

**New required block: `.why-us`.** A neutral comparison table left readers with five options and no
reason to pick ours. `.why-us` sits directly under every `.compare` and argues the case in 4-5
bullets, leading with the one structural difference: **every other row charges before the outcome,
ours charges $100 only after an earlier date is secured.** Then: we carry the work rather than
sending an alert; no portal password ever; terms, refund policy and privacy published before you
pay. Each block closes with `.why-us-foot` conceding the free row for readers who should not pay
anyone, which is what keeps the table above it credible.

Constraint-compliant by construction: arguments are about *our* model, never about how a named
company behaves. No guarantee, no success rate, no automation language. Constraint sweep is clean,
all hits are negative statements ("nobody can guarantee a date").

**New enforcement.** `blog/README.md` gains a competitor-naming sweep grep
(`atlys|chrome extension|browser extension|web store`) and a checklist line; `css/blog.css` gains
the `.why-us` rules in §9; `blog/_template/` carries the block with authoring rules inline.

---

## 2026-08-12 — Blog system rebuilt + first three queue posts

### Shipped — awaiting deploy verification

**A real blog system, not three orphan pages.** The blog was three hand-styled HTML files, each
carrying its own ~230-line `<style>` block, with no author, no dates, no categories, no related
posts and no way to add a fourth without copying 900 lines by hand.

- **`css/blog.css`** — every blog style in one place: hub grid, post typography, and 8 named
  reusable blocks (`.answer-box`, `.key-facts`, `.toc`, `.honesty`, `.compare`, `.cta-inline`,
  `.cta-end`, `.sources`, `.author-card`, `.related`). A §16 legacy shim maps the three old posts'
  class names onto the new design, scoped under `.blog-article` so it cannot leak into new posts.
- **`js/blog.js`** — reading progress, TOC scrollspy, hub category filter. Progressive enhancement
  only; every page is fully readable and fully crawlable with JS off.
- **`blog/_template/`** + **`blog/README.md`** — copy-a-folder authoring flow, 7-step publish
  checklist, the constraint-sweep grep, and the rule that the comparison block must never let us
  win every row. Both excluded in `.vercelignore` so the template cannot be indexed.
- **`/blog/` rebuilt** — featured post, card grid with covers/dates/read-time, five category filter
  chips, `Blog` + `blogPost[]` + `BreadcrumbList` schema.

**Categories are filter-only.** Five chips matching the `02-growth-plan.md` §3 clusters, filtering
static cards client-side. Deliberately **no** `/blog/category/*` URLs: thin category pages on a
domain with zero referring domains are a doorway-classification risk for no gain.

**H1 fixed on `/blog/`.** It read *"Visa Guides and Tips for **Agents**"* — a surviving agent-facing
framing that the v3.0.0 compliance pass missed because it was a heading, not a link or an offer. Now
"US Visa Appointment Guides". Flagged rather than fixed silently: this one was a live Stripe
exposure on an indexed page.

### Three posts published — F1, F4 and queue #3

| Post | Cluster | Information gain that no competing page states plainly |
|---|---|---|
| `/blog/us-visa-expedited-appointment-750/` | C3 | **The pilot is Mission Mexico only.** Every law-firm briefing describes the $750 mechanism accurately and then omits the fact that decides relevance: as of 2026-08-12 exactly one mission is designated (announced 2026-07-22). Also: 25,000-request cap, B-1/B-2 only, $935 all-in with the MRV fee |
| `/blog/is-us-visa-slot-booking-legit/` | C4 | **Seven checks, run publicly against ourselves** — including stating that we publish no testimonials and claim no success rate, and why |
| `/blog/reschedule-us-visa-appointment-earlier/` | C1 | **Per-country reschedule allowances**: India 1 since 2026-01-01 *(cut from 3)*, Philippines 3, Thailand 3, Japan 6, plus the ~48h lock and the 3-business-day margin |

Every post carries the comparison block naming **CheckVisaSlots**, **Atlys**, the **$750 government
expedite** and plain **DIY** alongside us, with the free options first and an explicit "if this is
you, do it yourself and keep your money" paragraph. Competitor pricing is **not** quoted — neither
publishes a stable public figure, so the table compares *models* and links out. Comparing models
rather than prices also means the tables do not go stale.

> **Superseded 2026-08-13.** Atlys is no longer named anywhere, third parties are described as
> websites only, and named competitors now appear in two posts rather than all six. See the
> 2026-08-13 entry.

### Legacy posts retrofitted — prose untouched

Canada, Dubai and World Cup keep their body copy verbatim per the `03-content-queue.md` hold and the
standing instruction not to convert their voice. What changed is the shell: byline + `Person`
author schema, `BlogPosting.image`, category chip, shared stylesheet, `table-scroll` wrappers,
comparison block, honesty callout, author card, related posts, `dateModified` 2026-08-12.

### Closes
- `01-fix-plan.md` §6.2 — author bylines. Zero existed sitewide; all 6 posts now carry a named
  `Person` author ✅
- `01-fix-plan.md` §4.3 — `BlogPosting.image` on all 6 posts ✅
- `03-content-queue.md` F1, F4 and #3 ✅ (3 of the 4 foundation pages; F2 wait-times and F3 pillar
  remain)

### Judgment calls worth flagging

- **Post covers are SVG, social images are raster.** The three new posts use hand-built SVG covers
  carrying the headline fact (~2KB each, sharp at any size, and unique — six posts sharing two stock
  photos was the alternative). `og:image` and `BlogPosting.image` stay on JPGs because no major
  social platform renders SVG previews. Documented in the `blog/README.md` checklist.
- **The reschedule allowances are sourced to RedBus2US, not a primary source.** No consulate
  publishes these numbers centrally. The post attributes them explicitly and tells the reader to
  trust the warning text in their own portal over the table. Left in because the information gain is
  the single strongest differentiator in Cluster 1 — but it is the most likely thing on the site to
  go stale without notice.
- **`/blog/` H1 no longer contains a keyword-stuffed phrase.** "US Visa Appointment Guides" targets
  the hub intent; the individual queries are owned by the posts. A hub competing with its own
  children was the existing Canada problem.

### Scheduled publishing — automated

The stagger is no longer a discipline anyone has to remember. All three posts merge together and
each is released on its own date by `.github/workflows/publish-scheduled-posts.yml`
(daily, 04:10 UTC / 09:40 IST):

| Post | Live | Note |
|---|---|---|
| `/blog/us-visa-expedited-appointment-750/` | 2026-08-12, on push | Has a deadline; every day of delay costs |
| `/blog/is-us-visa-slot-booking-legit/` | 2026-08-11, on push | **Was scheduled for the 15th.** Released early via `--slug`, which publishes immediately and dates the post *today* — hence 08-11 against F1's 08-12. Kept deliberately after review rather than reverted |
| `/blog/reschedule-us-visa-appointment-earlier/` | 2026-08-19 | Held; auto-releases |

So the first launch is two posts rather than one. Not harmful on a six-post blog, but it does spend
most of the stagger's value — attribution in GSC between F1 and F4 will be muddier, and a structural
mistake would already be in two posts rather than one. The remaining post keeps the full benefit.

**Note for next time:** `--slug` means *publish now, dated today*. To bring a scheduled post forward
to a specific date instead, edit `publishOn` in `blog/publish-queue.json` and let the daily job take
it.

**How a post is held.** ~~Three markers: `noindex, follow` on the page, the hub card inside an inert
`<template data-scheduled>`, and the sitemap `<url>` inside an XML comment.~~ Superseded 2026-08-13 —
those three hold the *post* but not the paths to it, so Google still found it through inbound links.
Five markers now; see the entry at the top of this log. On the due date
`scripts/publish_scheduled.py` stamps six date fields, releases the `noindex`, unwraps the template,
uncomments the sitemap entry, updates the hub schema's `datePublished`, moves the queue entry to
`published`, and pushes. Vercel deploys the push — no Vercel token in CI, nothing to configure there.

**Why `noindex` rather than excluding the files from the deploy.** The footer "Popular Guides"
column and the related-posts blocks link to all three posts from every blog page. Gating with
`.vercelignore` would have made two of those 404 sitewide for a week. `noindex, follow` keeps every
page returning 200 while keeping it out of the index — the correct mechanism for "written but not
published". Still correct; the mistake was leaving those links live, which is what the 2026-08-13
entry fixes. The links are now held too, so the page returns 200 for anyone with the URL while
nothing crawlable points at it.

**Design choices worth knowing**
- The script builds every edit in memory and writes nothing unless all of them succeed, so a partial
  failure leaves the repo untouched rather than half-published.
- Every replacement is anchored and asserts exactly one match. Markup drift fails loudly and names
  the anchor, instead of silently publishing something half-wired.
- It stamps the post's **scheduled** date, not the date the job happened to run. A job delayed by
  GitHub's scheduler still produces the intended date.
- **"Retrieved &lt;date&gt;" lines in the sources blocks are deliberately excluded** from the date
  stamping — they record when a source was actually checked and must not drift.
- Manual overrides exist: `--dry-run`, `--today YYYY-MM-DD`, `--slug <slug>`, plus a
  `workflow_dispatch` with the same two controls from the Actions tab.

Tested end-to-end locally against a real copy of the repo: dry runs at three dates, a live run
publishing both posts, verification of the resulting markup and schema, then restore. Verified that
the second post stays held while the first publishes — the `</template>` matching is scoped per
block, which was the first bug found and fixed.

`.github/` and `scripts/` are added to `.vercelignore`; they run against the repo, never in a browser.

### Still open
- **§3.1 real OG image** — the three new posts inherit the same generic `carousel-*.jpg` placeholder
  as everything else. The SVG covers now exist and are on-brand; a 1200×630 raster export of the
  same design would close §3.1 for the blog in one pass.
- **First scheduled run is unproven in CI.** The script is tested; the workflow is not, because it
  cannot run until it is on `main`. Run it once with `dry_run: true` from the Actions tab after
  merging, before 2026-08-15. If the repo has branch protection on `main`, the bot push will be
  rejected and the two posts will simply stay held — visible immediately in the Actions log.
- GSC submission after an automated publish is still manual; the workflow summary lists the URLs.

### ⏰ Verify after deploy
```
curl -sI https://www.easyvisabooking.com/blog/_template/            -> expect 404 (must not be live)
curl -s  https://www.easyvisabooking.com/blog/README.md             -> expect 404
Rich Results Test on all 3 new posts                                -> BlogPosting + FAQPage valid
```
Then submit the three new URLs in GSC and confirm the sitemap reports 17 rather than 14.

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
