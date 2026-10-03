# C4 Nivel 3 - Componentes del Backend API de CampusMarket

Fuente canónica: [`03-componentes-backend.puml`](./03-componentes-backend.puml).

El Backend API continúa siendo una única unidad de despliegue FastAPI dentro del monolito modular.

## Contextos

| Contexto | Código | Estado |
|---|---|---|
| Gestión de Usuarios | `backend/app/usuarios/` | Límite definido; autenticación real pendiente |
| Gestión de Publicaciones | `backend/app/publicaciones/` | Materializado |
| Catálogo | `backend/app/catalogo/` | Materializado |
| Administración | `backend/app/administracion/` | Límite definido; no materializado completamente |

## Componentes vigentes

### Entrada de aplicación

`backend/app/main.py`

Configura FastAPI, CORS, routers, health y el montaje local de `/uploads`.

### Catálogo

- API: `backend/app/catalogo/router.py`
- Servicio: `backend/app/catalogo/service.py`

Catálogo implementa búsqueda, filtros, composición y detalle. Consume capacidades de lectura del servicio de Publicaciones y no accede directamente a `publicaciones.repository` ni a MySQL.

```text
Flutter
  ↓ GET /catalogo
API Catálogo
  ↓
Servicio Catálogo
  ↓ capacidad de lectura
Servicio Publicaciones
```

### Gestión de Publicaciones

- API: `backend/app/publicaciones/router.py`
- Servicio: `backend/app/publicaciones/service.py`
- Repositorio: `backend/app/publicaciones/repository.py`
- Almacenamiento local de imágenes: `backend/app/publicaciones/image_storage.py`

La dirección principal permanece:

```text
router → service → repository → MySQL
```

El repositorio concentra el acceso relacional mediante PyMySQL.

Entidades materializadas:

- `publicaciones`;
- `publicacion_imagenes`.

Operaciones principales:

```text
POST   /publicaciones
GET    /publicaciones
GET    /publicaciones/mias
PUT    /publicaciones/{publication_id}
PATCH  /publicaciones/{publication_id}/estado
DELETE /publicaciones/{publication_id}
POST   /publicaciones/{publication_id}/imagenes
```

## Imágenes

ADR-0011 separa los metadatos relacionales del archivo físico. En desarrollo local los archivos se almacenan bajo `backend/uploads/publicaciones/` y MySQL conserva metadatos y referencias.

El filesystem local no se presenta como almacenamiento durable de producción.

## Propiedad de datos

| Dato | Propietario | Escritor productivo |
|---|---|---|
| `publicaciones` | Gestión de Publicaciones | `backend/app/publicaciones/repository.py` |
| `publicacion_imagenes` | Gestión de Publicaciones | `backend/app/publicaciones/repository.py` |

Catálogo no adquiere propiedad de escritura por consumir estos datos.

## Identidad

Las operaciones propias usan actualmente `propietario_id = 1` como mecanismo temporal del prototipo. No equivale a autenticación real; EC-02 permanece parcialmente materializado.

## Contrato

Contrato: [`contracts/openapi-v1.json`](../../contracts/openapi-v1.json).

Prueba: [`backend/tests/test_contrato_openapi.py`](../../backend/tests/test_contrato_openapi.py).

## Verificación arquitectónica

- `test_modularidad_s6.py`: escritor único, aislamiento de persistencia y dirección de dependencias;
- `test_erosion_s9.py`: impide acceso de Catálogo al repositorio/PyMySQL/escrituras directas;
- `test_catalogo.py`: comportamiento funcional de Catálogo;
- `test_gestion_publicaciones.py`: gestión propia e imágenes;
- `test_publicaciones_vertical.py`: corte vertical y persistencia;
- `test_contrato_openapi.py`: OpenAPI frente a FastAPI.

## Decisiones relacionadas

- ADR-0001 — monolito modular;
- ADR-0003 — integración síncrona HTTP/JSON;
- ADR-0004 — MySQL;
- ADR-0009 — Catálogo consume capacidad explícita de lectura de Publicaciones;
- ADR-0011 — gestión de imágenes.
