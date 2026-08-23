#!/bin/bash
# Reconstruye tags/ y feed.xml desde cero (borra huérfanos) y republica
# TODOS los posts de primer nivel + about, en un solo paso.
#
# Uso: ./scripts/rebuild.sh
#
# Cuándo correrlo: después de sacar/renombrar una etiqueta en varios posts,
# o si sospechás que quedaron carpetas de tags/ viejas sin usar.
set -e

echo "→ Borrando tags/ y feed.xml para reconstruir de cero..."
rm -rf tags
rm -f feed.xml

if [ -f about/about.md ]; then
  echo "→ Republicando about..."
  ./publish.sh about/about.md
fi

echo "→ Republicando todos los posts de primer nivel..."
for f in posts/*/*.md; do
  ./publish.sh "$f"
done

echo "→ Republicando sub-páginas anidadas (si las hay)..."
for f in posts/*/*/*.md; do
  [ -e "$f" ] || continue
  ./publish.sh "$f"
done

echo ""
echo "✔ Reconstrucción completa. Revisá 'git status' para ver qué cambió"
echo "  (tags/ borradas que ya no correspondían deberían aparecer como 'deleted')."
