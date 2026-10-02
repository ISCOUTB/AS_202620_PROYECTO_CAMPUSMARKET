from typing import Literal

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

from backend.app.publicaciones.service import (
    PublicationPersistenceUnavailableError,
)
from .service import (
    buscar_publicaciones,
    obtener_publicacion,
)


router = APIRouter(
    prefix="/catalogo",
    tags=["catalogo"],
)


class ImagenCatalogo(BaseModel):
    id: int
    publicacion_id: int
    imagen_url: str
    orden: int
    es_principal: bool


class PublicacionCatalogo(BaseModel):
    id: int
    titulo: str
    descripcion: str
    precio: float
    modalidad: Literal["venta", "alquiler"]
    estado: Literal[
        "nuevo",
        "usado",
        "reacondicionado",
    ]
    imagenes: list[ImagenCatalogo] = []


class ErrorResponse(BaseModel):
    detail: str


@router.get(
    "",
    response_model=list[PublicacionCatalogo],
    operation_id="buscarCatalogo",
    summary="Buscar publicaciones del catálogo",
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": ErrorResponse,
            "description": "Persistencia temporalmente no disponible",
        }
    },
)
def buscar(
    q: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
    ),
    modalidad: Literal[
        "venta",
        "alquiler",
    ]
    | None = None,
    estado: Literal[
        "nuevo",
        "usado",
        "reacondicionado",
    ]
    | None = None,
    precio_min: float | None = Query(
        default=None,
        ge=0,
    ),
    precio_max: float | None = Query(
        default=None,
        ge=0,
    ),
):
    if (
        precio_min is not None
        and precio_max is not None
        and precio_min > precio_max
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="precio_min no puede ser mayor que precio_max",
        )

    try:
        return buscar_publicaciones(
            texto=q,
            modalidad=modalidad,
            estado=estado,
            precio_min=precio_min,
            precio_max=precio_max,
        )

    except PublicationPersistenceUnavailableError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El catálogo está temporalmente no disponible.",
        ) from error


@router.get(
    "/{publicacion_id}",
    response_model=PublicacionCatalogo,
    operation_id="obtenerPublicacionCatalogo",
    summary="Consultar una publicación del catálogo",
    responses={
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
def obtener(publicacion_id: int):
    try:
        publicacion = obtener_publicacion(
            publicacion_id,
        )

        if publicacion is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Publicación no encontrada",
            )

        return publicacion

    except PublicationPersistenceUnavailableError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El catálogo está temporalmente no disponible.",
        ) from error
    
    