# Adenda arc42 S10 - Cliente incompatible con el contrato de catálogo

Esta adenda amplía el estado vigente sin reescribir las secciones históricas. Entrada: [evidencia S10](../evidencias/evidencia-s10-corte2-2026-10-11.md). Decisión: [ADR-0020](../adr/0020-preservar-contrato-v2-y-adaptar-consumidor-incompatible.md).

## 6. Vista de ejecución del escenario S10-CT-01

| Fase | Petición | Recorrido y respuesta |
|---|---|---|
| Línea base | GET /catalogo?modalidad=venta | FastAPI -> Catálogo -> servicio de Publicaciones -> MySQL; lista JSON / 200 |
| Consumidor incompatible | GET /catalogo?modalidad=sale | Validación de query por FastAPI -> error seguro 422; prueba local comprueba que no se invoca el servicio |
| Consumidor adaptado | El adaptador convierte sale -> venta | Mismo recorrido que la línea base; lista JSON / 200 |

El middleware produce `http_request` con `request_id`, ruta, código y duración. El observador envía un UUID y comprueba que el servidor lo devuelve en `X-Request-ID`. En producción se observa esa correlación; el contenido del log interno se valida separadamente mediante pruebas del código equivalente.

## 7. Vista de despliegue y correspondencia de revisión

No cambian nodos, contenedores, recursos ni contratos. El origen del experimento es `https://campusmarket.iscoutb.dev`. El frontend sigue en GitHub Pages; API y MySQL, en Dokploy, con los volúmenes y límites existentes de [la vista 7](07-vista-despliegue.md) y [C4 L2](../c4/02-contenedores.md).

Revisión del proveedor observada: `7856416795bb4accdf9d05e01adb470654875e56`. Base documental: `de6ed67c05ccdb7eabd9b1951f146ab8958b1d00`. El diff de `backend/app`, Dockerfile, requirements de producto, contracts y deploy entre ambas revisiones es vacío. No se atribuye la API a un commit documental posterior. Las corridas exigen esa revisión y el mismo OpenAPI antes/después; una diferencia falla el experimento.

## 9. Decisiones

ADR-0020 confirma integración HTTP/JSON y fronteras del catálogo bajo una incompatibilidad nueva. Decide mantener el proveedor v2 y adaptar el consumidor de prueba. Ningún ADR anterior queda superseded porque no se reemplaza una decisión arquitectónica.

## 10. Escenario de calidad y umbral prospectivo

- Fuente: un consumidor nuevo de la API pública.
- Estímulo: usar `sale` donde v2 admite `venta` o `alquiler`.
- Entorno: MVP público HTTPS, una secuencia serial, misma revisión y contrato.
- Artefacto: validación del catálogo y consumidor HTTP de prueba.
- Respuesta: rechazo explícito 422; después de corregir el consumidor, catálogo 200 y dependencia sana.
- Medida: 15/15 por fase (3 repeticiones x 5 muestras), p95 por fase <=10000 ms, health 200/ok y correlación 100 %. Se registran todas las muestras; no se recortan tiempos ni se reintentan fallos.

El [plan anterior a la corrida](../evidencias/s10/ejecucion-20261012T0419Z/plan.json), [observaciones](../evidencias/s10/ejecucion-20261012T0419Z/observaciones.jsonl) y [resumen calculado](../evidencias/s10/ejecucion-20261012T0419Z/resumen.json) distinguen requisito, ejecución y resultado. Este umbral acota la respuesta pública del reto y no modifica EC-01.

## 11. Riesgos y deuda

Véase [11-riesgos-y-deuda-tecnica.md](11-riesgos-y-deuda-tecnica.md). Incluye límites de validez, permisos de Dokploy y deudas transversales sin declararlas cerradas.
