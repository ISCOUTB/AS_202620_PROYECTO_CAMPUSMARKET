from pathlib import Path
from uuid import uuid4


UPLOAD_ROOT = Path("backend/uploads/publicaciones")

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}

MAX_FILE_SIZE = 5 * 1024 * 1024


class InvalidImageError(ValueError):
    """La imagen no cumple las restricciones permitidas."""


def save_publication_image(
    publication_id: int,
    original_filename: str,
    content: bytes,
) -> str:
    extension = Path(original_filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise InvalidImageError(
            "Formato no permitido. Usa JPG, JPEG, PNG o WEBP."
        )

    if len(content) > MAX_FILE_SIZE:
        raise InvalidImageError(
            "La imagen supera el tamaño máximo de 5 MB."
        )

    publication_dir = UPLOAD_ROOT / str(publication_id)
    publication_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid4().hex}{extension}"
    destination = publication_dir / filename

    destination.write_bytes(content)

    return f"/uploads/publicaciones/{publication_id}/{filename}"

