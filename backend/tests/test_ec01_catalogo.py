from time import perf_counter

from fastapi.testclient import TestClient

from backend.app.main import app
import backend.app.catalogo.service as catalogo_service


client = TestClient(app)


PUBLICACIONES_EC01 = [
    {
        "id": indice,
        "titulo": f"Producto universitario {indice}",
        "descripcion": (
            f"Publicación de prueba número {indice} "
            "para validar rendimiento del catálogo."
        ),
        "precio": float(10000 + indice),
        "modalidad": "venta" if indice % 2 == 0 else "alquiler",
        "estado": (
            "nuevo"
            if indice % 3 == 0
            else "usado"
            if indice % 3 == 1
            else "reacondicionado"
        ),
    }
    for indice in range(1, 1001)
]


def test_ec01_consulta_catalogo_1000_publicaciones(monkeypatch):
    monkeypatch.setattr(
        catalogo_service,
        "listar_publicaciones",
        lambda: PUBLICACIONES_EC01,
    )

    tiempos = []

    for ejecucion in range(1, 11):
        inicio = perf_counter()

        response = client.get(
            "/catalogo",
            params={"q": "producto"},
        )

        duracion = perf_counter() - inicio
        tiempos.append(duracion)

        assert response.status_code == 200
        assert len(response.json()) == 1000

        print(
            f"EC01 ejecución {ejecucion}: "
            f"{duracion:.6f} s"
        )

    dentro_umbral = sum(
        tiempo <= 2.0
        for tiempo in tiempos
    )

    print(
        f"EC01 resultado: {dentro_umbral}/10 "
        "ejecuciones <= 2.0 s"
    )

    print(
        f"EC01 promedio: "
        f"{sum(tiempos) / len(tiempos):.6f} s"
    )

    print(
        f"EC01 máximo: "
        f"{max(tiempos):.6f} s"
    )

    assert dentro_umbral >= 9
