from typing import Literal

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
    status,
)
from pydantic import BaseModel, Field

from .image_storage import (
    InvalidImageError,
    save_publication_image,
)
from .repository import (
    PersistenceUnavailableError,
    count_publication_images,
    create_publication_image,
    publication_exists,
)
from .service import (
    PublicationPersistenceUnavailableError,
    crear_publicacion,
    listar_publicaciones,
)


router = APIRouter(
    prefix="/publicaciones",
    tags=["publicaciones"],
)


class PublicacionCreate(BaseModel):
    titulo: str = Field(min_length=3, max_length=100)
    descripcion: str = Field(min_length=3, max_length=500)
    precio: float = Field(gt=0)
    modalidad: Literal["venta", "alquiler"]
    estado: Literal["nuevo", "usado", "reacondicionado"]


class Publicacion(PublicacionCreate):
    id: int


class PublicacionImagen(BaseModel):
    id: int
    publicacion_id: int
    imagen_url: str
    orden: int
    es_principal: bool


class ErrorResponse(BaseModel):
    detail: str


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
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "La persistencia está temporalmente no disponible. "
                "Intenta nuevamente."
            ),
        ) from error


@router.get(
    "",
    response_model=list[Publicacion],
    operation_id="listarPublicaciones",
    summary="Listar publicaciones",
)
def listar():
    return listar_publicaciones()


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
    try:
        if not publication_exists(publication_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La publicación no existe.",
            )

        if count_publication_images(publication_id) >= 3:
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

        return create_publication_image(
            publication_id=publication_id,
            imagen_url=imagen_url,
        )

    except InvalidImageError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    except PersistenceUnavailableError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "La persistencia está temporalmente no disponible."
            ),
        ) from error

    