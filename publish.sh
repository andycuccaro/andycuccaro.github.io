#!/bin/bash
# Uso: ./publish.sh projects/mi-proyecto/mi-proyecto.md
set -e

SRC="$1"
if [ -z "$SRC" ] || [ ! -f "$SRC" ]; then
  echo "Uso: ./publish.sh ruta/al/archivo.md"
  exit 1
fi

TYPE=$(awk '/^type:/{print $2; exit}' "$SRC")
TITLE=$(awk -F': ' '/^title:/{ $1=""; sub(/^ /,""); print; exit }' "$SRC")
DIR=$(dirname "$SRC")
SLUG=$(basename "$DIR")

case "$TYPE" in
  project)
    TEMPLATE="templates/project.html"
    ;;
  article)
    TEMPLATE="templates/article.html"
    ;;
  page)
    TEMPLATE="templates/page.html"
    ;;
  *)
    echo "Error: no encontré un campo 'type:' válido (project / article / page) en $SRC"
    exit 1
    ;;
esac

pandoc "$SRC" -s --template="$TEMPLATE" -o "$DIR/index.html"

echo "✔ Publicado en $DIR/index.html"
if [ "$TYPE" = "project" ]; then
  python3 scripts/add_project_card.py "$SLUG" "$TITLE" "index.html"
elif [ "$TYPE" = "article" ]; then
  echo "  Recordá agregar la línea correspondiente en articles/index.html."
fi
