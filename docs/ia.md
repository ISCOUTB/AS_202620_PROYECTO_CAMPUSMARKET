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
| 04/09/2026 | ChatGPT | Revisión de la retroalimentación acumulada de S1-S4 y apoyo para estructurar `correcciones.md` con los hallazgos, correcciones realizadas y pendientes antes del primer corte. | El equipo contrastó cada punto con los archivos actuales del repositorio y con la retroalimentación oficial antes de incorporar el documento. | Se rechazó marcar todas las semanas como completamente saneadas porque todavía existían pendientes reales, como SonarCloud, la evidencia del arranque, el enlace ADR-0001 → commit y la medición de línea base. |
| 04/09/2026 | ChatGPT | Apoyo para configurar SonarQube Cloud e integrarlo con el workflow existente de GitHub Actions. | El equipo verificó la configuración mediante el Run #29 en `master`, donde las pruebas automatizadas y el análisis de SonarQube Cloud finalizaron correctamente con resultado `success`. | Se rechazó mantener el análisis de Sonar sobre los pull requests porque el proyecto de Sonar no estaba vinculado directamente al repositorio oficial de ISCOUTB y se produjo el error `Could not find the pull request with key '17'`. Se optó por ejecutar el análisis en los `push` a `master`, donde fue verificado correctamente. |
| 04/09/2026 | ChatGPT | Apoyo para revisar la retroalimentación de S4 y establecer la trazabilidad entre ADR-0001 y el commit que materializó inicialmente la decisión de monolito modular. | El equipo verificó el historial del repositorio y confirmó que el PR #5 consolidó el esqueleto ejecutable con los módulos `usuarios`, `publicaciones`, `catalogo` y `administracion`; la evidencia quedó documentada en `docs/arc42/09-decisiones.md`. | Se rechazó modificar el contenido del ADR-0001 aceptado únicamente para añadir el enlace al commit, porque reescribir una decisión arquitectónica aceptada alteraría su historial. Se optó por registrar la evidencia de implementación en la sección 9 de arc42. |
| 04/09/2026 | ChatGPT | Apoyo para atender la retroalimentación pendiente de S1 mediante la formulación de dos tensiones entre atributos de calidad y para actualizar el estado acumulado de correcciones S1-S4. | El equipo verificó que las tensiones fueran coherentes con los escenarios EC-01 y EC-03 y con la estrategia de monolito modular ya adoptada. También se contrastó `correcciones.md` con el estado actual del repositorio antes de marcar S1 como saneado. | Se rechazó formular tensiones genéricas sin relación con CampusMarket. Se conservaron mantenibilidad vs rapidez de desarrollo y rendimiento vs mantenibilidad porque ambas representan trade-offs aplicables al diseño y evolución actuales del sistema. |
| 04/09/2026 | ChatGPT | Apoyo para verificar el procedimiento de arranque con un solo comando y estructurar la evidencia reproducible solicitada en la retroalimentación de S4. | El equipo ejecutó `scripts/run_s4.ps1` en Windows y comprobó directamente el inicio del backend FastAPI, el frontend Flutter Web en `localhost:3000` y la respuesta exitosa del endpoint `/health`. Además, se almacenaron capturas de cada comprobación en `docs/evidencias/`. | Se rechazó considerar suficiente la existencia del script o la descripción del README sin ejecutarlo, porque la retroalimentación solicitaba evidencia verificable. Se optó por realizar la ejecución real y conservar procedimiento, resultado y capturas en el repositorio. |

## Criterio de uso

La IA se utiliza como apoyo para análisis, documentación, organización y revisión. El equipo mantiene la responsabilidad de ejecutar las pruebas, revisar los cambios, interpretar los resultados y defender las decisiones arquitectónicas.
