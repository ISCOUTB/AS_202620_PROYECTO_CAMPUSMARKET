
# 3. Contexto y alcance

Esta sección describe el contexto actual de CampusMarket, los actores externos,
el alcance funcional y las interfaces que delimitan el sistema.

## 3.1 Contexto del sistema

CampusMarket es un marketplace universitario orientado a centralizar la
publicación, consulta y búsqueda de productos dentro de la comunidad
universitaria.

Los actores externos principales son:

- **Estudiante:** utiliza CampusMarket para publicar y consultar productos.
- **Administrador:** participa en la supervisión de publicaciones y contenido.

El contexto del sistema está representado en el C4 Nivel 1:

[C4 Nivel 1 - Contexto](../c4/01-contexto.md)

Fuente versionada del diagrama:

[`01-contexto.puml`](../c4/01-contexto.puml)

---

## 3.2 Alcance funcional

CampusMarket contempla como capacidades objetivo del sistema:

- gestión de publicaciones de productos;
- consulta y búsqueda de productos;
- modalidades de venta y alquiler;
- gestión básica de usuarios;
- supervisión de publicaciones.

No todas las capacidades del alcance objetivo se encuentran materializadas
actualmente.

El corte vertical implementado y verificable se concentra principalmente en:

- creación de publicaciones;
- consulta de publicaciones;
- persistencia de publicaciones;
- comunicación HTTP/JSON entre frontend y backend.

Actualmente no forman parte del alcance:

- pagos electrónicos;
- procesamiento bancario;
- servicios de envío;
- logística de entrega;
- integraciones con empresas de transporte.

Estas exclusiones permiten mantener el alcance del prototipo compatible con las
restricciones del proyecto.

---

## 3.3 Interfaces externas

En el estado actual del prototipo:

- el frontend se ejecuta mediante **Flutter Web**;
- el frontend se comunica con el backend mediante **HTTP/JSON REST**;
- la interacción Frontend → Backend es actualmente **síncrona**;
- el backend utiliza **FastAPI / Python**;
- la persistencia vigente utiliza **MySQL**;
- el acceso a MySQL desde el backend se realiza mediante **PyMySQL**.

El frontend no accede directamente a la persistencia.

El recorrido actualmente implementado es:

```text
Flutter Web
    ↓ HTTP/JSON síncrono
Backend API FastAPI
    ↓
Gestión de Publicaciones
    ↓ PyMySQL / SQL
MySQL
````

En desarrollo local:

* Frontend: `http://localhost:3000`
* Backend: `http://localhost:8000`
* Base de datos: `campusmarket`

La tabla actualmente materializada para el contexto Gestión de Publicaciones es:

`publicaciones`

La persistencia productiva se encuentra encapsulada en:

`backend/app/publicaciones/repository.py`

Las credenciales de base de datos no se versionan en el repositorio. La
configuración del entorno se suministra mediante variables de entorno.

---

## 3.4 Contrato de API

La comunicación entre el frontend y el Backend API se define mediante un
contrato **OpenAPI** versionado.

El contrato se encuentra en:

`contracts/openapi-v1.json`

Los endpoints actualmente materializados incluyen:

* `POST /publicaciones`;
* `GET /publicaciones`;
* `GET /health`.

La integración implementada es síncrona:

```text
Cliente
   ↓ solicitud HTTP
Backend API
   ↓ procesamiento
Cliente
   ↑ respuesta HTTP
```

La implementación del proveedor se verifica mediante pruebas automatizadas de
contrato, evitando depender únicamente de una inspección manual de la
especificación.

---

## 3.5 Persistencia vigente e historia arquitectónica

La tecnología de persistencia vigente de CampusMarket es **MySQL**.

El acceso productivo a los datos del contexto Gestión de Publicaciones se
realiza exclusivamente desde su repositorio mediante **PyMySQL**.

SQLite fue utilizado durante el primer corte del proyecto y formó parte de la
respuesta arquitectónica documentada en ese momento.

Las referencias a SQLite que permanecen en:

* ADR-0002;
* evidencias de medición;
* documentación histórica del primer corte;

se conservan como trazabilidad de decisiones anteriores y no representan la
persistencia vigente.

---

## 3.6 Seguridad de transporte

Durante el desarrollo local se utiliza HTTP.

La comunicación mediante **HTTPS** corresponde a un despliegue externo y debe
utilizarse cuando CampusMarket sea expuesto fuera del entorno local.

No se documenta un proveedor cloud como implementado mientras no exista
evidencia verificable de dicho despliegue.

Actualmente no existen integraciones implementadas con sistemas externos de:

* pagos;
* banca;
* transporte;
* logística.

---

## 3.7 Relación con los diagramas C4

El **C4 Nivel 1** representa CampusMarket como un único sistema e identifica a
sus actores externos.

El **C4 Nivel 2** muestra los contenedores actuales:

* **Frontend:** Flutter / Dart;
* **Backend API:** FastAPI / Python;
* **Persistencia:** MySQL.

El **C4 Nivel 3** amplía el Backend API y muestra la estructura interna
actualmente verificable del contexto Gestión de Publicaciones:

```text
API de Publicaciones
        ↓
Servicio de Publicaciones
        ↓
Repositorio de Publicaciones
        ↓
MySQL
```

Los actores externos definidos en el Nivel 1 se mantienen conectados a través
del frontend en el Nivel 2.

Documentación:

* [C4 Nivel 1 - Contexto](../c4/01-contexto.md)
* [C4 Nivel 2 - Contenedores](../c4/02-contenedores.md)
* [C4 Nivel 3 - Componentes del Backend](../c4/03-componentes-backend.md)

Fuentes versionadas:

* [`01-contexto.puml`](../c4/01-contexto.puml)
* [`02-contenedores.puml`](../c4/02-contenedores.puml)
* [`03-componentes-backend.puml`](../c4/03-componentes-backend.puml)
