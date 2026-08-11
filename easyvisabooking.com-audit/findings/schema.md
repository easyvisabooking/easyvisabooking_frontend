# Schema.org / Structured Data Audit — easyvisabooking.com
Audit date: 2026-08-11. Method: raw HTML fetch (`render_page.py --mode never`, confirmed non-SPA / `is_spa: false` on every URL, so raw fetch is authoritative — no client-side-injected JSON-LD to miss). 15 URLs checked: the 14 sitemap URLs + `/for-agents/`.

## 1. Per-URL schema inventory

| URL | JSON-LD blocks | Types present | Valid JSON-LD? |
|---|---|---|---|
| `/` | 4 | Organization+ContactPoint; Service+Offer+Organization+ServiceChannel+Country+ContactPoint; WebSite+SearchAction+EntryPoint; FAQPage+Question+Answer | Yes, all 4 parse-valid |
| `/services/` | 0 | — (none) | N/A |
| `/services/us-visa-appointment-canada/` | 2 | Service+Organization+Country; BreadcrumbList | Yes |
| `/services/us-visa-appointment-toronto/` | 3 | Service+Organization+Country; BreadcrumbList; FAQPage | Yes |
| `/how-it-works/` | 0 | — (none) | N/A |
| `/about/` | 2 | AboutPage+Organization+Person(founder); BreadcrumbList | Yes |
| `/contact/` | 0 | — (none) | N/A |
| `/blog/` | 0 | — (none) | N/A |
| `/blog/us-visa-appointment-world-cup-2026-guide/` | 3 | BlogPosting+Organization(author/publisher); BreadcrumbList; FAQPage | Yes |
| `/blog/us-visa-appointment-canada-guide-2026/` | 3 | BlogPosting+Organization(author/publisher); BreadcrumbList; FAQPage | Yes |
| `/blog/us-visa-appointment-dubai-fast-2026/` | 2 | BlogPosting+Organization(author/publisher); BreadcrumbList | Yes |
| `/terms/` | 1 | BreadcrumbList | Yes |
| `/privacy/` | 1 | BreadcrumbList | Yes |
| `/refund-policy/` | 1 | BreadcrumbList | Yes |
| `/for-agents/` | 0 | — (none) | N/A — page content beyond nav/footer links not deep-crawled; **flagged as unconfirmed** for content-fit purposes (schema absence itself is confirmed via raw HTML grep) |

**Totals:** 5 of 15 pages ship zero structured data (`/services/`, `/how-it-works/`, `/contact/`, `/blog/`, `/for-agents/`). 9 of 15 pages have `BreadcrumbList`; 6 do not (`/`, `/services/`, `/how-it-works/`, `/contact/`, `/blog/`, `/for-agents/`).

---

## 2. Homepage deep-dive (4 known blocks)

### Block 1 — `Organization` + `ContactPoint`
```json
{"@type":"Organization","name":"Easy Visa Booking","url":"https://www.easyvisabooking.com/",
 "contactPoint":{"@type":"ContactPoint","email":"contact@easyvisabooking.com","contactType":"Customer Support","availableLanguage":["English","Hindi"]},
 "sameAs":["https://www.linkedin.com/company/easyvisabooking","https://t.me/YourTelegramChannel"],
 "areaServed":["Canada","UAE","Turkey","Australia","United Kingdom"]}
```
- **Required properties** (Organization has none strictly "required" by Google, but for eligibility for Knowledge-Panel-adjacent sameAs treatment, `name` + `url` are the baseline): present.
- **Recommended properties present:** `sameAs`, `areaServed`, `contactPoint`, `description`.
- **Recommended properties missing:** `logo` (no `logo` anywhere on the canonical Organization node), `telephone` at the Organization/ContactPoint level (phone only exists buried in Block 2's `ServiceChannel`, not as a real `ContactPoint.telephone`).

**FINDING — Critical / Placeholder text in production schema.**
Evidence: `"sameAs":[...,"https://t.me/YourTelegramChannel"]`. This is literal placeholder text — the site's actual, live Telegram link (confirmed via `grep` on the real footer HTML) is `https://t.me/earlyusvisabooking`. The schema is currently telling Google/AI crawlers the business's Telegram channel is called "YourTelegramChannel," which does not exist.
Fix: replace with `https://t.me/earlyusvisabooking` (see `schema-generated/01-homepage-organization-website-service-graph.jsonld`).
Falsifiability: verifiable by diffing the JSON-LD `sameAs` array against `grep -o 'href="https://t.me/[^"]*"'` on the live page footer — they currently do not match.

**FINDING — Medium / Unverifiable sameAs claim.**
Evidence: `"https://www.linkedin.com/company/easyvisabooking"` appears only inside the JSON-LD. It is not a clickable link anywhere on the homepage, About page, or Contact page (checked all three via raw HTML grep for "linkedin" — zero visible `<a>` references).
Fix: either add a real, visible LinkedIn link somewhere on the site (footer/about), or confirm the company page exists and is actually owned by this business before keeping the claim in schema. Do not publish `sameAs` entries that can't be independently verified by a crawler landing on the page.
Falsifiability: check for `href` containing "linkedin.com" in the rendered page — currently absent.

### Block 2 — `Service` + `Offer` + `Organization` + `ServiceChannel` + `Country` + `ContactPoint`
- `Service` is valid schema.org markup but **has no dedicated Google rich-result type** — it aids entity/knowledge-graph understanding, not SERP visual features. Framed correctly in existing markup.
- `Offer.price = "100"`, `priceCurrency = "USD"` present — good, no placeholder text.
- **Provider is a second, independent `Organization` object** — `{"@type":"Organization","name":"Easy Visa Booking","url":"..."}` — with no `@id` connecting it back to Block 1's Organization.

**FINDING — High / Duplicated Organization "islands," no `@id` entity linking.**
Evidence: the homepage alone declares `Organization` twice — once as the top-level node in Block 1 (with full `sameAs`/`areaServed`/`contactPoint`), and again as a bare `{name, url}` stub nested inside Block 2's `Service.provider`. Neither carries an `@id`. Continuing across the site: `/about/` nests a third Organization instance inside `AboutPage.mainEntity`; `/services/us-visa-appointment-canada/` and `/services/us-visa-appointment-toronto/` each nest a fourth/fifth bare-stub instance as `Service.provider`; each of the 3 blog posts declares Organization twice more (as `author` and `publisher`) — 6 more instances. **Total: 7+ independent, unlinked Organization declarations site-wide**, none sharing an `@id`.
Why it matters: without `@id`, Google/AI systems must infer these are "the same entity" purely from exact `name`+`url` string matching. That's brittle — it already silently degrades because the stub instances carry none of the rich signal (`sameAs`, `areaServed`, `contactPoint`, `logo`) that the canonical homepage instance has, so any consumer that *does* successfully merge them still only inherits the thinnest version. This directly affects AI/LLM entity consolidation, which is explicitly the concern raised in the task.
Fix: adopt a single canonical `Organization` node with `@id = "https://www.easyvisabooking.com/#organization"` (defined once, ideally on the homepage or a global template), and have every other page reference it via `{"@id": "https://www.easyvisabooking.com/#organization"}` instead of re-declaring name/url. Same pattern for `WebSite` (`#website`) and each `Service` (`#service`, or per-page `#service` ids). See `schema-generated/01-homepage-organization-website-service-graph.jsonld` for the corrected pattern, applied consistently in files 04–07.
Falsifiability: `grep -c '"@type": "Organization"'` across all 15 pages' JSON-LD currently returns 7+ with zero occurrences of `"@id"` anywhere in any block on any page (confirmed — no `@id` key appears in any of the 15 extracted JSON-LD payloads).

### Block 3 — `WebSite` + `SearchAction` + `EntryPoint`
Valid, all required Sitelinks Searchbox properties present (`url`, `potentialAction.target.urlTemplate`, `query-input`). No issues. Missing only the optional `@id`/`publisher` link discussed above.

### Block 4 — `FAQPage` (8 Q&As)
**Severity: Info only**, per hard rule. Google retired FAQ rich results for all sites on 2026-05-07, so this block currently earns no Google SERP feature. Content quality is good (no placeholder text, answers are genuine and specific) and any AI/LLM citation benefit is unconfirmed. **Do not remove it and do not add new FAQPage blocks expecting a Google SERP benefit** — this note also applies to the 3 other FAQPage blocks found on `/services/us-visa-appointment-toronto/`, `/blog/us-visa-appointment-canada-guide-2026/`, and `/blog/us-visa-appointment-world-cup-2026-guide/` (4 FAQPage blocks total site-wide, all Info severity).

---

## 3. Gaps by page type

### Blog posts (`/blog/us-visa-appointment-*`) — 3 pages
All 3 already have `BlogPosting` + `BreadcrumbList` (2 of 3; Dubai post is missing... no, it has BreadcrumbList too — confirmed present on all 3). What's genuinely missing:

**FINDING — Critical / `image` property absent from every BlogPosting.**
Evidence: none of the 3 live `BlogPosting` blocks contain an `image` key (confirmed by direct inspection of all 3 extracted JSON-LD payloads — `headline`, `description`, `author`, `publisher`, `datePublished`, `dateModified`, `url`, `mainEntityOfPage`, `keywords` are all present, `image` is not).
Why it matters: `image` is Google's most consistently required Article property for rich-result/visual-card eligibility — without it these posts cannot surface with a thumbnail in Article-type rich results.
Fix: add `image` (array of 1+ absolute URLs, 1200px+ wide recommended) to all 3 posts. Template in `schema-generated/02-blogposting-template.jsonld`.
Falsifiability: search each post's JSON-LD payload for the string `"image"` — currently zero matches across all 3.

**FINDING — Medium / `publisher.logo` absent.**
Evidence: `publisher` on all 3 posts is `{"@type":"Organization","name":"Easy Visa Booking","url":"https://www.easyvisabooking.com"}` — no `logo` sub-property.
Fix: add `publisher.logo` as an `ImageObject` (recommended for full Article eligibility and consistent brand display). Template in file 02.

**FINDING — Low / author & publisher declared as duplicate anonymous nodes, not @id-linked.**
Same root cause as the homepage duplication issue — each post independently declares `author` and `publisher` as bare `{name,url}` Organization stubs instead of referencing the canonical Organization `@id`. Fix included in file 02.

**FINDING — Low / breadcrumb URL inconsistency.**
Evidence: the Dubai post's breadcrumb uses `"item":"https://www.easyvisabooking.com/blog"` (no trailing slash) while the Canada and World Cup posts use `"https://www.easyvisabooking.com/blog/"` (trailing slash, matching the sitemap). Minor, but should be standardized.

**Cross-check (not a defect, noted for completeness):** `datePublished` and `dateModified` are identical on all 3 posts, and both match `htmldate`'s independently-extracted publication date for each post (Canada: 2026-06-23, Dubai: 2026-03-16, World Cup: 2026-06-29) — dates are accurate, ISO 8601, no falsification concern. `dateModified == datePublished` is expected for content that hasn't been edited since publish; flag for future maintenance to make sure `dateModified` actually gets bumped when posts are edited.

### `/services/*` location pages — 2 pages
**FINDING — High / `offers` property missing from both location pages.**
Evidence: `/services/us-visa-appointment-canada/` and `/services/us-visa-appointment-toronto/` `Service` blocks contain `serviceType`, `provider`, `areaServed`, `description`, `url` — no `offers`. (The homepage's separate `Service` block does have an `Offer`, but that's a different, unlinked node — see @id finding above.)
Fix: add page-specific `Offer` blocks. Templates in `schema-generated/04-service-location-pages-offers.jsonld` (price copied from the homepage's $100 starting fee — **confirm with the business this is accurate per-location before publishing**, flagged inline in the generated file).

**FINDING — Info / `/services/` hub page has zero structured data.**
The hub page that lists all service locations (and links to 3 further location pages not in the sitemap: `australia`, `dubai`, `uae`) has no JSON-LD at all. Recommended `CollectionPage`+`ItemList`+`BreadcrumbList` in `schema-generated/06-services-hub-collectionpage.jsonld`. Note: the 3 un-sitemapped service pages are a separate indexing/sitemap gap (same pattern as the already-logged `/for-agents/` gap) — out of strict schema scope but flagged for visibility.

### `/about/` — Organization detail
Present: `AboutPage` wrapping an `Organization` with `founder` (Person), `areaServed`, `knowsAbout`, `BreadcrumbList`.
**Missing:** `foundingDate` and `sameAs` on this instance (the page visibly says "Easy Visa Booking was founded by Meghkumar Girishbhai Sheth..." but states no date, so **no `foundingDate` value can be honestly generated** — do not fabricate one; add only if/when the business supplies a real date). `logo` also absent, consistent with the site-wide gap.
Fix direction: once this Organization instance is replaced by an `@id` reference to the canonical node (file 01), it automatically inherits `sameAs`/`logo`/`contactPoint` — no separate fix needed here beyond adding `foundingDate` if a real date becomes available.

### `/contact/` — ContactPoint completeness
**FINDING — Critical / zero structured data on the Contact page.**
Evidence: raw HTML fetch of `/contact/` returns `block_count: 0`. This is the single largest concrete gap relative to task priorities — the page most likely to need a machine-readable `ContactPoint` has none.
Additional evidence gathered from the page itself: the real, working contact channel is WhatsApp (`https://wa.me/8849146234`, used in 4 places including a floating button) plus email (`contact@easyvisabooking.com`) — consistent with the phone number already used in the homepage's `ServiceChannel.servicePhone`. No fabricated contact info needed; all values are already verified live on-site.
Fix: `schema-generated/05-contact-page.jsonld` (ContactPage + Organization `@id` ref + consolidated ContactPoint with both telephone and email) + the matching `contact` BreadcrumbList from file 03.

### `/how-it-works/` and `/for-agents/`
Both ship zero JSON-LD. **Do not use `HowTo` for `/how-it-works/`** — deprecated since Sept 2023, explicitly called out in `schema-generated/07-how-it-works-and-for-agents-webpage.jsonld`. Recommended plain `WebPage` + `BreadcrumbList` for both. `/for-agents/` content was not deep-crawled beyond confirming zero schema and zero sitemap presence (already logged in CONTEXT.md) — the generated template's description is a placeholder that must be replaced with real page-specific copy before publishing.

### All pages — `BreadcrumbList`
Confirmed **missing on 6 of 15 pages**: `/`, `/services/`, `/how-it-works/`, `/contact/`, `/blog/`, `/for-agents/`. Present and valid on the other 9 (`/about/`, both service-location pages, all 3 blog posts, `/terms/`, `/privacy/`, `/refund-policy/`). Templates for the 5 missing non-homepage instances in `schema-generated/03-breadcrumblist-missing-pages.jsonld` (homepage breadcrumb is optional/low-value since it's the root node — not included).

### Review / AggregateRating
**Not recommended — correctly absent.** Checked homepage HTML directly: found an HTML comment `<!-- Testimonial section removed -->` and no testimonial/review markup with real names, quotes, or star ratings anywhere on the crawled pages. Per hard rule, Review/AggregateRating markup must never be fabricated, and Google's review-snippet policy prohibits self-serve/author-controlled review markup without genuine, verifiable third-party reviews. No action recommended; flag as **Info** only if the business later adds a genuine, verifiable review widget (e.g., Google Business Profile / Trustpilot embed) — schema should then be generated from that real data, not authored from scratch.

---

## 4. sameAs / social profile links — summary

| Source | Claimed in JSON-LD | Verified live on site? |
|---|---|---|
| Telegram | `https://t.me/YourTelegramChannel` (placeholder) | No — real link is `https://t.me/earlyusvisabooking` |
| LinkedIn | `https://www.linkedin.com/company/easyvisabooking` | Not linked anywhere in visible HTML — unverified |
| WhatsApp | Not in `sameAs` (used via `ContactPoint`/`ServiceChannel` phone instead, correctly — WhatsApp has no schema.org sameAs convention) | Yes, live and prominent (floating button + 3 inline links) |

No Facebook, Instagram, X/Twitter, or YouTube presence found anywhere on the crawled pages.

---

## 5. Generated JSON-LD (ready to paste)

All files in `easyvisabooking.com-audit/findings/schema-generated/`:
1. `01-homepage-organization-website-service-graph.jsonld` — canonical `@id`-linked Organization/WebSite/Service graph; fixes the Telegram placeholder.
2. `02-blogposting-template.jsonld` — adds `image` (currently 100% missing) and `publisher.logo`; reusable pattern for all 3 posts.
3. `03-breadcrumblist-missing-pages.jsonld` — 5 missing BreadcrumbList blocks.
4. `04-service-location-pages-offers.jsonld` — adds `offers` to both `/services/*` location pages.
5. `05-contact-page.jsonld` — ContactPage + full ContactPoint for `/contact/` (currently zero schema).
6. `06-services-hub-collectionpage.jsonld` — CollectionPage/ItemList for `/services/`.
7. `07-how-it-works-and-for-agents-webpage.jsonld` — plain WebPage (explicitly NOT HowTo) for both pages.

Every generated file that contains a value which could not be independently verified from live page content (logo file dimensions, LinkedIn ownership, `/for-agents/` description, per-location pricing) is marked inline with a `_comment`/`_comment_VERIFY` key — these are guidance annotations for the implementer and must be stripped before the JSON-LD is published (they are not valid schema.org properties).

---

## Severity legend
Critical = blocks a Google-supported rich result or contains false/placeholder data live in production. High = meaningful gap vs. task-specified requirement, no immediate SERP risk. Medium = quality/completeness gap. Low = polish/consistency. Info = no actionable SERP impact under current Google policy (FAQPage).
