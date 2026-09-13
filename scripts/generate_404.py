#!/usr/bin/env python3
"""
Genera 404.html a partir de site.config.
Se llama automáticamente desde publish.sh en cada publicación.
"""
from generate_chrome import HEADER, FOOTER
from site_config import CONFIG

TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>404 — {sitetitle}</title>
<link rel="icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/style.css">
</head>
<body>

{header}

<main class="error-page">
  <p class="error-code">404</p>
  <p class="error-msg">This page doesn't exist.</p>
  <a href="/">← Back to Portfolio</a>
</main>

{footer}

</body>
</html>
'''


def main():
    html = TEMPLATE.format(
        sitetitle=CONFIG["SITE_TITLE"],
        header=HEADER,
        footer=FOOTER,
    )
    with open("404.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✔ 404.html generado")


if __name__ == "__main__":
    main()
