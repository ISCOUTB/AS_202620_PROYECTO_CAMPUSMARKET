# 9. Decisiones arquitectónicas

Las decisiones arquitectónicas de CampusMarket se mantienen en registros ADR independientes. Esta sección no repite su contenido; funciona como índice trazable.

| ADR | Estado | Decisión | Escenario principal |
|---|---|---|---|
| [ADR-0001](../adr/0001-usar-monolito-modular.md) | Aceptado | Adoptar un monolito modular como estrategia arquitectónica inicial. | EC-03 - Modificación del sistema |

## Evidencia de implementación de ADR-0001

La decisión definida en ADR-0001 se materializó inicialmente durante la
construcción del esqueleto ejecutable de la Evidencia S3.

La implementación introdujo una única aplicación backend en FastAPI
organizada mediante módulos asociados con capacidades del negocio:

- `usuarios`
- `publicaciones`
- `catalogo`
- `administracion`

La incorporación del esqueleto ejecutable fue consolidada mediante:

- Pull Request: [#5 - Completar esqueleto ejecutable de Evidencia S3](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/pull/5)
- Commit de integración: [`4dd857a`](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/commit/4dd857a1e238e50956facd7156b967f03ae30db0)

Este commit constituye la evidencia trazable de la primera materialización
de la decisión arquitectónica adoptada en ADR-0001.

La implementación de S4 conserva posteriormente las mismas fronteras
definidas por ADR-0001. El corte vertical se implementa dentro del módulo
`publicaciones` y no convierte los módulos en servicios distribuidos.
