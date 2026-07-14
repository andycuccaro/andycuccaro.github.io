#!/bin/bash
# Uso: ./publish.sh content/projects/mi-proyecto.md
set -e

SRC="$1"
if [ -z "$SRC" ] || [ ! -f "$SRC" ]; then
  echo "Uso: ./publish.sh ruta/al/archivo.md"
  exit 1
fi

TYPE=$(awk '/^type:/{print $2; exit}' "$SRC")
SLUG=$(basename "$SRC" .md)

case "$TYPE" in
  project)
    OUTDIR="projects/$SLUG"
    TEMPLATE="templates/project.html"
    ;;
  article)
    OUTDIR="articles/$SLUG"
    TEMPLATE="templates/article.html"
    ;;
  page)
    OUTDIR="$SLUG"
    TEMPLATE="templates/page.html"
    ;;
  *)
    echo "Error: no encontré un campo 'type:' válido (project / article / page) en $SRC"
    exit 1
    ;;
esac

mkdir -p "$OUTDIR"
pandoc "$SRC" -s --template="$TEMPLATE" -o "$OUTDIR/index.html"

echo "✔ Publicado en $OUTDIR/index.html"
if [ "$TYPE" = "project" ]; then
  echo "  Recordá agregar/actualizar la miniatura en index.html (home)."
elif [ "$TYPE" = "article" ]; then
  echo "  Recordá agregar la línea correspondiente en articles/index.html."
fi
