"""Verifica autorización del cliente introduciendo defectos y restaurando fuentes."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend/campusmarket"
CASES = [
    (
        "lib/publicaciones/publicaciones_api.dart",
        "{'titulo': titulo,",
        "{'propietario_id': 1, 'titulo': titulo,",
        "crear y consultar propias envía sesión y omite cualquier propietario suministrado",
        "propietario fijo en el cliente",
    ),
    (
        "lib/usuarios/session_controller.dart",
        "if (authorization == 'Bearer $_token') _clear();",
        "if (authorization != null) _clear();",
        "respuesta antigua de A no invalida una sesión nueva de B",
        "invalidación de la cuenta nueva por una respuesta antigua",
    ),
]


def main():
    for relative, original, defect, test, name in CASES:
        path = FRONTEND / relative
        content = path.read_text()
        if content.count(original) != 1:
            raise RuntimeError("La mutación requiere un único punto verificable.")
        try:
            path.write_text(content.replace(original, defect, 1))
            result = subprocess.run(
                ["flutter", "test", "test/session_authorization_test.dart", "--plain-name", test],
                cwd=FRONTEND, capture_output=True, text=True, timeout=120,
            )
            output = result.stdout + result.stderr
            if result.returncode != 1 or "Expected:" not in output or "Actual:" not in output:
                raise RuntimeError("La prueba no detectó el defecto por una aserción: " + name)
            print("Mutación detectada: " + name)
        finally:
            path.write_text(content)
    print("2/2 defectos del cliente detectados; fuentes restauradas.")


if __name__ == "__main__":
    main()
