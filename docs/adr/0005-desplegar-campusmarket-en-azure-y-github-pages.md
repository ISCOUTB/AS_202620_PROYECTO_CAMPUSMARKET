# ADR-0005 - Desplegar CampusMarket con GitHub Pages y Microsoft Azure

## Estado

Aceptado

## Fecha

2026-09-27

## Contexto

Hasta S7 CampusMarket podía ejecutarse y verificarse principalmente desde un
entorno de desarrollo.

Durante S8 el proyecto requiere evolucionar hacia un entorno de despliegue
público, reproducible y observable, de forma que el corte vertical pueda ser
verificado sin depender exclusivamente del equipo local de desarrollo.

La arquitectura vigente antes de esta decisión ya establece:

- Flutter Web como frontend;
- FastAPI como Backend API;
- MySQL como tecnología de persistencia;
- integración síncrona mediante HTTP/JSON;
- monolito modular como estilo arquitectónico del backend;
- Gestión de Publicaciones como propietario de los datos de publicaciones.

La decisión de despliegue no debe modificar innecesariamente estas fronteras.

También se requiere mantener:

- acceso público al sistema;
- comunicación mediante HTTPS;
- health check verificable;
- protección de credenciales;
- infraestructura reproducible;
- posibilidad de rollback;
- observabilidad del backend;
- un costo adecuado para un prototipo académico.

## Problema

Un sistema que solamente funciona desde el equipo de desarrollo no permite
verificar de forma independiente sus características operativas.

Era necesario determinar dónde ejecutar cada pieza materializada de
CampusMarket:

- frontend Flutter Web;
- Backend API FastAPI;
- persistencia MySQL.

La solución debía permitir conservar la topología lógica:

```text
Flutter Web
    ↓
FastAPI
    ↓
MySQL
```

sin introducir una división innecesaria del monolito modular.

## Decisión

Se adopta la siguiente distribución para S8:

### Frontend

Flutter Web se publica mediante:

**GitHub Pages**

URL pública:

`https://nnigarp.github.io/AS_202620_PROYECTO_CAMPUSMARKET/`

La aplicación se compila para producción proporcionando la URL pública del
backend mediante:

`CAMPUSMARKET_API_BASE_URL`

### Backend

FastAPI se despliega mediante:

**Microsoft Azure App Service sobre Linux**

Aplicación:

`campusmarket-s8-api-nilver`

URL pública:

`https://campusmarket-s8-api-nilver.azurewebsites.net`

La ejecución utiliza Python 3.12 y Uvicorn.

### Persistencia

La persistencia se despliega mediante:

**Azure Database for MySQL Flexible Server**

La versión utilizada durante S8 corresponde a MySQL 8.4.

La base utilizada por el corte vertical es:

`campusmarket`

El acceso se realiza exclusivamente desde el backend mediante PyMySQL.

### Infraestructura como código

La infraestructura principal de Azure se describe mediante:

`infra/main.bicep`

La definición incluye los recursos necesarios para el Backend API y la
persistencia, utilizando parámetros para valores dependientes del entorno y un
parámetro seguro para la contraseña administrativa de MySQL.

## Topología resultante

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

Esta decisión modifica la infraestructura de ejecución, pero no cambia las
fronteras de dominio del backend.

La dirección interna continúa siendo:

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

## Justificación

### Separación de responsabilidades de despliegue

El frontend es un artefacto web estático una vez compilado.

Por esta razón puede publicarse independientemente del Backend API mediante
GitHub Pages.

FastAPI requiere un proceso de servidor en ejecución, por lo que se despliega
en Azure App Service.

MySQL requiere persistencia administrada y acceso desde el backend, por lo que
se utiliza Azure Database for MySQL Flexible Server.

Esta distribución permite seleccionar un mecanismo de despliegue adecuado para
cada tipo de componente sin modificar la arquitectura lógica del sistema.

### Reproducibilidad

La infraestructura principal utilizada en Azure está versionada mediante
Bicep.

La plantilla fue compilada y validada satisfactoriamente durante S8.

El backend también puede reconstruirse desde un commit conocido mediante
`git archive` y desplegarse nuevamente con Azure CLI.

El frontend puede reconstruirse desde el código Flutter y volver a publicarse
en `gh-pages`.

### Seguridad

Las credenciales reales de la base de datos no se almacenan en el repositorio.

La configuración sensible se proporciona mediante:

- parámetros seguros de Bicep;
- App Settings;
- variables de entorno.

La comunicación pública utiliza HTTPS y la conexión entre backend y MySQL
utiliza TLS.

### Observabilidad

El backend dispone de:

`GET /health`

y de logs estructurados para solicitudes HTTP.

También dispone de:

`GET /ops/metrics/ec01`

como mecanismo de consulta de información operacional asociada a EC-01.

## Alternativas consideradas

### Alternativa 1 - Mantener todo únicamente en entorno local

No se adopta.

Ventajas:

- menor complejidad operativa;
- no requiere recursos cloud;
- facilita el desarrollo inicial.

Desventajas:

- no produce una URL pública;
- depende del equipo del desarrollador;
- dificulta la verificación independiente;
- no demuestra una arquitectura de despliegue real.

Esta alternativa deja de ser suficiente para S8.

### Alternativa 2 - Servir frontend y backend desde un único App Service

No se adopta para el despliegue S8.

Era posible incorporar el build estático de Flutter dentro del mismo entorno
que ejecuta FastAPI.

Ventajas:

- una única URL principal;
- menor cantidad de destinos de despliegue.

Desventajas:

- mezcla la publicación de un frontend estático con el ciclo operativo del
  Backend API;
- obliga a redesplegar el backend ante cambios exclusivamente visuales;
- incrementa el acoplamiento operativo entre dos artefactos que pueden
  publicarse independientemente.

### Alternativa 3 - GitHub Pages + Azure App Service + Azure MySQL

Se adopta.

Ventajas:

- cada pieza utiliza un mecanismo apropiado para su naturaleza;
- frontend y backend pueden desplegarse independientemente;
- se obtiene una URL pública;
- la persistencia utiliza un servicio MySQL administrado;
- permite health checks y logs del backend;
- mantiene las fronteras del monolito modular;
- permite versionar la infraestructura Azure mediante Bicep.

Desventajas:

- existen varios recursos operativos que deben coordinarse;
- se requiere configurar CORS entre GitHub Pages y Azure App Service;
- la base de datos representa el principal componente con costo potencial;
- la operación es más compleja que un entorno exclusivamente local.

## Consecuencias positivas

- CampusMarket queda accesible públicamente.
- El corte vertical puede probarse fuera del equipo de desarrollo.
- El frontend puede desplegarse independientemente.
- El Backend API dispone de health check.
- MySQL se ejecuta como servicio administrado.
- La comunicación pública utiliza HTTPS.
- La infraestructura Azure queda versionada.
- Los secretos reales permanecen fuera del repositorio.
- El backend produce logs estructurados.
- Se dispone de un procedimiento de rollback.

## Consecuencias negativas

- El despliegue requiere coordinar GitHub Pages, Azure App Service y MySQL.
- CORS debe configurarse correctamente entre frontend y backend.
- El entorno cloud requiere controlar consumo y costos.
- La persistencia administrada introduce mayor complejidad operativa que una
  base local.
- Los cambios de configuración cloud deben mantenerse coherentes con la
  documentación y la infraestructura versionada.

## Verificación realizada

Durante S8 se verificó:

- frontend accesible desde GitHub Pages;
- Backend API accesible desde Azure;
- `GET /health` con HTTP 200 y MySQL disponible;
- HTTP 503 ante indisponibilidad controlada de MySQL;
- recuperación posterior a HTTP 200;
- CORS desde el origen público de GitHub Pages;
- creación real de una publicación desde Flutter Web;
- persistencia real en MySQL;
- consulta posterior de publicaciones;
- logs estructurados;
- métrica operacional de EC-01;
- pipeline del backend en verde;
- despliegue de GitHub Pages en verde;
- compilación satisfactoria de Bicep;
- validación satisfactoria de la plantilla de infraestructura.

## Rollback

El backend puede regresar a una versión conocida generando un paquete desde un
commit previamente validado:

```text
git archive --format=zip -o campusmarket-rollback.zip <KNOWN_GOOD_SHA>
```

y desplegándolo nuevamente mediante:

```text
az webapp deploy \
  --resource-group rg-campusmarket-s8 \
  --name campusmarket-s8-api-nilver \
  --src-path campusmarket-rollback.zip \
  --type zip
```

Después del rollback deben volver a comprobarse:

- `/health`;
- `GET /publicaciones`;
- creación de una publicación.

Para el frontend, el rollback consiste en republicar en `gh-pages` un
`build/web` correspondiente a una versión previamente validada.

## Relación con decisiones anteriores

### ADR-0001 - Monolito modular

Continúa vigente.

El despliegue no convierte los contextos de negocio en microservicios.

### ADR-0002 - Manejo de bloqueo temporal de SQLite

Se mantiene como decisión histórica correspondiente al primer corte.

No describe la persistencia vigente de S8.

### ADR-0003 - Integración síncrona HTTP/JSON

Continúa vigente conceptualmente.

En el entorno público la comunicación se realiza mediante HTTPS/JSON.

### ADR-0004 - Migrar la persistencia de SQLite a MySQL

Continúa vigente.

ADR-0005 define dónde se ejecuta la instancia MySQL utilizada por el entorno
público, sin modificar la decisión de encapsular la persistencia detrás del
Repository.

## Documentación relacionada

- `docs/arc42/07-vista-despliegue.md`
- `docs/arc42/02-restricciones.md`
- `docs/arc42/ARC42.md`
- `infra/main.bicep`
