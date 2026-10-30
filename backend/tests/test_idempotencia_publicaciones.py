"""Pruebas de regresion del incremento CampusMarket 2.0: Idempotency-Key.
Copiar a backend/tests/test_idempotencia_publicaciones.py antes de ejecutarlas.
Requieren exclusivamente CAMPUSMARKET_DB_NAME terminado en _test.
"""
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

from backend.app.db import transaction


def _post(client, payload, key=None):
    headers = {'Idempotency-Key': key} if key is not None else {}
    return client.post('/publicaciones', json=payload, headers=headers)


def _count(publication_ids):
    with transaction() as cursor:
        placeholders = ','.join(['%s'] * len(publication_ids))
        cursor.execute(f'SELECT COUNT(*) AS total FROM publicaciones WHERE id IN ({placeholders})', tuple(publication_ids))
        return cursor.fetchone()['total']


def test_t1_reintento_serial_no_duplica(cuentas, payload_publicacion):
    client = cuentas[0]['client']
    key = str(uuid4())
    first = _post(client, payload_publicacion, key)
    second = _post(client, payload_publicacion, key)
    assert (first.status_code, second.status_code) == (201, 201)
    assert first.json() == second.json()
    assert _count([first.json()['id']]) == 1
    assert len(client.get('/publicaciones/mias').json()) == 1


def test_t2_reintento_concurrente_no_duplica(cuentas, payload_publicacion):
    client = cuentas[0]['client']
    key = str(uuid4())
    with ThreadPoolExecutor(max_workers=4) as pool:
        responses = list(pool.map(lambda _: _post(client, payload_publicacion, key), range(4)))
    assert [r.status_code for r in responses] == [201] * 4
    assert len({r.json()['id'] for r in responses}) == 1
    assert len(client.get('/publicaciones/mias').json()) == 1


def test_t3_misma_clave_distintos_datos_conflicto(cuentas, payload_publicacion):
    client = cuentas[0]['client']
    key = str(uuid4())
    first = _post(client, payload_publicacion, key)
    changed = {**payload_publicacion, 'titulo': 'Titulo modificado'}
    second = _post(client, changed, key)
    assert first.status_code == 201
    assert second.status_code == 409
    assert len(client.get('/publicaciones/mias').json()) == 1


def test_t4_reintento_tras_respuesta_perdida(cuentas, payload_publicacion):
    client = cuentas[0]['client']
    key = str(uuid4())
    first = _post(client, payload_publicacion, key)
    assert first.status_code == 201
    # El cliente no usa la respuesta, como si se hubiera perdido despues del COMMIT.
    recovered = _post(client, payload_publicacion, key)
    assert recovered.status_code == 201
    assert recovered.json()['id'] == first.json()['id']
    assert len(client.get('/publicaciones/mias').json()) == 1


def test_t5_claves_distintas_crean_dos(cuentas, payload_publicacion):
    client = cuentas[0]['client']
    first = _post(client, payload_publicacion, str(uuid4()))
    second = _post(client, payload_publicacion, str(uuid4()))
    assert first.status_code == second.status_code == 201
    assert first.json()['id'] != second.json()['id']
    assert len(client.get('/publicaciones/mias').json()) == 2


def test_t6_misma_clave_usuarios_distintos(cuentas, payload_publicacion):
    a, b = cuentas
    key = str(uuid4())
    first = _post(a['client'], payload_publicacion, key)
    second = _post(b['client'], payload_publicacion, key)
    assert first.status_code == second.status_code == 201
    assert first.json()['id'] != second.json()['id']
    assert len(a['client'].get('/publicaciones/mias').json()) == 1
    assert len(b['client'].get('/publicaciones/mias').json()) == 1


def test_cliente_anterior_sin_header_sigue_funcionando(cuentas, payload_publicacion):
    client = cuentas[0]['client']
    response = _post(client, payload_publicacion)
    assert response.status_code == 201


def test_clave_corta_es_rechazada(cuentas, payload_publicacion):
    response = _post(cuentas[0]['client'], payload_publicacion, 'abc')
    assert response.status_code == 422
