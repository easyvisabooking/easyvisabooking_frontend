# Visual / Mobile UX Findings — easyvisabooking.com

Captured via Playwright (Chromium). Desktop = 1920×1080, Mobile = 390×844 (device scale factor 2). Pages: `/`, `/services/us-visa-appointment-canada/`, `/blog/us-visa-appointment-canada-guide-2026/`, `/contact/`, plus `/services/` (for the broken-location-link visual check requested by the coordinator).

All screenshots live in `easyvisabooking.com-audit/screenshots/` (paths below are relative to that directory unless stated otherwise). Raw DOM diagnostics (image attrs, tap-target geometry, overlay geometry, trust-term text scan) were dumped to `easyvisabooking.com-audit/raw/visual_dom_analysis.json`.

---

## 1. Mobile above-the-fold value proposition

**Severity: Medium (content/positioning issue, not a technical defect)**

Evidence: `home_mobile.png`. At 390×844 the fold shows: logo, hamburger icon, H1 "Get Your US Visa Appointment Booked Without the Wait.", one paragraph of body copy, a red "Book Your Appointment" CTA button, a secondary "See How It Works" link, a WhatsApp bubble, and carousel arrows. `services-canada_mobile.png` shows H1 "US Visa Appointment Canada – Get Earlier Dates Fast (2026 Update)," intro copy, and the line "No upfront payment • Pay only successful booking" — but no visible CTA button in that same viewport (the "Check Availability Now" button sits at DOM top=898px, just below the 844px fold per `visual_dom_analysis.json`).

Assessment against "what is this, what does it cost, why trust it":
- **What is this**: answered clearly on both pages (US visa appointment booking/rescheduling assistance).
- **What does it cost**: NOT answered on either fold. `pricingMentioned` is `false` site-wide on the homepage (no $, no "price/fee/cost" language above the fold), and the services-canada page only signals cost indirectly via "No upfront payment • Pay only successful booking" — no number, no range. An anxious applicant researching a paid intermediary in a scam-prone niche has to click through or contact the business to learn the price at all.
- **Why trust it**: NOT answered on either fold. No testimonial, no review count, no security/payment badge, no "X appointments booked" counter, and no government-affiliation disclaimer is visible without scrolling (see Finding 2). The only trust cue is the WhatsApp icon (implies a real human is reachable).

Fix: Add a one-line trust/price cue directly under the H1 subhead on both home and service pages — e.g. "Flat fee, pay only after your appointment is confirmed — see pricing" (linked) plus a compact disclaimer chip ("Independent service — not affiliated with the U.S. Government") pinned near the hero, not just in the footer.

Falsifiability: Re-screenshot `/` and `/services/us-visa-appointment-canada/` at 390×844 after launch; if a $ figure/fee range and a disclaimer/trust line are visible in that single viewport screenshot, this finding is resolved.

---

## 2. No government-affiliation disclaimer above the fold (any page)

**Severity: High**

Evidence: The disclaimer text *does* exist — confirmed in `services-index_desktop_full.png` and `services-index_mobile_full.png`: "Easy Visa Booking is an independent appointment scheduling assistance service. We are not affiliated with, endorsed by, or acting on behalf of the U.S. Government, the U.S. Department of State, any U.S. Embassy or Consulate, CGI Federal, or the AIS portal…" — but it lives in the red bar at the very bottom of the global footer. On the homepage that footer sits roughly 9,000px down (`home_mobile_full.png`, `home_desktop_full.png`); none of the four target pages' fold screenshots (`home_mobile.png`, `services-canada_mobile.png`, `blog-canada-guide_mobile.png`, `contact_mobile.png`) show any disclaimer text. A `/services/canada/`-style FAQ item titled "Is this an official government service?" also exists but is inside a collapsed accordion far below the fold (DOM top ≈8,166px desktop / similarly deep on mobile per `visual_dom_analysis.json`), so it requires both scrolling and a click to read.

This matters specifically because the category is scam-heavy: a user who lands from a paid/organic search for "US visa appointment" and doesn't scroll ~9,000px will never see the one piece of copy that distinguishes this business from a phishing/scam operation impersonating government services.

Fix: Add a short, persistent disclaimer above the fold — e.g., a thin banner strip under the header ("Independent scheduling assistance — not affiliated with the U.S. Government or CGI Federal") on every page, not just the footer. This is a two-line CSS/template change reused site-wide.

Falsifiability: Screenshot each page at 390×844 with zero scroll; disclaimer text (or a link directly to it) must be pixel-visible in that frame.

---

## 3. Zero third-party trust signals (testimonials, reviews, badges) found anywhere on the homepage

**Severity: High**

Evidence: `visual_dom_analysis.json` → homepage `trustTermsFound` (full-page `innerText` scan, not just above-the-fold): `["refund", "secure", "official", "whatsapp", "privacy policy"]`. Terms explicitly searched for and **not found anywhere on the page**: `testimonial`, `review`, `trustpilot`, `bbb` / `better business bureau`, `money back`, `licensed`, `registered`. No `tel:` links exist on any of the four pages (`telLinks: []` throughout); the only contact channels are `mailto:contact@easyvisabooking.com`, WhatsApp, and Telegram (`@earlyusvisabooking`), all confirmed only in the footer, never above the fold.

For a paid intermediary in a category associated with scams, the absence of any attributed testimonial, review count, or recognizable trust badge (Trustpilot, BBB, payment-processor logo, etc.) — combined with no phone number — leaves WhatsApp/Telegram/email as the sole legitimacy signals, and those are only visible after a full scroll to the footer.

Fix: Add at least one attributed testimonial with a name/photo/case detail, and a real business phone number, ideally displayed near the hero or in a persistent trust strip. If testimonials don't exist yet, a specific, verifiable claim (e.g., "500+ appointments booked since 2025") is a lower-effort interim step — but only if verifiably true.

Falsifiability: Re-run the same `innerText` term scan against the shipped homepage; presence of "testimonial"/"review" text tied to a named person, or a `tel:` link, resolves this finding.

---

## 4. Horizontal scroll on mobile — home and services-canada pages

**Severity: Medium**

Evidence: `visual_dom_analysis.json`:
- Home mobile: `scrollWidth: 438` vs `viewportWidth: 390` → `horizontalOverflow: true` (48px overflow).
- Services-canada mobile: `scrollWidth: 412` vs `viewportWidth: 390` → `horizontalOverflow: true` (22px overflow).
- Blog and Contact mobile: no overflow (`scrollWidth === viewportWidth`).

This is a genuine, measured layout bug (not a false positive from a fixed-position element), confirmed by comparing `document.documentElement.scrollWidth` to `window.innerWidth` after full page load + 1.5s settle. The hero carousel (full-bleed image, prev/next arrow buttons positioned at the viewport edges) is the most likely culprit on both pages since it's the shared component between the two affected pages.

Fix: Audit the hero carousel and any full-bleed containers for `width: 100vw` or negative margins that don't account for the vertical scrollbar / box-sizing on mobile; add `overflow-x: hidden` on `body` as a stopgap, but fix the root element causing the extra 22–48px first.

Falsifiability: `document.documentElement.scrollWidth > window.innerWidth` at 390px viewport width should return `false` on both pages after the fix.

---

## 5. CLS risk — every image on every page lacks explicit width/height attributes

**Severity: Medium-High**

Evidence: `visual_dom_analysis.json`, aggregated across all four pages: 8 images on home, 14 on services-canada, 2 on blog-canada-guide, 1 on contact — **100% have `widthAttr: null` and `heightAttr: null`** (relying entirely on CSS for sizing). This includes the hero carousel image (`carousel-2.jpg`, natural size 1920×1080, rendered at 390×844 on mobile) — the likely LCP element on the homepage. Without explicit `width`/`height` (or `aspect-ratio` in CSS), the browser cannot reserve layout space before the image downloads, risking CLS especially on slower mobile connections.

Fix: Add explicit `width` and `height` attributes (or a CSS `aspect-ratio`) to every `<img>` tag, starting with the hero/carousel images on `/` and `/services/us-visa-appointment-canada/` since those are the LCP candidates.

Falsifiability: Inspect rendered DOM — `img.hasAttribute('width') && img.hasAttribute('height')` should be `true` for all `<img>` elements; confirm via Lighthouse/PageSpeed CLS score improvement.

---

## 6. `/services/` — large broken/empty content block between location cards and footer

**Severity: Medium-High**

Evidence: `services-index_desktop_full.png` and `services-index_mobile_full.png`. Below the "Choose Your Location" section (which shows only 3 cards: Canada, Toronto — both live/clickable — and Dubai, greyed out with a "Coming Soon" badge, not a broken link), there is roughly 1,200–1,500px of dead white space on desktop, followed by an empty pale-lavender rectangle with no content, before the footer begins. This pattern repeats on mobile. This strongly suggests a component (stats counter, testimonial carousel, or additional location cards) failed to render — either a missing image/data source or a broken conditional.

Note on the coordinator's flagged context (5 location pages, 3 returning 404 and blocked by robots.txt): only **3** location cards actually render on `/services/` (Canada, Toronto, Dubai-disabled) — no UAE or Australia cards appear at all in this section, so those broken links are not being surfaced to users through this card grid; they must be linked elsewhere (sitemap/internal blog links) not visible in this capture. The empty content block itself, however, is a clear, self-contained visual defect independent of the 404/robots issue.

Fix: Investigate the CMS/template block rendering between the location grid and the footer on `/services/` — likely a stats/testimonial section with no data bound, or a broken conditional leaving an empty container in the DOM. Remove or populate it.

Falsifiability: Full-page screenshot of `/services/` should show continuous content (no unstyled/empty containers >200px tall) between the location grid and the footer.

---

## 7. Fixed WhatsApp button overlaps body copy on `/contact/` (mobile)

**Severity: Medium**

Evidence: `contact_mobile.png` — the fixed green WhatsApp bubble (bottom-left, ~52×52px per `visual_dom_analysis.json` overlay data, `class="whatsapp-float"`, `position: fixed`) sits directly over the intro paragraph text ("…confirm whether we can help, and set out our exact service fee in…"), visually obscuring the left edge of that sentence in the very first viewport a mobile visitor sees on the contact page — ironically, the page whose entire purpose is to be read and acted on.

Fix: Add bottom padding/margin to the contact page's intro paragraph container equal to the WhatsApp button's height + 16px safe margin on mobile, or reposition the button to avoid the text column on this specific page/breakpoint.

Falsifiability: Compare the WhatsApp button's bounding box to the paragraph's bounding box after the fix — they should not intersect (`DOMRect` overlap test = false).

---

## 8. Sub-44px tap targets

**Severity: Low-Medium**

Evidence: `visual_dom_analysis.json`, mobile tap-target list, elements confirmed visible in the initial viewport with a dimension under the 44–48px accessibility guideline:
- Hamburger menu button: 60×**42**px (top:17, left:307) — height fails.
- Header "Get Started Today" button (desktop, also present at same height on tablet breakpoints): 177×**39**px — height fails.
- Breadcrumb links ("Home", "Blog", "Services") on blog and services-canada pages: consistently **22px** tall.

These are borderline (not drastically undersized) but fall short of Google's 48×48px recommendation and WCAG's 44×44px minimum, which matters more here than average because the audience often includes stressed, less tech-fluent users on older phones.

Fix: Increase the tappable hit area (via padding, not necessarily visual size) of the hamburger icon and breadcrumb links to at least 44px in both dimensions.

Falsifiability: Re-measure `getBoundingClientRect()` for these elements post-fix; height and width should both be ≥44px.

---

## 9. Blog is not reachable from primary navigation or footer

**Severity: Medium**

Evidence: `visual_dom_analysis.json` — the header `<nav>`/`<header>` link scan on every page returns exactly: Home, How It Works, Services, About, Contact, "Get Started Today." The footer link scan (captured via the full tap-target sweep, which includes `<footer>` anchors) lists: "US Visa Appointment Booking," "US Visa Appointment Canada," "US Visa Appointment Toronto," "How It Works," "Canada," "Toronto," email/WhatsApp/Telegram, "About Us," "Contact," "Terms of Service," "Privacy Policy," "Refund & Cancellation Policy" — **no "Blog" link appears in either the header nav or the footer on any of the captured pages.** This is consistent with the CONTEXT.md GSC data showing `/blog/us-visa-appointment-canada-guide-2026/` receiving 300 impressions but 0 clicks — the blog content is essentially orphaned from on-site navigation and only reachable via direct URL, sitemap, or search.

Fix: Add a "Blog" (or "Guides") item to the primary nav and/or footer link list.

Falsifiability: `navLinks`/footer link scan on any page should include an anchor with `href` matching `/blog/`.

---

## 10. Non-issues checked and cleared

- **Viewport meta tag**: present and correct (`width=device-width, initial-scale=1.0`) on all four pages.
- **Base font size**: 16px on all pages/viewports — passes the 16px legibility baseline.
- **Alt text**: every `<img>` across all four pages has a non-empty, descriptive `alt` attribute (`visual_dom_analysis.json` — 0 images missing alt across home, services-canada, blog-canada-guide, contact).
- **Intrusive interstitials**: no `dialog` events fired on load on any page, and the only full-viewport fixed-position overlay in the DOM (`#spinner`, a loading spinner) was verified via computed style to be `visibility: hidden; opacity: 0` after load — it does not block interaction or obscure content despite being present in the DOM at full-viewport size. Not a genuine interstitial-penalty risk.
- **Mobile nav mechanism**: a hamburger button is present and toggles a menu containing Home/How It Works/Services/About/Contact/Get Started (confirmed present in DOM, hidden until toggled) — mechanism itself works, only the missing Blog link (Finding 9) limits it.

---

## Summary table

| # | Finding | Severity | Pages affected |
|---|---|---|---|
| 1 | No price/trust cue above the fold (content gap) | Medium | Home, services-canada |
| 2 | Government-affiliation disclaimer buried in footer only | High | All |
| 3 | No testimonials/reviews/badges/phone number anywhere | High | All |
| 4 | Horizontal scroll on mobile (22–48px overflow) | Medium | Home, services-canada |
| 5 | 100% of images lack explicit width/height attrs (CLS risk) | Medium-High | All |
| 6 | Large broken/empty content block on `/services/` | Medium-High | /services/ |
| 7 | WhatsApp button overlaps contact-page copy on mobile | Medium | Contact |
| 8 | Several tap targets under 44px | Low-Medium | All |
| 9 | Blog unreachable from nav/footer | Medium | All |

---

## Score

**Visual / Mobile UX score: 54/100**

Rationale: technical mobile hygiene is decent (viewport meta correct, 16px base font, full alt-text coverage, no real interstitials, working hamburger menu, functional CTAs above the fold with correct href targets). But the site loses significant points where it matters most for this specific business: a scam-adjacent, paid-intermediary YMYL category where the fold must establish legitimacy fast. It currently does not — no trust badges, no testimonials, no phone number, and the one disclaimer that would meaningfully differentiate this from a scam site is buried at the bottom of a 9,000px-tall page. Add the measured layout bugs (horizontal scroll, missing image dimensions, the broken `/services/` content block) and this sits solidly in the middle of the range rather than higher.

## Top issues (priority order)
1. Government-affiliation disclaimer is not visible without scrolling on any page (High).
2. No testimonials, reviews, trust badges, or phone number anywhere on the site (High).
3. Pricing/cost is never shown above the fold, and rarely shown at all outside blog copy (Medium, compounds #1/#2 for conversion).
4. `/services/` has a large broken/empty content block between the location cards and footer (Medium-High).
5. All images site-wide lack explicit width/height attributes — CLS risk on the LCP hero image (Medium-High).
6. Mobile horizontal scroll on home and services-canada (Medium).
7. Blog has no path in from site navigation (Medium).

## Screenshots referenced
- `easyvisabooking.com-audit/screenshots/home_desktop.png`, `home_mobile.png`, `home_desktop_full.png`, `home_mobile_full.png`
- `easyvisabooking.com-audit/screenshots/services-canada_desktop.png`, `services-canada_mobile.png`, `services-canada_desktop_full.png`, `services-canada_mobile_full.png`
- `easyvisabooking.com-audit/screenshots/blog-canada-guide_desktop.png`, `blog-canada-guide_mobile.png`, `blog-canada-guide_desktop_full.png`, `blog-canada-guide_mobile_full.png`
- `easyvisabooking.com-audit/screenshots/contact_desktop.png`, `contact_mobile.png`, `contact_desktop_full.png`, `contact_mobile_full.png`
- `easyvisabooking.com-audit/screenshots/services-index_desktop_full.png`, `services-index_mobile_full.png`
- Raw diagnostics: `easyvisabooking.com-audit/raw/visual_dom_analysis.json`
