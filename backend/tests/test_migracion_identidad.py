from concurrent.futures import ThreadPoolExecutor, TimeoutError
from threading import Event

import pytest

from backend.app.db import connect, transaction
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


def test_inicializadores_concurrentes_preservan_propietario_real(db_limpia, cuenta_factory):
    user = cuenta_factory()
    holder = connect()
    started = Event()

    def initialize_worker():
        started.set()
        initialize_database()

    with ThreadPoolExecutor(max_workers=1) as pool:
        try:
            with holder.cursor() as cursor:
                cursor.execute("SELECT GET_LOCK(CONCAT('cm:pub:', LEFT(SHA2(DATABASE(), 256), 40)), 5) AS acquired")
                assert cursor.fetchone()["acquired"] == 1
                cursor.execute("ALTER TABLE publicaciones MODIFY propietario_id BIGINT UNSIGNED NULL DEFAULT 1")
                cursor.execute("INSERT INTO publicaciones (titulo, descripcion, precio, modalidad, estado) VALUES ('Heredada concurrente', 'Anterior a sesiones reales', 1000, 'venta', 'usado')")
                legacy_id = cursor.lastrowid
                holder.commit()
                future = pool.submit(initialize_worker)
                assert started.wait(2)
                with pytest.raises(TimeoutError):
                    future.result(timeout=0.5)
                # El primer inicializador termina la migración mientras conserva su lock.
                cursor.execute("UPDATE publicaciones SET propietario_id = NULL")
                holder.commit()
                cursor.execute("ALTER TABLE publicaciones MODIFY propietario_id BIGINT UNSIGNED NULL")
                cursor.execute(
                    "INSERT INTO publicaciones (titulo, descripcion, precio, modalidad, estado, propietario_id) VALUES ('Autenticada', 'Creada con identidad real', 2000, 'venta', 'usado', %s)",
                    (user["usuario"]["id"],),
                )
                owned_id = cursor.lastrowid
                holder.commit()
        finally:
            holder.close()
        future.result(timeout=6)
    with transaction() as cursor:
        cursor.execute("SELECT propietario_id FROM publicaciones WHERE id = %s", (owned_id,))
        assert cursor.fetchone()["propietario_id"] == user["usuario"]["id"]
        cursor.execute("SELECT propietario_id FROM publicaciones WHERE id = %s", (legacy_id,))
        assert cursor.fetchone()["propietario_id"] is None
