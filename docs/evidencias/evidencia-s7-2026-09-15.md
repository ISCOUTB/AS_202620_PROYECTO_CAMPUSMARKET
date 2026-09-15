# Evidencia S7 - Contrato de API y prueba de contrato

**Periodo:** 14-20/09/2026

**Proyecto:** CampusMarket

**Rama de trabajo:** `S7-interfaces-contratos`

## Resultado

CampusMarket formaliza como API principal la integración síncrona entre el
Frontend Flutter y el Backend FastAPI. El contrato OpenAPI `1.0.0` describe las
tres operaciones existentes y sus esquemas; la prueba compara el contrato con
el proveedor y se ejecuta como paso explícito del pipeline.

## Matriz de cumplimiento S7

| Criterio | Estado | Evidencia |
|---|---|---|
| Contrato ejecutable versionado | Cumple | `contracts/openapi-v1.json`: OpenAPI `3.1.0`, API `1.0.0` |
| Rutas y esquemas de datos | Cumple | `GET /health`, `GET /publicaciones`, `POST /publicaciones`; `HealthResponse`, `PublicacionCreate`, `Publicacion`, `ErrorResponse` |
| Correspondencia contrato-API | Cumple | `backend/app/main.py`, `backend/app/publicaciones/router.py` y `backend/tests/test_contrato_openapi.py` |
| Versión declarada e historial | Cumple al consolidar la rama | `info.version: 1.0.0`; el historial quedará en el commit/PR S7 |
| Prueba de contrato | Cumple | `backend/tests/test_contrato_openapi.py` |
| Pipeline ejecuta la prueba | Cumple | paso `Ejecutar prueba de contrato OpenAPI` en `.github/workflows/backend-tests.yml` |
| Falla ante cambio incompatible | Cumple | `docs/evidencias/fallo-contrato-s7-2026-09-15.md`: `titulo` → `nombre`, exit code `1` |
| ADR síncrono/asíncrono | Cumple | `docs/adr/0003-usar-integracion-sincrona-http-json.md`, ligado a EC-06 y EC-05 |
| arc42 sección 6 | Cumple | flujos de creación, consulta e indisponibilidad en `docs/arc42/06-vista-ejecucion.md` |
| C4 nivel 2 etiquetado | Cumple | protocolo y formato en cada flecha de `docs/c4/02-contenedores.puml` |

**Resultado local:** `11 passed`.

**Demostración incompatible:** `1 failed, 2 passed`, exit code `1`.

**Cliente generado:** OpenAPI Generator `7.25.0`, generador Dart, operaciones
`crearPublicacion`, `listarPublicaciones` y `consultarSalud`.

**Configuración pendiente del repositorio:** `master` no tiene actualmente
protección activa. El pipeline detecta y muestra el fallo, pero el equipo debe
marcar el check `Pruebas del backend / test` como requerido para impedir una
fusión manual mientras esté en rojo.

## Decisión y trade-off

Se mantiene la integración síncrona porque crear y consultar publicaciones
requiere respuesta inmediata. Se acepta el acoplamiento temporal y se hace
visible mediante códigos HTTP y manejo de indisponibilidad. La alternativa
asíncrona se descarta en este alcance porque exige estados pendientes,
reintentos, idempotencia, consistencia eventual y nueva infraestructura sin una
necesidad demostrada.

## Cadena de trazabilidad

**ASP-07 → EC-06 → C4 Nivel 2 → ADR-0003 → OpenAPI 1.0.0 → FastAPI/Flutter → prueba de contrato → pipeline → evidencia de fallo controlado**
