# AI Search / GEO Readiness — easyvisabooking.com

Audit date: 2026-08-11. Canonical host: `https://www.easyvisabooking.com`.

## Headline judgment

The technical door is open (any AI crawler that wants in can get in), and several
content blocks (FAQ answers, the 4-step process, the Canada guide) are genuinely
written as self-contained, quotable passages — that part of the work is already done
well. But this is a commercial intermediary in a YMYL category (US visa appointments,
money changing hands) with heavy scam activity, near-zero third-party trust signals,
one broken/placeholder social profile in its own schema, three different and
contradictory lists of "which countries we serve" on the same domain, a mismatch
between the FAQ schema and the FAQ users actually see, and essentially no organic
footprint (9 clicks / 382 impressions / avg. position 45.2 over 90 days per GSC).
**No amount of markup fixes this.** Formatting changes below will not, by themselves,
produce AI Overview or ChatGPT citations on a YMYL "book me a visa slot" query — the
binding constraint is trust/authority, and that has to be built (real reviews, a
verifiable business identity, consistent factual claims, third-party corroboration)
before formatting improvements pay off.

---

## 1. AI Crawler Accessibility

**robots.txt (verified live, `https://www.easyvisabooking.com/robots.txt`, HTTP 200):**

```
User-agent: *
Allow: /
Disallow: /services/us-visa-appointment-dubai/
Disallow: /services/us-visa-appointment-uae/
Disallow: /services/us-visa-appointment-australia/

Sitemap: https://www.easyvisabooking.com/sitemap.xml
```

There is exactly one user-agent block (`*`), no crawler-specific rules at all. Every
named crawler inherits the wildcard.

| Crawler | Status | Consequence |
|---|---|---|
| GPTBot (OpenAI training/browsing) | **Allowed** | Content eligible for ChatGPT's underlying model and browsing tool. |
| OAI-SearchBot (ChatGPT Search index) | **Allowed** | Content eligible for indexing into ChatGPT Search results. |
| ClaudeBot | **Allowed** | Content eligible for Claude training crawl. |
| Claude-User | **Allowed** | Content eligible for real-time fetch when a user asks Claude to browse/cite this page. |
| Claude-SearchBot | **Allowed** | Content eligible for Claude's search-index crawl. |
| PerplexityBot | **Allowed** | Content eligible for Perplexity's index. |
| Google-Extended | **Allowed** (not that it matters here — see note) | See note below. |
| Applebot-Extended | **Allowed** | Content eligible for Apple Intelligence / Siri summarization. |
| CCBot (Common Crawl) | **Allowed** | Feeds many smaller LLMs and research indices. |
| meta-externalagent | **Allowed** | Content eligible for Meta AI. |
| Bingbot | **Allowed** | Standard Bing web index crawl — this is what actually feeds Bing Copilot citations (see §5). |

**Severity: Info.** Nothing is blocked. There is no finding to fix here — flagging
only because the task requires precision.

**Important correction on Google-Extended, stated precisely because this is commonly
misunderstood:** `Google-Extended` is a *content-usage token*, not an indexing
crawler. It controls whether Google may use already-crawled content (fetched via
ordinary Googlebot) to **train** Gemini/Vertex AI foundation models and, per Google's
current documentation, to power **grounding** in Gemini and AI Mode. It does **not**
control, and blocking it would **not** affect:
- Whether pages appear in classic Google Search results.
- Whether pages appear in **Google AI Overviews** — AI Overviews sources are drawn
  from Google's regular web index (crawled by Googlebot/Googlebot-Image etc.),
  independent of the Google-Extended toggle.

Since `Google-Extended` is not blocked here, this is moot for easyvisabooking.com —
but if anyone on this team later considers adding a `Disallow` for it "for privacy,"
they should understand it will not remove the site from AI Overviews; it only opts
the content out of Gemini model training/some grounding use.

**Three now-orphaned Disallow rules — Severity: Low.**
```
Disallow: /services/us-visa-appointment-dubai/
Disallow: /services/us-visa-appointment-uae/
Disallow: /services/us-visa-appointment-australia/
```
All three URLs return **HTTP 404** (verified via curl, live). These are dead rules
blocking pages that don't exist — harmless to crawling, but they are also evidence
that the site once had (or planned) dedicated Dubai/UAE/Australia location pages that
no longer exist, which lines up with the entity-consistency problem in §4: the
Organization and Service schema still *claim* UAE and Australia as `areaServed`, but
there is no crawlable page to substantiate that claim for either humans or AI
crawlers.
- **Fix:** Either remove the three dead Disallow lines, or (better) build the pages
  and remove the Disallow once they exist, so the areaServed claim in schema has a
  corresponding indexable page.
- **Falsifiable:** Re-request each URL; if any returns 200, this finding is stale.

---

## 2. llms.txt

**Verified: `https://www.easyvisabooking.com/llms.txt` returns HTTP 404** (confirmed
via `curl -o /dev/null -w "%{http_code}"` — the URL serves the site's branded 404
page, not a 404-with-content trick). No llms.txt exists.

**Severity: Info, not a fix priority.** Being direct about the value here: llms.txt
is a voluntary, community-proposed convention. **Google does not consume it for
Search or AI Overviews. No major AI vendor (OpenAI, Anthropic, Perplexity, Microsoft)
has confirmed that their production crawlers or answer engines actually read and act
on llms.txt today.** It is, at best, speculative future-proofing.

- **Recommendation:** Do not prioritize this. If the team wants a low-cost hedge
  (it's a static text file, minutes of effort), a short llms.txt listing the core
  pages (home, how-it-works, services, refund policy) with one-line descriptions is
  harmless to add — but do not represent it internally as something that will drive
  citations. Rank it below every other item in this report.
- **Falsifiable:** Re-request `/llms.txt`; if it 200s in a future audit, this is
  resolved.

**RSL 1.0 licensing:** No `/rsl.xml` and no RSL declarations found (also 404).
Given RSL adoption is even earlier-stage than llms.txt and this is a service site
with no licensable original media/data assets, **no recommendation to add it** —
low value for this business type.

---

## 3. Passage-Level Citability

This is the strongest dimension on the site, and also where the sharpest concrete
defect (schema/content mismatch) lives. Assessed against the query class specified:
*"how do I get an earlier US visa appointment?"*, *"how long is the US visa wait in
Canada?"*, *"are visa appointment booking services legit?"*

**What's working — Severity: Info (positive finding).**

The `/how-it-works/` page states the process as four short, literal, self-contained
steps rather than narrative marketing copy, e.g. (quoted verbatim, Step 4):
> "When an appointment within your requested range becomes available, we secure it
> through the official scheduling portal and confirm it with you by email and
> WhatsApp, along with the official confirmation for your records. Our service fee
> becomes payable at this point and not before."

And the Canada guide (`/blog/us-visa-appointment-canada-guide-2026/`) has a genuinely
extractable, source-attributed answer to the wait-time question (quoted verbatim,
confirmed present in both the FAQPage JSON-LD *and* the visible page body at line 758
of the rendered HTML):
> "Wait times vary significantly by location and visa category. For B1/B2 visitor
> visas, some locations show wait times of several months, with Toronto often being
> the longest. You can check current estimated wait times on the official US
> Department of State website."

This is close to the ideal citable-passage shape: direct answer, specific claim,
attributed to an authoritative external source (travel.state.gov), no throat-clearing.
No fix needed on this passage.

**Finding: marketing-prose passages bury the same facts elsewhere on the same page —
Severity: Medium.**

Quoted (same Canada guide, body text, immediately preceding the good passage above):
> "You have been refreshing the appointment calendar for days. Maybe weeks. Every
> time you log in, the earliest available date is months away, or worse, the system
> shows nothing at all... And now you are stuck waiting, watching your travel plans
> slowly fall apart while the portal offers you a date sometime next year."

This is scene-setting/empathy copy with no extractable fact in it. It is not harmful,
but it dilutes the ratio of citable-to-decorative text on the page and pushes the
direct-answer passage further from the top of the article (the good passage
above is roughly 700+ words into the piece, not in the first 40-60 words of the
section that introduces the topic).

- **Fix:** Move a compressed version of the direct-answer sentence ("Wait times for
  B1/B2 visitor visas in Canada currently run several months at most locations, with
  Toronto typically the longest...") into the first paragraph under the H2 that
  introduces wait times, before the narrative framing, not after it. Keep the
  narrative paragraph — it serves human readers and conversion — just don't let it
  precede the answer.
- **Falsifiable:** Check word position of the first fully-contained factual sentence
  after the relevant H2 in a future crawl; target under ~60 words.

**Finding: homepage FAQPage schema and the homepage's visible FAQ section are two
different FAQs — Severity: High.**

This is the single most concrete citability/trust defect found. The homepage carries
a `FAQPage` JSON-LD block with 7 Q&As. Quoted verbatim, JSON-LD question 1:
> `"name": "How quickly can you secure an earlier US visa appointment?"`

The **visible, on-page FAQ accordion** (same URL, same render) has a *different*
question 1, worded and scoped differently:
> `<h6 class="faq-question">How soon can I get an urgent appointment?</h6>`

This isn't a paraphrase — the two FAQ sets diverge entirely. JSON-LD includes
questions never shown on the page at all: *"Is Easy Visa Booking affiliated with the
US government?"*, *"What is your refund policy?"*, *"What does the US visa
appointment booking service cost?"* (with a specific "$100" figure). The visible
accordion instead has *"Is my data secure and private?"*, *"What should I do if I
have more questions?"* — none of which exist in the JSON-LD.

Why this matters for GEO specifically (beyond Google's structured-data policy
against hidden/mismatched content, which is a separate SEO risk): AI answer engines
that parse structured data alongside rendered text for consistency will find two
irreconcilable claims about the same entity (e.g., is the service fee "$100" per the
schema, or unstated per the visible page?). Inconsistent facts about pricing and
guarantees, on a fraud-sensitive commercial-intermediary page, are exactly the kind
of thing that suppresses citation confidence — not because of a formatting rule, but
because it looks unmaintained or unreliable.

- **Fix:** Make the FAQPage JSON-LD an exact structured mirror of the visible
  accordion (same questions, same answers, same count). Pick one canonical FAQ set.
- **Falsifiable:** Extract both the JSON-LD `mainEntity[].name` array and the visible
  `.faq-question` text nodes from the rendered homepage; diff them. Currently: 7 vs 6
  items, 0 of 6 visible questions match a JSON-LD question by exact or near text.
- Note per audit instructions: this is **not** flagged for lost Google FAQ rich
  results — Google retired FAQ rich results for all sites on 2026-05-07, so that
  upside no longer exists regardless of the mismatch. This is flagged purely as a
  factual-consistency/trust problem relevant to AI citation and to Google's general
  structured-data content-matching guidance.

**Finding: pricing is stated once, in a single schema block, nowhere near the
visible page prominence it deserves — Severity: Medium.**

The only place a specific number appears is the FAQPage JSON-LD:
> "Our service fee starts from USD $100 per appointment successfully secured and
> varies by consulate location... This fee is for our scheduling assistance only and
> is separate from the MRV visa fee payable to the US Department of State."

This is exactly the kind of self-contained, quotable fact AI engines look for
("how much do visa appointment booking services cost?") — but it isn't in the
visible FAQ shown in §3 above (visible FAQ item "How and when am I charged?" states
*when* payment happens but never states *how much*, no dollar figure). A user or an
AI engine reading only the rendered page has no price; the number exists only in code.
- **Fix:** State the $100-starting-price and "varies by consulate" line as visible
  body text, not schema-only, ideally on `/services/` and in the visible FAQ item
  about charges.
- **Falsifiable:** Search rendered `extracted_text` of `/`, `/services/`, `/how-it-works/`
  for a currency figure; none is currently present outside JSON-LD.

---

## 4. Brand Mention / Entity Signals

**Severity: High — broken/placeholder profile inside the Organization schema itself.**

Homepage Organization JSON-LD, quoted verbatim:
```json
"sameAs": [
  "https://www.linkedin.com/company/easyvisabooking",
  "https://t.me/YourTelegramChannel"
]
```
`https://t.me/YourTelegramChannel` is a literal unfilled placeholder — a real
Telegram channel is used elsewhere on the same page (`https://t.me/earlyusvisabooking`,
linked from the "Join Telegram Channel" CTA, verified live with a distinct og:title
"Early US Visa Appointment"). The `sameAs` entry does not point to that channel or to
any real channel; the string `t.me/YourTelegramChannel` resolves to Telegram's
generic per-handle placeholder page (og:title "Your Channel") because Telegram
renders a preview for any syntactically valid, unclaimed handle — it is not a live
Easy Visa Booking asset.
- **Fix:** Replace with `https://t.me/earlyusvisabooking` (the real channel already
  in use), or remove the entry if there is no intent to maintain it as an official
  profile.
- **Falsifiable:** curl `https://t.me/YourTelegramChannel` og:description reads
  "You can view and join @YourTelegramChannel right away" — generic placeholder
  copy, not channel-specific content, confirming it is not a real established channel.

**Finding: LinkedIn company page cannot be verified as live from this audit —
Severity: Low/Info.** `https://www.linkedin.com/company/easyvisabooking` returns
HTTP 999 to automated requests, which is LinkedIn's standard anti-bot response and
not proof the page is dead — but it also means it cannot be confirmed as a real,
populated, active profile from this audit. Recommend manual visual verification that
the page exists, has a logo, and has at least minimal activity, since it is the only
`sameAs` entity link the schema offers besides the broken Telegram one.

**Finding: three (arguably four) different, contradictory lists of "which countries
we serve" across the same domain — Severity: High.**

| Location | Countries listed (quoted) |
|---|---|
| Homepage Organization `description` (JSON-LD) | "...for applicants in **Canada, UAE, India and Australia**." |
| Homepage Organization `areaServed` (JSON-LD) | `["Canada", "UAE", "Turkey", "Australia", "United Kingdom"]` — **no India** |
| Homepage Service `areaServed` (JSON-LD) | `Canada, United Arab Emirates, Turkey, Australia` — **no UK, no India** |
| About page Organization `areaServed` (JSON-LD) | `Canada, United Arab Emirates, Turkey, Australia, United Kingdom` |
| Homepage visible FAQ ("Do you book appointments worldwide?") | "Canada, United Kingdom, Dubai, Turkey, **India**, European Union countries, And many more..." |
| Homepage "Latest Guides" section subhead (visible text) | "...for visa agents and applicants across **Canada, UAE, India and Australia**" |
| Sitemap.xml location pages that actually exist | **Canada and Toronto only** — no UAE/Turkey/Australia/UK/India page exists |

No two of these lists match exactly, and only 2 of the ~6 countries claimed
(Canada, and Toronto as a Canadian city) have a corresponding indexable page. For a
YMYL commercial-intermediary entity, an AI engine (or a skeptical human) checking
"where does this company actually operate" gets a different answer depending on
which part of the site it reads. This is exactly the kind of internal inconsistency
that erodes the entity-confidence signals AI systems use before citing a commercial
source on a scam-prone topic.
- **Fix:** Pick one authoritative `areaServed` list, use it verbatim in every schema
  block and every visible mention, and only list a country if a corresponding page
  (or clear evidence of service capability) exists. If UAE/Turkey/Australia/UK/India
  are aspirational rather than currently served, say so, or remove them until pages
  exist.
- **Falsifiable:** Diff the areaServed/description arrays above in any future crawl.

**Finding: no third-party corroboration found within this audit — Severity: High
(binding constraint, not a formatting fix).** No Wikipedia entity, no Reddit
discussion, no Trustpilot/Google Business Profile reviews, no press mentions were
discoverable from on-site evidence. The homepage itself has an HTML comment reading
`<!-- Testimonial section removed -->` — i.e., a testimonials section existed and was
taken down, and none currently exists anywhere on the site. Per the GEO brief's own
correlation table, YouTube/Reddit/Wikipedia presence correlates far more strongly
with AI citation than any on-page formatting change. None of these exist for this
entity as far as this audit can determine.
- **Fix (realistic, not a quick win):** This requires actually earning citations —
  genuine customer reviews on a well-known platform (Google Business Profile,
  Trustpilot), a presence in relevant Reddit threads (r/immigration, r/USCIS-adjacent
  visa subreddits) answering real questions without spam, and a restored, honest
  testimonial/case-study section with attributable names. This is a trust-building
  program, not a code change, and will take months, not a sprint.
- **Falsifiable:** Search Wikipedia, Reddit, Trustpilot, Google Business Profile for
  "Easy Visa Booking" / "easyvisabooking.com" in a future audit; absence of results
  in all four keeps this finding open.

**Finding: named founder exists (positive) but has no independent verification —
Severity: Low.** The About page names a founder in schema and body text:
> `"founder": {"@type": "Person", "name": "Meghkumar Girishbhai Sheth"}`
This is good — better than an anonymous org-only byline — but there's no `sameAs` on
the Person (no LinkedIn/personal profile link), no photo, no bio/credentials, and
blog posts are authored by the **Organization**, not this named person (`BlogPosting.author`
= `{"@type": "Organization", "name": "Easy Visa Booking"}`), which is weaker for
E-E-A-T on YMYL content than a named, credentialed human author.
- **Fix:** Add `sameAs` (e.g., LinkedIn) to the founder Person entity; consider
  attributing blog posts to the named founder or a named team member with a short
  bio, consistent with YMYL author-expertise expectations.
- **Falsifiable:** Check `founder.sameAs` and `BlogPosting.author.@type` in future
  schema pulls.

**NAP/contact consistency — Severity: Info (positive).** Phone number is consistent
between the Service schema `servicePhone` (`+91-8849146234`) and the visible
WhatsApp float link (`wa.me/8849146234`) — no contradiction found here. No physical
address is published anywhere on the site (fully remote/digital service model),
which is common for this business type but is one more missing verifiability signal
in a scam-prone category; not flagging as a required fix, just noting it compounds
the trust gap above.

---

## 5. Platform-Specific Readiness

Grounding fact for all of the below: per the shared audit context (GSC, verified
access), the entire domain generated **9 clicks and 382 impressions over 90 days**,
at an **average Google position of 45.2**. The best-performing content page,
the Canada guide, has 300 impressions at **average position 50.3** — effectively
invisible even in classic Google web search. Domain has no confirmed backlink
authority data available (Tier 0 credentials only).

| Platform | Assessment |
|---|---|
| **Google AI Overviews** | Sourced from Google's regular web index. At position ~45-50 for its core queries, this domain is nowhere near the result set AI Overviews typically draws from (usually top ~10-20 organic). Not a plausible citation today; fixing schema/robots.txt does not change this — ranking has to improve first, which is a classic-SEO/authority problem, not a GEO-formatting one. |
| **Google AI Mode** | Same index dependency as AI Overviews, same conclusion. AI Mode also does more multi-step retrieval/synthesis, which could theoretically surface a niche page even at lower rank for a very specific query — but the entity-consistency problems in §4 work against it being selected as a trustworthy source once found. |
| **ChatGPT Search / OAI-SearchBot** | Crawler access is open (§1). No evidence of current visibility (no DataForSEO tools were available in this session to test live). Realistically low probability of citation on a YMYL "book my visa appointment" query given the trust gaps in §4 — OpenAI's search product is also conservative about surfacing commercial intermediaries for consequential topics. |
| **Perplexity** | Crawler access open. Perplexity tends to cite a wider, longer tail of sources than Google AI Overviews, and rewards clean, direct-answer passages (which this site partly has, per §3) — of the platforms assessed, this is the most plausible near-term citation opportunity, though still gated by the trust issues in §4. |
| **Bing Copilot** | Bing Copilot citations are fed by the Bing web index, not a separate crawl. Bingbot is not blocked in robots.txt (§1). Bing indexation status could not be directly confirmed in this session (no Bing Webmaster Tools credentials verified in this audit run) — this should be checked directly via Bing Webmaster Tools or a `site:easyvisabooking.com` query on Bing before assuming indexation. Given the near-total absence from Google's index at any usable position, it would be reasonable to expect similarly thin Bing indexation, but this is inferred, not confirmed — flag for direct verification. |

---

## 6. Query-Class Assessment: "How do I get an earlier US visa appointment?"

**Would this site plausibly be cited today? No — and formatting will not change that
by itself.**

What the site has going for it, if trust were solved:
- A direct, non-hedging answer to the underlying mechanism exists and is accurate to
  how the AIS/CGI reschedule system actually works ("Once you have a confirmed
  appointment, you gain access to the reschedule function inside the AIS portal...
  cancellations from other applicants create openings that appear and disappear
  within minutes").
- The FAQ explicitly and correctly disclaims guaranteed outcomes ("No, and you should
  be cautious of any service that says otherwise") — this kind of self-aware,
  non-overpromising language is actually a *positive* trust signal for a YMYL
  commercial page, and is worth preserving/highlighting, not softening.

What's missing, in order of what actually gates citation:
1. **Third-party trust corroboration** (§4) — zero verifiable reviews, zero Reddit/
   Wikipedia presence, a broken placeholder in its own schema. This is the primary
   blocker. AI engines summarizing a YMYL "is this legit / how do I do this" query
   pull from a *pattern* of corroborating sources (official government pages,
   established forums, review aggregators) far more than from a single vendor's own
   site, however well-formatted.
2. **Organic authority** (§5) — average Google position ~45 means the page isn't
   even in the candidate pool most retrieval-augmented answer engines draw from.
3. **Internal factual consistency** (§4) — contradictory areaServed claims and a
   FAQ schema that doesn't match the visible FAQ actively work against citation
   confidence once a page is found.
4. Only then does passage-level polish (§3) matter at the margin — and that part is
   already reasonably close to best practice.

**Bottom line:** this is not a "add more schema" problem. It is a "become a source
worth citing on a topic full of scams" problem, which requires earned trust signals
over time, not a formatting sprint.

---

## GEO Readiness Score: 48 / 100

| Dimension | Weight | Score | Notes |
|---|---|---|---|
| Citability | 25% | 60/100 | Genuinely good direct-answer passages exist (§3), undercut by the FAQ schema/visible-content mismatch and pricing hidden in schema only. |
| Structural Readability | 20% | 68/100 | Clean semantic headings, numbered 4-step process, question-form FAQ headings, breadcrumbs. No HowTo/Article-level structural markup beyond BlogPosting/FAQPage. |
| Multi-Modal Content | 15% | 30/100 | No video, no data tables, no downloadable/comparison assets, generic stock-style imagery with non-descriptive alt text. Testimonial section was built and then removed. |
| Authority & Brand Signals | 20% | 18/100 | Broken placeholder in Organization sameAs, contradictory areaServed claims in up to 6 places, no discoverable Wikipedia/Reddit/review presence, near-zero organic authority (GSC avg. position ~45). This is the binding constraint on the whole score. |
| Technical Accessibility | 20% | 82/100 | Static SSR HTML (not an SPA), robots.txt open to every major AI crawler with no specific blocks, HTTPS/HSTS, sitemap present, canonical tags present. llms.txt absent but low-value per §2. Three dead Disallow rules (cosmetic). |

**Weighted score: 0.25×60 + 0.20×68 + 0.15×30 + 0.20×18 + 0.20×82 ≈ 48**

## Top 5 Highest-Impact Changes

1. **Fix the Organization `sameAs` placeholder and reconcile the areaServed/country
   claims across all schema blocks and visible copy.** (§4) — Effort: Low (a few
   hours of copy/schema edits). Impact: Removes an actively broken, embarrassing
   signal and a factual-consistency red flag; necessary before any trust-building
   work will read as credible.
2. **Make the homepage FAQPage schema match the visible FAQ exactly (pick one FAQ
   set).** (§3) — Effort: Low (content decision + schema edit). Impact: Removes the
   single largest concrete "this page contradicts itself" signal found in the audit.
3. **Build real, verifiable third-party trust signals: reviews on Google Business
   Profile/Trustpilot, a restored testimonials section with attributable names,
   presence in relevant public forums.** (§4) — Effort: High, ongoing. Impact: This
   is the actual gate on AI citation for a YMYL intermediary; nothing else on this
   list matters much without it.
4. **Improve organic ranking enough to enter the retrieval candidate pool** (currently
   avg. position ~45) — Effort: High, separate classic-SEO workstream. Impact:
   Necessary precondition for AI Overviews/AI Mode citation regardless of content
   quality.
5. **Surface pricing ($100 starting fee) and the country-list as plain visible text,
   not schema-only, and move direct-answer sentences to the front of each section
   before narrative framing.** (§3) — Effort: Low-Medium. Impact: Marginal but real
   improvement to passage extractability once the trust/authority gates above are
   addressed.

Deprioritized / explicitly not recommended: adding llms.txt as a priority (§2,
unconfirmed adoption by any major AI engine), adding or expanding FAQPage schema for
Google SERP benefit (Google retired FAQ rich results for all sites 2026-05-07), and
adding RSL 1.0 licensing (no licensable media assets, near-zero current adoption).
