from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.resource_limits import MAX_JSON_BODY, MAX_MULTIPART_BODY


def test_body_json_excesivo_se_rechaza_antes_de_autenticacion_y_db():
    with TestClient(app) as client:
        response = client.post("/usuarios/login", content=b"x" * (MAX_JSON_BODY + 1), headers={"Content-Type": "application/json"})
    assert response.status_code == 413
    assert response.json() == {"detail": "La solicitud supera el límite permitido."}


def test_multipart_excesivo_se_rechaza_antes_del_parser():
    with TestClient(app) as client:
        response = client.post(
            "/publicaciones/1/imagenes", content=b"x" * (MAX_MULTIPART_BODY + 1),
            headers={"Content-Type": "multipart/form-data; boundary=prueba"},
        )
    assert response.status_code == 413


def test_body_sin_content_length_se_acota_por_bytes_recibidos():
    def chunks():
        yield b'{"correo":"'
        yield b"x" * MAX_JSON_BODY
        yield b'"}'
    with TestClient(app) as client:
        response = client.post("/usuarios/login", content=chunks(), headers={"Content-Type": "application/json"})
    assert "content-length" not in response.request.headers
    assert response.status_code == 413


def test_respuestas_privadas_no_se_almacenan(cuentas):
    a, b = cuentas
    for account in (a, b):
        response = account["client"].get("/usuarios/me")
        assert response.headers["Cache-Control"] == "no-store"
        assert response.json()["id"] == account["usuario"]["id"]
        assert account["client"].get("/publicaciones/mias").headers["Cache-Control"] == "no-store"
