# Easy Visa Booking - Frontend

## Project Overview
A responsive marketing website for Easy Visa Booking, an independent US visa appointment booking and
rescheduling assistance service. The site presents the service, pricing model, booking process and legal
policies for applicants in Canada, the UAE, Turkey, Australia and the UK.

---

## Version History

### **Version 3.1.0** (August 19, 2026)
#### Content Build-Out: 21 Posts Written and Scheduled Through October

**Content**
- ✅ **21 new blog posts written**, covering every remaining item on the SEO content queue plus two
  topics that were missing from it. Held at `noindex` and scheduled one every 2 to 3 days from
  **2026-08-22 to 2026-09-10**, one post per day, respecting the documented publishing cadence.
- ✅ **First in the batch is `/blog/us-visa-appointment-abu-dhabi/`** (publishes 2026-08-21), written
  because the UAE has reopened for bookings. Mission UAE has been on ordered departure since March
  2026; its own messaging now states that limited nonimmigrant appointments are available while all
  immigrant visa services remain suspended. Leads on the mission's published Friday 07:30 to 11:30
  release window.
- ✅ **World Cup post rewritten.** The tournament ended 19 July 2026 and the page was still written in
  the future tense telling readers to book for it. Reframed as aftermath; URL kept.

**Corrections**
- ⚠️ **The site was understating the cost of a US visa by $250 a head.** The Visa Integrity Fee
  (One Big Beautiful Bill Act, effective FY2026) is charged on issuance on top of the MRV fee, so a
  B-1/B-2 applicant faces **$435** and a family of four **$1,740**. All 21 new posts use corrected
  wording. The three older posts with `.compare` tables still carry the old line and are logged for
  amendment.
- ✅ **Em-dash sweep hole closed.** The documented grep only matched the literal `—` and `–`
  characters, and three posts carried **18 `&mdash;` entities** that render identically. All fixed,
  and the build now fails on entity and numeric forms too.

**Tooling** (internal, `.vercelignore`d, no deployment change)
- ✅ `scripts/build_post.py` — assembles a post from a JSON spec plus a body fragment, reading the
  shared shell from `blog/_template/index.html`. Generates the FAQ schema and the visible `<details>`
  block from one list so they cannot drift, generates the cover SVG, and runs the house-style and
  structural sweeps before writing anything.
- ✅ `scripts/wire_posts.py` — adds each post's hub card, sitemap entry and queue entry in held form.

---

### **Version 3.0.0** (August 7, 2026)
#### Compliance & Positioning Overhaul (Payment Gateway Readiness)

Prepared the site for payment-processor underwriting review. The service is now described by **what the
client receives**, not by **how the work is performed**.

**Positioning changes (site-wide):**
- ✅ **Removed all automation / auto-booking language** — no "24/7 automated monitoring", "checks every few
  seconds", "books it instantly", "grabs slots", or references to systems/servers/algorithms acting on the
  scheduling portal. Replaced with team- and outcome-based language.
- ✅ **Removed the entire agent / B2B programme** — deleted `/for-agents/`, all navigation and footer links,
  both agent pricing cards, and the agent sections on the Canada and Toronto service pages. Removed
  "white-label", "bulk booking", "volume discounts" and "first slot free trial" throughout.
- ✅ **Removed credential-collection language from marketing pages** — the requirement is now disclosed
  properly in the Terms of Service instead, where it legally belongs.
- ✅ **Removed unsubstantiated claims** — "98% success rate", "100% money-back guarantee", "Trusted by
  Thousands", "<10 sec slot detection". Replaced with defensible statements and explicit no-guarantee
  disclaimers.

**Pages removed:**
- ❌ `for-agents/` — agent partnership programme (301 → `/services/`)
- ❌ `office/` — placeholder content, fictional worldwide offices (301 → `/contact/`)
- ❌ `testimonial/` — Lorem ipsum placeholder content (301 → `/`)
- ❌ Commented-out fabricated testimonial carousel and fictional office block removed from `index.html`

**Pages added:**
- ✅ `terms/` — Terms of Service: scope, exclusions, eligibility, fees, no-guarantee clause, liability limits
- ✅ `privacy/` — Privacy Policy: data collected, legal basis, processors, retention, rights
- ✅ `refund-policy/` — Refund & Cancellation Policy: pay-on-success model, refund eligibility, chargebacks

**Pages rewritten:**
- ✅ `about/` — expanded from three sentences to a full company page with a "what we do / what we do not do"
  section, pricing model, business details table and independence notice
- ✅ `how-it-works/` — all four process steps rewritten; switched from agent voice ("your client") to
  applicant voice ("you")

**SEO changes:**
- ✅ All titles, meta descriptions and keyword sets rewritten around applicant-side search intent
- ✅ All JSON-LD rewritten: Organization, Service, FAQPage, AboutPage, BreadcrumbList
- ✅ Footer service links repointed from `/` to real deep links with descriptive anchor text
- ✅ Toronto page `og:title` and Service schema `url` corrected (previously pointed at the Canada page)
- ✅ `/about/` added to sitemap (was never included); legal pages added; all `lastmod` refreshed
- ✅ Broken `/how-it-works.html` link on homepage fixed
- ✅ Dead breadcrumb and `href="#"` contact links fixed

**Portal credentials — stated position (revised 2026-08-19):**
- The cloud plan requires the applicant's scheduling-portal credentials, so the previous site-wide
  claim ("we never ask for, receive or store your login") was **false and has been removed**
  everywhere it appeared in marketing copy: every blog post, the blog template, the homepage trust
  badge and step 1 of `how-it-works/`.
- **Marketing copy now says nothing about credentials in either direction.** Do not reintroduce the
  denial, and do not advertise the requirement either. Where the old claim carried conversion weight,
  it was replaced with date-range flexibility copy, which is honest and does the same job.
- ⚠️ **Outstanding:** `terms/` §6 and `privacy/` §2 still carry the old denial. A privacy policy that
  is silent about credentials while the product collects them is worse than one that is merely out of
  date, so those two sections need positive disclosure of what the cloud plan actually does: what is
  collected, where it is held, for how long, and how to have it deleted. Blocked on those facts.

**Business identity — deliberate omission:**
- Registered legal entity name, registration number, registered address and a named governing-law
  jurisdiction are intentionally not published. The About identity table shows trading name, founder,
  nature of business, countries served and support channels only. `terms/` §13 refers to "the laws
  applicable at Easy Visa Booking's principal place of business" rather than naming a jurisdiction.
- Note for future review: payment processors generally expect the business name shown on the site to
  match the name on the payment account.

---

### **Version 2.0.0** (March 7, 2026)
#### Major Architecture Update: Navbar & Footer Unification

**Key Changes:**
- ✅ **Unified Navbar System**: Implemented consistent navbar across all pages with active link highlighting
- ✅ **Unified Footer System**: Created 4-column footer layout replicated across all pages
- ✅ **Direct HTML Embedding**: Switched from failed dynamic JavaScript injection to reliable static HTML
  embedding (replaced CORS-blocked `common-loader.js` fetch approach)
- ✅ **Active Page Highlighting**: Each page highlights its current section in navbar navigation
- ✅ **Responsive Design**: Bootstrap 5 responsive layout with mobile hamburger menu

**Files Removed (Obsolete):**
- ~~`common.html`~~ — Replaced by direct HTML embedding
- ~~`js/common-loader.js`~~ — Non-functional fetch-based loader

---

### **Version 1.0.0** (Initial Release)
- Basic homepage with carousel showcase
- Individual feature pages
- Bootstrap responsive design
- Font Awesome icon integration

---

## Project Structure

```
easyvisabooking_frontend/
├── index.html                              # Homepage
├── 404.html                                # Not-found page
├── about/index.html                        # Company information & business details
├── how-it-works/index.html                 # 4-step booking process
├── contact/index.html                      # Contact & enquiry form
├── services/
│   ├── index.html                          # Services by location
│   ├── us-visa-appointment-canada/         # Canada landing page
│   └── us-visa-appointment-toronto/        # Toronto landing page
├── blog/
│   ├── index.html                          # Blog hub (card grid + Blog JSON-LD)
│   ├── _template/                          # Post template (not deployed)
│   ├── README.md                           # How posts are authored and scheduled (not deployed)
│   ├── publish-queue.json                  # Scheduled posts (not deployed)
│   └── <28 post folders>/                  # One index.html each. 7 live, 21 scheduled
├── terms/index.html                        # Terms of Service
├── privacy/index.html                      # Privacy Policy
├── refund-policy/index.html                # Refund & Cancellation Policy
├── sitemap.xml                             # XML sitemap
├── robots.txt                              # Crawler directives
├── vercel.json                             # Trailing-slash config + 301 redirects
├── README.md                               # This file
├── LICENSE.txt                             # Project license
├── css/
│   ├── bootstrap.min.css                   # Bootstrap framework
│   └── style.css                           # Custom styling
├── js/
│   └── main.js                             # Main JavaScript logic
├── lib/                                    # animate, easing, owlcarousel, waypoints, wow
└── img/                                    # Images and assets
```

---

## Content Guidelines

When editing or adding pages, keep the following consistent:

**Do not use** — automation framing of any kind: "automated", "auto-booking", "our system monitors",
"every few seconds", "instantly books", "bots", "scripts", "24/7 monitoring". Do not reintroduce agent,
bulk, reseller or white-label offerings. Do not state success-rate percentages, guarantees, or
money-back promises. Do not make any claim about portal credentials in marketing copy, in either
direction: not "we never ask for your password", and not a request for them either. Credential
handling is disclosed in `terms/` and `privacy/` only.

**Do use** — "our team", "our coordinators", "appointment support", "we review availability", "we act
promptly on your behalf", "booked through the official portal", "pay only on success". Always pair
capability claims with the limitation: appointment availability is controlled by the consulate.

**Punctuation** — no em dashes (`—`) or en dashes (`–`) in any published page. They read as AI-written
copy. Use a comma, colon, semicolon, full stop or parentheses instead, and a plain hyphen for numeric
ranges ("30-60 days", "June 11 to June 27"). Internal files that never ship (`README.md`, `seo/`,
`easyvisabooking.com-audit/`, `blog/_template/` docs) are exempt.

**Founder name** — the site shows **Megh** only. Never publish the full legal name in bylines, author
schema, `<meta name="author">`, the About identity table or article body copy.

Every page must carry the independence disclaimer in the copyright bar and link to the three legal pages.

---

## Technologies Used

- **HTML5** — Semantic markup
- **CSS3** — Custom styling with Bootstrap
- **Bootstrap 5** — Responsive grid framework
- **Font Awesome 5.15.4** — Icon library
- **JavaScript** — Interactivity and form handling
- **Animate.css** — CSS animations
- **Owl Carousel** — Image carousel component
- **WOW.js** — Scroll animations
- **JSON-LD** — Structured data (Organization, Service, FAQPage, AboutPage, BreadcrumbList)
- **Web3Forms** — Contact form submission handling
- **Google Analytics + Ahrefs Analytics** — Traffic measurement

---

## Future Improvements

- [ ] Server-side templating for true single-source navbar/footer management
- [ ] Build-time template compilation for production optimization
- [ ] Backend API integration
- [ ] Email notification system
- [ ] Payment gateway integration (Chrome extension)
- [ ] Analytics dashboard

---

## Browser Compatibility

- Chrome (Latest)
- Firefox (Latest)
- Safari (Latest)
- Edge (Latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

---

## License

See [LICENSE.txt](LICENSE.txt) for licensing information.

---

**Last Updated:** August 19, 2026
