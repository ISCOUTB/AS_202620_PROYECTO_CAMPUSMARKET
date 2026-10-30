from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from backend.app.web_frontend import mount_web_frontend


@pytest.fixture
def web_dir(tmp_path):
    directory = tmp_path / "web"
    directory.mkdir()
    (directory / "index.html").write_text('<base href="/app/">fixture de transporte', encoding="utf-8")
    (directory / "flutter_bootstrap.js").write_text("/* fixture */", encoding="utf-8")
    (directory / "main.dart.js").write_text("/* fixture */", encoding="utf-8")
    return directory


def test_missing_build_does_not_replace_api(tmp_path):
    app = FastAPI()
    assert mount_web_frontend(app, tmp_path) is False
    assert TestClient(app).get("/app/").status_code == 404


def test_partial_build_fails_explicitly(web_dir):
    (web_dir / "main.dart.js").unlink()
    with pytest.raises(RuntimeError, match="Build Flutter incompleto"):
        mount_web_frontend(FastAPI(), web_dir)


def test_mount_preserves_root_contracts_and_docs(web_dir):
    app = FastAPI()
    app.add_api_route("/health", lambda: JSONResponse({"status": "ok"}))
    app.add_api_route("/catalogo", lambda: JSONResponse([]))
    schema = app.openapi()
    assert mount_web_frontend(app, web_dir) is True
    client = TestClient(app)
    assert client.get("/").status_code == 404
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/catalogo").json() == []
    assert client.get("/docs").status_code == 200
    assert client.get("/openapi.json").json() == schema
    assert client.get("/app/").status_code == 200
    assert 'base href="/app/"' in client.get("/app/").text


def test_redirect_keeps_https_without_trusting_proxy_headers(web_dir):
    app = FastAPI()
    mount_web_frontend(app, web_dir)
    client = TestClient(app, base_url="https://campusmarket.iscoutb.dev")
    response = client.get("/app", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["Location"] == "/app/"


def test_missing_assets_never_return_html_and_cache_revalidates(web_dir):
    app = FastAPI()
    mount_web_frontend(app, web_dir)
    client = TestClient(app)
    assert client.get("/app/missing.js").status_code == 404
    response = client.get("/app/main.dart.js")
    assert "javascript" in response.headers["Content-Type"]
    assert response.headers["Cache-Control"] == "no-cache"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert client.get("/app/main.dart.js", headers={"If-None-Match": response.headers["ETag"]}).status_code == 304


def test_mount_does_not_follow_symlinks_or_escape_directory(web_dir):
    private = Path(web_dir.parent) / "private.txt"
    private.write_text("synthetic private fixture", encoding="utf-8")
    (web_dir / "escape.txt").symlink_to(private)
    app = FastAPI()
    mount_web_frontend(app, web_dir)
    client = TestClient(app)
    for path in ("/app/escape.txt", "/app/%2e%2e/private.txt"):
        assert client.get(path).status_code == 404
