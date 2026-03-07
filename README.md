# Easy Visa Booking - Frontend

## Project Overview
A responsive web application for US visa appointment booking services. The platform provides visa booking assistance, travel agent partnerships, and customer testimonials.

---

## Version History

### **Version 2.0.0** (March 7, 2026)
#### Major Architecture Update: Navbar & Footer Unification

**Key Changes:**
- ✅ **Unified Navbar System**: Implemented consistent navbar across all 8 pages with active link highlighting
- ✅ **Unified Footer System**: Created 4-column footer layout (Company, Services, For Agents, Contact) replicated across all pages
- ✅ **Direct HTML Embedding**: Switched from failed dynamic JavaScript injection to reliable static HTML embedding
  - Replaced non-functional `common-loader.js` approach (CORS-blocked fetch)
  - All navbar/footer now embedded directly in each page HTML
- ✅ **Active Page Highlighting**: Each page highlights its current section in navbar navigation
- ✅ **Responsive Design**: Maintained Bootstrap 5 responsive layout with mobile hamburger menu
- ✅ **Professional Footer**: Implemented standardized footer with:
  - Company information (Easy Visa Booking + social links)
  - Services column (US Visa, AIS Portal, CGI Portal, Bulk Booking)
  - For Agents column (Partnership, Inquiry, Canada, Dubai programs)
  - Contact column (Email, WhatsApp, Telegram)
  - Copyright disclaimer and back-to-top button

**Files Updated:**
- `index.html` - Homepage with carousel + unified navbar/footer
- `for-agents.html` - Travel agent partnership page with highlighted "For Agents" nav link
- `contact.html` - Contact page with highlighted "Contact" nav link
- `about.html` - Company information page with unified navbar/footer
- `service.html` - Services page with unified navbar/footer
- `office.html` - Office locations page with unified navbar/footer
- `testimonial.html` - Client testimonials page with unified navbar/footer
- `how-it-works.html` - Booking process guide with highlighted "How It Works" nav link

**Files Removed (Obsolete):**
- ~~`common.html`~~ - Replaced by direct HTML embedding (5.7 KB removed)
- ~~`js/common-loader.js`~~ - Non-functional fetch-based loader (2.9 KB removed)

**Technical Details:**
- **Navbar Structure**: Logo, 4 navigation links, "Get Started Today" CTA button, mobile toggle
- **Footer Structure**: 4-column responsive grid with consistent styling across all pages
- **Active Link Management**: Hardcoded `active` class on current page's nav link (no JavaScript required)
- **Bootstrap Version**: 5.0.0 - Full responsive grid support
- **Icons**: Font Awesome 5.15.4 for navbar hamburger, footer social icons, and back-to-top button

**Problem Solved:**
- ❌ Previous Issue: Pages displayed without navbar/footer after JavaScript injection attempt
- ❌ Root Cause: Browser CORS policy blocks fetch() on file:// protocol
- ✅ Solution: Direct HTML embedding ensures all pages render correctly with complete navigation structure

---

### **Version 1.0.0** (Initial Release)
- Basic homepage with carousel showcase
- Individual feature pages (About, Services, Contact, Testimonials, Office, How It Works)
- Travel agent partnership program page
- Bootstrap responsive design
- Font Awesome icon integration

---

## Project Structure

```
easyvisabooking_frontend/
├── index.html              # Homepage with carousel
├── for-agents.html         # Travel agent partnership page
├── contact.html            # Contact & inquiry form
├── about.html              # Company information
├── service.html            # Services offered
├── office.html             # Office locations & pricing
├── testimonial.html        # Client testimonials
├── how-it-works.html       # Booking process guide
├── README.md               # This file
├── LICENSE.txt             # Project license
├── css/
│   ├── bootstrap.min.css   # Bootstrap framework
│   └── style.css           # Custom styling
├── js/
│   └── main.js             # Main JavaScript logic
├── lib/
│   ├── animate/            # Animation library
│   ├── easing/             # Easing functions
│   ├── owlcarousel/        # Carousel library
│   ├── waypoints/          # Waypoints library
│   └── wow/                # WOW.js animation
└── img/                    # Images and assets
```

---

## Features

✨ **Core Features:**
- Responsive design for all devices (mobile, tablet, desktop)
- Unified navigation system with active page highlighting
- Professional footer with business information and social links
- Carousel component for showcasing services
- Travel agent partnership program interface
- Contact form for customer inquiries
- Client testimonials section
- Booking process guide (How It Works)
- Back-to-top navigation button

---

## Technologies Used

- **HTML5** - Semantic markup
- **CSS3** - Custom styling with Bootstrap
- **Bootstrap 5** - Responsive grid framework
- **Font Awesome 5.15.4** - Icon library
- **JavaScript** - Interactivity and form handling
- **Animate.css** - CSS animations
- **Owl Carousel** - Image carousel component
- **WOW.js** - Scroll animations

---

## Future Improvements

- [ ] Server-side templating (PHP/Node.js) for true single-source navbar/footer management
- [ ] Build-time template compilation for production optimization
- [ ] CMS integration for dynamic content management
- [ ] Backend API integration for visa applications
- [ ] Email notification system
- [ ] Payment gateway integration
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

**Last Updated:** March 7, 2026