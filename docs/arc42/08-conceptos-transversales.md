# 8. Conceptos transversales

Esta sección documenta los conceptos de dominio y las reglas de modularidad
adoptadas por CampusMarket durante la Evidencia S6.

El objetivo es mantener un lenguaje común entre interesados, documentación y
código, además de establecer límites explícitos entre los módulos del monolito
modular y la propiedad de los datos.

---

## 8.1 Lenguaje ubicuo

CampusMarket utiliza los siguientes términos de manera consistente en el
dominio:

| Término | Significado en CampusMarket |
|---|---|
| Estudiante | Usuario principal de CampusMarket que puede consultar o publicar productos. |
| Usuario | Identidad utilizada por una persona para interactuar con CampusMarket. |
| Producto | Artículo que un estudiante desea ofrecer dentro de la comunidad universitaria. |
| Publicación | Registro mediante el cual un estudiante ofrece un producto en CampusMarket. |
| Modalidad | Forma en que se ofrece un producto. Actualmente puede ser `venta` o `alquiler`. |
| Estado del producto | Condición declarada del producto: `nuevo`, `usado` o `reacondicionado`. |
| Catálogo | Conjunto consultable de publicaciones disponibles en CampusMarket. |
| Administrador | Usuario encargado de supervisar el contenido disponible en la plataforma. |
| Propietario | Estudiante responsable de una publicación. |
| Contexto delimitado | Límite dentro del dominio en el que los términos, reglas y responsabilidades mantienen un significado consistente. |
| Dueño del dato | Módulo con autoridad para crear o modificar un determinado dato de dominio. |

### Producto y publicación

En CampusMarket, **Producto** y **Publicación** no son sinónimos.

Un **Producto** representa el artículo que un estudiante desea vender o
alquilar.

Una **Publicación** representa la información registrada en CampusMarket para
ofrecer ese producto.

Esta distinción evita utilizar ambos términos indistintamente en la
documentación y en la evolución del código.

---

## 8.2 Contextos delimitados

A partir del lenguaje del dominio y de las capacidades definidas previamente
para el monolito modular, CampusMarket identifica los siguientes contextos:

### Gestión de Usuarios

Responsable de la identidad y datos asociados a los usuarios de CampusMarket.

Responsabilidades previstas:

- registro de estudiantes;
- autenticación;
- información básica del usuario;
- identificación del propietario de una publicación.

Correspondencia en el código:

`backend/app/usuarios/`

Estado actual: el límite modular existe en el repositorio, pero todavía no se
encuentra materializada toda la funcionalidad prevista para este contexto.

---

### Gestión de Publicaciones

Responsable del ciclo de vida de las publicaciones mediante las cuales los
estudiantes ofrecen productos.

Responsabilidades actuales:

- crear publicaciones;
- validar los datos de una publicación;
- almacenar publicaciones;
- recuperar publicaciones;
- mantener modalidad, precio y estado del producto.

Correspondencia principal en el código:

`backend/app/publicaciones/`

En el estado actual del sistema, este es el contexto con mayor
materialización funcional.

---

### Catálogo

Responsable de ofrecer una vista consultable de las publicaciones disponibles.

Responsabilidades previstas:

- consulta de publicaciones;
- búsqueda;
- filtrado;
- organización de resultados.

Correspondencia en el código:

`backend/app/catalogo/`

Este contexto no es propietario de las publicaciones. Cuando requiera
información de ellas deberá obtenerla a través de las operaciones expuestas por
Gestión de Publicaciones y no modificar directamente su persistencia.

---

### Administración

Responsable de las capacidades de supervisión y moderación de CampusMarket.

Responsabilidades previstas:

- supervisión de publicaciones;
- gestión de contenido que incumpla las reglas de la plataforma;
- operaciones administrativas autorizadas.

Correspondencia en el código:

`backend/app/administracion/`

Administración no debe modificar directamente tablas pertenecientes a otros
contextos. Las operaciones sobre una publicación deberán solicitarse al
contexto Gestión de Publicaciones mediante un contrato explícito.

---

## 8.3 Mapa de contextos

El mapa de contextos de CampusMarket establece las siguientes relaciones:

```text
Gestión de Usuarios
        |
        | identidad / propietario
        v
Gestión de Publicaciones
        |
        | publicaciones consultables
        v
      Catálogo

Administración
        |
        | solicita operaciones de moderación
        v
Gestión de Publicaciones