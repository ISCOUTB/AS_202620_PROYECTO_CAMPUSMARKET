# Uso de Inteligencia Artificial - CampusMarket

Este documento registra el uso de herramientas de IA como apoyo al proyecto. Todo resultado se revisa antes de incorporarse y las decisiones finales corresponden al equipo.

## Evidencia S1

| Fecha | Herramienta | Uso realizado | Verificación del equipo | Qué se rechazó y por qué |
|---|---|---|---|---|
| 08/08/2026 | ChatGPT | Apoyo para analizar ideas y estructurar problema, objetivo y alcance inicial. | Se contrastó con el alcance acordado por el equipo. | Se descartaron funcionalidades de pagos y envíos porque excedían el alcance del semestre. |
| 08/08/2026 | ChatGPT | Apoyo para organizar documentación inicial y mantenibilidad. | Se revisó antes de subir al repositorio. | Se descartó ampliar el prototipo con funciones no necesarias para S1. |

## Evidencia S2

| Fecha | Herramienta | Uso realizado | Verificación del equipo | Qué se rechazó y por qué |
|---|---|---|---|---|
| 16/08/2026 | ChatGPT | Apoyo para estructurar arc42 1–3 y restricciones. | Se contrastó con la actividad de S2. | Se rechazaron restricciones que eran requisitos funcionales y no restricciones arquitectónicas. |
| 16/08/2026 | ChatGPT | Apoyo para formular escenarios y árbol de utilidad. | Se verificó que cada escenario tuviera las seis partes y medida numérica. | Se descartaron medidas no verificables o formuladas de manera subjetiva. |
| 16/08/2026 | ChatGPT | Apoyo para C4 Nivel 1 mediante PlantUML. | Se verificaron actores, relaciones, leyenda y alcance. | Se descartaron actores o integraciones que no pertenecían al alcance actual. |

## Evidencia S3

| Fecha | Herramienta | Uso realizado | Verificación del equipo | Qué se rechazó y por qué |
|---|---|---|---|---|
| 17-23/08/2026 | ChatGPT | Comparación de arquitectura en capas, hexagonal y monolito modular. | Se contrastó con EC-01 a EC-04 y las restricciones del proyecto. | Se descartó recomendar microservicios porque no era una alternativa solicitada y añadía complejidad innecesaria. |
| 17-23/08/2026 | ChatGPT | Apoyo para redactar ADR-0001 y tácticas. | El equipo revisó contexto, alternativas, decisión y consecuencias. | Se descartó arquitectura hexagonal como decisión actual por su mayor costo de abstracción para el alcance. |
| 23/08/2026 | ChatGPT | Apoyo para organizar el esqueleto FastAPI, prueba de salud y documentación. | Se comprobó mediante GitHub Actions. | Se descartó implementar lógica de negocio completa porque S3 pedía únicamente el esqueleto ejecutable. |

## Evidencia S4

| Fecha | Herramienta | Uso realizado | Verificación del equipo | Qué se rechazó y por qué |
|---|---|---|---|---|
| 25/08/2026 | ChatGPT | Auditoría de CampusMarket contra la ficha oficial de S4 y el feedback del curso. | Se contrastaron los 10 criterios uno por uno con el repositorio. | Se descartó crear C4 Nivel 3 porque la actividad lo pospone a Semana 6. |
| 25/08/2026 | ChatGPT | Apoyo para diseñar el corte vertical crear publicación: Flutter → FastAPI → SQLite. | Se revisó que atraviese interfaz, lógica y persistencia y que corresponda con ADR-0001. | Se descartó documentar MySQL como persistencia implementada porque todavía no existe en el código. |
| 25/08/2026 | ChatGPT | Apoyo para arc42 5, 6, 9, 12, C4 Nivel 2 y trazabilidad. | Se verificó que la documentación describa únicamente elementos presentes en la propuesta de implementación S4. | Se descartó copiar el contenido del ADR dentro de la sección 9; se mantiene un enlace al ADR. |
| 28/08/2026 | ChatGPT | Revisión de la retroalimentación provisional de S4 y apoyo para ajustar arc42 sección 3, coherencia entre C4 Nivel 1 y Nivel 2, correspondencia con el código y trazabilidad. | El equipo contrastó los ajustes con la ficha S4, el estado real del repositorio y las evidencias existentes antes de incorporarlos. | Se rechazó incluir routers, servicios, repositorios y otros detalles internos dentro del C4 Nivel 2 porque ese nivel de detalle corresponde al C4 Nivel 3 y no era requerido para S4. |
| 29/08/2026 | GitHub Copilot | Generación automática de sugerencias para mensajes y descripciones de commits durante la actualización documental del repositorio. | El equipo revisó las sugerencias antes de confirmar los cambios y mantuvo únicamente las que resultaban coherentes con el cambio realizado. | Se rechazaron mensajes genéricos sugeridos automáticamente y se reemplazaron por mensajes específicos como `Completar README con evidencia verificable de S4`, para mantener mayor trazabilidad en el historial del repositorio. |
| 29/08/2026 | ChatGPT | Auditoría final de la Evidencia S4 y apoyo para completar el README con arranque, corte vertical, pruebas, GitHub Actions, arc42, C4 y trazabilidad. | Se verificó en `master` que el README estuviera completo y que el pipeline ejecutara correctamente las pruebas del backend. | Se rechazó introducir SonarCloud apresuradamente en este cierre y modificar nuevamente el ADR-0001, porque no eran cambios necesarios para resolver los hallazgos principales de la ficha S4 y podían introducir inconsistencias innecesarias. |
| 30/08/2026 | ChatGPT | Revisión de la última retroalimentación automática de S4 y apoyo para hacer explícitas en el README las evidencias que el agente no había podido verificar: glosario de dominio y trazabilidad ASP-05. | El equipo comprobó que `docs/arc42/12-glosario.md` y `docs/aspectos.md` ya contenían la información requerida y expuso esa evidencia en el README sin modificar la arquitectura ni el código. | Se rechazó alterar nuevamente los documentos arquitectónicos solo para satisfacer la extracción del agente; se mantuvo la información original y únicamente se hizo más visible y navegable desde el README. |

## Evidencia S5

| Fecha | Herramienta | Uso realizado | Verificación del equipo | Qué se rechazó y por qué |
|---|---|---|---|---|
| 04/09/2026 | ChatGPT | Apoyo para revisar la retroalimentación S1-S4, organizar `correcciones.md`, verificar la trazabilidad de ADR-0001 y revisar el arranque reproducible del sistema. | El equipo contrastó los cambios con el feedback oficial, verificó el PR #5 y el commit `4dd857a`, y ejecutó el arranque con FastAPI, Flutter Web y `/health`. | Se rechazó marcar elementos como saneados sin evidencia y modificar ADR-0001 únicamente para agregar trazabilidad posterior. |
| 05/09/2026 | ChatGPT | Apoyo para revisar SonarQube Cloud y definir el reto arquitectónico S5 a partir del estado real de CampusMarket. | Se verificó el proyecto oficial de SonarQube Cloud y se midió la línea base del bloqueo SQLite: HTTP `500`, `7.323 s`, sin escritura parcial y recuperación HTTP `201`. | Se rechazó usar el monolito modular como nueva restricción y agregar PostgreSQL, colas, cachés o nuevos servicios sin evidencia que lo justificara. |
| 06/09/2026 | ChatGPT | Apoyo para comparar alternativas, definir ADR-0002, implementar la degradación controlada ante bloqueo SQLite y revisar la trazabilidad de S5. | El equipo obtuvo `3 passed`, `flutter analyze` sin errores y una medición formal de HTTP `503` en `1.283 s`, sin escritura parcial y con recuperación HTTP `201`. | Se rechazó migrar la persistencia o agregar infraestructura porque R-07 exige mantener SQLite y conservar el backend como una única aplicación monolítica modular, sin crear nuevos servicios desplegables. También se descartó el reintento automático por su impacto potencial en el umbral de `≤ 2 s`. |

## Evidencia S6

**Fecha:** 12/09/2026

| Herramienta | Uso realizado | Verificación del equipo | Qué se rechazó y por qué |
|---|---|---|---|
| ChatGPT | Apoyo para interpretar la Evidencia S6, identificar los contextos delimitados de CampusMarket y estructurar el lenguaje ubicuo, mapa de contextos y propiedad de datos. | Se contrastó la propuesta con los módulos reales `usuarios`, `publicaciones`, `catalogo` y `administracion`, y con el estado actual del código. | Se rechazó declarar como implementadas capacidades de Usuarios, Catálogo y Administración que todavía no están materializadas en el repositorio. |
| ChatGPT | Apoyo para auditar la modularidad del backend y localizar operaciones de persistencia relacionadas con `publicaciones`. | Se revisaron `backend/app/publicaciones/`, `backend/app/usuarios/`, `backend/app/catalogo/`, `backend/app/administracion/`, pruebas y scripts. Se confirmó que el escritor productivo de `publicaciones` se encuentra en `backend/app/publicaciones/repository.py`. | Se rechazó afirmar que existían escrituras compartidas sin evidencia. Los accesos SQLite de pruebas y medición se clasificaron como instrumentación y no como módulos de dominio propietarios. |
| ChatGPT | Apoyo para documentar los riesgos MOD-01 a MOD-04 y definir reglas preventivas de comunicación entre contextos. | Los riesgos se contrastaron con el mapa de contextos y con la regla de dueño único de datos de S6. | Se rechazó crear nuevos microservicios, bases de datos o infraestructura únicamente para demostrar separación entre contextos. |
| ChatGPT | Apoyo para actualizar la trazabilidad de S6 en `docs/aspectos.md` y revisar si era necesario modificar C4 Nivel 3 o generar un nuevo ADR. | Se verificó que S6 mantiene los límites principales del monolito modular definidos anteriormente y que no introduce un nuevo estilo arquitectónico. | Se descartó crear un ADR nuevo o modificar artificialmente los límites solo para aumentar la documentación, porque la actividad los exige únicamente si los límites cambian respecto al corte anterior. |

### Actualización S6 — 13/09/2026

| Herramienta | Uso realizado | Verificación del equipo | Qué se rechazó y por qué |
|---|---|---|---|
| ChatGPT | Apoyo para completar el C4 Nivel 3 del Backend y revisar su correspondencia con la implementación real. | Se contrastó el diagrama con `main.py`, `router.py`, `service.py`, `repository.py` y SQLite. | Se rechazó presentar Usuarios, Catálogo y Administración como funcionalidades ya implementadas. |
| ChatGPT | Apoyo para incorporar `backend/tests/test_modularidad_s6.py` y reforzar la auditoría de propiedad de datos. | Se verificó que la prueba controle el escritor único de `publicaciones`, las dependencias entre módulos y el acceso a SQLite. GitHub Actions finalizó con las pruebas en verde. | Se rechazó crear pruebas sobre capacidades que todavía no existen en el código. |
| ChatGPT | Apoyo para actualizar la trazabilidad documental de S6 en README, `docs/aspectos.md` y arc42. | Se revisó que los documentos apunten a C4 Nivel 3, auditoría, propiedad de datos y prueba automática sin contradecir ADR-0001. | Se rechazó crear un nuevo ADR porque los límites definidos en el primer corte no cambiaron. |
| ChatGPT | Apoyo para la revisión final de S6 contra los criterios de la actividad. | Se contrastaron los artefactos con el estado actual de `master`, las pruebas de GitHub Actions y el Quality Gate de SonarQube Cloud. | Se rechazó agregar microservicios, nueva infraestructura o documentación artificial que no correspondiera con el repositorio. |

## Evidencia S7

**Fecha:** 15/09/2026

| Herramienta | Uso realizado | Verificación del equipo | Qué se rechazó y por qué |
|---|---|---|---|
| ChatGPT | Apoyo para contrastar la ficha S7 con la API realmente implementada y definir el alcance del contrato. | Se localizaron `GET /health`, `GET /publicaciones` y `POST /publicaciones` en FastAPI y se comprobaron sus consumidores y pruebas existentes. | Se rechazó inventar endpoints, mensajería o eventos porque no existen en el código actual y no corresponden al alcance de S7. |
| ChatGPT | Apoyo para estructurar OpenAPI 3.1, la prueba de correspondencia y el escenario EC-06. | Se ejecutaron las 11 pruebas y se confirmó la igualdad entre el contrato `1.0.0` y el esquema del proveedor, además de las necesidades del consumidor Flutter. | Se rechazó considerar la documentación automática de Swagger como prueba suficiente; por sí sola no bloquea cambios incompatibles. |
| OpenAPI Generator | Generación reproducible de un cliente Dart a partir de `contracts/openapi-v1.json`. | OpenAPI Generator 7.25.0 produjo las operaciones `crearPublicacion`, `listarPublicaciones` y `consultarSalud` a partir de los `operationId` del contrato. | Se rechazó incorporar un segundo cliente productivo al frontend porque `publicaciones_api.dart` ya cubre el corte actual y mantener ambos duplicaría responsabilidades. |
| ChatGPT | Apoyo para comparar integración síncrona y asíncrona y redactar ADR-0003. | La decisión se contrastó con el flujo Flutter-FastAPI, EC-05, EC-06 y la ausencia de infraestructura de mensajería. | Se descartó la integración asíncrona para crear/listar publicaciones porque eliminaría la confirmación inmediata y obligaría a diseñar estados pendientes, reintentos, idempotencia y consistencia eventual sin evidencia que lo justifique. |
| ChatGPT | Apoyo para diseñar y documentar la mutación incompatible `titulo` → `nombre`. | La prueba de contrato produjo `exit code 1` con `1 failed, 2 passed`; tras restaurar `titulo`, el conjunto completo volvió a verde. | Se rechazó conservar el cambio incompatible o debilitar la prueba para hacerla pasar, porque rompería al consumidor Flutter. |
| ChatGPT | Apoyo para hacer explícita la prueba de contrato en el pipeline, diseñar la mutación controlada de `operationId`, consolidar la evidencia real y auditar el cierre de S7. | Se verificó la ejecución roja con `1 failed, 10 passed` y `exit code 1`; después de restaurar `crearPublicacion`, las ejecuciones del fork y del PR #38 finalizaron en verde con las pruebas funcionales y de contrato separadas. SonarQube Cloud reportó Quality Gate aprobado y cero problemas nuevos. | Se rechazó conservar el cambio incompatible `registrarPublicacion`, debilitar la comparación entre OpenAPI y FastAPI, o declarar cerrado el trabajo sin comprobar las ejecuciones reales de GitHub Actions. |

### Actualización S7 — 16/09/2026

| Herramienta | Uso realizado | Verificación del equipo | Qué se rechazó y por qué |
|---|---|---|---|
| ChatGPT | Apoyo para revisar la observación docente sobre persistencia y planear la migración de SQLite a MySQL sin modificar las fronteras del monolito modular. | Se contrastó la propuesta con `repository.py`, la arquitectura vigente y las pruebas. Se implementó MySQL mediante PyMySQL encapsulado en el repositorio de Publicaciones. | Se rechazó mantener SQLite como persistencia vigente y se evitó alterar los límites del monolito modular por un cambio exclusivamente tecnológico de persistencia. |
| ChatGPT | Apoyo para redactar ADR-0004 y alinear C4, arc42 y la trazabilidad arquitectónica con la persistencia MySQL, preservando SQLite únicamente donde corresponde como evidencia histórica. | Se revisaron ADR-0004, C4 Niveles 1, 2 y 3, arc42 y `docs/aspectos.md` contra la implementación actual. | Se rechazó reescribir las evidencias históricas de S4 y S5 como si MySQL hubiera sido utilizado originalmente en esos cortes. |
| ChatGPT | Apoyo para adaptar GitHub Actions a una base MySQL de CI y revisar las pruebas funcionales, de modularidad y de contrato. | Se ejecutó `python -m pytest backend/tests -q` y se verificó el pipeline con MySQL, pruebas del backend, SonarCloud y análisis de código. | Se rechazó incorporar credenciales locales o reales dentro del repositorio o del workflow. |
| ChatGPT | Apoyo para revisar la coherencia entre el contrato OpenAPI, FastAPI, la persistencia vigente y la documentación del proyecto. | Se contrastaron `contracts/openapi-v1.json`, FastAPI, C4, ADR-0003, ADR-0004, README y pruebas automatizadas. | Se rechazó presentar SQLite como tecnología vigente o confundir las decisiones históricas con el estado arquitectónico actual. |
| ChatGPT | Auditoría de cierre documental de S7. | Se corrigió el formato de `docs/aspectos.md`, se aclaró el estado histórico de ADR-0002 en `docs/arc42/09-decisiones.md`, se revisaron referencias SQLite/MySQL y se mejoró el script de arranque para validar la disponibilidad de MySQL. | Se rechazó eliminar ADR, mediciones, scripts o evidencias históricas únicamente por contener referencias a SQLite, ya que forman parte de la trazabilidad real del proyecto. |

### Saneamiento posterior a revisión automática S7 — 17/09/2026

| Herramienta | Uso realizado | Verificación del equipo | Qué se rechazó y por qué |
|---|---|---|---|
| ChatGPT | Apoyo para revisar los hallazgos de la pasada temprana del agente y localizar la evidencia real de S7. | Se contrastaron `contracts/openapi-v1.json`, FastAPI, `test_contrato_openapi.py`, el workflow, `docs/aspectos.md`, README y los runs de GitHub Actions. | Se rechazó modificar arquitectura, endpoints o contrato solo para mejorar el resultado del revisor; los hallazgos principales requerían hacer visible evidencia ya existente. |
| ChatGPT | Apoyo para sanear la evidencia S7 y hacer explícitos schemas, correspondencia contrato ↔ código, historial Git, ejecución contractual en CI y fallo ante incompatibilidad. | Se verificaron OpenAPI `3.1.0`, API `1.0.0`, `POST /publicaciones`, `GET /publicaciones`, `GET /health`, commit `485249a`, Run #93 verde y un run rojo real por cambio incompatible. | Se rechazó declarar cumplimiento únicamente mediante texto; se utilizaron rutas, commits y ejecuciones reproducibles. |
| ChatGPT | Apoyo para reforzar la trazabilidad en `docs/aspectos.md`, README, arc42 sección 6 y C4 Nivel 2. | Se comprobó ASP-07, se corrigió el formato Markdown de la vista de ejecución y se repararon los enlaces hacia ADR-0004 sin modificar código, contrato ni ADR aceptados. | Se rechazó modificar ADR-0003 o introducir cambios arquitectónicos innecesarios durante el saneamiento documental. |
| ChatGPT | Apoyo para revisar el estado de SonarQube Cloud y la configuración oficial del proyecto. | Se verificó el proyecto `ISCOUTB_AS_202620_PROYECTO_CAMPUSMARKET`, Quality Gate aprobado y análisis público. El workflow aún no invoca explícitamente el scanner. | Se rechazó restaurar una configuración personal, duplicar mecanismos de análisis o declarar cerrado Sonar sin scanner en CI y un run exitoso asociado. |

### Cierre documental S7 — 18/09/2026

| Herramienta | Uso realizado | Verificación del equipo | Qué se rechazó y por qué |
|---|---|---|---|
| ChatGPT | Apoyo para realizar la auditoría final de S7, actualizar la evidencia consolidada y alinear README con el estado real de `master`, GitHub Actions y SonarQube Cloud. | Se verificó el proyecto oficial `ISCOUTB_AS_202620_PROYECTO_CAMPUSMARKET`, la organización `isco-utb`, Quality Gate `Passed`, la configuración `.sonarcloud.properties` y el pipeline estable de `master`. GitHub Actions volvió a finalizar correctamente después de los ajustes documentales. | Se rechazó declarar como cumplida la integración del scanner sin un run exitoso que lo ejecutara y se rechazó conservar en `master` una configuración conocida como fallida únicamente para aparentar cumplimiento. |
| ChatGPT | Apoyo para evaluar una integración explícita del scanner de SonarQube Cloud desde GitHub Actions y determinar la causa de su imposibilidad actual. | La validación controlada permitió comprobar que la ejecución del scanner sobre el proyecto oficial requiere una credencial con autorización para ejecutar análisis en la organización `isco-utb`. Después de la comprobación se preservó el workflow estable de `master`. | Se rechazó utilizar el proyecto personal de SonarQube Cloud como sustituto del proyecto oficial del curso y se rechazó mantener una integración que dejara el pipeline principal en rojo por falta de autorización. |

---

## Evidencia S8

**Fecha:** 21-27/09/2026

| Herramienta | Uso realizado | Verificación del equipo | Qué se rechazó y por qué |
|---|---|---|---|
| ChatGPT | Apoyo para interpretar literalmente la ficha oficial de S8 y separar los criterios de despliegue reproducible, CI, health check, observabilidad, secretos, costos y documentación arquitectónica. | El equipo contrastó cada criterio contra la ficha oficial, el repositorio y resultados reales de ejecución antes de declararlo cumplido. | Se rechazó considerar un criterio cumplido únicamente porque existiera un archivo o una configuración. Se exigió requisito → implementación → ejecución real → evidencia verificable. |
| ChatGPT | Apoyo para revisar el estado inicial de S8 y organizar una matriz de cumplimiento antes de modificar el sistema. | Se contrastaron código, documentación, workflows, persistencia vigente y arquitectura real antes de implementar cambios. | Se rechazó reutilizar evidencia histórica de SQLite como si describiera el estado vigente de MySQL. |
| ChatGPT | Apoyo para diseñar e implementar un health check dependiente de la disponibilidad real de MySQL. | Se verificó `GET /health` con MySQL disponible obteniendo HTTP `200`; con la base detenida se obtuvo HTTP `503`; al restablecerla volvió a HTTP `200`. | Se rechazó utilizar un health check que comprobara únicamente que FastAPI estuviera ejecutándose, porque no evidenciaría el estado de la dependencia principal. |
| ChatGPT | Apoyo para estructurar logs HTTP en formato estructurado con campos operativos verificables. | En la ejecución real de Azure App Service se observaron campos como `timestamp`, `level`, `event`, `request_id`, `method`, `path`, `status_code` y `duration_ms`. | Se rechazó considerar mensajes libres de consola como evidencia equivalente a logs estructurados. |
| ChatGPT | Apoyo para implementar una métrica operacional consultable mediante `GET /ops/metrics/ec01`. | Se generaron solicitudes reales y se observaron 10 de 10 dentro del objetivo de `2000 ms`, con un máximo aproximado de `164.41 ms` y `meets_backend_target: true`. | Se rechazó presentar esta medición como validación completa extremo a extremo de EC-01, porque mide principalmente el comportamiento del backend y no toda la experiencia desde Flutter Web. |
| ChatGPT | Apoyo para incorporar Ruff al pipeline y revisar el workflow de GitHub Actions junto con MySQL 8.4 y las pruebas automatizadas. | El workflow ejecutó análisis estático, servicio MySQL, pruebas funcionales, arquitectónicas y de contrato. Después del merge S8, el job `test` sobre `master` terminó en `success`. | Se rechazó declarar el pipeline cerrado utilizando solamente ejecuciones de la rama de trabajo; se verificó nuevamente el estado del merge en `master`. |
| ChatGPT | Apoyo para preparar FastAPI para Azure App Service mediante configuración por entorno, TLS hacia MySQL y CORS para el frontend público. | Se comprobó el backend público, `/health`, la preflight `OPTIONS /publicaciones` desde `https://nnigarp.github.io` y posteriormente un `POST /publicaciones` real desde Flutter Web. | Se rechazó desactivar TLS, hardcodear credenciales o utilizar una política CORS más abierta de la necesaria. |
| ChatGPT | Apoyo para desplegar FastAPI en Azure App Service y MySQL en Azure Database for MySQL Flexible Server. | Se verificó que el backend público accede realmente a MySQL y que una publicación creada desde la interfaz pública queda persistida y puede recuperarse posteriormente. | Se rechazó considerar una captura del portal de Azure como evidencia suficiente del despliegue. La validación se realizó mediante URL pública y comportamiento funcional. |
| ChatGPT | Apoyo para versionar la infraestructura de Azure mediante `infra/main.bicep`. | La plantilla fue compilada con `az bicep build` y validada mediante `az deployment group validate`, obteniendo `provisioningState: Succeeded` y `error: null`. | Se rechazó documentar solamente comandos manuales de creación de recursos como si fueran infraestructura reproducible. |
| ChatGPT | Apoyo para proteger secretos mediante parámetros seguros de Bicep, App Settings y variables de entorno. | Se revisó que la contraseña real de MySQL no quedara almacenada en el código, Bicep ni documentación versionada. | Se rechazó escribir credenciales reales en archivos del repositorio o evidencias. |
| ChatGPT | Apoyo para hacer configurable la URL del backend en Flutter mediante `CAMPUSMARKET_API_BASE_URL` y preparar el build Web de producción. | Se ejecutó `flutter analyze`, se generó el build con la URL pública de Azure y se comprobó posteriormente desde navegador. | Se rechazó mantener `localhost:8000` como backend fijo para el frontend de producción. |
| ChatGPT | Apoyo para publicar Flutter Web mediante GitHub Pages. | El build fue publicado en la rama `gh-pages`, el workflow de Pages finalizó correctamente y la aplicación quedó accesible públicamente. | Se rechazó considerar el build local como evidencia de publicación mientras todavía no existiera una URL pública verificable. |
| ChatGPT | Apoyo para detectar una inconsistencia documental en la interfaz que todavía indicaba `Flutter → FastAPI → SQLite`. | Se verificó el código fuente, se corrigió el texto a `CampusMarket S8: Flutter Web → FastAPI → MySQL en Azure.`, se reconstruyó y republicó el frontend, y después se comprobó visualmente la versión pública corregida. | Se rechazó dejar una interfaz públicamente desplegada que contradijera la arquitectura vigente. |
| ChatGPT | Apoyo para actualizar arc42 sección 7 con la vista de despliegue real y sección 2 con restricciones operativas de S8. | La documentación se contrastó con GitHub Pages, Azure App Service, Azure MySQL, Bicep, health check y observabilidad realmente ejecutados. | Se rechazó conservar la descripción histórica en la que el proveedor cloud aparecía todavía como pendiente. |
| ChatGPT | Apoyo para redactar ADR-0005 y documentar las consecuencias de distribuir frontend, backend y persistencia entre GitHub Pages y Azure. | Se contrastó la decisión con la topología realmente desplegada y con la continuidad del monolito modular. | Se rechazó describir el despliegue como una migración a microservicios, porque las fronteras de dominio del backend no cambiaron. |
| ChatGPT | Apoyo para documentar costo mensual, supuestos y punto de ruptura. | Se utilizó la configuración realmente observada: App Service F1 y Azure MySQL `Standard_B1ms`, 1 vCore, 2 GiB y 32 GiB; la estimación aproximada observada para MySQL fue `USD 14.71/mes` antes de beneficios académicos. | Se rechazó presentar los créditos académicos como garantía permanente de costo cero o inventar una factura no observada. |
| ChatGPT | Apoyo para definir un procedimiento de rollback reproducible a partir de un commit conocido. | Se documentó el uso de `git archive` y `az webapp deploy` para backend y la republicación de un `build/web` conocido para frontend. | Se rechazó definir rollback únicamente como “volver a una versión anterior” sin pasos ejecutables. |
| ChatGPT | Apoyo para consolidar la evidencia S8 en `docs/evidencias/evidencia-s8-2026-09-27.md` y actualizar el README con el estado de operación real. | Se contrastaron URLs, infraestructura, CI, health, observabilidad, costos, rollback y documentación con los artefactos y resultados ejecutados durante S8. | Se rechazó utilizar solamente capturas de paneles de proveedor como sustituto de evidencia reproducible. |
| ChatGPT | Auditoría final del PR #43 y del estado de `master`. | El PR `S8 - Despliegue y operación de CampusMarket` fue integrado al repositorio oficial. El merge commit `bea2412082b0acb2dc37262376622d63fccff5df` produjo un job `test` exitoso y SonarQube Cloud reportó `Quality Gate passed`. | Se rechazó cerrar S8 usando únicamente el hash de la rama `S8-despliegue-operacion`; la referencia de cierre debía corresponder a `master`. |

### Evidencias verificables de S8

La validación realizada durante S8 utilizó, entre otros, los siguientes
artefactos:

- `infra/main.bicep`;
- `.github/workflows/backend-tests.yml`;
- `backend/app/main.py`;
- `backend/app/publicaciones/repository.py`;
- `backend/tests/test_health.py`;
- `backend/tests/test_publicaciones_vertical.py`;
- `backend/tests/test_contrato_openapi.py`;
- `docs/arc42/02-restricciones.md`;
- `docs/arc42/07-vista-despliegue.md`;
- `docs/arc42/ARC42.md`;
- `docs/adr/0005-desplegar-campusmarket-en-azure-y-github-pages.md`;
- `docs/evidencias/evidencia-s8-2026-09-27.md`;
- `README.md`.

### Estado de cierre revisado con apoyo de IA

```text
Repositorio:
ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET

PR:
#43 - S8 - Despliegue y operación de CampusMarket

Merge commit:
bea2412082b0acb2dc37262376622d63fccff5df

Rama:
master

GitHub Actions:
success

SonarQube Cloud:
Quality Gate passed

Frontend:
https://nnigarp.github.io/AS_202620_PROYECTO_CAMPUSMARKET/

Backend:
https://campusmarket-s8-api-nilver.azurewebsites.net

Health:
https://campusmarket-s8-api-nilver.azurewebsites.net/health
```

## Evidencia S9

**Fecha:** 01/10/2026

| Herramienta | Uso realizado | Verificación del equipo | Qué se rechazó y por qué |
|---|---|---|---|
| ChatGPT | Apoyo para identificar una porción real de CampusMarket que permitiera materializar ASP-01 y EC-01 sin romper el monolito modular. Se propuso implementar Catálogo con búsqueda, filtros y detalle consumiendo una capacidad de lectura de Publicaciones. | El equipo contrastó la propuesta con ADR-0001, la propiedad de datos definida en S6 y el riesgo MOD-01. Se verificó que `publicaciones` permanezca como único propietario de persistencia. | Se rechazó que `catalogo` accediera directamente a MySQL o importara `backend/app/publicaciones/repository.py`, porque eso introduciría un segundo módulo acoplado a la persistencia y erosionaría la frontera definida en S6. |
| ChatGPT | Apoyo para redactar ADR-0009 y estructurar alternativas: acceso directo a MySQL, servicio independiente y consumo de una capacidad explícita de lectura de Publicaciones. | El equipo mantuvo el monolito modular, descartó nuevos servicios desplegables y dejó ADR-0009 en estado `Propuesto` hasta completar implementación, pruebas y medición. | Se rechazó introducir microservicios para Catálogo porque no existe evidencia de escalado o aislamiento que justifique esa complejidad. |
| ChatGPT | Apoyo para implementar `backend/app/catalogo/service.py`, `router.py` y registrar el nuevo router en FastAPI. | Se ejecutaron pruebas funcionales del catálogo, pruebas de contrato OpenAPI y pruebas de modularidad. El contrato versionado se regeneró desde `app.openapi()` y volvió a coincidir con el proveedor. | Se rechazó editar manualmente partes aisladas del contrato OpenAPI porque el contrato versionado debe corresponder exactamente con el esquema generado por FastAPI. |
| ChatGPT | Apoyo para diseñar pruebas funcionales del Catálogo con datos controlados mediante `monkeypatch`. | `backend/tests/test_catalogo.py` verificó listado, búsqueda por texto, filtros por modalidad, estado y precio, detalle y errores controlados. Resultado: `8 passed`. | Se corrigió una primera versión de pruebas que dependía de una instancia MySQL local sin credenciales cargadas. Se evitó confundir una falla de infraestructura con una falla de lógica del Catálogo. |
| ChatGPT | Apoyo para diseñar `backend/tests/test_erosion_s9.py` como regla ejecutable de arquitectura. | La prueba verificó que Catálogo no importe el repositorio de Publicaciones, no use PyMySQL y no ejecute escrituras SQL directas. Resultado normal: `3 passed`. | Se rechazó dejar la restricción únicamente documentada. Se exigió una prueba automática capaz de detectar una violación real. |
| ChatGPT | Apoyo para realizar una mutación controlada agregando temporalmente `from backend.app.publicaciones import repository` dentro de Catálogo. | La ejecución produjo `1 failed, 2 passed` y falló específicamente `test_catalogo_no_importa_repository_de_publicaciones`. Tras retirar la mutación, la prueba volvió a `3 passed`. | Se rechazó conservar la importación directa del repositorio o debilitar la prueba para hacerla pasar, porque esa dependencia viola la frontera acordada. |
| ChatGPT | Apoyo para diseñar la medición controlada de EC-01 con 1.000 publicaciones y 10 búsquedas consecutivas. | `backend/tests/test_ec01_catalogo.py` obtuvo `10/10` ejecuciones bajo 2 segundos, promedio `0.020482 s` y máximo `0.050431 s`. La prueba terminó con `1 passed`. | Se rechazó declarar esta medición como validación productiva completa porque usa publicaciones controladas mediante `monkeypatch` y no incluye latencia real de MySQL ni red. |
| ChatGPT | Apoyo para corregir el manejo de indisponibilidad de persistencia en la consulta de publicaciones. | `listar_publicaciones()` traduce `PersistenceUnavailableError` a `PublicationPersistenceUnavailableError`, y el router de Catálogo responde con HTTP `503` controlado. | Se rechazó permitir que la excepción de PyMySQL escapara directamente hasta la capa HTTP, porque expondría detalles internos y produciría comportamiento no controlado. |

---

## Actualización de producto — 02–03/10/2026

| Herramienta | Uso realizado | Verificación del equipo | Qué se corrigió o rechazó y por qué |
|---|---|---|---|
| ChatGPT | Apoyo para evolucionar la interfaz Flutter hacia una experiencia de marketplace responsive con Inicio, Catálogo, detalle, Publicar y Mis publicaciones. | Se ejecutó la aplicación en Android y se recorrieron flujos reales contra FastAPI y MySQL. `flutter analyze` terminó con `No issues found!`. | Se rechazó copiar de referencias visuales funciones que no existen en el backend, como favoritos, mensajería, vendedor verificado, ubicación, perfil, reservas o contacto. Mostrar controles falsos habría hecho divergir la interfaz de las capacidades reales. |
| ChatGPT | Apoyo para diseñar la carga de hasta tres imágenes por publicación y mantener la propiedad del dato dentro de Gestión de Publicaciones. | Se verificó creación real con tres imágenes, lectura desde Catálogo, visualización de imagen principal y galería, y respuesta de imágenes en Mis publicaciones. La suite backend terminó con `36 passed`. | Se rechazó almacenar imágenes como BLOB/Base64 dentro de `publicaciones` y se rechazó que Catálogo accediera directamente a la persistencia. La decisión quedó formalizada en ADR-0011. |
| ChatGPT | Apoyo para implementar Mis publicaciones: listar, editar, cambiar estado y eliminar. | En Android se creó una publicación real, se comprobó su aparición en Catálogo y Mis publicaciones y se probaron edición, cambio de estado y eliminación. | Se corrigió la interpretación de identidad: `propietario_id = 1` se conserva únicamente como mecanismo temporal y no se presenta como autenticación implementada. |
| ChatGPT | Apoyo para detectar y corregir overflows de tarjetas responsive en Catálogo e Inicio. | Los defectos fueron observados en ejecución Android mediante `RenderFlex overflowed`; después de los ajustes y hot restart la interfaz dejó de mostrar la franja de overflow. `flutter analyze` permaneció limpio. | Se rechazó ocultar el error visual o considerarlo irrelevante solo porque el flujo funcional continuaba operando. |
| ChatGPT | Apoyo para sincronizar el contrato OpenAPI después de ampliar la respuesta de `/publicaciones/mias` con imágenes. | `backend/tests/test_contrato_openapi.py` terminó con `3 passed`; la suite completa terminó con `36 passed`. | Se rechazó restaurar el snapshot anterior para forzar las pruebas a verde. El contrato se actualizó para representar el proveedor real. |
| ChatGPT | Auditoría final de modularidad y trazabilidad antes del cierre. | Se revisó `test_modularidad_s6.py`, la dirección `router → service → repository → MySQL`, la dependencia Catálogo → servicio de Publicaciones y el working tree limpio antes del bloque documental. | Se rechazó declarar EC-02 como completamente cumplido porque el escenario exige usuarios autenticados distintos y esa capacidad todavía no existe. También se corrigió la duplicación de numeración ADR: la gestión de imágenes pasó a ADR-0011 y ADR-0010 permanece como la decisión S9 sobre no incorporar un componente generativo. |

### Resultado de verificación del 03/10/2026

```text
backend completo:
36 passed, 2 warnings

contrato OpenAPI:
3 passed

Flutter:
No issues found!

git diff --check:
sin errores
```

La generación asistida no se considera evidencia suficiente por sí sola. Los
cambios anteriores fueron contrastados con ejecución real, pruebas automáticas,
análisis estático y las fronteras arquitectónicas vigentes.

## Criterio de uso

La IA se utiliza como apoyo para análisis, documentación, organización, comparación de alternativas y revisión técnica.

El equipo mantiene la responsabilidad de:

- revisar cada propuesta antes de incorporarla;
- ejecutar directamente las pruebas y mediciones;
- contrastar las recomendaciones con el estado real del repositorio;
- aceptar, corregir o rechazar las propuestas de IA con justificación técnica;
- tomar y defender las decisiones arquitectónicas finales.

Las propuestas generadas por IA no se consideran evidencia por sí mismas. La evidencia utilizada por el proyecto corresponde a resultados verificables del repositorio, pruebas ejecutadas, mediciones, documentación trazable y decisiones revisadas por el equipo.
## 2026-10-03 — MVP bloque 1: identidad real y propiedad

| Propuesta IA | Decisión del equipo | Motivo / verificación |
|---|---|---|
| Sesión opaca revocable, scrypt estándar | Aceptado | ADR-0012; prueba real de registro/login, expiración y reutilización tras logout |
| Derivar propietario de sesión; no aceptar ID en body | Aceptado | Dos cuentas reales, EC-02 10/10; datos revisados después de cada intento |
| Allowlist de moderadores por correo sin verificar | Rechazado y corregido | Permite registrar un correo privilegiado; ADR-0014 usa IDs de cuentas comprobadas fuera del flujo público |
| Asignar datos heredados al primer usuario | Rechazado | Propiedad no demostrada; preservar filas en cuarentena sin propietario |
| Considerar rowcount=0 como falta de permiso | Corregido | MySQL cuenta filas cambiadas: PUT/PATCH idénticos son válidos; comprobar lectura acotada por propietario |
| Repetir contraseña en error de validación | Rechazado | Respuesta de validación solo contiene loc/msg/type; nunca input |
| Añadir JWT, OAuth, recuperación o roles amplios | Rechazado | No necesarios para el MVP; no se añadieron dependencias de producto |
| Instalar httpx2 para eliminar aviso de deprecación | Rechazado en este bloque | httpx existente pasa las pruebas; aviso documentado, sin añadir dependencia por estética |

Herramienta: Codex. Revisado con Ruff, pruebas sobre MySQL 8.0.46 aislado,
contrato v2 y mutaciones en copias temporales. Las tres mutaciones (autoría SQL,
contraseña ignorada y acceso a repository ajeno) hacen fallar una aserción;
no se consideran detectadas por errores de colección. No se exponen tokens,
contraseñas ni hashes reales en documentación.

## 2026-10-03 — MVP bloque 2: imágenes y administración

| Propuesta IA | Decisión | Motivo / verificación |
|---|---|---|
| Validar imágenes solo por extensión o firma manual | Rechazado | No asegura decodificación ni retiro de metadatos |
| Pillow 12.3.0 como única dependencia nueva del backend | Aceptado | PyPI oficial: Python >=3.10, CPython 3.12 Linux/Windows, licencia MIT-CMU, código python-pillow; ADR-0015 |
| pytest-cov como dependencia del proyecto | Rechazado | No es necesario para este bloque; pruebas reales y mutaciones verifican el defecto |
| Reportes reales y moderación por ID de cuenta comprobada | Aceptado | ADR-0013 y 0014; registro/perfil no pueden conceder capacidad |
| Panel de métricas o botones ficticios | Rechazado | No hay requisito ni contrato ejecutable que justifique esa interfaz |
| Resolver reportes sin exclusión mutua | Corregido | Mantener la fila de reporte bloqueada durante la revisión; ocultado de publicación idempotente por servicio |
| Elegir principal y retirar fotos desde el router/SQL ajeno | Rechazado | Router→service→repository; único escritor y propiedad comprobados |
| Limitar imágenes solo desde Flutter | Rechazado | Límite tres bajo lock en MySQL; cuatro subidas concurrentes producen 3×201 + 1×400 |

Verificación: 66 pruebas pasan sobre MySQL real; imágenes decodificadas,
metadatos retirados, autorización y concurrencia; pruebas AST de propiedad
por tabla y de imports. No se alteraron ADR aceptados.
