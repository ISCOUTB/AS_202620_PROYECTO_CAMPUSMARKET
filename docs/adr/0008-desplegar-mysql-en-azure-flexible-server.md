# ADR-0008 - Desplegar MySQL mediante Azure Database for MySQL Flexible Server

## Estado

Aceptado

## Fecha

2026-09-27

## Pieza decidida

**Persistencia MySQL de CampusMarket**

Esta decisión corresponde exclusivamente a la pieza de base de datos.

No decide el hosting de Flutter Web ni la plataforma utilizada por FastAPI.

---

## Contexto

ADR-0004 estableció MySQL como tecnología de persistencia vigente de
CampusMarket.

Durante S8 debe decidirse dónde ejecutar esta base de datos para soportar el
corte vertical público:

```text
Flutter Web
    ↓
FastAPI
    ↓
Repository
    ↓
MySQL
```

La base de datos debe:

- estar accesible desde el Backend API desplegado;
- mantener las credenciales fuera del código;
- utilizar comunicación protegida;
- conservar la propiedad de datos definida por Gestión de Publicaciones;
- poder recrearse mediante infraestructura versionada;
- ser suficiente para la carga académica actual;
- disponer de una política explícita de costo.

Restricciones relacionadas:

- R-08 - despliegue público;
- R-09 - protección de secretos;
- R-10 - infraestructura como código;
- R-11 - límite de costo;
- R-12 - no dependencia de tarjeta personal.

---

## Alternativas consideradas

### Alternativa A - Azure Database for MySQL Flexible Server

Utilizar MySQL como servicio administrado de Azure.

Ventajas:

- motor MySQL compatible con la decisión ADR-0004;
- conexión remota desde App Service;
- configuración TLS;
- recurso declarable mediante Bicep;
- separación entre aplicación y persistencia;
- menor administración manual del motor;
- permite mantener `repository.py` sin cambiar sus responsabilidades.

Desventajas:

- representa el principal costo potencial del entorno;
- depende de créditos o presupuesto cuando no existe cobertura académica;
- requiere reglas de red y configuración correctas;
- un servicio administrado añade dependencia del proveedor.

---

### Alternativa B - MySQL autogestionado en servidor del laboratorio

Instalar y operar MySQL directamente sobre infraestructura institucional.

Ventajas:

- alternativa utilizable sin tarjeta bancaria personal;
- puede evitar consumo de créditos Azure;
- control directo sobre el proceso MySQL.

Desventajas:

- el equipo debe instalar, actualizar, configurar y operar el motor;
- debe gestionar manualmente seguridad, TLS, disponibilidad y copias;
- aumenta las tareas operativas ajenas al objetivo principal del prototipo;
- dificulta reproducir exactamente el entorno utilizado durante S8 mediante el
  Bicep actual;
- aumenta la dependencia de acceso al servidor institucional.

---

## Decisión

Se selecciona:

**Azure Database for MySQL Flexible Server**

para ejecutar la persistencia del entorno S8.

Configuración utilizada:

```text
Motor: MySQL 8.4
SKU: Standard_B1ms
vCPU: 1
Memoria: 2 GiB
Almacenamiento: 32 GiB
Alta disponibilidad: deshabilitada
Base de datos: campusmarket
```

El acceso desde FastAPI se realiza mediante:

```text
PyMySQL
```

---

## Justificación

La alternativa administrada permite concentrar la responsabilidad de
CampusMarket en el código y en la arquitectura de la aplicación, evitando que el
equipo tenga que administrar manualmente un servidor MySQL completo durante la
evidencia S8.

La decisión no modifica la propiedad de datos.

La dirección permanece:

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

## Infraestructura como código

La instancia MySQL y la base de datos se encuentran declaradas en:

`infra/main.bicep`

La plantilla fue compilada y validada durante S8.

Resultado:

```text
provisioningState: Succeeded
error: null
```

El parámetro de contraseña administrativa se encuentra marcado como seguro y el
valor real no se versiona.

---

## Capa gratuita, créditos y costo

Para esta pieza **no se asume una capa gratuita permanente propia de MySQL
Flexible Server**.

Durante S8 la instancia se utilizó dentro de la suscripción académica disponible
para el equipo.

Configuración observada:

```text
Standard_B1ms
32 GiB
Alta disponibilidad: No
```

Durante la configuración se observó una estimación aproximada de:

```text
USD 14.71 / mes
```

antes de aplicar créditos o beneficios académicos.

Por tanto se diferencia explícitamente:

```text
Precio estimado del recurso: ~USD 14.71/mes
Pago directo observado durante S8: cubierto por el beneficio/crédito académico disponible
Tarjeta bancaria personal requerida para la evidencia utilizada: No
```

No se declara el servicio como permanentemente gratuito.

---

## Supuestos de carga

La elección se basa en un prototipo académico con:

- tres integrantes;
- concurrencia baja;
- pocas publicaciones;
- una sola API;
- una única base de datos;
- sin alta disponibilidad;
- sin procesamiento masivo;
- 32 GiB como almacenamiento configurado.

No existe evidencia que justifique actualmente un SKU superior.

---

## Punto de ruptura

El beneficio económico actual se rompe cuando:

- se agoten o finalicen los créditos académicos;
- se mantenga el servidor activo fuera del periodo cubierto;
- se requiera aumentar el SKU;
- se requiera almacenamiento superior;
- se habilite alta disponibilidad;
- se creen réplicas o nuevos servidores;
- el volumen real haga insuficiente `Standard_B1ms`.

En ausencia de créditos, la referencia observada durante S8 para la
configuración actual es aproximadamente:

```text
USD 14.71 / mes
```

Por ello, antes de mantener este recurso de manera permanente debe realizarse
una nueva estimación de costos.

---

## Seguridad

Las credenciales reales no se encuentran en el repositorio.

Se suministran mediante:

- parámetros seguros Bicep;
- App Settings del Backend API;
- variables de entorno.

La comunicación backend → MySQL utiliza TLS.

El frontend no tiene acceso directo a la base de datos.

---

## Verificación realizada

Durante S8 se comprobó:

- disponibilidad real del servidor MySQL;
- conexión desde FastAPI;
- `/health` HTTP 200 con MySQL disponible;
- `/health` HTTP 503 con la dependencia detenida;
- recuperación posterior HTTP 200;
- creación real de publicaciones;
- consulta posterior de publicaciones;
- funcionamiento desde Flutter Web público;
- conexión TLS;
- validación de Bicep.

La publicación creada desde la interfaz confirmó el recorrido:

```text
GitHub Pages
→ Flutter
→ FastAPI
→ repository
→ PyMySQL
→ Azure MySQL
```

---

## Reproducción

La definición principal del recurso se encuentra en:

```text
infra/main.bicep
```

Validación:

```bash
az bicep build --file infra/main.bicep
```

y:

```bash
az deployment group validate \
  --resource-group rg-campusmarket-s8 \
  --template-file infra/main.bicep \
  --parameters mysqlAdministratorPassword="<VALOR_SEGURO>"
```

La contraseña real nunca debe incluirse en el repositorio.

---

## Rollback y contingencia

La aplicación mantiene la tecnología MySQL definida por ADR-0004.

Si la instancia actual falla o debe reemplazarse:

```text
1. provisionar una instancia MySQL compatible mediante la infraestructura
   versionada;
2. recrear la base `campusmarket`;
3. restaurar los datos disponibles cuando corresponda;
4. actualizar las variables CAMPUSMARKET_DB_* del Backend API;
5. verificar TLS;
6. ejecutar /health;
7. ejecutar GET /publicaciones;
8. ejecutar POST /publicaciones.
```

Si el costo del servicio deja de ser aceptable, la alternativa de contingencia
es desplegar MySQL en infraestructura académica disponible y conservar la misma
interfaz repository → MySQL.

La aplicación no debe modificarse para acceder directamente a otra tecnología
sin una nueva decisión arquitectónica.

---

## Consecuencias positivas

- persistencia MySQL administrada;
- separación entre aplicación y base de datos;
- infraestructura reproducible;
- TLS;
- secretos externos al código;
- compatibilidad con PyMySQL;
- conserva ADR-0004 y la propiedad única de datos.

---

## Consecuencias negativas

- costo potencial mensual;
- dependencia de Azure;
- dependencia temporal de créditos académicos para mantener bajo el costo;
- mayor configuración de red respecto a una base local;
- debe revisarse el costo si aumenta la carga.

---

## Relación con decisiones anteriores

ADR-0004 continúa siendo la decisión que define **MySQL como tecnología de
persistencia**.

ADR-0008 define exclusivamente **dónde se ejecuta MySQL en el entorno S8**.

ADR-0005 queda refinado por este ADR para la decisión específica de
persistencia.

---

## Evidencia relacionada

- `infra/main.bicep`
- `backend/app/publicaciones/repository.py`
- `backend/tests/test_health.py`
- `backend/tests/test_publicaciones_vertical.py`
- `docs/arc42/07-vista-despliegue.md`
- `docs/arc42/02-restricciones.md`
- `docs/evidencias/evidencia-s8-2026-09-27.md`
- `README.md`
