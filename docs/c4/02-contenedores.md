
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
- las relaciones entre contenedores;
- los protocolos principales de comunicación.

Este nivel responde principalmente a:

- qué partes principales forman el sistema;
- qué responsabilidad tiene cada contenedor;
- qué tecnología utiliza cada uno;
- cómo se comunican entre sí.

Los actores externos se mantienen coherentes con el C4 Nivel 1:

- **Estudiante:** utiliza CampusMarket para publicar y consultar productos.
- **Administrador:** accede al sistema para funciones de supervisión.

---

## Contenedores actuales

| Contenedor | Tecnología | Responsabilidad |
|---|---|---|
| Frontend Web | Flutter / Dart | Proporcionar la interfaz mediante la cual los usuarios interactúan con CampusMarket. |
| Backend API | FastAPI / Python | Recibir solicitudes HTTP, validar datos, ejecutar casos de uso y coordinar el acceso a la persistencia. |
| Persistencia | MySQL | Almacenar y recuperar los datos actualmente materializados del dominio. |

La topología vigente puede resumirse como:

```text
Frontend Web
    ↓ HTTP/JSON
Backend API
    ↓ PyMySQL / SQL
MySQL
````

La sustitución de SQLite por MySQL modifica la tecnología de persistencia, pero
mantiene la separación arquitectónica entre:

* interfaz;
* lógica de aplicación;
* almacenamiento.

---

## Correspondencia con el código

| Contenedor C4      | Evidencia en el repositorio                                                          |
| ------------------ | ------------------------------------------------------------------------------------ |
| Frontend Web       | `frontend/campusmarket/lib/`                                                         |
| Backend API        | `backend/app/`                                                                       |
| Persistencia MySQL | `backend/app/publicaciones/repository.py`, que utiliza PyMySQL para acceder a MySQL. |

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

## Relaciones entre contenedores

Las relaciones principales son:

### Estudiante → Frontend Web

El estudiante utiliza la interfaz Flutter para crear y consultar publicaciones.

### Administrador → Frontend Web

El administrador utilizará el frontend para capacidades de supervisión.

Las capacidades administrativas todavía no se presentan como completamente
materializadas.

### Frontend Web → Backend API

El frontend crea y consulta publicaciones mediante:

* HTTP;
* JSON;
* estilo REST;
* comunicación síncrona.

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

El frontend no accede directamente a MySQL.

---

## Corte vertical implementado

El corte vertical actualmente verificable recorre:

```text
Flutter Web
    ↓
FastAPI
    ↓
módulo publicaciones
    ↓
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

`contracts/openapi-v1.json`

La estrategia síncrona, sus consecuencias y su acoplamiento temporal se
registran en:

[ADR-0003 - Integración síncrona HTTP/JSON](../adr/0003-usar-integracion-sincrona-http-json.md)

La implementación del proveedor se verifica mediante:

[`backend/tests/test_contrato_openapi.py`](../../backend/tests/test_contrato_openapi.py)

La relación puede resumirse como:

```text
Flutter
   ↓
Contrato OpenAPI
   ↓
FastAPI
```

La prueba de contrato evita depender únicamente de la inspección manual del
documento OpenAPI.

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
   ↓
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

La decisión de migración debe quedar registrada mediante un ADR independiente.

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

---

## Alcance del Nivel 2

Este diagrama representa únicamente:

* contenedores principales;
* responsabilidades generales;
* tecnologías principales;
* relaciones entre contenedores;
* protocolos de comunicación principales.

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
Frontend Web
    ↓
Backend API
    ↓
MySQL
```

Los actores y límites permanecen coherentes entre ambos niveles.

---

## Relación con el C4 Nivel 3

El C4 Nivel 3 amplía exclusivamente el contenedor Backend API.

La estructura materializada es:

```text
API de Publicaciones
        ↓
Servicio de Publicaciones
        ↓
Repositorio de Publicaciones
        ↓
MySQL
```

Documentación:

[C4 Nivel 3 - Componentes del Backend](./03-componentes-backend.md)

Fuente:

[`03-componentes-backend.puml`](./03-componentes-backend.puml)

---

## Fuente canónica

El archivo:

[`02-contenedores.puml`](./02-contenedores.puml)

es la fuente versionada y vigente del C4 Nivel 2.

Cualquier modificación gráfica debe realizarse sobre ese archivo para evitar
versiones contradictorias de la arquitectura.

La documentación textual de este archivo complementa el diagrama, pero no
reemplaza su fuente PlantUML.

````
