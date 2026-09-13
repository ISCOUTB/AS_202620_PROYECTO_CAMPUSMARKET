# C4 Nivel 3 - Componentes del Backend API de CampusMarket

El C4 Nivel 3 de CampusMarket realiza un acercamiento al interior del
contenedor **Backend API**, identificado previamente en el C4 Nivel 2.

Su propósito es mostrar los componentes internos actualmente verificables,
sus responsabilidades, las relaciones entre ellos y su correspondencia con
los límites de dominio definidos durante la Evidencia S6.

La fuente canónica del diagrama se encuentra en:

[`03-componentes-backend.puml`](./03-componentes-backend.puml)

---

## 1. Contenedor ampliado

El contenedor que se descompone en este nivel es:

**Backend API**

Tecnología:

**FastAPI / Python**

En el C4 Nivel 2 este contenedor aparece entre:

**Frontend Web → Backend API → SQLite**

El Nivel 3 no agrega nuevos contenedores desplegables ni modifica esa
topología.

Su objetivo es mostrar cómo se organiza internamente el backend.

---

## 2. Relación con los contextos delimitados de S6

Durante S6 se identificaron los siguientes contextos delimitados:

- Gestión de Usuarios
- Gestión de Publicaciones
- Catálogo
- Administración

Estos límites corresponden con los módulos definidos previamente para el
monolito modular de CampusMarket.

Sin embargo, no todos poseen actualmente el mismo grado de implementación.

| Contexto delimitado | Correspondencia estructural | Estado actual |
|---|---|---|
| Gestión de Usuarios | `backend/app/usuarios/` | Límite definido, funcionalidad todavía no materializada |
| Gestión de Publicaciones | `backend/app/publicaciones/` | Implementado en el corte vertical actual |
| Catálogo | `backend/app/catalogo/` | Límite definido, funcionalidad todavía no materializada |
| Administración | `backend/app/administracion/` | Límite definido, funcionalidad todavía no materializada |

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

Configurar la aplicación FastAPI, registrar middleware y conectar los routers
disponibles con la aplicación principal.

En el estado actual registra el router perteneciente a Gestión de
Publicaciones.

Este elemento actúa como punto de composición del Backend API.

---

### 3.2 API de Publicaciones

**Archivo**

`backend/app/publicaciones/router.py`

**Responsabilidad**

Exponer mediante HTTP las capacidades actualmente disponibles del contexto
Gestión de Publicaciones.

Actualmente proporciona:

- creación de publicaciones mediante `POST /publicaciones`;
- consulta de publicaciones mediante `GET /publicaciones`;
- validación de los datos recibidos;
- definición de los modelos utilizados por la API;
- traducción de una indisponibilidad temporal de persistencia a una respuesta
  HTTP `503 Service Unavailable`.

La API no accede directamente a SQLite.

Delega las operaciones de aplicación al Servicio de Publicaciones.

---

### 3.3 Servicio de Publicaciones

**Archivo**

`backend/app/publicaciones/service.py`

**Responsabilidad**

Coordinar las operaciones de aplicación relacionadas con publicaciones y
mantener separadas las responsabilidades HTTP de los detalles de
persistencia.

Actualmente:

- normaliza `titulo` y `descripcion`;
- normaliza el valor de `precio`;
- recibe `modalidad` y `estado`;
- solicita al repositorio la creación de una publicación;
- solicita al repositorio el listado de publicaciones;
- traduce errores de persistencia a errores propios de la capa de aplicación.

El servicio no ejecuta SQL directamente.

---

### 3.4 Repositorio de Publicaciones

**Archivo**

`backend/app/publicaciones/repository.py`

**Responsabilidad**

Encapsular el acceso productivo a la persistencia correspondiente al contexto
Gestión de Publicaciones.

Actualmente:

- crea la tabla `publicaciones` cuando es necesario;
- abre las conexiones a SQLite;
- inserta nuevas publicaciones;
- consulta publicaciones;
- detecta condiciones de bloqueo temporal de SQLite;
- encapsula los detalles concretos del mecanismo de persistencia.

Este componente constituye actualmente el **único escritor productivo** de la
entidad persistida `publicaciones`.

---

## 4. Relaciones entre componentes

El flujo principal actualmente implementado es:

```text
Frontend Web
     |
     | HTTP / JSON
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
     | SQL / sqlite3
     v
SQLite


```

La composición inicial ocurre de la siguiente manera:

```text
main.py
   |
   | registra
   v
router.py
```

Estas dependencias mantienen una dirección explícita:

```text
Router → Service → Repository → SQLite
```

No existe una dependencia inversa desde Repository hacia Service o Router.

---

## 5. Correspondencia entre C4 Nivel 3 y código

| Elemento del C4 Nivel 3 | Evidencia en el repositorio |
|---|---|
| Entrada de aplicación | `backend/app/main.py` |
| API de Publicaciones | `backend/app/publicaciones/router.py` |
| Servicio de Publicaciones | `backend/app/publicaciones/service.py` |
| Repositorio de Publicaciones | `backend/app/publicaciones/repository.py` |
| Gestión de Usuarios | `backend/app/usuarios/` |
| Catálogo | `backend/app/catalogo/` |
| Administración | `backend/app/administracion/` |
| Persistencia SQLite | acceso encapsulado en `backend/app/publicaciones/repository.py` |

La presencia de un límite estructural en el repositorio no implica que su
funcionalidad esté completamente implementada.

Por ello Usuarios, Catálogo y Administración se representan como límites
arquitectónicos definidos, pero no se documentan como componentes funcionales
ya materializados.

---

## 6. Propiedad de datos

La Evidencia S6 adopta la regla:

> Cada dato de dominio tiene un único módulo responsable de escribirlo.

En el estado actual del sistema, la entidad persistida de dominio
materializada es:

`publicaciones`

Su propietario es:

**Gestión de Publicaciones**

La escritura se encuentra encapsulada en:

`backend/app/publicaciones/repository.py`

Los campos actualmente persistidos son:

| Campo | Propietario |
|---|---|
| `id` | Gestión de Publicaciones |
| `titulo` | Gestión de Publicaciones |
| `descripcion` | Gestión de Publicaciones |
| `precio` | Gestión de Publicaciones |
| `modalidad` | Gestión de Publicaciones |
| `estado` | Gestión de Publicaciones |

Ningún otro contexto debe ejecutar directamente operaciones de escritura sobre
esta entidad.

---

## 7. Reglas entre contextos

### Gestión de Usuarios y Gestión de Publicaciones

Cuando Gestión de Usuarios sea materializada, deberá proporcionar la identidad
del estudiante mediante un contrato explícito.

Gestión de Publicaciones podrá utilizar una referencia al propietario, pero no
deberá modificar directamente los datos internos de Usuarios.

### Gestión de Publicaciones y Catálogo

Catálogo podrá utilizar publicaciones para implementar búsqueda, consulta y
filtrado.

Consumir esos datos no convierte a Catálogo en propietario de
`publicaciones`.

Catálogo no deberá ejecutar directamente operaciones `INSERT`, `UPDATE` o
`DELETE` sobre dicha entidad.

### Gestión de Publicaciones y Administración

Administración podrá solicitar acciones de moderación sobre publicaciones.

La operación deberá realizarse mediante un contrato explícito de Gestión de
Publicaciones.

Administración no deberá depender directamente del repositorio ni escribir en
la tabla `publicaciones`.

La separación documentada en S6 prevé utilizar una capa anticorrupción en este
límite cuando las capacidades de Administración sean materializadas.

---

## 8. Coherencia con C4 Nivel 2

El C4 Nivel 2 representa:

```text
Frontend Web → Backend API → SQLite
```

El C4 Nivel 3 no reemplaza esa representación.

Realiza únicamente un acercamiento al interior del contenedor:

**Backend API**

y muestra los componentes actualmente verificables responsables del corte
vertical de publicaciones.

Por tanto:

- Nivel 1 muestra CampusMarket y sus actores externos;
- Nivel 2 muestra los contenedores ejecutables;
- Nivel 3 muestra la estructura interna del Backend API.

---

## 9. Coherencia con ADR-0001

El C4 Nivel 3 no introduce un nuevo estilo arquitectónico.

CampusMarket continúa utilizando el **monolito modular** definido en:

[`ADR-0001 - Adoptar un monolito modular`](../adr/0001-usar-monolito-modular.md)

Los límites principales continúan siendo:

- `usuarios`;
- `publicaciones`;
- `catalogo`;
- `administracion`.

S6 hace explícitos sus contextos, relaciones y propiedad de datos, pero no
reemplaza, fusiona ni divide estos límites.

Por esta razón, la elaboración de este C4 Nivel 3 constituye una
profundización de la arquitectura existente y no un reajuste de los límites
que requiera reemplazar ADR-0001.

---

## 10. Relación con la Evidencia S6

Este C4 Nivel 3 debe interpretarse junto con:

- [Sección 8 de arc42 - Conceptos transversales](../arc42/08-conceptos-transversales.md)
- [Auditoría de modularidad S6](../evidencias/auditoria-modularidad-s6-2026-09-12.md)
- [ADR-0001 - Monolito modular](../adr/0001-usar-monolito-modular.md)
- [C4 Nivel 2 - Contenedores](./02-contenedores.md)
- [Fuente PlantUML del C4 Nivel 3](./03-componentes-backend.puml)

La sección 8 define los contextos y las relaciones de dominio.

La auditoría verifica esas reglas contra el código existente.

El C4 Nivel 3 permite visualizar cómo dichos límites se materializan
actualmente dentro del Backend API.

---

## 11. Estado actual y evolución

El componente con mayor materialización funcional en el backend es Gestión de
Publicaciones.

Usuarios, Catálogo y Administración mantienen sus fronteras estructurales,
pero sus capacidades todavía deberán desarrollarse progresivamente.

Cuando esos contextos sean implementados se deberá conservar la regla de
propiedad única y actualizar este C4 Nivel 3 si aparecen nuevos componentes o
cambian relaciones internas verificables.

Si una evolución futura modifica realmente los límites establecidos por
ADR-0001, el cambio deberá documentarse mediante un nuevo ADR y la
actualización correspondiente de los diagramas C4.

---

## Fuente canónica

La fuente versionada del diagrama es:

[`03-componentes-backend.puml`](./03-componentes-backend.puml)

Este archivo Markdown explica y aporta trazabilidad al diagrama, pero no
sustituye su fuente PlantUML.
