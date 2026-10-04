# Auditoría S9 - Dependencias y secretos

**Proyecto:** CampusMarket
**Semana:** S9
**Fecha:** 2026-10-01

---

## 1. Dependencias

Para la porción S9 correspondiente a la materialización del Catálogo se revisaron:

- `requirements.txt`
- `frontend/campusmarket/pubspec.yaml`

No se incorporaron nuevas dependencias como consecuencia de la implementación de Catálogo.

La solución utiliza capacidades ya presentes en el proyecto:

- FastAPI;
- Pydantic;
- Pytest;
- TestClient;
- biblioteca estándar de Python.

Por tanto, no existen nuevas dependencias propuestas por IA que deban incorporarse al sistema para esta porción.

---

## 2. Búsqueda de secretos de alto riesgo

Se ejecutó:

git grep -n -I -E "AKIA|AIza|sk-[A-Za-z0-9]|ghp_|github_pat_|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY"

Resultado:
Sin coincidencias.

No se detectaron:
- claves privadas;
- tokens GitHub;
- claves OpenAI;
- claves Google;
- patrones AWS revisados.

## 3. Revisión de referencias a credenciales
Se ejecutó:
git grep -n -I -E "PASSWORD|SECRET|TOKEN|API_KEY"

Las coincidencias fueron revisadas individualmente.
Variables de entorno
Referencias como:
- CAMPUSMARKET_DB_PASSWORD
- SONAR_TOKEN
corresponden a nombres de variables de entorno o documentación de configuración.
No contienen el valor de una credencial productiva.
Placeholders documentales
El README utiliza:
<PASSWORD_LOCAL>

como marcador explícito e indica que no debe sustituirse por una credencial real dentro de un archivo versionado.
Credenciales efímeras de CI
El workflow backend-tests.yml contiene:
MYSQL_ROOT_PASSWORD: root_ci
MYSQL_PASSWORD: campusmarket_ci
CAMPUSMARKET_DB_PASSWORD: campusmarket_ci

Estos valores pertenecen exclusivamente al servicio MySQL efímero creado durante GitHub Actions.
No corresponden a la base de datos desplegada ni otorgan acceso a un recurso persistente externo.
Se clasifican como datos de prueba reproducibles del entorno CI, no como secretos productivos.

## 4. Resultado
Control	Resultado
Nuevas dependencias S9	Ninguna
Tokens detectados	Ninguno
Claves privadas detectadas	Ninguna
Credenciales productivas hardcodeadas detectadas	Ninguna
Placeholders documentales	Sí, controlados
Credenciales efímeras de CI	Sí, identificadas y limitadas al entorno de pruebas


Resultado de auditoría: sin evidencia de secretos productivos incorporados por la porción S9.

## Ampliacion al periodo S9 completo

Revisión: 3 de octubre de 2026, America/Bogota. Base S8 `784d788`;
estado contrastado `7856416795bb4accdf9d05e01adb470654875e56`.
La ausencia de nuevas dependencias descrita arriba se limita al Catálogo inicial.
El [diff del periodo](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/compare/784d788...7856416795bb4accdf9d05e01adb470654875e56)
y la lectura de ambos manifests muestran estas incorporaciones:

| Dependencia / manifest | Necesidad y legitimidad | Comprobación oficial |
|---|---|---|
| python-multipart==0.0.20; [requirements](../../backend/requirements.txt) | Parser multipart para subida de archivos. Paquete python-multipart; no confundir con otro paquete llamado multipart. PyPI declara Python >=3.8 y Source Kludex/python-multipart | [JSON exacto de versión](https://pypi.org/pypi/python-multipart/0.0.20/json), [código](https://github.com/Kludex/python-multipart) |
| Pillow==12.3.0; [requirements](../../backend/requirements.txt) | Decodificación/reencodificación real, orientación y retiro de metadatos. PyPI devuelve nombre pillow, versión 12.3.0, Python >=3.10 y Source python-pillow/Pillow; ADR-0015 | [JSON exacto de versión](https://pypi.org/pypi/Pillow/12.3.0/json), [código](https://github.com/python-pillow/Pillow) |
| file_picker ^13.1.0; [pubspec](../../frontend/campusmarket/pubspec.yaml) | Selector de archivos Web/Android para fotos reales. Registro pub.dev contiene versión 13.1.0, repository vicajilau/flutter_file_picker/packages/file_picker, SDK >=3.10.0 <4.0.0 y Flutter >=3.38.0 | [Registro JSON](https://pub.dev/api/packages/file_picker), [paquete](https://pub.dev/packages/file_picker/versions/13.1.0), [lockfile](../../frontend/campusmarket/pubspec.lock) |
| integration_test; dev_dependency del SDK | Verifica el flujo del consumidor con API/MySQL, navegador y emulador. Se obtiene del SDK Flutter, no de un nombre sugerido descargado de un registro externo | [pubspec oficial Flutter 3.47.3](https://github.com/flutter/flutter/blob/3.47.3/packages/integration_test/pubspec.yaml) |

Los tres registros/versiones externos fueron consultados de nuevo al preparar
este complemento: HTTP 200 y nombre/versión/source concordantes. El paquete del
SDK fue leído en el repositorio oficial Flutter, ref 3.47.3. La identidad se
contrasta con el proyecto mantenedor; encontrar un nombre en un registro no basta.

pytest==9.1.1 y httpx==0.28.1 ya existían: se trasladan a
[requirements-dev.txt](../../backend/requirements-dev.txt), no se incorporan al
runtime de producción. Ruff y Gitleaks son herramientas de CI, descritas en el
[workflow](../../.github/workflows/backend-tests.yml); integration_test solo se
usa en verificación. No se añade un proveedor generativo ni pytest-cov.

Instalación, resolución y compatibilidad ejecutable del estado contrastado:
[Backend](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37173110650),
[Flutter](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37173110679),
[Web/Android](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37173110670).
No afirmar que la consulta del registro acredita ausencia absoluta de vulnerabilidades.

### Alcance actual del barrido de secretos

[Backend del SHA contrastado](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37173110650/job/111349967672)
concluyó success en «Auditar secretos del historial y checkout con Gitleaks».
Gitleaks 8.30.1 se descarga del mantenedor con SHA-256 fijado, usa --redact,
escanea el checkout (también docs/ejemplos) y el intervalo
`bfe3222c1e29dddc404560cdd9d61095d4bdb3fe..HEAD`. Informes en artefacto
`secretos-7856416795bb4accdf9d05e01adb470654875e56`.

La lectura identifica las contraseñas constantes de MySQL CI como datos
efímeros de ese job; las credenciales de producción se suministran por Environment
y no se reproducen. Nombres de variables, secretos referenciados, hashes de
commits y marcadores de ejemplo no son valores productivos.

Este éxito no cubre por sí mismo los commits anteriores a bfe3222c.
No se declara limpio todo el historial del semestre por ampliar el alcance
de esta frase: conservar el barrido histórico y repetir el del CONTRATO antes
de una declaración global. El nuevo commit documental debe superar también
la auditoría de CI una vez integrado.
