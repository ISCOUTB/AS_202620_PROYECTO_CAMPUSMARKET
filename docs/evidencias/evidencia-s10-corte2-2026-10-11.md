# Evidencia S10 - Segundo corte de CampusMarket

**Escenario operativo único S10-CT-01: un consumidor nuevo utiliza un valor incompatible con el contrato público del catálogo.** Familia: incompatibilidad/cambio de contrato del consumidor. El proveedor desplegado conserva OpenAPI v2.

## 1. Consigna, entrega y estado de partida

El equipo selecciona este escenario según la instrucción oral que Nilver García Pimentel informa haber recibido del docente: escoger uno según el comportamiento de su despliegue. Este documento identifica expresamente el escenario del segundo corte. No se afirma una asignación escrita localizada en el repositorio, ni se reutiliza EC-01/N+1 de S9 como experimento nuevo.

**PDF no entregado: no estaba habilitada su entrega, según informa el equipo.** Además, la [revisión preliminar docente de CampusMarket, del 6 de octubre](https://github.com/ISCOUTB/AS_202620_feedback/blob/master/revisiones/2026-2/AS_202620_PROYECTO_CAMPUSMARKET/semana-10-corte2.md) declara: "PDF excluido por instrucción docente" y conserva doce comprobaciones. Se presenta hipótesis, decisión, ejecución y resultado completos en Git. La exclusión no se extiende a otros requisitos.

Fuentes de requisitos: [ficha S10 del agente](https://github.com/ISCOUTB/AS_202620_feedback/blob/master/fichas/semana-10-corte2.md), [CONTRATO del curso](https://github.com/ISCOUTB/AS_202620_feedback/blob/master/CONTRATO.md) y revisión preliminar anterior. La rúbrica conserva cinco criterios y la sustentación corresponde al docente. No se propone una nota automática.

| Estado | Referencia verificable |
|---|---|
| Rama principal antes del trabajo | master |
| Base de este trabajo | de6ed67c05ccdb7eabd9b1951f146ab8958b1d00 |
| Revisión de API observada | 7856416795bb4accdf9d05e01adb470654875e56, en las 58 respuestas |
| API pública | https://campusmarket.iscoutb.dev |
| Frontend existente | https://nnigarp.github.io/AS_202620_PROYECTO_CAMPUSMARKET/ |
| Corrida nueva UTC | 2026-10-12 04:20:08 a 04:22:41 |
| Corrida nueva Colombia | 2026-10-11 23:20:08 a 23:22:41 |
| Cierre indicado por la revisión preliminar | 2026-10-12 05:00 UTC, 00:00 Colombia |

La ficha califica el último commit de master/main anterior al cierre, no una rama de trabajo ni un tag. El estado final de integración se registra en el [complemento de cierre](cierre-s10-corte2-2026-10-11.md); este documento conserva el hash base de la medición y no atribuye un hash documental a la API.

## 2. Caracterización, hipótesis y línea base

**Estímulo nuevo:** un integrador envía `GET /catalogo?modalidad=sale`. El enum publicado exige `venta` o `alquiler`. El rechazo puede confundirse con indisponibilidad si el consumidor no entiende el contrato.

**Hipótesis:** manteniendo el contrato v2, la API rechazará explícitamente el valor incompatible con 422, seguirá sana y devolverá el catálogo con 200 cuando el consumidor traduzca `sale` a `venta`; la corrección del consumidor será suficiente sin cambiar el proveedor ni la topología.

| Variable | Definición |
|---|---|
| Independiente | Modalidad enviada: venta -> sale -> venta mediante adaptación explícita |
| Dependientes | Código HTTP, detalle de validación, duración externa, salud, correlación y hash del catálogo público |
| Controladas | Mismo origen HTTPS, contrato v2, revisión API, método GET, filtro y consumidor serial; UUID por petición y no-cache |
| Montaje | Python 3.12/urllib desde entorno de trabajo, contra HTTPS público real; sin Docker local, credenciales ni mocks para la corrida pública |
| Carga | 3 repeticiones x 5 solicitudes por fase; 45 de catálogo filtrado, 9 de salud, 2 de contrato y 2 de catálogo completo = 58 |
| Línea base | Primera fase válida de cada repetición, medida en la corrida nueva; no se toma una cifra histórica S9 |

**Umbral prospectivo:** 100 % de peticiones baseline/adaptadas con 200; 100 % de incompatibles con 422 identificado como `query/modalidad`; p95 de cada fase <=10000 ms; health 200/ok; correlación 100 %; revisión constante y contrato público igual al versionado antes/después. Se observa también igualdad del snapshot público, con sus límites declarados.

El [plan.json](s10/ejecucion-20261012T0419Z/plan.json) se escribió **antes de la primera solicitud de la corrida** y fija carga y umbral. El p95 se calcula con nearest-rank sobre las quince muestras de cada fase, sin eliminar errores, escoger la mejor repetición o descontar red/TLS. Con n=15 el p95 coincide con el máximo. La cota de 10 s corresponde a este observador y no cambia EC-01 de 2 s.

## 3. Decisión e implementación de la respuesta

[ADR-0020](../adr/0020-preservar-contrato-v2-y-adaptar-consumidor-incompatible.md) compara admitir un alias en el proveedor con preservar v2 y corregir el consumidor. Se elige preservar el proveedor: no se acredita una demanda de clientes publicados que justifique ampliar el enum.

La respuesta S10 se materializa en `adapt_sale_filter` del [consumidor/observador nuevo](../../scripts/experimento_s10_contrato.py): traduce `sale` a `venta` antes de la tercera fase. No modifica Flutter, la API de producción, MySQL, las fronteras de dominio ni infraestructura. La ficha permite decidir no cambiar la arquitectura si se demuestra la decisión con evidencia.

Las [pruebas nuevas](../../backend/tests/test_s10_contrato_cliente.py) comprueban que la solicitud incompatible no invoca el servicio de Catálogo, que la adaptada recupera la lectura y que los tres códigos aparecen en logs JSON con sus IDs. Esto acredita la frontera en pruebas locales del código equivalente; no pretende ser una inspección de SQL de producción.

## 4. Ejecución y resultados reales

Todas las [observaciones JSONL](s10/ejecucion-20261012T0419Z/observaciones.jsonl) y el [resumen calculado](s10/ejecucion-20261012T0419Z/resumen.json) se conservan.

| Fase | Solicitud | Resultado real | p95 externo | Contraste |
|---|---|---|---:|---|
| Línea base | modalidad=venta | 15/15 HTTP 200; lista JSON | 4220.798 ms | 100 % y <=10000 ms |
| Incompatible | modalidad=sale | 15/15 HTTP 422; error de modalidad | 3209.699 ms | Rechazo explícito en 100 % |
| Adaptado | sale -> venta en consumidor | 15/15 HTTP 200; lista JSON | 5969.802 ms | Recuperación del consumidor en 100 % |
| Salud después de fases | GET /health | 9/9 HTTP 200 y status ok | No se usa para p95 de catálogo | Dependencia sana en esas comprobaciones |

- Correlación: 58/58 UUID recibidos iguales a los enviados.
- Errores de red: cero en las tres fases.
- Revisión: la misma 7856416795bb4accdf9d05e01adb470654875e56 en todas las respuestas.
- OpenAPI público antes/después: igualdad exacta con contracts/openapi-v2.json.
- Catálogo completo antes/después: una publicación visible y hash igual `e9b2e1e2cb758adc9250017310431768a1f95ed4d86519144e0f646b8ea21a30`.
- Resultado del evaluador: nueve comprobaciones verdaderas, `passed: true`.

**Conclusión:** en la muestra, la incompatibilidad del consumidor se diagnostica con 422 y se resuelve normalizando la solicitud, manteniendo el proveedor v2. No se requiere un nuevo despliegue para esta respuesta. La fase adaptada fue más lenta que la línea base; no se atribuye una mejora de rendimiento a la adaptación ni se oculta esa diferencia.

## 5. Observabilidad, seguridad y CI

La métrica específica S10 es del **observador externo**: ratio de códigos esperados por fase, p95 público, errores de red y ratio de correlación. Se exporta en resumen.json con escenario S10-CT-01. No se presenta la ventana EC-01 del servidor como si midiera este reto.

El emisor vigente [observability.py](../../backend/app/observability.py) produce logs JSON con timestamp, request_id, método, ruta, status_code y duration_ms. La API pública devuelve IDs reales; las pruebas capturan y verifican los registros de los tres estados. Los logs privados de Dokploy no se extraen en esta ejecución. Para sustentación se puede buscar cualquiera de los UUID en la consola autorizada de logs; no se incluye una captura como sustituto de la demo.

[Workflow S10 adicional](../../.github/workflows/s10-contrato-cliente.yml): pruebas de contrato/frontera/logs, repetición contra la API pública y artefactos, incluso si la medición falla. Usa permisos contents:read y no necesita secretos. Si cambia la revisión del proveedor o el contrato, el experimento falla en vez de ignorar la divergencia.

Validación local: `pytest backend/tests/test_s10_contrato_cliente.py backend/tests/test_contrato_openapi.py backend/tests/test_observability.py -q` -> **8 passed**. Ruff sobre backend y scripts -> sin hallazgos después de ordenar imports del archivo nuevo. Se conserva el script exacto de la primera corrida en [script-ejecutado.py](s10/ejecucion-20261012T0419Z/script-ejecutado.py), cuyo SHA256 coincide con plan.json; el script canónico solo recibió esa corrección de formato.

El pipeline existente [backend-tests.yml](../../.github/workflows/backend-tests.yml) mantiene su análisis y prueba completa; la [regla activa de master](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/rules/24001118) exige PR y estado `test` exitoso, sin bypass. Los runs finales se registran en el complemento de cierre. No se afirma que escribir un workflow equivalga a que haya pasado.

El [CI S10 38204357938](https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/38204357938) ejecutó ocho pruebas y repitió las 58 solicitudes públicas con success. Sus [muestras y resumen](s10/ci-38204357938/) se preservan separadamente de la primera corrida. El barrido redactado de secretos y sus resultados están en el [complemento de cierre](cierre-s10-corte2-2026-10-11.md). Sonar scanner/Quality Gate en CI permanece deuda; no se declara corregido por este experimento.

## 6. Trazabilidad y correspondencia con lo desplegado

| Eslabón | Evidencia |
|---|---|
| Aspecto y requisito | [Tabla S10 con ocho columnas](../aspectos-s10.md), sección 2 de esta evidencia |
| C4 | [Mapeo S10 sobre L1/L2/L3 vigentes](../c4/04-escenario-s10-contrato.md) |
| arc42 6/7/9/10 | [Adenda operativa](../arc42/s10-adenda-operativa.md) |
| arc42 11 | [Riesgos y deuda técnica](../arc42/11-riesgos-y-deuda-tecnica.md) |
| Decisión | [ADR-0020](../adr/0020-preservar-contrato-v2-y-adaptar-consumidor-incompatible.md), confirma ADR-0003/0009 |
| Implementación/configuración | [Adaptador consumidor](../../scripts/experimento_s10_contrato.py) y router vigente |
| Contrato | [OpenAPI v2](../../contracts/openapi-v2.json), idéntico al público antes/después |
| Prueba | [Regresión S10](../../backend/tests/test_s10_contrato_cliente.py), contrato y observabilidad |
| Medición | [Plan previo](s10/ejecucion-20261012T0419Z/plan.json), JSONL y resumen |
| CI e IA | [Workflow nuevo](../../.github/workflows/s10-contrato-cliente.yml), [registro IA canónico](../ia.md), [detalle S10](../ia-s10.md) |

Comprobación de equivalencia del proveedor, ejecutada con resultado vacío:

```bash
git diff 7856416795bb4accdf9d05e01adb470654875e56 de6ed67c05ccdb7eabd9b1951f146ab8958b1d00 -- backend/app backend/Dockerfile backend/requirements.txt contracts deploy
```

La ampliación añade archivos y solo agrega el registro S10 al final de docs/ia.md. El complemento de cierre verifica que todos los ADR previos, código de producto, contrato, despliegue y documentos anteriores conservan sus bytes.

## 7. Matriz de las doce comprobaciones S10

| Comprobación | Estado documentado | Evidencia y alcance |
|---|---|---|
| Estado final principal anterior al cierre | Integración oficial pendiente | Fork publicado y CI S10 verificado; no se confunde el fork con master oficial; estado en complemento de cierre |
| Despliegue accesible | Cumple en la corrida | 58 respuestas públicas; catálogo y health, hora/revisión por muestra |
| Hipótesis, montaje, variables y umbral | Cumple para S10-CT-01 | Sección 2 y plan prospectivo; selección según indicación oral informada por el equipo |
| Línea base medida y reproducible | Cumple | 15 solicitudes válidas nuevas, script y JSONL |
| Decisión registrada y coherente | Cumple en el alcance del reto | ADR-0020 y alternativas; no requiere cambio de proveedor |
| Respuesta implementada/configurada | Cumple | Adaptación explícita en consumidor de prueba; API preservada |
| Resultado contrastado con umbral | Cumple en la muestra | Resumen computado, todas las observaciones, límites declarados |
| Pipeline, health, logs y métrica | CI S10 verificado; deudas declaradas | Run success, health/correlación públicos, logs probados y métrica del observador; logs privados no extraídos y Sonar pendiente |
| Secretos protegidos | Verificado en el alcance del barrido | Checkout sin hallazgos; historial completo con cinco identificadores públicos clasificados y reportes redactados preservados |
| C4/arc42/ADR/contrato correspondientes | Cumple para la ampliación | Tabla anterior, código equivalente y contrato público idéntico |
| Decisión anterior confirmada o reemplazada | Cumple como confirmación acotada | ADR-0020 confirma HTTP/JSON y lectura por Publicaciones para este estímulo; no hay decisión reemplazada |
| Sustentación sobre despliegue y pipeline vivo | No verificado; lo califica el docente | Guion siguiente; no se asigna puntaje desde Git |

La exclusión de PDF está en sección 1. No se convierte la matriz en una nota ni se ocultan las deudas transversales.

## 8. Factores de confusión y límites de validez

Mismo origen, contrato, revisión, carga serial y solicitud controlan la comparación. UUID/no-cache reducen ambigüedad de correlación y caché. Red, DNS, TLS, proxy, carga ajena y orden de las fases no están aislados; los tiempos son externos. No se reintenta ni selecciona la mejor muestra. Las comprobaciones de health son puntuales y no garantizan disponibilidad entre ellas.

Una publicación visible no representa mil filas o carga concurrente. Hash público igual no prueba todas las tablas ni ausencia de cambios ajenos intermedios. No se mide CPU, memoria, consultas SQL productivas, navegador autenticado ni caída de MySQL. El adaptador pertenece al consumidor del experimento, no a un cliente externo que ya haya sido desplegado.

## 9. Reproducción y sustentación

Desde el repositorio, con Python 3.12 y acceso HTTPS:

```bash
python scripts/experimento_s10_contrato.py --output artifacts/s10/demo-corte2 --expected-revision 7856416795bb4accdf9d05e01adb470654875e56
```

El directorio debe ser nuevo: el script se niega a sobrescribir una corrida. Cada UUID y respuesta aparece en consola y JSONL. Repite 58 peticiones; si cambia la revisión o no alcanza el umbral, sale con código 1 y conserva resultados. Las salidas nuevas de demo no sustituyen las muestras de la corrida entregada.

Guion para la sesión: identificar consigna/hipótesis; abrir OpenAPI y mostrar modalidades; ejecutar baseline, consulta incompatible y adaptación en la URL pública; contrastar 422/200, health, IDs y resumen; abrir y ejecutar el workflow S10 en vivo; explicar ADR, alternativa y límites.

Tres preguntas preparadas:

1. Fallo: ¿cómo distinguimos un 422 del consumidor de una caída de MySQL y qué prueba acredita que la validación no alcanza el servicio?
2. Costo: ¿qué nos haría preferir un alias compatible en el proveedor y qué costo de contrato/despliegue tendría?
3. Medición: ¿por qué la fase adaptada tarda más que la base y qué evidencia falta para atribuir esa diferencia al backend?

La sustentación y aceptación docente del escenario siguen correspondiendo a la sesión.
