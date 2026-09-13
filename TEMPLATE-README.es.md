# Cómo usar este sitio como plantilla para el tuyo

[🇬🇧 Read in English](TEMPLATE-README.md)

Este repo separa dos cosas:

- **El motor** (`publish.sh`, `scripts/`, `templates/`, `style.css`): la parte
  reusable, sin ningún dato personal adentro. No hace falta tocarla para
  arrancar.
- **Tu contenido** (`site.config`, `content/`, `posts/`, `about/`, imágenes,
  favicon): todo lo que sí tenés que reemplazar.

## Requisitos

- [Pandoc](https://pandoc.org/installing.html)
- Python 3 (solo librería estándar — no hace falta `pip install`)
- Git

Nada de Node, nada de frameworks, nada de build steps raros, sin base de datos.

## Para arrancar

```bash
git clone <url-de-este-repo> mi-sitio
cd mi-sitio
chmod +x publish.sh scripts/*.py
```


## 1. Tus datos básicos

Editá `site.config` (un solo archivo, formato `CLAVE="valor"`):

```bash
SITE_TITLE="Tu Nombre"
SITE_ROLE="Tu rol / profesión"
SITE_URL="https://tu-dominio.com"
SITE_TAGLINE="Una descripción corta de una línea."
COPYRIGHT_YEAR="2026"
DEMO_REEL_EMBED_URL="https://player.vimeo.com/video/TU_VIDEO_ID"
OG_IMAGE_URL="https://tu-dominio.com/og-image.jpg"
```

Esto alimenta el `<title>`, las etiquetas Open Graph (la vista previa que se
ve al compartir el link), el feed RSS, y el header/footer de **todas** las
páginas — no hay que tocar HTML en ningún otro lado para esto.

## 2. Tu linktree

Editá `content/links.txt`. Cada entrada es un bloque de `clave: valor`,
separado del siguiente por una línea con exactamente `---`:

```
title: Instagram
desc: Mi arte y proceso
url: https://instagram.com/tu-usuario
footer: true
```

- `footer: true` es opcional — decide si ese link también aparece en el pie
  de página de todo el sitio (no solo en `/links/`).
- Para agregar un separador visual entre grupos de links:
  ```
  separator: true
  ```
- Los links internos (que empiezan con `/`) no llevan `target="_blank"`
  automáticamente; los externos (`http://`/`https://`) sí.

## 3. Tu portfolio (la home)

`content/portfolio.txt` es una lista de slugs, uno por línea, en el orden en
que querés que aparezcan como miniaturas en la home:

```
mi-primer-proyecto
otro-proyecto
```

Cada slug tiene que tener un post correspondiente en
`posts/<slug>/<slug>.md` con `portfolio: true` en su front matter (ver
punto 5). El título y la miniatura (`media/img/thumb.webp`) se toman de ahí
automáticamente.

## 4. Tu "About" y tu contenido existente

- Reemplazá `about/about.md` por tu propio texto (Markdown normal).
- Borrá el contenido de `posts/` (son ejemplos de otra persona) y empezá el
  tuyo — ver el punto 5 para el formato.
- Reemplazá `favicon.ico`, `favicon-16x16.png`, `favicon-32x32.png`,
  `apple-touch-icon.png`, y `og-image.jpg` por los tuyos (mismos nombres de
  archivo, mismas dimensiones).

## 5. Publicar contenido nuevo

Cada post/proyecto vive en su propia carpeta: `posts/mi-post/mi-post.md`,
con un front matter mínimo:

```markdown
---
title: Mi Post
type: Article
---

Contenido en Markdown normal.
```

- `type` es una etiqueta libre (`Article`, `Project`, lo que quieras) — se
  muestra tal cual en la página del post y en el listado de `/posts/`.
- `type: Page` es especial: usa una plantilla sin fecha, sin "related
  posts", pensada para páginas únicas como el About.
- `portfolio: true` (opcional): si lo agregás, el post entra a la home
  automáticamente la próxima vez que lo publiques (y a `content/portfolio.txt`,
  al final — reordená el archivo a mano si querés otra posición).
- `date: YYYY-MM-DD` (opcional): sin fecha, el post no aparece en ningún
  feed RSS (para no romper el orden cronológico con fechas inventadas), pero
  sigue apareciendo en `/posts/` igual.
- `tags:` (opcional): lista de etiquetas. Prefijalas con `topic/` o
  `subtopic/` — solo los `topic/` generan su propio feed RSS
  (`/tags/nombre/feed.xml`); los `subtopic/` son solo para navegar/filtrar.

Publicás con:
```bash
./publish.sh posts/mi-post/mi-post.md
```

Esto genera el HTML del post, y **regenera automáticamente** todo lo
derivado: `feed.xml`, las páginas de etiquetas, `posts/index.html`
(paginado de a 25), `index.html` (home), `links/index.html`, y `404.html`.
Nunca edites estos archivos generados a mano — se pisan solos en la próxima
publicación.

## Estructura de imágenes/video por post

Convención (no obligatoria, pero es la que usan los ejemplos):
```
posts/mi-proyecto/
├── mi-proyecto.md
└── media/
    ├── img/
    │   ├── thumb.webp        ← usada en la home
    │   ├── 01.webp
    │   └── full/
    │       └── 01.jpg         ← versión sin comprimir, opcional
    └── vid/
        └── clip.mp4
```

## Qué NO tocar

`templates/_header.html` y `templates/_footer.html` son generados por
`scripts/generate_chrome.py` en cada `publish.sh` — no los edites, se
pisan solos. Si querés cambiar el diseño del header/footer, editá
`scripts/generate_chrome.py`.

## Publicar el sitio (deploy)

El sitio es HTML/CSS/XML estático puro — funciona en GitHub Pages, GitLab
Pages, Netlify, o cualquier hosting estático. Para GitLab Pages en
particular, vas a necesitar un `.gitlab-ci.yml` que copie todo excepto los
archivos fuente del motor a una carpeta `public/` — pedilo en un issue si
querés un punto de partida.

## Licencia

El motor (`publish.sh`, `scripts/`, `templates/`, `style.css`) es libre de
reusar y adaptar. Por favor no reutilices el contenido de ejemplo bajo
`posts/`, `about/`, y `content/` de este repo — es personal del autor
original.
