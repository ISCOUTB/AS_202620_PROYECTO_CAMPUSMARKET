from .repository import create_publication, list_publications


def crear_publicacion(data: dict) -> dict:
    normalized = {
        "titulo": data["titulo"].strip(),
        "descripcion": data["descripcion"].strip(),
        "precio": float(data["precio"]),
        "modalidad": data["modalidad"],
        "estado": data["estado"],
    }
    return create_publication(normalized)


def listar_publicaciones() -> list[dict]:
    return list_publications()
