from fastapi.testclient import TestClient

from backend.app.main import app


def test_ec02_diez_intentos_ajenos_no_modifican_datos(cuentas, payload_publicacion):
    a, b = cuentas
    response = a["client"].post("/publicaciones", json=payload_publicacion)
    assert response.status_code == 201
    created = response.json()
    assert created["propietario_id"] == a["usuario"]["id"]
    denied = 0
    for intento in range(10):
        url = f"/publicaciones/{created['id']}?propietario_id={a['usuario']['id']}"
        if intento % 2:
            result = b["client"].delete(url)
        else:
            result = b["client"].put(url, json={**payload_publicacion, "titulo": "Intento de suplantación"})
        assert result.status_code == 404
        denied += 1
        # Verificar respuesta Y datos: un 404 después de escribir tampoco cumple.
        assert a["client"].get("/publicaciones/mias").json() == [{**created, "imagenes": []}]
    assert denied == 10
    assert b["client"].get(f"/publicaciones/mias?propietario_id={a['usuario']['id']}").json() == []
    print("EC-02: 10/10 intentos ajenos rechazados; datos sin cambios; identidad real en MySQL")


def test_sin_sesion_no_se_puede_crear_ni_mutar(cuentas, payload_publicacion):
    a, _ = cuentas
    created = a["client"].post("/publicaciones", json=payload_publicacion).json()
    public = TestClient(app)
    assert public.post("/publicaciones", json=payload_publicacion).status_code == 401
    assert public.get("/publicaciones/mias").status_code == 401
    assert public.put(f"/publicaciones/{created['id']}", json=payload_publicacion).status_code == 401
    assert public.delete(f"/publicaciones/{created['id']}").status_code == 401
    assert public.post(f"/publicaciones/{created['id']}/imagenes", files={"archivo": ("foto.jpg", b"imagen", "image/jpeg")}).status_code == 401


def test_identidad_en_body_se_rechaza_y_cambio_estado_ajeno_no_se_aplica(cuentas, payload_publicacion):
    a, b = cuentas
    spoofed = a["client"].post("/publicaciones", json={**payload_publicacion, "propietario_id": b["usuario"]["id"]})
    assert spoofed.status_code == 422
    created = a["client"].post("/publicaciones", json=payload_publicacion).json()
    assert b["client"].patch(f"/publicaciones/{created['id']}/estado", json={"estado_publicacion": "vendido"}).status_code == 404
    assert a["client"].get("/publicaciones/mias").json()[0]["estado_publicacion"] == "disponible"


def test_otro_usuario_no_sube_imagen_y_propietario_puede_eliminar(cuentas, payload_publicacion):
    a, b = cuentas
    created = a["client"].post("/publicaciones", json=payload_publicacion).json()
    assert b["client"].post(f"/publicaciones/{created['id']}/imagenes", files={"archivo": ("foto.jpg", b"imagen", "image/jpeg")}).status_code == 404
    assert a["client"].get("/publicaciones/mias").json()[0]["imagenes"] == []
    assert a["client"].delete(f"/publicaciones/{created['id']}").status_code == 204
    assert b["client"].get(f"/catalogo/{created['id']}").status_code == 404
