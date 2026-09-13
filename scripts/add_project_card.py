#!/usr/bin/env python3
"""
Asegura que un slug esté presente en content/portfolio.txt (lo agrega al
final si falta). La regeneración real de index.html la hace generate_home.py,
llamado después de este script en publish.sh.

Uso: add_project_card.py <slug>
"""
import sys


def main():
    if len(sys.argv) != 2:
        print("Uso: add_project_card.py <slug>", file=sys.stderr)
        sys.exit(1)

    slug = sys.argv[1]
    path = "content/portfolio.txt"

    try:
        with open(path, encoding="utf-8") as f:
            slugs = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        slugs = []

    if slug in slugs:
        print(f"  '{slug}' ya está en {path}")
        return

    slugs.append(slug)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(slugs) + "\n")
    print(f"✔ '{slug}' agregado a {path} (al final — reordená el archivo a mano si querés otra posición)")


if __name__ == "__main__":
    main()
