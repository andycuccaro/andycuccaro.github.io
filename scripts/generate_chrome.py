"""
Fuente única de verdad para el <header> y <footer> del sitio.

Genera:
  - HEADER, FOOTER: strings Python, importados por generate_home.py,
    generate_links.py, generate_404.py y generate_tags.py.
  - templates/_header.html, templates/_footer.html: los mismos bloques,
    como "partials" de Pandoc, incluidos por templates/post.html y
    templates/page.html vía $_header()$ / $_footer()$.

Se llama automáticamente desde publish.sh, ANTES de correr Pandoc
(los partials tienen que existir antes de que Pandoc los use).
"""
from records import parse_records
from site_config import CONFIG


def build_header():
    return f'''<header>
  <h1><a href="/">{CONFIG['SITE_TITLE']}</a></h1>
  <p class="role">{CONFIG['SITE_ROLE']}</p>
  <nav>
    <a href="/">Portfolio</a>
    <a href="/posts/">Posts</a>
    <a href="/about/">About</a>
    <a href="/links/">Links</a>
  </nav>
</header>'''


def build_footer():
    records = parse_records("content/links.txt")
    footer_links = [r for r in records if r.get("footer") == "true"]
    links_html = "\n".join(
        f'    <a href="{r["url"]}"{"" if r["url"].startswith(("mailto:", "/")) else " target=\"_blank\" rel=\"noopener noreferrer\""}>{r["title"]}</a>'
        for r in footer_links
    )
    return f'''<footer>
  <p>© {CONFIG['COPYRIGHT_YEAR']} {CONFIG['SITE_TITLE']}</p>
  <div class="footer-links">
{links_html}
  </div>
</footer>'''


HEADER = build_header()
FOOTER = build_footer()


def write_partials():
    with open("templates/_header.html", "w", encoding="utf-8") as f:
        f.write(HEADER + "\n")
    with open("templates/_footer.html", "w", encoding="utf-8") as f:
        f.write(FOOTER + "\n")


if __name__ == "__main__":
    write_partials()
    print("✔ templates/_header.html y templates/_footer.html generados")
