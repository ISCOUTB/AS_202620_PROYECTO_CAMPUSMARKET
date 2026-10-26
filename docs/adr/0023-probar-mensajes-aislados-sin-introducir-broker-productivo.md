# ADR-0023 — Probar mensajería aislada sin introducir un broker productivo

- Estado: Aceptado para el **prototipo formativo aislado** de S12.
- Fecha: 2026-10-25.
- Relación: ADR-0022 continúa vigente sin modificaciones.

## Contexto
CampusMarket confirma la creación de publicaciones síncronamente en MySQL. Enviar una notificación secundaria puede desacoplarse temporalmente, pero el MVP no requiere todavía despliegue de consumidor ni mensajería productiva. Se necesita demostrar entrega, duplicados y recuperación con bajo riesgo.

## Opciones
| Alternativa | Ventaja | Coste y consecuencia |
|---|---|---|
| HTTP síncrono al subsistema de notificaciones | Simplicidad, resultado inmediato | Mayor latencia y acoplamiento de disponibilidad: fallar notificación puede bloquear publicación |
| Broker productivo y outbox transaccional | Entrega durable y escalamiento desacoplado | Broker, monitoreo, deduplicación, idempotencia, outbox y operación real no justificados para MVP |
| **Simulador aislado de cola** | Permite probar at-least-once, reintentos, DLQ y logs sin cambiar la API | No acredita transporte real, durabilidad de cola, concurrencia ni publicación real |

## Decisión
Construir únicamente un **prototipo aislado** en `scripts/taller_mensajes_s12.py` que representa `PublicacionCreada.v1` y una notificación secundaria ficticia. **No incorporarlo a CampusMarket productivo**. Mantener la transacción síncrona MySQL y el C4 L2 existente, sin broker nuevo.

## Garantías y consecuencias
- Entrega simulada **al menos una vez (at-least-once)**: el consumidor puede recibir duplicados.
- Deduplicación por `message_id` persistido en SQLite del simulador. `notifications.message_id` es UNIQUE y la inserción de deduplicación y efecto comparten transacción SQLite. Distintos `message_id` con el mismo `publication_id` no quedan deduplicados semánticamente.
- Tres intentos máximos; backoff lógico de 2 s y 4 s sin dormir realmente. Al agotarse: `dead_letters` con payload, número de intentos y motivo. La cola de entrada no es persistente: no prometer supervivencia a crash de proceso.
- Log por `correlation_id`, `message_id`, fase e intento, desde productor a consumidor.
- Compatible: campos adicionales opcionales manteniendo `schema_version=1` y campos requeridos. Incompatible: retirar/renombrar campos requeridos, alterar su semántica o cambiar versión mayor.
- El prototipo no resuelve atomicidad entre INSERT productivo y publicación de evento: adoptar esto realmente requeriría **transactional outbox**, versionado, monitoreo y recuperación.

## Trazabilidad
- Requisito: Taller aplicado S12 — Mensajes y consistencia.
- C4: sin cambios; MySQL y API son los contenedores existentes.
- Esquema: `contracts/messages/publicacion-creada-v1.schema.json`.
- Implementación: `scripts/taller_mensajes_s12.py`.
- Pruebas: `backend/tests/test_taller_mensajes_s12.py`.
- CI: `.github/workflows/s12-taller-mensajes.yml`.
- Evidencia: `docs/evidencias/taller-mensajes-s12-2026-10-25.md`.
