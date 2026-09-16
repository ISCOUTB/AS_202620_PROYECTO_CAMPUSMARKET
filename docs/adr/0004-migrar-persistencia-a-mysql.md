# ADR-0004 - Migrar la persistencia de SQLite a MySQL

## Estado

Aceptado

## Fecha

2026-09-16

## Contexto

Durante el primer corte de CampusMarket se utilizo SQLite como mecanismo de
persistencia del corte vertical.

SQLite fue adecuado para esa etapa inicial porque permitia mantener una
infraestructura minima y demostrar el funcionamiento del prototipo.

Posteriormente, durante la revision del proyecto, el docente realizo la
observacion de que la persistencia debia evolucionar de SQLite hacia MySQL.

Por esta razon, la migracion no corresponde solamente a una preferencia
tecnologica del equipo. Es una correccion arquitectonica realizada a partir de
la retroalimentacion recibida durante la revision del proyecto.

La correccion debe aplicarse conservando las decisiones arquitectonicas que ya
se encuentran vigentes:

- mantener el monolito modular;
- conservar Gestion de Publicaciones como propietario de sus datos;
- evitar accesos directos a la persistencia desde otras capas;
- mantener la direccion router -> service -> repository;
- conservar la API HTTP/JSON existente;
- mantener las pruebas automatizadas.

## Problema

La arquitectura del primer corte utilizaba:

```text
Flutter
  |
  v
FastAPI
  |
  v
Gestion de Publicaciones
  |
  v
SQLite
````

Despues de la observacion del docente, mantener SQLite como persistencia
vigente habria generado una inconsistencia entre:

* la correccion solicitada;
* el codigo;
* los diagramas C4;
* arc42;
* las pruebas;
* la arquitectura presentada por el equipo.

Era necesario sustituir SQLite por MySQL sin modificar innecesariamente las
fronteras del sistema.

## Decision

CampusMarket utilizara MySQL como tecnologia de persistencia vigente.

El acceso desde el Backend API se realizara mediante PyMySQL.

La dependencia tecnologica permanece encapsulada en:

`backend/app/publicaciones/repository.py`

La direccion interna es:

```text
router
  |
  v
service
  |
  v
repository
  |
  v
PyMySQL
  |
  v
MySQL
```

El frontend no accede directamente a MySQL.

Gestion de Publicaciones continua siendo el unico contexto con autoridad de
escritura sobre la tabla:

`publicaciones`

La configuracion de conexion se proporciona mediante variables de entorno.

Las credenciales de acceso no se almacenan en el repositorio.

## Justificacion

La decision responde directamente a la observacion del docente de sustituir
SQLite por MySQL para la evolucion del proyecto.

El cambio se realiza sin modificar:

* el monolito modular;
* las fronteras de dominio;
* la propiedad de datos;
* la separacion router / service / repository;
* el contrato HTTP/JSON entre Flutter y FastAPI;
* la estrategia API-first documentada en S7.

Se modifica principalmente:

* el motor de persistencia;
* el driver de acceso;
* la configuracion de conexion;
* las pruebas de integracion;
* la documentacion asociada.

## Consecuencias positivas

* Se atiende la observacion realizada por el docente.
* La documentacion queda alineada con la implementacion vigente.
* MySQL permanece aislado detras del repositorio.
* Router y Service no dependen directamente del motor de base de datos.
* Se conserva el propietario unico de los datos.
* La integracion real con MySQL puede verificarse automaticamente.

## Consecuencias negativas

* El entorno de desarrollo requiere una instancia MySQL disponible.
* Las pruebas de integracion necesitan una base de datos.
* El pipeline de integracion continua debe disponer de MySQL.
* La configuracion operativa es mayor que con una base SQLite embebida.

## Alternativas consideradas

### Mantener SQLite

No se adopta como solucion vigente.

SQLite se conserva como parte de la historia arquitectonica del primer corte.

Mantenerlo como tecnologia actual habria contradicho la observacion recibida.

### Dividir el backend en microservicios

No se adopta.

La observacion requiere modificar la persistencia, no cambiar el estilo
arquitectonico del sistema.

### MySQL encapsulado mediante Repository

Se adopta.

Permite realizar la migracion conservando las fronteras arquitectonicas ya
definidas.

## Relacion con ADR anteriores

### ADR-0001 - Monolito modular

Continua vigente.

La migracion no modifica los contextos:

* usuarios;
* publicaciones;
* catalogo;
* administracion.

### ADR-0002 - Manejo de bloqueo temporal de SQLite

Se conserva como decision historica correspondiente al primer corte.

Las referencias a SQLITE_BUSY, SQLITE_LOCKED y las mediciones realizadas con
SQLite no describen la persistencia vigente.

### ADR-0003 - Integracion sincrona HTTP/JSON

Continua vigente.

La migracion de persistencia no modifica la comunicacion entre Flutter y
FastAPI.

## Implementacion

La decision se materializa principalmente en:

* `backend/app/publicaciones/repository.py`;
* `backend/requirements.txt`;
* `.gitignore`;
* configuracion mediante variables de entorno;
* MySQL como motor de persistencia;
* PyMySQL como driver.

El flujo vigente es:

```text
Flutter
  |
  | HTTP/JSON
  v
FastAPI
  |
  v
router
  |
  v
service
  |
  v
repository
  |
  | PyMySQL
  v
MySQL
```

## Verificacion

La migracion se verifica mediante:

`backend/tests/test_publicaciones_vertical.py`

que comprueba:

* creacion de una publicacion;
* respuesta HTTP 201;
* persistencia en MySQL;
* recuperacion posterior;
* respuesta controlada cuando la persistencia no esta disponible.

Tambien se verifica mediante:

`backend/tests/test_modularidad_s6.py`

que comprueba:

* Gestion de Publicaciones mantiene el unico escritor productivo;
* otros contextos no escriben directamente sobre `publicaciones`;
* la direccion interna se mantiene como
  router -> service -> repository -> MySQL.

El contrato HTTP se verifica independientemente mediante:

`backend/tests/test_contrato_openapi.py`

contra:

`contracts/openapi-v1.json`

## Trazabilidad

Esta decision debe mantenerse alineada con:

* `docs/arc42/ARC42.md`;
* `docs/arc42/03-contexto.md`;
* `docs/arc42/05-bloques-de-construccion.md`;
* `docs/arc42/06-vista-ejecucion.md`;
* `docs/arc42/08-conceptos-transversales.md`;
* `docs/arc42/09-decisiones.md`;
* `docs/aspectos.md`;
* `docs/c4/02-contenedores.md`;
* `docs/c4/02-contenedores.puml`;
* `docs/c4/03-componentes-backend.md`;
* `docs/c4/03-componentes-backend.puml`.

## Resultado

La observacion del docente se atiende sustituyendo SQLite por MySQL sin alterar
innecesariamente la arquitectura general de CampusMarket.

La arquitectura vigente queda:

```text
Flutter
  |
  | HTTP/JSON sincrono
  v
FastAPI
  |
  v
Gestion de Publicaciones
  |
  | PyMySQL
  v
MySQL
```

SQLite se conserva unicamente como parte de la trazabilidad historica del
primer corte.


