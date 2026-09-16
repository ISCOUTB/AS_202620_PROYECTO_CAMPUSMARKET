
# ADR-0003 - Usar integración síncrona HTTP/JSON para publicaciones

**Estado:** Aceptado

**Fecha:** 2026-09-15

**Decisión:** Mantener la integración síncrona entre Flutter y FastAPI mediante HTTP/JSON REST.

**Escenario principal:** EC-06 - Compatibilidad del contrato de API.

**Aspectos relacionados:** ASP-05 - Creación de publicaciones; ASP-07 - Contrato ejecutable de la API.

---

## 1. Contexto

El corte vertical vigente de CampusMarket permite que un estudiante cree y
consulte publicaciones mediante el siguiente recorrido:

```text
Flutter Web
    ↓ HTTP/JSON
FastAPI
    ↓
Gestión de Publicaciones
    ↓
MySQL
````

El usuario necesita conocer inmediatamente si una publicación fue aceptada,
si los datos enviados son inválidos o si el sistema no puede completar la
operación.

La interfaz Flutter y el proveedor FastAPI deben compartir un contrato explícito
para evitar que un cambio de ruta, campo, tipo o código de respuesta rompa al
consumidor sin ser detectado.

La decisión se evalúa principalmente por:

* acoplamiento temporal;
* simplicidad de integración;
* compatibilidad del contrato;
* modos de fallo observables.

---

## 2. Fuerzas arquitectónicas

* respuesta inmediata requerida al crear y consultar publicaciones;
* contrato OpenAPI versionado;
* correspondencia entre contrato, cliente Flutter y proveedor FastAPI;
* fallos expresados mediante códigos HTTP;
* simplicidad operativa;
* ausencia actual de necesidad de mensajería asíncrona;
* evolución compatible sin romper consumidores existentes.

---

## 3. Alternativas evaluadas

### A. Integración síncrona HTTP/JSON REST

El frontend realiza una solicitud y espera la respuesta del backend dentro de
la misma interacción.

**Ventajas:**

* proporciona confirmación inmediata;
* corresponde con el código actual;
* corresponde con los diagramas C4 vigentes;
* OpenAPI puede describir rutas, cuerpos y respuestas;
* los fallos pueden expresarse mediante códigos HTTP;
* no requiere colas ni brokers.

**Desventajas y riesgos:**

* existe acoplamiento temporal entre frontend y backend;
* una respuesta lenta mantiene al usuario esperando;
* cambios incompatibles pueden romper al consumidor si no son detectados por
  las pruebas de contrato.

### B. Integración asíncrona mediante colas o eventos

El frontend enviaría una solicitud o comando y el procesamiento continuaría de
forma diferida.

**Ventajas:**

* reduce el acoplamiento temporal;
* permite desacoplar determinados procesamientos.

**Desventajas:**

* no proporciona confirmación inmediata de persistencia;
* requiere definir estados pendientes;
* introduce reintentos, idempotencia y consistencia eventual;
* requiere infraestructura adicional;
* no corresponde con el corte vertical actual.

**Resultado:** no se adopta para las operaciones actuales.

---

## 4. Decisión

CampusMarket adopta la integración:

**Flutter → FastAPI mediante HTTP/JSON REST síncrono**

El contrato fuente de verdad se versiona en:

[`contracts/openapi-v1.json`](../../contracts/openapi-v1.json)

La versión inicial del contrato es:

`1.0.0`

La relación arquitectónica vigente es:

```text
Flutter
   ↓
HTTP/JSON
   ↓
Contrato OpenAPI
   ↓
FastAPI
```

La persistencia utilizada internamente por FastAPI no forma parte del contrato
externo entre consumidor y proveedor.

Actualmente esa persistencia corresponde a MySQL y está documentada mediante
ADR-0004.

---

## 5. Cambios compatibles e incompatibles

Se consideran cambios incompatibles, entre otros:

* eliminar una ruta;
* renombrar una operación;
* retirar un campo requerido por el consumidor;
* cambiar el tipo de un campo;
* convertir un campo opcional en obligatorio;
* eliminar un código de respuesta pactado.

Pueden considerarse compatibles:

* agregar una operación nueva;
* agregar campos opcionales;
* ampliar la documentación sin modificar la semántica existente.

---

## 6. Modos de fallo

| Condición                  | Comportamiento esperado                                                   |
| -------------------------- | ------------------------------------------------------------------------- |
| Backend no disponible      | La solicitud HTTP falla y el cliente informa que no pudo comunicarse.     |
| Datos inválidos            | FastAPI responde HTTP `422`.                                              |
| Persistencia no disponible | Backend responde HTTP `503 Service Unavailable`.                          |
| Cambio incompatible de API | `test_contrato_openapi.py` falla.                                         |
| Respuesta tardía           | El consumidor permanece temporalmente acoplado hasta respuesta o timeout. |

El tratamiento específico del bloqueo de SQLite documentado en ADR-0002
pertenece al primer corte y se conserva como evidencia histórica.

La persistencia vigente es MySQL según ADR-0004.

---

## 7. Consecuencias

### Positivas

* contrato y proveedor pueden compararse automáticamente;
* se mantienen las fronteras del monolito modular;
* la integración es sencilla de observar;
* las respuestas poseen semántica HTTP explícita;
* los cambios incompatibles pueden detectarse antes de integrarse.

### Negativas

* existe acoplamiento temporal entre Flutter y FastAPI;
* contrato y código deben mantenerse sincronizados;
* una indisponibilidad del backend afecta directamente al consumidor;
* futuras operaciones que toleren procesamiento diferido podrían requerir una
  decisión distinta.

---

## 8. Verificación

La decisión se verifica mediante:

[`backend/tests/test_contrato_openapi.py`](../../backend/tests/test_contrato_openapi.py)

que compara:

```text
contracts/openapi-v1.json
        ↕
FastAPI
```

La integración funcional se verifica también mediante:

[`backend/tests/test_publicaciones_vertical.py`](../../backend/tests/test_publicaciones_vertical.py)

---

## 9. Trazabilidad

| Elemento             | Evidencia                                                        |
| -------------------- | ---------------------------------------------------------------- |
| Contrato OpenAPI     | `contracts/openapi-v1.json`                                      |
| Proveedor            | `backend/app/main.py`, `backend/app/publicaciones/router.py`     |
| Consumidor           | `frontend/campusmarket/lib/publicaciones/publicaciones_api.dart` |
| Prueba de contrato   | `backend/tests/test_contrato_openapi.py`                         |
| Pipeline             | `.github/workflows/backend-tests.yml`                            |
| Vista de ejecución   | `docs/arc42/06-vista-ejecucion.md`                               |
| C4 Nivel 2           | `docs/c4/02-contenedores.puml`                                   |
| Persistencia vigente | ADR-0004 / MySQL                                                 |

---

## 10. Relación con otras decisiones

### ADR-0001

Se mantiene vigente el monolito modular.

### ADR-0002

Se conserva como evidencia histórica del manejo de bloqueo temporal de SQLite
durante el primer corte.

### ADR-0004

Define la persistencia vigente mediante MySQL y PyMySQL.

ADR-0003 no depende del motor concreto de persistencia.

Su responsabilidad es definir la integración:

**Flutter ↔ FastAPI**

mediante HTTP/JSON y OpenAPI.
