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
from datetime import datetime

from rss_utils import SITE_URL, build_rss

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
{feed_link}<link rel="stylesheet" href="/style.css">
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


def split_tag(raw):
    """'topic/art' -> ('art', 'topic'); 'blender' (sin prefijo) -> ('blender', 'subtopic')."""
    if raw.startswith("topic/"):
        return raw[len("topic/"):], "topic"
    if raw.startswith("subtopic/"):
        return raw[len("subtopic/"):], "subtopic"
    return raw, "subtopic"  # sin prefijo: tratamos como subtopic (sin feed) por seguridad


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
        raw_tags = meta.get("tags", [])
        if isinstance(raw_tags, str):
            raw_tags = [raw_tags] if raw_tags else []
        tags = [split_tag(t)[0] for t in raw_tags]  # nombres pelados, para related/tag_map
        posts.append({
            "slug": slug,
            "title": meta["title"],
            "type": meta.get("type", ""),
            "date": meta.get("date", ""),
            "tags": tags,
            "raw_tags": raw_tags,
        })

    posts.sort(key=lambda p: p.get("date", ""), reverse=True)

    # --- Clasificar cada tag pelado como topic o subtopic ---
    # (si aparece como topic/ en CUALQUIER post, se lo considera topic)
    tag_kind = {}
    for p in posts:
        for raw in p["raw_tags"]:
            name, kind = split_tag(raw)
            if tag_kind.get(name) != "topic":
                tag_kind[name] = kind

    # --- Páginas por etiqueta ---
    tag_map = {}
    for p in posts:
        for t in p["tags"]:
            tag_map.setdefault(t, []).append(p)

    for tag, tag_posts in tag_map.items():
        is_topic = tag_kind.get(tag) == "topic"
        os.makedirs(f"tags/{tag}", exist_ok=True)

        if is_topic:
            feed_link = f'<link rel="alternate" type="application/rss+xml" title="Andy Cuccaro — #{tag}" href="/tags/{tag}/feed.xml">\n'
        else:
            feed_link = ""

        html = PAGE_TEMPLATE.format(
            title=f"#{tag}",
            feed_link=feed_link,
            header=HEADER,
            heading=f"#{tag}",
            body=card_list_html(tag_posts),
            footer=FOOTER,
        )
        with open(f"tags/{tag}/index.html", "w", encoding="utf-8") as f:
            f.write(html)

        if not is_topic:
            continue  # los subtopics no llevan feed.xml

        # Feed RSS de la etiqueta (mismos posts, mismo criterio de fecha que feed.xml general)
        feed_items = []
        for p in tag_posts:
            try:
                dt = datetime.strptime(p["date"][:10], "%Y-%m-%d")
            except (ValueError, KeyError):
                continue
            feed_items.append({
                "title": p["title"],
                "type": p.get("type", ""),
                "url": f"{SITE_URL}/posts/{p['slug']}/",
                "date": dt,
            })
        feed_items.sort(key=lambda x: x["date"], reverse=True)

        feed_xml = build_rss(
            feed_items,
            feed_title=f"{SITE_TITLE} — #{tag}",
            feed_description=f"Posts tagged #{tag}",
            feed_self_url=f"{SITE_URL}/tags/{tag}/feed.xml",
        )
        with open(f"tags/{tag}/feed.xml", "w", encoding="utf-8") as f:
            f.write(feed_xml)

    # --- Índice de todas las etiquetas, separado en Topics / Subtopics ---
    os.makedirs("tags", exist_ok=True)

    def pills_for(names):
        return " ".join(
            f'<a class="tag-pill" href="/tags/{t}/">{t} ({len(tag_map[t])})</a>'
            for t in names
        )

    topic_names = sorted(t for t in tag_map if tag_kind.get(t) == "topic")
    subtopic_names = sorted(t for t in tag_map if tag_kind.get(t) != "topic")

    body_parts = []
    if topic_names:
        body_parts.append(f'<h2>Topics</h2>\n<p class="tags">{pills_for(topic_names)}</p>')
    if subtopic_names:
        body_parts.append(f'<h2>Subtopics</h2>\n<p class="tags">{pills_for(subtopic_names)}</p>')
    body = "\n".join(body_parts) if body_parts else "<p>No tags yet.</p>"

    html = PAGE_TEMPLATE.format(
        title="Tags",
        feed_link="",
        header=HEADER,
        heading="Tags",
        body=body,
        footer=FOOTER,
    )
    with open("tags/index.html", "w", encoding="utf-8") as f:
        f.write(html)

    # --- Inyectar chips de tags en cada post ya generado ---
    for p in posts:
        index_path = f"posts/{p['slug']}/index.html"
        if not os.path.exists(index_path):
            continue
        with open(index_path, encoding="utf-8") as f:
            html = f.read()

        if p["tags"]:
            chips = ""
            for t in p["tags"]:
                if tag_kind.get(t) == "topic":
                    chips += (
                        f'<span class="tag-group">'
                        f'<a class="tag-pill is-topic" href="/tags/{t}/">{t}</a>'
                        f'<a class="tag-rss" href="/tags/{t}/feed.xml" title="Subscribe to #{t} via RSS">RSS</a>'
                        f'</span> '
                    )
                else:
                    chips += f'<a class="tag-pill" href="/tags/{t}/">{t}</a> '
            tags_html = f'<div id="tags-block"><p class="tags">{chips.strip()}</p></div>'
        else:
            tags_html = '<div id="tags-block"></div>'

        html = re.sub(
            r'<div id="tags-block">.*?</div>',
            tags_html.replace("\\", "\\\\"),
            html,
            flags=re.DOTALL,
        )
        with open(index_path, "w", encoding="utf-8") as f:
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
