# Aspectos del proyecto - CampusMarket

Este documento mantiene la trazabilidad de los aspectos de CampusMarket desde
los requisitos y decisiones arquitectónicas hasta su implementación y evidencia
verificable.

La cadena general de trazabilidad utilizada es:

**Aspecto → Requisito → C4 → ADR → Código → Pruebas → Evidencia**

A partir de S6, la trazabilidad de dominio se complementa con:

**Aspecto → Contexto delimitado → Propietario del dato → C4 Nivel 3 → Código → Auditoría → Prueba automática**

A partir de S7, la trazabilidad de integración incorpora además:

**Aspecto → Contrato OpenAPI → Proveedor FastAPI → Prueba de contrato**

La evolución de persistencia se registra mediante:

**Observación docente → ADR-0004 → C4 → Código → MySQL → Pruebas**

---

## Matriz general de trazabilidad

| ID | Aspecto | Requisito | C4 | ADR | Código | Pruebas | Evidencia |
|---|---|---|---|---|---|---|---|
| ASP-01 | Consulta y búsqueda de productos | [EC-01 - Consulta de productos](./arc42/10-escenarios-de-calidad.md#ec-01---consulta-de-productos) | [C4 Nivel 2](./c4/02-contenedores.md) | Sin ADR específico: escenario aún no materializado | No materializado completamente | Sin prueba específica de EC-01 | Escenario definido y asociado al contexto Catálogo |
| ASP-02 | Gestión segura de publicaciones | [EC-02 - Protección de publicaciones](./arc42/10-escenarios-de-calidad.md#ec-02---protección-de-publicaciones) | [C4 Nivel 1](./c4/01-contexto.md) | Sin ADR específico: escenario aún no materializado | No materializado completamente | Sin prueba específica de EC-02 | Relacionado con Usuarios, Publicaciones y Administración |
| ASP-03 | Evolución de la gestión de productos | [EC-03 - Modificación del sistema](./arc42/10-escenarios-de-calidad.md#ec-03---modificación-del-sistema) | [C4 Nivel 2](./c4/02-contenedores.md) / [C4 Nivel 3](./c4/03-componentes-backend.md) | [ADR-0001 - Monolito modular](./adr/0001-usar-monolito-modular.md) | [`backend/app/publicaciones/`](../backend/app/publicaciones/) | [`test_publicaciones_vertical.py`](../backend/tests/test_publicaciones_vertical.py) | Evidencia S3/S4 y profundización modular S6 |
| ASP-04 | Recuperación del prototipo | [EC-04 - Recuperación del prototipo](./arc42/10-escenarios-de-calidad.md#ec-04---recuperación-del-prototipo) | [C4 Nivel 1](./c4/01-contexto.md) | [ADR-0001](./adr/0001-usar-monolito-modular.md) | [`scripts/run_s4.ps1`](../scripts/run_s4.ps1) | [`test_health.py`](../backend/tests/test_health.py) | [Evidencia de arranque](./evidencias/arranque-un-comando-2026-09-04.md) |
| ASP-05 | Creación de publicaciones | [Alcance funcional](./arc42/ARC42.md#32-alcance-funcional) | [C4 Nivel 2](./c4/02-contenedores.md) / [C4 Nivel 3](./c4/03-componentes-backend.md) | [ADR-0001](./adr/0001-usar-monolito-modular.md) / [ADR-0004](./adr/0004-migrar-persistencia-a-mysql.md) | [`router.py`](../backend/app/publicaciones/router.py), [`service.py`](../backend/app/publicaciones/service.py), [`repository.py`](../backend/app/publicaciones/repository.py) | [`test_publicaciones_vertical.py`](../backend/tests/test_publicaciones_vertical.py) | Corte vertical vigente con MySQL |
| ASP-06 | Degradación controlada de persistencia | [EC-05](./arc42/10-escenarios-de-calidad.md#ec-05---degradación-ante-bloqueo-temporal-de-persistencia) | [C4 Nivel 2](./c4/02-contenedores.md) / [Vista de ejecución](./arc42/06-vista-ejecucion.md) | [ADR-0002](./adr/0002-manejo-bloqueo-sqlite.md) histórico / [ADR-0004](./adr/0004-migrar-persistencia-a-mysql.md) vigente | [`repository.py`](../backend/app/publicaciones/repository.py), [`service.py`](../backend/app/publicaciones/service.py), [`router.py`](../backend/app/publicaciones/router.py) | [`test_publicaciones_vertical.py`](../backend/tests/test_publicaciones_vertical.py) | Evidencia histórica SQLite + verificación vigente MySQL |
| ASP-07 | Contrato ejecutable de API | [EC-06 - Compatibilidad del contrato](./arc42/10-escenarios-de-calidad.md#ec-06---compatibilidad-del-contrato-de-api) | [C4 Nivel 2](./c4/02-contenedores.md) / [Vista de ejecución](./arc42/06-vista-ejecucion.md) | [ADR-0003](./adr/0003-usar-integracion-sincrona-http-json.md) | [`openapi-v1.json`](../contracts/openapi-v1.json), [`main.py`](../backend/app/main.py), [`router.py`](../backend/app/publicaciones/router.py) | [`test_contrato_openapi.py`](../backend/tests/test_contrato_openapi.py) | Contrato OpenAPI versionado y verificable |
| ASP-08 | Migración de persistencia a MySQL | Observación docente sobre persistencia vigente | [C4 Nivel 2](./c4/02-contenedores.md) / [C4 Nivel 3](./c4/03-componentes-backend.md) | [ADR-0004 - Migrar persistencia a MySQL](./adr/0004-migrar-persistencia-a-mysql.md) | [`repository.py`](../backend/app/publicaciones/repository.py), [`requirements.txt`](../backend/requirements.txt), [`.gitignore`](../.gitignore) | [`test_publicaciones_vertical.py`](../backend/tests/test_publicaciones_vertical.py), [`test_modularidad_s6.py`](../backend/tests/test_modularidad_s6.py) | Implementación vigente MySQL/PyMySQL |

---

## Alcance de materialización

Los aspectos **ASP-01** y **ASP-02** continúan definidos arquitectónicamente,
pero todavía no cuentan con una materialización funcional completa.

No se asocian pruebas artificialmente a escenarios que aún no están
implementados.

La materialización vigente se concentra principalmente en:

- Gestión de Publicaciones;
- integración Flutter → FastAPI;
- persistencia MySQL;
- contrato OpenAPI;
- modularidad;
- degradación controlada ante indisponibilidad.

---

# Trazabilidad histórica S4

Durante S4 se materializó el primer corte vertical funcional.

En ese momento, la arquitectura utilizada era:

```text
Flutter
   ↓
FastAPI
   ↓
Gestión de Publicaciones
   ↓
SQLite
```

Esta referencia se conserva como historia arquitectónica.

La creación de publicaciones permitió demostrar:

* formulario Flutter;
* solicitud HTTP;
* lógica de backend;
* persistencia;
* consulta posterior.

La arquitectura de S4 no representa el estado actual de persistencia.

---

## Verificación histórica de EC-03 en S4

Durante S4 se incorporó el estado:

`reacondicionado`

como modificación verificable dentro del módulo Publicaciones.

El cambio se mantuvo dentro de:

`backend/app/publicaciones/`

sin modificar:

* autenticación;
* catálogo;
* administración;
* fronteras del monolito modular.

En aquel momento la prueba utilizaba SQLite.

Actualmente la misma prueba ha evolucionado y utiliza MySQL.

Por tanto, la referencia a SQLite debe interpretarse exclusivamente dentro del
contexto histórico de S4.

---

# Trazabilidad histórica S5

Durante S5 se trabajó el aspecto:

**ASP-06 - Degradación controlada ante bloqueo de persistencia**

La cadena histórica fue:

```text
ASP-06
   ↓
R-07 / EC-05
   ↓
C4 Nivel 2
   ↓
ADR-0002
   ↓
Código
   ↓
Prueba
   ↓
Medición
   ↓
Evidencia
```

Durante ese corte se mantenía SQLite.

La restricción R-07 indicaba no incorporar nueva infraestructura para resolver
el reto.

ADR-0002 implementó:

* espera SQLite acotada;
* detección de `SQLITE_BUSY`;
* detección de `SQLITE_LOCKED`;
* respuesta HTTP `503`;
* ausencia de escritura parcial;
* recuperación posterior.

### Línea base histórica

* HTTP durante bloqueo: `500`;
* tiempo durante bloqueo: `7.323 s`;
* escritura parcial: `No`;
* recuperación posterior: `201`.

### Resultado histórico posterior

* HTTP durante bloqueo: `503`;
* tiempo durante bloqueo: `1.283 s`;
* escritura parcial: `No`;
* recuperación posterior: `201`;
* tiempo de recuperación: `0.006 s`.

Estas mediciones permanecen como evidencia histórica.

No representan el comportamiento técnico vigente de MySQL.

Evidencias:

* [Línea base](./evidencias/linea-base-bloqueo-sqlite-2026-09-05.md)
* [Medición posterior](./evidencias/medicion-bloqueo-sqlite-2026-09-06.md)
* [ADR-0002](./adr/0002-manejo-bloqueo-sqlite.md)

---

# Trazabilidad S6 — Dominio y modularidad

Durante S6 se hicieron explícitos los límites de dominio del monolito modular y
la propiedad de los datos.

Los contextos definidos son:

| Contexto delimitado      | Responsabilidad                | Estado actual                                   |
| ------------------------ | ------------------------------ | ----------------------------------------------- |
| Gestión de Usuarios      | Identidad y autenticación      | Límite definido, no materializado completamente |
| Gestión de Publicaciones | Ciclo de vida de publicaciones | Materializado                                   |
| Catálogo                 | Consulta, búsqueda y filtrado  | Límite definido                                 |
| Administración           | Moderación y supervisión       | Límite definido                                 |

---

## Propiedad de datos

CampusMarket adopta la regla:

> Cada dato de dominio tiene un único módulo responsable de escribirlo.

La entidad materializada es:

`publicaciones`

Su propietario es:

**Gestión de Publicaciones**

El escritor productivo es:

`backend/app/publicaciones/repository.py`

La correspondencia vigente es:

| Dato / entidad  | Contexto propietario     | Componente escritor                       | Otros contextos con escritura |
| --------------- | ------------------------ | ----------------------------------------- | ----------------------------- |
| `publicaciones` | Gestión de Publicaciones | `backend/app/publicaciones/repository.py` | Ninguno                       |

Los campos persistidos son:

* `id`;
* `titulo`;
* `descripcion`;
* `precio`;
* `modalidad`;
* `estado`.

---

## Auditoría de modularidad

La auditoría de S6 se mantiene en:

[Auditoría de modularidad S6](./evidencias/auditoria-modularidad-s6-2026-09-12.md)

En S6 se inspeccionaron:

* `INSERT`;
* `UPDATE`;
* `DELETE`;
* repositorios;
* servicios;
* accesos a `publicaciones`;
* uso de SQLite existente en ese momento.

El resultado fue:

**No se detectaron escrituras compartidas entre módulos de dominio.**

La evolución posterior hacia MySQL mantiene la misma regla arquitectónica.

---

## Riesgos vigentes

| ID     | Riesgo                                                          | Tratamiento                                              |
| ------ | --------------------------------------------------------------- | -------------------------------------------------------- |
| MOD-01 | Catálogo podría acceder directamente a la tabla `publicaciones` | Consumir capacidades de Publicaciones mediante contratos |
| MOD-02 | Administración podría modificar directamente `publicaciones`    | Solicitar operaciones mediante Gestión de Publicaciones  |
| MOD-03 | Propietario de publicación aún no materializado                 | Mantener Usuarios como dueño de identidad                |
| MOD-04 | Tests o scripts podrían acoplarse al motor de persistencia      | Mantener esos accesos fuera del código productivo        |

---

## C4 Nivel 3 vigente

La materialización actual sigue:

```text
Frontend Web
     ↓
API de Publicaciones
     ↓
Servicio de Publicaciones
     ↓
Repositorio de Publicaciones
     ↓
MySQL
```

Correspondencia:

| Elemento C4 Nivel 3          | Código                                    |
| ---------------------------- | ----------------------------------------- |
| Entrada de aplicación        | `backend/app/main.py`                     |
| API de Publicaciones         | `backend/app/publicaciones/router.py`     |
| Servicio de Publicaciones    | `backend/app/publicaciones/service.py`    |
| Repositorio de Publicaciones | `backend/app/publicaciones/repository.py` |
| Persistencia                 | MySQL                                     |

---

## Verificación automática de modularidad

La prueba:

[`backend/tests/test_modularidad_s6.py`](../backend/tests/test_modularidad_s6.py)

verifica actualmente que:

* `repository.py` sea el único escritor productivo de `publicaciones`;
* otros contextos no utilicen directamente PyMySQL para escribir
  `publicaciones`;
* otros contextos no importen el repositorio de Publicaciones;
* la dirección se mantenga:

```text
router → service → repository → MySQL
```

---

# Trazabilidad S7 — API-first

Durante S7 se formaliza la interfaz entre:

**Frontend Flutter → Backend FastAPI**

La comunicación vigente utiliza:

* HTTP;
* JSON;
* estilo REST;
* comportamiento síncrono.

El contrato está versionado en:

`contracts/openapi-v1.json`

Los endpoints materializados son:

* `POST /publicaciones`;
* `GET /publicaciones`;
* `GET /health`.

La decisión se registra mediante:

[ADR-0003 - Integración síncrona HTTP/JSON](./adr/0003-usar-integracion-sincrona-http-json.md)

---

## Verificación del contrato

La prueba:

[`backend/tests/test_contrato_openapi.py`](../backend/tests/test_contrato_openapi.py)

compara:

```text
contracts/openapi-v1.json
        ↕
FastAPI
```

Esto permite detectar incompatibilidades entre:

* contrato;
* implementación;
* proveedor.

La trazabilidad de ASP-07 es:

```text
ASP-07
   ↓
EC-06
   ↓
ADR-0003
   ↓
OpenAPI
   ↓
FastAPI
   ↓
test_contrato_openapi.py
```

---

# Trazabilidad de migración MySQL — ADR-0004

La evolución de persistencia se origina en una observación realizada por el
docente después del primer corte.

La observación indicó que la persistencia debía evolucionar de SQLite hacia
MySQL.

Por tanto, la migración no corresponde únicamente a una preferencia técnica del
equipo.

La decisión se registra mediante:

[ADR-0004 - Migrar persistencia a MySQL](./adr/0004-migrar-persistencia-a-mysql.md)

---

## Persistencia vigente

La tecnología actual es:

**MySQL**

El mecanismo de acceso es:

**PyMySQL**

El acceso productivo permanece encapsulado en:

`backend/app/publicaciones/repository.py`

La dirección vigente es:

```text
router.py
   ↓
service.py
   ↓
repository.py
   ↓
PyMySQL
   ↓
MySQL
```

---

## Consecuencias de la migración

La migración modifica:

* motor de persistencia;
* driver de acceso;
* configuración de conexión;
* pruebas de integración;
* documentación C4 y arc42.

No modifica:

* monolito modular;
* propietario de `publicaciones`;
* límites de contexto;
* comunicación Flutter → FastAPI;
* contrato OpenAPI;
* dirección router → service → repository.

---

## Verificación vigente de MySQL

La prueba:

[`backend/tests/test_publicaciones_vertical.py`](../backend/tests/test_publicaciones_vertical.py)

verifica actualmente:

* `POST /publicaciones`;
* HTTP `201`;
* persistencia real en MySQL;
* `GET /publicaciones`;
* recuperación del dato;
* respuesta `503` cuando la persistencia no está disponible.

La migración también se verifica mediante:

[`backend/tests/test_modularidad_s6.py`](../backend/tests/test_modularidad_s6.py)

para comprobar que la sustitución tecnológica no rompa las fronteras del
monolito modular.

---

## Cadena de trazabilidad de ADR-0004

```text
Observación docente
        ↓
ADR-0004
        ↓
C4 Nivel 2
        ↓
C4 Nivel 3
        ↓
arc42
        ↓
repository.py
        ↓
PyMySQL
        ↓
MySQL
        ↓
test_publicaciones_vertical.py
```

---

# Estado arquitectónico vigente

El recorrido actual del sistema es:

```text
Flutter Web
    ↓ HTTP/JSON síncrono
    ↓ OpenAPI
FastAPI
    ↓
router.py
    ↓
service.py
    ↓
repository.py
    ↓ PyMySQL / SQL
MySQL
```

Las principales decisiones vigentes son:

* ADR-0001: monolito modular;
* ADR-0003: integración síncrona HTTP/JSON;
* ADR-0004: persistencia MySQL.

ADR-0002 permanece como evidencia histórica del primer corte.

---

## Cadena de trazabilidad actual

```text
Aspecto
   ↓
Requisito / observación
   ↓
ADR
   ↓
C4
   ↓
Contrato
   ↓
Código
   ↓
Persistencia
   ↓
Pruebas
   ↓
Evidencia
```

Para Gestión de Publicaciones:

```text
ASP-03 / ASP-05 / ASP-06 / ASP-07 / ASP-08
        ↓
Gestión de Publicaciones
        ↓
Dueño de publicaciones
        ↓
C4 Nivel 3
        ↓
router.py → service.py → repository.py
        ↓
OpenAPI + MySQL
        ↓
test_modularidad_s6.py
test_publicaciones_vertical.py
test_contrato_openapi.py
```

De esta forma, CampusMarket mantiene trazabilidad entre la evolución histórica
del proyecto y la arquitectura vigente, sin reescribir decisiones anteriores ni
presentar tecnologías históricas como si continuaran activas.
