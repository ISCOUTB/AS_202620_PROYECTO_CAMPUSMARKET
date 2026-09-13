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




## Criterio de uso

La IA se utiliza como apoyo para análisis, documentación, organización, comparación de alternativas y revisión técnica.

El equipo mantiene la responsabilidad de:

- revisar cada propuesta antes de incorporarla;
- ejecutar directamente las pruebas y mediciones;
- contrastar las recomendaciones con el estado real del repositorio;
- aceptar, corregir o rechazar las propuestas de IA con justificación técnica;
- tomar y defender las decisiones arquitectónicas finales.

Las propuestas generadas por IA no se consideran evidencia por sí mismas. La evidencia utilizada por el proyecto corresponde a resultados verificables del repositorio, pruebas ejecutadas, mediciones, documentación trazable y decisiones revisadas por el equipo.
