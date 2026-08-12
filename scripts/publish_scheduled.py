#!/usr/bin/env python3
"""
Publish scheduled blog posts.

Posts are written and committed up front but held back until their publish date.
A held post is deployed and returns 200, but nothing Google can crawl may point
at it — otherwise Googlebot follows a link, hits the noindex, and files the URL
under "Excluded by 'noindex' tag" in Search Console. So a held post carries FIVE
markers, not three:

  * the post page carries  <meta name="robots" content="noindex, follow">
  * its card in blog/index.html sits inside an inert <template data-scheduled="...">
  * its <url> entry in sitemap.xml is commented out
  * every inbound link from a live page is inside a <!-- SCHEDULED LINK ... --> comment
  * it has NO entry in the hub's Blog schema blogPost[] array
  * every publish-date field still reads the day it was written

This script publishes anything whose publishOn date has arrived:

  1. stamps the real publish date into all six date fields
  2. flips robots to "index, follow"
  3. unwraps the <template> around the hub card
  4. uncomments the sitemap entry
  5. uncomments every held inbound link across the site
  6. inserts the post into the hub's Blog schema blogPost[] array
  7. moves the entry from "scheduled" to "published" in blog/publish-queue.json

Run by .github/workflows/publish-scheduled-posts.yml once a day. Every edit is
anchored and asserted, so a markup change upstream fails loudly instead of
silently publishing something half-wired.

--check is the guard for markers 2, 3, 4 and 5. It strips HTML/XML comments and
<template data-scheduled> blocks from every DEPLOYED file, then fails if a
scheduled slug still appears anywhere. .github/workflows/check-scheduled-holds.yml
runs it on every push, so a held post can never reach production discoverable.

Usage
    python scripts/publish_scheduled.py                      # publish anything due today (UTC)
    python scripts/publish_scheduled.py --check              # guard only: is every held post invisible?
    python scripts/publish_scheduled.py --dry-run            # show what would change
    python scripts/publish_scheduled.py --today 2026-08-15   # pretend it is that date
    python scripts/publish_scheduled.py --slug <slug>        # publish one post now, date = today

Exit codes
    0  finished (whether or not anything was published)
    1  a post was due but its markup did not match, or --check found an
       exposed scheduled slug. Nothing is written in either case.
"""

import argparse
import datetime as dt
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
QUEUE = ROOT / "blog" / "publish-queue.json"
HUB = ROOT / "blog" / "index.html"
SITEMAP = ROOT / "sitemap.xml"
VERCELIGNORE = ROOT / ".vercelignore"

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


class PublishError(Exception):
    """Markup did not match. Nothing is written when this is raised."""


def human(date: dt.date) -> str:
    """2026-08-15 -> '15 August 2026' (no leading zero, matching the posts)."""
    return "%d %s %d" % (date.day, MONTHS[date.month - 1], date.year)


def write(path, text):
    """Write with LF endings regardless of platform.

    A publish run rewrites every page that links to the post. Left to Python's
    default, a run on Windows would flip each of those files to CRLF and turn a
    ten-line publish into a whole-file diff.
    """
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def sub_once(text, pattern, repl, what, flags=0):
    """re.sub that insists on exactly one match."""
    new, n = re.subn(pattern, repl, text, flags=flags)
    if n != 1:
        raise PublishError("expected 1 match for %s, found %d" % (what, n))
    return new


# ---------------------------------------------------------------------------
# which files actually reach the browser
# ---------------------------------------------------------------------------
def deployed_paths():
    """Every .html/.xml file Vercel actually serves.

    Read from .vercelignore rather than hardcoded: blog/_template/, seo/ and
    friends are excluded there, and a page nobody can fetch cannot leak a
    scheduled URL. If that file grows an entry, this follows automatically.
    """
    ignored = []
    if VERCELIGNORE.exists():
        for line in VERCELIGNORE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                ignored.append(line.rstrip("/"))

    out = []
    for path in sorted(ROOT.rglob("*")):
        if path.suffix.lower() not in (".html", ".xml") or not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(".git/") or any(
                rel == ig or rel.startswith(ig + "/") for ig in ignored):
            continue
        out.append(path)
    return out


def strip_held(text):
    """Remove every region a crawler cannot see: <template data-scheduled>
    blocks and HTML/XML comments. Whatever survives is live markup."""
    text = re.sub(r'<template data-scheduled=.*?</template>', '', text, flags=re.S)
    return re.sub(r'<!--.*?-->', '', text, flags=re.S)


def check_holds(slugs):
    """Return ["file:line  offending text", ...] for scheduled slugs that are
    still visible to a crawler on a deployed page.

    Matches the post's URL path, not the bare slug: a held inline link keeps
    its text inside <span data-scheduled-link="the-slug">, and that attribute
    is not something a crawler can follow.
    """
    violations = []
    for slug in slugs:
        needle = "/blog/%s/" % slug
        own_page = (ROOT / "blog" / slug / "index.html").resolve()
        for path in deployed_paths():
            # A held post's own canonical, og:url, schema and footer self-link
            # all name its URL. They sit on the noindex page itself, so they
            # are not a discovery path — only pointers from OTHER pages are.
            if path.resolve() == own_page:
                continue
            live = strip_held(path.read_text(encoding="utf-8"))
            if needle not in live:
                continue
            rel = path.relative_to(ROOT).as_posix()
            for line in live.splitlines():
                if needle in line:
                    violations.append("%s: %s" % (rel, line.strip()[:110]))
    return violations


# ---------------------------------------------------------------------------
# post page
# ---------------------------------------------------------------------------
def publish_post_page(slug, date):
    path = ROOT / "blog" / slug / "index.html"
    if not path.exists():
        raise PublishError("post file not found: %s" % path)

    t = original = path.read_text(encoding="utf-8")
    iso, nice = date.isoformat(), human(date)

    # 1-2. OpenGraph article times
    t = sub_once(t, r'(<meta property="article:published_time" content=")[\d-]{10}(">)',
                 r"\g<1>%s\g<2>" % iso, "article:published_time")
    t = sub_once(t, r'(<meta property="article:modified_time" content=")[\d-]{10}(">)',
                 r"\g<1>%s\g<2>" % iso, "article:modified_time")

    # 3-4. BlogPosting schema
    t = sub_once(t, r'("datePublished": ")[\d-]{10}(")',
                 r"\g<1>%s\g<2>" % iso, "schema datePublished")
    t = sub_once(t, r'("dateModified": ")[\d-]{10}(")',
                 r"\g<1>%s\g<2>" % iso, "schema dateModified")

    # 5. visible byline date
    t = sub_once(t, r'<time datetime="[\d-]{10}">[^<]*</time>',
                 '<time datetime="%s">%s</time>' % (iso, nice), "byline <time>")

    # 6. "Published <date>." in the sources block.
    #    Anchored so the "Retrieved <date>" lines above it are left alone —
    #    those record when the sources were checked and must not move.
    t = sub_once(t, r'(<p class="sources-updated">Published )\d{1,2} [A-Z][a-z]+ \d{4}',
                 r"\g<1>%s" % nice, "sources-updated published date")

    # 7. release from noindex, dropping the scheduling note with it
    t = sub_once(
        t,
        r'[ \t]*<!-- SCHEDULED POST:.*?-->\n[ \t]*<meta name="robots" content="noindex, follow">',
        '    <meta name="robots" content="index, follow">',
        "robots noindex block", flags=re.S)

    return path, original, t


def post_schema_facts(text, slug):
    """Pull headline and OG image out of the post's own BlogPosting schema, so
    the hub entry cannot drift from the page it points at."""
    m = re.search(r'"headline": "([^"]+)"', text)
    if not m:
        raise PublishError('no "headline" in the BlogPosting schema for %s' % slug)
    headline = m.group(1)

    img = re.search(r'"image":\s*\{\s*"@type": "ImageObject",\s*"url": "([^"]+)"', text)
    return headline, (img.group(1) if img else None)


# ---------------------------------------------------------------------------
# hub
# ---------------------------------------------------------------------------
def publish_hub_card(text, slug):
    """Unwrap the <template> around the card.

    Matched as one block — comment, open tag, card, close tag — so the
    </template> that gets removed is always this post's own, even while other
    scheduled posts are still wrapped.
    """
    block = (
        r'[ \t]*<!-- SCHEDULED [\d-]{10}.*?-->\n'
        r'[ \t]*<template data-scheduled="%s"[^>]*>\n'
        r'(.*?\n)'
        r'[ \t]*</template>\n' % re.escape(slug)
    )
    return sub_once(text, block, lambda m: m.group(1),
                    "hub <template> block for %s" % slug, flags=re.S)


def publish_hub_schema(text, slug, date, headline, image):
    """Insert the post at the head of the hub's Blog schema blogPost[] array.

    Inserted at publish time rather than held-and-edited: a URL sitting in
    live JSON-LD is a discovery path for Googlebot exactly like an <a href>,
    so a held post must not appear there at all. Newest-first, matching the
    array's existing order.
    """
    url = "https://www.easyvisabooking.com/blog/%s/" % slug
    if url in text:
        raise PublishError(
            "%s is already in the hub Blog schema — a held post must not be listed "
            "there. Remove the entry and let this script insert it." % slug)

    lines = [
        '            {',
        '              "@type": "BlogPosting",',
        '              "headline": "%s",' % headline,
        '              "url": "%s",' % url,
        '              "datePublished": "%s"%s' % (date.isoformat(), "," if image else ""),
    ]
    if image:
        lines.append('              "image": "%s"' % image)
    lines.append('            },')
    entry = "\n".join(lines) + "\n"

    return sub_once(text, r'("blogPost": \[\n)', lambda m: m.group(1) + entry,
                    "hub blogPost[] array opening")


def publish_sitemap_entry(text, slug):
    return sub_once(
        text,
        r'[ \t]*<!-- SCHEDULED [\d-]{10}[^\n]*\n'
        r'(\s*<url>\n\s*<loc>https://www\.easyvisabooking\.com/blog/%s/</loc>\n\s*</url>)\n'
        r'\s*-->' % re.escape(slug),
        lambda m: m.group(1),
        "sitemap entry for %s" % slug)


# ---------------------------------------------------------------------------
# inbound links
# ---------------------------------------------------------------------------
def held_regions(text):
    """Character spans a crawler cannot see — comments and inert templates."""
    spans = []
    for pat in (r'<template data-scheduled=.*?</template>', r'<!--.*?-->'):
        spans += [m.span() for m in re.finditer(pat, text, flags=re.S)]
    return spans


def hold_links(slug, publish_on):
    """Wrap every inbound link to `slug` in a SCHEDULED LINK comment.

    Three shapes are handled, because those are the three the posts use:
      * a whole related-post <article class="post-card"> containing the link
      * a standalone <a>...</a> that starts its own line (footer link lists)
      * an inline link mid-sentence, demoted to a <span> that keeps its text

    Anything else — a URL sitting in JSON-LD, say — is reported for the author
    to handle rather than rewritten blind. --check is the backstop that proves
    none were missed.

    Returns (writes, held_count, manual_list).
    """
    writes, wrapped, manual = [], 0, []
    own_page = (ROOT / "blog" / slug / "index.html").resolve()
    needle = "/blog/%s/" % slug

    for path in deployed_paths():
        if path.suffix.lower() != ".html" or path.resolve() == own_page:
            continue
        text = path.read_text(encoding="utf-8")
        if needle not in text:
            continue
        rel = path.relative_to(ROOT).as_posix()

        hidden = held_regions(text)
        def is_hidden(pos):
            return any(a <= pos < b for a, b in hidden)

        # Candidate blocks, widest first: a card wins over an anchor inside it.
        #
        # Only .post-card articles qualify. Matching bare <article> would catch
        # the <article> wrapping a whole post body whenever the body happens to
        # link to the held post, and comment the entire page out.
        blocks, inline = [], []
        for m in re.finditer(
                r'<article\b[^>]*class="[^"]*post-card[^"]*"[^>]*>.*?</article>',
                text, flags=re.S):
            if slug in m.group(0) and not is_hidden(m.start()):
                blocks.append(m.span())
        for m in re.finditer(
                r'<a\b[^>]*href="[^"]*/blog/%s/"[^>]*>.*?</a>' % re.escape(slug),
                text, flags=re.S):
            if is_hidden(m.start()) or any(a <= m.start() < b for a, b in blocks):
                continue
            # Standalone means the anchor both starts its line and follows a
            # closed tag. A link can start a line and still sit mid-sentence
            # in wrapped markup — commenting that out would eat the prose.
            line_start = text.rfind("\n", 0, m.start()) + 1
            before = text[:m.start()].rstrip()
            if text[line_start:m.start()].strip() or not before.endswith(">"):
                inline.append(m.span())  # mid-sentence: demote, don't comment
                continue
            blocks.append(m.span())

        # An inline anchor is demoted to a <span> that keeps the visible text
        # and drops the href, so the sentence still reads and there is no URL
        # to follow. Only a bare <a href="..."> qualifies — anything carrying
        # classes or other attributes would lose them on the round trip.
        edits = [(s, e, "wrap") for s, e in blocks]
        for start, end in inline:
            anchor = text[start:end]
            if re.match(r'^<a href="/blog/%s/">' % re.escape(slug), anchor):
                edits.append((start, end, "demote"))

        # Report every remaining live mention no edit covers.
        covered = [(s, e) for s, e, _ in edits]
        for m in re.finditer(re.escape(needle), text):
            if is_hidden(m.start()) or any(a <= m.start() < b for a, b in covered):
                continue
            line = text[text.rfind("\n", 0, m.start()) + 1:
                        text.find("\n", m.start())].strip()
            manual.append("%s: %s" % (rel, line[:110]))

        if not edits:
            continue

        # Apply back-to-front so earlier offsets stay valid.
        for start, end, kind in sorted(edits, reverse=True):
            if kind == "demote":
                inner = re.sub(r'^<a [^>]*>|</a>$', '', text[start:end])
                text = (text[:start]
                        + '<span data-scheduled-link="%s" data-publish-on="%s">%s</span>'
                          % (slug, publish_on, inner)
                        + text[end:])
            else:
                line_start = text.rfind("\n", 0, start) + 1
                indent = text[line_start:start]
                block = text[line_start:end]
                text = (text[:line_start]
                        + "%s<!-- SCHEDULED LINK %s %s\n%s\n%s-->"
                          % (indent, publish_on, slug, block, indent)
                        + text[end:])
            wrapped += 1
        writes.append((path, text))

    return writes, wrapped, manual


def reveal_links(slug, pending):
    """Uncomment every held inbound link to this post across the whole site.

    Held links look like:

        <!-- SCHEDULED LINK 2026-08-19 the-slug
        <a href="/blog/the-slug/">Anchor text</a>
        -->

    and demoted inline links look like:

        <span data-scheduled-link="the-slug" data-publish-on="2026-08-19">text</span>

    which becomes <a href="/blog/the-slug/">text</a> again.

    Edits go into `pending` (path -> text), which is also read from, so the hub
    page can be edited here and by the card/schema steps in the same run without
    one overwriting the other. Returns the number of links revealed. Zero is
    allowed but warned about — a post with no inbound links publishes orphaned.
    """
    comment = (
        r'[ \t]*<!-- SCHEDULED LINK [\d-]{10} %s[ \t]*\n'
        r'(.*?)\n'
        r'[ \t]*-->' % re.escape(slug)
    )
    span = r'<span data-scheduled-link="%s"[^>]*>(.*?)</span>' % re.escape(slug)
    href = '<a href="/blog/%s/">' % slug

    total = 0
    for path in deployed_paths():
        if path.suffix.lower() != ".html":
            continue
        text = pending.get(path, None)
        if text is None:
            text = path.read_text(encoding="utf-8")
        new, n1 = re.subn(comment, lambda m: m.group(1), text, flags=re.S)
        new, n2 = re.subn(span, lambda m: href + m.group(1) + "</a>", new, flags=re.S)
        if n1 + n2:
            pending[path] = new
            total += n1 + n2
    return total


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Publish scheduled blog posts.")
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD)")
    ap.add_argument("--slug", help="publish this slug now regardless of its scheduled date")
    ap.add_argument("--dry-run", action="store_true", help="report without writing")
    ap.add_argument("--check", action="store_true",
                    help="verify every held post is invisible to crawlers, then exit")
    ap.add_argument("--hold", metavar="SLUG",
                    help="wrap this scheduled post's inbound links so crawlers cannot reach it")
    args = ap.parse_args()

    today = dt.date.fromisoformat(args.today) if args.today else dt.datetime.now(dt.timezone.utc).date()

    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    scheduled = queue.get("scheduled", [])

    # ---- guard mode -------------------------------------------------------
    if args.check:
        slugs = [e["slug"] for e in scheduled]
        if not slugs:
            print("nothing scheduled — nothing to hide.")
            return 0
        violations = check_holds(slugs)
        if violations:
            print("ERROR: scheduled posts are visible to crawlers on deployed pages.",
                  file=sys.stderr)
            print("Googlebot will follow these, hit the noindex, and log the URL as",
                  file=sys.stderr)
            print("'Excluded by noindex tag' in Search Console.\n", file=sys.stderr)
            for v in violations:
                print("  " + v, file=sys.stderr)
            print("\nWrap each in <!-- SCHEDULED LINK <publishOn> <slug> ... --> (see blog/README.md).",
                  file=sys.stderr)
            return 1
        print("ok: %d scheduled post(s) fully held — %s" % (len(slugs), ", ".join(slugs)))
        return 0

    # ---- hold mode --------------------------------------------------------
    if args.hold:
        entry = next((e for e in scheduled if e["slug"] == args.hold), None)
        if not entry:
            print("%r is not in the scheduled queue — add it to blog/publish-queue.json first."
                  % args.hold, file=sys.stderr)
            return 1

        writes, wrapped, manual = hold_links(args.hold, entry["publishOn"])
        for path, text in writes:
            if not args.dry_run:
                write(path, text)
            print("%s %d link(s) in %s"
                  % ("would wrap" if args.dry_run else "wrapped",
                     sum(1 for _ in re.finditer(r'<!-- SCHEDULED LINK', text)),
                     path.relative_to(ROOT).as_posix()))

        print("\n%s %d inbound link block(s)."
              % ("would hold" if args.dry_run else "held", wrapped))
        if manual:
            print("\nStill exposed — handle these by hand (an inline link keeps its text,")
            print("a hub JSON-LD entry is simply deleted and re-inserted on publish):",
                  file=sys.stderr)
            for m in manual:
                print("  " + m, file=sys.stderr)
            print("\nThen re-run --check.", file=sys.stderr)
            return 1
        if args.dry_run:
            print("dry run: no files written")
        return 0

    if args.slug:
        due = [e for e in scheduled if e["slug"] == args.slug]
        if not due:
            print("nothing scheduled with slug %r" % args.slug)
            return 0
    else:
        due = [e for e in scheduled if dt.date.fromisoformat(e["publishOn"]) <= today]

    if not due:
        nxt = min((e["publishOn"] for e in scheduled), default=None)
        print("nothing due on %s." % today, ("next: %s" % nxt) if nxt else "queue is empty.")
        return 0

    # One buffer for every file this run touches. The hub is edited by three
    # separate steps (card, schema, its own footer link); routing them all
    # through here is what stops the last write from discarding the others.
    pending = {}
    published = []

    # Build every edit in memory first. If any post fails, nothing is written,
    # so the repo is never left with a half-published post.
    for entry in due:
        slug = entry["slug"]
        date = today if args.slug else dt.date.fromisoformat(entry["publishOn"])
        if date > today:
            date = today
        try:
            path, _before, after = publish_post_page(slug, date)
            pending[path] = after
            headline, image = post_schema_facts(after, slug)

            hub = pending.get(HUB) or HUB.read_text(encoding="utf-8")
            hub = publish_hub_card(hub, slug)
            pending[HUB] = publish_hub_schema(hub, slug, date, headline, image)

            sitemap = pending.get(SITEMAP) or SITEMAP.read_text(encoding="utf-8")
            pending[SITEMAP] = publish_sitemap_entry(sitemap, slug)

            n_links = reveal_links(slug, pending)
        except PublishError as exc:
            print("ERROR publishing %s: %s" % (slug, exc), file=sys.stderr)
            print("Nothing was written. Fix the markup or publish by hand.", file=sys.stderr)
            return 1

        published.append(dict(entry, publishedOn=date.isoformat()))
        print("%s %s  ->  %s  (%d inbound link(s) revealed)"
              % ("would publish" if args.dry_run else "publishing", slug, date, n_links))
        if n_links == 0:
            print("  WARNING: no held inbound links found for %s — it will publish "
                  "with no internal links pointing at it." % slug)

    if args.dry_run:
        print("\ndry run: no files written")
        return 0

    for path, text in pending.items():
        write(path, text)

    done = {e["slug"] for e in published}
    queue["scheduled"] = [e for e in scheduled if e["slug"] not in done]
    queue.setdefault("published", []).extend(published)
    write(QUEUE, json.dumps(queue, indent=2, ensure_ascii=False) + "\n")

    print("\npublished %d post(s). %d still scheduled."
          % (len(published), len(queue["scheduled"])))

    # Whatever is still held must still be invisible after this run's edits.
    still_held = [e["slug"] for e in queue["scheduled"]]
    if still_held:
        leaks = check_holds(still_held)
        if leaks:
            print("\nWARNING: still-scheduled posts are now exposed:", file=sys.stderr)
            for v in leaks:
                print("  " + v, file=sys.stderr)

    # consumed by the workflow to build the commit message
    print("PUBLISHED_SLUGS=" + ",".join(sorted(done)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
