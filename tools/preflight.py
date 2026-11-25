"""Descubre un workspace y su capacidad; no cambia recursos."""

import argparse
import json
import shutil
import subprocess
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

BASE = "https://api.fabric.microsoft.com"
HEADER = "search-consumption-cli"


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def pages(url, token, opener=None):
    opener = opener or build_opener(NoRedirect)
    seen = set()
    result = []
    for _ in range(1000):
        parsed = urlsplit(url)
        if (parsed.scheme, parsed.netloc) != ("https", "api.fabric.microsoft.com") or not parsed.path.startswith("/v1/"):
            raise ValueError("URL de continuación no autorizada.")
        if url in seen:
            raise ValueError("Paginación circular.")
        seen.add(url)
        request = Request(url, headers={"Authorization": "Bearer " + token,
                                        "x-ms-fabric-skill": HEADER})
        with opener.open(request, timeout=30) as response:
            body = json.load(response)
        page = body["value"]
        if not isinstance(page, list):
            raise ValueError("Formato de página no reconocido.")
        result.extend(page)
        url = body.get("continuationUri")
        if not url:
            if body.get("continuationToken"):
                raise ValueError("Continuación sin URI; inventario incompleto.")
            return result
    raise ValueError("Límite de páginas superado; inventario incompleto.")


def inspect(workspace_name, token, opener=None):
    workspaces = pages(BASE + "/v1/workspaces", token, opener)
    matches = [w for w in workspaces if w.get("displayName") == workspace_name]
    if len(matches) != 1:
        raise ValueError(f"Hay {len(matches)} workspaces visibles con ese nombre exacto; revisa acceso o ambigüedad.")
    ws = matches[0]
    capacities = pages(BASE + "/v1/capacities", token, opener)
    capacity = next((c for c in capacities if c.get("id") == ws.get("capacityId")), None)
    items = pages(BASE + "/v1/workspaces/" + ws["id"] + "/items", token, opener)
    return {"workspace": ws["displayName"], "assigned": bool(ws.get("capacityId")),
            "capacity_state": capacity.get("state") if capacity else None,
            "capacity_sku": capacity.get("sku") if capacity else None,
            "items": [{"name": i.get("displayName"), "type": i.get("type")} for i in items]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", help="Nombre exacto; si se omite se pregunta al inicio.")
    args = parser.parse_args()
    workspace = args.workspace or input("Nombre exacto del workspace de Fabric: ").strip()
    if not workspace:
        raise SystemExit("Falta el nombre del workspace.")
    az = shutil.which("az")
    if not az:
        raise SystemExit("Falta Azure CLI; instala y autentica antes de continuar.")
    try:
        token = subprocess.run([az, "account", "get-access-token", "--resource", BASE,
                                "--query", "accessToken", "-o", "tsv"], capture_output=True,
                               text=True, check=True, timeout=60).stdout.strip()
        if not token:
            raise ValueError("Azure CLI no devolvió un token.")
        print(json.dumps(inspect(workspace, token), ensure_ascii=False, indent=2))
        print("Solo lectura. Los permisos de escritura y el acceso a datos no se han probado.")
    except (subprocess.SubprocessError, HTTPError, URLError, ValueError, KeyError) as error:
        detail = f"HTTP {error.code}" if isinstance(error, HTTPError) else type(error).__name__
        print(f"No se completó el descubrimiento: {detail}. Revisa identidad y permisos.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
