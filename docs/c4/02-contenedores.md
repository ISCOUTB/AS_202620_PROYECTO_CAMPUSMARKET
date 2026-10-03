# C4 Nivel 2 - Contenedores de CampusMarket

Fuente canónica del diagrama:

[`02-contenedores.puml`](./02-contenedores.puml)

Este nivel representa las unidades ejecutables principales de CampusMarket y sus relaciones técnicas. El backend continúa siendo una única unidad de despliegue y mantiene el estilo de **monolito modular** definido en ADR-0001.

---

## Contenedores vigentes

| Contenedor | Tecnología | Responsabilidad |
|---|---|---|
| Frontend | Flutter / Dart | Interfaz Web y Android para Inicio, Catálogo, detalle, Publicar y Mis publicaciones. |
| Backend API | FastAPI / Python 3.12 | Expone HTTP/JSON, contrato OpenAPI, Catálogo, Gestión de Publicaciones, health y observabilidad. |
| Persistencia | MySQL 8.4 | Conserva publicaciones y metadatos relacionales de imágenes. |
| Archivos de imágenes | Filesystem local de desarrollo | Conserva archivos JPG/JPEG/PNG/WEBP durante desarrollo y verificación local. |

Topología vigente:

```text
Estudiante
    ↓
Flutter Web / Android
    ↓ HTTP/JSON + multipart
FastAPI
    ├── Catálogo
    └── Publicaciones
            ↓ PyMySQL / SQL
           MySQL
            ↓ referencia
     archivos de imágenes
```

El filesystem local de imágenes **no se presenta como almacenamiento durable de producción**. ADR-0011 indica que un despliegue productivo de esta capacidad debe evaluar almacenamiento de objetos persistente manteniendo MySQL para metadatos y referencias.

---

## Actores

### Estudiante

Utiliza CampusMarket para:

- consultar el catálogo;
- buscar y filtrar productos;
- ver detalle;
- crear publicaciones;
- cargar imágenes;
- listar publicaciones propias;
- editar;
- cambiar estado operativo;
- eliminar.

### Administrador

Permanece como actor y límite arquitectónico previsto para supervisión y moderación. Su funcionalidad no se considera completamente materializada.

---

## Relaciones

### Estudiante → Frontend

```text
Estudiante
    ↓
Interacción Web / Android
    ↓
Flutter
```

### Frontend → Backend API

Comunicación principal:

- HTTP/HTTPS;
- JSON;
- estilo REST;
- síncrona;
- `multipart/form-data` para imágenes.

La superficie vigente incluye operaciones de salud, Catálogo y Gestión de Publicaciones. El contrato versionado se mantiene en:

[`contracts/openapi-v1.json`](../../contracts/openapi-v1.json)

La correspondencia proveedor ↔ contrato se verifica automáticamente mediante:

[`backend/tests/test_contrato_openapi.py`](../../backend/tests/test_contrato_openapi.py)

### Backend API → MySQL

```text
FastAPI
   ↓
Gestión de Publicaciones
   ↓
repository.py
   ↓ PyMySQL / SQL
MySQL
```

El acceso productivo a MySQL está encapsulado en:

`backend/app/publicaciones/repository.py`

Catálogo no accede directamente a MySQL ni importa el repositorio de Publicaciones.

### Backend API → archivos de imágenes

En desarrollo local:

```text
FastAPI
   ↓
image_storage.py
   ↓
backend/uploads/publicaciones/<id>/...
```

Los metadatos y referencias permanecen en MySQL; el binario no se guarda como BLOB/Base64 en la tabla `publicaciones`.

---

## Correspondencia con el repositorio

| Elemento C4 | Evidencia |
|---|---|
| Frontend | `frontend/campusmarket/lib/` |
| Backend API | `backend/app/` |
| Catálogo | `backend/app/catalogo/` |
| Gestión de Publicaciones | `backend/app/publicaciones/` |
| MySQL | `backend/app/publicaciones/repository.py` |
| Archivos de imágenes | `backend/app/publicaciones/image_storage.py` |
| Contrato OpenAPI | `contracts/openapi-v1.json` |

---

## Corte funcional vigente

El recorrido verificable principal es:

```text
Flutter
   ↓ HTTP/JSON
FastAPI
   ├── Catálogo → capacidad de lectura de Publicaciones
   └── Publicaciones → service → repository
                               ↓
                              MySQL
```

Para imágenes:

```text
Flutter
   ↓ POST /publicaciones
FastAPI / Publicaciones
   ↓
MySQL
   ↓ id
Flutter
   ↓ POST /publicaciones/{id}/imagenes
FastAPI
   ├── filesystem local de desarrollo
   └── metadatos → MySQL
```

---

## Propiedad y fronteras

Gestión de Publicaciones mantiene la propiedad de escritura de:

- `publicaciones`;
- `publicacion_imagenes`.

Catálogo materializa consulta, búsqueda, filtros, composición y detalle, pero no se convierte en propietario de la persistencia.

La regla se verifica mediante:

- `backend/tests/test_modularidad_s6.py`;
- `backend/tests/test_erosion_s9.py`.

---

## Identidad

Las operaciones de publicaciones propias utilizan actualmente `propietario_id = 1` como mecanismo temporal del prototipo.

Este dato no debe interpretarse como autenticación real. El contexto Usuarios continúa pendiente de materialización completa y EC-02 permanece parcialmente materializado.

---

## Evolución histórica

Durante el primer corte la persistencia fue SQLite. Posteriormente evolucionó a MySQL mediante ADR-0004. Las referencias a SQLite se conservan en evidencias y ADR históricos, pero no representan la persistencia vigente.

Durante S8 se desplegó la línea base:

```text
GitHub Pages → Azure App Service → Azure Database for MySQL
```

Las capacidades añadidas posteriormente en la rama `producto-marketplace-ui` no se consideran desplegadas públicamente hasta realizar un nuevo despliegue y verificar el mismo hash.
