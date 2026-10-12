# Trazabilidad del escenario S10-CT-01

Complemento nuevo de [la tabla histórica de aspectos](aspectos.md). No sustituye sus filas.

| ID | Aspecto | Requisito | C4 | ADR | Código | Pruebas | Evidencia |
|---|---|---|---|---|---|---|---|
| S10-CT-01 | Compatibilidad del consumidor y observabilidad del rechazo | [Escenario, hipótesis y umbral](arc42/s10-adenda-operativa.md) | [Correspondencia L1/L2/L3](c4/04-escenario-s10-contrato.md) | [ADR-0020](adr/0020-preservar-contrato-v2-y-adaptar-consumidor-incompatible.md), confirma ADR-0003/0009 | [Contrato público](../contracts/openapi-v2.json), [router vigente](../backend/app/catalogo/router.py), [adaptador y observador](../scripts/experimento_s10_contrato.py) | [Rechazo, recuperación y logs](../backend/tests/test_s10_contrato_cliente.py), [contrato](../backend/tests/test_contrato_openapi.py), [workflow nuevo](../.github/workflows/s10-contrato-cliente.yml) | [Plan previo](evidencias/s10/ejecucion-20261012T0419Z/plan.json), [58 observaciones HTTP](evidencias/s10/ejecucion-20261012T0419Z/observaciones.jsonl), [resumen](evidencias/s10/ejecucion-20261012T0419Z/resumen.json), [matriz S10](evidencias/evidencia-s10-corte2-2026-10-11.md) |
