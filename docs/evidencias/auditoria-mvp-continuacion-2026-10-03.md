# Auditoría de continuación MVP — CampusMarket

Fecha: 2026-10-03 (America/Bogota). Rama: `mvp-autenticacion-producto`.
Checkpoint de entrada: `fda38976882fd5abcca8486b4b114efd28ca2b1c`.
Base de esta fase: `bfe3222c1e29dddc404560cdd9d61095d4bdb3fe`.
Esta continuación recupera el trabajo persistido; no repite la auditoría inicial.
El MVP no se despliega en Dokploy ni Azure durante esta fase.

## Checkpoint y alcance de acceso

Clon temporal desde el fork GitHub; no hay acceso al clon Windows del usuario.
Se ejecutaron branch/status/log -10/rev-parse/diff --stat y se comparó remoto.
Local y remoto eran exactamente fda3897, working tree limpio, sin cambios locales.
Cambios que existan únicamente en el PC Windows no pueden verificarse aquí.

GitHub registraba cuatro workflows y seis jobs exitosos para ese SHA. Se descargaron
los artefactos Web escritorio, Web móvil, Android y Compose y se comprobaron sus
hashes, JSON y capturas; la existencia del archivo no se tomó como aprobación.

## Requisito → implementación → ejecución → prueba → evidencia

Los resultados de esta tabla están asociados al checkpoint de entrada. La
validación del HEAD de continuación se añade al cierre, sin atribuirle resultados
de otro hash.

| Requisito | Implementación | Ejecución/prueba real | Resultado y evidencia de fda3897 |
|---|---|---|---|
| Autenticación | Usuarios, scrypt, sesiones opacas revocables | Registro/login/perfil/logout, token inventado/expirado, hashes e intentos | Suite backend, repetida en intento 2; flujo en tres plataformas |
| Propiedad y EC-02 | Identidad desde token y predicados SQL del propietario | Dos cuentas; diez mutaciones ajenas, dato comprobado tras cada ataque | 10/10 rechazadas, datos intactos; backend, flujos y Compose |
| Fotografías protegidas | Publicaciones + Pillow, UUID, límites y bloqueo de galería | Contenido disfrazado, metadatos, orientación, 12 MP, concurrencia, principal/borrado | Backend, selector real en tres plataformas y Compose |
| Cuatro contextos | Routers/services/repositories de Usuarios, Publicaciones, Catálogo y Administración | Flujo de cuenta/publicación/catálogo/reporte/revisión | Nueve comprobaciones por plataforma; ocho en Compose |
| OpenAPI v2 | `contracts/openapi-v2.json`, API 2.0.0 | Comparación exacta FastAPI y consumidor, Bearer y propietario solo salida | Cuatro pruebas de contrato aprobadas |
| Modularidad/erosión | Servicio propietario para lecturas y ocultamiento; repository por contexto | AST de imports/SQL/escritor único y mutación de frontera | Suite completa aprobada; diez mutaciones backend detectadas |
| Flutter | SessionController, navegación, perfil, galería y moderación | analyze, seis pruebas y dos mutaciones | Flutter CI aprobado |
| Build Web/Android | SDK Flutter 3.47.3; Web y APK debug | `flutter build web`, `flutter build apk --debug` | Artefacto compilado por hash; no se afirma APK release firmado |
| Flujo real | `integration_test/mvp_flow_test.dart` con backend/MySQL | Chrome 1440×1000, Chrome 390×844, Android API 35 emulado | Nueve comprobaciones y 19 capturas por plataforma |
| Persistencia/recursos | Compose, API/MySQL 256 MiB cada uno, volúmenes y un worker | Recrear contenedores; mismo token/publicación/foto; trabajo concurrente | Sin OOM; API peak 195.084.288 bytes, DB 190.177.280 bytes |
| EC-01 | Consulta de imágenes en lote por servicio de Publicaciones | Diez búsquedas HTTP de 1000 filas bajo cuota | 10/10 <2 s, 152,70–198,04 ms; loopback, no red pública |

Ejecuciones verificadas:

- [Backend, intento 2](https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37141901670): relanzado durante esta continuación, MySQL 8.4 real, Ruff verde, 73 pruebas funcionales/arquitectónicas en 96,21 s y cuatro de contrato; diez mutaciones detectadas.
- [Flutter](https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37141901640): analyze, tests, dos mutaciones y builds.
- [Flujos Web/Android](https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37141901660): artefactos `flujo-<plataforma>-fda38976882fd5abcca8486b4b114efd28ca2b1c`.
- [Compose](https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37141901649): artefacto `compose-verificado-fda38976882fd5abcca8486b4b114efd28ca2b1c`.

## Validación ejecutada en el entorno de continuación

Python 3.12.14. Dependencias fijadas instaladas realmente, `pip check` aprobado.
Ruff 0.16.9: sin hallazgos. Contrato, modularidad, erosión y propiedad de datos:
15 pruebas aprobadas. El entorno impide crear sockets UNIX: MySQL local no pudo
arrancar; por eso las pruebas que requieren SQL se volvieron a ejecutar en GitHub
con MySQL real y no se sustituyó el motor ni se simularon resultados.

## Cambios de esta continuación

- `requirements.txt` contiene runtime; `requirements-dev.txt` conserva pytest/httpx
  existentes para tests. El Dockerfile instala solo runtime. El job backend usa dev.
- Pillow 12.3.0 continúa necesario según ADR-0015. Metadatos oficiales PyPI:
  Python >=3.10, licencia MIT-CMU y wheels CPython 3.12 Linux x86_64/Windows amd64.
  Instalación Linux comprobada. pytest-cov ausente, sin dependencias nuevas de producto.
- C4 L1/L2/L3, arc42 y aspectos ahora describen los cuatro contextos, identidad real,
  tablas con único escritor, contrato v2, fotografías y preparación Compose.
  Se conservan evidencia histórica y contenido de todos los ADR aceptados.
- UX: se revisaron capturas de escritorio, móvil y Android. Los textos de beneficios
  de Inicio ahora explican búsqueda, detalles y gestión para el estudiante.
  Los cambios de copy se validan en los flujos del nuevo HEAD antes de cerrarlos.
- Ruff se amplía a `backend` y `scripts` en CI. Se corrigieron dos espaciados de
  imports del medidor histórico y se hizo explícito `check=False` en el verificador
  de mutaciones Flutter, que debe inspeccionar el retorno de una prueba que falla.

## Barrido de secretos y consistencia

Gitleaks 8.30.1, binario verificado por checksum oficial. Historial de fase:
21 commits entre base y checkpoint, 349.678 bytes, cero hallazgos. Se escanea
también el working tree de continuación con redacción total en logs.
El barrido sin configuración detectó dos coincidencias: ambas son el `Project Key`
público de SonarCloud en la evidencia S7. Se preserva el dato histórico y se usa
una excepción exacta, limitada a ese archivo y regla, manteniendo todas las reglas
por defecto. La excepción se comprobó con un token sintético: continúa detectado.
Barrido clasificado: cero hallazgos; artefactos de checkpoint: cero hallazgos.
Las contraseñas fijas de los servicios CI son fixtures desechables, no credenciales
de entornos reales. Compose usa secretos efímeros fuera de Git y artefactos.
No se afirma ausencia universal de secretos: se informa el alcance escaneado.

`git diff --check` aprobado; ningún ADR aceptado modificado. Los enlaces locales de
los documentos actualizados se comprueban tras incorporar esta auditoría.

## Cierre del HEAD de continuación

Continuación publicada: `266a08d36e1770bfb7922103eedcf778ecdcf8f1`.
Backend: Ruff y 73+4 pruebas aprobadas; diez mutaciones detectadas. Flutter:
analyze, seis tests, dos mutaciones, build Web y APK debug aprobados. Flujos Web
escritorio/móvil: nueve comprobaciones y 19 capturas por plataforma, aprobados.
Compose: ocho comprobaciones, EC-02 10/10 con datos intactos, persistencia tras
recreación y EC-01 10/10 (290,26–299,59 ms).

Android en ese SHA terminó rojo: aunque completó las nueve comprobaciones,
Flutter detectó un SemanticsHandle activo al cerrar el test. Ese JSON no acredita
una ejecución aprobada. El asistente invocaba UiAutomation continuamente incluso
con CampusMarket en primer plano. Se limita la lectura nativa a DocumentsUI y el
test exige recuperar el número inicial de handles antes de finalizar. El relleno
de campos reutiliza la espera de control alcanzable para evitar taps durante un
cambio de teclado/layout.

Corrección validada: `094eaaa97bd0984af012a219c6b2ccad1e23e1c2`.
Los cuatro workflows y seis jobs finalizaron aprobados. Android completa los
nueve checks y 19 capturas; el driver registra `semantics_handles_restored=true`
y Flutter informa `All tests passed`. Web escritorio/móvil también pasan con el
helper corregido. Las verificaciones finales de Flutter permanecen activas.

| Bloque de 094eaaa | Prueba realmente ejecutada | Evidencia |
|---|---|---|
| Backend | Ruff backend/scripts; 73+4 tests; 10/10 mutaciones detectadas | [Run 37151076285](https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37151076285) |
| Flutter | analyze sin incidencias; 6 tests; 2 mutaciones; Web y APK debug compilados | [Run 37151076275](https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37151076275) |
| Flujo funcional | Chrome escritorio/móvil y Android API 35; 9 checks y 19 capturas por plataforma; handles Android restaurados | [Run 37151076247](https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37151076247) |
| Compose | 8 checks; EC-02 10/10 intacto; EC-01 10/10, 252,77–298,51 ms; recreación 12.995,02 ms | [Run 37151076227](https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37151076227) |

Compose conserva 256 MiB por contenedor, API uid 10001, sin OOM ni reinicios
inesperados. Pico API 180.269.056 bytes; MySQL 188.833.792 bytes. Pillow y las
dependencias runtime separadas construyen y ejecutan la imagen real correctamente.

UX inspeccionada en capturas descargadas del checkpoint y Web de 266a08d con los
textos nuevos; las tres plataformas de 094eaaa repiten la comprobación de ausencia
de excepciones de layout/imagen en cada captura. Los logs y JSON emitidos por el
driver acreditan el flujo y hash; el resultado se exige junto al job aprobado.
El traslado local de los ZIP nuevos no completó y el entorno terminó desconectado
(409 environment_offline). Los artefactos permanecen disponibles en el run citado.
No se atribuye revisión visual local a archivos que no pudieron descargarse.

Los cuatro cambios documentales que estaban preparados localmente se reconstruyen
desde los archivos exactos de 094eaaa y se guardan mediante GitHub. El cierre añade
al workflow backend la misma auditoría Gitleaks 8.30.1 ya ejecutada en esta fase:
descarga oficial con SHA-256 fijado, historial desde la base y checkout completo,
informes redactados fuera del repositorio. No es dependencia del producto.
También exige checkout CI limpio después de pruebas/mutaciones y registra su SHA.
Ese resultado debe distinguirse del scratch desconectado y del PC Windows inaccesible.

Restricciones/estrategia conservan su contexto histórico explícito; glosario y
C4 L1 incorporan Web/Android, estados reales, sesiones, propiedad y moderación.
El commit de cierre modifica documentación, verificaciones CI y asistencia nativa
del test, sin cambiar runtime del producto. Sus checks deben consultarse por SHA;
094eaaa no sustituye al CI final.

Se conserva el commit remoto adicional `7c73279` (selector con ANR del launcher,
confirmaciones localizadas y celda de imagen única). Como volvía a consultar
UiAutomation con la app activa, el cierre pausa ese asistente cuando CampusMarket
es la actividad resumida y mantiene el manejo de las pantallas nativas. La aserción
de handles restaurados se conserva y la implementación combinada debe superar el
flujo Android del nuevo HEAD; la ejecución de 094eaaa no valida esta combinación.


Fuente primaria del mecanismo de UiAutomation/semántica:
[flutter/flutter #129231](https://github.com/flutter/flutter/issues/129231),
contrastada con `SemanticsBinding` y `WidgetTester` de Flutter 3.47.3.

SonarCloud permanece pendiente. Crear el PR oficial con el conector devolvió
HTTP 403, `Resource not accessible by integration`; no se creó ningún PR ni merge.
La consulta directa al proyecto SonarCloud desde este entorno devuelve CloudFront
403; ese resultado no es un fallo del Quality Gate ni acredita un gate verde.
El fork no registra un análisis Sonar del nuevo HEAD. Se requiere acceso autorizado
al repositorio oficial/PR y al análisis para poder cerrar ese criterio.

## Límites explícitos del MVP

- Sesión del cliente solo en memoria; no verificación de correo/afiliación ni recuperación de contraseña.
- Moderador por ID comprobado externamente; revisar allowlist al reprovisionar SQL.
- SQL y archivos usan compensación; crash puede requerir reconciliación de huérfanos.
- Resolución de reporte y ocultamiento usan dos transacciones MySQL; ante fallo parcial puede quedar revisión pendiente para reintento.
- Android se verifica en emulador y APK debug; prueba en teléfono físico del usuario no se ejecuta aquí.
- No hay medición pública del MVP ni despliegue del nuevo SHA. HTTPS y almacenamiento durable se validarán en el siguiente bloque.

La validación del checkout final y CI se acredita por SHA en GitHub. El scratch
quedó inaccesible tras la desconexión y su status posterior no pudo consultarse.
Solo se declarará cierre completo cuando SonarCloud también acredite ese HEAD. La fase siguiente será despliegue,
con autorización independiente; esta auditoría no lo ejecuta.
