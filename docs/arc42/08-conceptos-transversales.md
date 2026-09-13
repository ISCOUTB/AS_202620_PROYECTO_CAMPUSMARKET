# 8. Conceptos transversales

Esta sección documenta los conceptos de dominio y las reglas de modularidad
adoptadas por CampusMarket para la Evidencia S6.

El objetivo es mantener un lenguaje común entre interesados, documentación y
código, establecer límites explícitos entre los contextos del dominio y definir
qué módulo tiene autoridad para escribir cada dato.

La definición se basa en el estado real del repositorio al inicio de S6. Por
esta razón se diferencia explícitamente entre capacidades actualmente
implementadas y responsabilidades previstas para la evolución del sistema.

---

## 8.1 Lenguaje ubicuo

El lenguaje ubicuo de CampusMarket establece los términos que deben utilizarse
de forma consistente en requisitos, documentación arquitectónica y código.

| Término | Significado en CampusMarket |
|---|---|
| Estudiante | Usuario principal de CampusMarket que puede consultar productos y, cuando la gestión de usuarios esté materializada, publicar productos. |
| Usuario | Identidad mediante la cual una persona interactúa con CampusMarket. |
| Producto | Artículo que un estudiante desea ofrecer dentro de la comunidad universitaria. |
| Publicación | Registro mediante el cual se describe y ofrece un producto en CampusMarket. |
| Modalidad | Forma en que se ofrece un producto: actualmente `venta` o `alquiler`. |
| Estado del producto | Condición declarada del artículo: `nuevo`, `usado` o `reacondicionado`. |
| Catálogo | Vista consultable de las publicaciones disponibles en CampusMarket. |
| Administrador | Usuario responsable de las capacidades de supervisión y moderación del contenido. |
| Propietario | Estudiante responsable de una publicación. Esta relación pertenece al modelo objetivo, pero todavía no está persistida en el corte actual. |
| Contexto delimitado | Límite del dominio dentro del cual términos, reglas y responsabilidades mantienen un significado consistente. |
| Dueño del dato | Módulo con autoridad exclusiva para crear o modificar un dato de dominio. |
| Escritura compartida | Situación no permitida en la que dos módulos modifican directamente el mismo dato o entidad persistida. |
| Contrato entre módulos | Operación o interfaz explícita utilizada para solicitar capacidades de otro contexto sin acceder directamente a su persistencia. |

Este vocabulario complementa el glosario general de CampusMarket y debe
mantenerse coherente con él durante la evolución del proyecto.

### Producto y publicación

En CampusMarket, **Producto** y **Publicación** no son sinónimos.

Un **Producto** es el artículo físico o bien que un estudiante desea vender o
alquilar.

Una **Publicación** es la representación registrada en CampusMarket mediante la
cual ese producto se ofrece a otros estudiantes.

En el corte actual no existe todavía una entidad `producto` independiente. Los
atributos del producto utilizados por el prototipo se encuentran almacenados
dentro de la entidad persistida `publicaciones`.

Esta distinción permite conservar un lenguaje de dominio consistente sin
afirmar que exista actualmente una estructura de persistencia separada para
Producto.

---

## 8.2 Contextos delimitados

La estrategia arquitectónica de CampusMarket define un monolito modular con
cuatro capacidades principales:

- Gestión de Usuarios;
- Gestión de Publicaciones;
- Catálogo;
- Administración.

Estos contextos representan límites de responsabilidad. No todos tienen el
mismo grado de implementación en el estado actual del prototipo.

### 8.2.1 Gestión de Usuarios

**Responsabilidad de dominio**

Gestionar la identidad de los estudiantes que interactúan con CampusMarket.

**Responsabilidades previstas**

- registro de estudiantes;
- autenticación;
- información básica del usuario;
- identificación del propietario de una publicación.

**Correspondencia estructural**

`backend/app/usuarios/`

**Estado actual**

El límite modular se encuentra creado en el repositorio, pero la funcionalidad
de usuarios y su persistencia todavía no están materializadas.

Por esta razón S6 no declara actualmente tablas o entidades persistidas como
propiedad de este contexto.

---

### 8.2.2 Gestión de Publicaciones

**Responsabilidad de dominio**

Gestionar el ciclo de vida de las publicaciones mediante las cuales se ofrecen
productos dentro de CampusMarket.

**Responsabilidades actualmente implementadas**

- recibir solicitudes para crear publicaciones;
- validar y normalizar los datos recibidos;
- crear publicaciones;
- almacenar publicaciones;
- listar publicaciones;
- manejar temporalmente fallos de disponibilidad de SQLite.

**Correspondencia estructural**

`backend/app/publicaciones/`

**Persistencia actual**

`backend/app/publicaciones/repository.py`

Actualmente este contexto posee la única entidad persistida de dominio
materializada en el prototipo: `publicaciones`.

La tabla contiene:

- `id`;
- `titulo`;
- `descripcion`;
- `precio`;
- `modalidad`;
- `estado`.

Gestión de Publicaciones es el único contexto que debe escribir directamente
esta entidad.

---

### 8.2.3 Catálogo

**Responsabilidad de dominio**

Proporcionar capacidades de consulta, búsqueda y filtrado sobre las
publicaciones disponibles.

**Responsabilidades previstas**

- consultar publicaciones disponibles;
- buscar productos;
- aplicar filtros;
- organizar resultados.

**Correspondencia estructural**

`backend/app/catalogo/`

**Estado actual**

El límite modular existe, pero la funcionalidad propia de Catálogo todavía no
está materializada.

Catálogo no es propietario de la entidad `publicaciones`.

Cuando estas capacidades sean implementadas deberá consumir información
proporcionada por Gestión de Publicaciones mediante un contrato explícito, sin
ejecutar escrituras directas sobre su persistencia.

---

### 8.2.4 Administración

**Responsabilidad de dominio**

Gestionar las capacidades de supervisión y moderación de CampusMarket.

**Responsabilidades previstas**

- supervisar publicaciones;
- solicitar acciones de moderación;
- gestionar contenido que incumpla las reglas de la plataforma.

**Correspondencia estructural**

`backend/app/administracion/`

**Estado actual**

El límite modular existe, pero sus capacidades todavía no están materializadas.

Administración no es propietaria de `publicaciones` y no debe ejecutar
operaciones directas sobre la tabla perteneciente a Gestión de Publicaciones.

Una futura operación administrativa sobre una publicación deberá solicitarse
mediante un contrato explícito del contexto Gestión de Publicaciones.

---

## 8.3 Mapa de contextos

El mapa de contextos diferencia las relaciones arquitectónicas previstas de las
capacidades que ya están implementadas.

```mermaid
flowchart LR
    U["Gestión de Usuarios"]
    P["Gestión de Publicaciones"]
    C["Catálogo"]
    A["Administración"]

    U -->|"Customer / Supplier<br/>identidad del estudiante<br/>(previsto)"| P
    P -->|"Customer / Supplier<br/>publicaciones consultables<br/>(previsto)"| C
    P -->|"Contrato de Publicaciones<br/>+ ACL en Administración<br/>(previsto)"| A
```

### Gestión de Usuarios → Gestión de Publicaciones

La relación prevista es **Customer/Supplier**.

Gestión de Usuarios actúa como contexto proveedor (*upstream*) de información
de identidad, mientras Gestión de Publicaciones consume esa capacidad
(*downstream*) para asociar operaciones con un estudiante.

Esta relación todavía no está completamente materializada porque el corte
actual no posee persistencia de usuarios ni una referencia de propietario
dentro de `publicaciones`.

### Gestión de Publicaciones → Catálogo

La relación prevista es **Customer/Supplier**.

Gestión de Publicaciones actúa como proveedor de información sobre
publicaciones y Catálogo como consumidor para construir búsquedas, filtros y
consultas.

Catálogo no obtiene derecho de escritura sobre los datos por consumir esa
información.

### Gestión de Publicaciones → Administración

Administración necesita solicitar acciones relacionadas con publicaciones, pero
no debe conocer ni modificar directamente su persistencia.

Para este límite se adopta como regla de diseño una **capa anticorrupción
(ACL)** en Administración. Esta capa deberá traducir las necesidades de
moderación a contratos explícitos ofrecidos por Gestión de Publicaciones.

La ACL se documenta como decisión de diseño para la evolución del módulo; no se
declara como implementada en el estado actual.

### Shared Kernel

En S6 **no se identifica un Shared Kernel entre los contextos**.

No existe actualmente un modelo de dominio compartido que necesite ser
modificado conjuntamente por dos módulos. Introducirlo sin necesidad aumentaría
el acoplamiento y debilitaría la regla de propiedad única de los datos.

---

## 8.4 Propiedad de datos

CampusMarket adopta como regla arquitectónica:

> Cada dato de dominio tiene un único módulo responsable de escribirlo.

La tabla refleja el estado actual del código, no únicamente el diseño futuro.

| Contexto / módulo | Dato o entidad | Estado actual | Lectura | Escritura | Dueño |
|---|---|---|---|---|---|
| Gestión de Publicaciones | `publicaciones` | Implementada en SQLite | Publicaciones; futuros consumidores mediante contrato | Solo Gestión de Publicaciones | Gestión de Publicaciones |
| Gestión de Usuarios | usuarios / identidad | No persistido actualmente | No aplica todavía | No aplica todavía | Gestión de Usuarios cuando se implemente |
| Catálogo | vista de publicaciones | No posee persistencia propia actualmente | Consumirá Publicaciones | No debe escribir `publicaciones` | Catálogo solo será dueño de datos propios si aparecen |
| Administración | datos administrativos | No persistidos actualmente | Podrá consultar mediante contratos | No debe escribir `publicaciones` directamente | Administración solo será dueño de datos propios si aparecen |

### Entidad `publicaciones`

La entidad persistida actualmente contiene:

| Campo | Significado | Dueño |
|---|---|---|
| `id` | Identificador interno de la publicación | Gestión de Publicaciones |
| `titulo` | Título con el que se ofrece el producto | Gestión de Publicaciones |
| `descripcion` | Descripción del producto publicado | Gestión de Publicaciones |
| `precio` | Precio declarado | Gestión de Publicaciones |
| `modalidad` | `venta` o `alquiler` | Gestión de Publicaciones |
| `estado` | `nuevo`, `usado` o `reacondicionado` | Gestión de Publicaciones |

No se asignan artificialmente entidades a Usuarios, Catálogo o Administración
porque esas estructuras todavía no existen en el código actual.

---

## 8.5 Reglas de comunicación entre módulos

Para conservar los límites del monolito modular se adoptan las siguientes
reglas:

1. Un módulo no puede ejecutar operaciones de escritura directa sobre tablas
   pertenecientes a otro módulo.
2. El módulo dueño conserva la autoridad para crear, modificar o eliminar sus
   datos.
3. Las necesidades de otro contexto deben expresarse mediante contratos,
   servicios u operaciones públicas.
4. Consultar información de otro contexto no transfiere la propiedad del dato.
5. No se permitirá que dos módulos tengan repositorios que modifiquen la misma
   entidad.
6. Una futura extracción de servicios deberá preservar los mismos límites de
   propiedad definidos en el monolito modular.

Ejemplos:

- Catálogo podrá consultar publicaciones, pero no ejecutar directamente un
  `INSERT`, `UPDATE` o `DELETE` sobre `publicaciones`.
- Administración podrá solicitar la moderación de una publicación, pero la
  operación deberá ser ejecutada por Gestión de Publicaciones.
- Gestión de Publicaciones podrá consumir identidad de Usuarios cuando dicha
  capacidad exista, pero no modificar directamente los datos internos de
  usuarios.

---

## 8.6 Correspondencia con el estado actual

La separación documentada en esta sección mantiene los límites establecidos
previamente para el monolito modular:

- `usuarios`;
- `publicaciones`;
- `catalogo`;
- `administracion`.

S6 no introduce por sí misma una separación en microservicios ni modifica el
estilo arquitectónico seleccionado.

El propósito de esta evidencia es hacer explícitos los límites de dominio, la
propiedad de los datos y las reglas de comunicación necesarias para evitar que
el monolito modular evolucione hacia un sistema altamente acoplado.

La auditoría de código de S6 complementa esta sección verificando si las
escrituras observadas en el repositorio respetan estas reglas.

---

## 8.7 Correspondencia con C4 Nivel 3 y verificación automática

Los límites y reglas de modularidad definidos en esta sección se complementan
con el C4 Nivel 3 del Backend API:

- [`C4 Nivel 3 - Componentes del Backend`](../c4/03-componentes-backend.md)
- [`Fuente PlantUML del C4 Nivel 3`](../c4/03-componentes-backend.puml)

El C4 Nivel 3 amplía el contenedor Backend API definido previamente en el
Nivel 2 y muestra la materialización actualmente verificable de Gestión de
Publicaciones mediante:

`API de Publicaciones → Servicio de Publicaciones → Repositorio de Publicaciones → SQLite`

Los contextos Gestión de Usuarios, Catálogo y Administración permanecen
representados como límites arquitectónicos definidos, pero todavía no se
declaran como capacidades funcionales materializadas.

La propiedad única de los datos se verifica adicionalmente mediante:

[`backend/tests/test_modularidad_s6.py`](../../backend/tests/test_modularidad_s6.py)

Esta prueba comprueba que:

- `backend/app/publicaciones/repository.py` sea el único escritor productivo de
  la entidad `publicaciones`;
- otros contextos no accedan directamente a SQLite;
- otros contextos no dependan directamente del repositorio interno de
  Publicaciones;
- el flujo implementado conserve la dirección
  `router → service → repository → SQLite`.

La auditoría detallada se encuentra en:

[`Auditoría de modularidad S6`](../evidencias/auditoria-modularidad-s6-2026-09-12.md)

### Coherencia con el primer corte

Los límites principales continúan siendo los definidos por ADR-0001:

- `usuarios`;
- `publicaciones`;
- `catalogo`;
- `administracion`.

La incorporación del C4 Nivel 3 hace explícita la estructura interna del
Backend API, pero no reemplaza, divide ni fusiona dichos límites.

Por esta razón no se registra un nuevo ADR de reajuste en S6. Un nuevo ADR
será necesario únicamente si una evolución posterior modifica realmente estas
fronteras arquitectónicas.
