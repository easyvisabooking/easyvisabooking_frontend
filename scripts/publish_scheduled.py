#!/usr/bin/env python3
"""
Publish scheduled blog posts.

Posts are written and committed up front but held back until their publish date:

  * the post page carries  <meta name="robots" content="noindex, follow">
  * its card in blog/index.html sits inside an inert <template data-scheduled="...">
  * its <url> entry in sitemap.xml is commented out
  * every publish-date field still reads the day it was written

This script publishes anything whose publishOn date has arrived:

  1. stamps the real publish date into all six date fields
  2. flips robots to "index, follow"
  3. unwraps the <template> around the hub card
  4. uncomments the sitemap entry
  5. updates datePublished in the hub's Blog schema
  6. moves the entry from "scheduled" to "published" in blog/publish-queue.json

Run by .github/workflows/publish-scheduled-posts.yml once a day. Every edit is
anchored and asserted, so a markup change upstream fails loudly instead of
silently publishing something half-wired.

Usage
    python scripts/publish_scheduled.py                      # publish anything due today (UTC)
    python scripts/publish_scheduled.py --dry-run            # show what would change
    python scripts/publish_scheduled.py --today 2026-08-15   # pretend it is that date
    python scripts/publish_scheduled.py --slug <slug>        # publish one post now, date = today

Exit codes
    0  finished (whether or not anything was published)
    1  a post was due but its markup did not match; nothing was written
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

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


class PublishError(Exception):
    """Markup did not match. Nothing is written when this is raised."""


def human(date: dt.date) -> str:
    """2026-08-15 -> '15 August 2026' (no leading zero, matching the posts)."""
    return "%d %s %d" % (date.day, MONTHS[date.month - 1], date.year)


def sub_once(text, pattern, repl, what, flags=0):
    """re.sub that insists on exactly one match."""
    new, n = re.subn(pattern, repl, text, flags=flags)
    if n != 1:
        raise PublishError("expected 1 match for %s, found %d" % (what, n))
    return new


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


# ---------------------------------------------------------------------------
# hub
# ---------------------------------------------------------------------------
def publish_hub_card(text, slug, date):
    """Unwrap the <template> around the card and correct its schema date.

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
    text = sub_once(text, block, lambda m: m.group(1),
                    "hub <template> block for %s" % slug, flags=re.S)

    # datePublished inside the hub's Blog schema, anchored on this post's url
    text = sub_once(
        text,
        r'("url": "https://www\.easyvisabooking\.com/blog/%s/",\s*\n\s*"datePublished": ")[\d-]{10}(")'
        % re.escape(slug),
        r"\g<1>%s\g<2>" % date.isoformat(),
        "hub schema datePublished for %s" % slug)
    return text


def publish_sitemap_entry(text, slug):
    return sub_once(
        text,
        r'[ \t]*<!-- SCHEDULED [\d-]{10}[^\n]*\n'
        r'(\s*<url>\n\s*<loc>https://www\.easyvisabooking\.com/blog/%s/</loc>\n\s*</url>)\n'
        r'\s*-->' % re.escape(slug),
        lambda m: m.group(1),
        "sitemap entry for %s" % slug)


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Publish scheduled blog posts.")
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD)")
    ap.add_argument("--slug", help="publish this slug now regardless of its scheduled date")
    ap.add_argument("--dry-run", action="store_true", help="report without writing")
    args = ap.parse_args()

    today = dt.date.fromisoformat(args.today) if args.today else dt.datetime.now(dt.timezone.utc).date()

    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    scheduled = queue.get("scheduled", [])

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

    hub_text = HUB.read_text(encoding="utf-8")
    sitemap_text = SITEMAP.read_text(encoding="utf-8")
    post_writes = []
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
            hub_text = publish_hub_card(hub_text, slug, date)
            sitemap_text = publish_sitemap_entry(sitemap_text, slug)
        except PublishError as exc:
            print("ERROR publishing %s: %s" % (slug, exc), file=sys.stderr)
            print("Nothing was written. Fix the markup or publish by hand.", file=sys.stderr)
            return 1

        post_writes.append((path, after))
        published.append(dict(entry, publishedOn=date.isoformat()))
        print("%s %s  ->  %s" % ("would publish" if args.dry_run else "publishing", slug, date))

    if args.dry_run:
        print("\ndry run: no files written")
        return 0

    for path, text in post_writes:
        path.write_text(text, encoding="utf-8")
    HUB.write_text(hub_text, encoding="utf-8")
    SITEMAP.write_text(sitemap_text, encoding="utf-8")

    done = {e["slug"] for e in published}
    queue["scheduled"] = [e for e in scheduled if e["slug"] not in done]
    queue.setdefault("published", []).extend(published)
    QUEUE.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("\npublished %d post(s). %d still scheduled."
          % (len(published), len(queue["scheduled"])))
    # consumed by the workflow to build the commit message
    print("PUBLISHED_SLUGS=" + ",".join(sorted(done)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
