# Evidencia S7 - Contrato de API y prueba de contrato

**Periodo:** 14-20/09/2026

**Proyecto:** CampusMarket

**Estado:** Implementación integrada mediante los PR #37 y #38.

## Resultado

CampusMarket formaliza como API principal la integración síncrona entre el
Frontend Flutter y el Backend FastAPI.

El contrato OpenAPI `1.0.0` describe las tres operaciones implementadas, sus
cuerpos, respuestas y esquemas. La prueba automatizada compara el contrato
versionado con la superficie OpenAPI generada por FastAPI y se ejecuta en un
paso explícito del pipeline.

## Matriz de cumplimiento S7

| Criterio | Estado | Evidencia |
|---|---|---|
| Contrato ejecutable versionado | Cumple | `contracts/openapi-v1.json`: OpenAPI `3.1.0`, API `1.0.0` |
| Rutas y esquemas de datos | Cumple | `GET /health`, `GET /publicaciones`, `POST /publicaciones`; esquemas `HealthResponse`, `PublicacionCreate`, `Publicacion` y `ErrorResponse` |
| Correspondencia contrato-API | Cumple | `backend/app/main.py`, `backend/app/publicaciones/router.py` y comparación exacta en `backend/tests/test_contrato_openapi.py` |
| Versión declarada e historial | Cumple | `info.version: 1.0.0`; contrato incorporado mediante el PR #37 |
| Prueba de contrato presente | Cumple | `backend/tests/test_contrato_openapi.py` |
| Pipeline ejecuta la prueba | Cumple | Paso `Ejecutar prueba de contrato OpenAPI` en `.github/workflows/backend-tests.yml` y ejecución oficial #81 |
| Falla ante cambio incompatible | Cumple | Ejecución roja ante `crearPublicacion` → `registrarPublicacion` y comprobación local `titulo` → `nombre` |
| ADR ligado a un escenario | Cumple | `docs/adr/0003-usar-integracion-sincrona-http-json.md`, ligado a EC-06 y EC-05 |
| arc42 sección 6 | Cumple | Flujos de creación, consulta e indisponibilidad en `docs/arc42/06-vista-ejecucion.md` |
| C4 nivel 2 etiquetado | Cumple | Protocolo y formato en cada relación de `docs/c4/02-contenedores.puml` |

**Recuento:** 10 de 10 criterios cumplidos.

## Operaciones contratadas

| Método | Ruta | Operación | Respuestas |
|---|---|---|---|
| `GET` | `/health` | `consultarSalud` | `200 HealthResponse` |
| `GET` | `/publicaciones` | `listarPublicaciones` | `200 Publicacion[]` |
| `POST` | `/publicaciones` | `crearPublicacion` | `201 Publicacion`, `422 HTTPValidationError`, `503 ErrorResponse` |

## Verificaciones ejecutadas

### Estado compatible

Resultado local:

```text
11 passed, 2 warnings
exit code: 0
```

Ejecución verde del fork con las pruebas separadas:

https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/34935043273

Ejecución oficial correspondiente al PR #38:

https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/34935516952

### Cambio incompatible en GitHub Actions

Se cambió temporalmente:

```diff
- operation_id="crearPublicacion",
+ operation_id="registrarPublicacion",
```

Ejecución roja:

https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/34934077733

Resultado:

```text
FAILED test_proveedor_fastapi_cumple_el_contrato_versionado

Contrato: operationId = crearPublicacion
Proveedor: operationId = registrarPublicacion

1 failed, 10 passed, 2 warnings
Process completed with exit code 1.
```

### Cambio incompatible local complementario

También se cambió temporalmente:

```diff
- titulo: str = Field(min_length=3, max_length=100)
+ nombre: str = Field(min_length=3, max_length=100)
```

Resultado:

```text
FAILED test_proveedor_fastapi_cumple_el_contrato_versionado

1 failed, 2 passed
exit code: 1
```

Las dos mutaciones fueron restauradas y no permanecen en el código final.

La demostración completa está registrada en:

[`fallo-contrato-s7-2026-09-15.md`](./fallo-contrato-s7-2026-09-15.md)

## Cliente generado

OpenAPI Generator `7.25.0` generó de forma reproducible un cliente Dart con
`crearPublicacion`, `listarPublicaciones` y `consultarSalud`.

El procedimiento se encuentra en:

[`contracts/README.md`](../../contracts/README.md)

El cliente generado se utilizó como comprobación del laboratorio y no como
segundo cliente productivo, porque eso duplicaría la responsabilidad de
`publicaciones_api.dart`.

## Decisión y trade-off

Se mantiene la integración síncrona porque crear y consultar publicaciones
requiere respuesta inmediata.

Se acepta el acoplamiento temporal entre Flutter y FastAPI. Los modos de fallo
se expresan mediante HTTP `422`, HTTP `503` y errores de comunicación.

La alternativa asíncrona se descarta porque exigiría estados pendientes,
reintentos, idempotencia, tratamiento de duplicados, consistencia eventual y
nueva infraestructura sin una necesidad demostrada.

La decisión está registrada en:

[`ADR-0003`](../adr/0003-usar-integracion-sincrona-http-json.md)

## Calidad y análisis

El PR #38 obtuvo:

- pipeline oficial en verde;
- prueba de contrato ejecutada explícitamente;
- Quality Gate de SonarQube Cloud aprobado;
- cero problemas nuevos;
- cero puntos críticos de seguridad nuevos.

https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/pull/38

## Riesgo pendiente

La rama `master` todavía no tiene protección activa. El pipeline detecta los
fallos, pero GitHub permite una fusión manual mientras una ejecución está
pendiente o en rojo.

Se recomienda configurar `Pruebas del backend / test` como check obligatorio y
exigir al menos una revisión antes de fusionar.

## Cadena de trazabilidad

**ASP-07 → EC-06 → C4 Nivel 2 → ADR-0003 → OpenAPI 1.0.0 → FastAPI/Flutter → prueba de contrato → pipeline → fallo controlado → restauración verde**
