"""
Parsers compartidos de "registros" estilo front matter (key: value, con
listas indentadas con '-'), y de archivos con múltiples bloques separados
por '---' en su propia línea (usado por content/links.txt).
"""


def parse_kv_block(text):
    """Parsea un bloque 'key: value' (con listas indentadas) a un dict."""
    meta = {}
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if ":" in line and not line.strip().startswith("-"):
            key, _, value = line.partition(":")
            key, value = key.strip(), value.strip()
            if value == "":
                items = []
                j = i + 1
                while j < len(lines) and lines[j].strip().startswith("-"):
                    items.append(lines[j].strip()[1:].strip())
                    j += 1
                if items:
                    meta[key] = items
                    i = j
                    continue
            meta[key] = value
        i += 1
    return meta


def parse_front_matter(path):
    """Parsea el front matter (entre --- ... ---) de un archivo .md."""
    import re
    with open(path, encoding="utf-8") as f:
        content = f.read()
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return None
    return parse_kv_block(match.group(1))


def parse_records(path):
    """
    Parsea un archivo de N bloques 'key: value', separados entre sí por
    una línea con exactamente '---'. Usado por content/links.txt.
    """
    import re
    with open(path, encoding="utf-8") as f:
        content = f.read()
    blocks = re.split(r"(?m)^---$", content)
    return [parse_kv_block(b) for b in blocks if b.strip()]
