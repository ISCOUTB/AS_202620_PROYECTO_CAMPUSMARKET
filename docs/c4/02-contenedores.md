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
incluyen Bearer. La exposición pública vigente utiliza HTTPS.

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

## Topología pública y topología de medición

Flutter Web está publicado en GitHub Pages:
https://nnigarp.github.io/AS_202620_PROYECTO_CAMPUSMARKET/.
Su bundle consume https://campusmarket.iscoutb.dev por HTTPS. Ese dominio expone
la API FastAPI en Dokploy; /health y /docs responden HTTP 200. MySQL y las fotos
permanecen en los volúmenes nombrados del Compose de ADR-0018.

API y MySQL tienen 256 MiB/0,5 CPU por contenedor y la API un worker.
CI recrea ambos contenedores y mide EC-01 con 1000 filas reales mediante HTTP
loopback/MySQL bajo cuota. Este resultado no equivale a latencia de navegador
público. El registro público de recreación acredita API, no recreación de MySQL.

Frontend fuente c38e0cf; API observada 7856416; repositorio auditado b5f10a2.
El código relevante es idéntico entre esas revisiones; sus resultados se citan
por separado en el [complemento S9](../evidencias/evidencia-s9-2026-10-01.md#17-complemento-final-de-auditoria-s9--4-de-octubre-de-2026).
Pages → Azure App Service → Azure MySQL se conserva como línea base histórica S8.

Véanse [C4 Nivel 3](03-componentes-backend.md), [arc42 despliegue](../arc42/07-vista-despliegue.md)
y [auditoría de continuación](../evidencias/auditoria-mvp-continuacion-2026-10-03.md).
