"""Entrega una imagen de prueba al MediaStore del emulador aislado de CI."""
import hashlib
import re
import subprocess
from pathlib import Path

fixture = Path(__file__).resolve().parents[1] / "artifacts/e2e/campusmarket-e2e.png"
collection = "content://media/external_primary/downloads"


def adb(*arguments, data=None):
    return subprocess.run(
        ["adb", *arguments], input=data, check=True, capture_output=True, timeout=15,
    ).stdout


adb(
    "shell", "content", "insert", "--uri", collection,
    "--bind", "_display_name:s:campusmarket-e2e.png",
    "--bind", "mime_type:s:image/png", "--bind", "relative_path:s:Download/",
)
rows = adb("shell", "content", "query", "--uri", collection, "--projection", "_id:_display_name").decode()
matching = [line for line in rows.splitlines() if "campusmarket-e2e.png" in line]
if len(matching) != 1:
    raise SystemExit("El MediaStore no contiene una única imagen de prueba.")
identifier = re.search(r"_id=(\d+)", matching[0])
if identifier is None:
    raise SystemExit("El MediaStore no devolvió el identificador del archivo.")
uri = collection + "/" + identifier.group(1)
source = fixture.read_bytes()
adb("shell", "content", "write", "--uri", uri, data=source)
stored = adb("exec-out", "content", "read", "--uri", uri)
if hashlib.sha256(stored).digest() != hashlib.sha256(source).digest():
    raise SystemExit("La imagen del emulador no coincide con el archivo de prueba.")
print("PNG real escrito y verificado mediante MediaStore; sin permisos de almacenamiento del producto.")
