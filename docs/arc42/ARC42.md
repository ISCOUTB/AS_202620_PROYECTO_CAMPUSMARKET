
# CampusMarket - Documentación arc42

## 1. Introducción y objetivos

### 1.1 Descripción del sistema

CampusMarket es una plataforma orientada a estudiantes universitarios que busca
facilitar la publicación, búsqueda, venta y alquiler de productos nuevos o
usados dentro de la comunidad estudiantil.

La idea surge debido a que muchos estudiantes ofrecen productos mediante grupos
de WhatsApp, redes sociales u otros medios informales, donde las publicaciones
pueden perderse fácilmente y no existe una forma centralizada y organizada de
consultar los artículos disponibles.

CampusMarket busca centralizar estas publicaciones en una plataforma donde los
estudiantes puedan encontrar y ofrecer productos de manera organizada,
manteniendo un alcance adecuado para el desarrollo académico durante el
semestre.

La interfaz se desarrolla con Flutter, utilizando inicialmente su capacidad Web
y manteniendo la posibilidad de extender el mismo frontend a Android e iOS en
etapas posteriores.

---

### 1.2 Objetivos de negocio e interesados

Los objetivos de negocio de CampusMarket se orientan a mejorar la forma en que
los estudiantes universitarios ofrecen y encuentran productos dentro de su
comunidad.

| ID | Objetivo de negocio | Interesado principal |
|---|---|---|
| ON-01 | Centralizar en una sola plataforma las publicaciones de productos que actualmente se encuentran dispersas en grupos de WhatsApp, redes sociales y otros medios informales. | Estudiantes universitarios |
| ON-02 | Facilitar que los estudiantes encuentren productos disponibles para compra o alquiler dentro de la comunidad universitaria. | Estudiantes compradores o arrendatarios |
| ON-03 | Dar mayor visibilidad a los productos que los estudiantes desean vender o alquilar mediante publicaciones organizadas y consultables. | Estudiantes vendedores o propietarios |
| ON-04 | Mantener un entorno controlado para las publicaciones y apoyar la supervisión del contenido disponible en la plataforma. | Administrador de CampusMarket |

---

### 1.3 Objetivos de calidad

Los principales atributos de calidad considerados para CampusMarket son los
siguientes.

#### Mantenibilidad

La aplicación debe estar organizada de forma que sea posible modificar o
agregar funcionalidades sin afectar innecesariamente partes del sistema que no
estén relacionadas con el cambio.

Este objetivo se desarrolla mediante el escenario de calidad
**EC-03 - Modificación del sistema**.

#### Seguridad

Un estudiante solamente podrá modificar o eliminar las publicaciones que le
pertenecen.

Los intentos de modificación realizados por usuarios que no sean propietarios
deberán ser rechazados.

Este objetivo se desarrolla mediante el escenario
**EC-02 - Protección de publicaciones**.

#### Rendimiento

Las funciones principales de consulta y búsqueda deben responder en tiempos
adecuados durante la operación normal del sistema.

Este objetivo se desarrolla mediante el escenario
**EC-01 - Consulta de productos**.

#### Disponibilidad y recuperación

En caso de una falla durante una prueba o demostración, el equipo debe poder
recuperar el funcionamiento del prototipo en un tiempo controlado y sin perder
la información almacenada correctamente antes de la falla.

Este objetivo se desarrolla mediante el escenario
**EC-04 - Recuperación del prototipo**.

Los escenarios completos y sus medidas verificables se encuentran en:

[10-escenarios-de-calidad.md](./10-escenarios-de-calidad.md)

El árbol de utilidad y su priorización se encuentran en:

[10-arbol-de-utilidad.md](./10-arbol-de-utilidad.md)

---

## 2. Restricciones

Las restricciones de CampusMarket delimitan el espacio de solución y
condicionan las decisiones arquitectónicas que puede tomar el equipo.

### R-01. Tiempo de desarrollo

**Tipo:** Organizativa  
**Origen:** Asignatura / calendario académico

CampusMarket debe alcanzar un prototipo funcional dentro del semestre
académico.

**Justificación:** El proyecto se desarrolla de manera incremental durante el
curso y debe producir un sistema funcional y verificable dentro del periodo
establecido. Esta condición limita el alcance y la complejidad que puede asumir
el equipo.

---

### R-02. Tamaño del equipo

**Tipo:** Organizativa  
**Origen:** Conformación del equipo

CampusMarket será desarrollado por un equipo de tres integrantes.

**Justificación:** La capacidad de desarrollo disponible está limitada al
trabajo de tres integrantes durante el semestre. Las decisiones arquitectónicas
y el alcance deben ser compatibles con los recursos humanos disponibles.

---

### R-03. Repositorio y control de versiones

**Tipo:** Técnica / organizativa  
**Origen:** Metodología de trabajo del curso

El código fuente, la documentación arquitectónica y las evidencias incrementales
de CampusMarket deberán mantenerse versionados en el repositorio del proyecto.

**Justificación:** El repositorio constituye el punto de referencia para
verificar la evolución del sistema y mantener trazabilidad entre documentación,
implementación y evidencias.

---

### R-04. Análisis de calidad del código

**Tipo:** Técnica  
**Origen:** Herramientas de calidad utilizadas en el proyecto

El repositorio de CampusMarket deberá mantenerse integrado con SonarQube Cloud
durante el desarrollo.

**Justificación:** La integración permite analizar de manera continua
características relacionadas con la calidad del código y obtener evidencia
verificable sobre los problemas detectados.

---

### R-05. Alcance funcional del prototipo

**Tipo:** Organizativa / alcance  
**Origen:** Alcance definido por el equipo

La versión inicial de CampusMarket no incluirá pagos en línea, procesamiento
bancario, servicios de envío ni logística de entrega.

**Justificación:** Estas funcionalidades requieren integraciones externas y
aumentan considerablemente la complejidad técnica y operativa del sistema.
Excluirlas permite concentrar el esfuerzo en las capacidades principales del
marketplace.

---

### R-06. Plataforma de ejecución inicial

**Tipo:** Técnica  
**Origen:** Alcance tecnológico inicial

CampusMarket será desarrollado inicialmente como una aplicación accesible desde
navegadores modernos mediante Flutter Web.

La tecnología seleccionada permitirá reutilizar la base de código del frontend
para una posible ejecución posterior en Android e iOS.

**Justificación:** Mantener Web como plataforma inicial permite controlar el
alcance del prototipo durante el semestre, mientras que Flutter ofrece la
posibilidad de extender posteriormente la solución a dispositivos móviles sin
mantener aplicaciones completamente independientes.

El detalle completo de las restricciones se encuentra en:

[02-restricciones.md](./02-restricciones.md)

---

## 3. Contexto y alcance

### 3.1 Contexto del sistema

CampusMarket tiene como principales actores a los estudiantes universitarios y
al administrador de la plataforma.

Dentro del alcance objetivo, los estudiantes utilizarán el sistema para
registrarse, iniciar sesión, publicar productos, consultar el catálogo,
realizar búsquedas y filtros y administrar sus propias publicaciones.

El administrador utilizará CampusMarket para supervisar las publicaciones y
apoyar la gestión general del contenido de la plataforma.

La materialización actual del prototipo se concentra principalmente en la
capacidad de **Gestión de Publicaciones**.

---

### 3.2 Alcance funcional

El alcance objetivo de CampusMarket incluye:

- gestión básica de usuarios;
- registro e inicio de sesión;
- gestión de publicaciones de productos;
- consulta del catálogo;
- búsqueda y filtrado de productos;
- clasificación del estado de los productos;
- publicaciones para venta o alquiler;
- edición y eliminación de publicaciones propias;
- consulta de información para contactar al propietario del producto;
- supervisión básica de publicaciones por parte del administrador.

No hacen parte del alcance inicial:

- pagos electrónicos;
- procesamiento bancario;
- servicios de envío;
- logística de entrega;
- integración con empresas de transporte.

No todas las capacidades del alcance objetivo están materializadas actualmente.

El corte vertical implementado se concentra principalmente en la creación y
consulta de publicaciones.

---

### 3.3 Interfaces externas

En el estado actual del prototipo, los estudiantes acceden a CampusMarket
mediante una interfaz desarrollada con **Flutter Web**.

El frontend se comunica con el backend mediante una **API REST sobre
HTTP/JSON**.

La integración actualmente materializada es **síncrona**: cada solicitud HTTP
realizada por el frontend recibe su respuesta dentro de la misma interacción.

Durante el desarrollo local, Flutter Web se ejecuta en:

`localhost:3000`

y el backend FastAPI en:

`localhost:8000`

El backend está implementado con **FastAPI y Python** y es responsable de:

- recibir solicitudes HTTP;
- validar los datos de entrada;
- ejecutar la lógica de aplicación;
- coordinar el acceso a la persistencia;
- devolver respuestas HTTP/JSON al cliente.

El contrato de integración se documenta mediante **OpenAPI** y se mantiene
versionado en:

`contracts/openapi-v1.json`

Los endpoints actualmente materializados para publicaciones incluyen:

- `POST /publicaciones`;
- `GET /publicaciones`.

También se expone:

- `GET /health`.

CampusMarket utiliza actualmente **MySQL** como mecanismo de persistencia para
el corte vertical materializado.

El acceso a MySQL se realiza desde Python mediante **PyMySQL**.

El frontend no accede directamente a la persistencia.

El recorrido implementado mantiene la separación:

```text
Flutter Web
    ↓ HTTP/JSON síncrono
FastAPI
    ↓
Gestión de Publicaciones
    ↓
MySQL
````

La persistencia productiva de publicaciones se encuentra encapsulada en:

`backend/app/publicaciones/repository.py`

La base de datos utilizada por el entorno actual se denomina:

`campusmarket`

y la entidad actualmente materializada se persiste en la tabla:

`publicaciones`

Las credenciales de acceso no forman parte del repositorio. La configuración
local se proporciona mediante variables de entorno y el archivo `.env` se
mantiene excluido mediante `.gitignore`.

SQLite fue utilizado durante el primer corte y se conserva únicamente como
parte de la evidencia histórica y de las decisiones arquitectónicas
correspondientes a ese momento del proyecto.

Cuando el prototipo sea desplegado en un entorno accesible externamente, la
comunicación entre clientes y CampusMarket deberá realizarse mediante
**HTTPS**.

En el alcance actual no se contemplan integraciones con sistemas bancarios,
plataformas de pago, empresas de transporte ni servicios externos de logística.

---

### 3.4 Diagrama de contexto

El diagrama C4 de contexto identifica a CampusMarket, sus usuarios principales
y las relaciones existentes entre ellos.

El diagrama se encuentra documentado en:

[01-contexto.md](../c4/01-contexto.md)

---

## 4. Estrategia de solución

La estrategia arquitectónica de CampusMarket se basa en la evaluación de:

* arquitectura en capas;
* arquitectura hexagonal;
* monolito modular.

Estas alternativas fueron contrastadas frente a los escenarios de calidad
priorizados por el equipo.

Como resultado de la comparación, se seleccionó un **monolito modular** como
estrategia arquitectónica inicial, buscando equilibrar mantenibilidad,
simplicidad operativa y capacidad de evolución dentro de las restricciones
actuales del proyecto.

El monolito modular se aplica principalmente al backend de CampusMarket, que se
organiza mediante módulos correspondientes a capacidades principales del
negocio:

* `usuarios`;
* `publicaciones`;
* `catalogo`;
* `administracion`.

Estos módulos deben mantener responsabilidades y fronteras explícitas, evitando
dependencias innecesarias entre sus componentes internos.

Durante S6 estas capacidades se formalizaron además como contextos delimitados:

* **Gestión de Usuarios**;
* **Gestión de Publicaciones**;
* **Catálogo**;
* **Administración**.

La capacidad actualmente materializada con mayor profundidad es
**Gestión de Publicaciones**.

Durante S7 se refuerza además una estrategia **API-first**, donde la
comunicación entre cliente y proveedor se define mediante un contrato OpenAPI
versionado y verificable automáticamente.

El detalle de la comparación entre estilos, las tácticas arquitectónicas
seleccionadas, sus costos y las consecuencias de la decisión se encuentra en:

[04-estrategia-de-solucion.md](./04-estrategia-de-solucion.md)

La decisión se registra formalmente en:

[ADR-0001 - Adoptar un monolito modular para CampusMarket](../adr/0001-usar-monolito-modular.md)

El escenario de calidad que motiva principalmente esta decisión es:

[EC-03 - Modificación del sistema](./10-escenarios-de-calidad.md#ec-03---modificación-del-sistema)

---

## 5. Bloques de construcción

La documentación detallada de los bloques de construcción se mantiene en:

[05-bloques-de-construccion.md](./05-bloques-de-construccion.md)

La estructura ejecutable principal corresponde a:

```text
Frontend Web
    ↓ HTTP/JSON
Backend API
    ↓ PyMySQL / SQL
MySQL
```

La estructura interna materializada del Backend API corresponde a:

```text
API de Publicaciones
        ↓
Servicio de Publicaciones
        ↓
Repositorio de Publicaciones
        ↓
MySQL
```

La dirección de dependencias mantiene separados los componentes responsables de
interfaz HTTP, lógica de aplicación y persistencia.

El repositorio de Publicaciones constituye el único componente productivo que
accede directamente a la tabla `publicaciones`.

El detalle de componentes, propiedad de datos y reglas de dependencia se
encuentra en la sección 5 específica.

---

## 6. Vista de ejecución

Los escenarios de ejecución del sistema se documentan en:

[06-vista-ejecucion.md](./06-vista-ejecucion.md)

La ejecución principal actualmente materializada conserva el recorrido:

```text
Flutter Web
    ↓ HTTP/JSON síncrono
FastAPI
    ↓
router.py
    ↓
service.py
    ↓
repository.py
    ↓ PyMySQL / SQL
MySQL
```

Para la creación de una publicación, el flujo principal es:

```text
Frontend
   ↓ POST /publicaciones
Router
   ↓
Service
   ↓
Repository
   ↓ INSERT
MySQL
   ↓
Repository
   ↓
Service
   ↓
Router
   ↓ HTTP 201
Frontend
```

Para la consulta de publicaciones:

```text
Frontend
   ↓ GET /publicaciones
Router
   ↓
Service
   ↓
Repository
   ↓ SELECT
MySQL
   ↓
Repository
   ↓
Service
   ↓
Router
   ↓ HTTP 200
Frontend
```

La vista de ejecución también documenta los comportamientos verificables
relacionados con indisponibilidad temporal de la persistencia.

Ante una condición en la que MySQL no pueda ser alcanzado, la capa de
persistencia traduce el error técnico a una condición controlada y la API
responde con:

`503 Service Unavailable`

La correspondencia entre proveedor e interfaz se protege mediante el contrato
OpenAPI `1.0.0` y pruebas automatizadas.

---

## 7. Vista de despliegue

El estado actual se ejecuta principalmente en un entorno local de desarrollo:

```text
Navegador
   ↓
Flutter Web
   ↓ HTTP/JSON
FastAPI
   ↓ TCP / SQL
MySQL
```

La configuración local utiliza:

* Flutter Web como cliente;
* FastAPI como backend;
* MySQL como persistencia;
* variables de entorno para la configuración de conexión.

Para un despliegue externo, la arquitectura prevista conserva los mismos
límites lógicos:

```text
Cliente Web
   ↓ HTTPS
Frontend
   ↓ HTTPS / JSON
Backend FastAPI
   ↓ conexión segura de base de datos
MySQL
```

La selección definitiva del proveedor cloud se mantiene como una decisión de
despliegue pendiente mientras no exista evidencia de un entorno productivo
implementado.

---

## 8. Conceptos transversales

Durante S6 se formalizaron los conceptos de dominio y las reglas de modularidad
necesarias para mantener coherente la evolución del monolito modular.

La documentación completa se encuentra en:

[08-conceptos-transversales.md](./08-conceptos-transversales.md)

Esta sección contiene:

* lenguaje ubicuo;
* contextos delimitados;
* mapa de contextos;
* relaciones entre contextos;
* propiedad única de datos;
* reglas de comunicación entre módulos;
* correspondencia con el estado actual del código;
* relación con C4 Nivel 3;
* verificación automática de modularidad.

Los contextos delimitados definidos para CampusMarket son:

* **Gestión de Usuarios**;
* **Gestión de Publicaciones**;
* **Catálogo**;
* **Administración**.

La regla central de propiedad adoptada es:

> Cada dato de dominio tiene un único módulo responsable de escribirlo.

En el estado actual, la entidad persistida de dominio materializada es:

`publicaciones`

y su propietario es:

**Gestión de Publicaciones**

La escritura productiva se encuentra encapsulada en:

`backend/app/publicaciones/repository.py`

La tecnología de persistencia vigente es **MySQL**, accedida mediante
**PyMySQL**.

---

### 8.1 Mapa de contextos

El mapa de contextos y sus relaciones tipadas se encuentran documentados en:

[08-conceptos-transversales.md](./08-conceptos-transversales.md#83-mapa-de-contextos)

Las relaciones definidas incluyen:

* Gestión de Usuarios → Gestión de Publicaciones:
  **Customer/Supplier**;
* Gestión de Publicaciones → Catálogo:
  **Customer/Supplier**;
* Gestión de Publicaciones → Administración:
  contrato explícito y **Anticorruption Layer** en Administración.

Actualmente no se adopta un **Shared Kernel** entre los contextos.

---

### 8.2 Propiedad y auditoría de datos

La tabla módulo → datos → propietario se encuentra documentada en:

[08-conceptos-transversales.md](./08-conceptos-transversales.md#84-propiedad-de-datos)

La evidencia fue contrastada contra el código mediante:

[Auditoría de modularidad S6](../evidencias/auditoria-modularidad-s6-2026-09-12.md)

La auditoría determinó que no existen actualmente dos contextos de dominio
escribiendo directamente la entidad `publicaciones`.

Los riesgos de evolución y sus planes preventivos se mantienen documentados en
la misma evidencia.

---

### 8.3 C4 Nivel 3

La materialización interna actual del Backend API se encuentra documentada en:

[C4 Nivel 3 - Componentes del Backend](../c4/03-componentes-backend.md)

Fuente PlantUML:

[03-componentes-backend.puml](../c4/03-componentes-backend.puml)

El Nivel 3 amplía el contenedor Backend API sin modificar los límites
principales del monolito modular.

La descomposición actualmente verificable es:

```text
API de Publicaciones
        ↓
Servicio de Publicaciones
        ↓
Repositorio de Publicaciones
        ↓
MySQL
```

Los límites de Usuarios, Catálogo y Administración se mantienen documentados,
pero no se presentan como funcionalidades ya materializadas.

---

### 8.4 Verificación automática

Las reglas principales de modularidad se verifican adicionalmente mediante:

[`test_modularidad_s6.py`](../../backend/tests/test_modularidad_s6.py)

La prueba comprueba que:

* `publicaciones` tenga un único escritor productivo;
* otros contextos no accedan directamente a la tecnología de persistencia;
* otros contextos no dependan directamente del repositorio interno de
  Publicaciones;
* la dirección interna permanezca:

  `router → service → repository → MySQL`.

La integración de persistencia se verifica mediante:

[`test_publicaciones_vertical.py`](../../backend/tests/test_publicaciones_vertical.py)

Estas pruebas comprueban:

* creación de una publicación mediante la API;
* recuperación posterior de la publicación;
* persistencia real en MySQL;
* degradación controlada mediante HTTP `503` cuando la persistencia no está
  disponible.

Las pruebas del backend se ejecutan mediante `pytest`.

---

### 8.5 Contrato de API

Durante S7 se formaliza la comunicación API-first entre frontend y backend.

El contrato versionado se mantiene en:

`contracts/openapi-v1.json`

FastAPI expone su implementación mediante los endpoints actualmente
materializados.

La prueba:

[`test_contrato_openapi.py`](../../backend/tests/test_contrato_openapi.py)

verifica automáticamente la correspondencia entre la implementación y el
contrato OpenAPI.

La integración actualmente implementada utiliza comunicación síncrona
HTTP/JSON.

---

### 8.6 Trazabilidad

La correspondencia entre aspectos, contextos, propiedad de datos, contratos,
código, auditoría y pruebas se mantiene en:

[docs/aspectos.md](../aspectos.md)

La cadena de trazabilidad vigente puede representarse como:

```text
Aspecto arquitectónico
   ↓
Contexto delimitado
   ↓
Propietario del dato
   ↓
C4 Nivel 2 / C4 Nivel 3
   ↓
Contrato OpenAPI
   ↓
Código
   ↓
Prueba automática
   ↓
Evidencia
```

---

### 8.7 Coherencia con ADR-0001

Los límites establecidos previamente por:

[ADR-0001 - Monolito modular](../adr/0001-usar-monolito-modular.md)

se mantienen:

* `usuarios`;
* `publicaciones`;
* `catalogo`;
* `administracion`.

Estos límites no han sido:

* fusionados;
* divididos;
* reemplazados;
* convertidos en microservicios.

La incorporación del C4 Nivel 3 hace explícita la estructura interna actual del
Backend API.

La migración de SQLite a MySQL modifica la tecnología de persistencia, pero no
modifica los límites funcionales del monolito modular.

---

## 9. Decisiones arquitectónicas

Las decisiones arquitectónicas se encuentran documentadas mediante ADR.

Actualmente:

* [ADR-0001 - Monolito modular](../adr/0001-usar-monolito-modular.md)
* [ADR-0002 - Manejo de bloqueo temporal de SQLite](../adr/0002-manejo-bloqueo-sqlite.md)
* [ADR-0003 - Integración síncrona HTTP/JSON](../adr/0003-usar-integracion-sincrona-http-json.md)

ADR-0002 corresponde a una decisión tomada durante el primer corte cuando
SQLite era la tecnología de persistencia vigente.

La migración posterior a MySQL debe registrarse mediante un ADR independiente,
manteniendo ADR-0002 como evidencia histórica y evitando reescribir una decisión
pasada.

El detalle de las decisiones y su relación con arc42 se mantiene en:

[09-decisiones.md](./09-decisiones.md)

---

## 10. Escenarios de calidad

Los escenarios de calidad medibles se encuentran en:

[10-escenarios-de-calidad.md](./10-escenarios-de-calidad.md)

El árbol de utilidad se encuentra en:

[10-arbol-de-utilidad.md](./10-arbol-de-utilidad.md)

Estos escenarios permiten relacionar requisitos de calidad con decisiones,
implementación y evidencia verificable.

---

## 12. Glosario

El glosario general del proyecto se encuentra en:

[12-glosario.md](./12-glosario.md)

El lenguaje ubicuo específico formalizado durante S6 se encuentra además en:

[08-conceptos-transversales.md](./08-conceptos-transversales.md#81-lenguaje-ubicuo)

Ambos documentos deben mantenerse coherentes durante la evolución de
CampusMarket.


