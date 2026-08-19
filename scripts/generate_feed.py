#!/usr/bin/env python3
"""
Genera feed.xml a partir de todos los posts/*/*.md de primer nivel
(no incluye sub-páginas anidadas como posts/suzy/making-of/).
Se llama automáticamente desde publish.sh en cada publicación.
"""
import glob
import re
from datetime import datetime
from email.utils import format_datetime, formatdate
from xml.sax.saxutils import escape

SITE_URL = "https://andycuccaro.info"
SITE_TITLE = "Andy Cuccaro"
SITE_DESCRIPTION = "2D & 3D Artist based in Buenos Aires — portfolio, articles and posts."

def parse_front_matter(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return None
    meta = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return meta

def main():
    items = []
    # Solo posts de primer nivel: posts/<slug>/<slug>.md
    for path in glob.glob("posts/*/*.md"):
        parts = path.split("/")
        if len(parts) != 3:
            continue  # se salta sub-páginas anidadas (más niveles de profundidad)
        slug = parts[1]
        meta = parse_front_matter(path)
        if not meta or "date" not in meta or "title" not in meta:
            continue  # sin fecha, no entra al feed
        try:
            dt = datetime.strptime(meta["date"][:10], "%Y-%m-%d")
        except ValueError:
            continue
        items.append({
            "title": meta["title"],
            "type": meta.get("type", ""),
            "url": f"{SITE_URL}/posts/{slug}/",
            "date": dt,
        })

    items.sort(key=lambda x: x["date"], reverse=True)

    rss_items = ""
    for item in items:
        pub_date = format_datetime(item["date"])
        rss_items += f"""  <item>
    <title>{escape(item['title'])}</title>
    <link>{item['url']}</link>
    <guid>{item['url']}</guid>
    <pubDate>{pub_date}</pubDate>
    <description>{escape(item['type'])}</description>
  </item>
"""

    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{escape(SITE_TITLE)}</title>
  <link>{SITE_URL}/</link>
  <description>{escape(SITE_DESCRIPTION)}</description>
  <language>en</language>
  <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml" />
  <lastBuildDate>{formatdate(usegmt=True)}</lastBuildDate>
{rss_items}</channel>
</rss>
"""

    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(feed)

    print(f"✔ feed.xml generado con {len(items)} entradas")

if __name__ == "__main__":
    main()
