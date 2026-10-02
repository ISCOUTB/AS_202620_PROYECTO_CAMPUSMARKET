from fastapi.testclient import TestClient

import backend.app.catalogo.service as catalogo_service
from backend.app.main import app

client = TestClient(app)


PUBLICACIONES_PRUEBA = [
    {
        "id": 1,
        "titulo": "Calculadora científica",
        "descripcion": "Calculadora para cursos de ingeniería",
        "precio": 120000.0,
        "modalidad": "venta",
        "estado": "usado",
    },
    {
        "id": 2,
        "titulo": "Libro de arquitectura de software",
        "descripcion": "Libro en excelente estado",
        "precio": 80000.0,
        "modalidad": "venta",
        "estado": "nuevo",
    },
    {
        "id": 3,
        "titulo": "Portátil para alquiler",
        "descripcion": "Equipo para trabajos universitarios",
        "precio": 50000.0,
        "modalidad": "alquiler",
        "estado": "reacondicionado",
    },
]


IMAGENES_PRUEBA = {
    1: [],
    2: [
        {
            "id": 21,
            "publicacion_id": 2,
            "imagen_url": "/uploads/publicaciones/2/libro.webp",
            "orden": 1,
            "es_principal": True,
        }
    ],
    3: [],
}


def _simular_publicaciones(monkeypatch):
    monkeypatch.setattr(
        catalogo_service,
        "listar_publicaciones",
        lambda: PUBLICACIONES_PRUEBA,
    )
    monkeypatch.setattr(
        catalogo_service,
        "listar_imagenes_publicacion",
        lambda publicacion_id: IMAGENES_PRUEBA.get(publicacion_id, []),
    )


def test_catalogo_lista_publicaciones(monkeypatch):
    _simular_publicaciones(monkeypatch)

    response = client.get("/catalogo")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_catalogo_incluye_imagenes_de_publicacion(monkeypatch):
    _simular_publicaciones(monkeypatch)

    response = client.get("/catalogo/2")

    assert response.status_code == 200

    resultado = response.json()

    assert len(resultado["imagenes"]) == 1
    assert resultado["imagenes"][0]["imagen_url"] == (
        "/uploads/publicaciones/2/libro.webp"
    )
    assert resultado["imagenes"][0]["es_principal"] is True


def test_catalogo_busca_por_texto(monkeypatch):
    _simular_publicaciones(monkeypatch)

    response = client.get(
        "/catalogo",
        params={"q": "arquitectura"},
    )

    assert response.status_code == 200

    resultado = response.json()

    assert len(resultado) == 1
    assert resultado[0]["id"] == 2


def test_catalogo_filtra_por_modalidad(monkeypatch):
    _simular_publicaciones(monkeypatch)

    response = client.get(
        "/catalogo",
        params={"modalidad": "alquiler"},
    )

    assert response.status_code == 200

    resultado = response.json()

    assert len(resultado) == 1
    assert resultado[0]["id"] == 3


def test_catalogo_filtra_por_estado(monkeypatch):
    _simular_publicaciones(monkeypatch)

    response = client.get(
        "/catalogo",
        params={"estado": "nuevo"},
    )

    assert response.status_code == 200

    resultado = response.json()

    assert len(resultado) == 1
    assert resultado[0]["id"] == 2


def test_catalogo_filtra_por_rango_precio(monkeypatch):
    _simular_publicaciones(monkeypatch)

    response = client.get(
        "/catalogo",
        params={
            "precio_min": 70000,
            "precio_max": 100000,
        },
    )

    assert response.status_code == 200

    resultado = response.json()

    assert len(resultado) == 1
    assert resultado[0]["id"] == 2


def test_catalogo_rechaza_rango_precio_invalido(monkeypatch):
    _simular_publicaciones(monkeypatch)

    response = client.get(
        "/catalogo",
        params={
            "precio_min": 500000,
            "precio_max": 100000,
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"] == (
        "precio_min no puede ser mayor que precio_max"
    )


def test_catalogo_consulta_detalle(monkeypatch):
    _simular_publicaciones(monkeypatch)

    response = client.get("/catalogo/2")

    assert response.status_code == 200
    assert response.json()["titulo"] == (
        "Libro de arquitectura de software"
    )


def test_catalogo_detalle_inexistente(monkeypatch):
    _simular_publicaciones(monkeypatch)

    response = client.get("/catalogo/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Publicación no encontrada"
