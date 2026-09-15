# Contrato HTTP de CampusMarket

`openapi-v1.json` es la fuente de verdad ejecutable de la API pública vigente.
Describe las operaciones implementadas por FastAPI:

- `GET /health`;
- `GET /publicaciones`;
- `POST /publicaciones`.

## Verificación

Desde la raíz del repositorio:

```bash
python -m pytest backend/tests/test_contrato_openapi.py -q
```

La prueba compara el documento versionado con el esquema expuesto por el
proveedor. Si se elimina o renombra una ruta, operación, campo o respuesta sin
evolucionar el contrato, la comparación falla.

## Generación de cliente

El contrato contiene `operationId` estables y se comprobó generando un cliente
Dart con OpenAPI Generator 7.25.0:

```bash
npx --yes @openapitools/openapi-generator-cli@2.25.2 generate \
  -i contracts/openapi-v1.json \
  -g dart \
  -o tmp/s7-client \
  --additional-properties=pubName=campusmarket_api_client,pubVersion=1.0.0
```

El resultado se mantiene como artefacto reproducible del laboratorio y no se
incorpora al producto mientras el frontend continúe utilizando su cliente
manual mínimo `publicaciones_api.dart`; mantener ambos clientes productivos
crearía duplicación sin beneficio en el corte actual.

## Regla de evolución

1. Proponer primero el cambio en este contrato.
2. Clasificarlo como compatible o incompatible.
3. Actualizar proveedor y consumidor en el mismo PR o planificar coexistencia.
4. Ejecutar la prueba de contrato antes de fusionar.
5. Para cambios incompatibles, publicar una nueva versión mayor y no sustituir
   silenciosamente la versión consumida.
