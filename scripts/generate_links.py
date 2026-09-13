#!/usr/bin/env python3
"""
Genera links/index.html a partir de site.config + content/links.txt.
Se llama automáticamente desde publish.sh en cada publicación.
"""
import os

from generate_chrome import HEADER, FOOTER
from records import parse_records
from site_config import CONFIG

TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="icon" href="/favicon.ico">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Links — {sitetitle}</title>
<meta property="og:type" content="website">
<meta property="og:site_name" content="{sitetitle}">
<meta property="og:title" content="Links — {sitetitle}">
<meta property="og:description" content="{sitetagline}">
<meta property="og:image" content="{ogimage}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Links — {sitetitle}">
<meta name="twitter:description" content="{sitetagline}">
<meta name="twitter:image" content="{ogimage}">
<link rel="stylesheet" href="/style.css">
</head>
<body>

{header}

<main class="links-page">

<ul class="link-list">
{items}
</ul>

</main>

{footer}

</body>
</html>
'''

ITEM = '''  <li>
    <a href="{url}"{target}>
      <span class="link-title">{title}</span>
      <span class="link-desc">{desc}</span>
    </a>
  </li>'''


def main():
    records = parse_records("content/links.txt")

    parts = []
    for r in records:
        if r.get("separator") == "true":
            parts.append('</ul>\n\n<hr class="link-separator">\n\n<ul class="link-list">')
            continue
        is_external = r["url"].startswith(("http://", "https://"))
        target = ' target="_blank" rel="noopener noreferrer"' if is_external else ""
        parts.append(ITEM.format(
            url=r["url"], target=target, title=r["title"], desc=r.get("desc", r["title"])
        ))

    items = "\n".join(parts)

    html = TEMPLATE.format(
        sitetitle=CONFIG["SITE_TITLE"],
        sitetagline=CONFIG["SITE_TAGLINE"],
        ogimage=CONFIG["OG_IMAGE_URL"],
        header=HEADER,
        footer=FOOTER,
        items=items,
    )

    os.makedirs("links", exist_ok=True)
    with open("links/index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✔ links/index.html generado con {len(records)} entradas")


if __name__ == "__main__":
    main()
