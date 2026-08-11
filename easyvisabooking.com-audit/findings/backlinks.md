# Backlink Profile — easyvisabooking.com

**Audit date:** 2026-08-11
**Data tier: 0** (Common Crawl web graph + verification crawler only — no Moz, no Bing Webmaster Tools configured)
**Tools run:** `commoncrawl_graph.py easyvisabooking.com --json` ; `backlinks_auth.py --check --json`
**Tools NOT run:** `verify_backlinks.py` — no candidate backlink URLs exist anywhere in this audit's raw data (no known-links file, no third-party mention list, no Moz/Bing inbound-link export). There is nothing to verify yet.
**Validation:** `validate_backlink_report.py` run against the collected data → **PASS**, 0 issues.

---

## Headline

**No numeric Backlink Health Score is reported. INSUFFICIENT DATA.**

Only 1 of the 7 scoring factors (domain quality distribution, and only a weak proxy for it) has any data source at Tier 0. Referring domain count, anchor text naturalness, toxic link ratio, link velocity, follow/nofollow ratio, and geographic relevance all have **zero** available data sources without Moz, Bing, or DataForSEO. Producing a score here would be fabrication. This is deliberate, not a gap in effort — see "What upgrading unlocks" below for the fastest path to real numbers.

---

## Finding 1: Domain is present in Common Crawl's web graph but at the bottom of the authority distribution

**Severity: Info** (context-setting, not actionable on its own)
**Evidence (confidence: 0.50 — Common Crawl, domain-level, quarterly snapshot, source: https://commoncrawl.org/web-graphs):**

| Metric | Value |
|---|---|
| In crawl | true |
| In rankings | true |
| PageRank (raw) | 3.37 × 10⁻⁸ |
| PageRank rank | 1,213,249 |
| Harmonic centrality (raw) | 17,345,958 |
| Harmonic centrality rank | 377,055 |
| n_hosts | 2 |
| CC release | cc-main-2026-jan-feb-mar |

**Interpretation, held to what the data actually supports:**
- The domain *was* discovered and crawled by Common Crawl's Jan–Mar 2026 web graph, and it clears CC's internal ranking threshold (`in_rankings: true`). That rules out the "totally invisible to crawlers" scenario.
- Both the PageRank rank (~1.2M) and harmonic centrality rank (~377K) place it very low in absolute terms, but **the tool does not return the total host count for this release**, so I cannot responsibly convert those ranks into a percentile. Do not treat any percentile figure for this domain as authoritative unless it's recomputed against the actual corpus size — I have not done that here and won't guess at it.
- `n_hosts: 2` is a domain-level host count from CC's own bookkeeping (almost certainly `www.` + apex), **not** a referring-domain or backlink count. Tier 0 Common Crawl does not extract inbound links or referring domains at all — this field should not be read as link data.
- CC PageRank is influenced by the *entire* link graph (including internal links, sitewide templates, and generic web structure), not solely external backlinks. A low score here is consistent with a new site with minimal external link equity, but it is not direct proof of referring domain count.

**Falsifiability check:** This finding is falsifiable by re-running `commoncrawl_graph.py easyvisabooking.com --json` against a newer CC release and comparing pagerank_rank/harmonic_centrality_rank trend, or by obtaining Moz/DataForSEO referring-domain counts and checking whether they correlate with a rank improvement over time.

**Action:** None required from this finding alone. Track it quarterly as a lagging indicator once real link-building begins — CC web graphs update quarterly, so month-to-month changes here are not meaningful signals.

---

## Finding 2: No referring domain, anchor text, spam, or link-velocity data exists at this tier

**Severity: Critical (structural, not a defect — but it caps what this audit can certify)**
**Evidence (confidence: n/a — absence of data, not a data point):** `backlinks_auth.py --check` confirms Moz and Bing Webmaster keys are both unset; Tier 0 capabilities are limited to "Common Crawl domain-level graph" and "Backlink verification crawler." Common Crawl's Tier 0 output does not expose referring domains, anchor text, or spam scores by design (see `commoncrawl_graph.py --help`: "Legacy no-op; referring domains are not extracted").

**Action:** Do not proceed to build a numeric health score on this data. Configure Moz (free) and/or Bing Webmaster (free) before requesting a scored backlink audit — see "What upgrading unlocks" below.

**Falsifiability check:** Re-run `backlinks_auth.py --check --json` after adding credentials; tier should report 1 or 2 and new capabilities should appear in the `services` block.

---

## Finding 3: No candidate backlinks were available to verify

**Severity: Info**
**Evidence (confidence: n/a):** No known-backlinks file was provided in `easyvisabooking.com-audit/raw/`, and there is no other source in this audit (Moz, Bing, DataForSEO, manual mention list) that could seed `verify_backlinks.py --links <file>`. The script requires an input file of candidate source URLs; none exists, so it was not run.
**Action:** Once any backlink is discovered by any means (a partner site, a directory listing, a press mention, a Moz/Bing export), pass it to `verify_backlinks.py --target https://www.easyvisabooking.com --links <file> --json` to confirm the link is live, dofollow, and not a JS-rendered false negative (per the skill's known "social media marked link_removed" failure mode).
**Falsifiability check:** Trivially re-runnable the moment a candidate list exists.

---

## Finding 4: Zero external link equity is very likely the binding constraint on this site's rankings — more binding than any on-page issue

**Severity: Critical**
**Evidence (confidence: 0.50 CC + cross-referenced against GSC data in CONTEXT.md, confidence: 0.95 GSC — verified access):**
- CONTEXT.md's GSC data shows 90-day average position of **45.2** across all queries, with commercial head terms ("canada us visa appointment", "book us visa appointment canada") sitting at **position 45–80** with **zero clicks** despite reasonable impression volume (e.g., the Canada guide blog post has 300 impressions at position 50.3).
- The site is brand new (first GSC data ~May 2026, so roughly 3 months old at audit time) in **US visa appointment booking** — a YMYL-adjacent, transactional, trust-sensitive niche that is also, per the task brief, heavily populated by scam and low-trust operators. Google's ranking systems apply extra scrutiny to exactly this category, and referring-domain trust signals are one of the primary ways a new entrant differentiates itself from scam sites in this space.
- Common Crawl shows no evidence of meaningful inbound link equity (Finding 1), and there is no known referring domain today (Finding 3).
- **Be blunt, as instructed:** a site sitting at position 45–80 for commercial terms like "us visa appointment canada," with an authority profile this thin, will not move into page-1 contention for those terms through on-page or technical optimization alone, no matter how well `/services/us-visa-appointment-canada/` or the Canada guide blog post is optimized. Referring domains from even a modest number of trusted, topically-relevant sites are very likely required before ranking improvements for competitive commercial terms become achievable. Treat this as the primary bottleneck for the whole site, not a secondary item alongside content and technical fixes.
- This is a claim about *relative priority*, not a claim that on-page work is worthless — `/seo content` and `/seo technical` fixes remain necessary preconditions (a site with zero backlinks and bad on-page signals ranks even worse), but they are not sufficient on their own in this niche.

**Falsifiability check:** This is falsifiable in two ways: (a) if position for these head terms improves substantially over the next 1–2 GSC reporting cycles without any new referring domains being acquired, the "binding constraint" claim would be weakened; (b) once Moz/Bing/DataForSEO data exists, a near-zero referring-domain count alongside continued sub-page-1 rankings would confirm it, while a nontrivial referring-domain count with continued flat rankings would falsify it (pointing instead to relevance/quality/toxic-link issues).

**Action:** Prioritize durable link acquisition (Finding 5) at least as highly as any remaining content/technical work. Recommend the user run `/seo content` and `/seo technical` for E-E-A-T and crawlability, but do not expect ranking movement on competitive terms from those alone.

---

## Finding 5: Recommended link acquisition paths (durable, low penalty-risk)

**Severity: High (opportunity, not a defect)**
**Confidence:** These are qualitative recommendations based on established, publicly-documented durable link-building practice for this niche, not derived from a data source, so they carry no confidence score — they are strategic advice, not measurements.

Legitimate, on-topic paths appropriate to an immigration/visa-appointment service, roughly in order of effort-to-authority payoff:

1. **University international student / study-abroad offices.** Many universities maintain curated resource pages for international students on visa logistics; a genuinely useful, non-promotional resource (e.g., a wait-time data page, a step-by-step interview prep guide) is a plausible link target. Outreach should lead with the resource, not the commercial service.
2. **Immigration and expat community resources.** Established expat-forum wikis, immigration-lawyer blogs' resource sections, and relocation-guide sites that already link out to visa-process explainers are natural, topically-relevant candidates — but link swaps or "you link to me, I'll link to you" arrangements should be avoided (see Finding 6).
3. **Relocation and corporate/HR global-mobility publications.** Global-mobility and HR-tech publications regularly cover visa-process friction for employers moving staff internationally; a well-sourced guest contribution or cited data point is a legitimate, on-topic placement.
4. **Genuine digital PR around visa wait-time data.** This is the highest-leverage path for a YMYL/scam-heavy niche: publishing original, sourced data (e.g., aggregated AIS/CGI interview wait times by consulate, sourced and dated) creates something journalists, immigration bloggers, and relocation publications have a real reason to cite. This is the single most defensible tactic listed here because the links are earned by genuinely useful information rather than solicited.
5. **Travel and visa-news publications** that cover consular policy changes (e.g., World Cup 2026 travel-visa coverage, which the site already has a blog post on) — pitching original data or expert commentary tied to a live news hook is a realistic, low-cost path.

**Action:** Treat link acquisition as its own workstream with its own timeline (months, not weeks). Start with #4 (data-driven digital PR) since it produces an asset (a citable page) that supports #1–3 and #5 simultaneously.

**Falsifiability check:** Success is measurable — track referring domain count via Moz/Bing/DataForSEO before and after each campaign; if referring domains do not increase over 60–90 days of active outreach, revisit the approach.

---

## Finding 6: Explicit warning against toxic/high-risk link tactics common in this niche

**Severity: Critical (risk mitigation)**
**Evidence:** Qualitative, based on well-documented Google Search spam policy enforcement patterns in commercial YMYL-adjacent niches; not derived from a measured data source for this specific domain (no toxic links have been detected — none exist to detect at Tier 0).

Given this is a new site in a niche saturated with low-trust and scam operators, Google's spam systems apply elevated scrutiny to exactly the tactics below. A penalty or manual action here would be far more damaging to a 3-month-old site with no track record than to an established domain. Explicitly avoid:

- **Private blog networks (PBNs).** High detection risk; a manual action against a brand-new domain with no earned trust could be effectively fatal to its ranking prospects.
- **Paid link networks / link-buying marketplaces.** Directly against Google's spam policies; common in this niche's competitor set, which raises rather than lowers the risk of being caught in a sweep.
- **Mass/low-quality guest posting** (unrelated sites, spun/AI content, irrelevant niches purely for a link). Produces exactly the kind of unnatural anchor-text and low-relevance-domain pattern that toxic-link detection targets.
- **Comment and forum spam.** Near-zero durable value, high association with scam-site link patterns already common in this space — this is a category Google is specifically primed to distrust in visa/immigration search results.

**Action:** If any past link-building activity (e.g., prior agency work, template purchases) is suspected of using these tactics, that should be investigated before an aggressive new outreach push — cleaning up toxic links is cheaper before new legitimate links are built than after.

**Falsifiability check:** Once Moz Spam Score or DataForSEO toxic-link data is available, this can be checked directly. At Tier 0, this is a preventive warning, not a detected finding — label it as such if it is repeated elsewhere in the audit.

---

## What upgrading credentials would unlock

**Moz API — free tier, 2,500 rows/month — https://moz.com/products/api**
- Domain Authority (DA) / Page Authority (PA)
- Spam Score (toxic-link proxy)
- Referring domain count and link counts
- Anchor text distribution
- Top linking pages
- Confidence level for this data, if configured: 0.85 (per skill convention)
- Rate limit note: 1 request per 10 seconds is enforced by the bundled script — plan calls accordingly once configured.

**Bing Webmaster Tools — free — https://www.bing.com/webmasters**
- Inbound link list for *verified* properties (easyvisabooking.com would need to be added and verified in Bing Webmaster)
- Confidence level for this data, if configured: 0.70 (per skill convention)
- Caveat: only usable for properties the user controls/verifies in the same Bing account — not usable for arbitrary competitor comparison.

**Recommendation:** Configuring Moz's free tier is the single highest-leverage next step for this audit category — it is the only free source that returns a referring-domain count and a spam score, both of which are currently completely blank. Bing Webmaster is a reasonable second step since it's free and the site is presumably already indexed there, but its data is scoped to properties the user has verified.

If neither is configured, the fallback is the DataForSEO extension (`./extensions/dataforseo/install.sh`) for Tier 3, premium, highest-fidelity data (confidence: 1.00).

---

## Cross-skill delegation (not duplicated here)

- **E-E-A-T / content trust signals:** run `/seo content <url>` — particularly relevant given the YMYL nature of this niche; content trust signals and link acquisition reinforce each other.
- **Crawlability / technical foundation:** run `/seo technical <url>` — necessary precondition, not a substitute, for the link-acquisition priority above.

---

## Summary of confidence levels used in this report

| Data point | Source | Confidence |
|---|---|---|
| CC PageRank / harmonic centrality (domain-level) | Common Crawl web graph (quarterly) | 0.50 |
| GSC position/impressions data (cited from CONTEXT.md) | Google Search Console API, verified access | 0.95 |
| Referring domains, spam score, anchor text, link velocity, follow/nofollow, geo relevance | No source available at Tier 0 | N/A — not reported |
| Link acquisition recommendations | Qualitative strategic guidance | N/A — advice, not measurement |
