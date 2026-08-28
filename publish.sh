#!/bin/bash
# Uso: ./publish.sh posts/mi-post/mi-post.md
set -e

SRC="$1"
if [ -z "$SRC" ] || [ ! -f "$SRC" ]; then
  echo "Uso: ./publish.sh ruta/al/archivo.md"
  exit 1
fi

TYPE=$(awk -F': ' '/^type:/{ $1=""; sub(/^ /,""); print; exit }' "$SRC")
TITLE=$(awk -F': ' '/^title:/{ $1=""; sub(/^ /,""); print; exit }' "$SRC")
DIR=$(dirname "$SRC")
SLUG=$(basename "$DIR")

if [ "$TYPE" = "Page" ]; then
  TEMPLATE="templates/page.html"
else
  TEMPLATE="templates/post.html"
fi

pandoc "$SRC" -s --template="$TEMPLATE" -o "$DIR/index.html"
echo "✔ Publicado en $DIR/index.html"

if grep -qE '^portfolio:\s*true\s*$' "$SRC"; then
  python3 scripts/add_project_card.py "$SLUG" "$TITLE" "index.html"
fi

python3 scripts/generate_feed.py
python3 scripts/generate_tags.py
