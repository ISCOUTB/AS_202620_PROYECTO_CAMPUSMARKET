# 9. Decisiones arquitectónicas

CampusMarket mantiene las decisiones arquitectónicas mediante ADR independientes. Esta sección funciona como índice vigente y evita duplicar dentro de arc42 el contenido completo de cada decisión.

Las decisiones históricas se conservan; una evolución posterior no reescribe el contexto original de un ADR aceptado.

## Índice de decisiones

| ADR | Estado | Decisión | Alcance |
|---|---|---|---|
| [ADR-0001](../adr/0001-usar-monolito-modular.md) | Aceptado | Mantener un monolito modular. | Arquitectura general |
| [ADR-0002](../adr/0002-manejo-bloqueo-sqlite.md) | Histórico - primer corte | Degradación controlada ante bloqueo temporal de SQLite. | Persistencia histórica / EC-05 |
| [ADR-0003](../adr/0003-usar-integracion-sincrona-http-json.md) | Aceptado | Integración síncrona HTTP/JSON protegida por contrato OpenAPI. | Frontend → Backend |
| [ADR-0004](../adr/0004-migrar-persistencia-a-mysql.md) | Aceptado | Migrar la persistencia vigente a MySQL. | Persistencia vigente |
| [ADR-0005](../adr/0005-desplegar-campusmarket-en-azure-y-github-pages.md) | Aceptado | Desplegar CampusMarket mediante GitHub Pages y Azure. | Despliegue |
| [ADR-0006](../adr/0006-publicar-frontend-flutter-web-en-github-pages.md) | Aceptado | Publicar Flutter Web en GitHub Pages. | Frontend |
| [ADR-0007](../adr/0007-desplegar-api-fastapi-en-azure-app-service.md) | Aceptado | Desplegar FastAPI en Azure App Service. | Backend |
| [ADR-0008](../adr/0008-desplegar-mysql-en-azure-flexible-server.md) | Aceptado | Desplegar MySQL en Azure Database for MySQL Flexible Server. | Persistencia desplegada |
| [ADR-0009](../adr/0009-materializar-catalogo-sin-romper-fronteras.md) | Aceptado | Materializar Catálogo mediante capacidad explícita de lectura de Publicaciones. | Modularidad / EC-01 |
| [ADR-0010](../adr/0010-no-incorporar-componente-generativo-en-campusmarket.md) | Aceptado | No incorporar actualmente un componente generativo dentro del producto. | IA en runtime |
| [ADR-0011](../adr/0011-gestionar-imagenes-de-publicaciones.md) | Aceptado | Gestionar hasta tres imágenes por publicación separando metadatos relacionales y archivo físico. | Publicaciones / imágenes |

## Composición vigente

```text
ADR-0001  Monolito modular
        ↓
Flutter Web / Android
        ↓
ADR-0003  HTTP/JSON síncrono + OpenAPI
        ↓
FastAPI
   ├── Catálogo
   │      ↓ capacidad explícita de lectura
   └── Publicaciones
          ↓
       repository
          ↓
ADR-0004  MySQL
```

La materialización de Catálogo sigue ADR-0009: `catalogo` no accede directamente a `publicaciones.repository`, no usa PyMySQL y no escribe los datos cuyo propietario es Gestión de Publicaciones.

La gestión de imágenes sigue ADR-0011. MySQL conserva metadatos y referencias; el filesystem local bajo `backend/uploads/` se utiliza para desarrollo y verificación local, no se presenta como almacenamiento durable de producción en Azure.

## Estado de identidad

Las operaciones de publicaciones propias utilizan actualmente `propietario_id = 1` como mecanismo temporal del prototipo. Esto no equivale a autenticación real. Por tanto, EC-02 permanece parcialmente materializado y Gestión de Usuarios continúa pendiente de materialización funcional completa.

## Decisiones históricas

ADR-0002 conserva la evidencia del comportamiento con SQLite durante el primer corte. ADR-0004 define la persistencia actual con MySQL; no se reinterpretan las mediciones históricas de SQLite como resultados de MySQL.

## Verificación

Las decisiones se contrastan con artefactos ejecutables y evidencia:

- `backend/tests/test_modularidad_s6.py` — propiedad de datos y dirección de dependencias;
- `backend/tests/test_erosion_s9.py` — frontera Catálogo → Publicaciones;
- `backend/tests/test_catalogo.py` — comportamiento de Catálogo;
- `backend/tests/test_ec01_catalogo.py` — medición de EC-01;
- `backend/tests/test_contrato_openapi.py` — contrato OpenAPI ↔ FastAPI;
- `backend/tests/test_gestion_publicaciones.py` — gestión propia e imágenes;
- `docs/evidencias/evidencia-s9-2026-10-01.md` — cadena verificable de S9.

La arquitectura vigente se describe además en:

- [C4 Nivel 2](../c4/02-contenedores.md);
- [C4 Nivel 3](../c4/03-componentes-backend.md);
- [Escenarios de calidad](10-escenarios-de-calidad.md);
- [Trazabilidad de aspectos](../aspectos.md).
