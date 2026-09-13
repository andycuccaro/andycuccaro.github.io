#!/usr/bin/env python3
"""
Genera feed.xml a partir de todos los posts/*/*.md de primer nivel
(no incluye sub-páginas anidadas como posts/suzy/making-of/).
Se llama automáticamente desde publish.sh en cada publicación.
"""
import glob
from datetime import datetime

from records import parse_front_matter
from rss_utils import SITE_URL, SITE_TITLE, build_rss
from site_config import CONFIG

SITE_DESCRIPTION = CONFIG["SITE_TAGLINE"]


def main():
    items = []
    # Solo posts de primer nivel: posts/<slug>/<slug>.md
    for path in glob.glob("posts/*/*.md"):
        parts = path.split("/")
        if len(parts) != 3:
            continue  # se salta sub-páginas anidadas
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

    feed = build_rss(
        items,
        feed_title=SITE_TITLE,
        feed_description=SITE_DESCRIPTION,
        feed_self_url=f"{SITE_URL}/feed.xml",
    )

    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(feed)

    print(f"✔ feed.xml generado con {len(items)} entradas")


if __name__ == "__main__":
    main()
