# Evidencia S7 - Contrato de API y prueba de contrato

**Periodo:** 14-20/09/2026  
**Última actualización:** 18/09/2026  
**Proyecto:** CampusMarket

**Estado:** Evidencia S7 integrada y saneada a partir de la pasada temprana del revisor automático.

La implementación principal del contrato se incorporó mediante los PR #37 y #38.
Durante el cierre de S7 se realizaron además los ajustes de persistencia MySQL,
trazabilidad arquitectónica y documentación mediante los PR #40 y #41, junto
con el ajuste final del C4 Nivel 2.

El 17/09/2026 se reforzó esta evidencia para hacer explícitas y auditables las
comprobaciones solicitadas por la ficha S7: esquemas del contrato, cotejo
bidireccional contrato-implementación, historial Git del contrato, ejecución de
la prueba contractual en CI y evidencia de fallo ante un cambio incompatible.

El 18/09/2026 se realizó una verificación final sobre `master`. El estado vigente
corresponde al commit `5bedc833c6324cba316cefd5ccc39d1269f3b984`, y el
GitHub Actions Run #95 fue reejecutado sobre ese mismo hash con conclusión
`success`, conservando en verde las pruebas funcionales, arquitectónicas y
contractuales.

---

## Resultado

CampusMarket formaliza como API principal la integración síncrona entre el
Frontend Flutter Web y el Backend FastAPI.

El contrato OpenAPI `1.0.0` describe las operaciones actualmente implementadas,
sus cuerpos, respuestas y esquemas de datos.

La prueba automatizada compara el contrato versionado con la superficie OpenAPI
generada por FastAPI y se ejecuta mediante un paso explícito de GitHub Actions.

Además, se verificó experimentalmente que la prueba falla cuando el proveedor
introduce un cambio incompatible y vuelve a verde después de restaurar la
compatibilidad.

---

## Matriz de cumplimiento S7

| Criterio | Estado | Evidencia auditable |
|---|---|---|
| Contrato ejecutable versionado | Cumple | [`contracts/openapi-v1.json`](../../contracts/openapi-v1.json): OpenAPI `3.1.0`, API `1.0.0` |
| Rutas y esquemas de datos | Cumple | El contrato contiene `paths` y `components.schemas`: `HealthResponse`, `PublicacionCreate`, `Publicacion`, `ErrorResponse`, `HTTPValidationError` y `ValidationError` |
| Correspondencia contrato-API | Cumple | Cotejo explícito de `POST /publicaciones`, `GET /publicaciones` y `GET /health` contra `router.py` y `main.py`, complementado por `test_contrato_openapi.py` |
| Versión declarada e historial | Cumple | `info.version: 1.0.0`; incorporación del contrato en commit `485249a4ac8be1f12e5bfc4c0b54af744e51e5d6` |
| Prueba de contrato presente | Cumple | [`backend/tests/test_contrato_openapi.py`](../../backend/tests/test_contrato_openapi.py) |
| Pipeline ejecuta la prueba | Cumple | Paso `Ejecutar prueba de contrato OpenAPI` en `.github/workflows/backend-tests.yml`; Run #95 en `master` sobre `5bedc83` con conclusión `success` |
| Falla ante cambio incompatible | Cumple | Run rojo ante `crearPublicacion` → `registrarPublicacion` y prueba local complementaria `titulo` → `nombre` |
| ADR ligado a un escenario | Cumple | [`ADR-0003`](../adr/0003-usar-integracion-sincrona-http-json.md), ligado principalmente a EC-06, con alternativa asíncrona descartada y consecuencias documentadas |
| arc42 sección 6 | Cumple | [`docs/arc42/06-vista-ejecucion.md`](../arc42/06-vista-ejecucion.md), con flujos de creación, consulta e indisponibilidad |
| C4 Nivel 2 etiquetado | Cumple | [`docs/c4/02-contenedores.puml`](../c4/02-contenedores.puml) y [`docs/c4/02-contenedores.md`](../c4/02-contenedores.md), con comunicaciones etiquetadas |

**Recuento específico S7:** 10 de 10 criterios con evidencia identificada.

> Este recuento corresponde exclusivamente a la matriz específica de S7.
> La comprobación transversal de SonarQube Cloud se documenta por separado
> más adelante y mantiene un pendiente transversal por autorización para ejecutar análisis en la organización `isco-utb`.

---

# Evidencia auditable para el revisor automático

Esta sección concentra de forma explícita las comprobaciones descritas por la
ficha S7 y permite reproducirlas directamente contra el repositorio.

---

## 1. Contrato ejecutable, rutas y esquemas

Contrato fuente:

[`contracts/openapi-v1.json`](../../contracts/openapi-v1.json)

Información declarada:

```text
OpenAPI: 3.1.0
API: 1.0.0
```

Rutas actualmente contratadas:

```text
GET  /health
GET  /publicaciones
POST /publicaciones
```

El contrato no contiene únicamente un listado de endpoints. Incluye
`components.schemas` con los modelos utilizados por las operaciones:

```text
components.schemas
├── HealthResponse
├── PublicacionCreate
├── Publicacion
├── ErrorResponse
├── HTTPValidationError
└── ValidationError
```

Correspondencia de operaciones y esquemas:

| Operación | Entrada | Respuesta |
|---|---|---|
| `GET /health` | — | `200 HealthResponse` |
| `GET /publicaciones` | — | `200 Publicacion[]` |
| `POST /publicaciones` | `PublicacionCreate` | `201 Publicacion` |
| `POST /publicaciones` | datos inválidos | `422 HTTPValidationError` |
| `POST /publicaciones` | persistencia no disponible | `503 ErrorResponse` |

Campos contractuales principales de `PublicacionCreate`:

```text
titulo       string   minLength=3   maxLength=100
descripcion  string   minLength=3   maxLength=500
precio       number   exclusiveMinimum=0
modalidad    venta | alquiler
estado       nuevo | usado | reacondicionado
```

`Publicacion` conserva esos campos y agrega:

```text
id integer
```

---

## 2. Cotejo bidireccional contrato ↔ implementación

La ficha S7 solicita comprobar dos rutas desde el contrato hacia el código y
una ruta desde el código hacia el contrato.

### Contrato → código: `POST /publicaciones`

Contrato:

```text
POST /publicaciones
operationId: crearPublicacion
requestBody: PublicacionCreate
response 201: Publicacion
response 503: ErrorResponse
```

Implementación:

[`backend/app/publicaciones/router.py`](../../backend/app/publicaciones/router.py)

```python
@router.post(
    "",
    response_model=Publicacion,
    status_code=status.HTTP_201_CREATED,
    operation_id="crearPublicacion",
    summary="Crear una publicación",
)
```

El router tiene prefijo:

```python
router = APIRouter(prefix="/publicaciones", tags=["publicaciones"])
```

Por tanto, la operación implementada es:

```text
POST /publicaciones
```

**Resultado:** correspondencia verificada.

---

### Contrato → código: `GET /publicaciones`

Contrato:

```text
GET /publicaciones
operationId: listarPublicaciones
response 200: Publicacion[]
```

Implementación:

[`backend/app/publicaciones/router.py`](../../backend/app/publicaciones/router.py)

```python
@router.get(
    "",
    response_model=list[Publicacion],
    operation_id="listarPublicaciones",
    summary="Listar publicaciones",
)
```

Con el prefijo `/publicaciones`, la operación implementada es:

```text
GET /publicaciones
```

**Resultado:** correspondencia verificada.

---

### Código → contrato: `GET /health`

Implementación:

[`backend/app/main.py`](../../backend/app/main.py)

```python
@app.get(
    "/health",
    response_model=HealthResponse,
    operation_id="consultarSalud",
    summary="Consultar la salud del backend",
)
```

Contrato:

```text
GET /health
operationId: consultarSalud
response 200: HealthResponse
```

**Resultado:** correspondencia verificada.

---

### Verificación automatizada adicional

La correspondencia completa también se verifica mediante:

[`backend/tests/test_contrato_openapi.py`](../../backend/tests/test_contrato_openapi.py)

La prueba compara el contrato versionado con el OpenAPI generado por FastAPI,
de forma que una desincronización entre proveedor y contrato produce un fallo
automático.

---

## 3. Versión e historial Git del contrato

El contrato declara:

```json
"openapi": "3.1.0",
"info": {
  "title": "CampusMarket API",
  "version": "1.0.0"
}
```

El archivo versionado es:

```text
contracts/openapi-v1.json
```

Su incorporación al repositorio quedó registrada mediante:

```text
Commit:
485249a4ac8be1f12e5bfc4c0b54af744e51e5d6

Fecha:
2026-09-15

Mensaje:
Implementar contrato OpenAPI y prueba de contrato S7
```

Comando reproducible de historial:

```bash
git log --format='%h %cI %s' -- contracts/openapi-v1.json
```

La versión de la API se encuentra tanto en el contrato como en la aplicación
FastAPI, que declara:

```python
app = FastAPI(
    title="CampusMarket API",
    version="1.0.0",
)
```

---

## 4. Prueba de contrato ejecutada por el pipeline

Workflow:

[`.github/workflows/backend-tests.yml`](../../.github/workflows/backend-tests.yml)

La prueba de contrato se invoca explícitamente mediante:

```yaml
- name: Ejecutar prueba de contrato OpenAPI
  run: python -m pytest backend/tests/test_contrato_openapi.py -q
```

La verificación final del estado vigente de `master` corresponde a:

```text
Commit: 5bedc833c6324cba316cefd5ccc39d1269f3b984
Rama: master
GitHub Actions: Run #95
Conclusión: success
```

URL:

https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/35291809164

El Run #95 fue reejecutado el 18/09/2026 sobre el mismo hash y volvió a finalizar
con conclusión `success`.

Esto demuestra que la prueba contractual no solamente existe en el árbol:
forma parte de la integración continua del estado vigente de `master`.

Como antecedente, el commit `baeca7e`, utilizado por la pasada temprana del
revisor automático, también obtuvo un pipeline exitoso mediante el Run #93.

---

## 5. Evidencia de fallo ante cambio incompatible

Para comprobar que la prueba contractual puede detectar una ruptura real, se
introdujo temporalmente la siguiente mutación:

```diff
- operation_id="crearPublicacion",
+ operation_id="registrarPublicacion",
```

GitHub Actions terminó en rojo:

https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/34934077733

Datos de la ejecución:

```text
conclusion: failure
```

Resultado principal:

```text
FAILED test_proveedor_fastapi_cumple_el_contrato_versionado

Contrato: operationId = crearPublicacion
Proveedor: operationId = registrarPublicacion

1 failed, 10 passed, 2 warnings
Process completed with exit code 1.
```

La ejecución demuestra que la prueba no pasa incondicionalmente: una ruptura
del proveedor respecto al contrato hace fallar el pipeline.

Después se restauró:

```text
operationId = crearPublicacion
```

y las ejecuciones posteriores volvieron a verde.

La evidencia detallada se conserva en:

[`fallo-contrato-s7-2026-09-15.md`](./fallo-contrato-s7-2026-09-15.md)

---

## 6. Mutación local complementaria

También se realizó una segunda comprobación modificando temporalmente el
esquema del proveedor:

```diff
- titulo: str = Field(min_length=3, max_length=100)
+ nombre: str = Field(min_length=3, max_length=100)
```

Resultado:

```text
FAILED test_proveedor_fastapi_cumple_el_contrato_versionado

1 failed, 2 passed
exit code: 1
```

La mutación fue restaurada y no forma parte del código vigente.

---

# Operaciones contratadas

| Método | Ruta | Operación | Respuestas |
|---|---|---|---|
| `GET` | `/health` | `consultarSalud` | `200 HealthResponse` |
| `GET` | `/publicaciones` | `listarPublicaciones` | `200 Publicacion[]` |
| `POST` | `/publicaciones` | `crearPublicacion` | `201 Publicacion`, `422 HTTPValidationError`, `503 ErrorResponse` |

---

# Verificaciones ejecutadas

## Estado compatible inicial

Durante la implementación inicial del contrato se obtuvo:

```text
11 passed, 2 warnings
exit code: 0
```

Ejecución verde del fork con las pruebas separadas:

https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/34935043273

Ejecución oficial correspondiente al PR #38:

https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/34935516952

---

## Verificación posterior en `master`

Después de la integración del contrato, la migración de persistencia a MySQL y
el saneamiento documental de S7 se volvió a ejecutar el pipeline sobre la rama
principal.

La verificación final vigente es:

```text
commit: 5bedc833c6324cba316cefd5ccc39d1269f3b984
rama: master
GitHub Actions: Run #95
resultado: success
```

URL:

https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/35291809164

El Run #95 ejecuta el workflow vigente de `master`, que incluye:

```text
Verificación de conexión con MySQL
Pruebas funcionales y arquitectónicas
Prueba de contrato OpenAPI
```

El mismo Run #95 fue reejecutado el 18/09/2026 sobre `5bedc83` y volvió a
finalizar en verde.

Como antecedentes adicionales:

- Run #91 verificó la integración posterior de MySQL y las pruebas de S7;
- Run #93 verificó el commit `baeca7e` utilizado por la pasada temprana del
  revisor automático.

Por tanto, el estado actual de `master` conserva un pipeline estable y exitoso
para las pruebas automatizadas exigidas por la ficha S7.

---

# C4 Nivel 2

Durante el cierre del 16/09/2026 se revisó el C4 Nivel 2 para hacer explícita la
tecnología, protocolo o formato utilizado en cada comunicación.

Las relaciones vigentes son:

```text
Estudiante
    ↓
[HTTPS / Flutter Web]
    ↓
Frontend Web
```

```text
Administrador
    ↓
[HTTPS / Flutter Web]
    ↓
Frontend Web
```

```text
Frontend Web
    ↓
[HTTP / JSON síncrono]
    ↓
Backend API
```

```text
Backend API
    ↓
[PyMySQL / SQL]
    ↓
MySQL
```

Fuentes:

- [`docs/c4/02-contenedores.puml`](../c4/02-contenedores.puml)
- [`docs/c4/02-contenedores.md`](../c4/02-contenedores.md)

---

# Cliente generado

OpenAPI Generator `7.25.0` generó de forma reproducible un cliente Dart con:

- `crearPublicacion`;
- `listarPublicaciones`;
- `consultarSalud`.

El procedimiento se documenta en:

[`contracts/README.md`](../../contracts/README.md)

El cliente generado se utilizó como comprobación reproducible del contrato y no
se incorporó como segundo cliente productivo, porque
`publicaciones_api.dart` ya representa el cliente actual del corte vertical.

---

# Decisión y trade-off

Se mantiene la integración síncrona porque crear y consultar publicaciones
requiere una respuesta inmediata para el consumidor Flutter.

Se acepta como consecuencia el acoplamiento temporal entre Frontend y Backend.

Los modos de fallo se expresan mediante:

- HTTP `422`;
- HTTP `503`;
- errores de comunicación HTTP.

La alternativa asíncrona fue evaluada y descartada para el alcance actual
porque requeriría:

- estados pendientes;
- reintentos;
- idempotencia;
- tratamiento de duplicados;
- consistencia eventual;
- infraestructura adicional de mensajería.

No existe actualmente una necesidad arquitectónica que justifique introducir
esa complejidad.

La decisión está registrada en:

[`ADR-0003`](../adr/0003-usar-integracion-sincrona-http-json.md)

---

# Persistencia vigente

Durante el cierre de S7 la persistencia vigente de CampusMarket fue migrada de
SQLite a MySQL.

El acceso productivo se realiza mediante:

```text
FastAPI
   ↓
service.py
   ↓
repository.py
   ↓
PyMySQL / SQL
   ↓
MySQL
```

SQLite se conserva únicamente como evidencia histórica del primer corte y de
las mediciones realizadas durante S5.

La decisión de migración se encuentra registrada en:

[`ADR-0004`](../adr/0004-migrar-persistencia-a-mysql.md)

---

# Evidencia transversal del repositorio

## Tabla de aspectos

La trazabilidad transversal se mantiene en:

[`docs/aspectos.md`](../aspectos.md)

El archivo utiliza las ocho columnas requeridas por el contrato del curso:

```text
ID
Aspecto
Requisito
C4
ADR
Código
Pruebas
Evidencia
```

Para S7, la fila principal es `ASP-07 - Contrato ejecutable de API`, cuya
cadena de trazabilidad conecta:

```text
ASP-07
   ↓
EC-06
   ↓
C4 Nivel 2 / Vista de ejecución
   ↓
ADR-0003
   ↓
contracts/openapi-v1.json
   ↓
main.py / router.py
   ↓
test_contrato_openapi.py
   ↓
GitHub Actions
   ↓
fallo incompatible
   ↓
run verde
```

La evidencia navegable se encuentra directamente en la fila ASP-07 de
`docs/aspectos.md`.

---

## Registro de uso de IA

El registro se mantiene en:

[`docs/ia.md`](../ia.md)

La sección S7 registra, para cada uso:

- herramienta utilizada;
- uso realizado;
- verificación del equipo;
- qué se rechazó y por qué.

Entre los rechazos documentados se encuentran:

- inventar endpoints o eventos inexistentes;
- considerar Swagger automático como prueba contractual suficiente;
- incorporar un segundo cliente Dart productivo sin necesidad;
- conservar cambios incompatibles solamente para demostrar fallos;
- debilitar la prueba contractual para que una incompatibilidad pase.

El saneamiento posterior a la pasada temprana del revisor también fue registrado
el 17/09/2026 en `docs/ia.md`, incluyendo las verificaciones realizadas y las
propuestas rechazadas con su justificación técnica.

---

# Calidad y análisis estático

CampusMarket utiliza el proyecto oficial de SonarQube Cloud:

```text
ISCOUTB_AS_202620_PROYECTO_CAMPUSMARKET
```

Configuración versionada:

```text
.sonarcloud.properties
```

El análisis correspondiente al PR #41 reportó:

- Quality Gate: **Passed**;
- problemas nuevos: **0**;
- problemas aceptados nuevos: **0**;
- Security Hotspots nuevos: **0**;
- duplicación en código nuevo: **0.0 %**.

PR:

https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/pull/41

Análisis público:

https://sonarcloud.io/dashboard?id=ISCOUTB_AS_202620_PROYECTO_CAMPUSMARKET&pullRequest=41

---

## Estado transversal pendiente de saneamiento

La pasada temprana del revisor automático señaló que, aunque SonarQube Cloud
dispone de análisis público y Quality Gate aprobado, el workflow vigente
`.github/workflows/backend-tests.yml` no invoca explícitamente un scanner de
SonarQube Cloud.

El proyecto oficial verificado es:

```text
Project Key: ISCOUTB_AS_202620_PROYECTO_CAMPUSMARKET
Organization Key: isco-utb
Quality Gate: Passed
```

La configuración del análisis permanece versionada en:

```text
.sonarcloud.properties
```

El equipo puede consultar públicamente el proyecto oficial y su Quality Gate.
Sin embargo, la credencial disponible para el equipo no está autorizada para
publicar un análisis CI sobre el proyecto de la organización `isco-utb`.

Durante una validación temporal, realizada fuera de `master`, el scanner fue
invocado desde GitHub Actions, pero SonarQube Cloud rechazó la publicación del
análisis por autorización. Esa ejecución no se conserva como evidencia de
cumplimiento y no fue incorporada a `master`.

Por esta razón no se fusionó un paso de scanner conocido como fallido. La rama
principal se mantuvo en el commit estable
`5bedc833c6324cba316cefd5ccc39d1269f3b984`, cuyo Run #95 concluye
`success` y ejecuta las pruebas funcionales, arquitectónicas y contractuales.

El estado verificable queda así:

```text
Proyecto oficial SonarQube Cloud: verificado
Project Key: ISCOUTB_AS_202620_PROYECTO_CAMPUSMARKET
Organization Key: isco-utb
Quality Gate público: Passed
Configuración .sonarcloud.properties: versionada
Pipeline principal de master: success
Scanner explícito en workflow de master: pendiente
Run exitoso del scanner desde CI: pendiente
Restricción actual: autorización para ejecutar análisis sobre isco-utb
```

Por tanto, según la comprobación transversal exigida por `CONTRATO.md`, este
punto no se declara como cumplido mientras no exista una ejecución exitosa del
scanner sobre el proyecto oficial.

Para cerrar esta conformidad transversal se requiere una de estas acciones:

1. otorgar al equipo permiso `Execute Analysis` sobre
   `ISCOUTB_AS_202620_PROYECTO_CAMPUSMARKET`; o
2. configurar en el repositorio un `SONAR_TOKEN` autorizado por un administrador
   de la organización `isco-utb`.

Mientras esa autorización no exista, `master` conserva el pipeline estable de
pruebas funcionales, arquitectónicas y contractuales, evitando introducir una
integración conocida como fallida.

La restricción se documenta como una limitación de autorización externa y no
como evidencia de cumplimiento.

---

# Cadena de trazabilidad S7

La trazabilidad principal es:

```text
ASP-07
   ↓
EC-06
   ↓
C4 Nivel 2
   ↓
ADR-0003
   ↓
OpenAPI 1.0.0
   ↓
FastAPI / Flutter Web
   ↓
test_contrato_openapi.py
   ↓
GitHub Actions
   ↓
fallo ante cambio incompatible
   ↓
restauración
   ↓
pipeline verde
```

Esta cadena conecta:

- aspecto arquitectónico;
- escenario de calidad;
- representación C4;
- decisión arquitectónica;
- contrato ejecutable;
- implementación;
- prueba automática;
- pipeline;
- evidencia experimental de fallo;
- restauración del estado compatible.

---

# Estado final de la evidencia S7

Al 18/09/2026, CampusMarket dispone de evidencia auditable para:

- contrato OpenAPI ejecutable y versionado;
- API `1.0.0`;
- rutas y `components.schemas`;
- cotejo bidireccional contrato ↔ implementación;
- historial Git del contrato;
- prueba contractual automatizada;
- invocación explícita de la prueba contractual en GitHub Actions;
- `master` en `5bedc833c6324cba316cefd5ccc39d1269f3b984`;
- Run #95 exitoso sobre el estado vigente de `master`;
- run rojo real ante cambio incompatible;
- ADR de integración síncrona;
- arc42 sección 6;
- C4 Nivel 2;
- trazabilidad navegable en `docs/aspectos.md`;
- registro de IA con decisiones rechazadas y motivo;
- Quality Gate público de SonarQube Cloud;
- identificación del proyecto y organización oficiales de SonarQube Cloud;
- documentación explícita de la restricción de autorización que impide obtener
  actualmente un run exitoso del scanner desde CI sobre `isco-utb`.

**Matriz específica S7: 10 de 10 criterios documentados con evidencia auditable.**

**Pendiente transversal:** integrar el scanner de SonarQube Cloud al workflow de
`master` y obtener un run exitoso asociado al proyecto oficial. Este punto no se
declara cumplido mientras no exista una credencial autorizada para ejecutar
análisis sobre la organización `isco-utb`.

El pendiente transversal no modifica la evidencia específica ya documentada
para los diez criterios de S7; se mantiene separado y explícito para la revisión
automática y la sustentación.




