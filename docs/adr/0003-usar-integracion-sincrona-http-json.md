# ADR-0003 - Usar integración síncrona HTTP/JSON para publicaciones

**Estado:** Aceptado

**Fecha:** 2026-09-15

**Decisión:** Mantener la integración síncrona entre Flutter y FastAPI mediante HTTP/JSON REST

**Escenario principal:** EC-06 - Compatibilidad del contrato de API

**Escenario relacionado:** EC-05 - Degradación ante bloqueo temporal de persistencia

**Aspectos relacionados:** ASP-05 - Creación de publicaciones; ASP-07 - Contrato ejecutable de la API

---

## 1. Contexto

El corte vertical vigente de CampusMarket permite que un estudiante cree y
consulte publicaciones mediante este recorrido:

**Flutter Web → FastAPI → Gestión de Publicaciones → SQLite**

El usuario necesita conocer inmediatamente si la publicación fue aceptada
(`201`), si sus datos son inválidos (`422`) o si la persistencia está
temporalmente indisponible (`503`). La interfaz y el proveedor deben compartir
un contrato explícito para evitar que un cambio de ruta, campo, tipo o código
de respuesta rompa al consumidor en silencio.

La decisión se evalúa por **acoplamiento temporal y modos de fallo**, no por la
afirmación genérica de que una opción sea más rápida.

## 2. Fuerzas arquitectónicas

- respuesta inmediata requerida en crear y consultar publicaciones;
- contrato OpenAPI 3.1 ejecutable y versionado;
- correspondencia entre contrato, cliente Flutter y proveedor FastAPI;
- manejo visible de indisponibilidad mediante HTTP `503` en un máximo de `2 s`;
- simplicidad operativa del monolito modular y la restricción de no agregar
  infraestructura sin evidencia;
- evolución compatible para no romper consumidores existentes.

## 3. Alternativas evaluadas

### A. Integración síncrona HTTP/JSON REST

El frontend realiza una solicitud y espera la respuesta del backend dentro de
la misma interacción.

**Ventajas:**

- entrega confirmación inmediata al usuario;
- corresponde con el código y el C4 vigentes;
- OpenAPI describe rutas, cuerpos, esquemas y respuestas;
- los fallos se expresan mediante códigos HTTP verificables;
- no agrega infraestructura.

**Desventajas y riesgos:**

- existe acoplamiento temporal: frontend y backend deben estar disponibles al
  mismo tiempo;
- una respuesta lenta mantiene al usuario esperando;
- los cambios incompatibles del proveedor rompen al consumidor si el pipeline
  no los detecta.

### B. Integración asíncrona mediante cola o eventos

El frontend enviaría un comando y el resultado se procesaría posteriormente.

**Ventajas:**

- reduce el acoplamiento de disponibilidad;
- permite absorber interrupciones temporales del consumidor o procesador.

**Desventajas y riesgos:**

- no confirma de inmediato si la publicación quedó persistida;
- obliga a diseñar estados pendientes, notificación posterior, reintentos,
  idempotencia, duplicados y consistencia eventual;
- requiere infraestructura y operación que no existen en el alcance actual;
- AsyncAPI no correspondería con la implementación vigente.

**Resultado:** descartada para el corte vertical actual. Puede reconsiderarse
para operaciones futuras que toleren respuesta diferida.

## 4. Decisión

CampusMarket adopta la **Alternativa A: integración síncrona HTTP/JSON REST**
entre el Frontend Web y el Backend API.

El contrato fuente de verdad se versiona en:

[`contracts/openapi-v1.json`](../../contracts/openapi-v1.json)

La versión pública inicial es `1.0.0`. Los cambios compatibles conservan la
versión mayor; un cambio incompatible requiere una nueva versión mayor y un
periodo de coexistencia o migración del consumidor.

Se consideran incompatibles, entre otros:

- eliminar o renombrar una ruta u operación;
- retirar un campo de respuesta;
- cambiar el tipo o significado de un campo;
- hacer obligatorio un campo que antes era opcional;
- eliminar un código de respuesta pactado.

Agregar un campo opcional o una operación nueva es compatible siempre que no
altere el significado de lo existente.

## 5. Modos de fallo aceptados y tratamiento

| Condición | Comportamiento pactado | Consecuencia para el usuario |
|---|---|---|
| Backend no disponible | falla la solicitud HTTP | la interfaz informa que no pudo comunicarse y permite reintentar |
| Datos inválidos | HTTP `422` con JSON de validación | el usuario corrige la entrada |
| SQLite bloqueada | HTTP `503` con `ErrorResponse` en `≤ 2 s` | la interfaz informa indisponibilidad temporal |
| Respuesta tardía | el cliente permanece acoplado hasta respuesta o timeout | debe definirse timeout de cliente al evolucionar el prototipo |
| Cambio incompatible | falla `test_contrato_openapi.py` en CI | el check queda en rojo; al marcarlo como requerido, GitHub bloquea la integración |

El tratamiento de SQLite permanece definido por
[ADR-0002](./0002-manejo-bloqueo-sqlite.md) y EC-05.

## 6. Consecuencias

### Positivas

- contrato y proveedor se comparan automáticamente;
- se conservan las fronteras del monolito modular;
- el flujo sigue siendo sencillo de observar y depurar;
- las operaciones poseen identificadores estables para generar clientes;
- un cambio no negociado deja de llegar silenciosamente al consumidor.

### Negativas y compromisos

- se acepta acoplamiento temporal entre Flutter y FastAPI;
- contrato y código deben evolucionar en el mismo cambio revisado;
- la prueba es deliberadamente estricta y también detectará cambios de
  metadatos o esquemas que deben negociarse;
- si aparecen operaciones que toleran espera, la estrategia deberá reevaluarse
  en otro ADR en lugar de editar este registro aceptado.

## 7. Trazabilidad y verificación

| Elemento | Evidencia |
|---|---|
| Contrato OpenAPI 3.1 | `contracts/openapi-v1.json` |
| Proveedor | `backend/app/main.py`, `backend/app/publicaciones/router.py` |
| Consumidor vigente | `frontend/campusmarket/lib/publicaciones/publicaciones_api.dart` |
| Prueba de contrato | `backend/tests/test_contrato_openapi.py` |
| Pipeline | `.github/workflows/backend-tests.yml` |
| Flujo de ejecución | `docs/arc42/06-vista-ejecucion.md` |
| Relaciones de contenedores | `docs/c4/02-contenedores.puml` |
| Fallo incompatible demostrado | `docs/evidencias/fallo-contrato-s7-2026-09-15.md` |

La decisión no agrega colas, eventos, servicios ni contenedores nuevos; cambia
la precisión del contrato y la forma de impedir cambios incompatibles.
