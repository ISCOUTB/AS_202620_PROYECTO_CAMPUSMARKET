from typing import Literal

from fastapi import APIRouter, status
from pydantic import BaseModel, Field

from .service import crear_publicacion, listar_publicaciones


router = APIRouter(prefix="/publicaciones", tags=["publicaciones"])


class PublicacionCreate(BaseModel):
    titulo: str = Field(min_length=3, max_length=100)
    descripcion: str = Field(min_length=3, max_length=500)
    precio: float = Field(gt=0)
    modalidad: Literal["venta", "alquiler"]
    estado: Literal["nuevo", "usado", "reacondicionado"]


class Publicacion(PublicacionCreate):
    id: int


@router.post("", response_model=Publicacion, status_code=status.HTTP_201_CREATED)
def crear(payload: PublicacionCreate):
    return crear_publicacion(payload.model_dump())


@router.get("", response_model=list[Publicacion])
def listar():
    return listar_publicaciones()
