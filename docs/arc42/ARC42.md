# CampusMarket - Documentación arc42

## 1. Introducción y objetivos

### 1.1 Descripción del sistema

CampusMarket es una plataforma orientada a estudiantes universitarios que busca facilitar la publicación, búsqueda, venta y alquiler de productos nuevos o usados dentro de la comunidad estudiantil.

La idea surge debido a que muchos estudiantes ofrecen productos mediante grupos de WhatsApp, redes sociales u otros medios informales, donde las publicaciones pueden perderse fácilmente y no existe una forma centralizada y organizada de consultar los artículos disponibles.

CampusMarket busca centralizar estas publicaciones en una plataforma donde los estudiantes puedan encontrar y ofrecer productos de manera organizada, manteniendo un alcance adecuado para el desarrollo académico durante el semestre.

La interfaz será desarrollada con Flutter, utilizando inicialmente su capacidad Web y manteniendo la posibilidad de extender el mismo frontend a Android e iOS en etapas posteriores.

---

### 1.2 Objetivos de negocio e interesados

Los objetivos de negocio de CampusMarket se orientan a mejorar la forma en que los estudiantes universitarios ofrecen y encuentran productos dentro de su comunidad.

| ID | Objetivo de negocio | Interesado principal |
|---|---|---|
| ON-01 | Centralizar en una sola plataforma las publicaciones de productos que actualmente se encuentran dispersas en grupos de WhatsApp, redes sociales y otros medios informales. | Estudiantes universitarios |
| ON-02 | Facilitar que los estudiantes encuentren productos disponibles para compra o alquiler dentro de la comunidad universitaria. | Estudiantes compradores o arrendatarios |
| ON-03 | Dar mayor visibilidad a los productos que los estudiantes desean vender o alquilar mediante publicaciones organizadas y consultables. | Estudiantes vendedores o propietarios |
| ON-04 | Mantener un entorno controlado para las publicaciones y apoyar la supervisión del contenido disponible en la plataforma. | Administrador de CampusMarket |

---

### 1.3 Objetivos de calidad

Los principales atributos de calidad considerados para CampusMarket son los siguientes.

#### Mantenibilidad

La aplicación debe estar organizada de forma que sea posible modificar o agregar funcionalidades sin afectar innecesariamente partes del sistema que no estén relacionadas con el cambio.

Este objetivo se desarrolla mediante el escenario de calidad **EC-03 - Modificación del sistema**.

#### Seguridad

Un estudiante solamente podrá modificar o eliminar las publicaciones que le pertenecen. Los intentos de modificación realizados por usuarios que no sean propietarios deberán ser rechazados.

Este objetivo se desarrolla mediante el escenario **EC-02 - Protección de publicaciones**.

#### Rendimiento

Las funciones principales de consulta y búsqueda deben responder en tiempos adecuados durante la operación normal del sistema.

Este objetivo se desarrolla mediante el escenario **EC-01 - Consulta de productos**.

#### Disponibilidad y recuperación

En caso de una falla durante una prueba o demostración, el equipo debe poder recuperar el funcionamiento del prototipo en un tiempo controlado y sin perder la información almacenada correctamente antes de la falla.

Este objetivo se desarrolla mediante el escenario **EC-04 - Recuperación del prototipo**.

Los escenarios completos y sus medidas verificables se encuentran en:

[10-escenarios-de-calidad.md](./10-escenarios-de-calidad.md)

El árbol de utilidad y su priorización se encuentran en:

[10-arbol-de-utilidad.md](./10-arbol-de-utilidad.md)

---

## 2. Restricciones

Las restricciones de CampusMarket delimitan el espacio de solución y condicionan las decisiones arquitectónicas que puede tomar el equipo.

### R-01. Tiempo de desarrollo

**Tipo:** Organizativa  
**Origen:** Asignatura / calendario académico

CampusMarket debe alcanzar un prototipo funcional dentro del semestre académico.

**Justificación:** El proyecto se desarrolla de manera incremental durante el curso y debe producir un sistema funcional y verificable dentro del periodo establecido. Esta condición limita el alcance y la complejidad que puede asumir el equipo.

---

### R-02. Tamaño del equipo

**Tipo:** Organizativa  
**Origen:** Conformación del equipo

CampusMarket será desarrollado por un equipo de tres integrantes.

**Justificación:** La capacidad de desarrollo disponible está limitada al trabajo de tres integrantes durante el semestre. Las decisiones arquitectónicas y el alcance deben ser compatibles con los recursos humanos disponibles.

---

### R-03. Repositorio y control de versiones

**Tipo:** Técnica / organizativa  
**Origen:** Metodología de trabajo del curso

El código fuente, la documentación arquitectónica y las evidencias incrementales de CampusMarket deberán mantenerse versionados en el repositorio del proyecto.

**Justificación:** El repositorio constituye el punto de referencia para verificar la evolución del sistema y mantener trazabilidad entre documentación, implementación y evidencias.

---

### R-04. Análisis de calidad del código

**Tipo:** Técnica  
**Origen:** Herramientas de calidad utilizadas en el proyecto

El repositorio de CampusMarket deberá integrarse con SonarCloud durante el desarrollo.

**Justificación:** La integración permitirá analizar de manera continua características relacionadas con la calidad del código y obtener evidencia verificable sobre los problemas detectados.

---

### R-05. Alcance funcional del prototipo

**Tipo:** Organizativa / alcance  
**Origen:** Alcance definido por el equipo

La versión inicial de CampusMarket no incluirá pagos en línea, procesamiento bancario, servicios de envío ni logística de entrega.

**Justificación:** Estas funcionalidades requieren integraciones externas y aumentan considerablemente la complejidad técnica y operativa del sistema. Excluirlas permite concentrar el esfuerzo en las capacidades principales del marketplace.

---

### R-06. Plataforma de ejecución inicial

**Tipo:** Técnica  
**Origen:** Alcance tecnológico inicial

CampusMarket será desarrollado inicialmente como una aplicación accesible desde navegadores modernos mediante Flutter Web.

La tecnología seleccionada permitirá reutilizar la base de código del frontend para una posible ejecución posterior en Android e iOS.

**Justificación:** Mantener Web como plataforma inicial permite controlar el alcance del prototipo durante el semestre, mientras que Flutter ofrece la posibilidad de extender posteriormente la solución a dispositivos móviles sin mantener aplicaciones completamente independientes.

El detalle completo de las restricciones se encuentra en:

[02-restricciones.md](./02-restricciones.md)

---

## 3. Contexto y alcance

### 3.1 Contexto del sistema

CampusMarket tendrá como principales actores a los estudiantes universitarios y al administrador de la plataforma.

Los estudiantes utilizarán el sistema para registrarse, iniciar sesión, publicar productos, consultar el catálogo, realizar búsquedas y filtros y administrar sus propias publicaciones.

El administrador utilizará CampusMarket para supervisar las publicaciones y apoyar la gestión general del contenido de la plataforma.

---

### 3.2 Alcance funcional

CampusMarket incluirá inicialmente:

- Gestión básica de usuarios.
- Registro e inicio de sesión.
- Gestión de publicaciones de productos.
- Consulta del catálogo.
- Búsqueda y filtrado de productos.
- Clasificación de productos como nuevos o usados.
- Publicaciones para venta, alquiler o ambas modalidades.
- Edición y eliminación de publicaciones propias.
- Consulta de información para contactar al propietario del producto.
- Supervisión básica de publicaciones por parte del administrador.

No harán parte del alcance inicial:

- Pagos electrónicos.
- Procesamiento bancario.
- Servicios de envío.
- Logística de entrega.
- Integración con empresas de transporte.

---

### 3.3 Interfaces externas

En el estado actual del prototipo, los estudiantes acceden a CampusMarket mediante una interfaz desarrollada con **Flutter Web**.

El frontend se comunica con el backend mediante una **API REST sobre HTTP/JSON**. Durante el desarrollo local de la Evidencia S4, Flutter Web se ejecuta en `localhost:3000` y el backend en `localhost:8000`.

El backend está implementado con **FastAPI y Python** y es responsable de recibir las solicitudes de la interfaz, validar los datos, ejecutar la lógica de aplicación y coordinar el acceso a la persistencia.

Para el **corte vertical de la Semana 4**, CampusMarket utiliza **SQLite** como mecanismo de persistencia local. Esta es la tecnología actualmente implementada y verificada en el prototipo para almacenar y recuperar publicaciones.

El frontend no accede directamente a la persistencia. El recorrido implementado mantiene la siguiente separación:

**Flutter Web → API FastAPI → lógica del módulo `publicaciones` → SQLite**

La persistencia se encuentra implementada en:

`backend/app/publicaciones/repository.py`

y la base de datos local se genera durante la ejecución en:

`backend/data/campusmarket.db`

**MySQL** se mantiene como tecnología de persistencia prevista para una evolución posterior del proyecto. No se documenta en esta etapa como si ya estuviera implementada.

Cuando el prototipo sea desplegado en un entorno accesible externamente, la comunicación entre los clientes y CampusMarket deberá realizarse mediante **HTTPS**.

En el alcance actual no se contemplan integraciones con sistemas bancarios, plataformas de pago, empresas de transporte ni servicios externos de logística.---

### 3.4 Diagrama de contexto

El diagrama C4 de contexto identifica a CampusMarket, sus usuarios principales y las relaciones existentes entre ellos.

El diagrama se encuentra documentado en:

[01-contexto.md](../c4/01-contexto.md)

---

## 4. Estrategia de solución

La estrategia arquitectónica de CampusMarket se basa en la evaluación de **arquitectura en capas, arquitectura hexagonal y monolito modular** frente a los escenarios de calidad priorizados por el equipo.

Como resultado de la comparación, se seleccionó un **monolito modular** como estrategia arquitectónica inicial, buscando equilibrar mantenibilidad, simplicidad operativa y capacidad de evolución dentro de las restricciones actuales del proyecto.

El monolito modular se aplicará principalmente al backend de CampusMarket, que será organizado mediante módulos correspondientes a las capacidades principales del negocio:

- `usuarios`
- `publicaciones`
- `catalogo`
- `administracion`

Estos módulos deberán mantener responsabilidades y fronteras explícitas, evitando dependencias innecesarias entre sus componentes internos.

El detalle de la comparación entre estilos, las tácticas arquitectónicas seleccionadas, sus costos y las consecuencias de la decisión se encuentra en:

[04-estrategia-de-solucion.md](./04-estrategia-de-solucion.md)

La decisión se registra formalmente en:

[ADR-0001 - Adoptar un monolito modular para CampusMarket](../adr/0001-usar-monolito-modular.md)

El escenario de calidad que motiva principalmente esta decisión es:

[EC-03 - Modificación del sistema](./10-escenarios-de-calidad.md#ec-03---modificación-del-sistema)
