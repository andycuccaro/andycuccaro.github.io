#!/usr/bin/env python3
"""
Genera index.html (home) a partir de:
  - site.config           (nombre, rol, tagline, demo reel, imagen OG)
  - content/portfolio.txt (orden curado de proyectos, un slug por línea)
  - el título de cada post (leído de su propio .md)

Se llama automáticamente desde publish.sh en cada publicación.
"""
from generate_chrome import HEADER, FOOTER
from records import parse_front_matter
from site_config import CONFIG

TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{sitetitle} — {siterole}</title>
<meta name="description" content="{sitetagline}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{sitetitle}">
<meta property="og:title" content="{sitetitle} — {siterole}">
<meta property="og:description" content="{sitetagline}">
<meta property="og:image" content="{ogimage}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{sitetitle} — {siterole}">
<meta name="twitter:description" content="{sitetagline}">
<meta name="twitter:image" content="{ogimage}">
<link rel="alternate" type="application/rss+xml" title="{sitetitle} — Posts" href="/feed.xml">
<link rel="stylesheet" href="/style.css">
</head>
<body>

{header}

<main>

<section>
  <h2>Demo Reel</h2>
  <div class="video-wrapper">
    <iframe src="{demoreel}" frameborder="0"
      allow="autoplay; fullscreen; picture-in-picture" allowfullscreen
      title="{sitetitle} Demo Reel"></iframe>
  </div>
</section>

<section>
  <h2>Selected Work</h2>
  <div class="portfolio-grid">
{cards}
  </div>
</section>

</main>

{footer}

</body>
</html>
'''

CARD = '''
    <a class="project-card" href="/posts/{slug}/">
      <img src="/posts/{slug}/media/img/thumb.webp" alt="{title} thumbnail" loading="lazy">
      <span>{title}</span>
    </a>
'''


def main():
    with open("content/portfolio.txt", encoding="utf-8") as f:
        slugs = [line.strip() for line in f if line.strip()]

    cards = ""
    for slug in slugs:
        meta = parse_front_matter(f"posts/{slug}/{slug}.md")
        if not meta:
            print(f"⚠ posts/{slug}/{slug}.md no existe o no tiene front matter — se salta en la home")
            continue
        cards += CARD.format(slug=slug, title=meta["title"])

    html = TEMPLATE.format(
        sitetitle=CONFIG["SITE_TITLE"],
        siterole=CONFIG["SITE_ROLE"],
        sitetagline=CONFIG["SITE_TAGLINE"],
        ogimage=CONFIG["OG_IMAGE_URL"],
        demoreel=CONFIG["DEMO_REEL_EMBED_URL"],
        header=HEADER,
        footer=FOOTER,
        cards=cards,
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✔ index.html (home) generado con {len(slugs)} proyectos")


if __name__ == "__main__":
    main()
