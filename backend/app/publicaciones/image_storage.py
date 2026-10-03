import os
import warnings
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from PIL import Image, ImageOps, UnidentifiedImageError

from backend.app.resource_limits import HEAVY_WORK_SLOT

UPLOAD_ROOT = Path(os.getenv("CAMPUSMARKET_UPLOAD_DIR", "backend/uploads")) / "publicaciones"
ALLOWED_EXTENSIONS = {".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG", ".webp": "WEBP"}
MAX_FILE_SIZE = 5 * 1024 * 1024
MAX_PIXELS = 20_000_000
Image.MAX_IMAGE_PIXELS = MAX_PIXELS
MAX_IMAGE_EDGE = 2048


class InvalidImageError(ValueError):
    """La imagen no cumple las restricciones permitidas."""


def _validated_image(extension: str, content: bytes) -> bytes:
    try:
        with HEAVY_WORK_SLOT, warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(BytesIO(content)) as original:
                if original.format != ALLOWED_EXTENSIONS[extension]:
                    raise InvalidImageError("El contenido no coincide con el formato de la imagen.")
                if original.width * original.height > MAX_PIXELS:
                    raise InvalidImageError("La imagen supera 20 megapíxeles.")
                # thumbnail utiliza draft para JPEG antes de decodificar.
                original.thumbnail((MAX_IMAGE_EDGE, MAX_IMAGE_EDGE), Image.Resampling.LANCZOS)
                original.load()
                oriented = ImageOps.exif_transpose(original)
                image = oriented.convert("RGB" if extension in {".jpg", ".jpeg"} else "RGBA")
                # Crear otro objeto sin info/EXIF del original.
                clean = Image.new(image.mode, image.size)
                clean.paste(image)
                output = BytesIO()
                clean.save(output, format=ALLOWED_EXTENSIONS[extension])
                encoded = output.getvalue()
                if len(encoded) > MAX_FILE_SIZE:
                    raise InvalidImageError("La imagen procesada supera 5 MB.")
                return encoded
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError, Image.DecompressionBombWarning, SyntaxError) as error:
        raise InvalidImageError("El archivo no es una imagen válida o excede el límite de píxeles.") from error


def save_publication_image(publication_id: int, original_filename: str, content: bytes) -> str:
    extension = Path(original_filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise InvalidImageError("Formato no permitido. Usa JPG, JPEG, PNG o WEBP.")
    if not content:
        raise InvalidImageError("La imagen está vacía.")
    if len(content) > MAX_FILE_SIZE:
        raise InvalidImageError("La imagen supera el tamaño máximo de 5 MB.")
    validated = _validated_image(extension, content)
    publication_dir = UPLOAD_ROOT / str(publication_id)
    publication_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}{extension}"
    (publication_dir / filename).write_bytes(validated)
    return f"/uploads/publicaciones/{publication_id}/{filename}"


def delete_publication_image(imagen_url: str) -> None:
    prefix = "/uploads/publicaciones/"
    if not imagen_url.startswith(prefix):
        return
    destination = (UPLOAD_ROOT / imagen_url[len(prefix):]).resolve()
    if not destination.is_relative_to(UPLOAD_ROOT.resolve()):
        return
    try:
        destination.unlink(missing_ok=True)
    except OSError:
        # Mantener el error principal; reconciliar huérfanos en operación.
        return
