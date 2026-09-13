# andycuccaro.info

[🇬🇧 Read in English](README.md)

El portfolio personal, blog, y linktree de **Andy Cuccaro** — artista 2D & 3D radicado en Buenos Aires, Argentina.

En vivo en **[andycuccaro.info](https://andycuccaro.info)**.

<!-- Espacio para captura: poné acá una captura del home, por ejemplo -->
<!-- ![Captura del home](docs/screenshot.png) -->

## Qué es esto

Un sitio personal completamente estático y sin dependencias — portfolio, artículos, y una página tipo linktree, todo generado desde Markdown con [Pandoc](https://pandoc.org/) y un puñado de scripts chicos en Python. Sin JavaScript, sin frameworks del lado del cliente, sin herramientas de build más allá de lo que ya viene en cualquier máquina Linux típica.

### Puntos destacados

- **Cero JavaScript.** Cada elemento con sensación "interactiva" (galerías de imágenes, estados de hover, modo oscuro) es HTML/CSS puro.
- **Publicación Markdown-first.** Cada post, proyecto y página se escribe en Markdown con un bloque chico de front matter YAML, y se convierte a HTML con un solo comando.
- **Pipeline de contenido unificado.** Proyectos de portfolio, artículos de blog, y tutoriales pasan todos por el mismo script de publicación — la única diferencia es una etiqueta `type:`.
- **Sistema de etiquetas con RSS selectivo.** Los posts pueden llevar etiquetas `topic/` y `subtopic/`; solo los topics tienen su propio feed RSS, para que las suscripciones tengan sentido en vez de saturar.
- **Todo lo que se puede romper, se genera solo.** La grilla de la home, el índice de posts (paginado), las páginas de etiquetas, los feeds RSS, y la página 404 son todos generados por scripts — nunca editados a mano, nunca desincronizados.
- **Reusable por diseño.** El "motor" (`publish.sh`, `scripts/`, `templates/`, `style.css`) está completamente desacoplado del contenido personal (`site.config`, `content/`, `posts/`). Ver [TEMPLATE-README.es.md](TEMPLATE-README.es.md) si querés bifurcar esto y armar tu propio sitio encima.

## Stack

| Parte | Herramienta |
|---|---|
| Markdown → HTML | [Pandoc](https://pandoc.org/) |
| Automatización (feeds, tags, paginación, generación de home/links) | Python 3 (solo librería estándar) |
| Publicación | Un solo script de Bash (`publish.sh`) |
| Estilos | CSS escrito a mano, sin framework |
| Hosting | GitHub Pages + GitLab Pages (espejados) |
| Control de versiones | Git, espejado a GitHub y GitLab |

Sin Node.js, sin paquetes de npm, sin generador de sitio estático de terceros, sin base de datos, sin código del lado del servidor de ningún tipo.

## Estructura del repositorio

```
.
├── site.config          # Configuración general del sitio: nombre, tagline, URL, etc.
├── content/
│   ├── links.txt          # Entradas del linktree
│   └── portfolio.txt      # Orden curado de las tarjetas de portfolio en la home
├── posts/                # Todos los proyectos, artículos y tutoriales (Markdown + HTML generado)
│   └── <slug>/
│       ├── <slug>.md
│       ├── index.html     # Generado — nunca editado a mano
│       └── media/         # Imágenes/video, junto a su post
├── about/                # La página de About/CV
├── links/                # Página de linktree generada
├── tags/                 # Páginas de etiquetas generadas + feeds RSS por topic
├── templates/            # Plantillas de Pandoc (post, page)
├── scripts/              # Generadores en Python (feed, tags, home, links, 404, chrome)
├── style.css             # Todo el sistema de diseño
├── publish.sh            # El único comando que conecta todo
└── feed.xml              # Feed RSS general del sitio
```

## Flujo de publicación

```bash
# Escribir un post nuevo
mkdir -p posts/mi-post
nano posts/mi-post/mi-post.md

# Publicarlo — regenera el post, el feed, las páginas de tags, la home, los links, y el 404
./publish.sh posts/mi-post/mi-post.md

# Subirlo
git add .
git commit -m "Nuevo post: Mi Post"
git push origin master
git push gitlab master
```

El front matter es intencionalmente mínimo:

```yaml
---
title: Mi Post
type: Article
date: 2026-01-01
tags:
  - topic/art
  - subtopic/blender
portfolio: true
---
```

- `type` es una etiqueta libre — se usa para mostrar y agrupar, no para elegir plantilla.
- `tags` sigue la convención `topic/` / `subtopic/`: los topics tienen su propio feed RSS en `/tags/<nombre>/feed.xml`; los subtopics son solo para filtrar.
- `portfolio: true` agrega el post a la grilla de la home automáticamente.
- Los posts sin `date` quedan afuera de los feeds RSS (para no romper el orden cronológico con una fecha inventada), pero igual aparecen en `/posts/`.

## ¿Querés armar tu propio sitio con esto?

Este repo está pensado para bifurcarse (fork). Todo el contenido personal vive en un puñado de archivos bien separados (`site.config`, `content/`, `posts/`, `about/`) — ver **[TEMPLATE-README.es.md](TEMPLATE-README.es.md)** para la guía completa de instalación.

## Licencia

El código (el "motor": `publish.sh`, `scripts/`, `templates/`, `style.css`) está disponible para reutilizar — ver [TEMPLATE-README.es.md](TEMPLATE-README.es.md) para cómo bifurcarlo.

El contenido (posts, imágenes, video, textos bajo `posts/`, `about/`, `content/`) es © Andy Cuccaro, todos los derechos reservados, salvo que un post puntual diga lo contrario.
