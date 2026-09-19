# CampusMarket

Marketplace universitario para la publicación, consulta, venta y alquiler de
productos dentro de la comunidad universitaria.

## Integrantes

- Joshua Tenorio Alvarez
- Camilo Martinez Berrio
- Nilver Garcia Pimentel

---

# Estado arquitectónico vigente

CampusMarket adopta un **monolito modular**, decisión registrada en:

[ADR-0001 - Usar monolito modular](docs/adr/0001-usar-monolito-modular.md)

Las capacidades principales se organizan alrededor de los contextos:

- `usuarios`
- `publicaciones`
- `catalogo`
- `administracion`

Actualmente la capacidad funcional materializada con mayor profundidad es:

**Gestión de Publicaciones**

El recorrido ejecutable vigente es:

```text
Flutter Web
    ↓ HTTP/JSON
    ↓ contrato OpenAPI
FastAPI
    ↓
router.py
    ↓
service.py
    ↓
repository.py
    ↓ PyMySQL / SQL
MySQL
```

La persistencia vigente es **MySQL**.

SQLite permanece únicamente como parte de la historia arquitectónica del
primer corte, principalmente S4 y S5.

La migración fue realizada posteriormente como respuesta a una observación
docente y se encuentra registrada en:

[ADR-0004 - Migrar persistencia de SQLite a MySQL](docs/adr/0004-migrar-persistencia-a-mysql.md)

---

# Tecnologías actuales

| Elemento | Tecnología |
|---|---|
| Frontend | Flutter / Dart |
| Backend | FastAPI / Python |
| Estilo arquitectónico | Monolito modular |
| Persistencia vigente | MySQL |
| Driver de persistencia | PyMySQL |
| API | HTTP/JSON REST |
| Contrato de API | OpenAPI 3.1 |
| Versión del contrato | `1.0.0` |
| Pruebas backend | pytest |
| Integración continua | GitHub Actions |
| Análisis estático | SonarQube Cloud |
| Diagramas arquitectónicos | PlantUML |

La integración entre Flutter y FastAPI es actualmente **síncrona** mediante
HTTP/JSON.

La decisión se documenta en:

[ADR-0003 - Integración síncrona HTTP/JSON](docs/adr/0003-usar-integracion-sincrona-http-json.md)

---

# Requisitos previos

Para ejecutar el estado vigente del proyecto se requiere:

- Python 3.12;
- Flutter disponible en `PATH`;
- Google Chrome;
- MySQL disponible;
- dependencias Python instaladas;
- configuración de conexión a MySQL mediante variables de entorno.

Desde la raíz del repositorio:

```bash
pip install -r backend/requirements.txt
```

Las dependencias del backend se encuentran en:

[`backend/requirements.txt`](backend/requirements.txt)

---

# Configuración de MySQL

La aplicación utiliza las siguientes variables de entorno:

```text
CAMPUSMARKET_DB_HOST
CAMPUSMARKET_DB_PORT
CAMPUSMARKET_DB_USER
CAMPUSMARKET_DB_PASSWORD
CAMPUSMARKET_DB_NAME
```

Ejemplo para PowerShell:

```powershell
$env:CAMPUSMARKET_DB_HOST="localhost"
$env:CAMPUSMARKET_DB_PORT="3306"
$env:CAMPUSMARKET_DB_USER="campusmarket_app"
$env:CAMPUSMARKET_DB_PASSWORD="<PASSWORD_LOCAL>"
$env:CAMPUSMARKET_DB_NAME="campusmarket"
```

Las credenciales reales no deben almacenarse en el repositorio.

El archivo `.env`, cuando se utiliza localmente, se mantiene fuera del control
de versiones mediante `.gitignore`.

El acceso productivo a MySQL se encuentra encapsulado en:

[`backend/app/publicaciones/repository.py`](backend/app/publicaciones/repository.py)

---

# Arranque del prototipo

## Windows

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_s4.ps1
```

## Linux/macOS

```bash
bash scripts/run_s4.sh
```

Los scripts permiten iniciar:

- Backend FastAPI: `http://localhost:8000`
- Frontend Flutter Web: `http://localhost:3000`

> **Importante:** estos scripts no levantan una instancia MySQL.
> Antes de iniciar CampusMarket, MySQL debe estar disponible y las variables de
> conexión deben encontrarse configuradas.

La evidencia histórica del arranque con un solo comando se encuentra en:

[Arranque con un solo comando](docs/evidencias/arranque-un-comando-2026-09-04.md)

Esta evidencia corresponde al estado del primer corte.

---

# Evidencia auditable S7 para revisión automática

La evidencia completa de S7 se encuentra en:

[`docs/evidencias/evidencia-s7-2026-09-15.md`](docs/evidencias/evidencia-s7-2026-09-15.md)

Esta sección concentra las rutas y ejecuciones que utiliza la ficha S7 para
verificar el estado del repositorio.

| Comprobación | Evidencia |
|---|---|
| Contrato OpenAPI ejecutable | [`contracts/openapi-v1.json`](contracts/openapi-v1.json) |
| OpenAPI / versión | OpenAPI `3.1.0`, API `1.0.0` |
| Schemas del contrato | `HealthResponse`, `PublicacionCreate`, `Publicacion`, `ErrorResponse`, `HTTPValidationError`, `ValidationError` |
| Implementación `POST /publicaciones` | [`backend/app/publicaciones/router.py`](backend/app/publicaciones/router.py) |
| Implementación `GET /publicaciones` | [`backend/app/publicaciones/router.py`](backend/app/publicaciones/router.py) |
| Implementación `GET /health` | [`backend/app/main.py`](backend/app/main.py) |
| Prueba contractual | [`backend/tests/test_contrato_openapi.py`](backend/tests/test_contrato_openapi.py) |
| Workflow CI | [`.github/workflows/backend-tests.yml`](.github/workflows/backend-tests.yml) |
| Run oficial verde vigente | https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/35291809164 |
| Commit vigente revisado | `5bedc833c6324cba316cefd5ccc39d1269f3b984` |
| Run rojo por incompatibilidad | https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/34934077733 |
| Trazabilidad de aspectos | [`docs/aspectos.md`](docs/aspectos.md) |
| Registro de IA | [`docs/ia.md`](docs/ia.md) |
| ADR de integración | [`docs/adr/0003-usar-integracion-sincrona-http-json.md`](docs/adr/0003-usar-integracion-sincrona-http-json.md) |
| arc42 sección 6 | [`docs/arc42/06-vista-ejecucion.md`](docs/arc42/06-vista-ejecucion.md) |
| C4 Nivel 2 | [`docs/c4/02-contenedores.puml`](docs/c4/02-contenedores.puml) |

## Cotejo mínimo contrato ↔ código

La ficha S7 exige comprobar dos rutas desde el contrato hacia el código y una
ruta desde el código hacia el contrato.

```text
Contrato POST /publicaciones
→ backend/app/publicaciones/router.py
→ operation_id = crearPublicacion

Contrato GET /publicaciones
→ backend/app/publicaciones/router.py
→ operation_id = listarPublicaciones

Código GET /health
→ backend/app/main.py
→ contrato OpenAPI GET /health
→ operationId = consultarSalud
```

La prueba automatizada:

[`backend/tests/test_contrato_openapi.py`](backend/tests/test_contrato_openapi.py)

compara adicionalmente la superficie OpenAPI generada por FastAPI con el
contrato versionado.

---

## Historial del contrato

El contrato está versionado en:

```text
contracts/openapi-v1.json
```

La versión declarada es:

```text
OpenAPI 3.1.0
API 1.0.0
```

El contrato fue incorporado al historial mediante:

```text
485249a4ac8be1f12e5bfc4c0b54af744e51e5d6
Implementar contrato OpenAPI y prueba de contrato S7
```

El historial puede reproducirse mediante:

```bash
git log --format='%h %cI %s' -- contracts/openapi-v1.json
```

---

## Prueba contractual en CI

El workflow:

[`.github/workflows/backend-tests.yml`](.github/workflows/backend-tests.yml)

ejecuta explícitamente:

```yaml
- name: Ejecutar prueba de contrato OpenAPI
  run: python -m pytest backend/tests/test_contrato_openapi.py -q
```

La ejecución oficial vigente sobre `master` corresponde a:

```text
Run #95
Commit: 5bedc833c6324cba316cefd5ccc39d1269f3b984
Rama: master
Conclusión: success
```

URL:

https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/35291809164

El Run #95 fue reejecutado el 18/09/2026 y volvió a finalizar correctamente,
confirmando el estado estable del pipeline sobre el mismo commit.

La ejecución incluye:

- disponibilidad del servicio MySQL de CI;
- pruebas funcionales y arquitectónicas;
- verificación de modularidad;
- ejecución explícita de la prueba contractual OpenAPI.

Esto demuestra que la prueba de contrato no solamente existe en el repositorio:
forma parte de la integración continua del estado vigente de `master`.

---

## Evidencia de fallo ante incompatibilidad

También se demostró que la prueba contractual puede fallar cuando el proveedor
rompe el contrato.

Cambio temporal:

```diff
- operation_id="crearPublicacion",
+ operation_id="registrarPublicacion",
```

Run rojo:

https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/34934077733

Resultado:

```text
conclusion: failure
FAILED test_proveedor_fastapi_cumple_el_contrato_versionado
1 failed, 10 passed, 2 warnings
Process completed with exit code 1.
```

La incompatibilidad fue restaurada posteriormente y las ejecuciones siguientes
regresaron a verde.

Evidencia detallada:

[`docs/evidencias/fallo-contrato-s7-2026-09-15.md`](docs/evidencias/fallo-contrato-s7-2026-09-15.md)

---

## Evidencia transversal

La matriz de trazabilidad se encuentra en:

[`docs/aspectos.md`](docs/aspectos.md)

y utiliza las ocho columnas requeridas:

```text
ID · Aspecto · Requisito · C4 · ADR · Código · Pruebas · Evidencia
```

El registro de uso de inteligencia artificial se encuentra en:

[`docs/ia.md`](docs/ia.md)

y documenta herramienta, uso, verificación del equipo y propuestas rechazadas
con su justificación técnica.

---

## Estado de SonarQube Cloud

CampusMarket utiliza el proyecto oficial público de SonarQube Cloud:

```text
Project Key: ISCOUTB_AS_202620_PROYECTO_CAMPUSMARKET
Organization Key: isco-utb
Quality Gate: Passed
```

Análisis público:

https://sonarcloud.io/dashboard?id=ISCOUTB_AS_202620_PROYECTO_CAMPUSMARKET&pullRequest=41

La configuración versionada del análisis se encuentra en:

[`.sonarcloud.properties`](.sonarcloud.properties)

El proyecto oficial presenta un **Quality Gate aprobado** y corresponde a la
organización `isco-utb` utilizada por el curso.

La comprobación transversal definida en `CONTRATO.md` exige además que el
scanner de SonarQube Cloud sea invocado explícitamente desde GitHub Actions y
que exista un run exitoso de CI asociado a ese análisis.

Actualmente el pipeline estable de `master` no ejecuta directamente el scanner
de SonarQube Cloud.

La incorporación del scanner requiere una credencial con autorización para
ejecutar análisis sobre el proyecto oficial de la organización `isco-utb`.

El equipo no dispone actualmente de esa autorización sobre el proyecto oficial.
Por esta razón, no se mantiene en `master` una configuración del scanner que
dejaría el pipeline principal deliberadamente en estado fallido.

El estado verificable actualmente es:

```text
Proyecto oficial SonarQube Cloud: verificado
Project Key: ISCOUTB_AS_202620_PROYECTO_CAMPUSMARKET
Organization Key: isco-utb
Quality Gate público: Passed
Configuración .sonarcloud.properties: versionada
Pipeline vigente de master: success
GitHub Actions Run #95: success
Scanner explícito en workflow de master: pendiente
Run exitoso del scanner desde CI: pendiente
Restricción actual: autorización para ejecutar análisis sobre isco-utb
```

Por tanto, este punto transversal no se declara completamente cerrado.

Para completar la conformidad se requiere:

1. una credencial con autorización para ejecutar análisis sobre el proyecto
   oficial `ISCOUTB_AS_202620_PROYECTO_CAMPUSMARKET`;
2. invocar el scanner desde `.github/workflows/backend-tests.yml`;
3. obtener un run exitoso del pipeline que ejecute dicho scanner; y
4. conservar la URL pública del análisis con Quality Gate aprobado.

Mientras esa autorización no se encuentre disponible, CampusMarket conserva en
`master` el pipeline estable de pruebas funcionales, arquitectónicas y
contractuales.

---

# API de CampusMarket

Durante S7 se formalizó la interfaz entre:

**Frontend Flutter → Backend FastAPI**

La integración utiliza:

- HTTP;
- JSON;
- estilo REST;
- comunicación síncrona;
- contrato OpenAPI versionado.

El contrato fuente se encuentra en:

[`contracts/openapi-v1.json`](contracts/openapi-v1.json)

La guía asociada se encuentra en:

[`contracts/README.md`](contracts/README.md)

## Operaciones actualmente materializadas

| Método | Ruta | Propósito |
|---|---|---|
| `GET` | `/health` | Consultar disponibilidad del backend |
| `GET` | `/publicaciones` | Consultar publicaciones |
| `POST` | `/publicaciones` | Crear una publicación |

La API mantiene identificadores de operación estables para facilitar generación
de clientes y verificación de compatibilidad.

---

# Contrato OpenAPI y API-first

CampusMarket utiliza un contrato OpenAPI versionado como referencia explícita
de la interfaz entre consumidor y proveedor.

La relación es:

```text
Flutter
   ↓
HTTP/JSON
   ↓
Contrato OpenAPI
   ↓
FastAPI
```

La prueba:

[`backend/tests/test_contrato_openapi.py`](backend/tests/test_contrato_openapi.py)

compara el contrato versionado con el esquema generado por FastAPI.

La intención es detectar automáticamente cambios incompatibles como:

- eliminar una ruta;
- renombrar una operación;
- retirar un campo requerido;
- cambiar tipos;
- hacer obligatorio un campo previamente opcional;
- eliminar respuestas acordadas.

Durante S7 se realizó una demostración controlada de ruptura del contrato.

Evidencia:

[Demostración de cambio incompatible S7](docs/evidencias/fallo-contrato-s7-2026-09-15.md)

Después de restaurar la compatibilidad, el conjunto completo de pruebas volvió
a verde.

---

# Pruebas automatizadas

Desde la raíz:

```bash
python -m pytest backend/tests -q
```

Las pruebas principales incluyen:

- [`backend/tests/test_health.py`](backend/tests/test_health.py)
- [`backend/tests/test_publicaciones_vertical.py`](backend/tests/test_publicaciones_vertical.py)
- [`backend/tests/test_modularidad_s6.py`](backend/tests/test_modularidad_s6.py)
- [`backend/tests/test_contrato_openapi.py`](backend/tests/test_contrato_openapi.py)

El conjunto actual verifica:

- disponibilidad del backend mediante `/health`;
- creación de publicaciones;
- consulta de publicaciones;
- persistencia real en MySQL;
- respuesta HTTP `201` en creación válida;
- respuesta controlada HTTP `503` cuando la persistencia no está disponible;
- propiedad única del dato `publicaciones`;
- ausencia de escritura directa desde otros contextos;
- dirección interna:
  `router → service → repository → MySQL`;
- correspondencia entre contrato OpenAPI y proveedor FastAPI.

La evidencia vigente del pipeline se encuentra en el Run #95:

https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/35291809164

El pipeline finaliza correctamente con las pruebas funcionales,
arquitectónicas y contractuales.

---

# Verificación del frontend

Desde:

```bash
cd frontend/campusmarket
```

puede ejecutarse:

```bash
flutter analyze
```

Durante las verificaciones realizadas se obtuvo:

```text
No issues found!
```

---

# Integración continua

Las pruebas automatizadas se ejecutan mediante:

[`.github/workflows/backend-tests.yml`](.github/workflows/backend-tests.yml)

El pipeline actual:

1. obtiene el repositorio;
2. configura Python 3.12;
3. instala las dependencias;
4. levanta un servicio MySQL para CI;
5. configura los parámetros de conexión;
6. comprueba disponibilidad de MySQL;
7. ejecuta las pruebas funcionales y arquitectónicas;
8. ejecuta explícitamente la prueba de contrato OpenAPI.

De esta manera, la ejecución de CI reproduce también la dependencia vigente
sobre MySQL sin requerir credenciales locales del equipo.

El estado vigente de `master` se encuentra respaldado por:

```text
Run #95
Commit: 5bedc833c6324cba316cefd5ccc39d1269f3b984
Conclusión: success
```

https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/35291809164

---

# SonarQube Cloud

El análisis estático se mantiene en el proyecto oficial de CampusMarket en
**SonarQube Cloud**.

Configuración versionada:

[`.sonarcloud.properties`](.sonarcloud.properties)

Código fuente declarado para análisis:

- `backend/app`
- `frontend/campusmarket/lib`

Pruebas:

- `backend/tests`

Proyecto oficial:

```text
Project Key: ISCOUTB_AS_202620_PROYECTO_CAMPUSMARKET
Organization Key: isco-utb
```

Estado público verificado:

```text
Quality Gate: Passed
```

Dashboard:

https://sonarcloud.io/dashboard?id=ISCOUTB_AS_202620_PROYECTO_CAMPUSMARKET&pullRequest=41

El pipeline vigente de GitHub Actions permanece estable y exitoso sobre
`master`, incluyendo MySQL, pruebas funcionales, arquitectónicas y
contractuales.

La ejecución explícita del scanner de SonarQube Cloud desde ese workflow
permanece como pendiente transversal debido a que requiere una credencial
autorizada para ejecutar análisis sobre la organización `isco-utb`.

No se mantiene en `master` una integración conocida como fallida únicamente
para aparentar cumplimiento. El pendiente se encuentra documentado de forma
explícita hasta disponer de la autorización requerida.

---

# Diagramas C4

Los diagramas arquitectónicos se mantienen como **diagramas como código**
mediante PlantUML.

## C4 Nivel 1 - Contexto

- [Documentación](docs/c4/01-contexto.md)
- [Fuente PlantUML](docs/c4/01-contexto.puml)

Representa CampusMarket como un único sistema frente a:

- Estudiante;
- Administrador.

El cambio de SQLite a MySQL no modifica el Nivel 1 porque se trata de una
decisión interna del sistema.

---

## C4 Nivel 2 - Contenedores

- [Documentación](docs/c4/02-contenedores.md)
- [Fuente PlantUML](docs/c4/02-contenedores.puml)

El estado vigente representa:

```text
Frontend Web
    ↓ HTTP/JSON
Backend API
    ↓ PyMySQL / SQL
MySQL
```

Los contenedores vigentes son:

- **Frontend Web** — Flutter / Dart;
- **Backend API** — FastAPI / Python;
- **Persistencia** — MySQL.

SQLite se conserva únicamente como referencia histórica de los cortes
anteriores.

---

## C4 Nivel 3 - Componentes del Backend

- [Documentación](docs/c4/03-componentes-backend.md)
- [Fuente PlantUML](docs/c4/03-componentes-backend.puml)

El Nivel 3 realiza un acercamiento al contenedor **Backend API**.

La materialización vigente es:

```text
Frontend Web
     ↓
API de Publicaciones
     ↓
Servicio de Publicaciones
     ↓
Repositorio de Publicaciones
     ↓
MySQL
```

Correspondencia:

| Componente | Implementación |
|---|---|
| Entrada de aplicación | `backend/app/main.py` |
| API de Publicaciones | `backend/app/publicaciones/router.py` |
| Servicio de Publicaciones | `backend/app/publicaciones/service.py` |
| Repositorio de Publicaciones | `backend/app/publicaciones/repository.py` |
| Persistencia | MySQL |

Los contextos:

- `usuarios`;
- `catalogo`;
- `administracion`;

se mantienen como límites arquitectónicos definidos, pero todavía no se
declaran como capacidades funcionales completamente materializadas.

---

# S4 - Corte vertical inicial

> **Estado histórico:** esta sección describe la arquitectura existente durante
> S4 y no la persistencia vigente.

Durante S4 se construyó el primer corte vertical:

```text
Flutter Web
    ↓
FastAPI
    ↓
Gestión de Publicaciones
    ↓
SQLite
```

La funcionalidad permitía crear y consultar publicaciones.

La correspondencia principal era:

**Frontend**

- [`publicacion_form_page.dart`](frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart)
- [`publicaciones_api.dart`](frontend/campusmarket/lib/publicaciones/publicaciones_api.dart)

**Backend**

- [`router.py`](backend/app/publicaciones/router.py)
- [`service.py`](backend/app/publicaciones/service.py)
- [`repository.py`](backend/app/publicaciones/repository.py)

Esta evidencia se conserva porque representa la evolución real del proyecto.

---

# S5 - Reto arquitectónico del primer corte

> **Estado histórico:** S5 fue ejecutado mientras SQLite era la persistencia
> vigente.

## Restricción R-07

Durante el primer corte se definió:

**R-07 - Persistencia sin nueva infraestructura durante el primer corte**

Documentación:

[`docs/arc42/02-restricciones.md`](docs/arc42/02-restricciones.md)

La restricción establecía durante ese corte:

- mantener SQLite;
- conservar el monolito modular;
- no incorporar una base externa;
- no agregar colas;
- no agregar cachés distribuidas;
- no crear nuevos servicios desplegables.

---

## EC-05 - Degradación ante bloqueo temporal

El escenario analizó un bloqueo temporal de SQLite durante la creación de una
publicación.

### Línea base histórica

| Métrica | Resultado |
|---|---:|
| HTTP durante bloqueo | `500` |
| Tiempo durante bloqueo | `7.323 s` |
| Escritura parcial | `No` |
| Recuperación posterior | `201` |
| Tiempo de recuperación | `0.007 s` |

Evidencia:

[Línea base de bloqueo SQLite](docs/evidencias/linea-base-bloqueo-sqlite-2026-09-05.md)

---

## ADR-0002

La respuesta arquitectónica se documentó mediante:

[ADR-0002 - Manejo de bloqueo temporal de SQLite](docs/adr/0002-manejo-bloqueo-sqlite.md)

Durante S5 se aplicó:

- timeout SQLite de `0.5 s`;
- detección de `SQLITE_BUSY`;
- detección de `SQLITE_LOCKED`;
- HTTP `503 Service Unavailable`;
- ausencia de reintentos automáticos;
- preservación de la transacción;
- recuperación posterior.

### Resultado histórico

| Métrica | Línea base | Después | Umbral |
|---|---:|---:|---:|
| HTTP durante bloqueo | `500` | `503` | `503` |
| Tiempo durante bloqueo | `7.323 s` | `1.283 s` | `≤ 2 s` |
| Escritura parcial | `No` | `No` | `No` |
| Recuperación posterior | `201` | `201` | `201` |

Evidencia:

[Medición posterior a ADR-0002](docs/evidencias/medicion-bloqueo-sqlite-2026-09-06.md)

Estas mediciones no deben interpretarse como resultados obtenidos sobre MySQL.

El escenario se conserva como evidencia histórica de S5.

---

# S6 - Dominio y modularidad

Durante S6 se formalizaron:

- lenguaje ubicuo;
- contextos delimitados;
- relaciones entre contextos;
- propiedad única de datos;
- auditoría de modularidad;
- C4 Nivel 3;
- pruebas automáticas de reglas arquitectónicas.

Los contextos definidos son:

- **Gestión de Usuarios**
- **Gestión de Publicaciones**
- **Catálogo**
- **Administración**

Documentación:

- [Conceptos transversales](docs/arc42/08-conceptos-transversales.md)
- [C4 Nivel 3](docs/c4/03-componentes-backend.md)
- [Fuente PlantUML C4 Nivel 3](docs/c4/03-componentes-backend.puml)
- [Auditoría de modularidad](docs/evidencias/auditoria-modularidad-s6-2026-09-12.md)
- [Trazabilidad](docs/aspectos.md)

---

## Propiedad de datos

La regla arquitectónica adoptada es:

> Cada dato de dominio tiene un único módulo responsable de escribirlo.

La entidad actualmente materializada es:

```text
publicaciones
```

Su propietario es:

**Gestión de Publicaciones**

El escritor productivo permanece en:

[`backend/app/publicaciones/repository.py`](backend/app/publicaciones/repository.py)

Los campos persistidos son:

| Campo | Propietario |
|---|---|
| `id` | Gestión de Publicaciones |
| `titulo` | Gestión de Publicaciones |
| `descripcion` | Gestión de Publicaciones |
| `precio` | Gestión de Publicaciones |
| `modalidad` | Gestión de Publicaciones |
| `estado` | Gestión de Publicaciones |

La sustitución SQLite → MySQL no modifica esta propiedad arquitectónica.

---

## Verificación automática de modularidad

La prueba:

[`backend/tests/test_modularidad_s6.py`](backend/tests/test_modularidad_s6.py)

verifica actualmente:

- `repository.py` como único escritor productivo de `publicaciones`;
- ausencia de acceso directo desde otros contextos;
- ausencia de importación del repositorio interno por otros módulos;
- dirección:

```text
router → service → repository → MySQL
```

S6 definió la regla arquitectónica.

S7 y ADR-0004 conservaron la regla después de migrar la persistencia a MySQL.

---

# S7 - API-first e integración

Durante S7 se hizo explícita la interfaz entre:

**Frontend Flutter → Backend FastAPI**

Se definieron:

- contrato OpenAPI versionado;
- proveedor FastAPI;
- consumidor Flutter;
- comunicación síncrona HTTP/JSON;
- prueba automática de contrato;
- demostración de ruptura incompatible;
- correspondencia con C4 y arc42.

La trazabilidad principal es:

```text
ASP-07
   ↓
EC-06
   ↓
ADR-0003
   ↓
OpenAPI
   ↓
FastAPI
   ↓
test_contrato_openapi.py
```

La evidencia consolidada se encuentra en:

[`docs/evidencias/evidencia-s7-2026-09-15.md`](docs/evidencias/evidencia-s7-2026-09-15.md)

La matriz específica S7 dispone actualmente de evidencia identificada para sus
10 criterios.

---

## EC-06 - Compatibilidad del contrato

Documentación:

[`docs/arc42/10-escenarios-de-calidad.md`](docs/arc42/10-escenarios-de-calidad.md)

El escenario busca detectar cambios incompatibles antes de fusionarlos a la
rama principal.

La verificación automática utiliza:

[`backend/tests/test_contrato_openapi.py`](backend/tests/test_contrato_openapi.py)

---

## ADR-0003

[ADR-0003 - Integración síncrona HTTP/JSON](docs/adr/0003-usar-integracion-sincrona-http-json.md)

La decisión mantiene:

```text
Flutter ↔ FastAPI
```

mediante comunicación síncrona HTTP/JSON.

No se incorporan colas ni mensajería asíncrona porque las operaciones actuales
requieren confirmación inmediata y no existe evidencia que justifique esa
complejidad adicional.

---

# Evolución de persistencia - MySQL

Después del primer corte se recibió una observación docente indicando que la
persistencia debía evolucionar desde SQLite hacia MySQL.

La decisión se registra mediante:

[ADR-0004 - Migrar persistencia de SQLite a MySQL](docs/adr/0004-migrar-persistencia-a-mysql.md)

La migración:

**modifica**

- motor de persistencia;
- driver;
- configuración de conexión;
- pruebas de integración;
- CI;
- C4;
- arc42.

La migración **no modifica**:

- monolito modular;
- contextos delimitados;
- propietario de `publicaciones`;
- comunicación Flutter → FastAPI;
- contrato OpenAPI;
- dirección `router → service → repository`.

La persistencia vigente es:

```text
MySQL
```

y el acceso se realiza mediante:

```text
PyMySQL
```

---

# ADR vigentes e históricos

## Vigentes

- [ADR-0001 - Usar monolito modular](docs/adr/0001-usar-monolito-modular.md)
- [ADR-0003 - Integración síncrona HTTP/JSON](docs/adr/0003-usar-integracion-sincrona-http-json.md)
- [ADR-0004 - Migrar persistencia a MySQL](docs/adr/0004-migrar-persistencia-a-mysql.md)

## Histórico

- [ADR-0002 - Manejo de bloqueo temporal de SQLite](docs/adr/0002-manejo-bloqueo-sqlite.md)

ADR-0002 continúa siendo válido como evidencia del contexto en el que fue
tomado, pero no describe el motor de persistencia vigente.

---

# Trazabilidad arquitectónica

La trazabilidad general se mantiene en:

[`docs/aspectos.md`](docs/aspectos.md)

La cadena general es:

```text
Aspecto
   ↓
Requisito / escenario
   ↓
ADR
   ↓
C4
   ↓
Código
   ↓
Prueba
   ↓
Evidencia
```

A partir de S7 también se incorpora:

```text
Aspecto
   ↓
Contrato OpenAPI
   ↓
Proveedor FastAPI
   ↓
Prueba de contrato
```

Para la migración de persistencia:

```text
Observación docente
        ↓
ADR-0004
        ↓
C4
        ↓
arc42
        ↓
repository.py
        ↓
PyMySQL
        ↓
MySQL
        ↓
pruebas
```

---

# Documentación arc42

La documentación arquitectónica principal se encuentra en:

- [Secciones principales](docs/arc42/ARC42.md)
- [Sección 2 - Restricciones](docs/arc42/02-restricciones.md)
- [Sección 3 - Contexto](docs/arc42/03-contexto.md)
- [Sección 4 - Estrategia de solución](docs/arc42/04-estrategia-de-solucion.md)
- [Sección 5 - Bloques de construcción](docs/arc42/05-bloques-de-construccion.md)
- [Sección 6 - Vista de ejecución](docs/arc42/06-vista-ejecucion.md)
- [Sección 8 - Conceptos transversales](docs/arc42/08-conceptos-transversales.md)
- [Sección 9 - Decisiones](docs/arc42/09-decisiones.md)
- [Sección 10 - Escenarios de calidad](docs/arc42/10-escenarios-de-calidad.md)
- [Sección 12 - Glosario](docs/arc42/12-glosario.md)

---

# Registro de uso de Inteligencia Artificial

El registro se encuentra en:

[`docs/ia.md`](docs/ia.md)

El documento registra:

- fecha;
- herramienta utilizada;
- uso realizado;
- verificación realizada por el equipo;
- propuestas rechazadas;
- justificación del rechazo.

La IA se utiliza como apoyo para:

- análisis;
- estructuración documental;
- comparación de alternativas;
- revisión arquitectónica;
- elaboración de pruebas;
- auditoría de consistencia;
- trazabilidad.

El equipo conserva la responsabilidad sobre:

- decisiones arquitectónicas;
- código incorporado;
- pruebas ejecutadas;
- mediciones;
- validación del repositorio;
- aceptación o rechazo de propuestas.

Las respuestas de IA no se utilizan por sí solas como evidencia del sistema.

---

# Evidencias principales

## Primer corte / S1-S5

- [Correcciones S1-S4](correcciones.md)
- [Restricciones arquitectónicas](docs/arc42/02-restricciones.md)
- [ADR-0001](docs/adr/0001-usar-monolito-modular.md)
- [ADR-0002](docs/adr/0002-manejo-bloqueo-sqlite.md)
- [C4 Nivel 1](docs/c4/01-contexto.md)
- [C4 Nivel 2](docs/c4/02-contenedores.md)
- [Arranque histórico con un comando](docs/evidencias/arranque-un-comando-2026-09-04.md)
- [Línea base S5](docs/evidencias/linea-base-bloqueo-sqlite-2026-09-05.md)
- [Medición S5](docs/evidencias/medicion-bloqueo-sqlite-2026-09-06.md)

## S6

- [Conceptos transversales](docs/arc42/08-conceptos-transversales.md)
- [C4 Nivel 3](docs/c4/03-componentes-backend.md)
- [Fuente PlantUML C4 Nivel 3](docs/c4/03-componentes-backend.puml)
- [Auditoría de modularidad](docs/evidencias/auditoria-modularidad-s6-2026-09-12.md)
- [Prueba automática de modularidad](backend/tests/test_modularidad_s6.py)
- [Trazabilidad](docs/aspectos.md)

## S7

- [Evidencia consolidada S7](docs/evidencias/evidencia-s7-2026-09-15.md)
- [Contrato OpenAPI](contracts/openapi-v1.json)
- [Guía del contrato](contracts/README.md)
- [Prueba de contrato](backend/tests/test_contrato_openapi.py)
- [ADR-0003](docs/adr/0003-usar-integracion-sincrona-http-json.md)
- [ADR-0004](docs/adr/0004-migrar-persistencia-a-mysql.md)
- [Vista de ejecución](docs/arc42/06-vista-ejecucion.md)
- [C4 Nivel 2](docs/c4/02-contenedores.md)
- [C4 Nivel 3](docs/c4/03-componentes-backend.md)
- [Demostración de incompatibilidad](docs/evidencias/fallo-contrato-s7-2026-09-15.md)
- [Prueba funcional vigente](backend/tests/test_publicaciones_vertical.py)
- [Prueba de modularidad](backend/tests/test_modularidad_s6.py)
- [Registro de IA](docs/ia.md)
- [Run #95 vigente en master](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/35291809164)

---

# Estado actual del proyecto

La arquitectura vigente es:

```text
Flutter Web
    ↓ HTTP/JSON síncrono
    ↓ OpenAPI
FastAPI
    ↓
Gestión de Publicaciones
    ↓
Repository
    ↓ PyMySQL
MySQL
```

CampusMarket mantiene:

- monolito modular;
- cuatro contextos delimitados;
- propiedad única de los datos;
- C4 Nivel 1, 2 y 3;
- documentación arc42;
- contrato OpenAPI versionado;
- API HTTP/JSON síncrona;
- persistencia MySQL;
- pruebas funcionales;
- pruebas arquitectónicas;
- prueba automática de contrato;
- GitHub Actions con pipeline vigente exitoso;
- SonarQube Cloud oficial con Quality Gate público aprobado;
- trazabilidad arquitectónica;
- registro de uso de IA.

La integración explícita del scanner de SonarQube Cloud dentro de GitHub
Actions permanece como pendiente transversal por requerir autorización para
ejecutar análisis sobre la organización `isco-utb`.

Este pendiente no modifica el estado estable del pipeline vigente de `master`.

Los elementos todavía no completamente materializados se mantienen
explícitamente identificados como tales.

SQLite no se presenta como tecnología vigente.

Permanece únicamente dentro de la documentación histórica correspondiente al
momento en que realmente formó parte de la arquitectura.

La evolución SQLite → MySQL conserva las fronteras del monolito modular y hace
coincidir nuevamente:

```text
documentación
    ↓
C4
    ↓
ADR
    ↓
código
    ↓
pruebas
    ↓
CI
```

con el estado real de CampusMarket.

---

# Estado de cierre S7

El estado vigente de `master` utilizado como referencia de cierre es:

```text
Commit:
5bedc833c6324cba316cefd5ccc39d1269f3b984

GitHub Actions:
Run #95

Conclusión:
success
```

La matriz específica de S7 dispone de evidencia auditable para:

- contrato ejecutable y versionado;
- rutas y esquemas de datos;
- correspondencia contrato ↔ implementación;
- versión e historial del contrato;
- prueba contractual;
- ejecución contractual en CI;
- fallo ante cambio incompatible;
- ADR de estrategia de integración;
- vista de ejecución arc42;
- C4 Nivel 2 con protocolo y formato.

**Recuento específico S7: 10 de 10 criterios documentados con evidencia auditable.**

La única conformidad pendiente identificada en este cierre pertenece a la
matriz transversal de SonarQube Cloud:

```text
Quality Gate público: Passed
Configuración versionada: disponible
Scanner explícito en CI: pendiente
Run exitoso del scanner: pendiente
Motivo: autorización requerida sobre la organización isco-utb
```

Este pendiente se documenta explícitamente y no se declara como cumplimiento
hasta disponer de la evidencia exigida por `CONTRATO.md`.
