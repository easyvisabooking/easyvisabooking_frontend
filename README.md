# Easy Visa Booking - Frontend

## Project Overview
A responsive marketing website for Easy Visa Booking, an independent US visa appointment booking and
rescheduling assistance service. The site presents the service, pricing model, booking process and legal
policies for applicants in Canada, the UAE, Turkey, Australia and the UK.

---

## Version History

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

**Portal credentials — stated position:**
- We never ask for, receive, or store the applicant's scheduling-portal login. Any portal sign-in is
  performed by the applicant on their own device. Stated in `terms/` §6, `privacy/` §2, a homepage
  trust badge, and step 1 of `how-it-works/`.

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
│   ├── index.html                          # Blog index
│   ├── us-visa-appointment-world-cup-2026-guide/
│   ├── us-visa-appointment-canada-guide-2026/
│   └── us-visa-appointment-dubai-fast-2026/
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
money-back promises. Do not request portal credentials in marketing copy.

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

**Last Updated:** August 7, 2026
