
# C4 Nivel 3 - Componentes del Backend API de CampusMarket

El C4 Nivel 3 de CampusMarket realiza un acercamiento al interior del
contenedor **Backend API**, identificado previamente en el C4 Nivel 2.

Su propósito es mostrar los componentes internos actualmente verificables,
sus responsabilidades, las relaciones entre ellos y su correspondencia con
los límites de dominio definidos durante S6.

Durante S7 este nivel también hace explícita la relación entre:

- API;
- servicio;
- repositorio;
- persistencia MySQL;
- contrato OpenAPI;
- comunicación síncrona HTTP/JSON.

La fuente canónica del diagrama se encuentra en:

[`03-componentes-backend.puml`](./03-componentes-backend.puml)

---

## 1. Contenedor ampliado

El contenedor que se descompone en este nivel es:

**Backend API**

Tecnología:

**FastAPI / Python**

En el C4 Nivel 2 la topología vigente corresponde a:

```text
Frontend Web
    ↓ HTTP/JSON
Backend API
    ↓ PyMySQL / SQL
MySQL
````

El Nivel 3 no introduce un nuevo servicio desplegable.

Su objetivo es mostrar cómo se organiza internamente el Backend API y cómo sus
componentes colaboran para materializar Gestión de Publicaciones.

---

## 2. Relación con los contextos delimitados

Durante S6 se identificaron los siguientes contextos delimitados:

* Gestión de Usuarios;
* Gestión de Publicaciones;
* Catálogo;
* Administración.

Estos límites corresponden con los módulos definidos previamente para el
monolito modular de CampusMarket.

No todos poseen actualmente el mismo grado de implementación.

| Contexto delimitado      | Correspondencia estructural   | Estado actual                                           |
| ------------------------ | ----------------------------- | ------------------------------------------------------- |
| Gestión de Usuarios      | `backend/app/usuarios/`       | Límite definido; funcionalidad todavía no materializada |
| Gestión de Publicaciones | `backend/app/publicaciones/`  | Materializado actualmente                               |
| Catálogo                 | `backend/app/catalogo/`       | Límite definido; funcionalidad todavía no materializada |
| Administración           | `backend/app/administracion/` | Límite definido; funcionalidad todavía no materializada |

Por esta razón, el C4 Nivel 3 diferencia entre:

1. componentes actualmente materializados en código;
2. límites de contexto definidos arquitectónicamente pero todavía no
   implementados funcionalmente.

---

## 3. Componentes materializados del Backend API

### 3.1 Entrada de aplicación

**Archivo**

`backend/app/main.py`

**Responsabilidad**

* configurar la aplicación FastAPI;
* registrar middleware;
* configurar CORS;
* registrar los routers disponibles;
* actuar como punto de composición del Backend API.

En el estado actual registra el router perteneciente a Gestión de
Publicaciones.

También expone:

`GET /health`

como endpoint básico para comprobar disponibilidad del backend.

---

### 3.2 API de Publicaciones

**Archivo**

`backend/app/publicaciones/router.py`

**Responsabilidad**

Exponer mediante HTTP las capacidades actualmente disponibles del contexto
Gestión de Publicaciones.

Actualmente proporciona:

* creación de publicaciones mediante `POST /publicaciones`;
* consulta de publicaciones mediante `GET /publicaciones`;
* validación de los datos recibidos;
* modelos de entrada y salida;
* delegación hacia el servicio;
* traducción de una indisponibilidad temporal de persistencia a
  `503 Service Unavailable`.

La API no ejecuta SQL ni accede directamente a MySQL.

Su responsabilidad se limita a la interfaz HTTP y a la traducción entre el
contrato externo y la capa de aplicación.

---

### 3.3 Servicio de Publicaciones

**Archivo**

`backend/app/publicaciones/service.py`

**Responsabilidad**

Coordinar las operaciones de aplicación relacionadas con publicaciones y
mantener separadas las responsabilidades HTTP de los detalles de persistencia.

Actualmente:

* normaliza `titulo`;
* normaliza `descripcion`;
* normaliza el valor de `precio`;
* recibe `modalidad`;
* recibe `estado`;
* solicita al repositorio la creación de una publicación;
* solicita al repositorio el listado de publicaciones;
* traduce errores de persistencia a errores propios de la capa de aplicación.

El servicio no ejecuta SQL directamente.

Tampoco depende de PyMySQL.

---

### 3.4 Repositorio de Publicaciones

**Archivo**

`backend/app/publicaciones/repository.py`

**Responsabilidad**

Encapsular el acceso productivo a la persistencia correspondiente al contexto
Gestión de Publicaciones.

Actualmente:

* establece conexiones con MySQL;
* utiliza PyMySQL como driver de acceso;
* crea la tabla `publicaciones` cuando es necesario;
* inserta nuevas publicaciones;
* consulta publicaciones;
* controla transacciones mediante `commit` y `rollback`;
* traduce errores técnicos de persistencia a una excepción controlada;
* encapsula los detalles concretos del mecanismo de persistencia.

Este componente constituye actualmente el **único escritor productivo** de la
entidad persistida:

`publicaciones`

---

## 4. Relaciones entre componentes

El flujo principal actualmente implementado es:

```text
Frontend Web
     |
     | HTTP / JSON síncrono
     v
API de Publicaciones
     |
     | crear_publicacion()
     | listar_publicaciones()
     v
Servicio de Publicaciones
     |
     | create_publication()
     | list_publications()
     v
Repositorio de Publicaciones
     |
     | PyMySQL / SQL
     v
MySQL
```

La composición inicial ocurre de la siguiente manera:

```text
main.py
   |
   | registra
   v
router.py
```

Las dependencias mantienen una dirección explícita:

```text
Router → Service → Repository → MySQL
```

No existe una dependencia inversa desde Repository hacia Service o Router.

---

## 5. Contrato de API

Durante S7 se formaliza el contrato externo entre consumidor y proveedor.

El consumidor es:

**Frontend Flutter**

El proveedor es:

**Backend FastAPI**

La interfaz utiliza:

* HTTP;
* JSON;
* estilo REST;
* comunicación síncrona.

El contrato versionado se encuentra en:

`contracts/openapi-v1.json`

Los endpoints actualmente materializados incluyen:

* `POST /publicaciones`;
* `GET /publicaciones`;
* `GET /health`.

La relación puede representarse como:

```text
Flutter
   ↓ HTTP/JSON
Contrato OpenAPI
   ↓
FastAPI
```

La implementación debe mantenerse coherente con este contrato.

La correspondencia se verifica mediante:

[`backend/tests/test_contrato_openapi.py`](../../backend/tests/test_contrato_openapi.py)

---

## 6. Correspondencia entre C4 Nivel 3 y código

| Elemento del C4 Nivel 3      | Evidencia en el repositorio                                     |
| ---------------------------- | --------------------------------------------------------------- |
| Entrada de aplicación        | `backend/app/main.py`                                           |
| API de Publicaciones         | `backend/app/publicaciones/router.py`                           |
| Servicio de Publicaciones    | `backend/app/publicaciones/service.py`                          |
| Repositorio de Publicaciones | `backend/app/publicaciones/repository.py`                       |
| Gestión de Usuarios          | `backend/app/usuarios/`                                         |
| Catálogo                     | `backend/app/catalogo/`                                         |
| Administración               | `backend/app/administracion/`                                   |
| Persistencia MySQL           | acceso encapsulado en `backend/app/publicaciones/repository.py` |
| Contrato OpenAPI             | `contracts/openapi-v1.json`                                     |

La presencia de un límite estructural en el repositorio no implica que su
funcionalidad esté completamente implementada.

Por ello Usuarios, Catálogo y Administración se representan como límites
arquitectónicos definidos, pero no se documentan como componentes funcionales
ya materializados.

---

## 7. Propiedad de datos

S6 adopta la regla:

> Cada dato de dominio tiene un único módulo responsable de escribirlo.

En el estado actual del sistema, la entidad persistida de dominio
materializada es:

`publicaciones`

Su propietario es:

**Gestión de Publicaciones**

La escritura se encuentra encapsulada en:

`backend/app/publicaciones/repository.py`

Los campos actualmente persistidos son:

| Campo         | Propietario              |
| ------------- | ------------------------ |
| `id`          | Gestión de Publicaciones |
| `titulo`      | Gestión de Publicaciones |
| `descripcion` | Gestión de Publicaciones |
| `precio`      | Gestión de Publicaciones |
| `modalidad`   | Gestión de Publicaciones |
| `estado`      | Gestión de Publicaciones |

Ningún otro contexto debe ejecutar directamente operaciones de escritura sobre
esta entidad.

---

## 8. Reglas entre contextos

### Gestión de Usuarios y Gestión de Publicaciones

Cuando Gestión de Usuarios sea materializada, deberá proporcionar la identidad
del estudiante mediante un contrato explícito.

Gestión de Publicaciones podrá utilizar una referencia al propietario, pero no
deberá modificar directamente los datos internos de Usuarios.

---

### Gestión de Publicaciones y Catálogo

Catálogo podrá utilizar publicaciones para implementar búsqueda, consulta y
filtrado.

Consumir esos datos no convierte a Catálogo en propietario de
`publicaciones`.

Catálogo no deberá ejecutar directamente:

```sql
INSERT INTO publicaciones
UPDATE publicaciones
DELETE FROM publicaciones
```

---

### Gestión de Publicaciones y Administración

Administración podrá solicitar acciones de moderación sobre publicaciones.

La operación deberá realizarse mediante un contrato explícito de Gestión de
Publicaciones.

Administración no deberá depender directamente del repositorio ni escribir en
la tabla `publicaciones`.

La separación documentada en S6 prevé utilizar una capa anticorrupción en este
límite cuando las capacidades de Administración sean materializadas.

---

## 9. Aislamiento de persistencia

La tecnología de persistencia vigente es:

**MySQL**

El acceso se realiza mediante:

**PyMySQL**

Esta dependencia tecnológica se encuentra encapsulada en:

`backend/app/publicaciones/repository.py`

Las capas superiores no deben depender directamente de PyMySQL.

La dirección esperada es:

```text
router.py
   ↓
service.py
   ↓
repository.py
   ↓
PyMySQL
   ↓
MySQL
```

Este aislamiento evita que la API o la lógica de aplicación conozcan detalles
específicos del motor de base de datos.

---

## 10. Indisponibilidad de persistencia

Cuando MySQL no puede ser alcanzado temporalmente:

1. el repositorio intenta establecer la conexión;
2. PyMySQL produce un error técnico;
3. el repositorio traduce el error a una condición controlada;
4. el servicio propaga una excepción propia de aplicación;
5. el router responde:

`503 Service Unavailable`

El consumidor recibe una respuesta HTTP estable sin conocer detalles internos
del motor de persistencia.

El comportamiento dinámico completo se documenta en:

[Vista de ejecución](../arc42/06-vista-ejecucion.md)

---

## 11. Verificación automática

La modularidad se verifica mediante:

[`backend/tests/test_modularidad_s6.py`](../../backend/tests/test_modularidad_s6.py)

La prueba comprueba que:

* `repository.py` sea el único escritor productivo de `publicaciones`;
* otros contextos no utilicen directamente PyMySQL para escribir
  `publicaciones`;
* otros contextos no dependan directamente del repositorio interno de
  Publicaciones;
* la dirección se mantenga como:

  `router → service → repository → MySQL`.

La integración vertical se verifica mediante:

[`backend/tests/test_publicaciones_vertical.py`](../../backend/tests/test_publicaciones_vertical.py)

Esta prueba comprueba:

* creación mediante `POST /publicaciones`;
* consulta mediante `GET /publicaciones`;
* persistencia real en MySQL;
* respuesta `503` ante indisponibilidad.

El contrato HTTP se verifica mediante:

[`backend/tests/test_contrato_openapi.py`](../../backend/tests/test_contrato_openapi.py)

---

## 12. Coherencia con C4 Nivel 2

El C4 Nivel 2 representa:

```text
Frontend Web
    ↓ HTTP/JSON
Backend API
    ↓ PyMySQL / SQL
MySQL
```

El C4 Nivel 3 no reemplaza esa representación.

Realiza un acercamiento al interior del contenedor:

**Backend API**

y muestra:

```text
API de Publicaciones
        ↓
Servicio de Publicaciones
        ↓
Repositorio de Publicaciones
        ↓
MySQL
```

Por tanto:

* Nivel 1 muestra CampusMarket y sus actores externos;
* Nivel 2 muestra los contenedores principales;
* Nivel 3 muestra la estructura interna del Backend API.

---

## 13. Evolución respecto al primer corte

Durante el primer corte, CampusMarket utilizaba SQLite como mecanismo de
persistencia.

En ese estado anterior, el flujo era:

```text
Router → Service → Repository → SQLite
```

También se documentaron condiciones específicas de bloqueo mediante ADR-0002.

Estas referencias se conservan como evidencia histórica del primer corte.

La arquitectura vigente utiliza:

```text
Router → Service → Repository → MySQL
```

La migración de persistencia:

* no modifica los contextos delimitados;
* no divide el backend;
* no introduce microservicios;
* mantiene Gestión de Publicaciones como dueño de `publicaciones`;
* mantiene la dirección de dependencias;
* sustituye SQLite/`sqlite3` por MySQL/PyMySQL.

---

## 14. Coherencia con ADR-0001

El C4 Nivel 3 no introduce un nuevo estilo arquitectónico.

CampusMarket continúa utilizando el **monolito modular** definido en:

[ADR-0001 - Adoptar un monolito modular](../adr/0001-usar-monolito-modular.md)

Los límites principales continúan siendo:

* `usuarios`;
* `publicaciones`;
* `catalogo`;
* `administracion`.

S6 hizo explícitos sus contextos, relaciones y propiedad de datos.

S7 mantiene esas fronteras y agrega:

* contrato OpenAPI;
* comunicación síncrona HTTP/JSON;
* persistencia MySQL;
* verificación automática del contrato.

La migración de persistencia constituye una decisión tecnológica independiente
y no reemplaza ADR-0001.

---

## 15. Relación con S6 y S7

Este C4 Nivel 3 debe interpretarse junto con:

* [Sección 8 de arc42 - Conceptos transversales](../arc42/08-conceptos-transversales.md)
* [Auditoría de modularidad S6](../evidencias/auditoria-modularidad-s6-2026-09-12.md)
* [ADR-0001 - Monolito modular](../adr/0001-usar-monolito-modular.md)
* [ADR-0003 - Integración síncrona HTTP/JSON](../adr/0003-usar-integracion-sincrona-http-json.md)
* [C4 Nivel 2 - Contenedores](./02-contenedores.md)
* [Fuente PlantUML del C4 Nivel 3](./03-componentes-backend.puml)
* [`contracts/openapi-v1.json`](../../contracts/openapi-v1.json)

S6 define principalmente:

* contextos;
* propiedad de datos;
* modularidad;
* reglas de comunicación.

S7 hace explícitos:

* interfaces;
* contrato API;
* comunicación síncrona;
* persistencia vigente;
* verificación automatizada.

---

## 16. Estado actual y evolución

El componente con mayor materialización funcional en el backend es
**Gestión de Publicaciones**.

Usuarios, Catálogo y Administración mantienen sus fronteras estructurales,
pero sus capacidades todavía deberán desarrollarse progresivamente.

Cuando estos contextos sean implementados se deberá conservar:

* propiedad única de datos;
* comunicación mediante contratos;
* aislamiento de persistencia;
* dirección de dependencias;
* correspondencia entre C4 y código.

Si una evolución futura modifica realmente los límites establecidos por
ADR-0001, el cambio deberá documentarse mediante un nuevo ADR y la
actualización correspondiente de los diagramas C4.

---

## Fuente canónica

La fuente versionada del diagrama es:

[`03-componentes-backend.puml`](./03-componentes-backend.puml)

Este archivo Markdown explica y aporta trazabilidad al diagrama, pero no
sustituye su fuente PlantUML.

````