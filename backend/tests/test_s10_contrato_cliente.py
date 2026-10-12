"""Regresión S10: el cliente incompatible no alcanza persistencia y puede corregirse."""

import json
from uuid import uuid4

from fastapi.testclient import TestClient

from backend.app import observability
from backend.app.catalogo import router as catalogo_router
from backend.app.main import app
from scripts.experimento_s10_contrato import adapt_sale_filter


def test_cliente_incompatible_es_rechazado_antes_del_servicio(monkeypatch):
    def servicio_prohibido(**kwargs):
        raise AssertionError("Un filtro inválido no debe llegar al servicio ni a MySQL")

    monkeypatch.setattr(catalogo_router, "buscar_publicaciones", servicio_prohibido)
    with TestClient(app) as client:
        response = client.get("/catalogo", params={"modalidad": "sale"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "modalidad"]
    assert response.json()["detail"][0]["type"] == "literal_error"
    assert "input" not in response.json()["detail"][0]


def test_adaptacion_del_consumidor_recupera_lectura_y_logs_correlacionados(monkeypatch):
    registros, llamadas = [], []
    expected = [{"id": 1, "titulo": "Fixture S10", "descripcion": "Solo en memoria",
                 "precio": 10.0, "modalidad": "venta", "estado": "usado"}]

    def servicio(**kwargs):
        llamadas.append(kwargs)
        return expected

    monkeypatch.setattr(catalogo_router, "buscar_publicaciones", servicio)
    monkeypatch.setattr(observability.logger, "info", registros.append)
    ids = [str(uuid4()) for _ in range(3)]
    with TestClient(app) as client:
        before = client.get("/catalogo?modalidad=venta", headers={"X-Request-ID": ids[0]})
        failed = client.get("/catalogo?modalidad=sale", headers={"X-Request-ID": ids[1]})
        after = client.get("/catalogo", params={"modalidad": adapt_sale_filter("sale")},
                           headers={"X-Request-ID": ids[2]})
    assert [before.status_code, failed.status_code, after.status_code] == [200, 422, 200]
    assert before.json() == after.json()
    assert len(llamadas) == 2
    assert all(call["modalidad"] == "venta" for call in llamadas)
    logs = [json.loads(value) for value in registros]
    assert [entry["request_id"] for entry in logs] == ids
    assert [entry["status_code"] for entry in logs] == [200, 422, 200]
    assert all(entry["event"] == "http_request" and entry["path"] == "/catalogo" for entry in logs)
    assert all(entry["duration_ms"] >= 0 for entry in logs)
    assert [response.headers["X-Request-ID"] for response in [before, failed, after]] == ids
