from .image_storage import delete_publication_image
from .repository import (
    PersistenceUnavailableError,
    create_publication,
    create_publication_image,
    delete_publication,
    get_publication,
    list_publication_images,
    list_publications,
    list_publications_by_owner,
    publication_exists,
    update_publication,
    update_publication_status,
)


class PublicationPersistenceUnavailableError(RuntimeError):
    """No es posible guardar o consultar publicaciones temporalmente."""


class PublicationNotFoundError(LookupError):
    """La publicación no existe o no pertenece al propietario indicado."""


def _normalizar_publicacion(data: dict) -> dict:
    return {
        "titulo": data["titulo"].strip(),
        "descripcion": data["descripcion"].strip(),
        "precio": float(data["precio"]),
        "modalidad": data["modalidad"],
        "estado": data["estado"],
    }


def crear_publicacion(data: dict) -> dict:
    normalized = {
        **_normalizar_publicacion(data),
        "propietario_id": int(data.get("propietario_id", 1)),
        "estado_publicacion": data.get(
            "estado_publicacion",
            "disponible",
        ),
    }

    try:
        return create_publication(normalized)
    except PersistenceUnavailableError as error:
        raise PublicationPersistenceUnavailableError(
            "No es posible guardar la publicación temporalmente."
        ) from error


def listar_publicaciones() -> list[dict]:
    try:
        return list_publications()
    except PersistenceUnavailableError as error:
        raise PublicationPersistenceUnavailableError(
            "No es posible consultar las publicaciones temporalmente."
        ) from error


def listar_publicaciones_propietario(
    propietario_id: int,
) -> list[dict]:
    try:
        publicaciones = list_publications_by_owner(propietario_id)
        return [
            {
                **publicacion,
                "imagenes": list_publication_images(publicacion["id"]),
            }
            for publicacion in publicaciones
        ]
    except PersistenceUnavailableError as error:
        raise PublicationPersistenceUnavailableError(
            "No es posible consultar las publicaciones temporalmente."
        ) from error


def obtener_publicacion(publicacion_id: int) -> dict | None:
    try:
        return get_publication(publicacion_id)
    except PersistenceUnavailableError as error:
        raise PublicationPersistenceUnavailableError(
            "No es posible consultar la publicación temporalmente."
        ) from error


def editar_publicacion(
    publicacion_id: int,
    propietario_id: int,
    data: dict,
) -> dict:
    try:
        updated = update_publication(
            publicacion_id,
            propietario_id,
            _normalizar_publicacion(data),
        )
        if updated is None:
            raise PublicationNotFoundError(
                "La publicación no existe o no pertenece al propietario."
            )
        return updated
    except PersistenceUnavailableError as error:
        raise PublicationPersistenceUnavailableError(
            "No es posible editar la publicación temporalmente."
        ) from error


def cambiar_estado_publicacion(
    publicacion_id: int,
    propietario_id: int,
    estado_publicacion: str,
) -> dict:
    try:
        updated = update_publication_status(
            publicacion_id,
            propietario_id,
            estado_publicacion,
        )
        if updated is None:
            raise PublicationNotFoundError(
                "La publicación no existe o no pertenece al propietario."
            )
        return updated
    except PersistenceUnavailableError as error:
        raise PublicationPersistenceUnavailableError(
            "No es posible cambiar el estado temporalmente."
        ) from error


def eliminar_publicacion(
    publicacion_id: int,
    propietario_id: int,
) -> None:
    try:
        imagenes = list_publication_images(publicacion_id)
        deleted = delete_publication(publicacion_id, propietario_id)
        if not deleted:
            raise PublicationNotFoundError(
                "La publicación no existe o no pertenece al propietario."
            )

        for imagen in imagenes:
            delete_publication_image(imagen["imagen_url"])
    except PersistenceUnavailableError as error:
        raise PublicationPersistenceUnavailableError(
            "No es posible eliminar la publicación temporalmente."
        ) from error


def listar_imagenes_publicacion(
    publicacion_id: int,
) -> list[dict]:
    try:
        return list_publication_images(publicacion_id)
    except PersistenceUnavailableError as error:
        raise PublicationPersistenceUnavailableError(
            "No es posible consultar las imágenes "
            "de la publicación temporalmente."
        ) from error


def existe_publicacion(publicacion_id: int) -> bool:
    try:
        return publication_exists(publicacion_id)
    except PersistenceUnavailableError as error:
        raise PublicationPersistenceUnavailableError(
            "No es posible consultar la publicación temporalmente."
        ) from error


def registrar_imagen_publicacion(
    publicacion_id: int,
    imagen_url: str,
) -> dict:
    try:
        return create_publication_image(publicacion_id, imagen_url)
    except PersistenceUnavailableError as error:
        raise PublicationPersistenceUnavailableError(
            "No es posible registrar la imagen temporalmente."
        ) from error
