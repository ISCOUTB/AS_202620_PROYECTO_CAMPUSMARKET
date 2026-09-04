# Correcciones acumuladas - CampusMarket

Este documento registra la retroalimentación recibida durante las evidencias
S1, S2, S3 y S4, junto con las correcciones realizadas por el equipo antes
del primer corte.

El objetivo es mantener trazabilidad entre los hallazgos identificados por
las revisiones del curso y el estado actual del repositorio.

---

## Semana 1 - Evidencia S1

### Retroalimentación recibida

Durante la revisión de S1 se identificaron principalmente los siguientes
hallazgos:

- No estaban declaradas de forma explícita dos tensiones entre atributos de
  calidad.
- `docs/aspectos.md` no contenía la tabla de ocho columnas requerida.
- No estaba organizada la documentación en `docs/arc42/`, `docs/adr/`
  y `docs/c4/`.
- `docs/ia.md` registraba el uso de IA, pero no indicaba qué propuestas
  habían sido rechazadas y por qué.
- La contribución al repositorio estaba concentrada inicialmente en una
  sola identidad.
- Existía una inconsistencia inicial en la cantidad de integrantes
  documentados.

### Correcciones realizadas

- Se reorganizó la documentación arquitectónica en las rutas:
  - `docs/arc42/`
  - `docs/adr/`
  - `docs/c4/`
- Se convirtió `docs/aspectos.md` en una tabla de trazabilidad de ocho
  columnas:
  `Aspecto → Requisito → C4 → ADR → Código → Pruebas → Evidencia`.
- Se actualizó `docs/ia.md` para registrar:
  - herramienta utilizada;
  - uso realizado;
  - verificación del equipo;
  - qué propuesta se rechazó y por qué.
- Se actualizó la identificación del equipo a tres integrantes.
- Actualmente existen contribuciones de los tres integrantes en el
  historial del repositorio.

### Evidencia

- `docs/aspectos.md`
- `docs/ia.md`
- `docs/arc42/`
- `docs/adr/`
- `docs/c4/`
- historial de commits del repositorio

### Estado

**Parcialmente saneado.**

La estructura, trazabilidad, registro de IA y contribución fueron corregidos.

Queda pendiente hacer explícitas en la documentación las tensiones entre
atributos de calidad identificadas para el proyecto.

---

## Semana 2 - Evidencia S2

### Retroalimentación recibida

La revisión de S2 destacó como aspectos positivos los escenarios de calidad,
restricciones, árbol de utilidad y C4 de contexto.

Los principales ajustes solicitados fueron:

- La sección 1 de arc42 describía funcionalidades en lugar de objetivos
  de negocio asociados con interesados.
- `docs/aspectos.md` todavía no enlazaba correctamente los escenarios.
- La documentación seguía distribuida en archivos sueltos.
- Existían referencias inconsistentes al tamaño del equipo.
- `docs/ia.md` no registraba las propuestas rechazadas.
- La contribución seguía concentrada en una sola cuenta.

### Correcciones realizadas

- Se actualizó la sección 1 de arc42 incorporando objetivos de negocio
  e interesados.
- Se reorganizó la documentación dentro de la estructura definida por
  el curso.
- Se actualizaron los enlaces de trazabilidad en `docs/aspectos.md`.
- Se unificó la documentación indicando que CampusMarket es desarrollado
  por un equipo de tres integrantes.
- Se completó `docs/ia.md` con verificación y propuestas rechazadas.
- Se distribuyeron las contribuciones entre los integrantes del equipo.

### Evidencia

- `docs/arc42/ARC42.md`
- `docs/arc42/02-restricciones.md`
- `docs/arc42/10-escenarios-de-calidad.md`
- `docs/arc42/10-arbol-de-utilidad.md`
- `docs/aspectos.md`
- `docs/ia.md`

### Estado

**Saneado.**

Los hallazgos principales señalados en la revisión de S2 están corregidos
en el estado actual del repositorio.

---

## Semana 3 - Evidencia S3

### Retroalimentación recibida

La revisión de S3 confirmó el cumplimiento de los nueve criterios principales.

Se dejaron dos observaciones para las siguientes semanas:

- `docs/ia.md` no contenía todavía las entradas correspondientes a S3.
- El frontend continuaba inicialmente con la estructura base de Flutter
  y todavía no reflejaba completamente las fronteras del monolito modular.

### Correcciones realizadas

- Se agregaron en `docs/ia.md` las actividades realizadas con IA durante S3,
  incluyendo las propuestas aceptadas, verificadas y rechazadas.
- Se organizaron las capacidades del frontend utilizando las mismas
  fronteras funcionales definidas por el ADR-0001:
  - `usuarios`
  - `publicaciones`
  - `catalogo`
  - `administracion`
- Se mantuvo la correspondencia entre la estructura del código y la
  decisión de utilizar un monolito modular.

### Evidencia

- `docs/ia.md`
- `docs/adr/0001-usar-monolito-modular.md`
- `frontend/campusmarket/lib/usuarios/`
- `frontend/campusmarket/lib/publicaciones/`
- `frontend/campusmarket/lib/catalogo/`
- `frontend/campusmarket/lib/administracion/`
- `backend/app/`

### Estado

**Saneado.**

Los hallazgos pendientes de S3 fueron atendidos durante la construcción
de la Evidencia S4.

---

## Semana 4 - Evidencia S4

### Retroalimentación recibida

La revisión definitiva de S4 confirmó una base arquitectónica consistente:

- arc42 secciones 1 a 6 redactadas;
- sección 9 enlazada con ADR-0001;
- escenarios de calidad y árbol de utilidad coherentes;
- glosario iniciado;
- C4 Nivel 1 y Nivel 2 coherentes;
- correspondencia entre C4 y estructura del código;
- corte vertical implementado;
- prueba automatizada en verde;
- trazabilidad ASP-05 completa.

Durante las revisiones provisionales también se solicitaron ajustes de
coherencia entre la documentación, el código y las evidencias.

### Correcciones realizadas

- Se actualizaron las secciones 3, 5, 6, 9 y 12 de arc42.
- Se verificó la coherencia entre C4 Nivel 1 y C4 Nivel 2.
- Se evitó incluir detalles internos de componentes dentro del C4 Nivel 2,
  manteniendo ese detalle para niveles posteriores.
- Se documentó el corte vertical:

  `Flutter → FastAPI → módulo publicaciones → SQLite`

- Se implementó la creación y recuperación de publicaciones.
- Se añadió la prueba automatizada:
  `backend/tests/test_publicaciones_vertical.py`.
- Se verificó el pipeline de GitHub Actions en verde.
- Se actualizó `docs/aspectos.md` con la trazabilidad del corte vertical.
- Se hizo explícita en el README la evidencia del glosario, C4, pruebas,
  corte vertical y trazabilidad.
- Se actualizó `docs/ia.md` con las decisiones y propuestas rechazadas
  durante S4.
- Se configuró SonarQube Cloud para el análisis estático del backend.
- Se agregó el archivo `sonar-project.properties` con la configuración
  del proyecto.
- Se integró SonarQube Cloud al workflow existente de GitHub Actions.
- El análisis estático se ejecuta después de las pruebas automatizadas
  en los `push` a `master`.
- Se verificó la integración mediante el Run #29 de GitHub Actions,
  donde tanto `pytest` como el análisis de SonarQube Cloud finalizaron
  correctamente con resultado `success`.

### Evidencia

- `README.md`
- `docs/arc42/`
- `docs/c4/01-contexto.md`
- `docs/c4/02-contenedores.md`
- `docs/adr/0001-usar-monolito-modular.md`
- `docs/aspectos.md`
- `docs/ia.md`
- `backend/tests/test_publicaciones_vertical.py`
- `.github/workflows/backend-tests.yml`
- `sonar-project.properties`
- GitHub Actions Run #29:
  `https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/33847799874`

### Estado

**Saneado parcialmente, con pendientes para el primer corte.**

Los criterios principales de la Evidencia S4 fueron atendidos.

El pendiente relacionado con SonarCloud fue resuelto el 04/09/2026:

- ✅ SonarQube Cloud integrado al pipeline.
- ✅ Pruebas automatizadas ejecutadas correctamente.
- ✅ Análisis estático ejecutado correctamente en `master`.
- ✅ GitHub Actions Run #29 con resultado `success`.

Se mantienen abiertos los siguientes pendientes:

1. Dejar evidencia verificable de la ejecución del arranque con un solo
   comando.
2. Enlazar ADR-0001 con el commit que materializa la decisión.
3. Obtener una medición de línea base reproducible para el primer corte.

---

## Estado acumulado antes del primer corte

| Semana | Estado |
|---|---|
| S1 | Parcialmente saneado |
| S2 | Saneado |
| S3 | Saneado |
| S4 | Parcialmente saneado; SonarQube Cloud resuelto y tres pendientes abiertos |

Los elementos todavía abiertos se atenderán antes de consolidar la
evidencia final del primer corte.

Este archivo documenta únicamente correcciones sobre las evidencias
acumuladas S1-S4. El reto arquitectónico específico de la Semana 5 se
documentará separadamente una vez aplicada la nueva restricción asignada
al equipo.
