"""
Lee site.config (formato KEY="value") y lo expone como diccionario.
Sin dependencias externas — mismo espíritu que el resto del proyecto.
"""
import re


def load_config(path="site.config"):
    config = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            match = re.match(r'^([A-Z_]+)="(.*)"$', line)
            if match:
                config[match.group(1)] = match.group(2)
    return config


CONFIG = load_config()
