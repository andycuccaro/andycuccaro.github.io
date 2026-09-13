#!/usr/bin/env python3
"""
Genera:
  - tags/<tag>/index.html   (listado de posts por etiqueta)
  - tags/index.html          (listado de todas las etiquetas)
  - inyecta "Related Posts" en cada posts/<slug>/index.html ya generado

Se llama automáticamente desde publish.sh en cada publicación.
Solo considera posts de primer nivel (posts/<slug>/<slug>.md),
igual que generate_feed.py — no incluye sub-páginas anidadas.
"""
import glob
import os
import re

SITE_TITLE = "Andy Cuccaro"

HEADER = '''<header>
  <h1><a href="/">Andy Cuccaro</a></h1>
  <p class="role">2D &amp; 3D Artist</p>
  <nav>
    <a href="/">Portfolio</a>
    <a href="/posts/">Posts</a>
    <a href="/about/">About</a>
    <a href="/links/">Links</a>
  </nav>
</header>'''

FOOTER = '''<footer>
  <p>© 2026 Andy Cuccaro</p>
  <div class="footer-links">
    <a href="https://www.artstation.com/andycuccaro" target="_blank" rel="noopener noreferrer">ArtStation</a>
    <a href="https://instagram.com/andycuccaro" target="_blank" rel="noopener noreferrer">Instagram</a>
    <a href="https://x.com/andycuccaro" target="_blank" rel="noopener noreferrer">X</a>
    <a href="https://youtube.com/andycuccaro" target="_blank" rel="noopener noreferrer">YouTube</a>
    <a href="https://linkedin.com/in/andycuccaro" target="_blank" rel="noopener noreferrer">LinkedIn</a>
    <a href="mailto:&#97;&#110;&#100;&#121;&#99;&#117;&#99;&#99;&#97;&#114;&#111;&#64;&#112;&#109;&#46;&#109;&#101;">Email</a>
  </div>
</footer>'''

PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="icon" href="/favicon.ico">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Andy Cuccaro</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>

{header}

<main>

<section>
<h1>{heading}</h1>
{body}
</section>

</main>

{footer}

</body>
</html>
'''


def parse_front_matter(path):
    """Parser liviano para nuestro front matter (sin dependencias externas)."""
    with open(path, encoding="utf-8") as f:
        content = f.read()
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return None
    meta = {}
    lines = match.group(1).split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if ":" in line and not line.strip().startswith("-"):
            key, _, value = line.partition(":")
            key, value = key.strip(), value.strip()
            if value == "":
                items = []
                j = i + 1
                while j < len(lines) and lines[j].strip().startswith("-"):
                    items.append(lines[j].strip()[1:].strip())
                    j += 1
                if items:
                    meta[key] = items
                    i = j
                    continue
            meta[key] = value
        i += 1
    return meta


def card_list_html(posts):
    items = ""
    for p in posts:
        date_part = f' · {p["date"]}' if p.get("date") else ""
        items += (
            f'  <li><a href="/posts/{p["slug"]}/">'
            f'<span>{p["title"]}</span>'
            f'<span class="dates">{p.get("type", "")}{date_part}</span>'
            f'</a></li>\n'
        )
    return f'<ul class="card-list">\n{items}</ul>'


def main():
    posts = []
    for path in glob.glob("posts/*/*.md"):
        parts = path.split("/")
        if len(parts) != 3:
            continue  # se salta sub-páginas anidadas
        slug = parts[1]
        meta = parse_front_matter(path)
        if not meta or "title" not in meta:
            continue
        tags = meta.get("tags", [])
        if isinstance(tags, str):
            tags = [tags] if tags else []
        posts.append({
            "slug": slug,
            "title": meta["title"],
            "type": meta.get("type", ""),
            "date": meta.get("date", ""),
            "tags": tags,
        })

    posts.sort(key=lambda p: p.get("date", ""), reverse=True)

    # --- Páginas por etiqueta ---
    tag_map = {}
    for p in posts:
        for t in p["tags"]:
            tag_map.setdefault(t, []).append(p)

    for tag, tag_posts in tag_map.items():
        os.makedirs(f"tags/{tag}", exist_ok=True)
        html = PAGE_TEMPLATE.format(
            title=f"#{tag}",
            header=HEADER,
            heading=f"#{tag}",
            body=card_list_html(tag_posts),
            footer=FOOTER,
        )
        with open(f"tags/{tag}/index.html", "w", encoding="utf-8") as f:
            f.write(html)

    # --- Índice de todas las etiquetas ---
    os.makedirs("tags", exist_ok=True)
    tag_pills = " ".join(
        f'<a class="tag-pill" href="/tags/{t}/">{t} ({len(ps)})</a>'
        for t, ps in sorted(tag_map.items())
    )
    html = PAGE_TEMPLATE.format(
        title="Tags",
        header=HEADER,
        heading="Tags",
        body=f'<p class="tags">{tag_pills}</p>' if tag_pills else "<p>No tags yet.</p>",
        footer=FOOTER,
    )
    with open("tags/index.html", "w", encoding="utf-8") as f:
        f.write(html)

    # --- Inyectar "Related Posts" en cada post ya generado ---
    for p in posts:
        if not p["tags"]:
            continue
        scored = []
        for other in posts:
            if other["slug"] == p["slug"]:
                continue
            shared = set(p["tags"]) & set(other["tags"])
            if shared:
                scored.append((len(shared), other))
        scored.sort(key=lambda x: (x[0], x[1].get("date", "")), reverse=True)
        related = [o for _, o in scored[:5]]

        index_path = f"posts/{p['slug']}/index.html"
        if not os.path.exists(index_path):
            continue
        with open(index_path, encoding="utf-8") as f:
            html = f.read()

        if related:
            section = f'<h2>Related Posts</h2>\n{card_list_html(related)}'
        else:
            section = ""

        new_div = f'<div id="related-posts">\n{section}\n</div>'
        html = re.sub(
            r'<div id="related-posts">.*?</div>',
            new_div.replace("\\", "\\\\"),
            html,
            flags=re.DOTALL,
        )
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html)

    print(f"✔ {len(tag_map)} etiquetas generadas, related posts inyectados en {len([p for p in posts if p['tags']])} posts")


if __name__ == "__main__":
    main()
