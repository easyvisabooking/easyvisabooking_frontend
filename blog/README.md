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
| Why-us block | `.why-us` | **Required** directly under every `.compare`. See below |
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
- **Categories by default, names by exception.** Every post gets the *categories*: DIY, slot
  availability websites, all-in-one visa platforms, the $750 government expedite. A company is
  named only in a post that is genuinely about choosing between providers, which today means
  `is-us-visa-slot-booking-legit` and `reschedule-us-visa-appointment-earlier`. Naming competitors
  in a location or event guide adds nothing and hands them the brand impression.
- **Atlys is not named anywhere.** Not in a table, not in prose, not in a sources list.
- **CheckVisaSlots and VisaGrader are referred to as websites only.** No Chrome extension, no
  install step, no user counts or store ratings. Where a name is used, the small-print pattern is
  `e.g. CheckVisaSlots, VisaGrader` under the category name.
- **Describe competitors factually and neutrally.** Public, verifiable facts about their *model*
  only: what the fee buys and when it is charged. Never allege wrongdoing by a named company. Never
  quote a competitor price we have not verified — link out for pricing.
- **Our row** uses `class="is-us"` and the `.compare-us-tag` badge, and always states: from $100,
  paid only on success, no guarantee. **Never** the old "no portal password" line: it was removed
  site-wide on 2026-08-19 because the cloud plan needs credentials.
- **Close with `.compare-foot`**: comparison not endorsement; no commercial relationship; verify
  pricing directly.

### The why-us block — required under every comparison table

A neutral table alone leaves the reader with five options and no reason to pick ours. `.why-us`
sits directly beneath it and answers that, in four or five bullets. It is the only place in a post
where we argue for ourselves, which is what keeps the table above it honest.

- **Argue from our own model, never against a named company.** "An alert plan bills every month for
  information" describes a pricing model and is fine. Anything about how a named company behaves is
  not.
- **Lead with pay-on-success.** It is the only genuinely structural difference: every other row
  charges before the outcome. Say so explicitly, and say the fee is $100.
- **Then: we carry the work, not the alert. A wide date range is the reader's biggest lever.
  Everything published before you pay** — link `/privacy/`, `/terms/`, `/refund-policy/`.
- **Say nothing about portal credentials, in either direction.** The old "we never ask for your
  portal password" bullet was false once the cloud plan shipped and was stripped from every post on
  2026-08-19. Do not reinstate it, and do not replace it with a request either.
- **Close with `.why-us-foot` conceding the free row.** State the reader profile that should not pay
  anyone. A why-us block with no concession in it reads as a sales page and undoes the table.
- **The constraint sweep applies here hardest.** No guarantee, no success rate, no automation
  language, no testimonial.

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
- ✅ "We cannot guarantee a date", "you pay only on success", "appointment availability is controlled
  by the consulate" — repeat these often
- ❌ **Never** "we never ask for your portal password". Removed site-wide on 2026-08-19: the cloud plan
  needs credentials, so the claim was false. Say nothing about credentials in either direction

Grep before shipping:

```bash
grep -rniE "auto-?book|24/7|every few seconds|instant alert|bot\b|white.?label|bulk booking|guarantee[ds]? (a |an |your )?(slot|date|visa|appointment)|success rate" blog/
```

Hits inside a sentence about *someone else's* product, or a sentence saying we do **not** do it, are
fine. Hits describing what we do are not.

---

## House style sweep — also run before every publish

Two rules that apply to every published page, not just blog posts.

**1. No em dashes or en dashes.** `—` and `–` are the single strongest tell that copy was written by an
AI, and this whole blog exists to read as first-hand human experience. Use a comma, colon, semicolon,
full stop or parentheses instead. For numeric and date ranges use a plain hyphen or the word "to":
"30-60 days", "June 11 to June 27, 2026". This applies to `<meta>` descriptions, JSON-LD `description`
and `text` fields, and visible body copy alike.

**2. The founder is "Megh" only.** Never publish the full legal name. It must be `Megh` in the byline,
the author card `<h2>`, `Person.name` in the BlogPosting schema, `<meta name="author">` and
`<meta property="article:author">`. The `.byline-avatar` initial is `M`.

Grep before shipping:

```bash
grep -rnP "[\x{2013}\x{2014}]" blog/ --include=index.html
grep -rniE "meghkumar|girishbhai" blog/ --include=index.html
```

Both must return nothing. (`blog/README.md` and `blog/_template/` docs are exempt — neither ships;
see `.vercelignore`.)

**3. Competitor-naming sweep.** Atlys must not appear at all, and no third-party tool may be
described as an extension or by install count or store rating:

```bash
grep -rniE "atlys|chrome extension|browser extension|web store|extensions?</th>" blog/ \
  --include=index.html --exclude-dir=_template
```

Must return nothing. Category labels are `Slot-availability websites` and `All-in-one visa
platforms`.

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
- [ ] Competitor-naming sweep clean; `.why-us` block present under the `.compare` table
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
| The guard | [`.github/workflows/check-scheduled-holds.yml`](../.github/workflows/check-scheduled-holds.yml) |

### Nothing may point at a held post

This is the rule the whole mechanism exists to enforce, and the one that is easy to get wrong.

A held post is deployed and returns 200 with `noindex`. That is fine **only while nothing Google can
crawl points at it**. The moment a live page links to it, Googlebot follows the link, hits the
`noindex`, and files the URL in Search Console under *"Excluded by 'noindex' tag"* — the page shows
as **"URL is not available to Google"** in URL Inspection. It resolves itself on the publish date,
but it is noise, it burns a crawl, and it looks like a broken site.

That happened once, in August 2026: `reschedule-us-visa-appointment-earlier` was held correctly but
still linked from six live pages and listed in the hub's `Blog` JSON-LD. Hence marker 4, marker 5,
and the CI guard below.

### How a post is held back

Five markers. The script fails loudly rather than half-publishing if any is missing.

1. **The page is `noindex`** — a `<!-- SCHEDULED POST: ... -->` comment directly above
   `<meta name="robots" content="noindex, follow">`.
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
4. **Every inbound link from a live page is held.** Two forms, both applied by `--hold`:
   ```html
   <!-- SCHEDULED LINK 2026-08-15 the-slug
   <a href="/blog/the-slug/" class="mb-2">Anchor text</a>
   -->
   ```
   for a related-post card or a footer link list, and — for a link mid-sentence, where commenting
   out the markup would eat the prose — the anchor is demoted to a span that keeps its text and
   drops the URL:
   ```html
   <span data-scheduled-link="the-slug" data-publish-on="2026-08-15">rescheduling to an earlier date</span>
   ```
   Both become live `<a>` tags again on publish.
5. **No entry in the hub's `Blog` schema `blogPost[]` array.** A URL in live JSON-LD is a discovery
   path exactly like an `<a href>`. The script *inserts* the entry on publish, reading the headline
   and image from the post's own `BlogPosting` schema — so do not add it by hand when scheduling.

Leave `datePublished` at the day you *wrote* it. The script overwrites it on publish.

### To schedule a new post

1. Write it normally (steps 1–3 of the publish flow above), including its inbound links from other
   posts and the footer. Write them as ordinary links — do not hand-comment anything.
2. Apply markers 1–3, and do **not** add the hub `blogPost[]` schema entry.
3. Add an entry to `blog/publish-queue.json`:
   ```json
   { "slug": "the-slug", "title": "…", "publishOn": "2026-09-02" }
   ```
4. Run `python scripts/publish_scheduled.py --hold the-slug`. It finds every inbound link across the
   site and holds it. Anything it will not rewrite blind it prints for you to handle.
5. Run `python scripts/publish_scheduled.py --check`. It must pass.
6. Commit and push. CI runs the same check; the Action takes it from there.

### Running it by hand

```bash
python scripts/publish_scheduled.py --hold the-slug        # hold every inbound link to a queued post
python scripts/publish_scheduled.py --check                # is every held post invisible to crawlers?
python scripts/publish_scheduled.py --dry-run              # what would happen today
python scripts/publish_scheduled.py --today 2026-08-15     # simulate a date
python scripts/publish_scheduled.py --slug the-slug        # publish one now, dated today
python scripts/publish_scheduled.py                        # publish anything due
```

`--check` runs on every push via **Actions → Check scheduled post holds**. It strips comments and
`<template data-scheduled>` blocks from every file `.vercelignore` does *not* exclude, then fails the
build if a scheduled post's URL survives anywhere. A held post cannot reach production discoverable.
A post's own canonical, `og:url` and self-link are exempt — they sit on the `noindex` page itself.

Or from GitHub: **Actions → Publish scheduled blog posts → Run workflow**, with a `dry_run`
checkbox and an optional `slug` to release one early.

### What it changes, per post

Six date fields (`article:published_time`, `article:modified_time`, schema `datePublished` and
`dateModified`, the visible `<time>`, and `Published <date>` in the sources block), the `robots`
meta, the hub `<template>`, the sitemap comment, every held inbound link across the site, and a
freshly inserted entry in the hub's `Blog` schema `blogPost[]` array.

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
| `us-visa-paid-expedite-canada` | expedite | 2026-08-19 | us visa paid expedite canada |
| `us-visa-expedited-appointment-750` | expedite | 2026-08-12 (updated 2026-08-19) | us visa expedited appointment 750 |
| `is-us-visa-slot-booking-legit` | trust | 2026-08-11 | are us visa slot booking services legit |
| `reschedule-us-visa-appointment-earlier` | rescheduling | ⏳ 2026-08-19 | reschedule us visa appointment earlier |
| `us-visa-appointment-world-cup-2026-guide` | basics | 2026-06-29 | fifa world cup 2026 us visa |
| `us-visa-appointment-canada-guide-2026` | wait-times | 2026-06-23 | us visa appointment canada |
| `us-visa-appointment-dubai-fast-2026` | wait-times | 2026-03-16 | us visa appointment dubai |

Next up is in [`seo/03-content-queue.md`](../seo/03-content-queue.md). Do not pick a topic that is
not on that queue without checking it for cannibalisation first.
