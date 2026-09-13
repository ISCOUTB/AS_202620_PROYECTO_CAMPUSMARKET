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
