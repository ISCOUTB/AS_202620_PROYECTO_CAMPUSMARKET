
# 9. Decisiones arquitectónicas

Las decisiones arquitectónicas de CampusMarket se mantienen mediante registros
ADR independientes.

Esta sección funciona como índice y mecanismo de trazabilidad entre:

- decisiones;
- restricciones;
- escenarios de calidad;
- código;
- pruebas;
- evidencias;
- evolución arquitectónica.

Las decisiones históricas no se eliminan cuando cambia la arquitectura. Se
conservan para mostrar por qué el sistema tuvo una determinada forma en cada
etapa del proyecto.

---

## 9.1 Índice de decisiones

| ADR | Estado | Decisión | Alcance |
|---|---|---|---|
| [ADR-0001](../adr/0001-usar-monolito-modular.md) | Aceptado | Adoptar un monolito modular como estrategia arquitectónica inicial. | Arquitectura general |
| [ADR-0002](../adr/0002-manejo-bloqueo-sqlite.md) | Histórico para la persistencia actual | Aplicar espera acotada y degradación controlada ante bloqueo temporal de SQLite durante el primer corte. | Persistencia del primer corte / EC-05 |
| [ADR-0003](../adr/0003-usar-integracion-sincrona-http-json.md) | Aceptado | Mantener integración síncrona HTTP/JSON y protegerla mediante un contrato OpenAPI versionado. | Integración Frontend → Backend |
| [ADR-0004](../adr/0004-migrar-persistencia-a-mysql.md) | Aceptado | Migrar la persistencia vigente de SQLite a MySQL a partir de la observación recibida del docente. | Persistencia vigente |

La arquitectura actual combina las decisiones vigentes de la siguiente forma:

```text
ADR-0001
Monolito modular
        ↓
Flutter
        ↓
ADR-0003
HTTP/JSON síncrono + OpenAPI
        ↓
FastAPI
        ↓
router → service → repository
        ↓
ADR-0004
PyMySQL → MySQL
````

ADR-0002 se conserva como evidencia histórica de la arquitectura utilizada
durante el primer corte.

---

# ADR-0001 - Monolito modular

## 9.2 Evidencia de implementación

ADR-0001 se materializó inicialmente durante la construcción del esqueleto
ejecutable de S3.

La implementación introdujo una única aplicación backend FastAPI organizada
mediante módulos asociados a capacidades del negocio:

* `usuarios`;
* `publicaciones`;
* `catalogo`;
* `administracion`.

La incorporación inicial del esqueleto fue consolidada mediante:

* Pull Request:
  [#5 - Completar esqueleto ejecutable de Evidencia S3](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/pull/5)
* Commit de integración:
  [`4dd857a`](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/commit/4dd857a1e238e50956facd7156b967f03ae30db0)

Las evoluciones posteriores conservan estos límites.

La sustitución de SQLite por MySQL no convierte los módulos en servicios
independientes ni modifica la decisión de utilizar un monolito modular.

Actualmente la capacidad con mayor materialización funcional continúa siendo:

`publicaciones`

---

# ADR-0002 - Manejo de bloqueo temporal de SQLite

## 9.3 Contexto histórico

ADR-0002 corresponde específicamente al **primer corte**.

En ese momento estaba vigente la restricción:

**R-07 - Persistencia sin nueva infraestructura durante el primer corte**

y CampusMarket utilizaba:

```text
Flutter Web
    ↓
FastAPI
    ↓
Gestión de Publicaciones
    ↓
SQLite
```

La condición adversa seleccionada fue:

**EC-05 - Degradación ante bloqueo temporal de persistencia**

El objetivo era responder de forma controlada cuando SQLite permanecía
temporalmente bloqueada durante la creación de una publicación.

---

## 9.4 Línea base de ADR-0002

Antes de aplicar la decisión se obtuvo:

| Métrica                | Línea base |
| ---------------------- | ---------: |
| HTTP durante bloqueo   |      `500` |
| Tiempo durante bloqueo |  `7.323 s` |
| Escritura parcial      |       `No` |
| HTTP de recuperación   |      `201` |
| Tiempo de recuperación |  `0.007 s` |

La línea base demostró que el sistema preservaba los datos y podía recuperarse,
pero la indisponibilidad:

* se manifestaba mediante HTTP `500`;
* mantenía la solicitud bloqueada durante `7.323 s`;
* superaba el umbral de `2 s` definido en EC-05.

Evidencia:

[Línea base de bloqueo SQLite](../evidencias/linea-base-bloqueo-sqlite-2026-09-05.md)

---

## 9.5 Decisión aplicada en ADR-0002

Durante el primer corte se mantuvo SQLite y se implementaron:

* timeout SQLite acotado a `0.5 s`;
* detección de `SQLITE_BUSY`;
* detección de `SQLITE_LOCKED`;
* traducción controlada de indisponibilidad;
* HTTP `503 Service Unavailable`;
* ausencia de escrituras parciales;
* preservación de la transacción;
* cierre controlado de conexiones;
* recuperación posterior.

En ese momento el recorrido era:

```text
Flutter
   ↓
FastAPI
   ↓
router
   ↓
service
   ↓
repository
   ↓
SQLite
```

ADR-0002 modificó el comportamiento ante fallos, pero no cambió la topología
del sistema.

---

## 9.6 Resultado histórico de ADR-0002

Después de implementar la decisión:

| Métrica                | Línea base | Después de ADR-0002 | Umbral EC-05 |
| ---------------------- | ---------: | ------------------: | -----------: |
| HTTP durante bloqueo   |      `500` |               `503` |        `503` |
| Tiempo durante bloqueo |  `7.323 s` |           `1.283 s` |      `≤ 2 s` |
| Escritura parcial      |       `No` |                `No` |         `No` |
| HTTP de recuperación   |      `201` |               `201` |        `201` |
| Tiempo de recuperación |  `0.007 s` |           `0.006 s` |  Informativo |

La solicitud pasó de:

**HTTP `500` en `7.323 s`**

a:

**HTTP `503` en `1.283 s`**

sin escrituras parciales.

Evidencia:

[Medición posterior a ADR-0002](../evidencias/medicion-bloqueo-sqlite-2026-09-06.md)

---

## 9.7 Evidencia histórica de implementación de ADR-0002

En el estado correspondiente a S5, la decisión involucró:

```text
backend/app/publicaciones/repository.py
backend/app/publicaciones/service.py
backend/app/publicaciones/router.py
frontend/campusmarket/lib/publicaciones/publicaciones_api.dart
frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart
backend/tests/test_publicaciones_vertical.py
scripts/medir_bloqueo_sqlite.py
```

En aquella versión:

* `repository.py` controlaba las condiciones específicas de SQLite;
* `service.py` propagaba la indisponibilidad dentro del contexto;
* `router.py` respondía HTTP `503`;
* Flutter informaba la condición al usuario;
* `test_publicaciones_vertical.py` verificaba el comportamiento sobre SQLite;
* `medir_bloqueo_sqlite.py` reproducía experimentalmente el bloqueo.

**Importante:** `test_publicaciones_vertical.py` evolucionó posteriormente y
actualmente verifica la persistencia MySQL. Por tanto, las afirmaciones
anteriores describen el estado histórico de S5 y no el contenido vigente de
la prueba.

La evidencia histórica permanece disponible mediante los commits, mediciones
y documentos versionados.

---

## 9.8 Trazabilidad histórica de ADR-0002

La respuesta arquitectónica de S5 fue consolidada mediante:

* Pull Request:
  [#28 - Completar reto arquitectónico S5 del primer corte](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/pull/28)
* Commit:
  [`ff68cf2`](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/commit/ff68cf255b90340634e0760f056870f9a19e9abd)

La cadena histórica es:

```text
ASP-06
   ↓
R-07 / EC-05
   ↓
C4 Nivel 2 del primer corte
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

Elementos relacionados:

* [R-07](02-restricciones.md#r-07-persistencia-sin-nueva-infraestructura-durante-el-primer-corte)
* [EC-05](10-escenarios-de-calidad.md#ec-05---degradación-ante-bloqueo-temporal-de-persistencia)
* [ADR-0002](../adr/0002-manejo-bloqueo-sqlite.md)
* [Línea base](../evidencias/linea-base-bloqueo-sqlite-2026-09-05.md)
* [Medición posterior](../evidencias/medicion-bloqueo-sqlite-2026-09-06.md)
* [Script histórico de medición](../../scripts/medir_bloqueo_sqlite.py)

---

# ADR-0003 - Integración síncrona HTTP/JSON

## 9.9 Decisión de integración

ADR-0003 documenta la forma de integración entre:

**Frontend Flutter → Backend FastAPI**

La comunicación actualmente materializada utiliza:

* HTTP;
* JSON;
* estilo REST;
* comportamiento síncrono.

Cada solicitud espera una respuesta en la misma interacción.

Los endpoints materializados incluyen:

* `POST /publicaciones`;
* `GET /publicaciones`;
* `GET /health`.

---

## 9.10 Contrato OpenAPI

La interfaz del Backend API se mantiene mediante un contrato versionado:

`contracts/openapi-v1.json`

La relación es:

```text
Frontend Flutter
       ↓
HTTP/JSON
       ↓
Contrato OpenAPI
       ↓
FastAPI
```

La correspondencia entre contrato e implementación se verifica mediante:

`backend/tests/test_contrato_openapi.py`

De esta forma OpenAPI no se utiliza únicamente como documentación, sino como
contrato verificable.

---

## 9.11 Consecuencias de ADR-0003

La integración síncrona simplifica el corte vertical actual porque:

* el consumidor recibe la respuesta dentro de la misma interacción;
* no se requieren colas;
* no se requieren brokers;
* no se requiere correlación de mensajes asíncronos.

Como consecuencia existe acoplamiento temporal: frontend y backend deben estar
disponibles durante la interacción.

En el alcance actual esta decisión se considera compatible con las necesidades
del prototipo.

---

# ADR-0004 - Migración de SQLite a MySQL

## 9.12 Origen de la decisión

Durante una revisión posterior al primer corte, el docente realizó la
observación de que la persistencia del proyecto debía evolucionar de SQLite
hacia MySQL.

Por tanto, esta migración no corresponde únicamente a una preferencia
tecnológica del equipo.

Es una corrección arquitectónica realizada a partir de la retroalimentación
académica recibida.

Mantener SQLite como persistencia vigente habría producido una inconsistencia
entre:

* la observación recibida;
* el código;
* C4;
* arc42;
* las pruebas;
* la arquitectura presentada por el equipo.

La decisión completa está registrada en:

[ADR-0004 - Migrar la persistencia de SQLite a MySQL](../adr/0004-migrar-persistencia-a-mysql.md)

---

## 9.13 Decisión vigente de persistencia

La persistencia actual utiliza:

**MySQL**

El acceso desde Python se realiza mediante:

**PyMySQL**

La dependencia tecnológica se encuentra encapsulada en:

`backend/app/publicaciones/repository.py`

La dirección vigente es:

```text
Flutter
   ↓ HTTP/JSON
FastAPI
   ↓
router
   ↓
service
   ↓
repository
   ↓ PyMySQL
MySQL
```

La migración no cambia:

* ADR-0001;
* los límites del monolito modular;
* la propiedad de `publicaciones`;
* la separación router / service / repository;
* ADR-0003;
* el contrato HTTP/JSON del frontend.

---

## 9.14 Implementación de ADR-0004

Los principales elementos relacionados con la migración son:

```text
backend/app/publicaciones/repository.py
backend/requirements.txt
backend/tests/test_publicaciones_vertical.py
backend/tests/test_modularidad_s6.py
.gitignore
```

La configuración de conexión se proporciona mediante variables de entorno.

Las credenciales no deben almacenarse en el repositorio.

El archivo local `.env` permanece excluido mediante `.gitignore`.

---

## 9.15 Verificación vigente de MySQL

La integración con MySQL se verifica mediante:

[`backend/tests/test_publicaciones_vertical.py`](../../backend/tests/test_publicaciones_vertical.py)

La prueba vigente comprueba:

* creación mediante `POST /publicaciones`;
* respuesta HTTP `201`;
* persistencia real en MySQL;
* recuperación posterior mediante `GET /publicaciones`;
* igualdad entre los datos escritos y recuperados;
* degradación controlada mediante HTTP `503` cuando MySQL no está disponible.

La modularidad se verifica mediante:

[`backend/tests/test_modularidad_s6.py`](../../backend/tests/test_modularidad_s6.py)

que comprueba, entre otros aspectos:

* un único escritor productivo de `publicaciones`;
* ausencia de acceso directo desde otros contextos;
* dirección:

  `router → service → repository → MySQL`.

El contrato HTTP continúa verificándose mediante:

[`backend/tests/test_contrato_openapi.py`](../../backend/tests/test_contrato_openapi.py)

---

## 9.16 Relación ADR-0002 → ADR-0004

ADR-0002 y ADR-0004 no representan decisiones contradictorias si se considera
su momento arquitectónico.

### Primer corte

```text
SQLite
   ↓
ADR-0002
   ↓
Manejo controlado de bloqueo
```

### Estado vigente

```text
Observación docente
   ↓
ADR-0004
   ↓
PyMySQL
   ↓
MySQL
```

ADR-0002 conserva valor como evidencia histórica.

ADR-0004 determina la tecnología de persistencia vigente.

Por tanto:

> SQLite pertenece a la historia arquitectónica del primer corte; MySQL
> representa la persistencia actual de CampusMarket.

---

## 9.17 Trazabilidad vigente

La trazabilidad actual puede representarse como:

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
PyMySQL / MySQL
        ↓
pruebas automatizadas
```

A esto se suma la integración definida por ADR-0003:

```text
Frontend
   ↓
OpenAPI
   ↓
FastAPI
   ↓
Gestión de Publicaciones
   ↓
MySQL
```

---

## 9.18 Estado arquitectónico actual

Las decisiones vigentes producen actualmente la siguiente arquitectura:

```text
Flutter Web
    ↓ HTTP/JSON síncrono
    ↓ contrato OpenAPI
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

La estructura conserva:

* monolito modular;
* contextos delimitados;
* propietario único de datos;
* API contractual;
* aislamiento de persistencia;
* degradación controlada;
* pruebas automatizadas.

La documentación histórica de SQLite permanece versionada para conservar la
evolución arquitectónica del proyecto.
