from pathlib import Path

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_corte_vertical_crea_y_recupera_publicacion(
    tmp_path: Path,
    monkeypatch,
):
    database = tmp_path / "campusmarket-test.db"
    monkeypatch.setenv("CAMPUSMARKET_DB_PATH", str(database))

    payload = {
        "titulo": "Calculadora científica",
        "descripcion": "Calculadora reacondicionada en buen estado",
        "precio": 65000,
        "modalidad": "venta",
        "estado": "reacondicionado",
    }

    create_response = client.post("/publicaciones", json=payload)

    assert create_response.status_code == 201

    created = create_response.json()

    assert created["id"] > 0
    assert created["titulo"] == payload["titulo"]
    assert created["estado"] == "reacondicionado"
    assert database.exists()

    list_response = client.get("/publicaciones")

    assert list_response.status_code == 200

    publicaciones = list_response.json()

    assert len(publicaciones) == 1
    assert publicaciones[0] == created
    assert publicaciones[0]["estado"] == "reacondicionado"