# Evidencia S8 - Despliegue y operación

## CampusMarket

**Semana:** S8 - Despliegue y operación  
**Fecha de cierre:** 2026-09-27

Esta evidencia documenta únicamente resultados ejecutados y verificables del
entorno utilizado durante S8.

---

## 1. Sistema público

### Frontend

Tecnología:

**Flutter Web**

Hosting:

**GitHub Pages**

URL pública:

`https://nnigarp.github.io/AS_202620_PROYECTO_CAMPUSMARKET/`

La interfaz pública identifica la arquitectura vigente como:

`CampusMarket S8: Flutter Web → FastAPI → MySQL en Azure.`

---

### Backend

Tecnología:

**FastAPI / Python 3.12**

Plataforma:

**Azure App Service**

URL:

`https://campusmarket-s8-api-nilver.azurewebsites.net`

---

### Health check

Endpoint:

`https://campusmarket-s8-api-nilver.azurewebsites.net/health`

Resultado verificado con la persistencia disponible:

```json
{
  "status": "ok",
  "service": "campusmarket-api"
}
```

Código HTTP:

`200`

También se verificó el comportamiento con MySQL no disponible:

`HTTP 503`

y la recuperación posterior al restablecer la persistencia:

`HTTP 200`

---

## 2. Topología desplegada

```text
Usuario
   |
   | HTTPS
   v
GitHub Pages
Flutter Web
   |
   | HTTPS / JSON
   v
Azure App Service
FastAPI
   |
   | TLS / SQL
   v
Azure Database for MySQL
Flexible Server
```

La arquitectura desplegada mantiene las fronteras lógicas definidas previamente.

El frontend no accede directamente a MySQL.

La dirección interna del backend continúa siendo:

```text
router
   ↓
service
   ↓
repository
   ↓
PyMySQL
   ↓
MySQL
```

---

## 3. Prueba funcional extremo a extremo

Desde la aplicación pública desplegada mediante GitHub Pages se realizó una
creación real de publicación.

La interfaz mostró:

`Publicación #2 guardada correctamente.`

Esto verifica el recorrido:

```text
Flutter Web público
       ↓
CORS
       ↓
FastAPI en Azure
       ↓
Service
       ↓
Repository
       ↓
PyMySQL
       ↓
MySQL en Azure
```

La información almacenada también pudo recuperarse mediante:

`GET /publicaciones`

Por lo tanto, la prueba no se limita a comprobar que la página carga: atraviesa
los componentes materializados del corte vertical.

---

## 4. CORS

El Backend API permite explícitamente el origen del frontend público:

`https://nnigarp.github.io`

La solicitud preflight realizada contra:

`OPTIONS /publicaciones`

respondió correctamente y permitió el origen público del frontend.

Esto permitió realizar posteriormente el `POST /publicaciones` desde Flutter Web.

---

## 5. Infraestructura como código

La infraestructura principal utilizada en Azure se encuentra versionada en:

`infra/main.bicep`

La plantilla declara recursos asociados con:

- Azure App Service Plan;
- Azure Web App;
- Azure Database for MySQL Flexible Server;
- base de datos `campusmarket`;
- configuración del Backend API;
- reglas necesarias para el acceso a la persistencia;
- parámetros dependientes del entorno.

### Compilación

Se ejecutó:

```text
az bicep build --file main.bicep
```

Resultado:

`BICEP_BUILD_OK`

### Validación

Se ejecutó `az deployment group validate`.

Resultado observado:

```text
provisioningState: Succeeded
error: null
```

Por tanto, la definición de infraestructura utilizada en S8 fue validada antes
del cierre de la evidencia.

---

## 6. Protección de secretos

Las credenciales reales de MySQL no se encuentran almacenadas directamente en
el repositorio.

La configuración sensible se proporciona mediante:

- parámetros seguros de Bicep;
- App Settings de Azure;
- variables de entorno.

La contraseña administrativa de MySQL se recibe en Bicep mediante un parámetro
marcado como seguro.

El repositorio conserva además `.env` fuera del control de versiones mediante
`.gitignore`.

No se incluye ninguna contraseña real en esta evidencia.

---

## 7. Observabilidad

### Logs estructurados

El Backend API genera logs estructurados para las solicitudes HTTP.

Entre los campos observados se encuentran:

- `timestamp`;
- `level`;
- `event`;
- `request_id`;
- `method`;
- `path`;
- `status_code`;
- `duration_ms`.

Los logs fueron observados durante la ejecución real de Azure App Service.

Esto permite relacionar una solicitud con su resultado y duración sin depender
únicamente de mensajes de consola informales.

---

## 8. Métrica operacional asociada a EC-01

Endpoint:

`GET /ops/metrics/ec01`

Se generó tráfico controlado mediante solicitudes reales al backend.

Resultado observado:

- solicitudes registradas: `10`;
- solicitudes dentro del objetivo de 2000 ms: `10`;
- máximo observado: aproximadamente `164.41 ms`;
- mínimo observado: aproximadamente `137.75 ms`;
- objetivo del backend: cumplido en la muestra.

El endpoint indicó:

`meets_backend_target: true`

La evidencia debe interpretarse correctamente:

esta medición verifica el comportamiento del **backend** y funciona como proxy
operacional de EC-01.

No se presenta como una medición completa del tiempo percibido por el usuario
desde la interfaz Flutter.

---

## 9. Integración continua

El workflow:

`.github/workflows/backend-tests.yml`

ejecuta verificaciones automáticas del backend.

Entre ellas:

- análisis estático mediante Ruff;
- servicio MySQL 8.4 para pruebas;
- pruebas automatizadas mediante pytest;
- comprobación del contrato OpenAPI.

Los cambios de S8 han producido ejecuciones exitosas del workflow en la rama
de trabajo.

Antes de entregar S8, el mismo conjunto de cambios deberá estar integrado en
`master` y verificarse nuevamente mediante una ejecución exitosa del pipeline
sobre la rama principal.

---

## 10. Publicación del frontend

Flutter Web se construyó para producción mediante:

```text
flutter build web --release \
  --dart-define=CAMPUSMARKET_API_BASE_URL=https://campusmarket-s8-api-nilver.azurewebsites.net \
  --base-href "/AS_202620_PROYECTO_CAMPUSMARKET/"
```

Antes del build se verificó:

`flutter analyze`

sin errores.

El artefacto generado se publicó mediante la rama:

`gh-pages`

El workflow de GitHub Pages finalizó correctamente y el sitio fue probado desde
un navegador.

---

## 11. Estimación de costo

La arquitectura utilizada durante S8 separa los costos por componente.

### GitHub Pages

Para el repositorio público utilizado por el proyecto, la publicación del
frontend no generó un costo adicional observado para el equipo durante S8.

### Azure App Service

El Backend API utiliza un App Service Plan de nivel:

`F1`

seleccionado para mantener el costo del prototipo al mínimo.

### Azure Database for MySQL

La persistencia utiliza:

`Standard_B1ms`

con:

- 1 vCore;
- 2 GiB de memoria;
- 32 GiB de almacenamiento;
- alta disponibilidad deshabilitada.

Durante la configuración se observó en Azure una estimación aproximada de:

`USD 14.71 / mes`

para el componente MySQL antes de aplicar créditos o beneficios disponibles en
la suscripción académica.

Esta cifra se registra como **estimación observada**, no como factura efectiva.

### Punto de ruptura de costo

El prototipo deja de poder considerarse esencialmente sin costo para el equipo
cuando ocurre alguno de los siguientes casos:

- se agotan los créditos o beneficios disponibles en la suscripción académica;
- se requiere abandonar el nivel gratuito F1 del App Service;
- aumenta la capacidad contratada de MySQL;
- aumenta el almacenamiento;
- se habilita alta disponibilidad;
- se agregan nuevos recursos Azure con cobro.

El principal costo potencial del entorno actual es la persistencia administrada
MySQL.

Por esta razón, el costo debe reevaluarse antes de considerar este despliegue
como una configuración permanente de producción.

---

## 12. Rollback

### Backend

El backend puede regresar a un commit previamente validado mediante:

```text
git archive --format=zip \
  -o campusmarket-rollback.zip \
  <KNOWN_GOOD_SHA>
```

seguido de:

```text
az webapp deploy \
  --resource-group rg-campusmarket-s8 \
  --name campusmarket-s8-api-nilver \
  --src-path campusmarket-rollback.zip \
  --type zip
```

Después del rollback deben verificarse:

- `/health`;
- `GET /publicaciones`;
- creación de una publicación desde el frontend.

### Frontend

El frontend puede regresar a una versión previamente validada reconstruyendo el
`build/web` correspondiente y publicándolo nuevamente en:

`gh-pages`

---

## 13. Documentación arquitectónica relacionada

La evidencia S8 se encuentra relacionada con:

- `docs/arc42/02-restricciones.md`;
- `docs/arc42/07-vista-despliegue.md`;
- `docs/arc42/ARC42.md`;
- `docs/adr/0005-desplegar-campusmarket-en-azure-y-github-pages.md`;
- `infra/main.bicep`;
- `.github/workflows/backend-tests.yml`.

---

## 14. Estado antes de la entrega

Verificado durante S8:

- [x] frontend accesible públicamente;
- [x] backend accesible públicamente;
- [x] MySQL funcionando en Azure;
- [x] HTTPS;
- [x] CORS funcional;
- [x] `/health` HTTP 200;
- [x] degradación HTTP 503 sin persistencia;
- [x] recuperación HTTP 200;
- [x] publicación creada desde la web pública;
- [x] persistencia real en MySQL;
- [x] logs estructurados;
- [x] métrica operacional consultable;
- [x] infraestructura versionada mediante Bicep;
- [x] Bicep compilado;
- [x] Bicep validado;
- [x] secretos fuera del repositorio;
- [x] rollback documentado;
- [x] estimación de costo documentada;
- [x] vista de despliegue arc42 actualizada;
- [x] restricciones operativas actualizadas;
- [x] ADR de despliegue documentado;
- [ ] integrar S8 en `master`;
- [ ] comprobar pipeline verde sobre el commit final de `master`.

Los dos elementos pendientes deben cerrarse antes de entregar el hash definitivo
en la plataforma del curso.
