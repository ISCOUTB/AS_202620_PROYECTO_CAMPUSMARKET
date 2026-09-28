# CampusMarket

Marketplace universitario para la publicación, consulta, venta y alquiler de
productos dentro de la comunidad universitaria.

## Integrantes

- Joshua Tenorio Alvarez
- Camilo Martinez Berrio
- Nilver Garcia Pimentel

---

# Estado arquitectónico vigente

CampusMarket utiliza un **monolito modular** como estrategia arquitectónica del
backend.

La decisión se encuentra registrada en:

[ADR-0001 - Usar monolito modular](docs/adr/0001-usar-monolito-modular.md)

Las capacidades principales del sistema se organizan alrededor de los contextos:

- `usuarios`;
- `publicaciones`;
- `catalogo`;
- `administracion`.

Actualmente la capacidad funcional materializada con mayor profundidad es:

**Gestión de Publicaciones**

La arquitectura lógica vigente es:

```text
Flutter Web
    ↓ HTTPS / JSON
    ↓ contrato OpenAPI
FastAPI
    ↓
router.py
    ↓
service.py
    ↓
repository.py
    ↓ PyMySQL / TLS
MySQL
```

La persistencia vigente es:

**MySQL**

SQLite permanece únicamente como parte de la historia arquitectónica del
primer corte.

La evolución de SQLite hacia MySQL se encuentra documentada en:

[ADR-0004 - Migrar persistencia de SQLite a MySQL](docs/adr/0004-migrar-persistencia-a-mysql.md)

---

# Tecnologías vigentes

| Elemento | Tecnología |
|---|---|
| Frontend | Flutter Web / Dart |
| Backend | FastAPI / Python 3.12 |
| Servidor ASGI | Uvicorn |
| Estilo arquitectónico | Monolito modular |
| Persistencia | MySQL 8.4 |
| Driver | PyMySQL |
| API | REST / HTTPS / JSON |
| Contrato | OpenAPI 3.1 |
| Versión API | `1.0.0` |
| Pruebas | pytest |
| Análisis estático CI | Ruff |
| Integración continua | GitHub Actions |
| Calidad | SonarQube Cloud |
| IaC | Azure Bicep |
| Frontend público | GitHub Pages |
| Backend público | Azure App Service |
| Base de datos pública | Azure Database for MySQL Flexible Server |
| Diagramas | PlantUML |

---

# S8 - Despliegue y operación

Durante S8 CampusMarket pasó de un entorno principalmente local a un entorno
público, reproducible y verificable.

La topología desplegada es:

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

Este despliegue modifica la infraestructura de ejecución, pero no modifica las
fronteras internas del monolito modular.

---

## URLs públicas

### Frontend

`https://nnigarp.github.io/AS_202620_PROYECTO_CAMPUSMARKET/`

### Backend

`https://campusmarket-s8-api-nilver.azurewebsites.net`

### Health check

`https://campusmarket-s8-api-nilver.azurewebsites.net/health`

La aplicación pública identifica la arquitectura vigente como:

```text
CampusMarket S8: Flutter Web → FastAPI → MySQL en Azure.
```

---

# Verificación del corte vertical público

Durante S8 se verificó desde un navegador el recorrido:

```text
GitHub Pages
    ↓
Flutter Web
    ↓ HTTPS / JSON
Azure App Service
    ↓
FastAPI
    ↓
Gestión de Publicaciones
    ↓
Repository
    ↓ TLS
Azure MySQL
```

Desde la aplicación pública se creó correctamente una publicación.

La interfaz confirmó:

```text
Publicación #2 guardada correctamente.
```

La publicación también pudo recuperarse posteriormente mediante:

```text
GET /publicaciones
```

Esto verifica que el recorrido público atraviesa realmente:

- frontend desplegado;
- CORS;
- API desplegada;
- lógica de aplicación;
- repositorio;
- conexión TLS;
- MySQL.

---

# CORS

El Backend API autoriza explícitamente el origen público del frontend:

```text
https://nnigarp.github.io
```

Durante la validación se realizó una solicitud:

```text
OPTIONS /publicaciones
```

desde ese origen.

Resultado:

```text
HTTP 200
Access-Control-Allow-Origin: https://nnigarp.github.io
```

Posteriormente fue posible ejecutar:

```text
POST /publicaciones
```

desde Flutter Web.

---

# Infraestructura como código

Los recursos principales utilizados por CampusMarket en Azure se encuentran
declarados mediante Bicep en:

[`infra/main.bicep`](infra/main.bicep)

La plantilla incluye recursos asociados con:

- Azure App Service Plan;
- Azure Web App;
- Azure Database for MySQL Flexible Server;
- base de datos `campusmarket`;
- configuración del backend;
- reglas de acceso necesarias;
- parámetros dependientes del entorno.

La contraseña administrativa de MySQL se proporciona mediante un parámetro
seguro y no se almacena directamente en el archivo.

## Compilación

La plantilla fue comprobada mediante:

```bash
az bicep build --file infra/main.bicep
```

Resultado:

```text
BICEP_BUILD_OK
```

## Validación

La infraestructura fue validada mediante:

```bash
az deployment group validate \
  --resource-group rg-campusmarket-s8 \
  --template-file infra/main.bicep \
  --parameters mysqlAdministratorPassword="<VALOR_SEGURO>"
```

Resultado:

```text
provisioningState: Succeeded
error: null
```

---

# Recursos desplegados

## Frontend

Tecnología:

```text
Flutter Web
```

Plataforma:

```text
GitHub Pages
```

Rama de publicación:

```text
gh-pages
```

URL:

`https://nnigarp.github.io/AS_202620_PROYECTO_CAMPUSMARKET/`

---

## Backend

Tecnología:

```text
FastAPI / Python 3.12
```

Plataforma:

```text
Azure App Service sobre Linux
```

Aplicación:

```text
campusmarket-s8-api-nilver
```

Región:

```text
Mexico Central
```

Comando de ejecución:

```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

URL:

`https://campusmarket-s8-api-nilver.azurewebsites.net`

---

## Persistencia

Servicio:

```text
Azure Database for MySQL Flexible Server
```

Configuración utilizada durante S8:

```text
MySQL 8.4
Standard_B1ms
1 vCore
2 GiB RAM
32 GiB almacenamiento
Alta disponibilidad: deshabilitada
```

Base de datos:

```text
campusmarket
```

El backend accede a la persistencia mediante:

```text
PyMySQL
```

y utiliza TLS para la conexión.

---

# Configuración y secretos

La aplicación utiliza variables de entorno para separar la configuración del
código fuente.

Variables principales:

```text
CAMPUSMARKET_DB_HOST
CAMPUSMARKET_DB_PORT
CAMPUSMARKET_DB_USER
CAMPUSMARKET_DB_PASSWORD
CAMPUSMARKET_DB_NAME
CAMPUSMARKET_DB_SSL
```

Las credenciales reales no deben almacenarse en el repositorio.

En Azure, los valores sensibles se proporcionan mediante:

- App Settings;
- variables de entorno;
- parámetros seguros de Bicep.

El archivo `.env`, cuando se utiliza localmente, permanece excluido mediante
`.gitignore`.

No se incluyen contraseñas reales dentro de la documentación del proyecto.

---

# Reproducción local

## Requisitos

- Python 3.12;
- Flutter disponible en `PATH`;
- Google Chrome;
- MySQL disponible;
- dependencias Python instaladas;
- variables de conexión configuradas.

Desde la raíz del repositorio:

```bash
pip install -r backend/requirements.txt
```

---

## Configuración MySQL local

Ejemplo PowerShell:

```powershell
$env:CAMPUSMARKET_DB_HOST="localhost"
$env:CAMPUSMARKET_DB_PORT="3306"
$env:CAMPUSMARKET_DB_USER="campusmarket_app"
$env:CAMPUSMARKET_DB_PASSWORD="<PASSWORD_LOCAL>"
$env:CAMPUSMARKET_DB_NAME="campusmarket"
$env:CAMPUSMARKET_DB_SSL="false"
```

Nunca reemplazar `<PASSWORD_LOCAL>` por una credencial real dentro de un archivo
versionado.

---

# Ejecución del backend

Desde la raíz:

```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

Backend local:

```text
http://localhost:8000
```

Health local:

```text
http://localhost:8000/health
```

---

# Ejecución del frontend

Desde:

```bash
cd frontend/campusmarket
```

puede verificarse primero:

```bash
flutter analyze
```

Para ejecución local:

```bash
flutter run -d chrome
```

El frontend utiliza por defecto:

```text
http://localhost:8000
```

como Backend API cuando no se proporciona una configuración distinta.

---

# Build del frontend desplegado

El frontend de producción se genera mediante:

```bash
flutter build web \
  --release \
  --dart-define=CAMPUSMARKET_API_BASE_URL=https://campusmarket-s8-api-nilver.azurewebsites.net \
  --base-href "/AS_202620_PROYECTO_CAMPUSMARKET/"
```

El artefacto resultante queda en:

```text
frontend/campusmarket/build/web
```

y se publica mediante la rama:

```text
gh-pages
```

Antes del build se verificó:

```bash
flutter analyze
```

con resultado:

```text
No issues found!
```

---

# Despliegue reproducible del backend

Un estado conocido del repositorio puede empaquetarse mediante:

```bash
git archive --format=zip \
  -o campusmarket-s8.zip \
  <COMMIT>
```

El ZIP puede desplegarse posteriormente mediante:

```bash
az webapp deploy \
  --resource-group rg-campusmarket-s8 \
  --name campusmarket-s8-api-nilver \
  --src-path campusmarket-s8.zip \
  --type zip
```

Después del despliegue deben comprobarse como mínimo:

```text
GET /health
GET /publicaciones
POST /publicaciones
```

---

# Health check

CampusMarket expone:

```text
GET /health
```

Con MySQL disponible se verificó:

```text
HTTP 200
```

Respuesta:

```json
{
  "status": "ok",
  "service": "campusmarket-api"
}
```

También se verificó el comportamiento de degradación.

Con MySQL no disponible:

```text
HTTP 503
```

Después de recuperar la dependencia:

```text
HTTP 200
```

El endpoint permite distinguir una API operativa de una API cuya dependencia de
persistencia no está disponible.

---

# Observabilidad

## Logs estructurados

Las solicitudes HTTP generan registros estructurados con información como:

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

Ejemplo conceptual de los datos emitidos:

```json
{
  "event": "http_request",
  "request_id": "...",
  "method": "GET",
  "path": "/health",
  "status_code": 200,
  "duration_ms": 145.20
}
```

Los registros fueron observados durante la ejecución real de Azure App Service.

---

## Métrica operacional EC-01

CampusMarket expone:

```text
GET /ops/metrics/ec01
```

La métrica está relacionada con:

**EC-01 - Consulta de productos**

Durante S8 se generaron solicitudes reales al backend.

Resultado observado:

```text
Solicitudes observadas: 10
Solicitudes <= 2000 ms: 10
Máximo aproximado: 164.41 ms
Mínimo aproximado: 137.75 ms
meets_backend_target: true
```

La medición corresponde al recorrido del backend.

No se presenta como una medición completa extremo a extremo del tiempo
percibido desde Flutter Web.

---

# Pruebas automatizadas

Desde la raíz:

```bash
python -m pytest backend/tests -q
```

Las pruebas principales incluyen:

- [`backend/tests/test_health.py`](backend/tests/test_health.py)
- [`backend/tests/test_publicaciones_vertical.py`](backend/tests/test_publicaciones_vertical.py)
- [`backend/tests/test_modularidad_s6.py`](backend/tests/test_modularidad_s6.py)
- [`backend/tests/test_contrato_openapi.py`](backend/tests/test_contrato_openapi.py)

El conjunto vigente verifica, entre otros aspectos:

- disponibilidad mediante `/health`;
- dependencia real del health check con MySQL;
- creación de publicaciones;
- consulta de publicaciones;
- persistencia real;
- respuesta HTTP `201`;
- degradación HTTP `503`;
- propiedad única del dato `publicaciones`;
- dirección `router → service → repository → MySQL`;
- correspondencia contrato OpenAPI ↔ FastAPI.

---

# Análisis estático

El pipeline ejecuta:

```bash
python -m ruff check backend
```

Ruff forma parte de la verificación automática de S8.

---

# Integración continua

El workflow se encuentra en:

[`.github/workflows/backend-tests.yml`](.github/workflows/backend-tests.yml)

El pipeline:

1. obtiene el repositorio;
2. configura Python 3.12;
3. instala dependencias;
4. levanta MySQL 8.4;
5. configura las variables de prueba;
6. verifica la disponibilidad de MySQL;
7. ejecuta Ruff;
8. ejecuta pruebas funcionales y arquitectónicas;
9. ejecuta la prueba de contrato OpenAPI.

---

# Cierre S8 en master

S8 fue integrada al repositorio oficial mediante:

**Pull Request #43**

Título:

```text
S8 - Despliegue y operación de CampusMarket
```

Merge commit:

```text
bea2412082b0acb2dc37262376622d63fccff5df
```

Rama:

```text
master
```

El pipeline ejecutado sobre ese merge finalizó correctamente.

GitHub Actions:

`https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/36377033900`

Resultado:

```text
conclusion: success
```

También se verificó:

```text
SonarQube Cloud
Quality Gate: Passed
```

---

# SonarQube Cloud

Proyecto:

```text
Project Key: ISCOUTB_AS_202620_PROYECTO_CAMPUSMARKET
Organization Key: isco-utb
```

Estado verificado después del merge de S8:

```text
Quality Gate: Passed
```

El análisis oficial continúa asociado al proyecto público de CampusMarket.

La configuración se encuentra en:

[`.sonarcloud.properties`](.sonarcloud.properties)

---

# Costo estimado del despliegue

La estimación se separa por pieza.

## Frontend

Plataforma:

```text
GitHub Pages
```

Durante S8 no se observó un costo adicional para el repositorio público
utilizado por el equipo.

---

## Backend

Plataforma:

```text
Azure App Service
```

Nivel utilizado:

```text
F1
```

Fue seleccionado para mantener el Backend API del prototipo dentro de una
configuración de costo mínimo.

---

## Persistencia

Servicio:

```text
Azure Database for MySQL Flexible Server
```

Configuración:

```text
Standard_B1ms
1 vCore
2 GiB RAM
32 GiB almacenamiento
Alta disponibilidad: deshabilitada
```

Durante la configuración se observó en Azure una estimación aproximada de:

```text
USD 14.71 / mes
```

antes de aplicar créditos o beneficios académicos.

Esta cifra corresponde a una **estimación observada**, no a una factura real.

---

## Supuestos de carga

Para el prototipo académico se consideran:

- tres integrantes del equipo;
- uso principalmente durante desarrollo, demostración y evaluación;
- concurrencia baja;
- número reducido de publicaciones;
- una única API;
- una única base de datos;
- sin alta disponibilidad;
- sin procesamiento masivo;
- sin archivos multimedia persistidos en Azure.

El volumen actual no justifica incrementar las capacidades contratadas.

---

## Punto de ruptura

La configuración actual deja de mantenerse bajo las condiciones de costo
académicas actuales cuando ocurre alguno de estos casos:

- se terminan los créditos o beneficios académicos disponibles;
- el backend requiere abandonar App Service F1;
- MySQL requiere un SKU superior;
- se incrementa el almacenamiento;
- se habilita alta disponibilidad;
- se despliegan instancias adicionales;
- se incorporan nuevos servicios Azure con cobro.

El principal costo potencial de la arquitectura S8 corresponde a:

**Azure Database for MySQL Flexible Server**

---

# Rollback

## Backend

El backend puede regresar a un commit previamente validado.

Generar el artefacto:

```bash
git archive --format=zip \
  -o campusmarket-rollback.zip \
  <KNOWN_GOOD_SHA>
```

Desplegarlo nuevamente:

```bash
az webapp deploy \
  --resource-group rg-campusmarket-s8 \
  --name campusmarket-s8-api-nilver \
  --src-path campusmarket-rollback.zip \
  --type zip
```

Después se deben verificar:

```text
GET /health
GET /publicaciones
POST /publicaciones
```

---

## Frontend

El frontend puede regresar a una versión conocida:

1. seleccionar el commit validado;
2. reconstruir `build/web`;
3. publicar nuevamente el artefacto mediante `gh-pages`;
4. comprobar la URL pública;
5. ejecutar nuevamente el corte vertical.

---

# Documentación S8

## Evidencia consolidada

[`docs/evidencias/evidencia-s8-2026-09-27.md`](docs/evidencias/evidencia-s8-2026-09-27.md)

## Vista de despliegue

[`docs/arc42/07-vista-despliegue.md`](docs/arc42/07-vista-despliegue.md)

## Restricciones

[`docs/arc42/02-restricciones.md`](docs/arc42/02-restricciones.md)

## arc42 consolidado

[`docs/arc42/ARC42.md`](docs/arc42/ARC42.md)

## Decisión de despliegue

[`docs/adr/0005-desplegar-campusmarket-en-azure-y-github-pages.md`](docs/adr/0005-desplegar-campusmarket-en-azure-y-github-pages.md)

## Infraestructura

[`infra/main.bicep`](infra/main.bicep)

## Registro de IA

[`docs/ia.md`](docs/ia.md)

---

# Contrato OpenAPI

Durante S7 se formalizó la interfaz:

```text
Flutter
   ↓ HTTPS / JSON
Contrato OpenAPI
   ↓
FastAPI
```

El contrato se mantiene en:

[`contracts/openapi-v1.json`](contracts/openapi-v1.json)

Versión:

```text
OpenAPI 3.1.0
API 1.0.0
```

Operaciones materializadas:

| Método | Ruta | Propósito |
|---|---|---|
| `GET` | `/health` | Consultar salud del backend |
| `GET` | `/publicaciones` | Consultar publicaciones |
| `POST` | `/publicaciones` | Crear publicación |

La prueba contractual se encuentra en:

[`backend/tests/test_contrato_openapi.py`](backend/tests/test_contrato_openapi.py)

---

# Dominio y modularidad

Los contextos definidos son:

- Gestión de Usuarios;
- Gestión de Publicaciones;
- Catálogo;
- Administración.

Regla arquitectónica principal:

> Cada dato de dominio tiene un único módulo responsable de escribirlo.

La entidad materializada actualmente es:

```text
publicaciones
```

y su propietario es:

**Gestión de Publicaciones**

El escritor productivo se encuentra en:

[`backend/app/publicaciones/repository.py`](backend/app/publicaciones/repository.py)

La prueba:

[`backend/tests/test_modularidad_s6.py`](backend/tests/test_modularidad_s6.py)

verifica la dirección:

```text
router → service → repository → MySQL
```

---

# Diagramas C4

## Nivel 1 - Contexto

- [Documentación](docs/c4/01-contexto.md)
- [PlantUML](docs/c4/01-contexto.puml)

## Nivel 2 - Contenedores

- [Documentación](docs/c4/02-contenedores.md)
- [PlantUML](docs/c4/02-contenedores.puml)

Estado lógico:

```text
Frontend Web
    ↓ HTTPS / JSON
Backend API
    ↓ PyMySQL / TLS
MySQL
```

## Nivel 3 - Backend

- [Documentación](docs/c4/03-componentes-backend.md)
- [PlantUML](docs/c4/03-componentes-backend.puml)

Descomposición materializada:

```text
API de Publicaciones
        ↓
Servicio de Publicaciones
        ↓
Repositorio de Publicaciones
        ↓
MySQL
```

---

# Evolución histórica

## S4

Primer corte vertical:

```text
Flutter Web
    ↓
FastAPI
    ↓
Gestión de Publicaciones
    ↓
SQLite
```

Esta sección pertenece al estado histórico inicial.

---

## S5

Se evaluó la degradación ante bloqueo temporal de SQLite.

Línea base:

```text
HTTP 500
7.323 s
```

Después de ADR-0002:

```text
HTTP 503
1.283 s
```

La decisión se conserva como evidencia histórica:

[ADR-0002 - Manejo de bloqueo temporal de SQLite](docs/adr/0002-manejo-bloqueo-sqlite.md)

---

## S6

Se formalizaron:

- lenguaje ubicuo;
- contextos delimitados;
- mapa de contextos;
- propiedad única de datos;
- C4 Nivel 3;
- reglas automáticas de modularidad.

Documentación:

[`docs/arc42/08-conceptos-transversales.md`](docs/arc42/08-conceptos-transversales.md)

---

## S7

Se formalizaron:

- contrato OpenAPI;
- API-first;
- integración síncrona HTTP/JSON;
- prueba contractual;
- demostración de incompatibilidad;
- migración a MySQL.

Evidencia:

[`docs/evidencias/evidencia-s7-2026-09-15.md`](docs/evidencias/evidencia-s7-2026-09-15.md)

---

## S8

Se materializaron:

- despliegue público;
- GitHub Pages;
- Azure App Service;
- Azure MySQL;
- HTTPS;
- CORS;
- health check dependiente de persistencia;
- logs estructurados;
- métrica operacional;
- Ruff;
- infraestructura Bicep;
- validación IaC;
- protección de secretos;
- costos;
- rollback;
- arc42 sección 7;
- restricciones operativas;
- ADR de despliegue;
- pipeline verde sobre `master`.

---

# ADR

## Vigentes

- [ADR-0001 - Monolito modular](docs/adr/0001-usar-monolito-modular.md)
- [ADR-0003 - Integración síncrona HTTP/JSON](docs/adr/0003-usar-integracion-sincrona-http-json.md)
- [ADR-0004 - Migrar persistencia a MySQL](docs/adr/0004-migrar-persistencia-a-mysql.md)
- [ADR-0005 - Despliegue Azure y GitHub Pages](docs/adr/0005-desplegar-campusmarket-en-azure-y-github-pages.md)

## Histórico

- [ADR-0002 - Manejo de bloqueo temporal de SQLite](docs/adr/0002-manejo-bloqueo-sqlite.md)

ADR-0002 permanece como evidencia válida del contexto del primer corte, pero no
describe la persistencia vigente.

---

# Documentación arc42

- [arc42 consolidado](docs/arc42/ARC42.md)
- [Sección 2 - Restricciones](docs/arc42/02-restricciones.md)
- [Sección 3 - Contexto](docs/arc42/03-contexto.md)
- [Sección 4 - Estrategia de solución](docs/arc42/04-estrategia-de-solucion.md)
- [Sección 5 - Bloques de construcción](docs/arc42/05-bloques-de-construccion.md)
- [Sección 6 - Vista de ejecución](docs/arc42/06-vista-ejecucion.md)
- [Sección 7 - Vista de despliegue](docs/arc42/07-vista-despliegue.md)
- [Sección 8 - Conceptos transversales](docs/arc42/08-conceptos-transversales.md)
- [Sección 9 - Decisiones](docs/arc42/09-decisiones.md)
- [Sección 10 - Árbol de utilidad](docs/arc42/10-arbol-de-utilidad.md)
- [Sección 10 - Escenarios de calidad](docs/arc42/10-escenarios-de-calidad.md)
- [Sección 12 - Glosario](docs/arc42/12-glosario.md)

---

# Trazabilidad

La trazabilidad general se mantiene en:

[`docs/aspectos.md`](docs/aspectos.md)

Cadena utilizada:

```text
Aspecto
   ↓
Restricción / escenario
   ↓
ADR
   ↓
C4 / arc42
   ↓
Código
   ↓
Pruebas
   ↓
CI
   ↓
Despliegue
   ↓
Evidencia
```

---

# Uso de Inteligencia Artificial

El registro se encuentra en:

[`docs/ia.md`](docs/ia.md)

Para cada uso de IA se documenta:

- herramienta;
- uso realizado;
- verificación del equipo;
- propuestas rechazadas;
- motivo del rechazo.

Las respuestas generadas por IA no se consideran evidencia por sí solas.

Durante S8 se aplicó como criterio:

```text
requisito literal
→ implementación
→ ejecución real
→ evidencia verificable
→ documentación
```

---

# Evidencias principales

## S1-S5

- [Correcciones S1-S4](correcciones.md)
- [ADR-0001](docs/adr/0001-usar-monolito-modular.md)
- [ADR-0002](docs/adr/0002-manejo-bloqueo-sqlite.md)
- [C4 Nivel 1](docs/c4/01-contexto.md)
- [C4 Nivel 2](docs/c4/02-contenedores.md)
- [Línea base S5](docs/evidencias/linea-base-bloqueo-sqlite-2026-09-05.md)
- [Medición S5](docs/evidencias/medicion-bloqueo-sqlite-2026-09-06.md)

## S6

- [Conceptos transversales](docs/arc42/08-conceptos-transversales.md)
- [C4 Nivel 3](docs/c4/03-componentes-backend.md)
- [Auditoría modular](docs/evidencias/auditoria-modularidad-s6-2026-09-12.md)
- [Prueba modularidad](backend/tests/test_modularidad_s6.py)

## S7

- [Evidencia S7](docs/evidencias/evidencia-s7-2026-09-15.md)
- [Contrato OpenAPI](contracts/openapi-v1.json)
- [Prueba de contrato](backend/tests/test_contrato_openapi.py)
- [ADR-0003](docs/adr/0003-usar-integracion-sincrona-http-json.md)
- [ADR-0004](docs/adr/0004-migrar-persistencia-a-mysql.md)
- [Fallo incompatible](docs/evidencias/fallo-contrato-s7-2026-09-15.md)

## S8

- [Evidencia consolidada S8](docs/evidencias/evidencia-s8-2026-09-27.md)
- [Vista de despliegue](docs/arc42/07-vista-despliegue.md)
- [Restricciones operativas](docs/arc42/02-restricciones.md)
- [ADR-0005](docs/adr/0005-desplegar-campusmarket-en-azure-y-github-pages.md)
- [Infraestructura Bicep](infra/main.bicep)
- [Workflow CI](.github/workflows/backend-tests.yml)
- [Registro de IA](docs/ia.md)

---

# Estado final verificable S8

- [x] frontend accesible públicamente;
- [x] backend accesible públicamente;
- [x] MySQL desplegado y utilizado por el backend;
- [x] HTTPS;
- [x] CORS funcional;
- [x] `GET /health` HTTP `200`;
- [x] degradación HTTP `503` sin MySQL;
- [x] recuperación posterior HTTP `200`;
- [x] publicación creada desde Flutter Web público;
- [x] persistencia real;
- [x] infraestructura Bicep versionada;
- [x] Bicep compilado;
- [x] Bicep validado;
- [x] logs estructurados;
- [x] métrica operacional asociada a EC-01;
- [x] Ruff en CI;
- [x] secretos fuera del código fuente;
- [x] estimación de costo documentada;
- [x] rollback documentado;
- [x] arc42 actualizado;
- [x] ADR de despliegue documentado;
- [x] PR #43 integrado;
- [x] pipeline exitoso sobre `master`;
- [x] SonarQube Cloud Quality Gate aprobado.

## Referencia de cierre S8

```text
Repositorio:
ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET

Rama:
master

Merge commit S8:
bea2412082b0acb2dc37262376622d63fccff5df

GitHub Actions:
https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/36377033900

Resultado:
success

Frontend:
https://nnigarp.github.io/AS_202620_PROYECTO_CAMPUSMARKET/

Backend:
https://campusmarket-s8-api-nilver.azurewebsites.net

Health:
https://campusmarket-s8-api-nilver.azurewebsites.net/health
```
