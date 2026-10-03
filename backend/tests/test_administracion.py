from fastapi.testclient import TestClient

from backend.app.main import app


def _report(b, publication_id):
    return b["client"].post("/administracion/reportes", json={"publicacion_id": publication_id, "motivo": "Contenido engañoso para revisar"})


def test_reporte_real_y_ocultacion_por_moderador(cuentas, cuenta_factory, payload_publicacion, monkeypatch):
    a, b = cuentas
    moderator = cuenta_factory("Moderador")
    monkeypatch.setenv("CAMPUSMARKET_ADMIN_USER_IDS", str(moderator["usuario"]["id"]))
    publication = a["client"].post("/publicaciones", json=payload_publicacion).json()
    assert _report(a, publication["id"]).status_code == 400
    response = _report(b, publication["id"])
    assert response.status_code == 201
    report = response.json()
    assert _report(b, publication["id"]).status_code == 409
    assert b["client"].get("/administracion/reportes").status_code == 403
    assert TestClient(app).get("/administracion/reportes").status_code == 401
    pending = moderator["client"].get("/administracion/reportes")
    assert pending.status_code == 200
    assert pending.json()[0]["titulo_publicacion"] == publication["titulo"]
    body = {"decision": "ocultado", "nota": "Contenido revisado y retirado"}
    assert b["client"].patch(f"/administracion/reportes/{report['id']}", json=body).status_code == 403
    resolved = moderator["client"].patch(f"/administracion/reportes/{report['id']}", json=body)
    assert resolved.status_code == 200
    assert resolved.json()["resuelto_por"] == moderator["usuario"]["id"]
    assert b["client"].get(f"/catalogo/{publication['id']}").status_code == 404
    assert b["client"].get("/publicaciones").json() == []
    assert a["client"].get("/publicaciones/mias").json()[0]["visible"] is False
    assert moderator["client"].get("/administracion/reportes").json() == []
    assert moderator["client"].patch(f"/administracion/reportes/{report['id']}", json=body).status_code == 409


def test_descartar_reporte_no_oculta_y_no_da_propiedad(cuentas, cuenta_factory, payload_publicacion, monkeypatch):
    a, b = cuentas
    moderator = cuenta_factory("Moderador")
    monkeypatch.setenv("CAMPUSMARKET_ADMIN_USER_IDS", str(moderator["usuario"]["id"]))
    publication = a["client"].post("/publicaciones", json=payload_publicacion).json()
    report = _report(b, publication["id"]).json()
    response = moderator["client"].patch(f"/administracion/reportes/{report['id']}", json={"decision": "descartado", "nota": "No se encuentra infracción"})
    assert response.status_code == 200
    assert a["client"].get(f"/catalogo/{publication['id']}").status_code == 200
    assert moderator["client"].delete(f"/publicaciones/{publication['id']}").status_code == 404


def test_registro_y_perfil_no_autorizan_moderacion(cuentas):
    a, _ = cuentas
    assert a["client"].patch("/usuarios/me", json={"nombre": "Administrador", "es_admin": True}).status_code == 422
    assert a["client"].get("/usuarios/me").json()["es_admin"] is False
    assert a["client"].get("/administracion/reportes").status_code == 403
