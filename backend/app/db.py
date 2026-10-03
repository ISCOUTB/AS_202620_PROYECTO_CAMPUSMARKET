"""Infraestructura MySQL compartida; no contiene tablas de dominio."""

import os
import ssl
from contextlib import contextmanager

import pymysql
from pymysql.cursors import DictCursor


class PersistenceUnavailableError(RuntimeError):
    """MySQL no puede atender la operación."""


def connect():
    options = {
        "host": os.getenv("CAMPUSMARKET_DB_HOST", "localhost"),
        "port": int(os.getenv("CAMPUSMARKET_DB_PORT", "3306")),
        "user": os.getenv("CAMPUSMARKET_DB_USER", "campusmarket_app"),
        "password": os.getenv("CAMPUSMARKET_DB_PASSWORD", ""),
        "database": os.getenv("CAMPUSMARKET_DB_NAME", "campusmarket"),
        "cursorclass": DictCursor,
        "autocommit": False,
        "connect_timeout": 2,
        "read_timeout": 10,
        "write_timeout": 10,
        "charset": "utf8mb4",
    }
    if os.getenv("CAMPUSMARKET_DB_SSL", "false").lower() in {"1", "true", "yes", "on"}:
        options["ssl"] = ssl.create_default_context()
    try:
        return pymysql.connect(**options)
    except pymysql.MySQLError as error:
        raise PersistenceUnavailableError("Persistencia temporalmente no disponible.") from error


@contextmanager
def transaction():
    connection = connect()
    try:
        with connection.cursor() as cursor:
            yield cursor
        connection.commit()
    except Exception as error:
        connection.rollback()
        if isinstance(error, pymysql.MySQLError):
            raise PersistenceUnavailableError("Persistencia temporalmente no disponible.") from error
        raise
    finally:
        connection.close()


def database_is_available() -> bool:
    try:
        with transaction() as cursor:
            cursor.execute("SELECT 1")
            return cursor.fetchone() is not None
    except PersistenceUnavailableError:
        return False
