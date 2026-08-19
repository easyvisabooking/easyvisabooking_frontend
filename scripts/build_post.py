#!/usr/bin/env python3
"""
Assemble a blog post from a spec + body fragment into blog/<slug>/index.html.

Why this exists
---------------
Every post shares roughly 500 lines of identical shell: the gtag block, the
font and stylesheet preloads, the navbar, the footer, the copyright bar and the
script tags. Hand-copying that for each post is how drift starts, and drift in
the footer or the schema is exactly what the pre-publish checklist keeps
catching. So the shell is read from blog/_template/index.html at build time and
only the per-post parts are authored.

The OUTPUT is ordinary static HTML, committed to the repo. Nothing about the
deployment changes: Vercel still serves plain files, and scripts/ is excluded
from the deploy. This is an authoring tool, not a build step.

Two guarantees it buys us that hand-authoring does not:

  * The FAQPage schema and the visible <details> block are generated from ONE
    list of question/answer pairs, so they cannot drift out of sync. That is a
    pre-publish checklist item that used to need manual proofreading.
  * The house-style sweeps (no em/en dashes, founder is "Megh" only, Atlys
    never named, no extension/install language, no guarantee or success-rate
    claims about us) run on the assembled page before anything is written.

Usage
    python scripts/build_post.py <slug> [<slug> ...]   # build named posts
    python scripts/build_post.py --all                 # build every spec
    python scripts/build_post.py --all --check         # sweeps only, write nothing

Input, per post, in scripts/post-src/
    <slug>.json        metadata, FAQ pairs, related cards, sources
    <slug>.body.html   the article body, with a <!--FAQ--> marker where the
                       FAQ block goes and a <!--SOURCES--> marker for sources

Exit codes
    0  every requested post built (or passed --check)
    1  a spec was invalid or a house-style sweep failed. Nothing is written.
"""

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "post-src"
TEMPLATE = ROOT / "blog" / "_template" / "index.html"

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

CATEGORIES = {
    "rescheduling": ("Rescheduling &amp; Slots", "cat-rescheduling"),
    "wait-times": ("Wait Times by Country", "cat-wait-times"),
    "expedite": ("Expedite &amp; Emergency", "cat-expedite"),
    "trust": ("Trust &amp; Cost", "cat-trust"),
    "basics": ("Application Basics", "cat-basics"),
}


class SpecError(Exception):
    """A spec or an assembled page failed a check. Nothing is written."""


# --------------------------------------------------------------------------
# shell extraction
# --------------------------------------------------------------------------

def slice_between(text, start, end, what):
    i = text.find(start)
    if i < 0:
        raise SpecError("template: could not find %s start anchor: %r" % (what, start))
    j = text.find(end, i)
    if j < 0:
        raise SpecError("template: could not find %s end anchor: %r" % (what, end))
    return text[i:j + len(end)]


def load_shell():
    """Pull the three placeholder-free constant regions out of the template."""
    t = TEMPLATE.read_text(encoding="utf-8")
    head_tail = slice_between(
        t, '    <link rel="preconnect" href="https://fonts.googleapis.com">',
        "</head>", "head tail")
    body_top = slice_between(
        t, "<body>\n", '<div class="post-shell pt-4">', "body top")
    footer = slice_between(
        t, "    <!-- Footer Start", "</html>\n", "footer")
    for name, chunk in (("head tail", head_tail), ("body top", body_top),
                        ("footer", footer)):
        if "{{" in chunk:
            raise SpecError("template: %s region still contains a placeholder" % name)
    return head_tail, body_top, footer


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def human(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return "%d %s %d" % (d, MONTHS[m - 1], y)


def esc_attr(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def json_str(s):
    """Encode for embedding inside a JSON-LD string literal."""
    return json.dumps(s, ensure_ascii=False)[1:-1]


def indent(block, spaces):
    pad = " " * spaces
    return "\n".join(pad + line if line.strip() else line for line in block.split("\n"))


# --------------------------------------------------------------------------
# per-post regions
# --------------------------------------------------------------------------

GTAG = """<!DOCTYPE html>
<html lang="en">

<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-3MTBDM446M"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() { dataLayer.push(arguments); }
        gtag('js', new Date());

        gtag('config', 'G-3MTBDM446M');
    </script>
    <!-- Google tag ends -->
"""


def build_head_meta(s):
    scheduled = s.get("publishOn")
    robots = ('    <!-- SCHEDULED POST: held at noindex until %s, released by '
              'scripts/publish_scheduled.py -->\n'
              '    <meta name="robots" content="noindex, follow">' % scheduled) if scheduled else \
             '    <meta name="robots" content="index, follow">'
    return """
    <meta charset="utf-8">
    <title>{title_tag}</title>
    <meta content="width=device-width, initial-scale=1.0" name="viewport">
    <meta name="description" content="{meta_desc}">
    <meta name="keywords" content="{keywords}">
    <link rel="canonical" href="https://www.easyvisabooking.com/blog/{slug}/">
    <meta property="og:title" content="{h1}">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:url" content="https://www.easyvisabooking.com/blog/{slug}/">
    <meta property="og:image" content="{og_image}">
    <meta property="og:image:width" content="{og_w}">
    <meta property="og:image:height" content="{og_h}">
    <meta property="og:site_name" content="Easy Visa Booking">
    <meta property="og:type" content="article">
    <meta property="article:published_time" content="{date}">
    <meta property="article:modified_time" content="{date}">
    <meta property="article:author" content="Megh">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title_tag}">
    <meta name="twitter:description" content="{meta_desc}">
    <meta name="twitter:image" content="{og_image}">
{robots}
    <meta name="author" content="Megh">
""".format(
        title_tag=esc_attr(s["titleTag"]), meta_desc=esc_attr(s["metaDescription"]),
        keywords=esc_attr(", ".join(s["keywords"])), slug=s["slug"],
        h1=esc_attr(s["h1"]), og_image=s["ogImage"], og_w=s["ogImageWidth"],
        og_h=s["ogImageHeight"], date=s["datePublished"], robots=robots)


def build_schema(s):
    faq_items = ",\n".join(
        '            {\n'
        '              "@type": "Question",\n'
        '              "name": "%s",\n'
        '              "acceptedAnswer": { "@type": "Answer", "text": "%s" }\n'
        '            }' % (json_str(q), json_str(a))
        for q, a in s["faq"])

    return """
    <!-- BlogPosting -->
    <script type="application/ld+json">
        {{
          "@context": "https://schema.org",
          "@type": "BlogPosting",
          "headline": "{h1}",
          "description": "{meta_desc}",
          "image": {{
            "@type": "ImageObject",
            "url": "{og_image}",
            "width": {og_w},
            "height": {og_h}
          }},
          "author": {{
            "@type": "Person",
            "name": "Megh",
            "jobTitle": "Founder, Easy Visa Booking",
            "url": "https://www.easyvisabooking.com/about/"
          }},
          "publisher": {{
            "@type": "Organization",
            "name": "Easy Visa Booking",
            "url": "https://www.easyvisabooking.com",
            "logo": {{
              "@type": "ImageObject",
              "url": "https://www.easyvisabooking.com/img/brand-logo-real.PNG"
            }}
          }},
          "datePublished": "{date}",
          "dateModified": "{date}",
          "url": "https://www.easyvisabooking.com/blog/{slug}/",
          "mainEntityOfPage": "https://www.easyvisabooking.com/blog/{slug}/",
          "articleSection": "{cat_label_plain}",
          "keywords": "{keywords}"
        }}
    </script>

    <!-- BreadcrumbList -->
    <script type="application/ld+json">
        {{
          "@context": "https://schema.org",
          "@type": "BreadcrumbList",
          "itemListElement": [
            {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.easyvisabooking.com/" }},
            {{ "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://www.easyvisabooking.com/blog/" }},
            {{ "@type": "ListItem", "position": 3, "name": "{crumb}", "item": "https://www.easyvisabooking.com/blog/{slug}/" }}
          ]
        }}
    </script>

    <!-- FAQPage: text MUST match the visible <details> answers word for word.
         Both are generated from the same list in scripts/post-src/{slug}.json -->
    <script type="application/ld+json">
        {{
          "@context": "https://schema.org",
          "@type": "FAQPage",
          "mainEntity": [
{faq_items}
          ]
        }}
    </script>
""".format(
        h1=json_str(s["h1"]), meta_desc=json_str(s["metaDescription"]),
        og_image=s["ogImage"], og_w=s["ogImageWidth"], og_h=s["ogImageHeight"],
        date=s["datePublished"], slug=s["slug"],
        cat_label_plain=CATEGORIES[s["category"]][0].replace("&amp;", "&"),
        keywords=json_str(", ".join(s["keywords"])),
        crumb=json_str(s["breadcrumb"]), faq_items=faq_items)


def build_masthead(s):
    label, css = CATEGORIES[s["category"]]
    return """
            <nav aria-label="Breadcrumb">
                <ol class="post-crumbs">
                    <li><a href="/">Home</a></li>
                    <li><a href="/blog/">Blog</a></li>
                    <li aria-current="page">{crumb}</li>
                </ol>
            </nav>

            <article>
                <header class="post-masthead">
                    <span class="cat {css}">{label}</span>
                    <h1>{h1}</h1>
                    <p class="post-deck">{deck}</p>

                    <div class="byline">
                        <div class="byline-avatar" aria-hidden="true">M</div>
                        <div class="byline-text">
                            <p class="byline-name"><a href="/about/">Megh</a></p>
                            <p class="post-meta">
                                Founder, Easy Visa Booking
                                <span class="dot">·</span>
                                <time datetime="{date}">{date_human}</time>
                                <span class="dot">·</span><span>{read} min read</span>
                            </p>
                        </div>
                    </div>

                    <figure class="post-cover">
                        <img src="{cover}" alt="{cover_alt}" width="1200" height="630">
                    </figure>
                </header>
""".format(crumb=esc_attr(s["breadcrumb"]), css=css, label=label, h1=s["h1"],
           deck=s["deck"], date=s["datePublished"],
           date_human=human(s["datePublished"]), read=s["readTime"],
           cover=s["cover"], cover_alt=esc_attr(s["coverAlt"]))


def build_faq_block(s):
    items = "\n".join(
        '                        <details class="faq-item">\n'
        '                            <summary class="faq-q">%s<span class="faq-icon" aria-hidden="true"></span></summary>\n'
        '                            <div class="faq-a">\n'
        '                                <p>%s</p>\n'
        '                            </div>\n'
        '                        </details>' % (q, a) for q, a in s["faq"])
    return ('                    <h2 id="faq">Frequently asked questions</h2>\n\n'
            '                    <div class="faq">\n' + items + "\n"
            '                    </div>')


def build_sources_block(s):
    date_human = human(s["datePublished"])
    items = []
    for src in s["sources"]:
        items.append(
            '                            <li>%s, <a href="%s" target="_blank" rel="noopener noreferrer">%s</a>. %s Retrieved %s.</li>'
            % (src["publisher"], src["url"], src["title"], src["note"],
               src.get("retrieved", date_human)))
    note = s.get("sourcesNote",
                 "This article is general information and is not legal or immigration advice.")
    return ('                    <div class="sources">\n'
            '                        <p class="sources-title">Sources</p>\n'
            '                        <ol>\n' + "\n".join(items) + "\n"
            '                        </ol>\n'
            '                        <p class="sources-updated">Published %s. %s</p>\n'
            '                    </div>' % (date_human, note))


AUTHOR_CARD = """                    <div class="author-card">
                        <div class="byline-avatar" aria-hidden="true">M</div>
                        <div>
                            <h2>Megh</h2>
                            <p class="author-role">Founder, Easy Visa Booking</p>
                            <p>Megh founded Easy Visa Booking after watching applicants lose travel plans to a
                                scheduling system nobody explains properly. He and the team work US visa appointment
                                rescheduling cases daily across consulates worldwide, and write these guides from what
                                the portals actually do rather than what the FAQs say.
                                <a href="/about/">More about Easy Visa Booking</a>.</p>
                        </div>
                    </div>"""


def build_cta(s):
    cta = s["cta"]
    buttons = "\n".join(
        '                            <a href="%s" class="cta-btn %s">%s</a>'
        % (b["href"], b["style"], b["label"]) for b in cta["buttons"])
    return """                    <section class="cta-end">
                        <h2>{heading}</h2>
                        <p>{body}</p>
                        <ul class="cta-points">
                            <li>From $100, and you pay only if we secure you an earlier date</li>
                            <li>The wider the date range you can accept, the more often we can move it</li>
                            <li>No guarantee of a date, stated plainly before you decide anything</li>
                        </ul>
                        <div class="cta-buttons">
{buttons}
                        </div>
                        <p class="cta-fine">Easy Visa Booking is an independent scheduling assistance service, not
                            affiliated with the US Department of State, any US Embassy or Consulate, CGI Federal or the
                            AIS portal. All appointments are made through the official portal.</p>
                    </section>""".format(heading=cta["heading"], body=cta["body"], buttons=buttons)


def build_related(s):
    cards = []
    for r in s["related"]:
        label, css = CATEGORIES[r["category"]]
        cards.append("""                    <article class="post-card">
                        <div class="post-card-media">
                            <img src="{img}" alt="{alt}" width="1200" height="630" loading="lazy">
                        </div>
                        <div class="post-card-body">
                            <span class="cat {css}">{label}</span>
                            <h3><a href="/blog/{slug}/">{title}</a></h3>
                            <p>{blurb}</p>
                        </div>
                    </article>""".format(img=r["image"], alt=esc_attr(r["alt"]), css=css,
                                         label=label, slug=r["slug"], title=r["title"],
                                         blurb=r["blurb"]))
    return ('            <aside class="related">\n'
            '                <h2 class="related-title">Keep reading</h2>\n'
            '                <div class="card-grid">\n' + "\n".join(cards) + "\n"
            '                </div>\n'
            '            </aside>')


# --------------------------------------------------------------------------
# cover art
# --------------------------------------------------------------------------

COVER_PALETTES = {
    "rescheduling": ("#1E2340", "#2C3566", "#3D4B93", "#A9B6EC"),
    "wait-times": ("#062E3F", "#0A4A61", "#0E6B85", "#8FD4E4"),
    "expedite": ("#00294A", "#003A66", "#005A93", "#9FCDEC"),
    "trust": ("#14322B", "#1B4C3F", "#236B55", "#95D8BE"),
    "basics": ("#2C2237", "#43305A", "#5B4180", "#C6B0E8"),
}


def build_cover(slug, s):
    """Generate the on-page hero SVG from the spec.

    Hand-drawing one of these per post is how they drift apart. The layout is
    fixed; a post supplies an eyebrow, one or two headline lines and four
    label/value pairs. The <title> and <desc> carry the content for screen
    readers, so the alt text never has to say "cover image".
    """
    c = s.get("coverSpec")
    if not c:
        return None
    dark, mid, light, accent = COVER_PALETTES[s["category"]]
    uid = "c" + re.sub(r"[^a-z0-9]", "", slug)[:14]

    head = c["headline"]
    if isinstance(head, str):
        head = [head]
    size = c.get("headlineSize", 88 if len(head) > 1 else 104)
    lines = "\n".join(
        '  <text x="136" y="%d" fill="#ffffff" font-size="%d" font-weight="600" letter-spacing="-2">%s</text>'
        % (300 + i * int(size * 0.98), size, esc_attr(t)) for i, t in enumerate(head))
    rule_y = 300 + (len(head) - 1) * int(size * 0.98) + 28

    facts = c["facts"]
    if len(facts) != 4:
        raise SpecError("%s: coverSpec needs exactly 4 facts" % slug)
    fx = []
    for i, (label, value) in enumerate(facts):
        col = 140 if i % 2 == 0 else 560
        row = 492 if i < 2 else 576
        fx.append('    <text x="%d" y="%d" fill="%s">%s</text>' % (col, row, accent, esc_attr(label)))
        fx.append('    <text x="%d" y="%d" fill="#ffffff">%s</text>' % (col, row + 32, esc_attr(value)))

    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" role="img"
     aria-labelledby="{uid}-title {uid}-desc" font-family="Poppins, 'Segoe UI', Helvetica, Arial, sans-serif">
  <title id="{uid}-title">{title}</title>
  <desc id="{uid}-desc">{desc}</desc>

  <defs>
    <linearGradient id="{uid}-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{dark}"/>
      <stop offset="55%" stop-color="{mid}"/>
      <stop offset="100%" stop-color="{light}"/>
    </linearGradient>
    <linearGradient id="{uid}-fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity=".10"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect width="1200" height="630" fill="url(#{uid}-bg)"/>
  <rect width="1200" height="630" fill="url(#{uid}-fade)"/>

  <text x="140" y="196" fill="{accent}" font-size="22" font-weight="600" letter-spacing="3.2">{eyebrow}</text>

{lines}
  <rect x="140" y="{rule_y}" width="86" height="5" rx="2.5" fill="#E02454"/>

  <line x1="140" y1="452" x2="1060" y2="452" stroke="#ffffff" stroke-opacity=".18" stroke-width="1"/>
  <line x1="140" y1="544" x2="1060" y2="544" stroke="#ffffff" stroke-opacity=".18" stroke-width="1"/>

  <g font-size="21" font-weight="500">
{facts}
  </g>

  <text x="1060" y="196" fill="#ffffff" fill-opacity=".45" font-size="17" text-anchor="end">easyvisabooking.com</text>
</svg>
""".format(uid=uid, title=esc_attr(c["title"]), desc=esc_attr(c["desc"]), dark=dark,
           mid=mid, light=light, accent=accent, eyebrow=esc_attr(c["eyebrow"]),
           lines=lines, rule_y=rule_y, facts="\n".join(fx))

    path = ROOT / "img" / "blog" / ("cover-%s.svg" % slug)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(svg)
    return path


# --------------------------------------------------------------------------
# sweeps
# --------------------------------------------------------------------------

# Both the literal characters and the HTML entities: they render identically to
# the reader, and the entity form slipped past the repo's grep-based sweep for
# months on three posts.
DASHES = re.compile("[–—]|&mdash;|&ndash;|&#821[12];|&#x201[34];", re.I)
FULL_NAME = re.compile(r"meghkumar|girishbhai", re.I)
COMPETITOR = re.compile(r"atlys|chrome extension|browser extension|web store", re.I)
CONSTRAINT = re.compile(
    r"auto-?book|24/7|every few seconds|instant alert|\bbots?\b|white.?label|"
    r"bulk booking|guarantee[ds]? (?:a |an |your )?(?:slot|date|visa|appointment)|"
    r"success rate", re.I)


def sweep(slug, html):
    """House-style and constraint sweeps. Raises on anything that must not ship."""
    problems = []

    for m in DASHES.finditer(html):
        problems.append("em/en dash at offset %d: ...%s..."
                        % (m.start(), html[max(0, m.start() - 40):m.start() + 40]))
    if FULL_NAME.search(html):
        problems.append("founder's full legal name appears; it must be 'Megh' only")
    for m in COMPETITOR.finditer(html):
        problems.append("competitor-naming sweep hit %r at offset %d" % (m.group(0), m.start()))
    if "{{" in html:
        problems.append("unreplaced {{PLACEHOLDER}} left in the page")

    # Constraint sweep. Hits are reported for review rather than hard-failed,
    # because a sentence about someone else's product, or one saying we do NOT
    # do a thing, is legitimate. Anything describing what WE do is not.
    warnings = ["constraint sweep: %r in ...%s..."
                % (m.group(0), strip_tags(html[max(0, m.start() - 90):m.start() + 90]).strip())
                for m in CONSTRAINT.finditer(html)]

    if problems:
        raise SpecError("%s failed the sweeps:\n  - %s" % (slug, "\n  - ".join(problems)))
    return warnings


REQUIRED_BLOCKS = ['class="answer-box"', 'class="toc"', 'class="honesty"',
                   'class="compare"', 'class="why-us"', 'class="cta-end"',
                   'class="faq"', 'class="sources"', 'class="author-card"',
                   'class="related"']


def structural_checks(slug, html, s):
    problems = []
    for block in REQUIRED_BLOCKS:
        if block not in html:
            problems.append("required block missing: %s" % block)
    if html.count('class="honesty"') < 2:
        problems.append("needs two .honesty blocks, one of them the closing "
                        '"What nobody can promise you"')
    if "What nobody can promise you" not in html:
        problems.append('closing honesty block must keep the heading "What nobody can promise you"')
    if html.count("<h1") != 1:
        problems.append("exactly one <h1> required, found %d" % html.count("<h1"))

    # every TOC anchor must resolve to a real id on the page
    ids = set(re.findall(r'\sid="([^"]+)"', html))
    toc = re.search(r'<nav class="toc".*?</nav>', html, re.S)
    if toc:
        for anchor in re.findall(r'href="#([^"]+)"', toc.group(0)):
            if anchor not in ids:
                problems.append("TOC anchor #%s has no matching id" % anchor)

    # FAQ schema and visible answers come from one list, so only check they landed
    for q, _ in s["faq"]:
        if q not in html:
            problems.append("FAQ question missing from the body: %s" % q[:60])

    if problems:
        raise SpecError("%s failed structural checks:\n  - %s" % (slug, "\n  - ".join(problems)))


# --------------------------------------------------------------------------
# assembly
# --------------------------------------------------------------------------

def build(slug, shell, write_out=True):
    spec_path = SRC / (slug + ".json")
    body_path = SRC / (slug + ".body.html")
    if not spec_path.exists():
        raise SpecError("no spec at %s" % spec_path)
    if not body_path.exists():
        raise SpecError("no body at %s" % body_path)

    s = json.loads(spec_path.read_text(encoding="utf-8"))
    s["slug"] = slug
    s["faq"] = [(item["q"], item["a"]) for item in s["faq"]]
    if s["category"] not in CATEGORIES:
        raise SpecError("%s: unknown category %r" % (slug, s["category"]))

    body = body_path.read_text(encoding="utf-8").rstrip("\n")
    if "<!--FAQ-->" not in body:
        raise SpecError("%s: body has no <!--FAQ--> marker" % slug)
    if "<!--SOURCES-->" not in body:
        raise SpecError("%s: body has no <!--SOURCES--> marker" % slug)
    # Markers are replaced with pre-indented blocks, so the marker's own leading
    # whitespace is consumed rather than added to it.
    for marker, block in (("FAQ", build_faq_block(s)),
                          ("SOURCES", build_sources_block(s)),
                          ("AUTHOR", AUTHOR_CARD),
                          ("CTA", build_cta(s))):
        body = re.sub(r"^[ 	]*<!--%s-->" % marker, lambda m, b=block: b,
                      body, flags=re.M)

    head_tail, body_top, footer = shell

    html = "".join([
        GTAG,
        build_head_meta(s),
        build_schema(s),
        "\n",
        head_tail,
        "\n\n",
        body_top,
        "\n",
        build_masthead(s),
        "\n",
        '                <div class="post-body">\n',
        body,
        "\n\n                </div>\n",
        "            </article>\n\n",
        build_related(s),
        "\n\n        </div>\n    </div>\n    <!-- Article End -->\n\n",
        footer,
    ])

    warnings = sweep(slug, html)
    structural_checks(slug, html, s)

    if write_out:
        build_cover(slug, s)
        out = ROOT / "blog" / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(html)
    # Count the article only. The shared shell would add ~400 words to every post
    # and make every count look the same.
    article = re.search(r'<div class="post-body">(.*?)\n                </div>', html, re.S)
    prose = re.sub(r"(?s)<!--.*?-->", " ", article.group(1) if article else "")
    words = len(strip_tags(prose).split())
    return words, warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slugs", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--check", action="store_true", help="run the sweeps, write nothing")
    args = ap.parse_args()

    slugs = args.slugs
    if args.all:
        slugs = sorted(p.name[: -len(".json")] for p in SRC.glob("*.json"))
    if not slugs:
        ap.error("give a slug or --all")

    try:
        shell = load_shell()
    except SpecError as e:
        print("FAIL: %s" % e)
        return 1

    failures = 0
    for slug in slugs:
        try:
            words, warnings = build(slug, shell, write_out=not args.check)
            flag = "checked" if args.check else "built"
            print("%-44s %s  %5d words" % (slug, flag, words))
            for w in warnings:
                print("    review: %s" % w)
        except SpecError as e:
            print("FAIL: %s" % e)
            failures += 1
        except Exception as e:  # noqa: BLE001 - surface the spec that broke
            print("FAIL: %s raised %s: %s" % (slug, type(e).__name__, e))
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
