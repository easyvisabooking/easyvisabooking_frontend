# Content Quality & E-E-A-T Audit — easyvisabooking.com
Audit date: 2026-08-11 | Pages assessed: 15 (14 sitemap URLs + /for-agents/)
Methodology: raw HTML fetched live (Vercel, status 200 unless noted), body text isolated via trafilatura
(boilerplate-stripped) for word counts / E-E-A-T reading, `content_quality.py` QRG scorer run per page,
duplicate-content overlap measured with SequenceMatcher + 8-word shingle Jaccard.

**Content Quality Score: 54/100** (YMYL-weighted; Trust factor dominates and is the weakest pillar)

---

## 0. Page inventory with verified body word counts (trafilatura-extracted, not raw HTML)

| Page | Words | Type / min (quality-gates.md) | Verdict |
|---|---|---|---|
| `/` | 805 | Homepage / 500 | Pass |
| `/services/` | 122 | Category/hub / 400 | **Thin** |
| `/services/us-visa-appointment-canada/` | 1,096 | Location (Primary) / 600 | Pass on count, fails 60%+ uniqueness (see §3) |
| `/services/us-visa-appointment-toronto/` | 1,670 | Location (Secondary) / 500 | Pass on count, fails 40%+ uniqueness (see §3) |
| `/how-it-works/` | 371 | Landing / 600 | **Thin** |
| `/about/` | 513 | About / 400 | Pass |
| `/contact/` | 163 | (no fixed min) | Adequate for a contact page |
| `/blog/` | 65 | Index (no fixed min) | Adequate for an index |
| `/blog/us-visa-appointment-world-cup-2026-guide/` | 3,502 | Blog / 1,500 | Pass |
| `/blog/us-visa-appointment-canada-guide-2026/` | 2,745 | Blog / 1,500 | Pass |
| `/blog/us-visa-appointment-dubai-fast-2026/` | 1,357 | Blog / 1,500 | **Borderline thin** (90% of floor) |
| `/terms/` | 847 | Legal (no fixed min) | Adequate |
| `/privacy/` | 655 | Legal (no fixed min) | Adequate |
| `/refund-policy/` | 512 | Legal (no fixed min) | Adequate |
| `/for-agents/` | 0 (unique) | — | **308-redirects to `/services/`; no longer a distinct page** |

---

## 1. TRUST (heaviest-weighted factor — YMYL + scam-prone category)

### 1a. Non-affiliation disclaimer — present, prominent, repeated. Severity: Info (positive finding)
**Evidence:** identical disclaimer block appears in the footer/body of every page checked (home, services, both location pages, about, contact, terms, privacy, refund policy):
> "Easy Visa Booking is an independent appointment scheduling assistance service. We are not affiliated with, endorsed by, or acting on behalf of the U.S. Government, the U.S. Department of State, any U.S. Embassy or Consulate, CGI Federal, or the AIS portal. We do not provide legal or immigration advice, and we do not influence visa decisions. All appointments are made through the official scheduling portal."

The Terms page reinforces this: *"No statement on this website should be read as suggesting any official status, partnership or endorsement."* This is exactly the kind of explicit, unambiguous disclaimer YMYL guidelines want from a paid intermediary in a scam-heavy niche.
**Fix:** none needed — keep as-is. **Falsifiability:** re-crawl any page and confirm the disclaimer string is present; if absent on a new page, this finding is void for that page.

### 1b. Pricing transparency — genuinely strong. Severity: Info (positive finding)
**Evidence:** Home: *"You are charged only when we successfully secure an appointment for you."* About: *"Our fee starts from USD $100 and varies by consulate location... If we do not secure an appointment for you, no service fee is payable."* Toronto page states a specific figure: *"Toronto service fee is USD $150 per appointment successfully secured."* Refund policy: *"We acknowledge every refund request within 2 business days... Approved refunds are issued... within 5 to 10 business days. We do not deduct any administration charge from a refund."*
**Fix:** none needed. **Falsifiability:** confirm these exact figures/timeframes still appear verbatim on `/about/`, `/services/us-visa-appointment-toronto/`, and `/refund-policy/`.

### 1c. No verifiable legal entity, registration number, or physical address — despite an explicit on-page claim that this information is provided. Severity: **High**
**Evidence:** `/terms/` states: *"Easy Visa Booking ('we', 'us', 'our') is a private, independent company... Our registered details are set out at the top of this page and on our About page."* The actual header of `/terms/` reads only: *"Last updated: 7 August 2026. Operated by: Easy Visa Booking."* — a trading name, not a legal entity name (no Ltd/LLC/Inc/Pvt suffix), no company/registration number, no registered address, no jurisdiction of incorporation. The About page table lists only: Trading name, Founder (personal name), Nature of business, Countries served, support email/channels — again no registration number or address. Governing-law clause in Terms says disputes are "governed by the laws applicable at Easy Visa Booking's principal place of business" — without ever naming that place. For a paid service that asks strangers to send DS-160/passport-adjacent personal data and payment before a government interview, this is a material trust gap, and it directly contradicts the page's own claim of disclosure.
**Fix:** Add a real registered legal entity name, company/business registration number, registered business address (or clearly stated principal place of business + jurisdiction), on both `/terms/` and `/about/`, matching the "registered details" the Terms page already promises exist there.
**Falsifiability:** Search `/terms/` and `/about/` raw HTML for a company number, "Ltd", "LLC", "Inc", "Pvt", a street address, or a named jurisdiction. If found on re-check, this finding is void.

### 1d. No phone number; only WhatsApp/Telegram/email. Severity: Medium
**Evidence:** `/contact/` lists only "Email, WhatsApp and Telegram enquiries are answered around the clock." Site-wide search for `tel:` links and formatted phone numbers returned zero matches. One raw contact channel exists in markup: `href="https://wa.me/8849146234"` (WhatsApp deep link, not a callable/verifiable business landline) and `https://t.me/earlyusvisabooking` (Telegram handle — notably branded "earlyusvisabooking", not "easyvisabooking", a minor brand-consistency red flag worth double-checking is actually owned by the business). No option to call and speak to a person is a meaningful trust gap for a YMYL service handling appointment-critical timelines.
**Fix:** Add a callable phone/landline number with country code, and verify/rebrand the Telegram handle to match the domain name, or explain the naming discrepancy.
**Falsifiability:** Check `/contact/` raw HTML for `tel:` links or a formatted phone number. If present, this finding is void.

### 1e. Zero testimonials, reviews, or third-party validation anywhere on the crawled pages. Severity: **High**
**Evidence:** Site-wide grep for "testimonial", "review" (customer-facing), star ratings, "Trustpilot", etc. across home, about, and both location pages returned no matches except unrelated internal copy ("we review availability"). No client names, no star ratings, no case counts, no Trustpilot/Google Business Profile badge, no press mentions. The Canada and Toronto pages instead show: *"Below are actual confirmation screenshots from recently expedited bookings across Canada. Screenshots are redacted for client privacy. Full confirmations available on request."* — an unverifiable claim of evidence that is not actually shown on the page (see §5).
**Fix:** Publish attributed testimonials (first name + city/consulate, e.g., "Priya, Toronto — B1/B2, secured May 2026") or embed a live Trustpilot/Google review widget. If genuine confirmation screenshots exist, actually publish 2–3 redacted examples on-page rather than describing them as "available on request."
**Falsifiability:** Grep any page for "testimonial", star-rating markup, or a review-platform embed. If found, this finding is void.

### 1f. Security/payment trust signals not visible in the crawled HTML. Severity: Low
**Evidence:** No visible payment-processor logos (Stripe/PayPal/etc.), no SSL/security badge, no "as seen in" press strip found in any extracted text. (Note: HSTS is present at the transport layer per CONTEXT.md, but that is not a *visible* trust signal to a visitor.)
**Fix:** Add a small trust strip (payment processor logo, SSL/security badge) near the pricing/CTA sections on home and location pages.
**Falsifiability:** Inspect footer/CTA areas of `/`, `/services/us-visa-appointment-canada/` for payment-logo `<img>`/`<svg>` elements.

### 1g. FAQPage structured data present — Info only, per program note.
**Evidence:** Homepage and Toronto page both carry valid `FAQPage` JSON-LD (3,778 B and 2,182 B respectively). Google retired FAQ rich results for all sites on 2026-05-07.
**Fix/Note:** No action required; do not remove, do not add more for SERP benefit, do not claim confirmed AI-citation benefit. Flagged at Info severity only, per audit program instructions.

**Trust sub-score: ~45/100** — strong disclaimers and pricing clarity are undermined by the absence of a verifiable legal entity/address/phone and the complete absence of third-party validation, in a category where scam-avoidance signals are the single biggest driver of both rankings and conversion.

---

## 2. FLAGSHIP DIAGNOSIS: `/blog/us-visa-appointment-canada-guide-2026/` — 300 impressions (79% of site total), 0 clicks, avg. position 50.3

**Verdict: this is primarily a competitive-authority/ranking problem, secondarily a keyword-cannibalization problem — not a content-depth problem, and not fundamentally a title/meta problem.**

Evidence and reasoning:

- **Content depth is not the bottleneck.** The page is 2,745 words, structured with H2/H3 hierarchy, a numbered process (DS-160 → AIS account → MRV fee → schedule → reschedule), a comparison table of Canadian consulate wait times, a "common mistakes" list, and 9 FAQ-style Q&As with self-contained answers. `content_quality.py` scores it 84/100 overall quality with zero filler and zero AI-pattern-phrase matches. This is materially more comprehensive than most competing "how to get a US visa appointment in Canada" content. Depth is not why it fails to earn clicks.
- **Position 50.3 is the real story, and it makes the 0-click outcome close to inevitable regardless of title/meta quality.** Organic CTR at position ~50 (page 5 of results) is close to 0% industry-wide — almost no searcher scrolls that far. So "0 clicks despite 300 impressions" is largely explained by position alone; title/meta rewrites will not move the needle until the page ranks inside the top 20.
- **Title/meta are not obviously broken** — `US Visa Appointment in Canada 2026: Find Earlier Dates | Easy Visa Booking` (H1: *"US Visa Appointment in Canada (2026 Guide): How People Are Actually Finding Earlier Interview Dates"*) is keyword-aligned with the query set in GSC ("canada us visa appointment", "book us visa appointment canada", "canada us consulate appointment"). This is not a mismatch case.
- **Query intent is matched, not mismatched.** The 28-day query list ("canada us visa appointment", "appointment for us visa in canada", "book us visa appointment canada", "best time to reschedule us visa appointment", "canada us consulate appointment", "book us visa date") maps directly onto what the article covers. This is not an intent-mismatch case (e.g., informational content ranking for transactional queries, or vice versa) — the content genuinely answers these queries.
- **Likely real cause #1 — keyword cannibalization.** Three separate pages on the site target essentially the same head term cluster ("US visa appointment Canada"): `/services/us-visa-appointment-canada/` (commercial/service page), `/services/us-visa-appointment-toronto/` (commercial, heavily overlapping with the Canada service page — see §3), and this blog post (informational). Google's algorithm has to choose which of 2–3 same-site pages to rank for overlapping queries, which dilutes topical authority that could otherwise consolidate on one URL. GSC's own by-page table shows the *service* page `/services/` ranks position 1.0 (on a low-impression query) while the *blog* page targeting closely related terms sits at 50.3 — consistent with signal-splitting across competing internal pages rather than a single strong page.
- **Likely real cause #2 — the whole site is a low-authority domain competing for commercially contested terms.** Every other query set in GSC for this site also clusters in the 45–80 position range (see CONTEXT.md: "all position 45-80, zero clicks" for the 28-day query themes), and the 90-day site-wide average position is 45.2 with only 9 clicks from 382 impressions. "US visa appointment Canada" is contested by government/quasi-official domains (ustraveldocs.com legacy pages, ais.usvisa-info.com, travel.state.gov) and established competitors with far more backlink history. A young/low-authority domain is very unlikely to break into page 1–2 for this term cluster purely on content quality; this needs off-page authority building (the domain has a Tier-0 backlink profile per CONTEXT.md — no Moz/Bing data available, but Common Crawl presence alone doesn't indicate meaningful authority).

**Fix:**
1. Pick one canonical URL to own "US visa appointment Canada" — recommend the *service* page (`/services/us-visa-appointment-canada/`, transactional intent, matches most of the query list's commercial framing) as canonical for the head term, and reposition the blog post around a distinctly informational long-tail angle it does not already fully own (e.g., "how the AIS reschedule function actually works," which is a sub-topic currently buried in the middle of the post) with internal links pointing site authority at the service page for the commercial term.
2. Do not expect a CTR/title fix alone to move clicks — the binding constraint is ranking position, which requires backlinks/authority, not more on-page content.
3. Re-measure in 90 days: if position improves into the top 20–30 without a backlink campaign, this diagnosis is falsified and title/meta becomes the more relevant lever.

**Falsifiability:** If GSC position for this page moves above ~20 without any new backlinks/referring domains, the authority-based explanation is wrong. If cannibalization is not the cause, merging or de-indexing one of the two commercial location pages should show no ranking change for the blog post's target queries after re-crawl.

---

## 3. DUPLICATE CONTENT: Canada vs. Toronto service pages — measured overlap

**Severity: High**

**Measured overlap** (SequenceMatcher on normalized body text, 6,815 chars Canada vs. 10,106 chars Toronto):
- Overall similarity ratio: **66.7%**
- Verbatim matched blocks (≥15 chars): **5,108 characters**, i.e. **75.0% of the shorter (Canada) page's content is duplicated verbatim inside the Toronto page**, and 50.5% of the longer Toronto page consists of text lifted straight from the Canada page.
- 8-word shingle Jaccard similarity: **34.9%**; overlap coefficient (shared shingles ÷ smaller set): **65.4%**.

**Quoted evidence of the duplication** (identical or near-identical passages, word-for-word, on both `/services/us-visa-appointment-canada/` and `/services/us-visa-appointment-toronto/`):
> "Canada has one of the highest volumes of US visa applicants globally. Hundreds of thousands of people apply each year for tourist, student, and work visas. The number of available interview slots at Canadian consulates has never kept pace with this demand. The result is a waiting list that stretches well past 300 days for B1/B2 categories."

> "Canada uses the AIS (Appointment Information System) portal for all US visa appointment scheduling. This is where applicants pay the MRV fee, book their interview date, and manage their appointment. The portal is operated by the official US Visa Scheduling system."

> "We cannot create appointment availability that does not exist. We cannot guarantee a specific interview date or timeline. We cannot influence whether your visa is approved. We do not provide legal or immigration advice. We do not collect your MRV fee..."

> "Despite the 300+ day wait times showing on the public portal, we continue to secure slots within weeks for our clients. Below are actual confirmation screenshots from recently expedited bookings across Canada."

The only genuinely unique material on the Toronto page is: the consulate street address ("360 University Avenue"), the local-demographic framing (Brampton, Mississauga, Scarborough, South Asian community), the comparison table ("Doing It Yourself vs. With Easy Visa Booking"), the FIFA World Cup 2026 section, three dated screenshot captions, and the $150 fee figure. Everything else — the "why Canada has long waits" section, the AIS mechanics explainer, the "what we cannot do" disclaimer block, the placeholder-booking strategy, and the closing disclaimer — is copy-pasted near-verbatim from the Canada page.

**Verdict:** This is not "genuinely differentiated" content; it is a templated location page with the city name and a few local facts swapped in around a large shared core, which is precisely the doorway-page pattern flagged in `quality-gates.md` ("Only city/state name changed between pages... No unique local information... Penalty risk"). Toronto is nested inside Canada geographically, so the two pages are also directly cannibalizing the same "US visa appointment Canada / Toronto" query cluster (reinforces §2's cannibalization finding).

**Fix:** Either (a) consolidate — fold Toronto-specific facts (consulate address, local demographics, FIFA angle, $150 fee) into the Canada page as a dedicated Toronto section, 301-redirect the standalone Toronto URL into that anchor, and stop maintaining two pages; or (b) genuinely differentiate — rewrite the shared boilerplate (AIS mechanics, "what we cannot do," pricing structure) into a single reusable component that's visually consistent but keep only the location-unique sections as prose, and cut the shared blocks down so unique-content share rises from ~25–35% to comfortably above the 60% (primary location) / 40% (secondary location) thresholds in `quality-gates.md`.

**Falsifiability:** Re-run the SequenceMatcher/shingle comparison after edits. If verbatim block overlap drops below ~40% of the shorter page and shingle Jaccard drops below ~20%, this finding is resolved.

---

## 4. AUTHORSHIP / E-E-A-T — Expertise & Experience

**Severity: High (Expertise), Medium (Experience)**

- **No author bylines anywhere.** Grep for "author", "byline", "written by", "reviewed by" across all three blog posts returned zero genuine matches (the only regex hits were false positives inside unrelated words like "authorization"). None of the three blog posts — the World Cup guide, the Canada guide, or the Dubai agent guide — names a writer, credentials, or a "reviewed by" line. For YMYL content about visa/immigration process mechanics, the complete absence of a named, credentialed author (immigration consultant, RCIC, attorney, or even "written by our booking team, reviewed by [name]") is a clear expertise gap under the Sept 2025 QRG.
  **Fix:** Add a byline + short bio to each blog post (e.g., "Written by [Name], [role] at Easy Visa Booking" or credit the named founder, Meghkumar Girishbhai Sheth, who is already named on `/about/`) and a "last reviewed" date.
  **Falsifiability:** Check blog post HTML for an `<address>`, `rel="author"`, or visible byline element. If present, void this finding.

- **One first-hand experience signal exists but is not substantiated on-page.** Evidence: Canada and Toronto service pages both state *"we continue to secure slots within weeks for our clients. Below are actual confirmation screenshots from recently expedited bookings across Canada... Screenshots are redacted for client privacy. Full confirmations available on request."* — three dated captions are shown ("Toronto Consulate | B1/B2 Appointment Secured — Date: May 26, 2026" etc.) but the actual screenshot images were not verifiable from the extracted text/markup pulled in this audit; the claim of evidence is stronger than the visible evidence itself, since the images are gated behind "available on request" rather than shown.
  **Fix:** Either embed the redacted screenshots directly on the page (image, not just a caption/date), or soften the copy to avoid implying visible proof that isn't actually shown.
  **Falsifiability:** Visually re-inspect the rendered Canada/Toronto pages for actual `<img>` screenshot elements near these captions. If images are present and visible, this finding is void.

- **Founder is named with a real full name on `/about/`** (Meghkumar Girishbhai Sheth) — a positive signal, but it is not extended to the blog content as a byline, and no professional credentials (immigration law, RCIC, travel-industry certification, etc.) are stated anywhere for this person or the "coordinators"/"team" repeatedly referenced ("An experienced coordinator handles the paperwork," "Our coordinators take responsibility for tracking availability").
  **Fix:** State the founder's/team's relevant background (years doing this, prior consulate-facing work, certifications if any) on `/about/`.
  **Falsifiability:** Check `/about/` for any credential/experience statement beyond the founder's name. If present, void this finding.

**Expertise sub-score: ~35/100. Experience sub-score: ~50/100** (process transparency is good; verifiable first-hand proof and named credentials are missing).

---

## 5. UNSUPPORTED CLAIMS / COMPLIANCE & QUALITY RISK

**Severity: Medium (aggregate)**

1. **"300+ day" wait-time figure repeated as fact across pages, without an on-page source or date-stamped citation at point of use.**
   **Evidence:** Canada service page: *"The result is a waiting list that stretches well past 300 days for B1/B2 categories."* Toronto service page: *"Toronto consulate wait times currently past 300 days in the standard queue."* Neither instance links to or names a source at the point the claim is made. By contrast, the **blog** Canada guide handles this correctly: *"You can check current estimated wait times for each Canadian location on the official US Department of State website... Keep in mind that these are estimates and actual availability can differ from what the published numbers suggest."* — sourced and appropriately hedged.
   **Fix:** Add the same sourcing/hedging language ("per the US Department of State's published wait-time estimates as of [date]") directly next to the "300 days" claim on both service pages, matching what the blog post already does correctly.
   **Falsifiability:** Check whether a citation/source link sits within 1–2 sentences of the "300 days" claim on the service pages. If present, void this finding.

2. **Dubai "6 to 8 weeks" wait-time claim is stated as current fact with no source or date.**
   **Evidence:** `/blog/us-visa-appointment-dubai-fast-2026/`: *"Current wait times for a US visa appointment in Dubai sit at approximately 6 to 8 weeks for B1 B2 tourist and business visa categories."* No link to travel.state.gov or an "as of [date]" qualifier accompanies this figure anywhere in the post, unlike the Canada guide's more careful sourcing pattern.
   **Fix:** Add "(source: US Department of State visa wait-time tool, checked [month/year])" and a direct link, and repeat the same hedge used in the Canada post ("estimates; actual availability can differ").
   **Falsifiability:** Search the Dubai post for a state.gov link/citation near the wait-time claim. If present, void this finding.

3. **No "guaranteed date" language found — this is a positive finding, not a risk.**
   **Evidence:** Multiple explicit disclaimers were found instead: *"We cannot guarantee a specific interview date or timeline"* (repeated on Canada and Toronto pages); *"No, and you should be cautious of any service that says otherwise"* (homepage FAQ); Toronto comparison table explicitly lists "Guaranteed date: No, nobody can promise this" as a row. The Terms page goes further: *"Any service claiming to guarantee you an earlier US visa appointment date should be treated with caution."* This is a well-handled compliance area — the site actively warns users away from competitors making guarantees, which is a genuine trust-building move in a scam-prone niche.
   **Fix:** None needed. **Falsifiability:** search all crawled pages for "guarantee" + a promised date; none found in this audit.

4. **"Official" language is used carefully and correctly** — every use of "official" in the crawled content refers to the actual US government portal/fee ("official AIS portal," "official scheduling portal," "MRV visa fee payable to the US Department of State"), never to the business itself. No instance of the business describing itself or its process as "official" was found.
   **Falsifiability:** grep all pages for "official" within 10 words of "Easy Visa Booking"/"we"/"our service" — none found describing the business as official.

5. **"Available on request" evidence claim (screenshots) — see §4** — flagged again here as a compliance-adjacent risk: describing unshown proof risks reading as an unverifiable claim if never actually produced to a prospect. Same fix as §4.

---

## 6. AI CITATION READINESS

**Severity: Low/Info**

- Self-contained, quotable factual passages exist and are reasonably well-formed for extraction, e.g.: *"For B1/B2 visitor and business visas, the fee is US$185. Petition-based categories like H, L, and O visas are US$205, while E-category visas are US$315."* (Canada blog guide) and *"Our fee starts from USD $100 and varies by consulate location."* (About). These are the kind of discrete, sourced-adjacent facts that extract cleanly.
- Clear H2/H3 hierarchy and FAQ-style Q&A blocks (Canada guide has 9 self-contained Q&A pairs) support answer-first extraction.
- Weaknesses: the repeated near-identical disclaimer/CTA blocks across pages (see §3) reduce information density per page for a crawler doing whole-page summarization, and the absence of bylines/dates reduces citation trustworthiness (no "who said this, when" for an AI system to attach to a quoted fact).
- FAQPage schema is present (home, Toronto) — flagged at Info severity only per program note; no rich-result or confirmed AI-citation benefit should be assumed post the 2026-05-07 retirement.

**Fix:** Add visible "last reviewed [date]" + author attribution near factual/pricing claims to increase citation trustworthiness; no urgent action needed on structure/formatting itself.

---

## 7. E-E-A-T SCORE SUMMARY

| Factor | Weight | Score /100 | Rationale |
|---|---|---|---|
| Experience | 20% | 50 | Process is described in granular, plausible operational detail (placeholder-booking, reschedule mechanics); claimed proof (screenshots) not actually visible in crawl; no client-attributed case studies. |
| Expertise | 25% | 35 | No author bylines on any blog post; no stated credentials for founder or "coordinators"; content is accurate-reading but unattributed. |
| Authoritativeness | 25% | 40 | Single named founder is a plus; no external validation, press mentions, or professional-body affiliation found anywhere in the crawl. |
| Trustworthiness | 30% | 45 | Strong disclaimers and pricing/refund transparency; undermined by missing legal entity/registration/address, no phone number, and zero testimonials — see §1. |
| **Weighted E-E-A-T** | 100% | **~43/100** | |

Combined with word-count/depth compliance (mostly passing, two thin pages) and the absence of AI-slop markers (content_quality.py scored 84–96/100 "overall_quality" on every page tested, with 0 filler/AI-pattern-phrase matches), the blended **Content Quality Score is 54/100** — solid raw writing quality dragged down heavily by the YMYL trust gaps and the structural duplication/cannibalization problem.

---

## 8. /for-agents/ — indexed URL now dead

**Severity: Medium**
**Evidence:** `/for-agents/` returns HTTP 308 → `/services/`. It is not in `/sitemap.xml` (per CONTEXT.md) yet still receives GSC impressions (6 impressions/90d, avg. position 11.2), meaning Google has not yet fully processed the redirect or is still surfacing a stale index entry.
**Fix:** Confirm no internal links still point to `/for-agents/` (update anchors to `/services/` directly); consider whether "for agents" deserves to exist as a genuinely distinct page — the Dubai blog post is explicitly written *"for visa consultants and agencies in Dubai,"* suggesting there is real audience demand for an agent-specific page that currently has nowhere permanent to live.
**Falsifiability:** Re-crawl `/for-agents/`; if it returns 200 with unique content, this finding is void.

---

## TOP 5 ISSUES (severity-ranked)

1. **[High] No verifiable legal entity, registration number, or address — despite the Terms page explicitly claiming this information is disclosed.** Direct YMYL trust risk and a self-contradiction between claim and actual content.
2. **[High] Zero testimonials/reviews/third-party validation anywhere on the site**, in a category defined by scam risk where social proof is a primary trust and conversion lever.
3. **[High] 65–75% verbatim content overlap between `/services/us-visa-appointment-canada/` and `/services/us-visa-appointment-toronto/`** — doorway-page pattern per quality-gates.md, and a likely contributor to query cannibalization.
4. **[High] No author bylines or stated credentials on any blog post** — an Expertise gap on YMYL content explaining consulate/immigration-adjacent process mechanics.
5. **[Medium] `/blog/us-visa-appointment-canada-guide-2026/` — 79% of site impressions, 0 clicks, position 50.3 — driven by low domain authority and cross-page keyword cannibalization, not content depth or title/meta**; fixing this requires consolidating the competing Canada/Toronto/blog pages onto one canonical target plus off-page authority building, not more on-page rewriting.
