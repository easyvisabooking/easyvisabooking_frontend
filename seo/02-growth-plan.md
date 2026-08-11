# Growth Plan — ranking, traffic, and clients

**Last updated:** 2026-08-11 · **Status:** LIVING DOCUMENT — see update protocol in [`README.md`](README.md)
**Goal:** maximum qualified traffic from anyone, anywhere, searching for a faster US visa appointment.

---

## 1. The strategic picture

### Where you actually stand

| Signal | Value | Read |
|---|---|---|
| Impressions (90d) | 382 | Effectively pre-launch |
| Clicks (90d) | 9 | " |
| Average position | 45.2 | Below the fold of page 4 |
| Impression trend | +196% (64 → 236 on flagship) | Query breadth growing |
| CTR trend | 3.26% → **1.47%** | …but rank is not |
| Common Crawl PageRank | rank ~1.2M | Bottom of the authority distribution |
| Discoverable referring domains | **0** | The binding constraint |

**The one-line diagnosis:** the site is being shown for *more* queries, all of them too deep to earn
a click. Growing impressions at position 41–97 is not progress — it is the same problem at greater
scale. Rank does not improve because the domain has no authority, and authority does not exist
because nothing links to it.

### The unwinnable line — do not cross it

Live SERP checks confirm these are owned by the US Government itself:

| Query class | Who owns the SERP |
|---|---|
| "us visa appointment" | `ais.usvisa-info.com` — **the actual booking portal** |
| "us visa interview slot" | `travel.state.gov`, `ustraveldocs.com` |
| "us visa wait times" | `travel.state.gov` (40–70% government-dominated) |

No commercial page displaces a government portal on its own name. Plus funded incumbents (Atlys,
VisaGrader, CheckVisaSlots) sit underneath them. **Anchoring strategy here guarantees failure.**

### The winnable line — where everything goes

SERPs for these are **blog- and forum-dominated with near-zero government presence**. Verified
competitors ranking here are ordinary content sites you can out-execute: `visaslotwatch.com`,
`visafortheunitedstates.com`, `beyondborderglobal.com`, `redbus2us.com`, `leso.co.in`, plus raw
Reddit/Quora/Teamblind threads.

> A Teamblind forum post outranking you is not a moat. That is the whole opportunity.

1. **Rescheduling mechanics** — how the system actually behaves
2. **Slot-release timing** — when slots appear and why
3. **Expedite and emergency routes** — including the brand-new $750 pilot
4. **Service legitimacy and cost** — "is this a scam / is it worth paying"
5. **Country and consulate specifics** — wait times, local process

**Your defensible angle, which a government portal structurally cannot publish:** real slot-release
timing patterns, consulate-by-consulate comparison, what actually happens during a reschedule, and
first-hand documentation of the process. Government sites publish policy. They never publish
behaviour.

---

## 2. 🔥 The time-sensitive opening — act on this first

**On 2026-07-01 the State Department launched a $750 expedited-interview pilot.** B-1/B-2 applicants
can pay $750 to secure a consular interview within **ten business days** at select posts. The pilot
runs **through 2026-12-31**.

Why this is the single best opportunity on the board:

- It is **six weeks old**. Nobody has built authority on it yet — the SERP is law-firm blogs and news
  coverage, not optimized content.
- It is **inherently high-intent**. Someone searching "$750 expedited visa appointment" is trying to
  get an earlier date *right now*. That is your exact customer.
- It has a **hard deadline**, which forces recurring searches ("is the pilot extended", "which
  embassies", "did it end") straight through December.
- It is **complementary, not competitive**: $750 for a government expedite versus your $100 service
  fee is a genuinely useful comparison, and it lands you in the consideration set honestly.

There is a real chance to own this cluster outright. It expires. Treat it as first in the queue.

Second time-boxed opening: the **FIFA World Cup 2026 visa priority system**. You already have
`/blog/us-visa-appointment-world-cup-2026-guide/` — expand it into a cluster rather than leaving it
as a single post.

---

## 3. Keyword architecture — 5 clusters

Replaces the audit's four-cluster design. **The audit's "B2B/Agent Booking" cluster is removed** —
Stripe constraint, see [`README.md`](README.md). Clusters 3 and 5 are new, added from 2026-08-11 research.

### Cluster 1 — Rescheduling & slot mechanics `[CORE]`
The strategic centre. Highest intent among winnable terms.

- Hub: **`/blog/us-visa-appointment-guide/`** (new pillar — see §4)
- Intent: informational → commercial
- Angles: can you reschedule earlier · how many times · why the option is greyed out · what happens
  when you reschedule · rescheduling limits and lockouts
- **Information-gain hook we can uniquely supply:** excessive refreshing triggers **24–72 hour
  temporary bans**. Almost nothing ranking says this clearly, and it is exactly the mistake your
  customers make before finding you.

### Cluster 2 — Wait times & country/consulate data `[TRAFFIC ENGINE]`
This is how you get global traffic. It is also the **link magnet** — see §6.

- Hub: **`/us-visa-wait-times/`** (new data page, refreshed monthly)
- Intent: informational, very high volume, global
- Verified 2026 hooks worth leading with — these are counter-intuitive and therefore linkable:
  - The longest B1/B2 waits are **no longer** in Africa or South Asia. They are in **Canada and
    Australia**: Toronto **14.5 months**, Sydney **15 months**, Vancouver **12.5 months**.
  - India averages 2–10 months; Brazil 6–12; many European posts schedule within **days**.
- Strategic fit: your existing Canada and Toronto pages sit on top of the *worst backlog in the
  world*. That is not a coincidence to waste.

### Cluster 3 — Expedite & emergency appointments `[TIME-BOXED — GO NOW]`
See §2. Hub: a dedicated $750 pilot explainer.

Angles: who qualifies · which embassies participate · $750 vs waiting vs a service · emergency
appointment criteria · what proof of urgency is needed · is the pilot being extended.

### Cluster 4 — Trust, legitimacy & cost `[BOTTOM FUNNEL — CONVERTS]`
Lowest volume, highest conversion. Every visitor in this niche is asking "is this a scam" before
anything else.

Angles: are visa slot services legit · agent fees compared · how to spot a fraudulent operator ·
free methods vs paid · what nobody can legitimately guarantee.

**Handle with unusual care.** Research confirms this category is full of genuine fraud — advance-fee
theft, Telegram con artists, blackmail using applicants' personal data, and a real risk of visa
denial where appointments are hoarded. The US Embassy in India explicitly warns that **no agent can
guarantee a visa or an interview slot.**

Your existing site language already aligns: "no upfront fee", "pay only on success", "we cannot
guarantee a date". **Lead with that.** Being the operator who states the risks plainly is the
strongest differentiator available to you given that testimonials and legal-entity details are off
the table. Honesty is the substitute trust signal.

### Cluster 5 — Application mechanics `[TOP OF FUNNEL — VOLUME]`
Broad, competitive, lower intent. Builds topical authority and feeds internal links downward.

Angles: DS-160 completion · document checklists · biometrics/VAC appointments · visa categories
(B1/B2, F-1, H-1B) · fees · interview preparation · what happens after the interview · status tracking.

Weight this **last**. It is where every competitor already is.

### Cluster weighting

| Cluster | Share of output | Why |
|---|---|---|
| 1 — Rescheduling mechanics | 30% | Core intent, winnable, converts |
| 2 — Wait times & countries | 25% | Global traffic + link magnet |
| 3 — Expedite / $750 pilot | 20% | Time-boxed, front-load then taper |
| 4 — Trust & cost | 15% | Converts; also the honest differentiator |
| 5 — Application mechanics | 10% | Authority filler, lowest priority |

---

## 4. New pages to build

You asked for more pages. These are the ones that earn their existence.

| Page | Type | Why | Priority |
|---|---|---|---|
| `/blog/us-visa-appointment-guide/` | Pillar, 3,000w+ | Cluster 1 hub. `/services/` at 495 words cannot carry hub duty — it is thinner than both its own children | 🔴 |
| `/us-visa-wait-times/` | Data page, monthly refresh | Cluster 2 hub **and the primary link-acquisition asset** (§6). Fresh data pages earn citations; sales pages never do | 🔴 |
| `/blog/us-visa-expedited-appointment-750/` | Explainer | Cluster 3 hub. Time-boxed opportunity | 🔴 |
| `/services/` rebuild | Commercial hub | 495w → 1,200w+, real hub structure, honest country list | 🟠 |
| `/blog/is-us-visa-slot-booking-legit/` | Trust | Cluster 4 hub. Ranks *and* converts | 🟠 |
| Country pages, phase 2 | Commercial | Only after the 60%-unique gate is provable. See warning below | 🟡 |

### ⚠️ Warning on scaling country pages

You serve applicants worldwide, so location pages are the obvious scale play. **They are also the
fastest way to get this domain classified as a doorway network.** The two that exist already share
**65–75% verbatim text**.

Hard gates before any new location page ships:
- **60%+ genuinely unique content** per page — consulate-specific wait times, local VAC details,
  local process quirks. Not a find-and-replace on the city name.
- **Stop at 30 pages** and re-evaluate. **Justify explicitly past 50.**
- Build them **only** where you can supply real local substance. Fewer, deeper pages beat a matrix.

Until that gate is provable, **route global traffic through Cluster 2 content pages instead** — one
strong `/us-visa-wait-times/` page covering every country outranks forty thin city pages, and carries
none of the risk.

### Geographic scope — resolve the contradiction

There are currently **up to six mutually inconsistent lists** of which countries you serve. Pick one
and use it everywhere (`Organization` description, `areaServed`, `Service.areaServed`, `/about/`
schema, visible FAQ, homepage subheading).

**Recommendation:** state global coverage in prose — *"applicants scheduling US visa interviews
worldwide"* — and reserve dedicated pages for locations with real substance. This is honest, matches
the business, ends the contradiction, and does not commit you to forty pages.

---

## 5. Content plan — 8+ posts/month

Full ordered queue with targets: [`03-content-queue.md`](03-content-queue.md).

### Publishing rhythm

- **8–10 posts/month**, ~2 per week.
- Front-load Cluster 3 (time-boxed) in months 1–2, then taper.
- **One "deep" post per month** (2,500w+, original analysis) — these earn links; the rest earn traffic.
- `/us-visa-wait-times/` refreshed **monthly**, with a visible "last updated" date.

### Non-negotiable quality gates per post

At 8+/month the failure mode is thin, repetitive content on a low-authority domain — which is worse
than publishing nothing. Every post must clear:

1. **Answer-first.** The question answered in the first 60 words, before any preamble.
2. **A named author with stated relevant experience.** Zero bylines exist today; this is one of the
   few E-E-A-T levers still open.
3. **At least one thing no competitor says.** A real number, a real mechanic, a real timing pattern.
   If it could be written without reading anything, do not publish it.
4. **Every statistic sourced and linked**, with a retrieval date.
5. **Distinct primary keyword.** Check `03-content-queue.md` before assigning — three-way
   cannibalization already exists on "US visa appointment Canada".
6. **Internal links:** 2–3 up to the cluster hub, 1–2 across to siblings, 1 to a commercial page.
7. **Constraint sweep passed** — see below.

### 🚨 Constraint sweep — run before every publish

Clusters 1 and 3 are the highest-risk content on the site, because writing about *slot monitoring*
sits one sentence away from describing *our own automation*, and Stripe reads this website.

Banned in all content — describing **our** service:
- ❌ auto-book, bot, automation, script, "24/7 monitoring", "checks every few seconds", "instant alerts"
- ❌ agent / travel agent / bulk / white-label / reseller offering
- ❌ any guarantee of a slot, date, or visa outcome

Allowed:
- ✅ Explaining what **applicants** can do themselves, including when and how to check
- ✅ Describing our service through **outcomes and the team** ("our team helps you secure an earlier date")
- ✅ Honest comparison against paid alternatives, including the $750 government expedite
- ✅ The existing "we cannot guarantee a date" and "pay only on success" language — repeat it often

The PDF topic list contains items that need reframing rather than rejection — #2 "Without an Agent",
#6 "Do Agents Really Get Earlier Dates", #22 "Best Strategy for Monitoring", #29 "Free vs Paid".
All are publishable as **applicant-facing advice**. None may become a description of our mechanics.

---

## 6. Backlinks — the binding constraint

**Zero discoverable referring domains.** Cross-referencing near-zero Common Crawl authority against
GSC position 45–80 supports a blunt conclusion: **link acquisition is more binding than any remaining
on-page or technical work.** Stages 1–5 of the fix plan are necessary and insufficient.

### 6.1 🙋 Set up measurement first — you cannot manage what you cannot see

| Tool | Cost | What it unblocks | Time |
|---|---|---|---|
| **Moz API** (moz.com/products/api) | Free, 2,500 rows/mo | Referring-domain count + spam score — both currently blank | 15 min |
| **Bing Webmaster Tools** | Free | Bing index data — **and it feeds Microsoft Copilot citations** | 15 min |
| **GA4 property ID** | Free | Organic traffic reporting in future audits | 5 min |

Config: `~/.config/claude-seo/backlinks-api.json` (`moz_api_key`) and
`~/.config/claude-seo/google-api.json` (`ga4_property_id`).

### 6.2 The strategy: be cited as a data source, not asked for a favour

Nobody links to a booking service. People link to **numbers they can quote**.

`/us-visa-wait-times/` is the asset. Kept genuinely current, structured for citation, with the
counter-intuitive Canada/Australia finding leading, it becomes something journalists, university
international offices, and relocation blogs cite when covering visa backlogs. Every one of those is a
link you did not have to ask for.

This is also why Cluster 2 outranks Cluster 5 in priority despite lower commercial intent.

### 6.3 Legitimate outreach targets

- **University international student offices** — publish visa resource pages, link freely, and carry
  real domain authority. Highest ratio of value to effort.
- **Immigration and expat community resources** — long-lived resource pages.
- **HR and global-mobility publications** — corporate travel and relocation press.
- **Relocation and travel media** — reactive coverage when backlogs spike.
- **Journalists covering visa backlogs** — the wait-time data is directly quotable.

### 6.4 🚫 Avoid — flagged Critical risk in this niche

PBNs, paid link networks, mass guest posting, comment and forum spam. This category is under elevated
Google scrutiny precisely because it is full of fraud, and this domain has no established track record
to absorb a penalty. **A manual action here would cost more than the links could ever return.**

### 6.5 Community presence — earned, not spammed

`r/usvisascheduling`, `r/immigration`, `r/ImmigrationCanada`, `r/TravelVisa`, `r/USAVisa`.

Participate genuinely: answer questions, share the wait-time data when relevant, disclose the
affiliation. **Do not drop links.** These communities detect and punish promotion instantly, and a
public accusation of spamming in a niche where trust is the product is a net loss. The realistic
value is topic intelligence and occasional organic citation — not link volume.

---

## 7. Measurement

### Leading indicators, by stage

| Stage | Watch | Healthy | Cadence |
|---|---|---|---|
| Indexation | GSC Pages → indexed count | 7 → 14 | Weekly |
| Trust/on-page | CTR on `/` and `/contact/` | Holds ≥9% as impressions grow | Monthly |
| Content | Avg position on **rescheduling** cluster specifically | Rising | Monthly |
| Authority | Referring domains (once Moz configured) | Any number above 0 | Monthly |
| Conversion | WhatsApp/Telegram enquiries | Rising | Weekly |

### Read these correctly

- **Impressions alone are not progress.** They rose 196% while CTR fell 3.26% → 1.47%.
  Track *position on target clusters*, not impression volume.
- **Ignore the "striking distance" mirage.** `/services/` pos 1.0, `/how-it-works/` pos 4.0,
  `/blog/` pos 5.0 are each built from 1–4 impressions and vanish between periods. `/services/` is
  not even indexed. Chasing these optimizes noise.
- **Zero clicks at position 50 is not a failure.** Expected clicks from 300 impressions at position
  50.3 is under 1. Do not rewrite pages in response to it.

### Realistic timeline

| Horizon | Expect |
|---|---|
| Weeks 1–4 | Indexed count 7 → 14. Little traffic change. This is the foundation, not the return |
| Months 2–3 | First long-tail rankings on Cluster 3 (the $750 pilot — least competition, freshest) |
| Months 4–6 | Cluster 1 and 2 positions climbing; first organic referring domains |
| Months 6–12 | Compounding, **if and only if** link acquisition ran as a standing workstream |

Anyone promising faster in a YMYL category from zero authority is selling something.

---

## 8. AI search visibility

AI crawler access is already fully open — GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, CCBot,
Bingbot, Google-Extended are all unblocked. Nothing to fix there.

**Realism:** at 9 clicks and average position 45.2, this domain is not in the candidate pool most AI
answer engines draw from. In a YMYL commercial-intermediary category with heavy scam activity,
**formatting alone cannot produce citations.** Trust and authority are the binding constraint here
exactly as they are in classic search — it is one problem, not two.

What genuinely helps, in order: entity consolidation (fix-plan §4.4), passage-level citability
(answer-first formatting, gate #1 above), and the wait-time data page being the kind of thing an
answer engine wants to quote.

**llms.txt:** absent (404). Honestly — Google does not use it and no major AI vendor has confirmed
production use. Cheap to add, speculative benefit. **Do not let it displace trust and authority work.**

---

## 9. Change log for this plan

Every amendment gets a line in [`04-changelog.md`](04-changelog.md). Superseded reasoning is struck
through, never deleted.

| Date | Change |
|---|---|
| 2026-08-11 | Initial plan. Built on the 2026-08-11 audit, the 39-topic Reddit list, and fresh SERP research |
| 2026-08-11 | **Removed** the audit's B2B/Agent cluster and its `/for-agents/` recommendation — Stripe constraint |
| 2026-08-11 | **Added** Cluster 3 (expedite / $750 pilot) — discovered in research, not in the audit. Time-boxed to 2026-12-31 |
| 2026-08-11 | **Added** Cluster 5 (application mechanics) from the PDF bonus topics |
| 2026-08-11 | Re-weighted Cluster 2 upward — it is the link-acquisition asset, not just traffic |
