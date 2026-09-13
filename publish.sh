#!/bin/bash
# Uso: ./publish.sh posts/mi-post/mi-post.md
set -e

SRC="$1"
if [ -z "$SRC" ] || [ ! -f "$SRC" ]; then
  echo "Uso: ./publish.sh ruta/al/archivo.md"
  exit 1
fi

# Cargar site.config (nombre, rol, URL, etc.)
set -a
source site.config
set +a

TYPE=$(awk -F': ' '/^type:/{ $1=""; sub(/^ /,""); print; exit }' "$SRC")
TITLE=$(awk -F': ' '/^title:/{ $1=""; sub(/^ /,""); print; exit }' "$SRC")
DIR=$(dirname "$SRC")
SLUG=$(basename "$DIR")

if [ "$TYPE" = "Page" ]; then
  TEMPLATE="templates/page.html"
else
  TEMPLATE="templates/post.html"
fi

# Generar los partials (header/footer) ANTES de correr Pandoc, ya que
# templates/post.html y templates/page.html los incluyen vía $_header()$/$_footer()$.
python3 scripts/generate_chrome.py

pandoc "$SRC" -s --wrap=none --template="$TEMPLATE" \
  --metadata sitetitle="$SITE_TITLE" \
  --metadata sitetagline="$SITE_TAGLINE" \
  --metadata ogimage="$OG_IMAGE_URL" \
  -o "$DIR/index.html"
echo "✔ Publicado en $DIR/index.html"

if grep -qE '^portfolio:\s*true\s*$' "$SRC"; then
  python3 scripts/add_project_card.py "$SLUG"
fi

python3 scripts/generate_feed.py
python3 scripts/generate_tags.py
python3 scripts/generate_home.py
python3 scripts/generate_links.py
python3 scripts/generate_404.py
