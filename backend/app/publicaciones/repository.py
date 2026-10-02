import os
import ssl

import pymysql
from pymysql.cursors import DictCursor


class PersistenceUnavailableError(RuntimeError):
    """La persistencia no está disponible temporalmente."""


def _connect():
    try:
        connection_options = {
            "host": os.getenv("CAMPUSMARKET_DB_HOST", "localhost"),
            "port": int(os.getenv("CAMPUSMARKET_DB_PORT", "3306")),
            "user": os.getenv("CAMPUSMARKET_DB_USER", "campusmarket_app"),
            "password": os.getenv("CAMPUSMARKET_DB_PASSWORD", ""),
            "database": os.getenv("CAMPUSMARKET_DB_NAME", "campusmarket"),
            "cursorclass": DictCursor,
            "autocommit": False,
            "connect_timeout": 2,
        }

        use_ssl = os.getenv(
            "CAMPUSMARKET_DB_SSL",
            "false",
        ).strip().lower() in {"1", "true", "yes", "on"}

        if use_ssl:
            connection_options["ssl"] = ssl.create_default_context()

        return pymysql.connect(**connection_options)

    except pymysql.MySQLError as error:
        raise PersistenceUnavailableError(
            "La persistencia está temporalmente no disponible."
        ) from error


def initialize_database() -> None:
    connection = None

    try:
        connection = _connect()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS publicaciones (
                    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
                    titulo VARCHAR(100) NOT NULL,
                    descripcion VARCHAR(500) NOT NULL,
                    precio DECIMAL(12, 2) NOT NULL,
                    modalidad ENUM('venta', 'alquiler') NOT NULL,
                    estado ENUM(
                        'nuevo',
                        'usado',
                        'reacondicionado'
                    ) NOT NULL,
                    PRIMARY KEY (id),
                    CONSTRAINT chk_publicaciones_precio
                        CHECK (precio > 0)
                )
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS publicacion_imagenes (
                    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
                    publicacion_id BIGINT UNSIGNED NOT NULL,
                    imagen_url VARCHAR(500) NOT NULL,
                    orden TINYINT UNSIGNED NOT NULL,
                    es_principal BOOLEAN NOT NULL DEFAULT FALSE,
                    PRIMARY KEY (id),
                    CONSTRAINT fk_publicacion_imagenes_publicacion
                        FOREIGN KEY (publicacion_id)
                        REFERENCES publicaciones(id)
                        ON DELETE CASCADE,
                    CONSTRAINT uq_publicacion_imagenes_orden
                        UNIQUE (publicacion_id, orden),
                    CONSTRAINT chk_publicacion_imagenes_orden
                        CHECK (orden BETWEEN 1 AND 3)
                )
                """
            )

        connection.commit()

    except pymysql.MySQLError as error:
        if connection:
            connection.rollback()

        raise PersistenceUnavailableError(
            "La persistencia está temporalmente no disponible."
        ) from error

    finally:
        if connection:
            connection.close()


def create_publication(data: dict) -> dict:
    initialize_database()

    connection = None

    try:
        connection = _connect()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO publicaciones (
                    titulo,
                    descripcion,
                    precio,
                    modalidad,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s)
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

            cursor.execute(
                """
                SELECT
                    id,
                    titulo,
                    descripcion,
                    CAST(precio AS DOUBLE) AS precio,
                    modalidad,
                    estado
                FROM publicaciones
                WHERE id = %s
                """,
                (publication_id,),
            )

            row = cursor.fetchone()

        connection.commit()

        return row

    except pymysql.MySQLError as error:
        if connection:
            connection.rollback()

        raise PersistenceUnavailableError(
            "La persistencia está temporalmente no disponible."
        ) from error

    finally:
        if connection:
            connection.close()


def list_publications() -> list[dict]:
    initialize_database()

    connection = None

    try:
        connection = _connect()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    titulo,
                    descripcion,
                    CAST(precio AS DOUBLE) AS precio,
                    modalidad,
                    estado
                FROM publicaciones
                ORDER BY id DESC
                """
            )

            rows = cursor.fetchall()

        return rows

    except pymysql.MySQLError as error:
        raise PersistenceUnavailableError(
            "La persistencia está temporalmente no disponible."
        ) from error

    finally:
        if connection:
            connection.close()


def publication_exists(publication_id: int) -> bool:
    initialize_database()

    connection = None

    try:
        connection = _connect()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT 1
                FROM publicaciones
                WHERE id = %s
                """,
                (publication_id,),
            )

            return cursor.fetchone() is not None

    except pymysql.MySQLError as error:
        raise PersistenceUnavailableError(
            "La persistencia está temporalmente no disponible."
        ) from error

    finally:
        if connection:
            connection.close()


def list_publication_images(publication_id: int) -> list[dict]:
    initialize_database()

    connection = None

    try:
        connection = _connect()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    publicacion_id,
                    imagen_url,
                    orden,
                    es_principal
                FROM publicacion_imagenes
                WHERE publicacion_id = %s
                ORDER BY orden ASC
                """,
                (publication_id,),
            )

            rows = cursor.fetchall()

        return rows

    except pymysql.MySQLError as error:
        raise PersistenceUnavailableError(
            "La persistencia está temporalmente no disponible."
        ) from error

    finally:
        if connection:
            connection.close()


def count_publication_images(publication_id: int) -> int:
    initialize_database()

    connection = None

    try:
        connection = _connect()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*) AS total
                FROM publicacion_imagenes
                WHERE publicacion_id = %s
                """,
                (publication_id,),
            )

            row = cursor.fetchone()

        return int(row["total"])

    except pymysql.MySQLError as error:
        raise PersistenceUnavailableError(
            "La persistencia está temporalmente no disponible."
        ) from error

    finally:
        if connection:
            connection.close()


def create_publication_image(
    publication_id: int,
    imagen_url: str,
) -> dict:
    initialize_database()

    connection = None

    try:
        connection = _connect()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*) AS total
                FROM publicacion_imagenes
                WHERE publicacion_id = %s
                """,
                (publication_id,),
            )

            row = cursor.fetchone()
            total = int(row["total"])

            if total >= 3:
                raise ValueError(
                    "La publicación ya tiene el máximo de 3 imágenes."
                )

            orden = total + 1
            es_principal = total == 0

            cursor.execute(
                """
                INSERT INTO publicacion_imagenes (
                    publicacion_id,
                    imagen_url,
                    orden,
                    es_principal
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    publication_id,
                    imagen_url,
                    orden,
                    es_principal,
                ),
            )

            image_id = cursor.lastrowid

            cursor.execute(
                """
                SELECT
                    id,
                    publicacion_id,
                    imagen_url,
                    orden,
                    es_principal
                FROM publicacion_imagenes
                WHERE id = %s
                """,
                (image_id,),
            )

            image = cursor.fetchone()

        connection.commit()

        return image

    except ValueError:
        if connection:
            connection.rollback()

        raise

    except pymysql.MySQLError as error:
        if connection:
            connection.rollback()

        raise PersistenceUnavailableError(
            "La persistencia está temporalmente no disponible."
        ) from error

    finally:
        if connection:
            connection.close()


def database_is_available() -> bool:
    connection = None

    try:
        connection = _connect()

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            return cursor.fetchone() is not None

    except (PersistenceUnavailableError, pymysql.MySQLError):
        return False

    finally:
        if connection:
            connection.close()

            