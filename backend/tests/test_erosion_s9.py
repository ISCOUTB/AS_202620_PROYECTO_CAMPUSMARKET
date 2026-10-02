from pathlib import Path

CATALOGO_DIR = (
    Path(__file__).resolve().parents[1]
    / "app"
    / "catalogo"
)


def _codigo_catalogo() -> str:
    contenido = []

    for archivo in CATALOGO_DIR.glob("*.py"):
        contenido.append(
            archivo.read_text(encoding="utf-8")
        )

    return "\n".join(contenido)


def test_catalogo_no_importa_repository_de_publicaciones():
    codigo = _codigo_catalogo()

    assert "publicaciones.repository" not in codigo
    assert "from backend.app.publicaciones import repository" not in codigo


def test_catalogo_no_usa_pymysql_directamente():
    codigo = _codigo_catalogo()

    assert "pymysql" not in codigo.lower()


def test_catalogo_no_escribe_publicaciones_directamente():
    codigo = _codigo_catalogo().upper()

    assert "INSERT INTO PUBLICACIONES" not in codigo
    assert "UPDATE PUBLICACIONES" not in codigo
    assert "DELETE FROM PUBLICACIONES" not in codigo
