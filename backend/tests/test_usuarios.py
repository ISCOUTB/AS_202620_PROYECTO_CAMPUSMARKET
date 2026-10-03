import secrets
from uuid import uuid4

from fastapi.testclient import TestClient

from backend.app.db import transaction
from backend.app.main import app
from backend.app.usuarios.security import verify_password


def test_registro_login_perfil_logout_revoca_token(cuenta_factory):
    cuenta = cuenta_factory()
    client = cuenta["client"]
    assert client.get("/usuarios/me").json() == cuenta["usuario"]
    response = client.patch("/usuarios/me", json={"nombre": "  Nilver García  "})
    assert response.status_code == 200
    assert response.json()["nombre"] == "Nilver García"
    assert response.json()["correo"] == cuenta["correo"]
    assert client.post("/usuarios/logout").status_code == 204
    assert client.get("/usuarios/me").status_code == 401


def test_password_y_token_solo_se_persisten_como_hash(cuenta_factory):
    cuenta = cuenta_factory()
    with transaction() as cursor:
        cursor.execute("SELECT password_hash FROM usuarios WHERE id = %s", (cuenta["usuario"]["id"],))
        encoded = cursor.fetchone()["password_hash"]
        assert encoded.startswith("scrypt$131072$8$1$")
        assert cuenta["password"] not in encoded
        assert verify_password(cuenta["password"], encoded)
        cursor.execute("SELECT token_hash FROM sesiones_usuario WHERE usuario_id = %s", (cuenta["usuario"]["id"],))
        digest = cursor.fetchone()["token_hash"]
        assert len(digest) == 64
        assert digest != cuenta["token"]


def test_credenciales_incorrectas_no_crean_sesion(cuenta_factory):
    cuenta = cuenta_factory()
    client = TestClient(app)
    wrong = client.post("/usuarios/login", json={"correo": cuenta["correo"], "password": secrets.token_urlsafe(24)})
    missing = client.post("/usuarios/login", json={"correo": "ausente@campus.test", "password": secrets.token_urlsafe(24)})
    assert wrong.status_code == missing.status_code == 401
    assert wrong.json() == missing.json()
    with transaction() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM sesiones_usuario")
        assert cursor.fetchone()["total"] == 1


def test_registro_normaliza_correo_y_rechaza_duplicado(db_limpia):
    client = TestClient(app)
    payload = {"nombre": "Estudiante", "correo": "ALUMNO@CAMPUS.TEST", "password": secrets.token_urlsafe(24)}
    response = client.post("/usuarios/registro", json=payload)
    assert response.status_code == 201
    assert response.json()["correo"] == "alumno@campus.test"
    payload["correo"] = "alumno@campus.test"
    assert client.post("/usuarios/registro", json=payload).status_code == 409


def test_registro_no_permite_asignar_privilegios_ni_id(db_limpia):
    client = TestClient(app)
    payload = {"nombre": "Estudiante", "correo": f"{uuid4().hex}@campus.test", "password": secrets.token_urlsafe(24), "es_admin": True, "id": 1}
    assert client.post("/usuarios/registro", json=payload).status_code == 422
    payload.pop("es_admin")
    payload.pop("id")
    response = client.post("/usuarios/registro", json=payload)
    assert response.status_code == 201
    assert response.json()["es_admin"] is False


def test_sesion_expirada_y_token_inventado_son_rechazados(cuenta_factory):
    cuenta = cuenta_factory()
    with transaction() as cursor:
        cursor.execute("UPDATE sesiones_usuario SET expira_en = DATE_SUB(UTC_TIMESTAMP(), INTERVAL 1 SECOND)")
    assert cuenta["client"].get("/usuarios/me").status_code == 401
    response = TestClient(app).get("/usuarios/me", headers={"Authorization": "Bearer inventado"})
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_errores_validacion_no_reflejan_password(db_limpia):
    password = "corto"
    response = TestClient(app).post("/usuarios/registro", json={"nombre": "Nombre", "correo": "valido@campus.test", "password": password})
    assert response.status_code == 422
    assert password not in response.text
    assert all("input" not in error for error in response.json()["detail"])


def test_login_limita_intentos_persistentemente(db_limpia):
    client = TestClient(app)
    with transaction() as cursor:
        from backend.app.usuarios.security import token_digest
        key = token_digest("login:correo:agotado@campus.test")
        cursor.execute("INSERT INTO intentos_autenticacion (clave, intentos, reinicia_en) VALUES (%s, 10, DATE_ADD(UTC_TIMESTAMP(), INTERVAL 5 MINUTE))", (key,))
    response = client.post("/usuarios/login", json={"correo": "agotado@campus.test", "password": secrets.token_urlsafe(24)})
    assert response.status_code == 429
    assert response.headers["retry-after"] == "300"


def test_sesion_de_otro_dispositivo_sobrevive_logout(cuenta_factory):
    cuenta = cuenta_factory()
    otro = TestClient(app)
    response = otro.post("/usuarios/login", json={"correo": cuenta["correo"], "password": cuenta["password"]})
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    otro.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    cuenta["client"].post("/usuarios/logout")
    assert otro.get("/usuarios/me").status_code == 200
