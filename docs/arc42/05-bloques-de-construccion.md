
````markdown
# 5. Bloques de construcción

CampusMarket mantiene tres bloques ejecutables principales dentro de la
arquitectura actual:

| Bloque | Responsabilidad | Tecnología | Ubicación |
|---|---|---|---|
| Frontend Web | Capturar información del usuario, presentar las funcionalidades disponibles y comunicarse con el backend. | Flutter / Dart | `frontend/campusmarket/lib/` |
| Backend API | Recibir solicitudes HTTP, coordinar reglas de aplicación y controlar el acceso a las capacidades del dominio. | FastAPI / Python | `backend/app/` |
| Persistencia | Almacenar y recuperar los datos actualmente materializados del dominio. | MySQL / PyMySQL | acceso productivo encapsulado en `backend/app/publicaciones/repository.py` |

Esta división corresponde a los contenedores representados en el
**C4 Nivel 2**.

Durante S6 se profundiza además en la estructura interna del contenedor
**Backend API** mediante un **C4 Nivel 3**, haciendo explícitos los límites
modulares, los componentes actualmente materializados y la propiedad de los
datos.

Durante S7 se complementa esta estructura con una orientación **API-first**,
donde el contrato entre frontend y backend se documenta mediante OpenAPI y se
verifica automáticamente.

---

## 5.1 Backend modular

La decisión:

[ADR-0001 - Monolito modular](../adr/0001-usar-monolito-modular.md)

organiza el backend alrededor de cuatro capacidades principales del dominio:

- `usuarios`;
- `publicaciones`;
- `catalogo`;
- `administracion`.

Durante S6 estas capacidades se formalizan además como contextos delimitados:

| Módulo | Contexto delimitado | Responsabilidad | Estado actual |
|---|---|---|---|
| `usuarios` | Gestión de Usuarios | Identidad, autenticación e información básica del estudiante | Límite definido; funcionalidad todavía no materializada |
| `publicaciones` | Gestión de Publicaciones | Ciclo de vida de publicaciones y propiedad de su persistencia | Materializado actualmente |
| `catalogo` | Catálogo | Consulta, búsqueda y filtrado de publicaciones | Límite definido; funcionalidad todavía no materializada |
| `administracion` | Administración | Supervisión y moderación del contenido | Límite definido; funcionalidad todavía no materializada |

La existencia de un límite modular no implica que toda su funcionalidad esté
implementada.

En el estado actual del prototipo, la capacidad con mayor materialización
funcional es:

`backend/app/publicaciones/`

Los demás módulos conservan sus fronteras arquitectónicas para evitar que la
evolución del sistema mezcle responsabilidades o introduzca escrituras
compartidas sobre los datos.

---

## 5.2 Descomposición del Backend API — C4 Nivel 3

El **C4 Nivel 3** realiza un acercamiento al interior del contenedor
**Backend API**.

La documentación se encuentra en:

- [C4 Nivel 3 - Componentes del Backend](../c4/03-componentes-backend.md)
- [Fuente PlantUML](../c4/03-componentes-backend.puml)

La materialización actualmente verificable de Gestión de Publicaciones sigue
el flujo:

```text
Frontend Web
     |
     | HTTP / JSON síncrono
     v
API de Publicaciones
     |
     v
Servicio de Publicaciones
     |
     v
Repositorio de Publicaciones
     |
     | PyMySQL / SQL
     v
MySQL
````

---

## 5.3 Componentes materializados de Gestión de Publicaciones

### Entrada de aplicación

**Ubicación**

`backend/app/main.py`

**Responsabilidad**

* configurar FastAPI;
* registrar middleware;
* registrar los routers actualmente disponibles;
* actuar como punto de composición del Backend API;
* exponer la configuración general de la API.

En el estado actual registra el router correspondiente a Publicaciones.

También expone el endpoint:

`GET /health`

como mecanismo básico de verificación del Backend API.

---

### API de Publicaciones

**Ubicación**

`backend/app/publicaciones/router.py`

**Responsabilidad**

* exponer los endpoints HTTP del contexto;
* recibir y validar solicitudes;
* utilizar los modelos de entrada y salida;
* delegar las operaciones al servicio;
* traducir condiciones de aplicación a respuestas HTTP;
* mantener separada la interfaz HTTP de la persistencia.

Actualmente participa en:

* `POST /publicaciones`;
* `GET /publicaciones`.

La API no ejecuta SQL ni accede directamente a MySQL.

La comunicación externa se mantiene mediante HTTP/JSON y su contrato se
documenta con OpenAPI.

---

### Servicio de Publicaciones

**Ubicación**

`backend/app/publicaciones/service.py`

**Responsabilidad**

* coordinar las operaciones de aplicación;
* normalizar los datos recibidos;
* mantener separada la lógica HTTP de la persistencia;
* delegar las operaciones de almacenamiento al repositorio;
* propagar de forma controlada las condiciones de indisponibilidad de
  persistencia.

El servicio no ejecuta SQL directamente ni conoce detalles de conexión con
MySQL.

---

### Repositorio de Publicaciones

**Ubicación**

`backend/app/publicaciones/repository.py`

**Responsabilidad**

* encapsular las conexiones a MySQL;
* inicializar la estructura de persistencia necesaria;
* insertar publicaciones;
* consultar publicaciones;
* manejar errores técnicos de acceso a persistencia;
* preservar las transacciones mediante `commit` y `rollback`;
* aislar del resto del contexto los detalles concretos de persistencia.

El acceso a MySQL se realiza mediante:

`PyMySQL`

Este componente constituye actualmente el **único escritor productivo** de la
entidad persistida:

`publicaciones`

---

## 5.4 Dirección de dependencias

La dirección interna implementada es:

```text
main.py
   |
   v
router.py
   |
   v
service.py
   |
   v
repository.py
   |
   v
MySQL
```

La regla adoptada es:

**Router → Service → Repository → Persistencia**

Esto implica que:

* `router.py` puede depender de `service.py`;
* `service.py` puede depender de `repository.py`;
* `repository.py` puede depender del mecanismo de persistencia;
* el repositorio no debe depender del servicio;
* el servicio no debe depender del router;
* otros contextos no deben utilizar directamente el repositorio interno de
  Publicaciones.

Esta dirección reduce el acoplamiento y mantiene explícitas las
responsabilidades internas del Backend API.

---

## 5.5 Interfaces relevantes

Las interfaces actualmente verificables son:

* **Flutter → FastAPI:** REST sobre HTTP/JSON.
* **FastAPI → MySQL:** SQL mediante PyMySQL.
* **Endpoint de creación:** `POST /publicaciones`.
* **Endpoint de consulta:** `GET /publicaciones`.
* **Endpoint de salud:** `GET /health`.
* **Contrato de API:** `contracts/openapi-v1.json`.

La comunicación Flutter → FastAPI actualmente materializada es **síncrona**:
cada solicitud HTTP espera una respuesta en la misma interacción.

En el interior del contexto Publicaciones, la comunicación mantiene la
secuencia:

```text
router.py → service.py → repository.py
```

Los otros contextos deberán comunicarse mediante contratos explícitos y no
mediante acceso directo a la persistencia de Publicaciones.

---

## 5.6 Contrato API-first

Durante S7 se formaliza el contrato entre consumidor y proveedor mediante
OpenAPI.

El contrato versionado se encuentra en:

`contracts/openapi-v1.json`

La implementación del Backend API debe permanecer coherente con dicho contrato.

La correspondencia se verifica mediante:

`backend/tests/test_contrato_openapi.py`

La intención arquitectónica es evitar que el contrato sea únicamente una
descripción documental: debe ser contrastado automáticamente contra la
implementación real.

---

## 5.7 Propiedad de datos

S6 adopta como regla arquitectónica:

> Cada dato de dominio tiene un único módulo responsable de escribirlo.

La entidad persistida de dominio actualmente materializada es:

`publicaciones`

Su propietario es:

**Gestión de Publicaciones**

La escritura productiva se encuentra encapsulada en:

`backend/app/publicaciones/repository.py`

La propiedad actual es:

| Campo         | Propietario              |
| ------------- | ------------------------ |
| `id`          | Gestión de Publicaciones |
| `titulo`      | Gestión de Publicaciones |
| `descripcion` | Gestión de Publicaciones |
| `precio`      | Gestión de Publicaciones |
| `modalidad`   | Gestión de Publicaciones |
| `estado`      | Gestión de Publicaciones |

Los módulos:

* `usuarios`;
* `catalogo`;
* `administracion`;

no deben ejecutar operaciones directas de escritura sobre esta entidad.

---

## 5.8 Reglas entre módulos

Para conservar las fronteras del monolito modular se establecen las siguientes
reglas:

1. Cada entidad persistida debe tener un único módulo propietario.
2. Un módulo no debe escribir directamente en los datos pertenecientes a otro
   contexto.
3. La comunicación entre contextos debe realizarse mediante contratos,
   servicios u operaciones explícitas.
4. Consultar información de otro contexto no transfiere la propiedad del dato.
5. Ningún módulo debe importar directamente el repositorio interno perteneciente
   a otro contexto.
6. Los detalles concretos de persistencia deben permanecer encapsulados en el
   módulo propietario.
7. La evolución futura del sistema deberá preservar estas fronteras incluso si
   posteriormente se extraen servicios independientes.

### Ejemplo: Catálogo

Catálogo podrá solicitar o consultar publicaciones para implementar búsqueda y
filtrado.

Sin embargo, no deberá ejecutar directamente:

```sql
INSERT INTO publicaciones
UPDATE publicaciones
DELETE FROM publicaciones
```

### Ejemplo: Administración

Administración podrá solicitar acciones de moderación sobre una publicación.

La modificación deberá ser ejecutada mediante un contrato ofrecido por Gestión
de Publicaciones.

Administración no deberá acceder directamente a:

`backend/app/publicaciones/repository.py`

ni escribir sobre la tabla `publicaciones`.

### Ejemplo: Usuarios

Cuando Gestión de Usuarios sea materializada, este contexto conservará la
propiedad de los datos de identidad.

Gestión de Publicaciones podrá mantener una referencia al propietario de una
publicación, pero no deberá modificar directamente la información interna del
usuario.

---

## 5.9 Verificación automática de la modularidad

Las reglas principales de separación se complementan mediante la prueba:

[`backend/tests/test_modularidad_s6.py`](../../backend/tests/test_modularidad_s6.py)

Esta prueba verifica que:

* `backend/app/publicaciones/repository.py` sea el único escritor productivo de
  `publicaciones`;

* `usuarios`, `catalogo` y `administracion` no accedan directamente a la
  tecnología de persistencia;

* otros contextos no importen directamente el repositorio interno de
  Publicaciones;

* el flujo implementado mantenga la dirección:

  `router → service → repository → MySQL`;

* la persistencia del contexto permanezca encapsulada en su repositorio.

La integración vertical se verifica además mediante:

[`backend/tests/test_publicaciones_vertical.py`](../../backend/tests/test_publicaciones_vertical.py)

Esta prueba comprueba:

* creación de publicaciones a través de la API;
* recuperación posterior mediante la API;
* persistencia real de los datos en MySQL;
* respuesta controlada `503` ante indisponibilidad de la persistencia.

Estas comprobaciones se ejecutan junto con las demás pruebas del backend.

---

## 5.10 Correspondencia con los niveles C4

La estructura arquitectónica queda representada en tres niveles.

### C4 Nivel 1 — Contexto

Representa CampusMarket como sistema y sus relaciones con los actores externos.

Documentación:

[`docs/c4/01-contexto.md`](../c4/01-contexto.md)

### C4 Nivel 2 — Contenedores

Representa:

```text
Frontend Web
    ↓ HTTP/JSON
Backend API
    ↓ PyMySQL / SQL
MySQL
```

Documentación:

[`docs/c4/02-contenedores.md`](../c4/02-contenedores.md)

### C4 Nivel 3 — Componentes

Amplía el contenedor **Backend API** y representa la estructura interna
actualmente materializada:

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

[`docs/c4/03-componentes-backend.md`](../c4/03-componentes-backend.md)

Fuente:

[`docs/c4/03-componentes-backend.puml`](../c4/03-componentes-backend.puml)

---

## 5.11 Evolución de la persistencia

Durante el primer corte, CampusMarket utilizó SQLite como mecanismo de
persistencia.

Esa decisión y sus mediciones se mantienen documentadas como evidencia
histórica, principalmente en:

* ADR-0002;
* evidencia de bloqueo de SQLite;
* scripts y mediciones del primer corte.

La persistencia vigente del sistema es **MySQL**.

La migración modifica la tecnología de persistencia, pero mantiene:

* el módulo propietario de `publicaciones`;
* la dirección `router → service → repository`;
* el principio de único escritor;
* las fronteras del monolito modular.

Por esta razón, la migración debe documentarse mediante un ADR independiente,
sin reescribir las decisiones históricas del primer corte.

---

## 5.12 Coherencia con ADR-0001

La incorporación del C4 Nivel 3 y la migración de persistencia no modifican la
decisión arquitectónica establecida por ADR-0001.

Los límites continúan siendo:

* `usuarios`;
* `publicaciones`;
* `catalogo`;
* `administracion`.

Estos límites:

* no fueron fusionados;
* no fueron divididos;
* no fueron reemplazados;
* no fueron convertidos en microservicios.

S6 profundiza en su definición, propiedad de datos y reglas de comunicación.

S7 añade el contrato API-first y actualiza la tecnología de persistencia sin
modificar esas fronteras funcionales.

---

## 5.13 Evidencia relacionada

La estructura documentada en esta sección se complementa con:

* [Conceptos transversales y contextos delimitados](./08-conceptos-transversales.md)
* [ADR-0001 - Monolito modular](../adr/0001-usar-monolito-modular.md)
* [C4 Nivel 2 - Contenedores](../c4/02-contenedores.md)
* [C4 Nivel 3 - Componentes del Backend](../c4/03-componentes-backend.md)
* [Auditoría de modularidad S6](../evidencias/auditoria-modularidad-s6-2026-09-12.md)
* [Trazabilidad de aspectos](../aspectos.md)
* [`contracts/openapi-v1.json`](../../contracts/openapi-v1.json)
* [`test_modularidad_s6.py`](../../backend/tests/test_modularidad_s6.py)
* [`test_publicaciones_vertical.py`](../../backend/tests/test_publicaciones_vertical.py)
* [`test_contrato_openapi.py`](../../backend/tests/test_contrato_openapi.py)

De esta forma, los bloques de construcción no se documentan únicamente como
una estructura conceptual: su correspondencia se mantiene trazada hacia el
código, la propiedad de los datos, los contratos, la auditoría y las pruebas
automáticas.

````
