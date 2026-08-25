import os
import sqlite3
from pathlib import Path


def _db_path() -> Path:
    configured = os.getenv("CAMPUSMARKET_DB_PATH")

    if configured:
        return Path(configured)

    return Path(__file__).resolve().parents[2] / "data" / "campusmarket.db"


def _connect() -> sqlite3.Connection:
    path = _db_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database() -> None:
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS publicaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                precio REAL NOT NULL CHECK (precio > 0),
                modalidad TEXT NOT NULL
                    CHECK (modalidad IN ('venta', 'alquiler')),
                estado TEXT NOT NULL
                    CHECK (
                        estado IN (
                            'nuevo',
                            'usado',
                            'reacondicionado'
                        )
                    )
            )
            """
        )


def create_publication(data: dict) -> dict:
    initialize_database()

    with _connect() as connection:
        cursor = connection.execute(
            """
            INSERT INTO publicaciones (
                titulo,
                descripcion,
                precio,
                modalidad,
                estado
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                data["titulo"],
                data["descripcion"],
                data["precio"],
                data["modalidad"],
                data["estado"],
            ),
        )

        publication_id = cursor.lastrowid

        row = connection.execute(
            """
            SELECT
                id,
                titulo,
                descripcion,
                precio,
                modalidad,
                estado
            FROM publicaciones
            WHERE id = ?
            """,
            (publication_id,),
        ).fetchone()

    return dict(row)


def list_publications() -> list[dict]:
    initialize_database()

    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                titulo,
                descripcion,
                precio,
                modalidad,
                estado
            FROM publicaciones
            ORDER BY id DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]