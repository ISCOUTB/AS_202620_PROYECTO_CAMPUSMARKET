from contextlib import contextmanager

import pymysql

from backend.app.db import transaction

from .errors import ReportConflictError, ReportNotFoundError


def initialize_database():
    with transaction() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reportes_publicacion (
                id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                publicacion_id BIGINT UNSIGNED NOT NULL,
                reportado_por BIGINT UNSIGNED NOT NULL,
                motivo VARCHAR(500) NOT NULL,
                estado ENUM('pendiente', 'ocultado', 'descartado') NOT NULL DEFAULT 'pendiente',
                resuelto_por BIGINT UNSIGNED NULL,
                nota VARCHAR(500) NULL,
                creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                resuelto_en DATETIME NULL,
                UNIQUE (publicacion_id, reportado_por)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)


def create_report(publication_id: int, user_id: int, motivo: str) -> dict:
    initialize_database()
    with transaction() as cursor:
        try:
            cursor.execute("INSERT INTO reportes_publicacion (publicacion_id, reportado_por, motivo) VALUES (%s, %s, %s)", (publication_id, user_id, motivo))
        except pymysql.IntegrityError as error:
            if error.args[0] == 1062:
                raise ReportConflictError("Ya reportaste esta publicación.") from error
            raise
        cursor.execute("SELECT * FROM reportes_publicacion WHERE id = %s", (cursor.lastrowid,))
        return cursor.fetchone()


def list_pending_reports() -> list[dict]:
    initialize_database()
    with transaction() as cursor:
        cursor.execute("SELECT * FROM reportes_publicacion WHERE estado = 'pendiente' ORDER BY creado_en, id")
        return cursor.fetchall()


class ReportReview:
    def __init__(self, cursor, data: dict):
        self.cursor = cursor
        self.data = data

    def finish(self, decision: str, moderator_id: int, note: str) -> dict:
        self.cursor.execute("UPDATE reportes_publicacion SET estado = %s, resuelto_por = %s, nota = %s, resuelto_en = UTC_TIMESTAMP() WHERE id = %s", (decision, moderator_id, note, self.data["id"]))
        self.cursor.execute("SELECT * FROM reportes_publicacion WHERE id = %s", (self.data["id"],))
        return self.cursor.fetchone()


@contextmanager
def open_review(report_id: int):
    initialize_database()
    with transaction() as cursor:
        cursor.execute("SELECT * FROM reportes_publicacion WHERE id = %s FOR UPDATE", (report_id,))
        data = cursor.fetchone()
        if not data:
            raise ReportNotFoundError("El reporte no existe.")
        if data["estado"] != "pendiente":
            raise ReportConflictError("El reporte ya fue resuelto.")
        yield ReportReview(cursor, data)
