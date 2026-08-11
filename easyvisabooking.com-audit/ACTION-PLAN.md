# Action Plan — easyvisabooking.com

Ordered by dependency, not just severity. Items early in the list **unblock** later ones;
doing them out of order wastes effort.

**The through-line:** you cannot rank pages Google has not indexed, you cannot convert
traffic that does not trust you, and you cannot outrank government portals for queries they
own. Phases 1–3 address those three in that order.

---

## Phase 1 — Week 1: Get the money pages into Google

*Nothing else in this plan matters until these pages exist in the index. Seven of your 14
pages — including every service page — have never been crawled.*

### 1.1 Resubmit the sitemap [CRITICAL]
Google's copy was last processed **2026-06-23** and contains **10 URLs**; the live file has 14.
- GSC → Sitemaps → enter `sitemap.xml` → Submit.
- **Verify:** GSC Sitemaps reports `submitted: 14` and a `last_submitted` date after today.
- **If it still reads 10 in 14 days:** check for a stale edge-cached `sitemap.xml` on Vercel.

### 1.2 Request indexing for the 7 unknown URLs [CRITICAL]
GSC → URL Inspection → each URL → Request Indexing:
```
/services/
/services/us-visa-appointment-canada/
/services/us-visa-appointment-toronto/
/about/
/terms/
/privacy/
/refund-policy/
```
- **Verify:** re-inspect in 14 days; coverage state should move off "URL is unknown to Google."
- **Do NOT use the Indexing API for these** — it officially supports only `JobPosting` and
  `BroadcastEvent`.

### 1.3 Fix the three broken service links [CRITICAL]
`/services/` and the homepage both link to `us-visa-appointment-dubai/`, `-uae/`, and
`-australia/`. All three return **404** and are simultaneously **robots.txt-Disallow'd**.

Pick one path per location — do not mix:
- **Building them:** delete the three `Disallow` lines, ship pages at 200, add to sitemap.
  *Recommended for Dubai* — you already have a ranking Dubai blog post to link into.
- **Abandoning them:** remove the links from `/services/` and the homepage, delete the three
  `Disallow` lines (so Google can actually process the removal), serve **410 Gone**, and fix
  the `/services/` meta description, which currently advertises all three.
- **Verify:** every outbound service link resolves 200; no URLs under "Indexed, though
  blocked by robots.txt" in GSC.

### 1.4 Fix `lastmod` [HIGH]
Every URL claims the identical `2026-08-07`. Uniform templated values get discounted by Google.
Emit true per-page modification dates, or **omit `lastmod` entirely** — omitting beats faking.
Drop `priority` and `changefreq` while you are in there; Google ignores both.

### 1.5 Fix the production schema placeholder [CRITICAL — 2 minutes]
Homepage `Organization.sameAs` contains the literal string
`"https://t.me/YourTelegramChannel"`. Your real channel is `https://t.me/earlyusvisabooking`.
Ready-to-paste fix: `findings/schema-generated/01-...jsonld`.

### 1.6 Fix the favicon case bug [HIGH — 5 minutes]
`brand-logo-real.PNG` is 200; `brand-logo-real.png` is 404. Vercel is case-sensitive. Eight
pages reference the lowercase path. Also add a `/favicon.ico` fallback.

**Leading indicator for Phase 1:** GSC "Pages" report shows indexed count rising from 7
toward 14. Watch this weekly — no re-audit needed.

---

## Phase 2 — Weeks 2–3: Earn the click once you're visible

*Indexation gets you into the auction. Trust decides whether anyone converts. This is a
category where visitors actively look for reasons to distrust you — and your best trust
assets are currently hidden.*

### 2.1 Move the government-affiliation disclaimer above the fold [HIGH]
You already have well-worded copy: *"We are not affiliated with… the U.S. Government."*
It sits in the footer ~9,000px down. **Move it into the hero.** Counter-intuitively, saying
"we are not the government" *increases* conversion here — it is the first question every
visitor has, and answering it immediately separates you from operators who obscure it.

### 2.2 Publish real legal identity [HIGH]
`/terms/` promises *"Our registered details are set out at the top of this page and on our
About page"* — and then does not provide them. A broken promise about registration details is
worse than silence. Add company registration number, registered address, and jurisdiction.

### 2.3 Add genuine social proof [HIGH]
The homepage contains `<!-- Testimonial section removed -->`. You have zero reviews,
testimonials, or case studies in a scam-heavy niche.
- Collect real, attributed client outcomes (name or initials + city + date + result).
- Show the confirmation screenshots you currently describe as "available on request."
- **Do not** add `Review`/`AggregateRating` schema until genuine on-page reviews exist —
  self-serve review markup violates Google policy.

### 2.4 Make pricing visible [MEDIUM]
The `$100 starting fee` currently exists **only inside JSON-LD** and never in visible text.
Structured data must describe what is on the page. Put the price on the page — your
"no upfront fee / pay only on success" model is a competitive advantage being hidden.

### 2.5 Reconcile the contradictory country lists [HIGH]
Up to six different, mutually inconsistent lists of which countries you serve appear across
Organization description, Organization `areaServed`, Service `areaServed`, About page schema,
visible FAQ text, and a homepage subheading. Pick one authoritative list matching pages that
actually exist. Entity clarity is what AI engines and Google both need most from you.

### 2.6 Reconcile the two different FAQ sets [HIGH]
The homepage's `FAQPage` JSON-LD and its visible FAQ accordion contain **entirely different
questions and answers**. Make the schema describe the visible content.

### 2.7 Add a phone number, or stop promising one [MEDIUM]
Schema and a homepage trust badge promise phone support; no `tel:` link exists anywhere.

### 2.8 Fix mobile overflow and the WhatsApp overlap [MEDIUM]
48px horizontal overflow on home, 22px on services-canada; fixed WhatsApp button overlaps
body copy on `/contact/` mobile.

**Leading indicator for Phase 2:** CTR in GSC for `/` and `/contact/` (currently 11.4% and
9.1%) should hold or rise as impressions grow — if CTR falls while impressions rise, the
trust work is not landing.

---

## Phase 3 — Month 2: Authority, and aiming at winnable SERPs

*This is the binding constraint. Phases 1–2 are necessary and insufficient.*

### 3.1 Stop targeting unwinnable queries [HIGH — strategic]
"canada us visa appointment" and its variants are owned by `ais.usvisa-info.com` (the actual
booking portal), `travel.state.gov`, and `ca.usembassy.gov`. No commercial page displaces
those. Redirect effort to the adjacent winnable cluster: **rescheduling mechanics, slot-release
timing, service legitimacy, cost transparency** — where SERPs are blog- and forum-dominated.

**Do not rewrite `/blog/us-visa-appointment-canada-guide-2026/` to chase CTR.** Its 300
impressions / 0 clicks is a *position* problem (expected clicks at position 50 is under 1),
not a snippet problem. The page is 2,745 words and scored 84/100. Rewriting it fixes nothing.

### 3.2 Begin link acquisition as a standing workstream [CRITICAL]
The domain sits at the bottom of Common Crawl's authority distribution with no discoverable
referring domains. Legitimate paths for this niche:
- **Digital PR around visa wait-time data** — highest leverage; you have proprietary
  operational data no government portal publishes.
- University international-student offices; immigration and expat community resources;
  HR/global-mobility publications; relocation and travel press.

**Avoid** — flagged Critical risk given scrutiny in this niche: PBNs, paid link networks,
mass guest posting, comment and forum spam.

### 3.3 Configure the free Moz API [HIGH — 15 minutes, unblocks measurement]
https://moz.com/products/api — free tier, 2,500 rows/month. It is the only free source that
returns referring-domain count and spam score, both currently blank. You cannot manage link
acquisition you cannot measure. Add `moz_api_key` to `~/.config/claude-seo/backlinks-api.json`.
Also worth adding: **Bing Webmaster Tools** (free) — it feeds Microsoft Copilot citations.

### 3.4 Resolve the Canada/Toronto duplication [HIGH]
The two location pages share **65–75% verbatim text**. Toronto is inside Canada, so they
compete directly. This is the doorway-page pattern — and the template you would replicate if
you scale locations. Either differentiate genuinely (consulate-specific wait times, local
detail) or consolidate to one.

**Quality gate before scaling locations:** at 30+ location pages, enforce 60%+ unique content
per page. At 50+, stop and justify. On the current template you would breach both.

### 3.5 Add author bylines with credentials [HIGH]
Zero bylines on any blog post. For YMYL content on consulate and AIS mechanics, named authors
with stated relevant experience are a direct Expertise signal.

### 3.6 Decide the B2B question [MEDIUM]
`/for-agents/` held **position 11.2** — your best average position anywhere — and was folded
into a 507-word consumer page with no B2B content. SERPs for agent/B2B queries show near-zero
government competition and real competitors ranking. Either reinstate a proper B2B page (in
the sitemap, linked from nav) or consciously drop the audience. Also collapse the 2-hop
`/for-agents` → `/for-agents/` → `/services/` chain to one hop.

### 3.7 Build the content pillar [MEDIUM]
`/services/` (~507 words) is thinner than both its children and cannot carry hub duty. Build
`/blog/us-visa-appointment-guide/` as an informational pillar; rebuild `/services/` separately.
Full four-cluster architecture and internal link matrix in `findings/cluster.md`.

**Leading indicator for Phase 3:** referring domain count (once Moz is configured) and average
position on the *rescheduling* query cluster specifically — not the head terms.

---

## Phase 4 — Ongoing

### 4.1 Performance — do this, but do not over-prioritize it
CrUX field data is unavailable (insufficient traffic), so Google cannot currently compute your
CWV ranking signal. **CWV is a weak lever here relative to indexation, trust, and links.** That
said, the images are genuinely bad and cheap to fix:
- `canada-visa-hero-banner.png` is **869KB (94% wasted)**; `breadcrumb.png` is **421KB**.
  Convert to WebP/AVIF. This alone should move mobile LCP substantially from 7.2–11.7s.
- Add `width`/`height` to all images (100% currently lack them) and `fetchpriority="high"` to
  the LCP image.
- Investigate desktop CLS 1.039 on home / 0.501 on blog — likely the `#spinner` overlay.
- gtag.js costs up to 656ms main-thread. Ahrefs analytics is negligible (~4ms) — leave it.

### 4.2 Security headers [HIGH]
Only HSTS present. Add via `vercel.json`: `X-Content-Type-Options: nosniff`,
`Referrer-Policy: strict-origin-when-cross-origin`, `X-Frame-Options: SAMEORIGIN`,
`Permissions-Policy`. Add CSP only after auditing gtag.js and Ahrefs — and **confirm analytics
still fires afterwards**, which is the step people skip and regret. Not a ranking factor;
it matters because you handle passport and payment data.

### 4.3 Complete the schema work [MEDIUM]
Seven ready-to-paste files in `findings/schema-generated/`: `@id` entity linking (Organization
is currently duplicated as 7+ anonymous islands), `BlogPosting.image` (missing on all three
posts), `BreadcrumbList` (absent on 6 pages), `Service.offers`, and `ContactPoint` for
`/contact/` (which currently ships zero JSON-LD).

**Leave the existing `FAQPage` blocks alone.** Google retired FAQ rich results for all sites on
2026-05-07, so they no longer produce a SERP feature — but they are valid, harmless, and
removing them costs effort for no gain. Just do not add new ones expecting SERP benefit.

### 4.4 Social/OG meta [MEDIUM]
No `og:description` or `twitter:card` sitewide; homepage `og:image` 404s; no other page has
`og:image` at all. You promote via WhatsApp and Telegram — link previews are a direct
acquisition surface.

### 4.5 Configure GA4 [LOW — unblocks reporting]
Add `ga4_property_id` to `~/.config/claude-seo/google-api.json` to unlock organic traffic
reporting in future audits.

### 4.6 llms.txt [LOW — genuinely optional]
Absent (404). Honestly: Google does not use it and no major AI vendor has confirmed production
use. Cheap to add, speculative benefit. **Do not let it displace trust and authority work.**

### 4.7 Set a drift baseline
Run `/seo drift baseline https://www.easyvisabooking.com` now, so future changes are diffable
and regressions surface without a full re-audit.

---

## What NOT to do

Explicitly flagged to prevent wasted effort:

| Don't | Why |
|---|---|
| Rewrite the Canada blog guide for CTR | 0 clicks at position 50 is expected; it is a position problem, not a snippet problem |
| Add internal links to fix indexation | The unindexed pages already have 8 homepage links; `/blog/` is indexed with none. Not the cause |
| Remove the existing FAQPage schema | Valid and harmless; removal is pure cost |
| Add new FAQPage for SERP benefit | Google retired FAQ rich results for all sites on 2026-05-07 |
| Add `HowTo` schema to `/how-it-works/` | Deprecated September 2023 |
| Add Review/AggregateRating schema | No genuine on-page reviews exist; self-serve markup violates policy |
| Chase head terms like "us visa appointment" | Owned by the government portal itself |
| Buy links / guest post at scale | Elevated penalty risk in this niche |
| Prioritize Core Web Vitals | No field data exists, so it is not currently a ranking signal for you |
| Optimize Ahrefs analytics | 3.7KB, ~4ms. Irrelevant |
| Chase the "striking distance" positions | `/services/` pos 1.0, `/how-it-works/` pos 4.0, `/blog/` pos 5.0 are built from 1–4 impressions and vanish between periods. Noise, not opportunity |
| Read rising impressions as progress | Impressions rose 196% while CTR fell 3.26%→1.47%. More visibility at position 41–97 earns nothing |

---

## Sequencing summary

```
Week 1     Phase 1  → get indexed          (unblocks everything)
Weeks 2-3  Phase 2  → earn trust           (unblocks conversion)
Month 2    Phase 3  → authority + strategy (the binding constraint)
Ongoing    Phase 4  → performance, schema, monitoring
```

If only three things get done: **1.1 + 1.2** (sitemap + request indexing),
**1.3** (broken service links), and **2.1** (disclaimer above the fold).
