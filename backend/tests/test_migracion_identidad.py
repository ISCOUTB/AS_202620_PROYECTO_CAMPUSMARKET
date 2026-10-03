from backend.app.db import transaction
from backend.app.publicaciones.repository import initialize_database


def test_legacy_se_preserva_sin_asignar_a_primera_cuenta(db_limpia, cuenta_factory):
    with transaction() as cursor:
        cursor.execute("ALTER TABLE publicaciones MODIFY propietario_id BIGINT UNSIGNED NULL DEFAULT 1")
        cursor.execute("INSERT INTO publicaciones (titulo, descripcion, precio, modalidad, estado) VALUES ('Heredada', 'Antes de autenticación', 50000, 'venta', 'usado')")
        legacy_id = cursor.lastrowid
    initialize_database()
    user = cuenta_factory()
    assert user["client"].get("/publicaciones/mias").json() == []
    assert user["client"].get(f"/catalogo/{legacy_id}").status_code == 404
    assert user["client"].delete(f"/publicaciones/{legacy_id}").status_code == 404
    with transaction() as cursor:
        cursor.execute("SELECT titulo, propietario_id FROM publicaciones WHERE id = %s", (legacy_id,))
        legacy = cursor.fetchone()
        assert legacy["titulo"] == "Heredada"
        assert legacy["propietario_id"] is None


def test_inicializacion_repetida_no_desvincula_cuentas_reales(cuentas, payload_publicacion):
    a, _ = cuentas
    created = a["client"].post("/publicaciones", json=payload_publicacion).json()
    initialize_database()
    initialize_database()
    assert a["client"].get("/publicaciones/mias").json()[0]["propietario_id"] == created["propietario_id"]
