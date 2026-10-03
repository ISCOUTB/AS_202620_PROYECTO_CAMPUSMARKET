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
| [ADR-0012](../adr/0012-autenticar-con-sesiones-opacas-revocables.md) | Aceptado | Sesiones opacas revocables e identidad real. | Usuarios / EC-02 |
| [ADR-0013](../adr/0013-materializar-reportes-y-moderacion-minima.md) | Aceptado; habilitación de moderadores sustituida por ADR-0014 | Reportes y moderación mínima. | Administración |
| [ADR-0014](../adr/0014-habilitar-moderadores-por-identificador-interno.md) | Aceptado | Moderadores por ID de cuenta comprobada. | Autorización |
| [ADR-0015](../adr/0015-validar-y-reencodificar-imagenes-con-pillow.md) | Aceptado | Decodificar y sanitizar contenido real con Pillow. | Seguridad de imágenes |
| [ADR-0016](../adr/0016-ajustar-recursos-a-la-cuota-del-laboratorio.md) | Aceptado | Acotar memoria, concurrencia y cuerpos HTTP. | Recursos |
| [ADR-0017](../adr/0017-serializar-inicializacion-y-migracion-de-identidad.md) | Aceptado | Lock MySQL y migración de identidad única. | Persistencia |
| [ADR-0018](../adr/0018-ejecutar-el-monolito-en-dokploy-con-volumenes.md) | Aceptado para preparación; despliegue pendiente | Compose con volúmenes para la próxima fase. | Operación |
| [ADR-0019](../adr/0019-consultar-imagenes-en-lote-a-traves-de-publicaciones.md) | Aceptado | Lectura de imágenes en lote por el service propietario. | Catálogo / rendimiento |

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

La gestión de imágenes sigue ADR-0011/0015/0016. MySQL conserva metadatos;
Compose usa un volumen nombrado (ADR-0018). Azure requiere almacenamiento durable.
Usuarios y Administración persisten sus tablas en sus repositories; Catálogo
consume el service de Publicaciones. Los cuatro contextos están materializados.

## Estado de identidad

Usuarios resuelve sesiones opacas revocables; Publicaciones usa el ID autenticado
en los predicados SQL. EC-02 se verifica con dos cuentas y 10/10 ataques rechazados.
Registro/perfil no conceden moderación: se habilita externamente por ID comprobado.
Véase la [auditoría de continuación](../evidencias/auditoria-mvp-continuacion-2026-10-03.md).

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
