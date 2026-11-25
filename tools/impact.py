"""Recorre dependencias descendentes de una muestra local, con evidencia."""

import json
import sys
from collections import deque
from pathlib import Path


def impact(edges, target):
    result = []
    visited = {target}
    queue = deque([(target, [])])
    while queue:
        node, path = queue.popleft()
        for edge in edges:
            if edge["from"] != node:
                continue
            next_path = path + [edge]
            if edge["to"] in visited:
                continue
            visited.add(edge["to"])
            result.append(next_path)
            queue.append((edge["to"], next_path))
    return result


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Uso: python tools/impact.py <grafo.json> <tabla>")
    graph = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    paths = impact(graph["edges"], sys.argv[2])
    print("Ejemplo local: dependencias conocidas, no linaje completo.")
    for path in paths:
        print(" -> ".join([path[0]["from"], *(edge["to"] for edge in path)]))
        for edge in path:
            print(f"  evidencia: {edge['evidence']}")
    if not paths:
        print("Sin rutas en este ejemplo; no implica ausencia de impacto.")


if __name__ == "__main__":
    main()
