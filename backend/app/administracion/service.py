from backend.app.publicaciones.service import obtener_publicacion, ocultar_publicacion

from .errors import InvalidReportError
from .repository import create_report, list_pending_reports, open_review


def reportar(publication_id: int, user_id: int, motivo: str) -> dict:
    publication = obtener_publicacion(publication_id)
    if not publication or not publication["visible"] or publication["propietario_id"] is None:
        raise InvalidReportError("La publicación no está disponible para reportar.")
    if publication["propietario_id"] == user_id:
        raise InvalidReportError("No puedes reportar tu propia publicación.")
    return create_report(publication_id, user_id, motivo.strip())


def listar_reportes() -> list[dict]:
    result = []
    for report in list_pending_reports():
        publication = obtener_publicacion(report["publicacion_id"])
        result.append({**report, "titulo_publicacion": publication["titulo"] if publication else "Publicación eliminada"})
    return result


def resolver(report_id: int, moderator_id: int, decision: str, note: str) -> dict:
    # Repository mantiene la fila bloqueada durante la revisión. Dos moderadores
    # no pueden resolver el mismo reporte con decisiones contradictorias.
    with open_review(report_id) as review:
        if decision == "ocultado":
            ocultar_publicacion(review.data["publicacion_id"])
        return review.finish(decision, moderator_id, note.strip())
