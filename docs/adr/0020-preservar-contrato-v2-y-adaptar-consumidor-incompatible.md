# ADR-0020 - Preservar el contrato v2 y adaptar el consumidor incompatible

- Estado: Aceptado para el experimento S10-CT-01; no modifica la API desplegada.
- Fecha: 2026-10-11 (America/Bogota).
- Relación: confirma, para este estímulo, la integración HTTP/JSON de [ADR-0003](0003-usar-integracion-sincrona-http-json.md) y el acceso a catálogo por el servicio de Publicaciones de [ADR-0009](0009-materializar-catalogo-sin-romper-fronteras.md). Mantiene [ADR-0018](0018-ejecutar-el-monolito-en-dokploy-con-volumenes.md). Ningún ADR anterior se reemplaza o reescribe.

## Contexto y estímulo operativo nuevo

Un nuevo consumidor utiliza la etiqueta inglesa `sale` en `GET /catalogo?modalidad=sale`, mientras [OpenAPI v2](../../contracts/openapi-v2.json) admite `venta` o `alquiler`. Es un escenario de incompatibilidad de contrato entre consumidor y proveedor. No se afirma que una versión histórica de CampusMarket admitiera `sale`, ni que la API cambiara en S10.

El equipo selecciona este escenario según la indicación oral que Nilver informa haber recibido del docente: elegir uno a partir del comportamiento del despliegue. El enunciado escrito, alcance y mediciones del equipo están en [la evidencia S10](../evidencias/evidencia-s10-corte2-2026-10-11.md). No se presenta EC-01/S9 como el nuevo reto.

## Alternativas viables

| Opción | Resultado | Costo y consecuencias |
|---|---|---|
| A. Admitir `sale` como alias en el proveedor | El nuevo consumidor funcionaría sin corregirse | Modificar esquema, router y pruebas; actualizar documentación y desplegar. Aumenta variantes que el contrato debe mantener. Es viable, pero no existe demanda de compatibilidad con un cliente ya publicado. |
| B. Mantener v2; traducir explícitamente `sale` a `venta` en el consumidor de prueba | El proveedor rechaza el dato incompatible con 422; la solicitud corregida vuelve a 200 | No agrega servicios, dependencias, secretos ni recursos. El consumidor asume la traducción. Usuarios y dominio siguen usando las mismas dos modalidades. |

## Decisión

Elegir B. El cambio S10 es un consumidor reproducible y su configuración de adaptación, no una nueva versión del proveedor. [adapt_sale_filter](../../scripts/experimento_s10_contrato.py) implementa la conversión explícita. Las tres fases usan el mismo origen HTTPS, API y contrato: línea base `venta`, estímulo `sale`, recuperación del consumidor por adaptación a `venta`.

Se conserva el rechazo estructurado de FastAPI: HTTP 422 identifica `query/modalidad` y `literal_error`; no hay valor inválido reflejado en `input`. No se devuelve un catálogo vacío o un 200 que esconda el fallo. Las pruebas nuevas comprueban que el dato incompatible no alcanza el servicio de Catálogo y que la petición corregida sí lo alcanza. La comprobación de ausencia de acceso al servicio es local; no se presenta como un contador SQL de producción.

## Verificación y criterio para no cambiar la arquitectura

La decisión se acepta contra el umbral declarado antes de la corrida en `plan.json`: 100 % de consultas válidas/adaptadas con 200, 100 % de incompatibles con 422, p95 público por fase <=10 s, health 200/ok y correlación de todas las peticiones. [Resultados y todas las muestras](../evidencias/s10/ejecucion-20261012T0419Z/) permiten contrastar la decisión. La cifra de 10 s es una cota del observador HTTP de este reto; no reemplaza EC-01 de 2 s ni acredita rendimiento extremo a extremo.

Mantener la arquitectura evita desplegar un alias innecesario cuando el consumidor de prueba resuelve la incompatibilidad y el contrato funciona según lo publicado. No implica que la opción A sea siempre peor: si aparecen clientes reales que necesiten el alias, se decidirá una evolución compatible con pruebas y otro ADR.

## Consecuencias y límites

- La recuperación corresponde al consumidor; no demuestra recuperación de MySQL ni reinicio de API.
- Rechazo, salud, correlación y latencias se miden sobre el despliegue real. Los logs de servidor se verifican con pruebas locales del mismo código; no se afirma haber extraído logs privados de Dokploy.
- No se agregan endpoints operativos. Las métricas S10 son del observador externo y se conservan en JSON; la ventana `/ops/metrics/ec01` mantiene su alcance S9.
- La prueba es serial, con una publicación visible en el catálogo observado; no demuestra saturación, gran volumen, consumo de memoria ni todos los flujos del marketplace.
- Se conservan las deudas históricas de Sonar en CI y modificaciones antiguas de ADR, documentadas en [arc42 11](../arc42/11-riesgos-y-deuda-tecnica.md).

## Trazabilidad

S10-CT-01 -> [adenda arc42](../arc42/s10-adenda-operativa.md) -> [C4 del escenario](../c4/04-escenario-s10-contrato.md) -> ADR-0020 -> [router vigente](../../backend/app/catalogo/router.py), [adaptador/observador](../../scripts/experimento_s10_contrato.py) -> [pruebas S10](../../backend/tests/test_s10_contrato_cliente.py), [contrato](../../backend/tests/test_contrato_openapi.py) -> [mediciones nuevas](../evidencias/s10/ejecucion-20261012T0419Z/) -> [pipeline S10](../../.github/workflows/s10-contrato-cliente.yml).
