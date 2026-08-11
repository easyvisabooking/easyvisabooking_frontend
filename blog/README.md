# Blog System — how to add and manage posts

Internal document. Excluded from deployment via `.vercelignore`.

The blog is plain static HTML with no build step. Everything shared lives in two files, so a UI
change happens once and applies everywhere:

| File | What it holds |
|---|---|
| [`css/blog.css`](../css/blog.css) | All blog styling — hub grid, post typography, every reusable block |
| [`js/blog.js`](../js/blog.js) | Reading progress bar, TOC scrollspy, hub category filter. Progressive enhancement only |
| [`blog/_template/index.html`](_template/index.html) | Copy this to start a new post |
| [`blog/index.html`](index.html) | The hub. Cards are static HTML — add one per new post |

**Never** put post styling in a page-level `<style>` block again. If a post needs something new, add
a class to `css/blog.css` so every future post gets it.

---

## Publishing a post — the 7 steps

1. **Copy the template.**
   `blog/_template/` → `blog/<url-slug>/`, keeping the filename `index.html`.
   The slug *is* the URL. Make it the primary keyword, lowercase, hyphenated, no dates, no stop
   words: `reschedule-us-visa-appointment-earlier`, not `how-to-reschedule-your-us-visa-2026`.

2. **Replace every `{{PLACEHOLDER}}`.** Search the file for `{{` — none should remain. The list is
   at the top of the template.

3. **Write the body.** Required blocks are marked in the template; the quality gates are below.

4. **Add a card to the hub.** Open [`blog/index.html`](index.html) and:
   - Move the current featured post down into the grid (change `<article class="featured">` markup
     to a `.post-card`), and promote the new post to featured if it is the lead story.
   - Add the new post's `<article class="post-card" data-category="…">` block at the top of the grid.
   - Add a matching entry to the `blogPost` array in the **Blog schema** in the `<head>`.
   - If it belongs in the footer's "Popular Guides", swap it in there.

5. **Add the URL to [`sitemap.xml`](../sitemap.xml).**

6. **Update the SEO docs** (not deployed): mark the row ✅ in
   [`seo/03-content-queue.md`](../seo/03-content-queue.md) and add a line to
   [`seo/04-changelog.md`](../seo/04-changelog.md).

7. **Run the pre-publish checklist** below, then deploy and submit the URL in Google Search Console.

---

## Categories

Five, matching the content clusters in [`seo/02-growth-plan.md`](../seo/02-growth-plan.md) §3. Pick
exactly one per post. The `data-category` value drives the hub filter; the `cat-*` class drives the
chip colour; both must agree.

| Category | `data-category` | Chip class | Cluster |
|---|---|---|---|
| Rescheduling & Slots | `rescheduling` | `cat-rescheduling` | C1 |
| Wait Times by Country | `wait-times` | `cat-wait-times` | C2 |
| Expedite & Emergency | `expedite` | `cat-expedite` | C3 |
| Trust & Cost | `trust` | `cat-trust` | C4 |
| Application Basics | `basics` | `cat-basics` | C5 |

Categories are **filter-only** — they create no URLs. That is deliberate: thin category pages on a
low-authority domain are a liability, and client-side filtering gives the same UX with none of the
crawl cost.

---

## Reusable blocks

All defined in `css/blog.css`. Copy from the template or from any published post.

| Block | Class | Use |
|---|---|---|
| Answer-first box | `.answer-box` | **Required.** First thing after the cover. Answers the title question in ~60 words. This is what AI answer engines quote |
| Key facts | `.key-facts` | A `<dl>` of quotable figures. Use when the post carries hard numbers |
| Table of contents | `.toc` | **Required** on posts over ~1,500 words. Hand-authored `<ol>` of `#anchor` links |
| Honesty callout | `.honesty` | **Required.** At least one per post, and one near the end titled "What nobody can promise you" |
| Comparison table | `.compare` | **Required.** See below |
| Neutral note | `.note` | Freshness notes, caveats, "tell us if this is out of date" |
| Inline CTA | `.cta-inline` | One mid-article, contextual. Not a sales pitch — a pointer to the next useful thing |
| End CTA | `.cta-end` | **Required.** Last block before sources |
| FAQ | `.faq` + `<details class="faq-item">` | Native `<details>`, no JS. Must mirror the FAQPage schema **word for word** |
| Sources | `.sources` | **Required.** Numbered, linked, with retrieval dates |
| Author card | `.author-card` | **Required.** E-E-A-T |
| Related posts | `.related` | **Required.** Three cards, siblings and hub |

### The comparison block — non-negotiable

Every post carries one. It places Easy Visa Booking honestly alongside the alternatives the reader
is already weighing, so we appear in the same consideration set as the established players rather
than asking to be trusted in isolation.

Rules that keep it credible:

- **Always include the free options**, and say plainly when the reader does not need us. A table
  where we win every row is an advertisement and reads as one.
- **Name real alternatives** — CheckVisaSlots, Atlys, the $750 government expedite, plain DIY. Use
  the small-print pattern `e.g. CheckVisaSlots` under the category name.
- **Describe competitors factually and neutrally.** Public, verifiable facts only. Never allege
  wrongdoing by a named company. Never quote a competitor price we have not verified — compare
  *models*, and link out for pricing.
- **Our row** uses `class="is-us"` and the `.compare-us-tag` badge, and always states: from $100,
  paid only on success, no portal password, no guarantee.
- **Close with `.compare-foot`**: "named for comparison, not endorsement; no commercial
  relationship; verify pricing directly."

---

## Quality gates — every post clears all seven

From [`seo/02-growth-plan.md`](../seo/02-growth-plan.md) §5.

1. **Answer-first.** The title question answered inside the first 60 words, before any preamble.
2. **Named author with stated experience.** Byline, author card and `Person` schema.
3. **At least one thing no competitor says.** A real number, mechanic or timing pattern. If the post
   could have been written without reading anything, do not publish it.
4. **Every statistic sourced, linked, with a retrieval date.**
5. **Distinct primary keyword.** Check `seo/03-content-queue.md` first — three-way cannibalisation
   already exists on "US visa appointment Canada". Do not manufacture more.
6. **Internal links:** 2–3 to sibling posts, 1–2 to a commercial page (`/services/`,
   `/how-it-works/`), and the related-posts block.
7. **Constraint sweep passed** — below. This one is not optional.

---

## 🚨 Constraint sweep — run before every publish

Stripe reviews this website to underwrite the payment gateway. Two categories of language can cost
the payment account. See [`seo/02-growth-plan.md`](../seo/02-growth-plan.md) §5 and the root
`README.md` content guidelines.

**Banned when describing *our* service:**

- ❌ auto-book, bot, automation, script, algorithm, "24/7 monitoring", "checks every few seconds",
  "instant alerts", "grabs slots", any system acting on the government portal
- ❌ agent / travel agent / bulk / white-label / reseller offering of any kind
- ❌ any guarantee of a slot, a date, a timeframe or a visa outcome
- ❌ success-rate percentages or testimonials we cannot substantiate

**Allowed:**

- ✅ Explaining what **applicants** can do themselves, including when and how to check
- ✅ Describing our service by **outcome and team** — "our team takes on the rescheduling work"
- ✅ Honest comparison against paid alternatives, including the $750 government expedite
- ✅ "We cannot guarantee a date", "you pay only on success", "we never ask for your portal
  password" — repeat these often

Grep before shipping:

```bash
grep -rniE "auto-?book|24/7|every few seconds|instant alert|bot\b|white.?label|bulk booking|guarantee[ds]? (a |an |your )?(slot|date|visa|appointment)|success rate" blog/
```

Hits inside a sentence about *someone else's* product, or a sentence saying we do **not** do it, are
fine. Hits describing what we do are not.

---

## Pre-publish checklist

- [ ] No `{{` placeholders remain
- [ ] Canonical URL correct and absolute, with trailing slash
- [ ] `datePublished` and `dateModified` set to the real publish date, in three places: BlogPosting
      schema, `article:published_time`/`article:modified_time` meta, and the visible `<time>`
- [ ] `BlogPosting.image` points at a **raster** file (JPG/PNG) at least 1200px wide — SVG covers
      are fine on-page but do not render as social previews
- [ ] `og:image` and `twitter:image` set and absolute
- [ ] FAQ `<details>` text matches the FAQPage schema exactly
- [ ] One `<h1>` only; headings descend without skipping levels
- [ ] Every TOC anchor resolves to a real `id`
- [ ] Every statistic has a source link and retrieval date
- [ ] Constraint sweep grep is clean
- [ ] Card added to `blog/index.html` grid **and** to the Blog schema `blogPost` array
- [ ] URL added to `sitemap.xml`
- [ ] `seo/03-content-queue.md` row marked ✅, `seo/04-changelog.md` line added
- [ ] Validate schema: https://validator.schema.org/ and Google's Rich Results Test

---

## Publishing cadence

Target is 8–10 posts a month (~2 a week) per the growth plan. **Space them.** Publishing a batch
in one day and then going quiet for three weeks produces a worse freshness signal than the same
posts spread across the month, makes attribution impossible in Search Console, and means a
structural mistake gets repeated across every post before anyone notices it in the first.

Rule of thumb: no more than one post per 48 hours, and never two on the same day.

---

## Scheduled publishing (automated)

Posts can be written and merged today but go live on a future date by themselves. A GitHub Action
runs daily at **04:10 UTC (09:40 IST)**, and when a queued post's date arrives it stamps the real
publish date, releases the page from `noindex`, reveals the hub card and sitemap entry, commits, and
pushes. The push triggers the normal Vercel deploy — there is no Vercel token involved and nothing
to configure on that side.

| Piece | Where |
|---|---|
| The queue | [`blog/publish-queue.json`](publish-queue.json) |
| The script | [`scripts/publish_scheduled.py`](../scripts/publish_scheduled.py) |
| The schedule | [`.github/workflows/publish-scheduled-posts.yml`](../.github/workflows/publish-scheduled-posts.yml) |

### How a post is held back

Three markers. All three must be present, or the script fails loudly rather than half-publishing.

1. **The page is `noindex`** — a `<!-- SCHEDULED POST: ... -->` comment directly above
   `<meta name="robots" content="noindex, follow">`. The page is deployed and returns 200, so links
   to it from the footer and from other posts never break; Google just will not index it.
2. **The hub card sits in an inert `<template>`** in [`blog/index.html`](index.html):
   ```html
   <!-- SCHEDULED 2026-08-15 — revealed automatically by scripts/publish_scheduled.py -->
   <template data-scheduled="the-slug" data-publish-on="2026-08-15">
   <article class="post-card" data-category="…"> … </article>
   </template>
   ```
   `<template>` content is parsed into a detached fragment: it does not render, is not in the DOM,
   and carries no link.
3. **The sitemap `<url>` is inside an XML comment** in [`sitemap.xml`](../sitemap.xml), opened with
   `<!-- SCHEDULED YYYY-MM-DD - …`.

Leave `datePublished` at the day you *wrote* it. The script overwrites it on publish.

### To schedule a new post

1. Write it normally (steps 1–3 of the publish flow above).
2. Apply the three hold markers.
3. Add an entry to `blog/publish-queue.json`:
   ```json
   { "slug": "the-slug", "title": "…", "publishOn": "2026-09-02" }
   ```
4. Commit and push. That is all — the Action takes it from there.

### Running it by hand

```bash
python scripts/publish_scheduled.py --dry-run              # what would happen today
python scripts/publish_scheduled.py --today 2026-08-15     # simulate a date
python scripts/publish_scheduled.py --slug the-slug        # publish one now, dated today
python scripts/publish_scheduled.py                        # publish anything due
```

Or from GitHub: **Actions → Publish scheduled blog posts → Run workflow**, with a `dry_run`
checkbox and an optional `slug` to release one early.

### What it changes, per post

Six date fields (`article:published_time`, `article:modified_time`, schema `datePublished` and
`dateModified`, the visible `<time>`, and `Published <date>` in the sources block), the `robots`
meta, the hub `<template>` and its schema `datePublished`, and the sitemap comment.

**"Retrieved &lt;date&gt;" lines in the sources block are deliberately left alone** — they record
when a source was actually checked, and must not drift with the publish date.

### If it fails

The script builds every edit in memory and writes nothing unless all of them succeed, so a failed
run leaves the repo untouched. The usual cause is markup drift — someone reformatted the hub card or
the robots block and an anchor no longer matches. The error names the exact anchor that failed. Fix
it, or publish that post by hand and delete its queue entry.

### Still manual after an automated publish

Submitting the URL in Google Search Console. The workflow summary lists what went live as a
reminder.

---

## Post inventory

| Slug | Category | Published | Primary query |
|---|---|---|---|
| `us-visa-expedited-appointment-750` | expedite | 2026-08-12 | us visa expedited appointment 750 |
| `is-us-visa-slot-booking-legit` | trust | 2026-08-11 | are us visa slot booking services legit |
| `reschedule-us-visa-appointment-earlier` | rescheduling | ⏳ 2026-08-19 | reschedule us visa appointment earlier |
| `us-visa-appointment-world-cup-2026-guide` | basics | 2026-06-29 | fifa world cup 2026 us visa |
| `us-visa-appointment-canada-guide-2026` | wait-times | 2026-06-23 | us visa appointment canada |
| `us-visa-appointment-dubai-fast-2026` | wait-times | 2026-03-16 | us visa appointment dubai |

Next up is in [`seo/03-content-queue.md`](../seo/03-content-queue.md). Do not pick a topic that is
not on that queue without checking it for cannibalisation first.
