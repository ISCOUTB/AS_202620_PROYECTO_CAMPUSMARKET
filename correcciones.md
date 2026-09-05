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
- Se hicieron explícitas dos tensiones entre atributos de calidad en
  `docs/arc42/10-escenarios-de-calidad.md`:
  - mantenibilidad vs rapidez de desarrollo;
  - rendimiento vs mantenibilidad.

### Evidencia

- `docs/aspectos.md`
- `docs/ia.md`
- `docs/arc42/`
- `docs/arc42/10-escenarios-de-calidad.md`
- `docs/adr/`
- `docs/c4/`
- historial de commits del repositorio

### Estado

**Saneado.**

Los hallazgos identificados en S1 fueron atendidos. La estructura documental,
la tabla de trazabilidad, el registro de IA, la contribución del equipo y las
dos tensiones entre atributos de calidad se encuentran documentados en el
estado actual del repositorio.

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
- Se enlazó ADR-0001 con su primera materialización en código mediante el
  PR #5 y el commit de integración `4dd857a`.
- La evidencia se documentó en `docs/arc42/09-decisiones.md` sin reescribir
  el ADR aceptado.
- Se ejecutó localmente el arranque completo de CampusMarket en Windows
  mediante un único comando:
  `powershell -ExecutionPolicy Bypass -File .\scripts\run_s4.ps1`.
- La ejecución inició correctamente el backend FastAPI y el frontend
  Flutter Web.
- Se verificó el frontend en `http://localhost:3000`.
- Se verificó el backend mediante `http://localhost:8000/health`, obteniendo
  la respuesta `{"status":"ok","service":"campusmarket-api"}`.
- Se documentó el procedimiento reproducible y se incorporaron capturas
  de la terminal, el frontend y el endpoint de salud en
  `docs/evidencias/arranque-un-comando-2026-09-04.md`.

### Saneamiento de SonarQube Cloud

Como parte del saneamiento de S4, el equipo realizó inicialmente una
integración manual de SonarQube Cloud mediante un proyecto temporal asociado
a una cuenta personal.

Esta primera integración utilizó:

- un archivo `sonar-project.properties`;
- un paso adicional dentro de GitHub Actions;
- una variable `SONAR_TOKEN`;
- ejecución del análisis después de las pruebas automatizadas.

La primera integración fue verificada mediante el Run #29 de GitHub Actions,
en el cual tanto `pytest` como el análisis estático finalizaron correctamente.

Posteriormente, el 05/09/2026, el docente habilitó el proyecto oficial de
CampusMarket en SonarQube Cloud. A partir de ese momento se realizó la
migración hacia la configuración oficial del curso.

La configuración final quedó de la siguiente manera:

- el análisis estático se ejecuta automáticamente mediante el proyecto
  oficial de SonarQube Cloud;
- GitHub Actions se mantiene dedicado únicamente a las pruebas automatizadas;
- se utiliza `.sonarcloud.properties` como configuración complementaria;
- se define Python 3.12;
- `backend/app` y `frontend/campusmarket/lib` se identifican como código
  fuente;
- `backend/tests` se identifica como código de pruebas;
- se eliminó el archivo `sonar-project.properties`;
- se retiró del workflow el análisis manual con `SONAR_TOKEN`.

Durante la primera ejecución de la configuración oficial se detectó una
superposición entre rutas de código fuente y pruebas. El problema se corrigió
delimitando explícitamente `sonar.sources` y `sonar.tests`.

Después de la corrección se verificó el análisis oficial sobre `master` con
los siguientes resultados:

- Quality Gate: **Passed**
- Issues nuevos: **0**
- Security Hotspots nuevos: **0**
- Duplicación en código nuevo: **0.0 %**
- Pruebas automatizadas del backend: **success**

El proyecto oficial utilizado es:

`ISCOUTB_AS_202620_PROYECTO_CAMPUSMARKET`

### Evidencia

- `README.md`
- `docs/arc42/`
- `docs/arc42/09-decisiones.md`
- `docs/c4/01-contexto.md`
- `docs/c4/02-contenedores.md`
- `docs/adr/0001-usar-monolito-modular.md`
- `docs/aspectos.md`
- `docs/ia.md`
- `backend/tests/test_publicaciones_vertical.py`
- `.github/workflows/backend-tests.yml`
- `.sonarcloud.properties`
- `scripts/run_s4.ps1`
- [`docs/evidencias/arranque-un-comando-2026-09-04.md`](docs/evidencias/arranque-un-comando-2026-09-04.md)
- `docs/evidencias/arranque-terminal-2026-09-04.png`
- `docs/evidencias/arranque-frontend-2026-09-04.png`
- `docs/evidencias/arranque-health-2026-09-04.png`
- PR #5 - Completar esqueleto ejecutable de Evidencia S3
- Commit de integración `4dd857a`
- GitHub Actions Run #29 como evidencia de la primera integración de SonarQube Cloud
- PR #24 - Configurar análisis automático oficial de Sonar
- PR #25 - Corregir rutas de fuentes y pruebas en Sonar
- PR #26 - Limpiar configuración SonarCloud personal
- Proyecto oficial de SonarQube Cloud:
  `ISCOUTB_AS_202620_PROYECTO_CAMPUSMARKET`

### Estado

**Saneado.**

Los criterios y pendientes identificados específicamente en la
retroalimentación de S4 fueron atendidos.

El pendiente relacionado con SonarQube Cloud quedó completamente saneado
el 05/09/2026:

- ✅ Proyecto oficial de CampusMarket habilitado en SonarQube Cloud.
- ✅ Análisis automático asociado al repositorio de ISCOUTB.
- ✅ `.sonarcloud.properties` configurado.
- ✅ Python 3.12 definido.
- ✅ Rutas de código fuente y pruebas separadas correctamente.
- ✅ Configuración SonarCloud personal retirada.
- ✅ GitHub Actions conserva únicamente las pruebas automatizadas.
- ✅ Quality Gate oficial en `master`: **Passed**.
- ✅ 0 issues nuevos.
- ✅ 0 security hotspots nuevos.

El pendiente relacionado con la trazabilidad entre ADR-0001 y su
implementación también fue resuelto el 04/09/2026:

- ✅ ADR-0001 enlazado con el PR #5.
- ✅ Commit de integración `4dd857a` identificado como primera
  materialización de la decisión.
- ✅ Evidencia registrada en `docs/arc42/09-decisiones.md`.

El pendiente relacionado con el arranque mediante un solo comando fue
resuelto el 04/09/2026:

- ✅ `scripts/run_s4.ps1` ejecutado desde la raíz del repositorio.
- ✅ Backend FastAPI iniciado correctamente.
- ✅ Frontend Flutter Web iniciado correctamente en `localhost:3000`.
- ✅ Endpoint `/health` respondió con estado `ok`.
- ✅ Procedimiento reproducible y capturas almacenados en
  `docs/evidencias/`.

---

## Estado acumulado antes del primer corte

| Semana | Estado |
|---|---|
| S1 | Saneado |
| S2 | Saneado |
| S3 | Saneado |
| S4 | Saneado; SonarQube Cloud oficial, ADR→commit y arranque con un comando verificados |

El saneamiento acumulado de las evidencias S1-S4 queda completado.

Antes de consolidar el primer corte permanece pendiente obtener una
**medición de línea base reproducible** y desarrollar la respuesta
arquitectónica correspondiente a la restricción definida por el equipo
para la Semana 5.

Este archivo documenta únicamente correcciones sobre las evidencias
acumuladas S1-S4. El reto arquitectónico específico de la Semana 5 se
documentará separadamente.
