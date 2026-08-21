# Content Queue

**Last updated:** 2026-08-19 (full re-analysis + queue cleared) · **Cadence:** 8–10 posts/month
**Status:** LIVING

Ordered by priority, not by cluster. Sources: the 39-topic Reddit list
([`research/`](research/)), 2026-08-11 SERP research, the audit's cluster analysis, and the
2026-08-19 re-analysis recorded below.

Status: ⬜ queued · 🟦 drafting · 🟨 review · ⏳ written and scheduled · ✅ published · 💀 killed
`C1`–`C5` = cluster (see [`02-growth-plan.md`](02-growth-plan.md) §3)

**Before writing any post:** re-read the constraint sweep in `02-growth-plan.md` §5 and the house
style sweep in [`blog/README.md`](../blog/README.md). Cluster 1 and 3 posts are the highest-risk on
the site: describing *how applicants check for slots* is fine; describing *how we do it* is not.

> **The queue is currently empty of unwritten work.** Every remaining item from the 2026-08-11
> queue is either written and scheduled, deliberately killed, or deferred with a stated date. What
> is left is the two items in **Still open** below and the rewrites in **R**.

---

## 🔎 Re-analysis, 2026-08-19 — why this queue looks different

The queue as written on 2026-08-11 was built before three things happened. All three change what is
worth writing, and two of them made queued items actively harmful.

### 1. The World Cup post was expired content

The 2026 FIFA World Cup ran 11 June to 19 July 2026 and is **over**. Spain beat Argentina in the
final on 19 July. `/blog/us-visa-appointment-world-cup-2026-guide/` was dated 29 June 2026, written
in the future tense throughout, and still telling readers to secure appointments for a tournament
that finished a month earlier.

- The growth plan's instruction to *"expand it into a cluster"* (§2, second time-boxed opening) is
  **withdrawn**. There is no opening left, and building a cluster on a finished event would be the
  worst available use of publishing capacity.
- **Done 2026-08-19:** rewritten as aftermath, URL kept. See R1.

### 2. The UAE reopened, and it is a news hook we own

Routine visa services at Mission UAE were suspended after the 3 March 2026 ordered departure.
Limited nonimmigrant appointments are available again, and the mission publishes its own release
window (Fridays, 07:30 to 11:30). Written and scheduled as `us-visa-appointment-abu-dhabi`.

This **absorbed queued item #16** ("UAE and the Gulf") entirely.

### 3. There is a $250 fee on this site nobody mentioned

The **Visa Integrity Fee** ($250, created by the One Big Beautiful Bill Act of 4 July 2025,
effective from FY2026 and phased in unevenly across posts) is charged **on visa issuance**, on top
of the MRV fee.

That is not just a missing topic. **Every comparison table on this site said "costs exclude the
US$185 MRV application fee, which everybody pays".** That sentence was incomplete on eight pages: a
reader budgeting $185 who is charged $435 has been misled by us, and cost transparency is what
Cluster 4 is built on. Fixed in every new post; see R4 for the older ones.

### 4. Cannibalisation found inside the queue itself

| Queued | Problem | Resolution |
|---|---|---|
| #5 *When do slots open* vs #12 *Best time of day to check* | Same intent, same SERP | **Merged** into #5 |
| #6 *How many times can you reschedule* | The published #3 already carries the per-country allowances, which **is** the answer | 💀 **Killed** |
| #8 *Why Canada has the longest waits* | Fourth page on "US visa appointment Canada" | 💀 **Killed.** Data folded into the wait-time posts and F2 |
| #13 *Which embassies offer the $750* | F1 carries the participating list; 6b owns the Canada half | 💀 **Killed** |
| #16 *UAE and the Gulf* | Absorbed by the Abu Dhabi post | 💀 **Killed** |

### 5. Two genuinely underserved topics were missing

Both are high-intent, both are directly relevant to enquiries we actually receive, and neither was
on the queue: the Visa Integrity Fee (N1) and the country-of-residence rule that closed third
country processing (N2). Both are now written.

### 6. The 2026-08-19 research produced a link asset that did not exist before

Post-level wait time data pulled for the country guides inverts the received wisdom, and it is the
most quotable thing this site has ever had:

| Post | B-1/B-2 interview wait, Aug 2026 |
|---|---|
| Toronto | ~495 days |
| Sydney / Vancouver | ~435 days |
| Hyderabad | ~315 days |
| Bogota | ~270 days |
| Mumbai / New Delhi | ~255 days |
| Kolkata | ~60 days |
| Lagos / Rio / Tijuana | ~30–45 days |
| **Abuja / Perth / Recife / Nogales** | **~15 days** |

**The longest US visitor visa queues in the world are now in wealthy English-speaking countries, not
in Africa or South Asia.** Toronto is roughly 33× Abuja. That single sentence is what F2 should lead
with, and it is the strongest link-acquisition asset available per `02-growth-plan.md` §6.2.

---

## Written and scheduled — 2026-08-22 to 2026-09-10 (one per day)

All 21 built with `scripts/build_post.py`, held at `noindex` per `blog/README.md`, released
automatically by `scripts/publish_scheduled.py`. Cadence respected: one post every 2 to 3 days,
never two on a day. Every internal link points **backwards** in time, so no post goes live with a
dead or held link in it.

| Slug | Cluster | Publishes | Primary keyword | Status |
|---|---|---|---|---|
| `us-visa-appointment-abu-dhabi` | C2 | 2026-08-21 | us visa appointment abu dhabi | ⏳ |
| `us-visa-integrity-fee-250` | C4 | 2026-08-22 | visa integrity fee | ⏳ |
| `cant-reschedule-us-visa-appointment` | C1 | 2026-08-23 | cant reschedule us visa appointment | ⏳ |
| `when-do-us-visa-slots-open` | C1 | 2026-08-24 | when do us visa slots open | ⏳ |
| `us-visa-appointment-scams` | C4 | 2026-08-25 | us visa appointment scam | ⏳ |
| `us-visa-wait-time-india` | C2 | 2026-08-26 | us visa appointment wait time india | ⏳ |
| `us-visa-third-country-application` | C5 | 2026-08-27 | us visa third country application | ⏳ |
| `us-visa-emergency-appointment` | C3 | 2026-08-28 | us visa emergency appointment | ⏳ |
| `us-visa-appointment-free-vs-paid` | C4 | 2026-08-29 | us visa appointment free vs paid | ⏳ |
| `what-happens-when-you-reschedule-us-visa` | C1 | 2026-08-30 | what happens when you reschedule us visa | ⏳ |
| `us-visa-appointment-website-not-working` | C1 | 2026-08-31 | us visa appointment website not working | ⏳ |
| `us-visa-wait-time-australia` | C2 | 2026-09-01 | us visa appointment australia wait | ⏳ |
| `us-visa-dropbox-interview-waiver` | C3 | 2026-09-02 | us visa dropbox interview waiver eligibility | ⏳ |
| `ds-160-mistakes` | C5 | 2026-09-03 | ds-160 mistakes | ⏳ |
| `what-to-bring-us-visa-interview` | C5 | 2026-09-04 | what to bring us visa interview | ⏳ |
| `us-visa-appointment-within-3-months` | C1 | 2026-09-05 | us visa appointment within 3 months | ⏳ |
| `us-visa-appointment-timeline` | C5 | 2026-09-06 | us visa appointment timeline | ⏳ |
| `us-visa-wait-time-nigeria` | C2 | 2026-09-07 | us visa appointment wait time nigeria | ⏳ |
| `us-visa-wait-time-latin-america` | C2 | 2026-09-08 | us visa appointment wait time mexico | ⏳ |
| `us-visa-appointment-family-group` | C1 | 2026-09-09 | us visa appointment family group reschedule | ⏳ |
| `us-visa-appointment-guide` *(F3 pillar)* | C1 | 2026-09-10 | us visa appointment guide | ⏳ |

**The pillar publishes last, deliberately.** It links down into fourteen spokes, so it cannot ship
before them.

### Information gain, per post

Gate #3 requires each post to carry something no competitor states. What shipped:

| Post | The thing nobody else says |
|---|---|
| Abu Dhabi | The mission's own published Friday 07:30–11:30 release window; the UAE is on `usvisascheduling.com`, not AIS; the $750 lane does **not** run there |
| Integrity fee | The fee exists in statute but collection is uneven post by post, and the refund has no published claim mechanism |
| Can't reschedule | Twelve causes as a decision tree, including the 24–72h temporary lock from excessive refreshing |
| When slots open | Two missions that publish their release schedule in writing (UAE, Dominican Republic), and the bulk-release vs cancellation distinction |
| Scams | The sanction for a broken scheduling rule lands on **the applicant's account**: ~2,000 cancelled in India, March 2025 |
| India | Kolkata ~60 days vs Hyderabad ~315, plus the one-reschedule rule that makes post choice decisive |
| Third country | The 6 Sep 2025 guidance is *guidance*, not a ban, which is exactly what makes it expensive |
| Emergency | The two-letter medical requirement, and the explicit not-qualifying list (weddings, graduations, conferences) |
| Free vs paid | A queue-length decision rule, published by a paid provider, that tells most readers not to pay |
| What happens on reschedule | Biometrics on the same day as the interview can **cancel the interview automatically** |
| Site not working | Outage vs account restriction vs browser, and why the natural response makes two of them worse |
| Australia | Perth ~15 days vs Sydney ~435, and that the queue is non-citizens because Australia is a VWP country |
| Dropbox | At Bogota and much of Mexico the **waiver queue is longer than the interview queue** |
| DS-160 | The expensive error is administrative, not a refusal: a new form breaks the link to your booking |
| What to bring | No storage facility exists, so a phone at the door can cost the appointment |
| Within 3 months | Three months is the State Department's own publication threshold, so the official table answers the question directly |
| Timeline | The published wait measures one of four stages |
| Nigeria | Abuja ~15 days is among the fastest posts on earth, inverting the assumption |
| Latin America | Mexico's 12:1 internal spread, and Bogota's waiver route at ~398 days |
| Family/group | A group needs *adjacent* slots, so it is a rarer event than four solo searches |
| Pillar | Consolidates all of the above with the current 2025–26 rule changes in one place |

---

## Still open

| # | Page | Type | Cluster | Primary keyword | Why it is not done | Status |
|---|---|---|---|---|---|---|
| F2 | `/us-visa-wait-times/` | Data page, monthly refresh | C2 | us visa appointment wait times by country | **Not a blog post.** A site-root page on a monthly refresh cycle, so it carries an ongoing maintenance commitment. The data now exists (see §6 above) and it is the site's single best link-acquisition asset | ⬜ |
| 25 | Is the $750 Pilot Being Extended Past December 2026? | Post | C3 | 750 expedited visa pilot extended | **Deliberately deferred to November 2026.** Written in August it is speculation, and speculation on a YMYL query is the wrong trade | ⬜ |

---

## Rewrites of existing posts

| # | Post | Problem | Action | Status |
|---|---|---|---|---|
| R1 | `/blog/us-visa-appointment-world-cup-2026-guide/` | Event finished 19 July 2026; page still written in the future tense and telling readers to book for it | Reframed as aftermath: a dated note at the top, a new title, H1, meta and schema headline, and an opening that tells holders of surplus appointments to cancel properly rather than no-show. Evergreen B-1/B-2 process retained. URL kept | ✅ 2026-08-19 |
| R2 | `/blog/us-visa-appointment-dubai-fast-2026/` | Written March 2026, before both the suspension and the platform migration. Describes a booking flow that has changed | Related card repointed at the new Abu Dhabi post. Body prose still describes the pre-migration flow and should be refreshed against N0 | ⬜ |
| R3 | `/blog/us-visa-appointment-canada-guide-2026/` | Prose never rewritten. 300 impressions, 0 clicks, pos 50.3 | Leave the prose. Zero clicks at position 50 is statistically expected. Revisit only if position improves | ⬜ |
| R4 | The three pre-2026-08-19 posts carrying a `.compare` table | "Costs exclude the US$185 MRV fee, which everybody pays" is now incomplete | All 21 new posts use the corrected wording. The three older posts still carry the old line and should be amended to point at `us-visa-integrity-fee-250` once it publishes on 2026-08-22 | ⬜ |

---

## 💀 Killed

| # | Title | Why |
|---|---|---|
| 6 | How Many Times Can You Reschedule a US Visa Appointment? | The published `reschedule-us-visa-appointment-earlier` already carries the per-country allowances and the run-out consequences. A second page splits the query |
| 8 | Why Canada Has the World's Longest US Visa Waits | Fourth page on "US visa appointment Canada". The data is used inside the other wait-time posts instead |
| 12 | Best Time of Day to Check for US Visa Appointment Slots | Merged into #5 `when-do-us-visa-slots-open`. Same intent, same SERP |
| 13 | Which Embassies Offer the $750 Expedited Interview? | F1 carries the participating list and 6b owns the Canada half |
| 16 | US Visa Appointment Wait Times: UAE and the Gulf | Absorbed by `us-visa-appointment-abu-dhabi`, which covers the UAE with a live news hook |

---

## Backlog — pull forward as findings warrant

- What's the Average Wait Time for a US Visa Appointment? *(C2 — folds into F2)*
- US Visa Appointment Cancellations: How to Grab Released Slots *(C1 — overlaps `when-do-us-visa-slots-open`; only worth it as original data)*
- Is There a "Secret Time" to Find Early US Visa Appointments? *(C1 — already answered inside `when-do-us-visa-slots-open`)*
- Do Visa Agents Really Get Earlier Appointment Dates? *(C4 — ⚠️ reframe: consumer evaluation, never a B2B offering)*
- Understanding US Visa Categories: B1/B2, F-1, H-1B *(C5)*
- Biometric / VAC Appointment Requirements *(C5 — partly covered by `what-happens-when-you-reschedule-us-visa`)*
- Common Reasons for Visa Interview Denials *(C5)*
- How to Track Your Visa Application Status *(C5)*
- Which Scheduling Portal Does Your Country Use? *(C1 — real information gain, thin standalone volume. It is a section of the pillar, not a page)*

**Rule:** four thin posts on one query cannibalise each other and dilute the domain. One deep post
wins the cluster.

---

## Post inventory

| Slug | Category | Published | Primary keyword |
|---|---|---|---|
| 20 scheduled posts | see table above | ⏳ 2026-08-22 to 2026-09-10, one per day | see table above |
| `us-visa-paid-expedite-canada` | expedite | 2026-08-19 | us visa paid expedite canada |
| `us-visa-expedited-appointment-750` | expedite | 2026-08-12 (updated 2026-08-19) | us visa expedited appointment 750 |
| `reschedule-us-visa-appointment-earlier` | rescheduling | 2026-08-19 | reschedule us visa appointment earlier |
| `is-us-visa-slot-booking-legit` | trust | 2026-08-11 | are us visa slot booking services legit |
| `us-visa-appointment-world-cup-2026-guide` | basics | 2026-06-29 (rewritten 2026-08-19) | world cup 2026 us visa |
| `us-visa-appointment-canada-guide-2026` | wait-times | 2026-06-23 | us visa appointment canada |
| `us-visa-appointment-dubai-fast-2026` | wait-times | 2026-03-16 | us visa appointment dubai |
