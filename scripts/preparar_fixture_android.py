"""Entrega una imagen de prueba al MediaStore del emulador aislado de CI."""
import hashlib
import re
import subprocess
import time
from pathlib import Path

fixture = Path(__file__).resolve().parents[1] / "artifacts/e2e/campusmarket-e2e.png"
collection = "content://media/external_primary/downloads"


def adb(*arguments, data=None):
    result = subprocess.run(
        ["adb", *arguments], input=data, check=True, capture_output=True, timeout=15,
    )
    error = result.stderr.decode(errors="replace")
    if "Volume external_primary not found" in error:
        raise RuntimeError("MediaStore aún no tiene montado external_primary.")
    if "Error while accessing provider" in error:
        raise SystemExit(error)
    return result.stdout


for attempt in range(60):
    ready = adb("shell", "getprop", "sys.user.0.ce_available").decode().strip()
    if ready == "true":
        break
    time.sleep(0.5)
else:
    raise SystemExit("El almacenamiento del usuario del emulador no está listo.")

deadline = time.monotonic() + 60
while True:
    try:
        created = adb(
            "shell", "content", "insert", "--uri", collection,
            "--bind", "_display_name:s:campusmarket-e2e.png",
            "--bind", "mime_type:s:image/png", "--bind", "relative_path:s:Download/",
        ).decode(errors="replace")
        break
    except RuntimeError:
        if time.monotonic() >= deadline:
            raise SystemExit("El volumen external_primary no se montó a tiempo.") from None
        time.sleep(0.5)
if created.strip():
    print("MediaStore insert: " + created, flush=True)
rows = adb("shell", "content", "query", "--uri", collection, "--projection", "_id:_display_name").decode()
matching = [line for line in rows.splitlines() if "campusmarket-e2e.png" in line]
if len(matching) != 1:
    print("MediaStore query: " + rows, flush=True)
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
