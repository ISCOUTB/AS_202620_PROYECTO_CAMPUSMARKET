# CampusMarket

Marketplace universitario para publicar, consultar, vender y alquilar productos dentro de la comunidad universitaria.

## Integrantes

- Joshua Tenorio Alvarez
- Camilo Martinez Berrio
- Nilver Garcia Pimentel

---

# Evolución y evidencias del proyecto

El README funciona como **puerta de entrada al estado vigente**. La evolución semanal no se repite completa aquí: se conserva mediante enlaces navegables a las decisiones, modelos, código, pruebas y evidencias que se fueron acumulando.

| Semana | Evolución principal | Evidencia / punto de entrada |
|---|---|---|
| **S1** | Problema, interesados, objetivos y trazabilidad inicial | [`docs/aspectos.md`](docs/aspectos.md), [`docs/ia.md`](docs/ia.md) |
| **S2** | Restricciones, escenarios de calidad, árbol de utilidad y C4 nivel 1 | [`docs/arc42/02-restricciones.md`](docs/arc42/02-restricciones.md), [`docs/arc42/10-escenarios-de-calidad.md`](docs/arc42/10-escenarios-de-calidad.md), [`docs/arc42/10-arbol-de-utilidad.md`](docs/arc42/10-arbol-de-utilidad.md), [`docs/c4/01-contexto.md`](docs/c4/01-contexto.md) |
| **S3** | Decisión del monolito modular y estrategia de solución | [`docs/adr/0001-usar-monolito-modular.md`](docs/adr/0001-usar-monolito-modular.md), [`docs/arc42/04-estrategia-de-solucion.md`](docs/arc42/04-estrategia-de-solucion.md) |
| **S4** | Corte vertical ejecutable Flutter → FastAPI → persistencia y CI | [`frontend/campusmarket/`](frontend/campusmarket/), [`backend/`](backend/), [`.github/workflows/backend-tests.yml`](.github/workflows/backend-tests.yml) |
| **S5** | Primera evaluación arquitectónica y evolución de persistencia hacia MySQL | [`docs/adr/0004-migrar-persistencia-a-mysql.md`](docs/adr/0004-migrar-persistencia-a-mysql.md), [`docs/arc42/09-decisiones.md`](docs/arc42/09-decisiones.md) |
| **S6** | Modularidad explícita, propiedad de datos y C4 nivel 3 | [`docs/evidencias/auditoria-modularidad-s6-2026-09-12.md`](docs/evidencias/auditoria-modularidad-s6-2026-09-12.md), [`docs/c4/03-componentes-backend.md`](docs/c4/03-componentes-backend.md), [`backend/tests/test_modularidad_s6.py`](backend/tests/test_modularidad_s6.py) |
| **S7** | Interfaces y contratos OpenAPI ejecutables | [`docs/evidencias/evidencia-s7-2026-09-15.md`](docs/evidencias/evidencia-s7-2026-09-15.md), [`contracts/openapi-v1.json`](contracts/openapi-v1.json), [`backend/tests/test_contrato_openapi.py`](backend/tests/test_contrato_openapi.py) |
| **S8** | Despliegue, operación, health check e infraestructura como código | [`docs/evidencias/evidencia-s8-2026-09-27.md`](docs/evidencias/evidencia-s8-2026-09-27.md), [`docs/arc42/07-vista-despliegue.md`](docs/arc42/07-vista-despliegue.md), [`infra/main.bicep`](infra/main.bicep) |
| **S9** | Catálogo materializado, verificación con IA, medición EC-01 y auditoría de erosión/dependencias | [`docs/evidencias/evidencia-s9-2026-10-01.md`](docs/evidencias/evidencia-s9-2026-10-01.md), [`docs/evidencias/evidencia-ec01-catalogo-s9-2026-10-01.md`](docs/evidencias/evidencia-ec01-catalogo-s9-2026-10-01.md), [`docs/evidencias/auditoria-s9-dependencias-secretos-2026-10-01.md`](docs/evidencias/auditoria-s9-dependencias-secretos-2026-10-01.md) |
| **Evolución posterior a S9** | Marketplace responsive, gestión de publicaciones propias e imágenes | [`docs/adr/0011-gestionar-imagenes-de-publicaciones.md`](docs/adr/0011-gestionar-imagenes-de-publicaciones.md), [`docs/aspectos.md`](docs/aspectos.md), [`backend/tests/test_gestion_publicaciones.py`](backend/tests/test_gestion_publicaciones.py) |

Para una revisión automática o manual, la ruta recomendada es:

```text
README
  ↓
docs/aspectos.md
  ↓
escenario de calidad / C4 / ADR
  ↓
código
  ↓
prueba ejecutable
  ↓
medición o evidencia
```

Así se conserva la historia del proyecto sin duplicar en el README el contenido completo de cada evidencia semanal.

---

# Estado arquitectónico vigente

CampusMarket utiliza un **monolito modular** en el backend.

Decisión principal:

- [ADR-0001 - Usar monolito modular](docs/adr/0001-usar-monolito-modular.md)

Contextos delimitados:

- `usuarios`;
- `publicaciones`;
- `catalogo`;
- `administracion`.

La persistencia vigente es **MySQL** y el acceso productivo se concentra en el contexto Publicaciones mediante PyMySQL.

La arquitectura lógica vigente es:

```text
Flutter Web / Android
        ↓ HTTP/JSON
        ↓ contrato OpenAPI
      FastAPI
        ├── Catálogo
        │      ↓ capacidad explícita de lectura
        └── Publicaciones
                 ↓
              service.py
                 ↓
              repository.py
                 ↓ PyMySQL
                MySQL
```

Reglas de frontera verificadas:

- `publicaciones` mantiene la propiedad de escritura de `publicaciones`;
- `catalogo` no importa `publicaciones.repository`;
- `catalogo` no usa PyMySQL directamente;
- `catalogo` consume capacidades de lectura expuestas por Publicaciones;
- Flutter no accede directamente a la base de datos;
- la dirección de Publicaciones permanece `router → service → repository → MySQL`.

La modularidad se verifica automáticamente mediante:

- [`backend/tests/test_modularidad_s6.py`](backend/tests/test_modularidad_s6.py)
- [`backend/tests/test_erosion_s9.py`](backend/tests/test_erosion_s9.py)

---

# Estado funcional vigente

CampusMarket materializa actualmente:

- Inicio responsive;
- Catálogo de publicaciones;
- búsqueda por texto;
- filtros por modalidad, estado y rango de precio;
- detalle de publicación;
- creación de publicaciones desde Flutter;
- carga de hasta tres imágenes por publicación;
- imagen principal y galería;
- listado de publicaciones propias;
- edición de publicaciones;
- cambio de estado operativo `disponible`, `reservado` y `vendido`;
- eliminación de publicaciones;
- persistencia MySQL;
- contrato OpenAPI ejecutable;
- health check y degradación controlada cuando la persistencia no está disponible.

El flujo fue verificado tanto en Flutter Web como en Android.

## Limitación vigente de identidad

Las operaciones de publicaciones propias utilizan actualmente `propietario_id = 1` como identidad temporal del prototipo.

Esto **no representa autenticación real**.

Por tanto:

- no se declara implementado un login real;
- no se declara EC-02 completamente satisfecho;
- Gestión de Usuarios continúa pendiente de materialización completa.

---

# Catálogo y S9

El aspecto **ASP-01 - Consulta y búsqueda de productos** fue materializado durante S9.

Decisión:

- [ADR-0009 - Materializar catálogo sin romper fronteras](docs/adr/0009-materializar-catalogo-sin-romper-fronteras.md)

Código principal:

- [`backend/app/catalogo/router.py`](backend/app/catalogo/router.py)
- [`backend/app/catalogo/service.py`](backend/app/catalogo/service.py)
- [`frontend/campusmarket/lib/catalogo/`](frontend/campusmarket/lib/catalogo/)

Pruebas:

- [`backend/tests/test_catalogo.py`](backend/tests/test_catalogo.py)
- [`backend/tests/test_ec01_catalogo.py`](backend/tests/test_ec01_catalogo.py)
- [`backend/tests/test_erosion_s9.py`](backend/tests/test_erosion_s9.py)

Evidencia:

- [`docs/evidencias/evidencia-s9-2026-10-01.md`](docs/evidencias/evidencia-s9-2026-10-01.md)
- [`docs/evidencias/evidencia-ec01-catalogo-s9-2026-10-01.md`](docs/evidencias/evidencia-ec01-catalogo-s9-2026-10-01.md)

La medición S9 de EC-01 registró 10/10 búsquedas dentro del umbral de 2 segundos con 1.000 publicaciones controladas. Esa medición corresponde al routing HTTP, lógica de búsqueda y serialización bajo carga controlada; no se presenta como una medición extremo a extremo de red de producción.

---

# Imágenes de publicaciones

La estrategia de imágenes se documenta mediante:

- [ADR-0011 - Gestionar imágenes de publicaciones](docs/adr/0011-gestionar-imagenes-de-publicaciones.md)

Reglas principales:

- máximo tres imágenes por publicación;
- primera imagen como principal;
- orden determinista;
- formatos JPG, JPEG, PNG y WEBP;
- máximo 5 MiB por imagen;
- MySQL conserva metadatos y referencias, no BLOB/Base64;
- `catalogo` obtiene las imágenes mediante Publicaciones;
- en desarrollo local los archivos se sirven desde `/uploads`.

El almacenamiento local de archivos es una solución de desarrollo. Antes de llevar esta capacidad a un despliegue productivo en infraestructura con filesystem no persistente debe utilizarse almacenamiento de objetos persistente, manteniendo MySQL para metadatos y referencias.

---

# Contrato API

Contrato versionado:

- [`contracts/openapi-v1.json`](contracts/openapi-v1.json)

Prueba contractual:

- [`backend/tests/test_contrato_openapi.py`](backend/tests/test_contrato_openapi.py)

La prueba compara el contrato versionado con la superficie OpenAPI generada por FastAPI y detecta divergencias en rutas, métodos, `operationId`, esquemas, campos requeridos y respuestas.

Operaciones materializadas incluyen, entre otras:

```text
GET    /health
POST   /publicaciones
GET    /publicaciones
GET    /publicaciones/mias
PUT    /publicaciones/{publication_id}
PATCH  /publicaciones/{publication_id}/estado
DELETE /publicaciones/{publication_id}
POST   /publicaciones/{publication_id}/imagenes
GET    /catalogo
GET    /catalogo/{publication_id}
```

---

# Verificación vigente al cierre del PR #47

La verificación local previa a integración del 3 de octubre de 2026 terminó con:

```text
python -m pytest backend/tests -q
36 passed, 2 warnings

python -m pytest backend/tests/test_contrato_openapi.py -q
3 passed

flutter analyze frontend/campusmarket
No issues found!

git diff --check
sin errores
```

El PR #47 (`Producto Marketplace UI - catálogo, gestión e imágenes`) fue integrado a `master` después de que GitHub Actions y SonarQube Cloud finalizaran en verde. El merge quedó registrado en el commit `cd7e029ded6ad33bfff0ff33557bf8efbd34f50f`.

Los dos warnings locales corresponden a deprecaciones de dependencias y no a fallos funcionales de la suite.

---

# Tecnologías vigentes

| Elemento | Tecnología |
|---|---|
| Frontend | Flutter / Dart |
| Plataformas verificadas | Web y Android |
| Backend | FastAPI / Python 3.12 |
| Servidor ASGI | Uvicorn |
| Estilo arquitectónico | Monolito modular |
| Persistencia | MySQL 8.4 |
| Driver | PyMySQL |
| API | REST / HTTP(S) / JSON |
| Contrato | OpenAPI 3.1 |
| Pruebas | pytest |
| Análisis estático | Ruff / `flutter analyze` |
| Integración continua | GitHub Actions |
| Calidad | SonarQube Cloud |
| IaC | Azure Bicep |
| Frontend público histórico S8 | GitHub Pages |
| Backend público histórico S8 | Azure App Service |
| Base de datos pública histórica S8 | Azure Database for MySQL Flexible Server |
| Diagramas | PlantUML |

---

# Reproducción local

## Backend

Requisitos:

- Python 3.12;
- MySQL disponible;
- dependencias instaladas;
- variables de entorno configuradas.

Instalación:

```bash
pip install -r backend/requirements.txt
```

Ejemplo de configuración PowerShell:

```powershell
$env:CAMPUSMARKET_DB_HOST="localhost"
$env:CAMPUSMARKET_DB_PORT="3306"
$env:CAMPUSMARKET_DB_USER="campusmarket_app"
$env:CAMPUSMARKET_DB_PASSWORD="<PASSWORD_LOCAL>"
$env:CAMPUSMARKET_DB_NAME="campusmarket"
$env:CAMPUSMARKET_DB_SSL="false"
```

Nunca versionar una credencial real.

Ejecución:

```bash
python -m uvicorn backend.app.main:app --reload
```

Backend local:

```text
http://localhost:8000
```

Health:

```text
http://localhost:8000/health
```

## Frontend Web

```bash
cd frontend/campusmarket
flutter analyze
flutter run -d chrome
```

## Android Emulator

Con backend ejecutándose en el host:

```bash
cd frontend/campusmarket
flutter run -d emulator-5554 --dart-define=CAMPUSMARKET_API_BASE_URL=http://10.0.2.2:8000
```

`10.0.2.2` permite al emulador Android acceder al host local.

---

# Despliegue S8

Durante S8 se desplegó una línea base pública con:

```text
GitHub Pages → Azure App Service → Azure Database for MySQL
```

Frontend:

```text
https://nnigarp.github.io/AS_202620_PROYECTO_CAMPUSMARKET/
```

Backend:

```text
https://campusmarket-s8-api-nilver.azurewebsites.net
```

Health:

```text
https://campusmarket-s8-api-nilver.azurewebsites.net/health
```

Infraestructura como código:

- [`infra/main.bicep`](infra/main.bicep)

La plantilla declara App Service, Azure Database for MySQL Flexible Server y configuración dependiente del entorno. Las credenciales sensibles se suministran mediante configuración externa y parámetros seguros.

> Las URLs anteriores corresponden al despliegue verificado en S8. Las capacidades añadidas posteriormente y ya integradas en `master` no deben considerarse desplegadas públicamente hasta realizar un nuevo despliegue y verificar el mismo hash.

---

# Integración continua

Workflow:

- [`.github/workflows/backend-tests.yml`](.github/workflows/backend-tests.yml)

El pipeline configura Python y MySQL, instala dependencias, verifica la base de datos, ejecuta análisis estático, pruebas funcionales/arquitectónicas y la prueba contractual OpenAPI.

---

# Documentación arquitectónica

Puntos de entrada principales:

- [arc42](docs/arc42/ARC42.md)
- [C4 Nivel 1](docs/c4/01-contexto.md)
- [C4 Nivel 2](docs/c4/02-contenedores.md)
- [C4 Nivel 3](docs/c4/03-componentes-backend.md)
- [Aspectos y trazabilidad](docs/aspectos.md)
- [Uso de IA](docs/ia.md)
