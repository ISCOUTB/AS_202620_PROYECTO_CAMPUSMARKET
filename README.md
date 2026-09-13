# CampusMarket

Marketplace universitario para la publicación, consulta, venta y alquiler de
productos dentro de la comunidad universitaria.

## Integrantes

- Joshua Tenorio Alvarez
- Camilo Martinez Berrio
- Nilver Garcia Pimentel

---

## Arquitectura

CampusMarket adopta un **monolito modular**, decisión registrada en:

[ADR-0001 - Usar monolito modular](docs/adr/0001-usar-monolito-modular.md)

Las capacidades principales del sistema se organizan alrededor de:

- `usuarios`
- `publicaciones`
- `catalogo`
- `administracion`

El corte vertical actualmente implementado y verificable se concentra
principalmente en la capacidad de `publicaciones`.

La arquitectura ejecutable mantiene el recorrido:

**Flutter Web → FastAPI → módulo `publicaciones` → SQLite**

Durante S6 estos módulos se formalizaron además como límites de dominio,
haciendo explícitas sus responsabilidades, relaciones y propiedad de datos.

---

## Tecnologías actuales

| Elemento | Tecnología |
|---|---|
| Frontend | Flutter / Dart |
| Backend | FastAPI / Python |
| Persistencia actual | SQLite |
| Pruebas backend | pytest |
| Integración continua | GitHub Actions |
| Análisis estático | SonarQube Cloud |
| Diagramas arquitectónicos | PlantUML |

SQLite es la persistencia realmente implementada actualmente.

Una eventual evolución hacia otra tecnología de persistencia no se documenta
como implementada mientras no exista en el código.

---

## Requisitos previos

- Python 3.12
- Flutter disponible en `PATH`
- Google Chrome
- dependencias Python instaladas

Desde la raíz del repositorio:

```bash
pip install -r backend/requirements.txt
```

---

## Arranque con un solo comando

### Windows

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_s4.ps1
```

### Linux/macOS

```bash
bash scripts/run_s4.sh
```

El comando inicia:

- Backend FastAPI: `http://localhost:8000`
- Frontend Flutter Web: `http://localhost:3000`

La ejecución fue comprobada directamente y documentada mediante procedimiento
reproducible y capturas.

Evidencia:

[Arranque con un solo comando](docs/evidencias/arranque-un-comando-2026-09-04.md)

Durante la verificación se confirmó:

- inicio correcto del backend;
- inicio correcto del frontend;
- acceso al frontend mediante `localhost:3000`;
- respuesta correcta del endpoint `/health`.

---

# Línea base arquitectónica S1-S4

Las evidencias construidas durante S1, S2, S3 y S4 conforman la línea base
arquitectónica utilizada para el primer corte.

## Corte vertical S4

El recorrido implementado es:

**Flutter Web → FastAPI → lógica de publicaciones → SQLite**

La funcionalidad verificable permite crear y consultar publicaciones.

### Correspondencia con el código

**Frontend**

- Interfaz:
  [`publicacion_form_page.dart`](frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart)
- Cliente HTTP:
  [`publicaciones_api.dart`](frontend/campusmarket/lib/publicaciones/publicaciones_api.dart)

**Backend**

- Entrada HTTP:
  [`router.py`](backend/app/publicaciones/router.py)
- Lógica de aplicación:
  [`service.py`](backend/app/publicaciones/service.py)
- Persistencia:
  [`repository.py`](backend/app/publicaciones/repository.py)

---

## Pruebas automatizadas

Desde la raíz:

```bash
python -m pytest backend/tests -q
```

Las pruebas principales del proyecto incluyen:

- [`backend/tests/test_health.py`](backend/tests/test_health.py)
- [`backend/tests/test_publicaciones_vertical.py`](backend/tests/test_publicaciones_vertical.py)
- [`backend/tests/test_modularidad_s6.py`](backend/tests/test_modularidad_s6.py)

El conjunto de pruebas verifica actualmente:

- disponibilidad del backend mediante `/health`;
- recorrido HTTP del corte vertical;
- creación y consulta de publicaciones;
- persistencia SQLite;
- degradación controlada ante bloqueo temporal;
- propiedad única de la entidad `publicaciones`;
- ausencia de acceso directo a SQLite desde otros contextos;
- dirección de dependencias `router → service → repository → SQLite`.

Las pruebas se ejecutan automáticamente mediante GitHub Actions.

---

## Verificación del frontend

Desde:

```bash
cd frontend/campusmarket
```

se ejecutó:

```bash
flutter analyze
```

Resultado verificado:

```text
No issues found!
```

---

# Integración continua y análisis estático

## GitHub Actions

Las pruebas automatizadas del backend se ejecutan mediante:

[`.github/workflows/backend-tests.yml`](.github/workflows/backend-tests.yml)

El workflow realiza:

1. obtención del repositorio;
2. configuración de Python 3.12;
3. instalación de dependencias;
4. ejecución de `pytest`.

Las pruebas de modularidad incorporadas en S6 forman parte del mismo conjunto
de pruebas y, por tanto, también se ejecutan dentro del pipeline.

## SonarQube Cloud

El análisis estático se realiza mediante el proyecto oficial de CampusMarket
en **SonarQube Cloud**, asociado al repositorio de ISCOUTB.

La configuración complementaria se encuentra en:

[`.sonarcloud.properties`](.sonarcloud.properties)

La configuración separa explícitamente:

**Código fuente**

- `backend/app`
- `frontend/campusmarket/lib`

**Pruebas**

- `backend/tests`

El proyecto oficial utilizado es:

`ISCOUTB_AS_202620_PROYECTO_CAMPUSMARKET`

Las integraciones verificadas reportaron:

- Quality Gate: **Passed**
- Issues nuevos: **0**
- Security Hotspots nuevos: **0**
- Duplicación en código nuevo: **0.0 %**

La configuración temporal de SonarCloud utilizada inicialmente durante el
saneamiento fue retirada una vez disponible el proyecto oficial del curso.

GitHub Actions permanece dedicado a las pruebas automatizadas y SonarQube
Cloud realiza el análisis estático oficial.

---

# Correcciones acumuladas antes del primer corte

Durante las clases, el docente solicitó organizar la respuesta a la
retroalimentación acumulada mediante un archivo Markdown en el repositorio,
separando las correcciones realizadas durante las semanas anteriores.

Ese seguimiento se encuentra en:

[`correcciones.md`](correcciones.md)

El documento registra para S1-S4:

- retroalimentación recibida;
- correcciones realizadas;
- evidencia correspondiente;
- estado de saneamiento.

Estado acumulado:

| Semana | Estado |
|---|---|
| S1 | **Saneado** |
| S2 | **Saneado** |
| S3 | **Saneado** |
| S4 | **Saneado** |

Entre los principales pendientes atendidos antes del primer corte se
encuentran:

- tensiones entre atributos de calidad;
- estructura documental arc42;
- tabla de trazabilidad de ocho columnas;
- actualización del registro de IA;
- distribución de contribuciones;
- correspondencia de las fronteras del monolito modular;
- trazabilidad ADR → implementación;
- arranque con un solo comando;
- integración oficial de SonarQube Cloud;
- medición de una línea base reproducible.

`correcciones.md` mantiene además de forma explícita el estado actual de los
aspectos que todavía no forman parte del corte vertical, evitando asociarlos
artificialmente con código o pruebas que no los materializan.

---

# Diagramas C4

Los diagramas arquitectónicos se mantienen como **diagramas como código**
mediante PlantUML.

## C4 Nivel 1 - Contexto

- [Documentación](docs/c4/01-contexto.md)
- [Fuente PlantUML](docs/c4/01-contexto.puml)

El Nivel 1 representa CampusMarket como un único sistema frente a:

- Estudiante;
- Administrador.

No expone tecnologías ni estructura interna.

---

## C4 Nivel 2 - Contenedores

- [Documentación](docs/c4/02-contenedores.md)
- [Fuente PlantUML](docs/c4/02-contenedores.puml)

El Nivel 2 representa:

**Frontend Web → Backend API → Persistencia local SQLite**

con sus responsabilidades, tecnologías y relaciones.

Incluye:

- contenedores ejecutables;
- responsabilidades;
- tecnologías;
- relaciones entre contenedores;
- flechas etiquetadas;
- leyenda arquitectónica.

No se incorporan routers, services, repositories o clases como cajas del
Nivel 2 porque ese detalle corresponde al Nivel 3.

---

## C4 Nivel 3 - Componentes del Backend API

- [Documentación](docs/c4/03-componentes-backend.md)
- [Fuente PlantUML](docs/c4/03-componentes-backend.puml)

El Nivel 3 realiza un acercamiento al interior del contenedor
**Backend API**.

La materialización actualmente verificable sigue el flujo:

```text
Frontend Web
     ↓
API de Publicaciones
     ↓
Servicio de Publicaciones
     ↓
Repositorio de Publicaciones
     ↓
SQLite
```

La correspondencia principal con el código es:

| Componente | Implementación |
|---|---|
| Entrada de aplicación | `backend/app/main.py` |
| API de Publicaciones | `backend/app/publicaciones/router.py` |
| Servicio de Publicaciones | `backend/app/publicaciones/service.py` |
| Repositorio de Publicaciones | `backend/app/publicaciones/repository.py` |

Los contextos:

- `usuarios`;
- `catalogo`;
- `administracion`;

se mantienen como límites arquitectónicos definidos, pero todavía no se
declaran como capacidades funcionales completamente materializadas.

El Nivel 3 no introduce nuevos servicios desplegables ni modifica la topología
del Nivel 2.

Hace explícita la organización interna del Backend API y su correspondencia
con los límites de dominio formalizados durante S6.

---

# Primer corte - Reto arquitectónico S5

## Definición de la restricción

Durante la explicación del reto de Semana 5, el equipo consultó si la nueva
restricción arquitectónica sería asignada directamente por el docente o
definida por cada grupo.

La aclaración recibida fue que **cada equipo debía definir la restricción a
partir del estado real de su arquitectura**.

Por esta razón, el equipo no reutilizó como nueva restricción una decisión ya
existente como el monolito modular.

Primero se revisó la arquitectura actual y posteriormente se definió:

**R-07 - Persistencia sin nueva infraestructura durante el primer corte**

La restricción se encuentra documentada en:

[`docs/arc42/02-restricciones.md`](docs/arc42/02-restricciones.md)

R-07 establece que durante el primer corte:

- se mantiene SQLite como persistencia;
- se conserva el backend como una única aplicación monolítica modular;
- no se incorporan bases de datos externas;
- no se agregan colas;
- no se agregan cachés distribuidas;
- no se crean nuevos servicios desplegables.

La restricción obliga a mejorar la respuesta del sistema utilizando la
arquitectura ya existente.

---

## Diagnóstico

Para evaluar el impacto de R-07 se analizó el comportamiento del corte
vertical ante una condición adversa de persistencia:

**bloqueo temporal de SQLite durante la creación de una publicación.**

Antes de aplicar cambios se realizó una medición reproducible.

### Línea base

| Métrica | Resultado inicial |
|---|---:|
| HTTP durante bloqueo | `500` |
| Tiempo durante bloqueo | `7.323 s` |
| Escritura parcial | `No` |
| HTTP después de liberar SQLite | `201` |
| Tiempo de recuperación | `0.007 s` |

La línea base mostró que:

- el sistema no generaba escrituras parciales;
- recuperaba su funcionamiento después de liberar SQLite;
- pero respondía con HTTP `500`;
- y demoraba `7.323 s`.

El principal problema era, por tanto, una **degradación no controlada y
demasiado lenta** ante la indisponibilidad temporal de persistencia.

Evidencia:

[Línea base de bloqueo SQLite](docs/evidencias/linea-base-bloqueo-sqlite-2026-09-05.md)

---

## Escenario de calidad EC-05

A partir del diagnóstico se formuló:

**EC-05 - Degradación ante bloqueo temporal de persistencia**

Documentación:

[`docs/arc42/10-escenarios-de-calidad.md`](docs/arc42/10-escenarios-de-calidad.md)

El escenario exige que, cuando SQLite se encuentre temporalmente bloqueada
durante la creación de una publicación:

- el sistema responda mediante HTTP `503`;
- la respuesta ocurra en un máximo de `2 segundos`;
- no exista escritura parcial;
- se informe la indisponibilidad temporal;
- después de liberar SQLite se recupere la creación normal.

---

## Decisión arquitectónica ADR-0002

La decisión se documentó en:

[ADR-0002 - Manejo de bloqueo temporal de SQLite](docs/adr/0002-manejo-bloqueo-sqlite.md)

Antes de decidir se consideraron alternativas como:

- mantener el comportamiento existente;
- aumentar la espera;
- realizar reintentos automáticos;
- migrar la persistencia;
- introducir nueva infraestructura;
- aplicar una espera acotada y degradación controlada.

La decisión final mantiene la infraestructura existente y aplica:

- timeout SQLite de `0.5 s`;
- detección específica de `SQLITE_BUSY`;
- detección específica de `SQLITE_LOCKED`;
- traducción controlada de la indisponibilidad;
- HTTP `503 Service Unavailable`;
- ausencia de reintentos automáticos;
- preservación de la transacción;
- cierre explícito de conexiones;
- propagación del estado hasta Flutter.

No se adoptaron PostgreSQL, colas, cachés ni nuevos servicios porque eso
contradiría directamente R-07.

Los reintentos automáticos tampoco fueron seleccionados porque podían
incrementar la latencia y comprometer el umbral de EC-05.

---

## Aplicación sobre el corte vertical

La modificación preserva el recorrido:

**Flutter Web → FastAPI → módulo `publicaciones` → SQLite**

### Backend

La degradación controlada atraviesa:

```text
SQLite
   ↓
repository.py
   ↓
service.py
   ↓
router.py
   ↓
HTTP 503
```

Archivos principales:

- [`repository.py`](backend/app/publicaciones/repository.py)
- [`service.py`](backend/app/publicaciones/service.py)
- [`router.py`](backend/app/publicaciones/router.py)

### Frontend

El HTTP `503` es interpretado específicamente por Flutter:

```text
HTTP 503
   ↓
publicaciones_api.dart
   ↓
publicacion_form_page.dart
   ↓
mensaje de indisponibilidad temporal
```

Archivos:

- [`publicaciones_api.dart`](frontend/campusmarket/lib/publicaciones/publicaciones_api.dart)
- [`publicacion_form_page.dart`](frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart)

De esta forma, la condición adversa no termina únicamente en un error
genérico: el usuario recibe información sobre la indisponibilidad temporal.

---

## Impacto sobre C4

R-07 y ADR-0002 **no agregan nuevos contenedores**.

La topología continúa siendo:

**Frontend Web → Backend API → SQLite**

El cambio afecta principalmente el comportamiento de la relación:

**Backend API → Persistencia local**

y posteriormente la forma en que:

**Frontend Web ← Backend API**

comunica la degradación controlada.

Esta decisión está explicada en:

[C4 Nivel 2 - Contenedores](docs/c4/02-contenedores.md)

---

# Medición posterior a ADR-0002

Después de aplicar la decisión se repitió el mismo escenario.

Resultado formal:

| Métrica | Línea base | Después | Umbral |
|---|---:|---:|---:|
| HTTP durante bloqueo | `500` | `503` | `503` |
| Tiempo durante bloqueo | `7.323 s` | `1.283 s` | `≤ 2 s` |
| Escritura parcial | `No` | `No` | `No` |
| HTTP después de liberar SQLite | `201` | `201` | `201` |
| Tiempo de recuperación | `0.007 s` | `0.006 s` | Informativo |

La respuesta durante el bloqueo pasó de:

**HTTP `500` en `7.323 s`**

a:

**HTTP `503` en `1.283 s`**

sin producir escrituras parciales.

La operación normal se recuperó mediante HTTP `201` después de liberar
SQLite.

Por lo tanto, la medición formal **cumple el umbral de EC-05**.

Evidencia:

[Medición posterior a ADR-0002](docs/evidencias/medicion-bloqueo-sqlite-2026-09-06.md)

Una ejecución posterior volvió a verificar el comportamiento con:

- HTTP `503`;
- `1.138 s` durante el bloqueo;
- ninguna escritura parcial;
- recuperación HTTP `201`.

La medición formal utilizada como evidencia continúa siendo la ejecución de
`1.283 s`.

---

## Medición reproducible

El escenario puede volver a ejecutarse desde la raíz mediante:

```bash
python scripts/medir_bloqueo_sqlite.py
```

Script:

[`scripts/medir_bloqueo_sqlite.py`](scripts/medir_bloqueo_sqlite.py)

La primera ejecución realizada durante el desarrollo permitió detectar además
un problema de cierre de conexiones temporales en Windows.

Esa ejecución no fue utilizada como evidencia final.

Después de corregir el ciclo de vida de las conexiones SQLite, la medición
fue repetida correctamente sin traceback y se utilizó como resultado formal.

---

# Evidencia S6 - Dominio y modularidad

Durante S6 se hizo explícita la organización del dominio de CampusMarket
utilizando:

- lenguaje ubicuo;
- contextos delimitados;
- relaciones entre contextos;
- propiedad única de datos;
- auditoría de modularidad;
- C4 Nivel 3;
- pruebas automáticas de reglas arquitectónicas.

Los contextos delimitados identificados son:

- **Gestión de Usuarios**
- **Gestión de Publicaciones**
- **Catálogo**
- **Administración**

La documentación principal se encuentra en:

- [Conceptos transversales - arc42 sección 8](docs/arc42/08-conceptos-transversales.md)
- [C4 Nivel 3 - Componentes del Backend](docs/c4/03-componentes-backend.md)
- [Fuente PlantUML del C4 Nivel 3](docs/c4/03-componentes-backend.puml)
- [Auditoría de modularidad S6](docs/evidencias/auditoria-modularidad-s6-2026-09-12.md)
- [Trazabilidad de aspectos](docs/aspectos.md)

---

## Lenguaje ubicuo y contextos delimitados

La sección 8 de arc42 establece un vocabulario común para términos como:

- estudiante;
- usuario;
- producto;
- publicación;
- modalidad;
- estado del producto;
- catálogo;
- administrador;
- propietario;
- dueño del dato;
- contexto delimitado.

También diferencia explícitamente entre **Producto** y **Publicación** para
evitar utilizar ambos términos como sinónimos.

El mapa de contextos documenta relaciones del tipo:

- **Customer/Supplier** entre Gestión de Usuarios y Gestión de Publicaciones;
- **Customer/Supplier** entre Gestión de Publicaciones y Catálogo;
- contrato explícito y **Anticorruption Layer** entre Publicaciones y
  Administración.

No se adopta actualmente un **Shared Kernel**, porque no existe un modelo que
deba ser modificado conjuntamente por dos contextos y su incorporación
aumentaría innecesariamente el acoplamiento.

---

## Propiedad de datos

La regla arquitectónica adoptada es:

> Cada dato de dominio tiene un único módulo responsable de escribirlo.

En el estado actual del prototipo, la entidad persistida de dominio
materializada es:

`publicaciones`

Su propietario es:

**Gestión de Publicaciones**

El único escritor productivo se encuentra en:

[`backend/app/publicaciones/repository.py`](backend/app/publicaciones/repository.py)

Los campos actualmente persistidos son:

| Campo | Propietario |
|---|---|
| `id` | Gestión de Publicaciones |
| `titulo` | Gestión de Publicaciones |
| `descripcion` | Gestión de Publicaciones |
| `precio` | Gestión de Publicaciones |
| `modalidad` | Gestión de Publicaciones |
| `estado` | Gestión de Publicaciones |

La auditoría no detectó escrituras compartidas de `publicaciones` desde:

- `usuarios`;
- `catalogo`;
- `administracion`.

---

## Auditoría de modularidad

La revisión del código se encuentra documentada en:

[Auditoría de modularidad S6](docs/evidencias/auditoria-modularidad-s6-2026-09-12.md)

La auditoría revisó:

- entidades persistidas;
- operaciones `INSERT`;
- operaciones `UPDATE`;
- operaciones `DELETE`;
- accesos directos mediante `sqlite3`;
- repositorios;
- servicios;
- límites de contexto.

El recorrido confirmó que el único escritor productivo de `publicaciones`
permanece dentro de Gestión de Publicaciones.

También se documentaron los riesgos:

- `MOD-01` - acceso futuro de Catálogo a persistencia;
- `MOD-02` - escritura futura desde Administración;
- `MOD-03` - materialización pendiente del propietario de publicación;
- `MOD-04` - accesos SQLite permitidos únicamente para pruebas e
  instrumentación.

Cada riesgo cuenta con un plan preventivo o correctivo.

---

## Verificación automática de modularidad

Además de la auditoría manual se incorporó:

[`backend/tests/test_modularidad_s6.py`](backend/tests/test_modularidad_s6.py)

La prueba verifica automáticamente que:

- `backend/app/publicaciones/repository.py` sea el único escritor productivo de
  `publicaciones`;
- `usuarios`, `catalogo` y `administracion` no accedan directamente a SQLite;
- los otros contextos no importen directamente el repositorio interno de
  Publicaciones;
- el flujo implementado mantenga la dirección:
  `router → service → repository → SQLite`;
- la creación y consulta de `publicaciones` permanezcan encapsuladas en el
  repositorio propietario.

Estas comprobaciones forman parte de `backend/tests` y se ejecutan mediante
GitHub Actions.

La integración utilizada para S6 finalizó con:

- pruebas del backend: **Passed**;
- SonarQube Cloud Quality Gate: **Passed**;
- nuevos problemas detectados en el análisis correspondiente: **0**.

---

## C4 Nivel 3 y coherencia con ADR-0001

El C4 Nivel 3 amplía únicamente el contenedor **Backend API**.

Representa:

```text
Frontend Web
     ↓
API de Publicaciones
     ↓
Servicio de Publicaciones
     ↓
Repositorio de Publicaciones
     ↓
SQLite
```

Los límites principales continúan siendo:

- `usuarios`;
- `publicaciones`;
- `catalogo`;
- `administracion`.

S6 no fusiona, divide ni reemplaza estos límites.

Por esta razón, la incorporación del C4 Nivel 3 constituye una profundización
de la arquitectura existente y **no un reajuste de los límites definidos por
ADR-0001**.

No se registra un nuevo ADR para S6 porque no existe una nueva decisión que
reemplace o modifique ADR-0001.

Si posteriormente cambia realmente alguno de estos límites, deberá
actualizarse el C4 Nivel 3 y registrarse un nuevo ADR explicando el reajuste.

---

# Trazabilidad arquitectónica

La trazabilidad general del proyecto se mantiene en:

[`docs/aspectos.md`](docs/aspectos.md)

## Trazabilidad S5

La cadena principal es:

**ASP-06 → R-07 / EC-05 → C4 Nivel 2 → ADR-0002 → código → pruebas → medición → evidencia**

| Elemento | Evidencia |
|---|---|
| Aspecto | `ASP-06` |
| Restricción | `R-07` |
| Escenario | `EC-05` |
| C4 | `docs/c4/02-contenedores.md` |
| Decisión | `docs/adr/0002-manejo-bloqueo-sqlite.md` |
| Código backend | `backend/app/publicaciones/` |
| Código frontend | `frontend/campusmarket/lib/publicaciones/` |
| Prueba | `backend/tests/test_publicaciones_vertical.py` |
| Medición | `scripts/medir_bloqueo_sqlite.py` |
| Línea base | `docs/evidencias/linea-base-bloqueo-sqlite-2026-09-05.md` |
| Resultado | `docs/evidencias/medicion-bloqueo-sqlite-2026-09-06.md` |

## Trazabilidad S6

Durante S6 la trazabilidad se amplía a:

**Aspecto → contexto delimitado → propietario del dato → C4 Nivel 3 → código → auditoría → prueba automática**

La correspondencia entre los contextos y los aspectos del proyecto está
documentada en:

[Aspectos y trazabilidad](docs/aspectos.md)

La cadena permite comprobar que las decisiones documentadas corresponden con
los módulos y datos realmente presentes en el repositorio.

---

# Documentación arc42

La documentación arquitectónica principal se encuentra en:

- [Secciones iniciales](docs/arc42/ARC42.md)
- [Sección 2 - Restricciones](docs/arc42/02-restricciones.md)
- [Sección 3 - Contexto](docs/arc42/03-contexto.md)
- [Sección 4 - Estrategia de solución](docs/arc42/04-estrategia-de-solucion.md)
- [Sección 5 - Bloques de construcción](docs/arc42/05-bloques-de-construccion.md)
- [Sección 6 - Vista de ejecución](docs/arc42/06-vista-ejecucion.md)
- [Sección 8 - Conceptos transversales y dominio](docs/arc42/08-conceptos-transversales.md)
- [Sección 9 - Decisiones](docs/arc42/09-decisiones.md)
- [Sección 10 - Escenarios de calidad](docs/arc42/10-escenarios-de-calidad.md)
- [Sección 12 - Glosario](docs/arc42/12-glosario.md)

## ADR

- [ADR-0001 - Usar monolito modular](docs/adr/0001-usar-monolito-modular.md)
- [ADR-0002 - Manejo de bloqueo temporal de SQLite](docs/adr/0002-manejo-bloqueo-sqlite.md)

No se crea un ADR adicional durante S6 porque los límites definidos por
ADR-0001 permanecen vigentes.

---

# Registro de uso de Inteligencia Artificial

El registro de uso de herramientas de IA se encuentra en:

[`docs/ia.md`](docs/ia.md)

El documento registra:

- fecha;
- herramienta utilizada;
- uso realizado;
- verificación realizada por el equipo;
- propuestas rechazadas;
- justificación del rechazo.

Para cada evidencia las actividades realizadas durante una misma jornada se
consolidan bajo una fecha general para evitar fragmentar el registro.

Durante S6 la IA fue utilizada como apoyo para:

- interpretar la evidencia;
- estructurar el lenguaje ubicuo;
- revisar contextos delimitados;
- contrastar propiedad de datos con el código;
- auditar modularidad;
- revisar C4 Nivel 3;
- formular pruebas de reglas arquitectónicas;
- mejorar la trazabilidad documental.

Las propuestas no se aceptan automáticamente.

El equipo conserva la responsabilidad sobre:

- decisiones arquitectónicas;
- modificaciones incorporadas;
- pruebas ejecutadas;
- mediciones;
- validación del repositorio;
- aceptación, corrección o rechazo de propuestas generadas con IA.

Las respuestas de IA no se utilizan por sí mismas como evidencia del sistema.

---

# Evidencias principales

## Primer corte

- [Correcciones acumuladas S1-S4](correcciones.md)
- [Restricciones arquitectónicas](docs/arc42/02-restricciones.md)
- [EC-05](docs/arc42/10-escenarios-de-calidad.md)
- [ADR-0001](docs/adr/0001-usar-monolito-modular.md)
- [ADR-0002](docs/adr/0002-manejo-bloqueo-sqlite.md)
- [C4 Nivel 1](docs/c4/01-contexto.md)
- [C4 Nivel 2](docs/c4/02-contenedores.md)
- [Arranque con un comando](docs/evidencias/arranque-un-comando-2026-09-04.md)
- [Línea base S5](docs/evidencias/linea-base-bloqueo-sqlite-2026-09-05.md)
- [Medición final S5](docs/evidencias/medicion-bloqueo-sqlite-2026-09-06.md)
- [Prueba del corte vertical](backend/tests/test_publicaciones_vertical.py)
- [Script de medición](scripts/medir_bloqueo_sqlite.py)

## Evidencia S6

- [arc42 sección 8 - Conceptos transversales](docs/arc42/08-conceptos-transversales.md)
- [C4 Nivel 3 - Componentes del Backend](docs/c4/03-componentes-backend.md)
- [Fuente PlantUML C4 Nivel 3](docs/c4/03-componentes-backend.puml)
- [Auditoría de modularidad](docs/evidencias/auditoria-modularidad-s6-2026-09-12.md)
- [Prueba automática de modularidad](backend/tests/test_modularidad_s6.py)
- [Trazabilidad de aspectos](docs/aspectos.md)
- [Registro de IA](docs/ia.md)

---

# Estado actual del proyecto

La línea base S1-S4 se encuentra documentada y saneada en:

[`correcciones.md`](correcciones.md)

El reto arquitectónico S5 cuenta con:

- restricción definida;
- diagnóstico;
- línea base reproducible;
- escenario de calidad medible;
- comparación de alternativas;
- ADR;
- cambio aplicado sobre el corte vertical;
- degradación controlada;
- pruebas automatizadas;
- medición posterior;
- contraste contra el umbral;
- recuperación verificada;
- C4 Nivel 2 actualizado;
- trazabilidad;
- registro de IA.

La Evidencia S6 cuenta con:

- lenguaje ubicuo;
- cuatro contextos delimitados;
- mapa de contextos;
- relaciones `Customer/Supplier`;
- capa anticorrupción prevista para Administración;
- decisión explícita de no utilizar Shared Kernel actualmente;
- tabla módulo → datos con propietario único;
- correspondencia con las entidades reales del código;
- auditoría de escrituras compartidas;
- riesgos MOD-01 a MOD-04;
- planes preventivos y correctivos;
- arc42 sección 8 actualizada;
- C4 Nivel 3 del Backend API;
- prueba automática de modularidad;
- ejecución mediante GitHub Actions;
- Quality Gate de SonarQube Cloud superado;
- trazabilidad S6;
- registro actualizado del uso de IA.

La arquitectura continúa siendo un **monolito modular**.

La evolución realizada durante S6 fortalece sus fronteras internas y la
propiedad de los datos sin introducir microservicios, nueva infraestructura o
límites de dominio artificiales.
