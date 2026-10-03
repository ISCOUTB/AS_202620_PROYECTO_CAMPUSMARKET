"""Ejecutar defectos controlados en copias temporales; nunca alterar el original."""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MUTATIONS = [
    (
        "imagen-disfrazada-sin-decodificacion",
        "backend/app/publicaciones/image_storage.py",
        "validated = _validated_image(extension, content)",
        "validated = content",
        "backend/tests/test_imagenes_seguras.py::test_contenido_no_puede_disfrazarse_con_otra_extension",
    ),
    (
        "moderacion-sin-capacidad",
        "backend/app/usuarios/dependencies.py",
        "if not user[\"es_admin\"]:",
        "if False:",
        "backend/tests/test_administracion.py::test_registro_y_perfil_no_autorizan_moderacion",
    ),
    (
        "EC02-escritura-sin-propietario",
        "backend/app/publicaciones/repository.py",
        "                  AND propietario_id = %s",
        "                  AND %s > 0",
        "backend/tests/test_ec02_autorizacion.py::test_ec02_diez_intentos_ajenos_no_modifican_datos",
    ),
    (
        "login-ignora-password-invalido",
        "backend/app/usuarios/service.py",
        "if not user or not valid:",
        "if not user:",
        "backend/tests/test_usuarios.py::test_credenciales_incorrectas_no_crean_sesion",
    ),
    (
        "catalogo-importa-repository-ajeno",
        "backend/app/catalogo/service.py",
        "from backend.app.publicaciones.service import (",
        "from backend.app.publicaciones import repository\nfrom backend.app.publicaciones.service import (",
        "backend/tests/test_erosion_s9.py::test_catalogo_no_importa_repository_de_publicaciones",
    ),
]


def main():
    evidence = []
    for name, path, old, new, test in MUTATIONS:
        with tempfile.TemporaryDirectory(prefix="campusmarket-mutacion-") as directory:
            clone = Path(directory)
            for item in ("backend", "contracts"):
                shutil.copytree(ROOT / item, clone / item, ignore=shutil.ignore_patterns("uploads", "__pycache__", "*.pyc"))
            target = clone / path
            original = target.read_text(encoding="utf-8")
            if old not in original:
                raise RuntimeError(f"El punto de mutación no existe: {name}")
            target.write_text(original.replace(old, new, 1), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-m", "pytest", test, "-q", "--tb=no"],
                cwd=clone, text=True, capture_output=True, check=False,
            )
            # Exit 1 significa fallo de aserción, no error de importación/colección.
            detected = result.returncode == 1 and "1 failed" in result.stdout
            evidence.append({"mutacion": name, "prueba": test, "exit_code": result.returncode, "detectada": detected})
    print(json.dumps({"mutaciones": evidence, "todas_detectadas": all(item["detectada"] for item in evidence)}, ensure_ascii=False, indent=2))
    return 0 if all(item["detectada"] for item in evidence) else 1


if __name__ == "__main__":
    raise SystemExit(main())
