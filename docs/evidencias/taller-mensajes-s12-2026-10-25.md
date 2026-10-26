# Taller aplicado S12 — Mensajes y consistencia · CampusMarket

## Alcance reproducible
Operación inspiradora: `POST /publicaciones`, evento conceptual posterior `PublicacionCreada.v1` para notificación secundaria. **No existe producción de mensajes en la API real**. Prototipo estrictamente aislado; no modifica datos de CampusMarket, arquitectura C4 productiva ni ADR-0022. ADR-0023 registra expresamente **no incorporarlo al sistema**.

Ejecutar desde raíz del repositorio, Python 3.12, sin paquetes adicionales:
```bash
python -m unittest discover -s backend/tests -p 'test_taller_mensajes_s12.py' -v
python scripts/taller_mensajes_s12.py
```
El workflow dedicado conserva la traza en artefacto. **No atribuir un run exitoso antes de verificar GitHub Actions con SHA y URL.**

## Contrato y compatibilidad
`contracts/messages/publicacion-creada-v1.schema.json` exige `message_id`, `correlation_id`, `publication_id` (>0), `title` no vacío y `schema_version=1`. Campos adicionales opcionales son compatibles; ausencia de campos requeridos o versión mayor incompatible. El simulador valida explícitamente los campos conocidos; el esquema es referencia contractual y no se afirma validación JSON Schema en runtime.

## Garantía y consecuencias
`at-least-once` **simulada** mediante reentrega explícita; un duplicado es posible. La garantía no proviene de un broker durable. Duplicados con el mismo `message_id` se ignoran tras efecto atómico en SQLite; si productor asigna otro ID al mismo evento semántico, podrían generarse notificaciones adicionales. Se debe mantener identidad estable en reintentos reales.

## Reintentos, backoff y fallidos
Máximo **3 intentos**; fallos recuperables simulados generan retrasos lógicos programados de **2 y 4 segundos** registrados en traza, sin `sleep` y sin afirmar temporización real. Tras el tercero, `dead_letters` almacena JSON original, motivo e intentos; no hay reintento infinito. Una caída del proceso perdería la cola no persistida.

## Pruebas automáticas
| Prueba | Propiedad |
|---|---|
| `test_duplicate_redelivery_is_idempotent` | Dos entregas, un único efecto, log de duplicado |
| `test_recoverable_failure_retry_and_trace` | Error recuperable al primer intento, segundo exitoso, backoff 2 s y correlación |
| `test_permanent_failure_enters_dead_letter_store` | Agotamiento y registro de DLQ, backoff 2/4 |
| `test_compatibility_rejects_major_version` | Rechazo de versión incompatible |

## Trazabilidad
Cada línea JSON registra `time`, `message_id`, `correlation_id`, `stage`, `attempt`; por ejemplo la secuencia `producer_published → consumer_received → attempt_failed → retry_scheduled → consumer_received → consumer_acked → duplicate_skipped`. Evidencia generada con ejecución real en CI y descargable del artefacto `s12-messages-trace-<SHA>`.

## Matriz de once criterios
| Criterio del docente | Evidencia | Estado antes de ejecución CI |
|---|---|---|
| Operación/prototipo y no incorporar | ADR-0023 y este archivo | Documentado |
| Contrato y compatibilidad | schema JSON y sección Contrato | Documentado |
| Garantía y consecuencias | ADR-0023 y simulador | Documentado |
| Idempotencia/deduplicación | `processed.message_id` PRIMARY KEY y `notifications.message_id` UNIQUE | Implementado |
| Reintentos y backoff | `MAX_ATTEMPTS`, `BACKOFF_SECONDS`, log retry | Implementado (tiempo lógico) |
| DLQ | SQLite `dead_letters` | Implementado |
| Test duplicado | `test_duplicate_redelivery_is_idempotent` | Pendiente run |
| Test fallo recuperable | `test_recoverable_failure_retry_and_trace` | Pendiente run |
| Log productor–consumidor | `BrokerSimulator.log` y artefacto CI | Pendiente run |
| ADR comparativo | ADR-0023: HTTP síncrono vs broker vs prototipo | Documentado |
| Límites | Apartado Límites y ADR-0023 | Documentado |

## Límites
No hay transporte de red, broker real, recepción asíncrona, cronómetro de backoff real, outbox productivo, retención/replay automático de DLQ, alta concurrencia ni garantías exactly-once distribuidas. SQLite `:memory:` pierde el estado al cerrar proceso. El consumidor produce una notificación **ficticia**, no envía emails/push ni accede a CampusMarket. Para producción: outbox transaccional, broker durable, workers, idempotencia durable, política de redrive, métricas y pruebas de fallos de proceso.

## Matriz transversal CONTRATO
Repositorio y estructura: ISCOUTB y directorios históricos. ADR nuevo sin editar aceptados. `docs/ia.md` y `docs/aspectos.md` extendidos. CI y SonarCloud: verificar en hash final. Secretos, autores, historial ADR y scanner: **no verificados aquí**, requieren auditoría específica. Estado evaluable: último `master` anterior al cierre, no basta una rama o un PR verde.


## Adenda posterior — backoff temporal verificable

El prototipo conserva `MAX_ATTEMPTS=3` y ahora **ejecuta** `sleep_fn(2)` y `sleep_fn(4)` antes de los reintentos. Por defecto `sleep_fn=time.sleep`, por lo que la demostración experimenta una espera real. En pruebas se inyecta `delays.append` para registrar y verificar exactamente `[2]` en el fallo recuperable y `[2,4]` en la DLQ, sin demoras de reloj real en CI. Se añaden eventos `retry_elapsed` posteriores a cada espera. La inyección valida el protocolo de espera, no mide precisión de un scheduler ni demuestra tiempos distribuidos. Los apartados anteriores que dicen 'tiempo lógico' describen la versión histórica del PR #64; esta adenda corresponde al commit correctivo posterior. ADR-0023 no se modifica: permanece como decisión histórica del montaje original. **Validar run nuevo antes de declarar Cumple**.
