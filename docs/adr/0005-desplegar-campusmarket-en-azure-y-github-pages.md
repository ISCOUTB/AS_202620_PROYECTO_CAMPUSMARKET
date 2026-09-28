# ADR-0005 - Distribuir el despliegue de CampusMarket por pieza

## Estado

Aceptado y refinado por ADR-0006, ADR-0007 y ADR-0008

## Fecha

2026-09-27

## Nota de evolución

ADR-0005 registra la decisión general tomada durante S8 de desplegar las piezas
de CampusMarket de forma independiente según sus características operativas.

Para evitar tratar el sistema completo como una única decisión de plataforma,
esta decisión fue refinada posteriormente en tres ADR específicos:

- [ADR-0006 - Publicar Flutter Web mediante GitHub Pages](./0006-publicar-frontend-flutter-web-en-github-pages.md)
- [ADR-0007 - Desplegar FastAPI mediante Azure App Service](./0007-desplegar-api-fastapi-en-azure-app-service.md)
- [ADR-0008 - Desplegar MySQL mediante Azure Database for MySQL Flexible Server](./0008-desplegar-mysql-en-azure-flexible-server.md)

Por tanto:

```text
Frontend Flutter Web
→ ADR-0006

Backend API FastAPI
→ ADR-0007

Persistencia MySQL
→ ADR-0008
```

ADR-0005 se conserva como decisión arquitectónica global y como evidencia de la
evolución de S8, mientras que ADR-0006, ADR-0007 y ADR-0008 contienen la
comparación, costo, capa gratuita o beneficio aplicable, consecuencias y
rollback de cada plataforma concreta.

---

## Contexto

Hasta S7 CampusMarket podía ejecutarse y verificarse principalmente desde un
entorno de desarrollo.

Durante S8 el proyecto debía evolucionar hacia un entorno:

- público;
- reproducible;
- observable;
- verificable desde fuera de la red de la universidad;
- compatible con las restricciones de costo del prototipo;
- sin exponer secretos;
- con mecanismos de rollback.

La arquitectura lógica existente antes de esta decisión ya establece:

- Flutter Web como frontend;
- FastAPI como Backend API;
- MySQL como tecnología de persistencia;
- integración síncrona mediante HTTP/JSON;
- monolito modular como estilo arquitectónico del backend;
- Gestión de Publicaciones como propietario de los datos de publicaciones.

El despliegue no debía modificar innecesariamente estas fronteras.

---

## Problema

CampusMarket está compuesto por piezas con necesidades operativas diferentes.

El frontend Flutter Web se convierte en contenido estático después del build.

FastAPI requiere un proceso Python activo capaz de responder solicitudes HTTP.

MySQL requiere almacenamiento persistente y una conexión controlada desde el
backend.

Por tanto, la pregunta arquitectónica no es:

> ¿En qué plataforma se despliega todo CampusMarket?

sino:

> ¿Dónde debe ejecutarse cada pieza concreta de CampusMarket?

Las piezas materializadas en S8 son:

1. Frontend Flutter Web.
2. Backend API FastAPI.
3. Persistencia MySQL.

---

## Restricciones relevantes

La decisión debe respetar:

- despliegue accesible públicamente;
- HTTPS;
- health check verificable;
- logs estructurados;
- métrica operacional;
- protección de secretos;
- infraestructura reproducible;
- costo compatible con un prototipo académico;
- ausencia de dependencia de una tarjeta bancaria personal para demostrar el
  entorno académico;
- posibilidad de reversión;
- preservación del monolito modular.

Las restricciones completas se encuentran en:

[`docs/arc42/02-restricciones.md`](../arc42/02-restricciones.md)

En particular:

- R-08 - despliegue público, reproducible y verificable;
- R-09 - protección de secretos;
- R-10 - infraestructura como código;
- R-11 - límite de costo operativo;
- R-12 - no dependencia de tarjeta bancaria personal.

---

## Alternativas globales consideradas

### Alternativa A - Ejecutar todo únicamente en entorno local

No se adopta.

Ventajas:

- simplicidad;
- ausencia de infraestructura externa;
- menor configuración inicial.

Desventajas:

- no produce una URL pública;
- depende del equipo del desarrollador;
- no permite validación independiente;
- no demuestra arquitectura de despliegue;
- no satisface la evidencia S8.

---

### Alternativa B - Desplegar todas las piezas en una única plataforma

No se adopta como principio general.

Por ejemplo, sería posible intentar servir Flutter y FastAPI desde un mismo
entorno y administrar MySQL dentro de infraestructura propia.

Ventajas:

- menos destinos de despliegue;
- posible simplificación inicial de operación.

Desventajas:

- mezcla piezas con necesidades operativas diferentes;
- aumenta el acoplamiento entre frontend y backend;
- dificulta rollback independiente;
- puede obligar a redesplegar piezas no modificadas;
- dificulta asignar costos y restricciones por componente.

---

### Alternativa C - Seleccionar plataforma por pieza

Se adopta.

Cada pieza se evalúa de forma independiente según:

- tipo de ejecución;
- persistencia requerida;
- costo;
- disponibilidad de capa gratuita o beneficio académico;
- necesidad de tarjeta;
- observabilidad;
- reproducibilidad;
- rollback.

La selección resultante es:

```text
Flutter Web
→ GitHub Pages
→ ADR-0006

FastAPI
→ Azure App Service
→ ADR-0007

MySQL
→ Azure Database for MySQL Flexible Server
→ ADR-0008
```

---

## Decisión

Se adopta una **estrategia de despliegue por pieza**.

La topología resultante es:

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

La asignación de plataformas es:

| Pieza | Plataforma | ADR específico |
|---|---|---|
| Frontend Flutter Web | GitHub Pages | ADR-0006 |
| Backend API FastAPI | Azure App Service | ADR-0007 |
| Persistencia MySQL | Azure Database for MySQL Flexible Server | ADR-0008 |

---

## Justificación

### Frontend

Flutter Web produce contenido estático después de:

```text
flutter build web
```

Por esta razón se publica de manera independiente mediante GitHub Pages.

La decisión específica, sus alternativas, costo y rollback se encuentran en:

[ADR-0006](./0006-publicar-frontend-flutter-web-en-github-pages.md)

---

### Backend

FastAPI necesita un proceso de servidor activo, configuración por entorno,
observabilidad y conectividad con MySQL.

Por esta razón se ejecuta mediante Azure App Service.

La decisión específica se encuentra en:

[ADR-0007](./0007-desplegar-api-fastapi-en-azure-app-service.md)

---

### Persistencia

MySQL requiere almacenamiento persistente y acceso controlado desde el backend.

Por esta razón se utiliza Azure Database for MySQL Flexible Server.

La decisión específica se encuentra en:

[ADR-0008](./0008-desplegar-mysql-en-azure-flexible-server.md)

---

## Arquitectura resultante

La estrategia de despliegue no modifica la arquitectura interna del backend.

La dirección continúa siendo:

```text
Flutter Web
    ↓ HTTPS / JSON
FastAPI
    ↓
router
    ↓
service
    ↓
repository
    ↓ PyMySQL / TLS
MySQL
```

El despliegue modifica **dónde se ejecutan las piezas**, no sus
responsabilidades de dominio.

---

## Infraestructura como código

Los recursos principales utilizados en Azure se encuentran declarados en:

`infra/main.bicep`

La plantilla incluye infraestructura correspondiente al Backend API y la
persistencia.

Durante S8 fue verificada mediante:

```text
az bicep build
```

y:

```text
az deployment group validate
```

Resultado observado:

```text
provisioningState: Succeeded
error: null
```

Los detalles específicos de cada plataforma se mantienen en los ADR
correspondientes.

---

## Seguridad

Las credenciales reales de MySQL no se almacenan en el repositorio.

La configuración sensible se proporciona mediante:

- parámetros seguros de Bicep;
- App Settings de Azure;
- variables de entorno.

La comunicación pública utiliza HTTPS.

La comunicación:

```text
FastAPI → MySQL
```

utiliza TLS.

El frontend nunca recibe credenciales de persistencia.

---

## Observabilidad

El Backend API dispone de:

```text
GET /health
```

y genera logs estructurados con información como:

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

También expone:

```text
GET /ops/metrics/ec01
```

como métrica operacional asociada con EC-01.

---

## Costo

El costo no se evalúa como un único precio del sistema.

Se evalúa por pieza.

### Frontend

GitHub Pages.

Durante S8 no se observó costo adicional para el repositorio público utilizado.

Detalle:

[ADR-0006](./0006-publicar-frontend-flutter-web-en-github-pages.md)

### Backend

Azure App Service F1.

El prototipo utiliza el nivel F1 dentro del entorno académico disponible.

Detalle:

[ADR-0007](./0007-desplegar-api-fastapi-en-azure-app-service.md)

### Persistencia

Azure Database for MySQL Flexible Server.

Configuración utilizada:

```text
Standard_B1ms
1 vCore
2 GiB RAM
32 GiB
Alta disponibilidad: deshabilitada
```

Estimación observada durante S8:

```text
~USD 14.71 / mes
```

antes de aplicar créditos o beneficios académicos.

Detalle:

[ADR-0008](./0008-desplegar-mysql-en-azure-flexible-server.md)

---

## Verificación realizada

Durante S8 se verificó realmente:

- frontend público mediante GitHub Pages;
- backend público mediante Azure App Service;
- MySQL ejecutándose en Azure;
- comunicación HTTPS;
- conexión TLS con MySQL;
- CORS desde el origen público;
- `/health` HTTP 200;
- degradación HTTP 503 sin MySQL;
- recuperación posterior HTTP 200;
- creación de una publicación desde Flutter Web;
- consulta posterior de publicaciones;
- persistencia real;
- logs estructurados;
- métrica EC-01;
- build Flutter Web;
- pipeline del backend en verde;
- infraestructura Bicep compilada y validada.

---

## Rollback

El rollback se define de manera independiente por pieza.

### Frontend

Se reconstruye y republica un `build/web` correspondiente a un commit
previamente validado.

Detalle:

[ADR-0006](./0006-publicar-frontend-flutter-web-en-github-pages.md)

### Backend

Se genera un ZIP a partir de un commit conocido y se redespliega mediante Azure
CLI.

Detalle:

[ADR-0007](./0007-desplegar-api-fastapi-en-azure-app-service.md)

### Persistencia

Se recrea una instancia MySQL compatible, se recuperan datos cuando
corresponda y se actualizan las variables de conexión del backend.

Detalle:

[ADR-0008](./0008-desplegar-mysql-en-azure-flexible-server.md)

---

## Consecuencias positivas

- cada pieza utiliza una plataforma apropiada para su naturaleza;
- frontend, API y persistencia pueden evolucionar independientemente;
- los costos pueden analizarse por componente;
- el rollback puede realizarse por pieza;
- se mantiene el monolito modular;
- existe una URL pública verificable;
- la infraestructura Azure queda versionada;
- los secretos permanecen fuera del código;
- se dispone de observabilidad operacional.

---

## Consecuencias negativas

- existen tres piezas operativas que deben coordinarse;
- deben mantenerse configuraciones entre proveedores;
- CORS debe mantenerse correctamente;
- el costo de MySQL debe vigilarse;
- los beneficios académicos no garantizan costo cero permanente;
- los cambios de plataforma deben mantenerse alineados con arc42, ADR e IaC.

---

## Relación con ADR anteriores

### ADR-0001 - Monolito modular

Continúa vigente.

El despliegue no convierte el backend en microservicios.

### ADR-0002 - Manejo de bloqueo temporal de SQLite

Se conserva como evidencia histórica del primer corte.

No describe la persistencia vigente.

### ADR-0003 - Integración síncrona HTTP/JSON

Continúa vigente.

En el entorno público la comunicación utiliza HTTPS/JSON.

### ADR-0004 - Migrar persistencia de SQLite a MySQL

Continúa vigente.

Define MySQL como tecnología de persistencia.

ADR-0008 define específicamente dónde se ejecuta esa persistencia durante S8.

---

## ADR que refinan esta decisión

Las decisiones vigentes por plataforma son:

### Frontend

[ADR-0006 - Publicar Flutter Web mediante GitHub Pages](./0006-publicar-frontend-flutter-web-en-github-pages.md)

### Backend API

[ADR-0007 - Desplegar FastAPI mediante Azure App Service](./0007-desplegar-api-fastapi-en-azure-app-service.md)

### Persistencia

[ADR-0008 - Desplegar MySQL mediante Azure Database for MySQL Flexible Server](./0008-desplegar-mysql-en-azure-flexible-server.md)

Estos tres ADR son la fuente específica para evaluar la decisión de plataforma
de cada pieza.

---

## Documentación relacionada

- `docs/arc42/02-restricciones.md`
- `docs/arc42/07-vista-despliegue.md`
- `docs/arc42/ARC42.md`
- `docs/evidencias/evidencia-s8-2026-09-27.md`
- `README.md`
- `infra/main.bicep`
