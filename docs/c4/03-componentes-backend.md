# C4 Nivel 3 - Componentes del Backend API de CampusMarket

Fuente canónica: [03-componentes-backend.puml](03-componentes-backend.puml).
El backend es una sola aplicación FastAPI: monolito modular, cuatro contextos
materializados al nivel MVP y una única base MySQL. Estado de verificación en
[auditoría de continuación](../evidencias/auditoria-mvp-continuacion-2026-10-03.md).

## Componentes y propiedad de datos

| Contexto | Entrada y servicio | Repositorio / datos propios | Estado MVP |
|---|---|---|---|
| Usuarios | `usuarios/router.py`, `service.py`, `dependencies.py`, `security.py` | `usuarios/repository.py`: `usuarios`, `sesiones_usuario`, `intentos_autenticacion` | Registro, login, perfil, sesión y logout |
| Publicaciones | `publicaciones/router.py`, `service.py`, `image_storage.py` | `publicaciones/repository.py`: `publicaciones`, `publicacion_imagenes` | CRUD propio, disponibilidad y galería |
| Catálogo | `catalogo/router.py`, `service.py` | Sin tablas ni SQL propios; lee por el servicio de Publicaciones | Búsqueda, filtros, tarjetas y detalle |
| Administración | `administracion/router.py`, `service.py` | `administracion/repository.py`: `reportes_publicacion` | Reportar, cola de revisión, ocultar o descartar con nota |

Las rutas son relativas a `backend/app/`. `main.py` registra los cuatro routers,
CORS, manejo de errores, límites HTTP, observabilidad, health y lectura pública de
`/uploads`. `db.py` comparte conexión/transacción, sin SQL de dominio.

## Relaciones permitidas

- Cada router delega en su service; cada service persiste mediante su repository.
- Publicaciones obtiene identidad por `usuarios/dependencies.py`; el usuario
  autenticado procede del hash del token vigente en MySQL, no del body o query.
- Catálogo consume `listar_publicaciones`, `listar_imagenes_publicaciones` y
  `listar_imagenes_publicacion` de Publicaciones. La lectura en lote evita una
  conexión por fila y preserva la propiedad de datos (ADR-0019).
- Administración consulta/oculta por el servicio de Publicaciones. Solo escribe
  sus reportes; una revisión bloquea el reporte para impedir decisiones simultáneas.
- Ningún contexto importa un repository ajeno. No hay microservicios ni Shared
  Kernel de entidades. La dirección sigue `router → service → repository → MySQL`.

## Identidad y fotografías

ADR-0012 fija sesiones Bearer opacas revocables y scrypt para contraseñas.
Flutter conserva el token en memoria: reinicio/recarga requiere login.
`propietario_id` es salida y predicado SQL de autorización. Las publicaciones
heredadas quedan sin propietario y fuera del catálogo hasta atribución comprobada.
ADR-0014 habilita moderadores por ID de una cuenta comprobada, en configuración
externa y vacío por defecto; no hay ascenso desde registro o perfil.

Publicaciones guarda el archivo con nombre aleatorio después de decodificar,
orientar, reducir a 2048 px y reencodificar con Pillow. El límite es tres imágenes,
5 MiB y 20 MP de entrada. MySQL conserva metadatos y referencias. Los archivos de
publicaciones visibles se leen públicamente; subir, cambiar principal y eliminar
exigen propietario autenticado. SQL y filesystem no comparten transacción:
compensación y reconciliación de huérfanos siguen ADR-0015.

El directorio se configura con `CAMPUSMARKET_UPLOAD_DIR`. Compose conserva el
directorio en un volumen nombrado (ADR-0018), probado tras recrear contenedores.
El MVP aún no está desplegado; Azure debe disponer de almacenamiento durable
antes de habilitar esta capacidad.

## Contrato y verificación

Contrato vigente: [OpenAPI v2](../../contracts/openapi-v2.json), API 2.0.0.
v1 permanece como evidencia histórica. `test_contrato_openapi.py` exige igualdad
exacta con FastAPI y Bearer en las operaciones protegidas.

Pruebas: `test_propiedad_datos.py`, `test_modularidad_s6.py`,
`test_erosion_s9.py`, `test_usuarios.py`, `test_ec02_autorizacion.py`,
`test_imagenes_seguras.py`, `test_administracion.py`, `test_catalogo.py`.
Las mutaciones comprueban que los tests fallan ante suplantación, password
incorrecto, moderación sin capacidad, archivo disfrazado o erosión de fronteras.

Decisiones aplicadas: ADR-0001/0003/0004/0009 y ADR-0011 a ADR-0019.
El índice de [decisiones](../arc42/09-decisiones.md) mantiene sus estados y enlaces.
