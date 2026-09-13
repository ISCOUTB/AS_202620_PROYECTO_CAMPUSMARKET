# Aspectos del proyecto - CampusMarket

Este documento mantiene la trazabilidad de los aspectos de CampusMarket desde
los requisitos y decisiones arquitectónicas hasta su implementación y evidencia
verificable.

La cadena general de trazabilidad utilizada es:

**Aspecto → Requisito → C4 → ADR → Código → Pruebas → Evidencia**

A partir de S6, la trazabilidad de dominio se complementa con:

**Aspecto → Contexto delimitado → Propietario del dato → C4 Nivel 3 → Código → Auditoría → Prueba automática**

---

## Matriz general de trazabilidad

| ID | Aspecto | Requisito | C4 | ADR | Código | Pruebas | Evidencia |
|---|---|---|---|---|---|---|---|
| ASP-01 | Consulta y búsqueda de productos | [EC-01 - Consulta de productos](./arc42/10-escenarios-de-calidad.md#ec-01---consulta-de-productos) | [C4 Nivel 2](./c4/02-contenedores.md) | Sin ADR específico: escenario aún no materializado | No materializado en el corte vertical actual | Sin prueba específica de EC-01 todavía | Escenario definido en S2; asociado en S6 al contexto Catálogo, todavía no materializado funcionalmente |
| ASP-02 | Gestión segura de publicaciones | [EC-02 - Protección de publicaciones](./arc42/10-escenarios-de-calidad.md#ec-02---protección-de-publicaciones) | [C4 Nivel 1](./c4/01-contexto.md) | Sin ADR específico: escenario aún no materializado | No materializado completamente en el corte vertical actual | Sin prueba específica de EC-02 todavía | Escenario definido en S2; relacionado en S6 con Usuarios, Publicaciones y Administración |
| ASP-03 | Evolución de la gestión de productos | [EC-03 - Modificación del sistema](./arc42/10-escenarios-de-calidad.md#ec-03---modificación-del-sistema) | [C4 Nivel 2](./c4/02-contenedores.md) / [C4 Nivel 3](./c4/03-componentes-backend.md) | [ADR-0001 - Monolito modular](./adr/0001-usar-monolito-modular.md) | [`backend/app/publicaciones/`](../backend/app/publicaciones/), [`publicacion_form_page.dart`](../frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart) | [`test_publicaciones_vertical.py`](../backend/tests/test_publicaciones_vertical.py) | Evidencia S3/S4 y profundización modular en S6 |
| ASP-04 | Recuperación del prototipo | [EC-04 - Recuperación del prototipo](./arc42/10-escenarios-de-calidad.md#ec-04---recuperación-del-prototipo) | [C4 Nivel 1](./c4/01-contexto.md) | [ADR-0001 - Monolito modular](./adr/0001-usar-monolito-modular.md) | [`scripts/run_s4.ps1`](../scripts/run_s4.ps1) | [`test_health.py`](../backend/tests/test_health.py) | [Evidencia de arranque con un comando](./evidencias/arranque-un-comando-2026-09-04.md) |
| ASP-05 | Creación de publicaciones | [Alcance funcional - Gestión de publicaciones](./arc42/ARC42.md#32-alcance-funcional) | [C4 Nivel 2](./c4/02-contenedores.md) / [C4 Nivel 3](./c4/03-componentes-backend.md) | [ADR-0001 - Monolito modular](./adr/0001-usar-monolito-modular.md) | [`publicacion_form_page.dart`](../frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart), [`publicaciones_api.dart`](../frontend/campusmarket/lib/publicaciones/publicaciones_api.dart), [`router.py`](../backend/app/publicaciones/router.py), [`service.py`](../backend/app/publicaciones/service.py), [`repository.py`](../backend/app/publicaciones/repository.py) | [`test_publicaciones_vertical.py`](../backend/tests/test_publicaciones_vertical.py) | Evidencia funcional S4 y correspondencia de componentes S6 |
| ASP-06 | Degradación controlada ante bloqueo de persistencia | [R-07 - Persistencia sin nueva infraestructura](./arc42/02-restricciones.md#r-07-persistencia-sin-nueva-infraestructura-durante-el-primer-corte) / [EC-05 - Degradación ante bloqueo temporal](./arc42/10-escenarios-de-calidad.md#ec-05---degradación-ante-bloqueo-temporal-de-persistencia) | [C4 Nivel 2](./c4/02-contenedores.md) / [C4 Nivel 3](./c4/03-componentes-backend.md) | [ADR-0002 - Manejo de bloqueo SQLite](./adr/0002-manejo-bloqueo-sqlite.md) | [`repository.py`](../backend/app/publicaciones/repository.py), [`service.py`](../backend/app/publicaciones/service.py), [`router.py`](../backend/app/publicaciones/router.py), [`publicaciones_api.dart`](../frontend/campusmarket/lib/publicaciones/publicaciones_api.dart), [`publicacion_form_page.dart`](../frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart) | [`test_publicaciones_vertical.py`](../backend/tests/test_publicaciones_vertical.py) | [Línea base](./evidencias/linea-base-bloqueo-sqlite-2026-09-05.md) / [Medición posterior](./evidencias/medicion-bloqueo-sqlite-2026-09-06.md) |

---

## Alcance de materialización de los aspectos

Los aspectos **ASP-01** y **ASP-02** corresponden a escenarios de calidad
definidos durante la construcción de la línea base arquitectónica en S2.

Estos escenarios permanecen especificados y trazados hacia sus requisitos y
vistas arquitectónicas correspondientes, pero todavía no forman parte completa
del corte vertical implementado.

Por esta razón, las columnas asociadas con ADR, código, pruebas y evidencia
indican explícitamente cuando todavía no existe una materialización verificable,
en lugar de asociar artificialmente elementos que no comprueban realmente
EC-01 o EC-02.

En particular:

- **ASP-01 / EC-01** define el comportamiento esperado para consulta y
  búsqueda de productos, incluida su medida de rendimiento. El contexto
  **Catálogo** está delimitado durante S6, pero todavía no se encuentra
  materializada la capacidad completa de búsqueda y filtrado necesaria para
  verificar el escenario.

- **ASP-02 / EC-02** define la protección de publicaciones frente a
  modificaciones realizadas por usuarios no propietarios. Durante S6 se
  identifican los contextos involucrados en esa responsabilidad, pero el corte
  actual todavía no incorpora el mecanismo completo de autenticación,
  propiedad, autorización y moderación necesario para verificar EC-02.

Estos escenarios permanecen como parte de la arquitectura prevista y podrán
materializarse en la evolución posterior del sistema.

La materialización funcional acumulada hasta S4 se concentra principalmente en
**ASP-03, ASP-04 y ASP-05**, asociados con evolución modular, recuperación del
prototipo y creación de publicaciones.

Para S5 se incorpora **ASP-06**, relacionado con la restricción R-07 y cuya
trazabilidad se completa de extremo a extremo:

**ASP-06 → R-07 / EC-05 → C4 Nivel 2 → ADR-0002 → código → pruebas → evidencia**

S6 no inventa nuevas implementaciones para ASP-01 o ASP-02. Su contribución es
hacer explícitos los límites de dominio, la propiedad de datos y las reglas de
comunicación necesarias para su futura materialización.

---

## Estado de trazabilidad S4

La fila **ASP-05 - Creación de publicaciones** representa el corte vertical
implementado durante S4.

La trazabilidad del corte vertical corresponde al recorrido:

**Interfaz Flutter → API FastAPI → lógica del módulo `publicaciones` → persistencia SQLite**

Durante la verificación local se creó una publicación desde la interfaz Flutter
y se comprobó posteriormente su almacenamiento en SQLite, por lo que las rutas
indicadas corresponden al comportamiento real del prototipo.

La recuperación del prototipo también quedó evidenciada mediante **ASP-04**,
utilizando el script de arranque con un solo comando, la prueba de salud y las
evidencias almacenadas en `docs/evidencias/`.

---

## Verificación de EC-03 en S4

Durante el ajuste final de la Evidencia S4 se incorporó el estado de producto
`reacondicionado`, utilizado como caso concreto para verificar el escenario
**EC-03 - Modificación del sistema**.

El cambio se mantuvo dentro de la capacidad funcional de `publicaciones` y
requirió ajustes únicamente en los elementos directamente relacionados con la
creación, validación y persistencia de publicaciones.

No fue necesario modificar los módulos de autenticación ni búsqueda,
manteniendo las fronteras definidas por el:

**ADR-0001 - Monolito modular**

La prueba automatizada:

[`test_publicaciones_vertical.py`](../backend/tests/test_publicaciones_vertical.py)

crea una publicación con estado `reacondicionado`, verifica su persistencia en
SQLite y posteriormente recupera el registro para comprobar que el nuevo estado
se conserva correctamente.

De esta forma queda trazada la relación:

**EC-03 → ADR-0001 → módulo `publicaciones` → código → prueba automatizada**

---

## Trazabilidad S5

Para la evaluación arquitectónica de S5 se incorporó el aspecto:

**ASP-06 - Degradación controlada ante bloqueo de persistencia**

La cadena completa es:

**ASP-06 → R-07 / EC-05 → C4 Nivel 2 → ADR-0002 → código → prueba automatizada → evidencia antes/después**

La restricción **R-07** mantiene SQLite y conserva el backend como una única
aplicación monolítica modular, sin incorporar una base de datos externa, colas,
cachés distribuidas ni nuevos servicios desplegables.

El escenario **EC-05** verifica la respuesta del corte vertical ante un bloqueo
temporal de persistencia.

### Línea base

La línea base previa al cambio registró:

- HTTP durante bloqueo: `500`;
- tiempo durante bloqueo: `7.323 s`;
- escritura parcial: `No`;
- recuperación posterior: HTTP `201`.

ADR-0002 materializa la respuesta arquitectónica mediante:

- espera SQLite acotada a `0.5 s`;
- detección específica de `SQLITE_BUSY` y `SQLITE_LOCKED`;
- traducción controlada de la indisponibilidad;
- respuesta HTTP `503`;
- ausencia de escritura parcial;
- mensaje explícito al usuario;
- recuperación normal después de liberar SQLite.

### Resultado posterior

Después de aplicar la decisión, la medición formal registró:

- HTTP durante bloqueo: `503`;
- tiempo durante bloqueo: `1.283 s`;
- escritura parcial: `No`;
- recuperación posterior: HTTP `201`;
- tiempo de recuperación: `0.006 s`.

El resultado cumple el umbral establecido por EC-05 de responder en un tiempo
máximo de **2 segundos** durante el bloqueo.

Una ejecución posterior de verificación volvió a confirmar el comportamiento,
obteniendo HTTP `503` en `1.138 s`, sin escritura parcial y con recuperación
HTTP `201`.

La implementación conserva las fronteras:

**Frontend Flutter → Backend FastAPI → Persistencia SQLite**

y no introduce infraestructura adicional.

De esta forma ASP-06 queda trazado desde la restricción arquitectónica hasta
una evidencia reproducible y contrastada con su umbral.

---

# Trazabilidad S6 — Dominio y modularidad

Durante S6 se hicieron explícitos los límites de dominio del monolito modular
de CampusMarket y la propiedad de los datos.

La evidencia se construye sobre el estado real del repositorio y diferencia
entre:

- contextos arquitectónicos definidos;
- capacidades actualmente materializadas;
- responsabilidades previstas para evolución posterior.

Los contextos delimitados identificados son:

| Contexto delimitado | Aspectos relacionados | Responsabilidad | Estado actual |
|---|---|---|---|
| Gestión de Usuarios | ASP-02 | Identidad, autenticación y propiedad de las publicaciones | Límite definido; funcionalidad todavía no materializada |
| Gestión de Publicaciones | ASP-02, ASP-03, ASP-05, ASP-06 | Ciclo de vida de publicaciones y propiedad exclusiva de `publicaciones` | Materializado actualmente |
| Catálogo | ASP-01 | Consulta, búsqueda y filtrado sin adquirir propiedad de `publicaciones` | Límite definido; funcionalidad todavía no materializada |
| Administración | ASP-02 | Supervisión y moderación mediante contratos con Publicaciones | Límite definido; funcionalidad todavía no materializada |

La documentación principal de S6 se encuentra en:

- [`arc42/08-conceptos-transversales.md`](./arc42/08-conceptos-transversales.md)
- [`c4/03-componentes-backend.md`](./c4/03-componentes-backend.md)
- [`c4/03-componentes-backend.puml`](./c4/03-componentes-backend.puml)
- [`evidencias/auditoria-modularidad-s6-2026-09-12.md`](./evidencias/auditoria-modularidad-s6-2026-09-12.md)
- [`test_modularidad_s6.py`](../backend/tests/test_modularidad_s6.py)

---

## Propiedad de datos en S6

CampusMarket adopta como regla arquitectónica:

> Cada dato de dominio tiene un único módulo responsable de escribirlo.

En el estado actual del prototipo se identificó una entidad persistida de
dominio materializada:

`publicaciones`

Su propietario es:

**Gestión de Publicaciones**

La escritura productiva se encuentra encapsulada en:

[`backend/app/publicaciones/repository.py`](../backend/app/publicaciones/repository.py)

La correspondencia de propiedad es:

| Dato / entidad | Contexto propietario | Componente escritor | Otros contextos con escritura |
|---|---|---|---|
| `publicaciones` | Gestión de Publicaciones | `backend/app/publicaciones/repository.py` | Ninguno detectado |

Los campos actualmente persistidos son:

- `id`;
- `titulo`;
- `descripcion`;
- `precio`;
- `modalidad`;
- `estado`.

No se asignan artificialmente entidades persistidas a Usuarios, Catálogo o
Administración porque dichas estructuras todavía no existen en el código
actual.

---

## Auditoría de modularidad S6

La auditoría se encuentra en:

[Auditoría de modularidad S6](./evidencias/auditoria-modularidad-s6-2026-09-12.md)

El recorrido revisó:

- `backend/app/usuarios/`;
- `backend/app/publicaciones/`;
- `backend/app/catalogo/`;
- `backend/app/administracion/`;
- `backend/tests/`;
- `scripts/`.

También se inspeccionaron operaciones relacionadas con:

- `INSERT`;
- `UPDATE`;
- `DELETE`;
- `sqlite3`;
- repositorios;
- servicios;
- accesos sobre la entidad `publicaciones`.

### Resultado

**No se detectaron escrituras compartidas entre módulos de dominio en el estado
actual del repositorio.**

El único escritor productivo identificado para `publicaciones` pertenece a
Gestión de Publicaciones.

Los accesos directos a SQLite identificados en pruebas o scripts de medición no
se clasifican como segundos propietarios de dominio, ya que corresponden a
instrumentación de prueba y permanecen fuera del código productivo de otros
contextos.

---

## Riesgos y planes de corrección

Aunque actualmente no existe una escritura compartida, S6 identifica riesgos de
evolución.

| ID | Riesgo / hallazgo | Tratamiento |
|---|---|---|
| MOD-01 | Catálogo podría acceder o escribir directamente sobre SQLite al implementarse | Consumir capacidades de Publicaciones mediante contratos explícitos y no escribir `publicaciones` |
| MOD-02 | Administración podría modificar directamente `publicaciones` al implementar moderación | Solicitar las operaciones mediante Gestión de Publicaciones y utilizar una capa anticorrupción |
| MOD-03 | La relación entre propietario y publicación todavía no está materializada | Mantener Usuarios como dueño de identidad y almacenar en Publicaciones únicamente la referencia necesaria |
| MOD-04 | Pruebas y scripts acceden directamente a SQLite para verificación experimental | Mantener estos accesos separados del código productivo y documentar su finalidad |

---

## C4 Nivel 3 en S6

S6 incorpora el C4 Nivel 3 del contenedor:

**Backend API**

Documentación:

- [C4 Nivel 3 - Componentes del Backend](./c4/03-componentes-backend.md)
- [Fuente PlantUML](./c4/03-componentes-backend.puml)

La materialización actualmente verificable sigue el recorrido:

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

Su correspondencia con el código es:

| Elemento C4 Nivel 3 | Código |
|---|---|
| Entrada de aplicación | `backend/app/main.py` |
| API de Publicaciones | `backend/app/publicaciones/router.py` |
| Servicio de Publicaciones | `backend/app/publicaciones/service.py` |
| Repositorio de Publicaciones | `backend/app/publicaciones/repository.py` |
| Persistencia | SQLite |

Usuarios, Catálogo y Administración se representan como límites
arquitectónicos definidos, pero no se declaran como capacidades funcionales
materializadas.

---

## Verificación automática de modularidad

Además de la auditoría manual, se incorporó:

[`backend/tests/test_modularidad_s6.py`](../backend/tests/test_modularidad_s6.py)

La prueba verifica que:

- `backend/app/publicaciones/repository.py` sea el único escritor productivo de
  la entidad `publicaciones`;
- `usuarios`, `catalogo` y `administracion` no accedan directamente a SQLite;
- otros contextos no importen directamente el repositorio interno de
  Publicaciones;
- el flujo de Publicaciones mantenga la dirección:

  `router → service → repository → SQLite`;

- la persistencia del contexto permanezca encapsulada en su repositorio.

Esta prueba se ejecuta junto con el resto de pruebas del backend mediante
GitHub Actions.

La prueba automática no reemplaza la auditoría documental; la complementa con
una regla ejecutable que permite detectar futuras violaciones.

---

## Relaciones entre contextos y aspectos

La relación entre los aspectos existentes y los contextos de S6 es:

### ASP-01 → Catálogo

ASP-01 se relaciona con **Catálogo**, porque este contexto será responsable de
consulta, búsqueda, filtrado y organización de publicaciones.

El contexto está delimitado, pero EC-01 todavía no se declara materializado.

### ASP-02 → Usuarios + Publicaciones + Administración

ASP-02 atraviesa varios contextos:

- Usuarios será dueño de la identidad;
- Publicaciones gestionará la publicación y su relación con el propietario;
- Administración solicitará operaciones de moderación mediante contratos.

La ausencia actual de autenticación y autorización completas impide afirmar que
EC-02 ya esté materializado.

### ASP-03 → Gestión de Publicaciones

La mantenibilidad y evolución modular de ASP-03 se relacionan directamente con
el límite de Gestión de Publicaciones y con la dirección interna:

`router → service → repository`

### ASP-05 → Gestión de Publicaciones

ASP-05 representa la capacidad actualmente materializada de creación de
publicaciones y constituye la evidencia funcional principal del contexto.

### ASP-06 → Gestión de Publicaciones

ASP-06 se mantiene dentro del mismo contexto y afecta principalmente el
repositorio, servicio y API de Publicaciones frente a indisponibilidad temporal
de SQLite.

---

## Coherencia con ADR-0001

Los límites principales continúan siendo:

- `usuarios`;
- `publicaciones`;
- `catalogo`;
- `administracion`.

Estos límites ya habían sido definidos por:

[ADR-0001 - Monolito modular](./adr/0001-usar-monolito-modular.md)

Durante S6:

- no se fusionó ningún módulo;
- no se dividió ningún módulo;
- no se reemplazó ningún límite;
- no se introdujeron microservicios;
- no se incorporó nueva infraestructura.

El C4 Nivel 3 profundiza en la estructura interna del Backend API y hace
explícita la materialización actual de Publicaciones, pero no representa un
reajuste de las fronteras establecidas por ADR-0001.

Por esta razón, **no se registra un nuevo ADR de reajuste para S6**.

Si una evolución posterior modifica realmente estas fronteras, deberá
actualizarse el C4 Nivel 3 y documentarse la decisión mediante un nuevo ADR.

---

## Cadena de trazabilidad final S6

La evidencia acumulada permite seguir la cadena:

**Aspecto**
↓
**Contexto delimitado**
↓
**Propietario del dato**
↓
**C4 Nivel 3**
↓
**Código**
↓
**Auditoría**
↓
**Prueba automática**

Para la parte materializada de Gestión de Publicaciones:

```text
ASP-03 / ASP-05 / ASP-06
        ↓
Gestión de Publicaciones
        ↓
Dueño de publicaciones
        ↓
C4 Nivel 3
        ↓
router.py → service.py → repository.py
        ↓
auditoria-modularidad-s6-2026-09-12.md
        ↓
test_modularidad_s6.py
```

De esta forma, S6 no se limita a describir módulos conceptualmente:
la documentación arquitectónica se contrasta con el código existente y se
complementa mediante una verificación automática de las reglas de modularidad.
