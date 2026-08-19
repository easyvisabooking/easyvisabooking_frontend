#!/usr/bin/env python3
"""
Wire built posts into the hub, the sitemap and the publish queue.

Each post is added in its HELD form, exactly as blog/README.md requires:

  * the hub card sits inside an inert <template data-scheduled>
  * the sitemap <url> sits inside an XML comment
  * no entry is added to the hub's Blog schema blogPost[] array

scripts/publish_scheduled.py releases all three on the publish date. Running
this twice is safe: anything already present is skipped.

Usage
    python scripts/wire_posts.py            # wire every spec that is not wired yet
    python scripts/wire_posts.py --check    # report what would change, write nothing
"""

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "post-src"
HUB = ROOT / "blog" / "index.html"
SITEMAP = ROOT / "sitemap.xml"
QUEUE = ROOT / "blog" / "publish-queue.json"

CATEGORIES = {
    "rescheduling": ("Rescheduling &amp; Slots", "cat-rescheduling"),
    "wait-times": ("Wait Times by Country", "cat-wait-times"),
    "expedite": ("Expedite &amp; Emergency", "cat-expedite"),
    "trust": ("Trust &amp; Cost", "cat-trust"),
    "basics": ("Application Basics", "cat-basics"),
}

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


def human(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return "%d %s %d" % (d, MONTHS[m - 1], y)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def hub_card(slug, s):
    label, css = CATEGORIES[s["category"]]
    publish_on = s["publishOn"]
    cover = s["cover"].replace("../../img/", "../img/")
    return """                <!-- SCHEDULED {on}, revealed automatically by scripts/publish_scheduled.py -->
                <template data-scheduled="{slug}" data-publish-on="{on}">
                <article class="post-card wow fadeInUp" data-wow-delay="0.1s" data-category="{cat}">
                    <div class="post-card-media">
                        <img src="{cover}"
                            alt="{alt}"
                            width="1200" height="630" loading="lazy">
                    </div>
                    <div class="post-card-body">
                        <span class="cat {css}">{label}</span>
                        <h3><a href="/blog/{slug}/">{h1}</a></h3>
                        <p>{blurb}</p>
                        <p class="post-meta">
                            <time datetime="{on}">{on_human}</time>
                            <span class="dot">·</span><span>{read} min read</span>
                        </p>
                    </div>
                </article>
                </template>
""".format(on=publish_on, slug=slug, cat=s["category"], cover=cover,
           alt=esc(s["coverAlt"]), css=css, label=label, h1=s["h1"],
           blurb=s["deck"], on_human=human(publish_on), read=s["readTime"])


def sitemap_entry(slug, publish_on):
    return """
  <!-- SCHEDULED {on}, uncommented by scripts/publish_scheduled.py
  <url>
    <loc>https://www.easyvisabooking.com/blog/{slug}/</loc>
  </url>
  -->
""".format(on=publish_on, slug=slug)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    specs = {}
    for p in sorted(SRC.glob("*.json")):
        slug = p.name[: -len(".json")]
        s = json.loads(p.read_text(encoding="utf-8"))
        if "publishOn" in s:
            specs[slug] = s

    hub = HUB.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    queued = {e["slug"] for e in queue["scheduled"]} | {e["slug"] for e in queue["published"]}

    # Newest publish date first, matching the hub's ordering.
    order = sorted(specs.items(), key=lambda kv: kv[1]["publishOn"], reverse=True)

    added = []
    for slug, s in order:
        if slug in hub:
            continue
        anchor = '            <div class="card-grid">\n\n'
        if anchor not in hub:
            print("FAIL: could not find the card grid opening in blog/index.html")
            return 1
        hub = hub.replace(anchor, anchor + hub_card(slug, s) + "\n", 1)
        added.append(slug)

    sm_added = []
    for slug, s in order:
        if slug in sitemap:
            continue
        anchor = "\n</urlset>"
        if anchor not in sitemap:
            print("FAIL: could not find </urlset> in sitemap.xml")
            return 1
        sitemap = sitemap.replace(anchor, sitemap_entry(slug, s["publishOn"]) + anchor, 1)
        sm_added.append(slug)

    q_added = []
    for slug, s in sorted(specs.items(), key=lambda kv: kv[1]["publishOn"]):
        if slug in queued:
            continue
        queue["scheduled"].append({
            "slug": slug,
            "title": s["h1"],
            "publishOn": s["publishOn"],
        })
        q_added.append(slug)
    queue["scheduled"].sort(key=lambda e: e["publishOn"])

    print("hub cards added:      %d  %s" % (len(added), ", ".join(added) or "none"))
    print("sitemap entries added:%d  %s" % (len(sm_added), ", ".join(sm_added) or "none"))
    print("queue entries added:  %d  %s" % (len(q_added), ", ".join(q_added) or "none"))

    if args.check:
        print("\n--check: nothing written")
        return 0

    with open(HUB, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(hub)
    with open(SITEMAP, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(sitemap)
    with open(QUEUE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(queue, indent=2, ensure_ascii=False) + "\n")
    print("\nwritten. run scripts/publish_scheduled.py --check next.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
