# 3. Contexto y alcance

CampusMarket centraliza venta/alquiler entre estudiantes. El estudiante consulta
catálogo y detalle públicos; se registra/inicia sesión para publicar, editar,
cambiar disponibilidad, gestionar fotografías, actualizar perfil o reportar.
El moderador habilitado por ID comprobado revisa reportes y oculta/descarta con nota.
Los actores y el sistema se muestran en [C4 Nivel 1](../c4/01-contexto.md).

## 3.2 Alcance funcional

Los cuatro contextos están materializados al nivel MVP: Usuarios, Publicaciones,
Catálogo y Administración. Registro por correo/contraseña no verifica afiliación
universitaria ni titularidad del correo. El MVP no ofrece pagos, banca, envíos,
logística, chat, recuperación de contraseña ni verificación de correo.

## 3.3 Interfaces externas

Flutter Web/Android consume FastAPI/Python 3.12 mediante HTTP/JSON síncrono y
multipart para fotografías. Bearer identifica las operaciones protegidas.
MySQL 8.4 es accesible únicamente por repositories del backend, mediante PyMySQL.
El cliente no accede a SQL. Fotos visibles se leen por `/uploads`; el directorio
se configura por entorno y se conserva en volumen durante la verificación Compose.

Desarrollo/verificación usan HTTP loopback; exposición pública requiere HTTPS.
La base de pruebas termina en `_test` y contiene exclusivamente fixtures propios.
Las credenciales proceden de variables de entorno, fuera de Git.

## 3.4 Contrato de API

[OpenAPI v2](../../contracts/openapi-v2.json) publica API 2.0.0 / OpenAPI 3.1.0.
Incluye usuarios, catálogo, publicaciones/galería, reportes/revisión y health.
`test_contrato_openapi.py` compara exactamente contrato y proveedor.
v1 permanece como referencia histórica anterior a la identidad real.

## 3.5 Historia y entorno

SQLite corresponde al primer corte y ADR-0002. MySQL sigue ADR-0004.
El despliegue S8 corresponde a una revisión anterior; la rama MVP no está
desplegada. ADR-0018 prepara la fase siguiente, sin ejecutarla.
Véanse [C4 Nivel 2](../c4/02-contenedores.md),
[vista de ejecución](06-vista-ejecucion.md) y
[auditoría](../evidencias/auditoria-mvp-continuacion-2026-10-03.md).
