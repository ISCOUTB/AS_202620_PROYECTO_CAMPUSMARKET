from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.publicaciones.repository import (
    _connect,
    initialize_database,
)


client = TestClient(app)


def _limpiar_publicaciones():
    initialize_database()
    connection = _connect()

    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM publicaciones")
        connection.commit()
    finally:
        connection.close()


def _crear_publicacion(propietario_id: int, titulo: str):
    response = client.post(
        "/publicaciones",
        json={
            "titulo": titulo,
            "descripcion": "Publicación para verificar gestión del propietario",
            "precio": 90000,
            "modalidad": "venta",
            "estado": "usado",
            "propietario_id": propietario_id,
        },
    )
    assert response.status_code == 201
    return response.json()


def test_mis_publicaciones_solo_lista_las_del_propietario():
    _limpiar_publicaciones()

    propia = _crear_publicacion(1, "Libro propio")
    _crear_publicacion(2, "Libro de otro usuario")

    response = client.get("/publicaciones/mias?propietario_id=1")

    assert response.status_code == 200
    publicaciones = response.json()
    assert len(publicaciones) == 1
    assert publicaciones[0]["id"] == propia["id"]
    assert publicaciones[0]["propietario_id"] == 1
    assert publicaciones[0]["estado_publicacion"] == "disponible"


def test_propietario_edita_su_publicacion():
    _limpiar_publicaciones()
    creada = _crear_publicacion(1, "Calculadora usada")

    response = client.put(
        f"/publicaciones/{creada['id']}?propietario_id=1",
        json={
            "titulo": "Calculadora científica",
            "descripcion": "Actualizada por su propietario",
            "precio": 120000,
            "modalidad": "venta",
            "estado": "reacondicionado",
        },
    )

    assert response.status_code == 200
    actualizada = response.json()
    assert actualizada["titulo"] == "Calculadora científica"
    assert actualizada["estado"] == "reacondicionado"
    assert actualizada["propietario_id"] == 1


def test_otro_propietario_no_puede_editar_publicacion():
    _limpiar_publicaciones()
    creada = _crear_publicacion(1, "Producto protegido")

    response = client.put(
        f"/publicaciones/{creada['id']}?propietario_id=2",
        json={
            "titulo": "Intento ajeno",
            "descripcion": "No debe poder modificar esta publicación",
            "precio": 100000,
            "modalidad": "venta",
            "estado": "usado",
        },
    )

    assert response.status_code == 404


def test_propietario_cambia_estado_operativo_sin_alterar_condicion():
    _limpiar_publicaciones()
    creada = _crear_publicacion(1, "Tablet usada")

    response = client.patch(
        f"/publicaciones/{creada['id']}/estado?propietario_id=1",
        json={"estado_publicacion": "reservado"},
    )

    assert response.status_code == 200
    actualizada = response.json()
    assert actualizada["estado"] == "usado"
    assert actualizada["estado_publicacion"] == "reservado"


def test_propietario_elimina_su_publicacion():
    _limpiar_publicaciones()
    creada = _crear_publicacion(1, "Producto a eliminar")

    response = client.delete(
        f"/publicaciones/{creada['id']}?propietario_id=1"
    )

    assert response.status_code == 204

    listado = client.get("/publicaciones/mias?propietario_id=1")
    assert listado.status_code == 200
    assert listado.json() == []
