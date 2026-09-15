# Evidencia S7 - La prueba detecta cambios incompatibles

**Fecha:** 2026-09-15

**Contrato:** `contracts/openapi-v1.json`, OpenAPI `3.1.0`, API `1.0.0`

**Prueba:** `backend/tests/test_contrato_openapi.py`

## Propósito

Comprobar que la prueba de contrato no pasa siempre, sino que detecta y detiene
cambios incompatibles del proveedor antes de que afecten al consumidor Flutter
o al cliente generado desde OpenAPI.

## Comprobación en GitHub Actions

### Cambio incompatible controlado

Se modificó temporalmente el identificador de la operación para crear
publicaciones:

```diff
- operation_id="crearPublicacion",
+ operation_id="registrarPublicacion",
```

El contrato versionado conservó `crearPublicacion`. Este cambio es incompatible
porque modifica el nombre del método que utiliza un cliente generado desde la
especificación OpenAPI.

### Procedimiento

1. Se ejecutó el pipeline con el contrato compatible y terminó en verde.
2. Se cambió temporalmente el `operationId` del proveedor FastAPI.
3. GitHub Actions ejecutó las pruebas y detectó la incompatibilidad.
4. Se restauró `operation_id="crearPublicacion"`.
5. El pipeline volvió a finalizar correctamente.

### Evidencias verificables

- Ejecución verde con la prueba de contrato explícita:
  https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/34933490103

- Ejecución roja ante el cambio incompatible:
  https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/34934077733

- Commit que introdujo temporalmente el cambio incompatible:
  https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/commit/043c7546a1ebe7a7077667b26c2092290689718e

- Commit que restauró la compatibilidad:
  https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/commit/013d92927ae154d07ea32de0134804c2e8ffaa27

### Resultado del cambio incompatible

```text
FAILED test_proveedor_fastapi_cumple_el_contrato_versionado

AssertionError: La API implementada ya no coincide con
contracts/openapi-v1.json. Un cambio del proveedor modificó rutas,
operaciones o esquemas sin evolucionar primero el contrato.

Contrato: operationId = crearPublicacion
Proveedor: operationId = registrarPublicacion

1 failed, 10 passed, 2 warnings
Process completed with exit code 1.
```

## Comprobación local complementaria

También se comprobó un cambio incompatible en el esquema de datos, renombrando
temporalmente `titulo` como `nombre` en el proveedor sin modificar el contrato:

```diff
- titulo: str = Field(min_length=3, max_length=100)
+ nombre: str = Field(min_length=3, max_length=100)
```

La prueba se ejecutó con:

```bash
python -m pytest backend/tests/test_contrato_openapi.py -q
```

Resultado:

```text
FAILED test_proveedor_fastapi_cumple_el_contrato_versionado

provider required: nombre, descripcion, precio, modalidad, estado, id
contract required: titulo, descripcion, precio, modalidad, estado, id

1 failed, 2 passed
exit code: 1
```

## Resultado final después de restaurar la compatibilidad

```text
11 passed
exit code: 0
```

## Interpretación

Las comprobaciones demuestran que la prueba detecta cambios incompatibles tanto
en las operaciones como en los esquemas de datos del proveedor.

La modificación del `operationId` habría cambiado la interfaz del cliente
generado. El cambio de `titulo` a `nombre` habría roto al consumidor Flutter,
que todavía envía y recibe el campo `titulo`.

Ambas mutaciones fueron deliberadas y temporales. No permanecen en el código
final. La mutación ejecutada en GitHub se realizó en el fork de evidencia y no
se fusionó al repositorio oficial.

El pipeline final ejecuta primero las pruebas funcionales y arquitectónicas y,
en un paso independiente, `backend/tests/test_contrato_openapi.py`. Esto permite
identificar claramente cuándo un cambio del proveedor rompe el contrato
versionado.

Para impedir también una fusión manual cuando las pruebas fallen, el check del
pipeline debe configurarse como requerido en la protección de la rama `master`.
