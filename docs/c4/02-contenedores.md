# C4 Nivel 2 - Contenedores de CampusMarket

El diagrama de contenedores vigente de CampusMarket se mantiene como
**diagrama como código** en:

[`02-contenedores.puml`](./02-contenedores.puml)

---

## Propósito

El C4 Nivel 2 representa los contenedores principales que conforman
CampusMarket, indicando:

- su responsabilidad general;
- la tecnología utilizada;
- las relaciones entre actores y contenedores;
- el propósito de cada comunicación;
- el protocolo y formato o tecnología utilizados en cada relación.

Este nivel responde principalmente a:

- qué partes principales forman el sistema;
- qué responsabilidad tiene cada contenedor;
- qué tecnología utiliza cada uno;
- cómo interactúan los actores con el sistema;
- cómo se comunican los contenedores entre sí.

Los actores externos se mantienen coherentes con el C4 Nivel 1:

- **Estudiante:** utiliza CampusMarket para publicar y consultar productos.
- **Administrador:** representa el actor previsto para capacidades de supervisión.
  Estas capacidades administrativas todavía no se consideran completamente
  materializadas en el corte vertical actual.

---

## Contenedores actuales

| Contenedor | Tecnología | Responsabilidad |
|---|---|---|
| Frontend Web | Flutter / Dart | Proporcionar la interfaz web mediante la cual los usuarios interactúan con CampusMarket. |
| Backend API | FastAPI / Python | Recibir solicitudes HTTP, validar datos, ejecutar casos de uso y coordinar el acceso a la persistencia. |
| Persistencia | MySQL | Almacenar y recuperar los datos actualmente materializados del dominio. |

La topología vigente puede resumirse como:

```text
Estudiante / Administrador
          ↓
  HTTPS / interfaz web
          ↓
     Flutter Web
          ↓
 HTTP/JSON síncrono
          ↓
      FastAPI
          ↓
   PyMySQL / SQL
          ↓
        MySQL
````

La sustitución de SQLite por MySQL modifica la tecnología de persistencia, pero
mantiene la separación arquitectónica entre:

* interfaz;
* lógica de aplicación;
* almacenamiento.

---

## Correspondencia con el código

| Contenedor C4      | Evidencia en el repositorio                                                         |
| ------------------ | ----------------------------------------------------------------------------------- |
| Frontend Web       | `frontend/campusmarket/lib/`                                                        |
| Backend API        | `backend/app/`                                                                      |
| Persistencia MySQL | `backend/app/publicaciones/repository.py`, que utiliza PyMySQL para acceder a MySQL |

El acceso productivo a la persistencia está encapsulado en:

`backend/app/publicaciones/repository.py`

El resto del Backend API no accede directamente al motor MySQL.

La configuración de conexión se proporciona mediante variables de entorno y
las credenciales no forman parte del repositorio.

La base de datos utilizada por el entorno actual se denomina:

`campusmarket`

La tabla actualmente materializada es:

`publicaciones`

---

## Relaciones entre actores y contenedores

Cada relación del C4 Nivel 2 explicita su propósito y el protocolo, formato o
tecnología utilizada.

### Estudiante → Frontend Web

El estudiante accede al Frontend Web para publicar y consultar productos.

La relación se representa como:

```text
Estudiante
    ↓
Publica y consulta productos
[HTTPS / interfaz web Flutter Web]
    ↓
Frontend Web
```

La interacción se realiza mediante una interfaz web implementada con
Flutter/Dart y servida al usuario mediante HTTPS en un entorno desplegado.

En desarrollo local puede utilizarse HTTP.

### Administrador → Frontend Web

El administrador representa el actor asociado a capacidades de supervisión.

La relación se representa como:

```text
Administrador
    ↓
Supervisa contenido
[HTTPS / interfaz web Flutter Web]
    ↓
Frontend Web
```

La capacidad administrativa se conserva como parte del límite arquitectónico y
del diseño del sistema, pero todavía no debe interpretarse como una
funcionalidad completamente materializada dentro del corte vertical actual.

### Frontend Web → Backend API

El Frontend Web crea y consulta publicaciones mediante:

* HTTP;
* JSON;
* estilo REST;
* comunicación síncrona.

La relación se representa como:

```text
Frontend Web
    ↓
GET /publicaciones
POST /publicaciones
[HTTP/JSON síncrono]
    ↓
Backend API
```

Los endpoints actualmente materializados incluyen:

* `POST /publicaciones`;
* `GET /publicaciones`;
* `GET /health`.

El contrato de esta comunicación se mantiene versionado en:

[`contracts/openapi-v1.json`](../../contracts/openapi-v1.json)

### Backend API → MySQL

El Backend API guarda y recupera publicaciones mediante:

* PyMySQL;
* SQL;
* conexiones controladas desde el repositorio.

La relación se representa como:

```text
Backend API
    ↓
Guarda y consulta publicaciones
[PyMySQL / SQL]
    ↓
MySQL
```

El Frontend Web no accede directamente a MySQL.

---

## Corte vertical implementado

El corte vertical actualmente verificable recorre:

```text
Estudiante
    ↓
Frontend Flutter Web
    ↓ HTTP/JSON
FastAPI
    ↓
Gestión de Publicaciones
    ↓ PyMySQL / SQL
MySQL
```

Su materialización principal se encuentra en:

* `frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart`
* `frontend/campusmarket/lib/publicaciones/publicaciones_api.dart`
* `backend/app/publicaciones/router.py`
* `backend/app/publicaciones/service.py`
* `backend/app/publicaciones/repository.py`

La prueba automatizada asociada se encuentra en:

[`backend/tests/test_publicaciones_vertical.py`](../../backend/tests/test_publicaciones_vertical.py)

Esta prueba verifica actualmente:

* creación mediante la API;
* consulta posterior;
* persistencia real en MySQL;
* respuesta controlada ante indisponibilidad de persistencia.

---

## Contrato API-first en S7

Durante S7 se hace explícito el contrato entre:

**Frontend Web → Backend API**

La integración utiliza:

```text
HTTP / JSON / REST / comunicación síncrona
```

El contrato se documenta mediante:

[`contracts/openapi-v1.json`](../../contracts/openapi-v1.json)

La versión actual de la API es:

`1.0.0`

El contrato utiliza:

`OpenAPI 3.1.0`

La estrategia síncrona, sus consecuencias y su acoplamiento temporal se
registran en:

[ADR-0003 - Integración síncrona HTTP/JSON](../adr/0003-usar-integracion-sincrona-http-json.md)

La implementación del proveedor se verifica mediante:

[`backend/tests/test_contrato_openapi.py`](../../backend/tests/test_contrato_openapi.py)

La relación puede resumirse como:

```text
Flutter Web
    ↓ HTTP/JSON
Contrato OpenAPI 1.0.0
    ↓
FastAPI
```

La prueba de contrato compara el contrato versionado con la superficie OpenAPI
generada por FastAPI.

Por tanto, la verificación no depende únicamente de inspección manual.

Un cambio incompatible de rutas, operaciones o esquemas provoca el fallo de la
prueba de contrato.

---

## Persistencia vigente

La tecnología de persistencia vigente es:

**MySQL**

El acceso desde Python se realiza mediante:

**PyMySQL**

La responsabilidad de acceso permanece encapsulada en:

`backend/app/publicaciones/repository.py`

Esto permite mantener:

```text
router.py
    ↓
service.py
    ↓
repository.py
    ↓ PyMySQL / SQL
MySQL
```

Los detalles del repositorio y de esta descomposición interna se representan en
el **C4 Nivel 3**, no como componentes separados del Nivel 2.

---

## Indisponibilidad temporal de persistencia

El Backend API mantiene un comportamiento controlado ante la indisponibilidad
de la persistencia.

En el estado actual:

1. el repositorio intenta acceder a MySQL;
2. una falla de conexión o persistencia se transforma en una condición
   controlada;
3. la condición se propaga hacia la capa de aplicación;
4. el Backend API responde:

`503 Service Unavailable`

El objetivo es evitar que detalles internos de MySQL o PyMySQL se filtren hacia
el consumidor de la API.

El comportamiento dinámico completo se documenta en:

[Vista de ejecución](../arc42/06-vista-ejecucion.md)

---

## Propiedad de los datos

La tabla:

`publicaciones`

pertenece al contexto:

**Gestión de Publicaciones**

La escritura productiva debe permanecer encapsulada en:

`backend/app/publicaciones/repository.py`

Otros contextos, como:

* Gestión de Usuarios;
* Catálogo;
* Administración;

no deben escribir directamente sobre esta tabla.

Si en el futuro necesitan consultar o modificar información de Publicaciones,
deberán hacerlo mediante interfaces definidas por el contexto propietario y no
mediante acceso directo a la persistencia.

Estas reglas se detallan en:

[Conceptos transversales](../arc42/08-conceptos-transversales.md)

---

## Evolución respecto al primer corte

Durante el primer corte, CampusMarket utilizaba **SQLite** como mecanismo de
persistencia.

En ese momento, la topología era:

```text
Frontend Web
    ↓
Backend API
    ↓
SQLite
```

La restricción:

**R-07 - Persistencia sin nueva infraestructura durante el primer corte**

motivó mantener SQLite durante ese corte.

También se documentó el comportamiento ante bloqueo temporal mediante:

[ADR-0002 - Manejo de bloqueo temporal de SQLite](../adr/0002-manejo-bloqueo-sqlite.md)

La respuesta implementada en ese momento:

* utilizaba una espera acotada;
* detectaba `SQLITE_BUSY`;
* detectaba `SQLITE_LOCKED`;
* devolvía HTTP `503` ante indisponibilidad;
* evitaba escrituras parciales;
* permitía recuperación posterior.

Estos elementos se mantienen como **evidencia histórica del primer corte**.

No representan la tecnología de persistencia vigente.

---

## Evidencia histórica de S5

La línea base previa al cambio de S5 registró:

* HTTP durante bloqueo: `500`;
* tiempo durante bloqueo: `7.323 s`;
* escritura parcial: `No`;
* recuperación posterior: HTTP `201`.

Después de aplicar ADR-0002 se obtuvo:

* HTTP durante bloqueo: `503`;
* tiempo durante bloqueo: `1.283 s`;
* escritura parcial: `No`;
* recuperación posterior: HTTP `201`;
* tiempo de recuperación: `0.006 s`.

El resultado cumplió el umbral definido en EC-05 para ese escenario.

Evidencias históricas:

* [Línea base](../evidencias/linea-base-bloqueo-sqlite-2026-09-05.md)
* [Medición posterior](../evidencias/medicion-bloqueo-sqlite-2026-09-06.md)
* [EC-05](../arc42/10-escenarios-de-calidad.md#ec-05---degradación-ante-bloqueo-temporal-de-persistencia)
* [ADR-0002](../adr/0002-manejo-bloqueo-sqlite.md)

Estas mediciones no se reinterpretan como mediciones de MySQL.

---

## Evolución de la topología

La arquitectura conserva tres responsabilidades principales:

```text
Frontend
    ↓
Backend
    ↓
Persistencia
```

La evolución de SQLite a MySQL no introduce nuevos límites de dominio ni
divide el Backend API en microservicios.

Sí modifica la tecnología concreta del contenedor de persistencia.

Por tanto:

* se mantienen las fronteras principales;
* se mantiene el monolito modular;
* cambia la tecnología de almacenamiento;
* cambia el mecanismo de acceso de `sqlite3` a PyMySQL.

La decisión de migración está registrada mediante un ADR independiente:

[ADR-0004 - Migración de SQLite a MySQL](../adr/0004-migrar-sqlite-a-mysql.md)

---

## Conservación de fronteras arquitectónicas

La arquitectura vigente conserva:

* Frontend separado del Backend API;
* Backend API separado de la persistencia;
* Gestión de Publicaciones como propietario de `publicaciones`;
* monolito modular;
* dirección interna `router → service → repository`;
* contratos explícitos entre consumidor y proveedor.

La decisión base continúa registrada en:

[ADR-0001 - Monolito modular](../adr/0001-usar-monolito-modular.md)

La estrategia de integración se documenta en:

[ADR-0003 - Integración síncrona HTTP/JSON](../adr/0003-usar-integracion-sincrona-http-json.md)

La persistencia vigente se documenta en:

[ADR-0004 - Migración de SQLite a MySQL](../adr/0004-migrar-sqlite-a-mysql.md)

---

## Alcance del Nivel 2

Este diagrama representa únicamente:

* actores externos;
* contenedores principales;
* responsabilidades generales;
* tecnologías principales;
* relaciones entre actores y contenedores;
* relaciones entre contenedores;
* propósito de las comunicaciones;
* protocolos, formatos o tecnologías principales utilizadas en cada relación.

No representa:

* módulos internos;
* componentes;
* clases;
* routers;
* services;
* repositories;
* excepciones internas;
* implementación de transacciones.

Ese nivel de detalle corresponde al **C4 Nivel 3**.

---

## Relación con el C4 Nivel 1

El [C4 Nivel 1](./01-contexto.md) representa CampusMarket como un único sistema
frente a Estudiante y Administrador.

El C4 Nivel 2 realiza un acercamiento al interior de esa caja y muestra cómo el
sistema se materializa actualmente mediante:

```text
Estudiante / Administrador
          ↓
     Frontend Web
          ↓
      Backend API
          ↓
         MySQL
```

Los actores y límites permanecen coherentes entre ambos niveles.

La presencia del actor Administrador expresa el límite y la responsabilidad
prevista del sistema, sin afirmar que todas sus capacidades estén actualmente
implementadas.

---

## Relación con el C4 Nivel 3

El C4 Nivel 3 amplía exclusivamente el contenedor Backend API.

La estructura actualmente materializada es:

```text
API de Publicaciones
        ↓
Servicio de Publicaciones
        ↓
Repositorio de Publicaciones
        ↓
MySQL
```

En este nivel también se mantienen explícitos los límites todavía no
materializados de:

* Gestión de Usuarios;
* Catálogo;
* Administración.

Documentación:

[C4 Nivel 3 - Componentes del Backend](./03-componentes-backend.md)

Fuente:

[`03-componentes-backend.puml`](./03-componentes-backend.puml)

---

## Trazabilidad S7

La relación arquitectónica principal de S7 puede seguirse mediante:

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
FastAPI / Flutter
  ↓
test_contrato_openapi.py
  ↓
GitHub Actions
```

Esta cadena conecta la decisión arquitectónica con:

* la documentación;
* el contrato;
* la implementación;
* la prueba automatizada;
* la evidencia del pipeline.

---

## Fuente canónica

El archivo:

[`02-contenedores.puml`](./02-contenedores.puml)

es la fuente versionada y vigente del C4 Nivel 2.

Cualquier modificación gráfica debe realizarse primero sobre ese archivo para
evitar versiones contradictorias de la arquitectura.

La documentación textual de este archivo complementa el diagrama, pero no
reemplaza su fuente PlantUML.
