# 9. Decisiones arquitectónicas

Las decisiones arquitectónicas de CampusMarket se mantienen en registros ADR independientes. Esta sección no repite su contenido; funciona como índice trazable.

| ADR | Estado | Decisión | Escenario principal |
|---|---|---|---|
| [ADR-0001](../adr/0001-usar-monolito-modular.md) | Aceptado | Adoptar un monolito modular como estrategia arquitectónica inicial. | EC-03 - Modificación del sistema |

La implementación de S4 conserva las fronteras definidas por ADR-0001. El corte vertical se implementa dentro del módulo `publicaciones` y no convierte los módulos en servicios distribuidos.
