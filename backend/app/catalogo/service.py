from backend.app.publicaciones.service import listar_publicaciones


def buscar_publicaciones(
    texto: str | None = None,
    modalidad: str | None = None,
    estado: str | None = None,
    precio_min: float | None = None,
    precio_max: float | None = None,
) -> list[dict]:
    publicaciones = listar_publicaciones()

    texto_normalizado = texto.strip().lower() if texto else None

    resultado = []

    for publicacion in publicaciones:
        if texto_normalizado:
            titulo = str(publicacion.get("titulo", "")).lower()
            descripcion = str(publicacion.get("descripcion", "")).lower()

            if (
                texto_normalizado not in titulo
                and texto_normalizado not in descripcion
            ):
                continue

        if modalidad and publicacion.get("modalidad") != modalidad:
            continue

        if estado and publicacion.get("estado") != estado:
            continue

        precio = float(publicacion.get("precio", 0))

        if precio_min is not None and precio < precio_min:
            continue

        if precio_max is not None and precio > precio_max:
            continue

        resultado.append(publicacion)

    return resultado


def obtener_publicacion(publicacion_id: int) -> dict | None:
    publicaciones = listar_publicaciones()

    for publicacion in publicaciones:
        if int(publicacion["id"]) == publicacion_id:
            return publicacion

    return None
