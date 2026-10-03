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


def _column_exists(cursor, table_name: str, column_name: str) -> bool:
    cursor.execute(
        """
        SELECT 1
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = %s
          AND COLUMN_NAME = %s
        LIMIT 1
        """,
        (table_name, column_name),
    )
    return cursor.fetchone() is not None


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
                    propietario_id BIGINT UNSIGNED NOT NULL DEFAULT 1,
                    estado_publicacion ENUM(
                        'disponible',
                        'reservado',
                        'vendido'
                    ) NOT NULL DEFAULT 'disponible',
                    PRIMARY KEY (id),
                    CONSTRAINT chk_publicaciones_precio
                        CHECK (precio > 0)
                )
                """
            )

            if not _column_exists(cursor, "publicaciones", "propietario_id"):
                cursor.execute(
                    """
                    ALTER TABLE publicaciones
                    ADD COLUMN propietario_id BIGINT UNSIGNED
                        NOT NULL DEFAULT 1
                    """
                )

            if not _column_exists(
                cursor,
                "publicaciones",
                "estado_publicacion",
            ):
                cursor.execute(
                    """
                    ALTER TABLE publicaciones
                    ADD COLUMN estado_publicacion ENUM(
                        'disponible',
                        'reservado',
                        'vendido'
                    ) NOT NULL DEFAULT 'disponible'
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


def _select_publication_fields() -> str:
    return """
        id,
        titulo,
        descripcion,
        CAST(precio AS DOUBLE) AS precio,
        modalidad,
        estado,
        propietario_id,
        estado_publicacion
    """


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
                    estado,
                    propietario_id,
                    estado_publicacion
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    data["titulo"],
                    data["descripcion"],
                    data["precio"],
                    data["modalidad"],
                    data["estado"],
                    data["propietario_id"],
                    data["estado_publicacion"],
                ),
            )

            publication_id = cursor.lastrowid
            cursor.execute(
                f"""
                SELECT {_select_publication_fields()}
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
                f"""
                SELECT {_select_publication_fields()}
                FROM publicaciones
                ORDER BY id DESC
                """
            )
            return cursor.fetchall()
    except pymysql.MySQLError as error:
        raise PersistenceUnavailableError(
            "La persistencia está temporalmente no disponible."
        ) from error
    finally:
        if connection:
            connection.close()


def list_publications_by_owner(propietario_id: int) -> list[dict]:
    initialize_database()
    connection = None

    try:
        connection = _connect()
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT {_select_publication_fields()}
                FROM publicaciones
                WHERE propietario_id = %s
                ORDER BY id DESC
                """,
                (propietario_id,),
            )
            return cursor.fetchall()
    except pymysql.MySQLError as error:
        raise PersistenceUnavailableError(
            "La persistencia está temporalmente no disponible."
        ) from error
    finally:
        if connection:
            connection.close()


def get_publication(publication_id: int) -> dict | None:
    initialize_database()
    connection = None

    try:
        connection = _connect()
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT {_select_publication_fields()}
                FROM publicaciones
                WHERE id = %s
                """,
                (publication_id,),
            )
            return cursor.fetchone()
    except pymysql.MySQLError as error:
        raise PersistenceUnavailableError(
            "La persistencia está temporalmente no disponible."
        ) from error
    finally:
        if connection:
            connection.close()


def publication_exists(publication_id: int) -> bool:
    return get_publication(publication_id) is not None


def update_publication(
    publication_id: int,
    propietario_id: int,
    data: dict,
) -> dict | None:
    initialize_database()
    connection = None

    try:
        connection = _connect()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE publicaciones
                SET titulo = %s,
                    descripcion = %s,
                    precio = %s,
                    modalidad = %s,
                    estado = %s
                WHERE id = %s
                  AND propietario_id = %s
                """,
                (
                    data["titulo"],
                    data["descripcion"],
                    data["precio"],
                    data["modalidad"],
                    data["estado"],
                    publication_id,
                    propietario_id,
                ),
            )

            if cursor.rowcount == 0:
                connection.rollback()
                return None

            cursor.execute(
                f"""
                SELECT {_select_publication_fields()}
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


def update_publication_status(
    publication_id: int,
    propietario_id: int,
    estado_publicacion: str,
) -> dict | None:
    initialize_database()
    connection = None

    try:
        connection = _connect()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE publicaciones
                SET estado_publicacion = %s
                WHERE id = %s
                  AND propietario_id = %s
                """,
                (
                    estado_publicacion,
                    publication_id,
                    propietario_id,
                ),
            )

            if cursor.rowcount == 0:
                connection.rollback()
                return None

            cursor.execute(
                f"""
                SELECT {_select_publication_fields()}
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


def delete_publication(publication_id: int, propietario_id: int) -> bool:
    initialize_database()
    connection = None

    try:
        connection = _connect()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM publicaciones
                WHERE id = %s
                  AND propietario_id = %s
                """,
                (publication_id, propietario_id),
            )
            deleted = cursor.rowcount > 0

        connection.commit()
        return deleted
    except pymysql.MySQLError as error:
        if connection:
            connection.rollback()
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
            return cursor.fetchall()
    except pymysql.MySQLError as error:
        raise PersistenceUnavailableError(
            "La persistencia está temporalmente no disponible."
        ) from error
    finally:
        if connection:
            connection.close()


def count_publication_images(publication_id: int) -> int:
    return len(list_publication_images(publication_id))


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
                (publication_id, imagen_url, orden, es_principal),
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
