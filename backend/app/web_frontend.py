"""Sirve el build Flutter opcional sin reemplazar rutas de la API."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles


class FlutterFiles(StaticFiles):
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        # Los nombres de bootstrap/main no cambian entre releases. Revalidarlos
        # evita mezclar builds sin desactivar ETag ni el aislamiento del mount.
        response.headers["Cache-Control"] = "no-cache"
        response.headers["X-Content-Type-Options"] = "nosniff"
        # Uvicorn cuenta conexiones keep-alive dentro del limite existente (6).
        # No retener slots por assets; no altera el keep-alive de las rutas API.
        response.headers["Connection"] = "close"
        return response


def mount_web_frontend(app: FastAPI, directory: Path | None = None) -> bool:
    directory = directory or Path(__file__).resolve().parents[1] / "web"
    if not (directory / "index.html").is_file():
        return False
    required = ("flutter_bootstrap.js", "main.dart.js")
    if not all((directory / name).is_file() for name in required):
        raise RuntimeError("Build Flutter incompleto: faltan archivos compilados")

    def canonical_url():
        # Location relativa conserva HTTPS incluso con --no-proxy-headers.
        return RedirectResponse("/app/", status_code=307)

    app.add_api_route("/app", canonical_url, methods=["GET", "HEAD"], include_in_schema=False)
    app.mount("/app", FlutterFiles(directory=directory, html=True), name="campusmarket-web")
    return True
