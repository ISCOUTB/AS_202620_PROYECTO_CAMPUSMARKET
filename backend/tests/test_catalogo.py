from fastapi.testclient import TestClient

import backend.app.catalogo.service as catalogo_service
from backend.app.db import transaction
from backend.app.main import app
from backend.app.publicaciones import repository as publicaciones_repository

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
    monkeypatch.setattr(
        catalogo_service,
        "listar_imagenes_publicaciones",
        lambda ids: {publicacion_id: IMAGENES_PRUEBA.get(publicacion_id, []) for publicacion_id in ids},
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


def test_catalogo_expone_disponibilidad_y_propietario_real(cuentas, payload_publicacion):
    a, b = cuentas
    creada = a["client"].post("/publicaciones", json=payload_publicacion).json()
    a["client"].patch(
        f"/publicaciones/{creada['id']}/estado",
        json={"estado_publicacion": "reservado"},
    )
    detalle = b["client"].get(f"/catalogo/{creada['id']}").json()
    assert detalle["propietario_id"] == a["usuario"]["id"]
    assert detalle["propietario_id"] != b["usuario"]["id"]
    assert detalle["estado_publicacion"] == "reservado"


def test_catalogo_rechaza_filtros_no_finitos():
    for value in ["inf", "nan", "-inf"]:
        assert client.get("/catalogo", params={"precio_min": value}).status_code == 422


def test_catalogo_real_no_repite_conexiones_por_publicacion(cuentas, payload_publicacion, imagen_png, monkeypatch):
    a, b = cuentas
    first = a["client"].post("/publicaciones", json={**payload_publicacion, "titulo": "Rendimiento con fotos"}).json()
    second = b["client"].post("/publicaciones", json={**payload_publicacion, "titulo": "Rendimiento de otra cuenta"}).json()
    first_image = a["client"].post(
        f"/publicaciones/{first['id']}/imagenes", files={"archivo": ("primera.png", imagen_png, "image/png")},
    ).json()
    other_image = b["client"].post(
        f"/publicaciones/{second['id']}/imagenes", files={"archivo": ("otra.png", imagen_png, "image/png")},
    ).json()
    with transaction() as cursor:
        cursor.executemany(
            "INSERT INTO publicaciones (titulo, descripcion, precio, modalidad, estado, propietario_id) VALUES (%s, 'Fixture MySQL real', 1000, 'venta', 'usado', %s)",
            [(f"Rendimiento {index}", a["usuario"]["id"]) for index in range(50)],
        )
        cursor.execute("INSERT INTO publicaciones (titulo, descripcion, precio, modalidad, estado, propietario_id, visible) VALUES ('Rendimiento oculta', 'Oculta', 1000, 'venta', 'usado', %s, FALSE)", (a["usuario"]["id"],))
        cursor.execute("INSERT INTO publicaciones (titulo, descripcion, precio, modalidad, estado, propietario_id) VALUES ('Rendimiento heredada', 'Sin identidad', 1000, 'venta', 'usado', NULL)")

    real_connect = publicaciones_repository._connect
    connections = []

    def counted_connect():
        connections.append(1)
        return real_connect()

    monkeypatch.setattr(publicaciones_repository, "_connect", counted_connect)
    response = a["client"].get("/catalogo", params={"q": "Rendimiento", "modalidad": "venta", "estado": "usado"})
    assert response.status_code == 200
    rows = response.json()
    assert len(rows) == 52
    assert len(connections) <= 4, "El catálogo repite inicialización/conexión por publicación."
    by_id = {row["id"]: row for row in rows}
    assert by_id[first["id"]]["imagenes"][0]["id"] == first_image["id"]
    assert by_id[second["id"]]["imagenes"][0]["id"] == other_image["id"]
    assert by_id[first["id"]]["propietario_id"] == a["usuario"]["id"]
    assert by_id[second["id"]]["propietario_id"] == b["usuario"]["id"]
    assert len([row for row in rows if row["imagenes"] == []]) == 50
    assert not any(row["titulo"] in {"Rendimiento oculta", "Rendimiento heredada"} for row in rows)
    assert a["client"].get(first_image["imagen_url"]).status_code == 200
    assert b["client"].get(other_image["imagen_url"]).status_code == 200
