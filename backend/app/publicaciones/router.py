from typing import Literal

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    Response,
    UploadFile,
    status,
)
from pydantic import BaseModel, Field

from .image_storage import (
    InvalidImageError,
    delete_publication_image,
    save_publication_image,
)
from .service import (
    PublicationNotFoundError,
    PublicationPersistenceUnavailableError,
    cambiar_estado_publicacion,
    crear_publicacion,
    editar_publicacion,
    eliminar_publicacion,
    existe_publicacion,
    listar_imagenes_publicacion,
    listar_publicaciones,
    listar_publicaciones_propietario,
    registrar_imagen_publicacion,
)


router = APIRouter(
    prefix="/publicaciones",
    tags=["publicaciones"],
)


class PublicacionBase(BaseModel):
    titulo: str = Field(min_length=3, max_length=100)
    descripcion: str = Field(min_length=3, max_length=500)
    precio: float = Field(gt=0)
    modalidad: Literal["venta", "alquiler"]
    estado: Literal["nuevo", "usado", "reacondicionado"]


class PublicacionCreate(PublicacionBase):
    propietario_id: int = Field(default=1, gt=0)
    estado_publicacion: Literal[
        "disponible",
        "reservado",
        "vendido",
    ] = "disponible"


class PublicacionUpdate(PublicacionBase):
    pass


class EstadoPublicacionUpdate(BaseModel):
    estado_publicacion: Literal[
        "disponible",
        "reservado",
        "vendido",
    ]


class Publicacion(PublicacionCreate):
    id: int


class PublicacionImagen(BaseModel):
    id: int
    publicacion_id: int
    imagen_url: str
    orden: int
    es_principal: bool


class PublicacionGestion(Publicacion):
    imagenes: list[PublicacionImagen] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    detail: str


def _service_unavailable(error: Exception) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=(
            "La persistencia está temporalmente no disponible. "
            "Intenta nuevamente."
        ),
    )


@router.post(
    "",
    response_model=Publicacion,
    status_code=status.HTTP_201_CREATED,
    operation_id="crearPublicacion",
    summary="Crear una publicación",
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": ErrorResponse,
            "description": "Persistencia temporalmente no disponible",
        }
    },
)
def crear(payload: PublicacionCreate):
    try:
        return crear_publicacion(payload.model_dump())
    except PublicationPersistenceUnavailableError as error:
        raise _service_unavailable(error) from error


@router.get(
    "",
    response_model=list[Publicacion],
    operation_id="listarPublicaciones",
    summary="Listar publicaciones",
)
def listar():
    try:
        return listar_publicaciones()
    except PublicationPersistenceUnavailableError as error:
        raise _service_unavailable(error) from error


@router.get(
    "/mias",
    response_model=list[PublicacionGestion],
    operation_id="listarMisPublicaciones",
    summary="Listar publicaciones de un propietario",
)
def listar_mias(propietario_id: int = 1):
    try:
        return listar_publicaciones_propietario(propietario_id)
    except PublicationPersistenceUnavailableError as error:
        raise _service_unavailable(error) from error


@router.put(
    "/{publication_id}",
    response_model=Publicacion,
    operation_id="editarPublicacion",
    summary="Editar una publicación propia",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Publicación no encontrada para el propietario",
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": ErrorResponse,
            "description": "Persistencia temporalmente no disponible",
        },
    },
)
def editar(
    publication_id: int,
    payload: PublicacionUpdate,
    propietario_id: int = 1,
):
    try:
        return editar_publicacion(
            publication_id,
            propietario_id,
            payload.model_dump(),
        )
    except PublicationNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except PublicationPersistenceUnavailableError as error:
        raise _service_unavailable(error) from error


@router.patch(
    "/{publication_id}/estado",
    response_model=Publicacion,
    operation_id="cambiarEstadoPublicacion",
    summary="Cambiar disponibilidad de una publicación propia",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Publicación no encontrada para el propietario",
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": ErrorResponse,
            "description": "Persistencia temporalmente no disponible",
        },
    },
)
def cambiar_estado(
    publication_id: int,
    payload: EstadoPublicacionUpdate,
    propietario_id: int = 1,
):
    try:
        return cambiar_estado_publicacion(
            publication_id,
            propietario_id,
            payload.estado_publicacion,
        )
    except PublicationNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except PublicationPersistenceUnavailableError as error:
        raise _service_unavailable(error) from error


@router.delete(
    "/{publication_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="eliminarPublicacion",
    summary="Eliminar una publicación propia",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Publicación no encontrada para el propietario",
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": ErrorResponse,
            "description": "Persistencia temporalmente no disponible",
        },
    },
)
def eliminar(publication_id: int, propietario_id: int = 1):
    try:
        eliminar_publicacion(publication_id, propietario_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except PublicationNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except PublicationPersistenceUnavailableError as error:
        raise _service_unavailable(error) from error


@router.post(
    "/{publication_id}/imagenes",
    response_model=PublicacionImagen,
    status_code=status.HTTP_201_CREATED,
    operation_id="subirImagenPublicacion",
    summary="Subir una imagen de una publicación",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Imagen inválida o máximo alcanzado",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Publicación no encontrada",
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": ErrorResponse,
            "description": "Persistencia temporalmente no disponible",
        },
    },
)
async def subir_imagen(
    publication_id: int,
    archivo: UploadFile = File(...),
):
    imagen_url: str | None = None

    try:
        if not existe_publicacion(publication_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La publicación no existe.",
            )

        if len(listar_imagenes_publicacion(publication_id)) >= 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "La publicación ya tiene el máximo "
                    "de 3 imágenes."
                ),
            )

        contenido = await archivo.read()
        imagen_url = save_publication_image(
            publication_id=publication_id,
            original_filename=archivo.filename or "",
            content=contenido,
        )

        return registrar_imagen_publicacion(
            publicacion_id=publication_id,
            imagen_url=imagen_url,
        )

    except InvalidImageError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
    except ValueError as error:
        if imagen_url is not None:
            delete_publication_image(imagen_url)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
    except PublicationPersistenceUnavailableError as error:
        if imagen_url is not None:
            delete_publication_image(imagen_url)
        raise _service_unavailable(error) from error
