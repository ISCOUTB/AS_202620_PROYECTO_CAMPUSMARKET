# C4 - Correspondencia del escenario S10-CT-01

No cambia la topología de [C4 L1](01-contexto.md), [C4 L2](02-contenedores.md) ni las fronteras de [C4 L3](03-componentes-backend.md). Este archivo añade el mapeo del estímulo nuevo sin reescribir esos modelos.

| Elemento existente | Participación en el reto | Trazabilidad |
|---|---|---|
| Consumidor HTTP de API | Simula cliente nuevo con sale; adapta a venta | [Script S10](../../scripts/experimento_s10_contrato.py), no es un nuevo contenedor de producción |
| API FastAPI | Valida modalidad, responde 422, emite request ID y log estructurado | [Router](../../backend/app/catalogo/router.py), [errores seguros](../../backend/app/main.py), [observabilidad](../../backend/app/observability.py) |
| Catálogo | Solo recibe parámetros válidos; consulta Publicaciones | [Service](../../backend/app/catalogo/service.py) |
| Publicaciones y MySQL | Conservan lectura y datos públicos existentes | [Service](../../backend/app/publicaciones/service.py), [snapshot de la corrida](../evidencias/s10/ejecucion-20261012T0419Z/resumen.json) |
| Frontend Flutter Web | Sigue consumiendo el contrato v2; no se modifica en S10 | [Fuente existente](../../frontend/campusmarket/lib/), [OpenAPI](../../contracts/openapi-v2.json) |

El rechazo se produce antes del servicio en las pruebas locales. Sobre producción se comprueban código 422, error de modalidad, health 200 y respuesta corregida 200; no se afirma inspección de SQL de producción.

[ADR-0020](../adr/0020-preservar-contrato-v2-y-adaptar-consumidor-incompatible.md) conserva decisiones previas. [Adenda arc42](../arc42/s10-adenda-operativa.md) describe ejecución, despliegue y calidad. [Evidencia S10](../evidencias/evidencia-s10-corte2-2026-10-11.md) permite navegar de la decisión a mediciones y pruebas.
