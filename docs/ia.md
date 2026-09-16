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

## Criterio de uso

La IA se utiliza como apoyo para análisis, documentación, organización, comparación de alternativas y revisión técnica.

El equipo mantiene la responsabilidad de:

- revisar cada propuesta antes de incorporarla;
- ejecutar directamente las pruebas y mediciones;
- contrastar las recomendaciones con el estado real del repositorio;
- aceptar, corregir o rechazar las propuestas de IA con justificación técnica;
- tomar y defender las decisiones arquitectónicas finales.

Las propuestas generadas por IA no se consideran evidencia por sí mismas. La evidencia utilizada por el proyecto corresponde a resultados verificables del repositorio, pruebas ejecutadas, mediciones, documentación trazable y decisiones revisadas por el equipo.
