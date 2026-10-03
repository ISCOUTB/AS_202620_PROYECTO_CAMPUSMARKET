from datetime import datetime
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from backend.app.publicaciones.service import PublicationPersistenceUnavailableError
from backend.app.usuarios.dependencies import ModeradorActual, UsuarioActual

from .errors import InvalidReportError, ReportConflictError, ReportNotFoundError
from .service import listar_reportes, reportar, resolver

router = APIRouter(prefix="/administracion", tags=["administracion"])


class ReporteCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    publicacion_id: int = Field(gt=0)
    motivo: str = Field(min_length=10, max_length=500)


class ReporteResolve(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    decision: Literal["ocultado", "descartado"]
    nota: str = Field(min_length=5, max_length=500)


class Reporte(BaseModel):
    id: int
    publicacion_id: int
    reportado_por: int
    motivo: str
    estado: Literal["pendiente", "ocultado", "descartado"]
    resuelto_por: int | None
    nota: str | None
    creado_en: datetime
    resuelto_en: datetime | None
    titulo_publicacion: str | None = None


def _call(function, *args):
    try:
        return function(*args)
    except ReportNotFoundError as error:
        raise HTTPException(404, str(error)) from error
    except ReportConflictError as error:
        raise HTTPException(409, str(error)) from error
    except InvalidReportError as error:
        raise HTTPException(400, str(error)) from error
    except PublicationPersistenceUnavailableError as error:
        raise HTTPException(503, "La persistencia está temporalmente no disponible.") from error


@router.post("/reportes", response_model=Reporte, status_code=201, operation_id="reportarPublicacion")
def nuevo_reporte(payload: ReporteCreate, user: UsuarioActual):
    return _call(reportar, payload.publicacion_id, user["id"], payload.motivo)


@router.get("/reportes", response_model=list[Reporte], operation_id="listarReportesPendientes")
def reportes(moderator: ModeradorActual):
    return _call(listar_reportes)


@router.patch("/reportes/{report_id}", response_model=Reporte, operation_id="resolverReporte")
def resolve(report_id: int, payload: ReporteResolve, moderator: ModeradorActual):
    return _call(resolver, report_id, moderator["id"], payload.decision, payload.nota)
