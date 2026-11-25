"""Valida nombres de tablas de la lista de ejemplo."""

import json
import re
import sys
from pathlib import Path

RULE = re.compile(r"(?:bronze|silver|gold)_[a-z][a-z0-9]*(?:_[a-z0-9]+)*\Z")


def invalid_names(names):
    if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
        raise ValueError("El archivo debe ser una lista de strings.")
    return [name for name in names if not RULE.fullmatch(name)]


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python tools/check_names.py <lista.json>")
    bad = invalid_names(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    for name in bad:
        print(f"NO CUMPLE: {name!r} (prefijo de capa y snake_case)")
    print(f"Total: {len(bad)} nombre(s) no conforme(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
