# SEO — Easy Visa Booking

Single home for every SEO plan, decision, and running log for `easyvisabooking.com`.

**Created:** 2026-08-11 · **Baseline health score:** 55/100 · **Target:** 78 by 2026-10-31

---

## Files in this folder

| File | What it is | Update cadence |
|---|---|---|
| [`01-fix-plan.md`](01-fix-plan.md) | Everything broken, ordered by dependency. Raises the audit score from 55. Finite — it ends when done. | As items ship |
| [`02-growth-plan.md`](02-growth-plan.md) | Keywords, content clusters, new pages, backlinks, measurement. **Living document — never "finished".** | Weekly + on any new finding |
| [`03-content-queue.md`](03-content-queue.md) | The actual publishing queue: what gets written, in what order, targeting what. | Weekly |
| [`04-changelog.md`](04-changelog.md) | Running log of what shipped, what moved, and every new finding as it surfaces. | Every session |
| [`research/`](research/) | Source material — topic lists, exports, competitor notes. | As added |

Raw audit output lives in [`../easyvisabooking.com-audit/`](../easyvisabooking.com-audit/) — the full report,
per-category findings, ready-to-paste JSON-LD, and screenshots. It is the evidence base for `01-fix-plan.md`.

---

## Hard constraints — read before writing anything

These override every SEO recommendation, including ones in the audit. Full context in `README.md`
(project root) → Content Guidelines.

1. **Never describe automation.** No auto-booking, bots, "24/7 monitoring", "checks every few seconds",
   or any system acting on the government portal. Describe outcomes and the team.
2. **No agent / travel-agent / bulk / white-label / reseller offering** anywhere on the site.
3. **Never claim a guaranteed slot or date.** The site's existing "we cannot guarantee a date" language
   stays, and should be repeated in new content.
4. **No invented testimonials, reviews, or `AggregateRating` schema.** Real, attributable, or nothing.

Reason: payment runs through a Chrome extension and Stripe underwrites the business off this website.
Automated access to a US Government portal and B2B aggregation are both Stripe restricted-business
triggers. A violation risks decline or account freeze — a bigger loss than any ranking gain.

**Consequence for the audit:** its Phase 3.6 recommendation to reinstate `/for-agents/` and its
"B2B/Agent Booking" content cluster are **rejected**, not deferred. Do not resurface them.

---

## Accepted risks — declined on 2026-08-07, re-confirmed 2026-08-11

These are real, scored SEO gaps that will not be fixed. Recorded so nobody re-raises them as
discoveries, and so the score ceiling is understood.

| Gap | Audit severity | What it costs |
|---|---|---|
| No verifiable legal entity (company no., registered address, jurisdiction) | HIGH | Caps Content Quality and Trust. `/terms/` promises registration details it does not deliver — a broken promise reads worse than silence. |
| No testimonials, reviews, or social proof | HIGH | Largest conversion gap in a scam-heavy niche. Homepage still contains `<!-- Testimonial section removed -->`. |
| No `tel:` link anywhere | MEDIUM | Schema and a homepage trust badge both promise phone support that does not exist. |

**Combined cost: roughly 6–8 points of the 100-point score, permanently.** The realistic ceiling with
these declined is ~82–84, not 90+. Everything in `01-fix-plan.md` is scoped to route around them.

Revisit trigger: if Stripe underwriting comes back with questions, the legal-entity item must be
reopened — Stripe expects the site's business name to match the Stripe account.

---

## Update protocol

`02-growth-plan.md` and `03-content-queue.md` are living. Whenever new information arrives —
a Google update, a policy change at State Dept, a competitor move, fresh GSC data, a new topic list:

1. Append the finding to `04-changelog.md` under today's date, with its source.
2. Amend the affected section of `02-growth-plan.md` in place.
3. Re-order `03-content-queue.md` if the finding changes priority.
4. Bump the `Last updated` line at the top of every file touched.

Never delete a superseded plan — strike it through and note why. The reasoning is worth more than
the tidiness.
