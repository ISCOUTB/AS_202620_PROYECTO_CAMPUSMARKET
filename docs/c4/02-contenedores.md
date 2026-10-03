# C4 Nivel 2 - Contenedores de CampusMarket

Fuente canónica: [02-contenedores.puml](02-contenedores.puml).
El backend conserva una única unidad de ejecución FastAPI (ADR-0001).

| Pieza | Tecnología y responsabilidad | Correspondencia |
|---|---|---|
| Frontend | Flutter/Dart, Web y Android; catálogo, autenticación, perfil, publicaciones y moderación | `frontend/campusmarket/lib/` |
| Backend API | Python 3.12/FastAPI; cuatro contextos, contrato y autorización | `backend/app/` |
| Base de datos | MySQL 8.4; seis tablas con único escritor por contexto | repositories de Usuarios, Publicaciones y Administración |
| Archivos | Fotos verificadas/reencodificadas; referencia en MySQL | `publicaciones/image_storage.py`, `CAMPUSMARKET_UPLOAD_DIR` |

Estudiantes consultan públicamente y se autentican para publicar, gestionar su
contenido o reportar. Moderadores comprobados revisan reportes, ocultan o descartan
con nota. El frontend usa HTTP/JSON síncrono y multipart; las operaciones protegidas
incluyen Bearer. HTTPS será obligatorio para exposición pública.

Contrato vigente: [OpenAPI v2](../../contracts/openapi-v2.json), API 2.0.0.
`test_contrato_openapi.py` compara FastAPI con ese archivo. v1 se conserva como historia.

## Persistencia y fronteras

Los routers delegan en sus services y estos en sus repositories. `db.py` comparte
la conexión/transacción. Usuarios escribe usuarios/sesiones/intentos;
Publicaciones escribe publicaciones/fotos; Administración escribe reportes.
Catálogo lee a través del servicio de Publicaciones. Administración solicita
ocultamiento por ese servicio y no escribe sus tablas.

Los archivos se sirven públicamente desde `/uploads`; las mutaciones de galería
requieren propietario autenticado. ADR-0015 exige decodificación/reencodificación,
nombres aleatorios, límites de tamaño/píxeles y limpieza al eliminar.

## Topología de verificación y próxima fase

ADR-0018 prepara API y MySQL en Compose, 256 MiB/0,5 CPU por contenedor, worker
único y dos volúmenes nombrados para datos y fotos. CI verifica persistencia al
recrear ambos contenedores. Solo el override local publica API en loopback.
La preparación no acredita un despliegue público del MVP.

Durante S8 se verificó una línea base en Pages → Azure App Service → Azure MySQL.
Es historia de otra revisión. El siguiente bloque será despliegue; esta fase no
efectúa operaciones en Dokploy ni Azure.

Véanse [C4 Nivel 3](03-componentes-backend.md), [arc42 despliegue](../arc42/07-vista-despliegue.md)
y [auditoría de continuación](../evidencias/auditoria-mvp-continuacion-2026-10-03.md).
