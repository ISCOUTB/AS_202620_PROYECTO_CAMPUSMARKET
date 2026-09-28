# ADR-0007 - Desplegar FastAPI mediante Azure App Service

## Estado

Aceptado

## Fecha

2026-09-27

## Pieza decidida

**Backend API FastAPI de CampusMarket**

Esta decisión corresponde exclusivamente a la pieza Backend API.

No decide dónde se publica Flutter Web ni dónde se ejecuta MySQL.

---

## Contexto

El backend de CampusMarket está construido con FastAPI y Python 3.12.

La pieza requiere un proceso de servidor activo capaz de:

- recibir solicitudes HTTPS;
- ejecutar la lógica del corte vertical;
- acceder a MySQL;
- exponer `/health`;
- producir logs estructurados;
- exponer la métrica `/ops/metrics/ec01`;
- recibir configuración sensible desde el entorno;
- mantenerse accesible desde fuera de la universidad.

La decisión de despliegue no debe modificar la estructura interna:

```text
router
   ↓
service
   ↓
repository
   ↓
MySQL
```

Restricciones relacionadas:

- R-08 - despliegue público y verificable;
- R-09 - protección de secretos;
- R-10 - infraestructura como código;
- R-11 - límite de costo;
- R-12 - no dependencia de tarjeta bancaria personal.

---

## Alternativas consideradas

### Alternativa A - Azure App Service sobre Linux

Ejecutar FastAPI en Azure App Service utilizando Python 3.12 y Uvicorn.

Ventajas:

- URL pública HTTPS;
- soporte para configuración mediante App Settings;
- integración con Azure CLI;
- logs operativos consultables;
- compatible con FastAPI y Python;
- permite configurar la conexión TLS hacia MySQL;
- puede declararse mediante Bicep;
- dispone de nivel F1 utilizado durante el prototipo;
- permitió mantener la API separada del frontend y de la base de datos.

Desventajas:

- requiere administrar configuración cloud;
- el nivel F1 tiene capacidad limitada;
- puede requerir migración a un nivel de pago si aumenta la carga;
- requiere configurar CORS para GitHub Pages.

---

### Alternativa B - Ejecutar FastAPI en el servidor del laboratorio

Una alternativa académica sin tarjeta consiste en desplegar la API en un
servidor institucional disponible para el curso.

Ventajas:

- no exige una tarjeta bancaria personal;
- permite ejecutar un proceso Python persistente;
- evita depender de créditos personales de un proveedor cloud.

Desventajas:

- el equipo depende de la disponibilidad y configuración del recurso
  institucional;
- menor autonomía para crear o modificar recursos;
- configuración y operación más manual;
- el entorno utilizado durante S8 ya fue implementado y verificado en Azure;
- no produce la misma integración reproducible con el Bicep desarrollado para
  el entorno actual.

---

## Decisión

Se selecciona:

**Azure App Service sobre Linux**

para ejecutar la pieza Backend API FastAPI.

Aplicación:

```text
campusmarket-s8-api-nilver
```

URL:

`https://campusmarket-s8-api-nilver.azurewebsites.net`

Runtime:

```text
Python 3.12
```

Comando de inicio:

```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

---

## Infraestructura como código

La definición se encuentra en:

`infra/main.bicep`

La plantilla describe:

- App Service Plan;
- Web App;
- runtime;
- configuración de aplicación;
- parámetros de acceso a MySQL.

Fue verificada mediante:

```bash
az bicep build --file infra/main.bicep
```

y:

```bash
az deployment group validate
```

Resultado observado:

```text
provisioningState: Succeeded
error: null
```

---

## Capa gratuita y condición de tarjeta

El Backend API utiliza el nivel:

```text
F1
```

de Azure App Service.

Para el prototipo S8 se utilizó dentro de la suscripción académica disponible y
no fue necesario registrar una tarjeta bancaria personal para mantener la
evidencia utilizada por el equipo.

Estado utilizado durante S8:

```text
App Service Plan: F1
Carga: académica / baja
Instancias: 1
Alta disponibilidad dedicada: No
```

No se considera F1 una solución garantizada para una carga productiva futura.

---

## Punto de ruptura

La decisión debe reevaluarse y probablemente migrar a un nivel superior cuando:

- el nivel F1 deje de soportar la carga requerida;
- se necesite mayor capacidad de CPU o memoria;
- se necesite disponibilidad o escalado no cubierto por el nivel actual;
- se necesiten características operativas no ofrecidas por F1;
- el entorno deje de estar cubierto por las condiciones académicas aplicables.

Ese cambio debe realizarse sin alterar la interfaz HTTP definida por OpenAPI.

---

## Protección de secretos

Las credenciales MySQL no se almacenan en el código fuente.

La aplicación recibe configuración mediante:

- App Settings de Azure;
- variables de entorno.

Variables principales:

```text
CAMPUSMARKET_DB_HOST
CAMPUSMARKET_DB_PORT
CAMPUSMARKET_DB_USER
CAMPUSMARKET_DB_PASSWORD
CAMPUSMARKET_DB_NAME
CAMPUSMARKET_DB_SSL
```

La conexión a MySQL utiliza TLS en el entorno desplegado.

---

## Observabilidad

El Backend API expone:

```text
GET /health
```

Comportamiento verificado:

```text
MySQL disponible
→ HTTP 200

MySQL no disponible
→ HTTP 503

MySQL recuperado
→ HTTP 200
```

Las solicitudes HTTP generan logs estructurados con campos como:

```text
timestamp
level
event
request_id
method
path
status_code
duration_ms
```

También se expone:

```text
GET /ops/metrics/ec01
```

relacionado con EC-01.

---

## Verificación realizada

Durante S8 se verificó:

- URL pública accesible;
- HTTPS;
- ejecución FastAPI;
- conexión real con Azure MySQL;
- `/health` HTTP 200;
- degradación HTTP 503;
- recuperación HTTP 200;
- logs estructurados;
- métrica operacional EC-01;
- CORS desde GitHub Pages;
- `POST /publicaciones`;
- `GET /publicaciones`;
- pipeline de pruebas en verde.

---

## Despliegue reproducible

Desde un commit conocido:

```bash
git archive --format=zip \
  -o campusmarket-api.zip \
  <COMMIT>
```

Despliegue:

```bash
az webapp deploy \
  --resource-group rg-campusmarket-s8 \
  --name campusmarket-s8-api-nilver \
  --src-path campusmarket-api.zip \
  --type zip
```

Después deben verificarse:

```text
GET /health
GET /publicaciones
POST /publicaciones
GET /ops/metrics/ec01
```

---

## Rollback

Seleccionar un commit previamente validado:

```bash
git archive --format=zip \
  -o campusmarket-rollback.zip \
  <KNOWN_GOOD_SHA>
```

Redesplegar:

```bash
az webapp deploy \
  --resource-group rg-campusmarket-s8 \
  --name campusmarket-s8-api-nilver \
  --src-path campusmarket-rollback.zip \
  --type zip
```

Verificación posterior:

```text
/health → HTTP 200
GET /publicaciones → operativo
POST /publicaciones → operativo
```

---

## Consecuencias positivas

- API pública HTTPS;
- configuración separada del código;
- soporte de logs;
- health check verificable;
- métrica operacional;
- despliegue reproducible;
- infraestructura versionada mediante Bicep;
- mantiene intacta la arquitectura interna.

---

## Consecuencias negativas

- dependencia operativa de Azure;
- F1 tiene capacidad limitada;
- requiere controlar costos y créditos;
- requiere mantener reglas CORS;
- requiere mantener coherentes App Settings y Bicep.

---

## Relación con decisiones anteriores

ADR-0001 continúa vigente: FastAPI sigue siendo un monolito modular.

ADR-0003 continúa vigente: la integración cliente-API es síncrona mediante
HTTP/JSON y HTTPS en el entorno público.

ADR-0005 queda refinado por este ADR para la decisión específica del Backend
API.

---

## Evidencia relacionada

- `backend/app/`
- `backend/tests/`
- `.github/workflows/backend-tests.yml`
- `infra/main.bicep`
- `docs/arc42/07-vista-despliegue.md`
- `docs/evidencias/evidencia-s8-2026-09-27.md`
- `README.md`
