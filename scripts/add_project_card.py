#!/usr/bin/env python3
"""
Inserta o actualiza la miniatura de un proyecto en index.html (portfolio-grid).
Uso: add_project_card.py <slug> <title> <index_html_path>
"""
import re
import sys

def main():
    if len(sys.argv) != 4:
        print("Uso: add_project_card.py <slug> <title> <index_html_path>", file=sys.stderr)
        sys.exit(1)

    slug, title, index_path = sys.argv[1], sys.argv[2], sys.argv[3]

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    card = (
        f'    <a class="project-card" href="/posts/{slug}/">\n'
        f'      <img src="/posts/{slug}/media/img/thumb.webp" alt="{title} thumbnail" loading="lazy">\n'
        f'      <span>{title}</span>\n'
        f'    </a>'
    )

    # Buscar si ya existe una card para este slug (por su href)
    existing_pattern = re.compile(
        r'    <a class="project-card" href="/posts/' + re.escape(slug) + r'/">.*?</a>',
        re.DOTALL
    )

    if existing_pattern.search(content):
        content = existing_pattern.sub(card, content)
        print(f"✔ Miniatura de '{slug}' actualizada en {index_path}")
    else:
        grid_open = '<div class="portfolio-grid">'
        idx = content.find(grid_open)
        if idx == -1:
            print(f"Error: no encontré '{grid_open}' en {index_path}", file=sys.stderr)
            sys.exit(1)
        close_idx = content.find("</div>", idx)
        if close_idx == -1:
            print(f"Error: no encontré el cierre de portfolio-grid en {index_path}", file=sys.stderr)
            sys.exit(1)
        content = content[:close_idx] + card + "\n\n  " + content[close_idx:]
        print(f"✔ Miniatura de '{slug}' agregada a {index_path}")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    main()
