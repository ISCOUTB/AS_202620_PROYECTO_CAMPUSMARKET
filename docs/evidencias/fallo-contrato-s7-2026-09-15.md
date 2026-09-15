# Evidencia S7 - La prueba detecta un cambio incompatible

**Fecha:** 2026-09-15

**Contrato:** `contracts/openapi-v1.json`, OpenAPI `3.1.0`, API `1.0.0`

**Prueba:** `backend/tests/test_contrato_openapi.py`

**Cambio controlado:** renombrar `titulo` como `nombre` en el esquema del
proveedor sin modificar el contrato.

## Propósito

Comprobar que la prueba de contrato no pasa siempre y que detiene un cambio del
proveedor que rompería al consumidor Flutter, el cual todavía envía y lee el
campo `titulo`.

## Procedimiento

1. Se verificó el contrato vigente en verde.
2. Se cambió temporalmente en `PublicacionCreate`:

   ```diff
   - titulo: str = Field(min_length=3, max_length=100)
   + nombre: str = Field(min_length=3, max_length=100)
   ```

3. Se ejecutó:

   ```bash
   python -m pytest backend/tests/test_contrato_openapi.py -q
   ```

4. Se restauró `titulo` y se volvió a ejecutar el conjunto completo.

## Resultado del cambio incompatible

```text
.F [100%]
FAILED test_proveedor_fastapi_cumple_el_contrato_versionado

AssertionError: La API implementada ya no coincide con
contracts/openapi-v1.json. Un cambio del proveedor modificó rutas,
operaciones o esquemas sin evolucionar primero el contrato.

Differing items:
provider required: nombre, descripcion, precio, modalidad, estado, id
contract required: titulo, descripcion, precio, modalidad, estado, id

1 failed, 2 passed
exit code: 1
```

## Resultado después de restaurar la compatibilidad

```text
11 passed
exit code: 0
```

## Interpretación

La prueba detectó el cambio incompatible antes de fusionarlo. El campo
`titulo` forma parte tanto del cuerpo `PublicacionCreate` como de la respuesta
`Publicacion`; renombrarlo únicamente en el proveedor rompe el contrato que
consume Flutter.

La mutación incompatible fue deliberada y temporal. No permanece en el código
final. El pipeline ejecuta la misma prueba en un paso explícito y deja el check
en rojo frente a futuros cambios no negociados. Para impedir además el botón de
fusión, el check debe configurarse como requerido en la protección de `master`.
