from fastapi.testclient import TestClient

from backend.app.main import app


def test_mis_publicaciones_solo_lista_las_del_propietario(cuentas, payload_publicacion):
    a, b = cuentas
    propia = a["client"].post("/publicaciones", json=payload_publicacion).json()
    b["client"].post("/publicaciones", json={**payload_publicacion, "titulo": "Libro de B"})
    response = a["client"].get("/publicaciones/mias")
    assert response.status_code == 200
    assert response.json() == [{**propia, "imagenes": []}]


def test_mis_publicaciones_incluye_imagen_principal(cuentas, payload_publicacion):
    a, _ = cuentas
    propia = a["client"].post("/publicaciones", json=payload_publicacion).json()
    upload = a["client"].post(f"/publicaciones/{propia['id']}/imagenes", files={"archivo": ("foto.jpg", b"contenido-imagen-prueba", "image/jpeg")})
    assert upload.status_code == 201
    images = a["client"].get("/publicaciones/mias").json()[0]["imagenes"]
    assert len(images) == 1
    assert images[0]["es_principal"] is True
    assert images[0]["orden"] == 1
    assert a["client"].delete(f"/publicaciones/{propia['id']}").status_code == 204


def test_propietario_edita_su_publicacion_y_put_identico_es_idempotente(cuentas, payload_publicacion):
    a, _ = cuentas
    creada = a["client"].post("/publicaciones", json=payload_publicacion).json()
    edited = {**payload_publicacion, "titulo": "Calculadora reacondicionada", "estado": "reacondicionado"}
    for _ in range(2):
        response = a["client"].put(f"/publicaciones/{creada['id']}", json=edited)
        assert response.status_code == 200
        assert response.json()["titulo"] == edited["titulo"]
        assert response.json()["propietario_id"] == a["usuario"]["id"]


def test_otro_propietario_no_puede_editar_publicacion(cuentas, payload_publicacion):
    a, b = cuentas
    creada = a["client"].post("/publicaciones", json=payload_publicacion).json()
    response = b["client"].put(f"/publicaciones/{creada['id']}", json={**payload_publicacion, "titulo": "Intento ajeno"})
    assert response.status_code == 404


def test_propietario_cambia_estado_sin_alterar_condicion(cuentas, payload_publicacion):
    a, _ = cuentas
    creada = a["client"].post("/publicaciones", json=payload_publicacion).json()
    for _ in range(2):
        response = a["client"].patch(f"/publicaciones/{creada['id']}/estado", json={"estado_publicacion": "reservado"})
        assert response.status_code == 200
        assert response.json()["estado"] == "usado"
        assert response.json()["estado_publicacion"] == "reservado"


def test_propietario_elimina_su_publicacion(cuentas, payload_publicacion):
    a, _ = cuentas
    creada = a["client"].post("/publicaciones", json=payload_publicacion).json()
    assert a["client"].delete(f"/publicaciones/{creada['id']}").status_code == 204
    assert a["client"].get("/publicaciones/mias").json() == []
    assert TestClient(app).get(f"/catalogo/{creada['id']}").status_code == 404
