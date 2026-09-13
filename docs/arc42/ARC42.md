# CampusMarket - Documentación arc42

## 1. Introducción y objetivos

### 1.1 Descripción del sistema

CampusMarket es una plataforma orientada a estudiantes universitarios que
busca facilitar la publicación, búsqueda, venta y alquiler de productos nuevos
o usados dentro de la comunidad estudiantil.

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
capacidad de Gestión de Publicaciones.

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

El frontend se comunica con el backend mediante una
**API REST sobre HTTP/JSON**.

Durante el desarrollo local, Flutter Web se ejecuta en:

`localhost:3000`

y el backend FastAPI en:

`localhost:8000`

El backend está implementado con **FastAPI y Python** y es responsable de
recibir las solicitudes de la interfaz, validar los datos, ejecutar la lógica
de aplicación y coordinar el acceso a la persistencia.

CampusMarket utiliza actualmente **SQLite** como mecanismo de persistencia local
para el corte vertical materializado.

El frontend no accede directamente a la persistencia.

El recorrido implementado mantiene la separación:

```text
Flutter Web
    ↓
FastAPI
    ↓
Gestión de Publicaciones
    ↓
SQLite
```

La persistencia productiva de publicaciones se encuentra encapsulada en:

`backend/app/publicaciones/repository.py`

y la base de datos local se genera durante la ejecución en:

`backend/data/campusmarket.db`

Una eventual evolución hacia otra tecnología de persistencia no se documenta
como implementada mientras no exista en el código.

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

- arquitectura en capas;
- arquitectura hexagonal;
- monolito modular.

Estas alternativas fueron contrastadas frente a los escenarios de calidad
priorizados por el equipo.

Como resultado de la comparación, se seleccionó un **monolito modular** como
estrategia arquitectónica inicial, buscando equilibrar mantenibilidad,
simplicidad operativa y capacidad de evolución dentro de las restricciones
actuales del proyecto.

El monolito modular se aplica principalmente al backend de CampusMarket, que se
organiza mediante módulos correspondientes a capacidades principales del
negocio:

- `usuarios`;
- `publicaciones`;
- `catalogo`;
- `administracion`.

Estos módulos deben mantener responsabilidades y fronteras explícitas, evitando
dependencias innecesarias entre sus componentes internos.

Durante S6 estas capacidades se formalizaron además como contextos delimitados:

- **Gestión de Usuarios**;
- **Gestión de Publicaciones**;
- **Catálogo**;
- **Administración**.

La capacidad actualmente materializada con mayor profundidad es
**Gestión de Publicaciones**.

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
Frontend Web → Backend API → SQLite
```

Durante S6 se profundiza la estructura interna del Backend API mediante C4
Nivel 3, manteniendo la dirección:

```text
API de Publicaciones
        ↓
Servicio de Publicaciones
        ↓
Repositorio de Publicaciones
        ↓
SQLite
```

El detalle de componentes, propiedad de datos y reglas de dependencia se
encuentra en la sección 5 específica.

---

## 6. Vista de ejecución

Los escenarios de ejecución del sistema se documentan en:

[06-vista-ejecucion.md](./06-vista-ejecucion.md)

La ejecución principal actualmente materializada conserva el recorrido:

```text
Flutter Web
    ↓
FastAPI
    ↓
router.py
    ↓
service.py
    ↓
repository.py
    ↓
SQLite
```

La vista de ejecución también documenta los comportamientos verificables
relacionados con el corte vertical y su evolución arquitectónica.

---

## 8. Conceptos transversales

Durante S6 se formalizaron los conceptos de dominio y las reglas de
modularidad necesarias para mantener coherente la evolución del monolito
modular.

La documentación completa se encuentra en:

[08-conceptos-transversales.md](./08-conceptos-transversales.md)

Esta sección contiene:

- lenguaje ubicuo;
- contextos delimitados;
- mapa de contextos;
- relaciones entre contextos;
- propiedad única de datos;
- reglas de comunicación entre módulos;
- correspondencia con el estado actual del código;
- relación con C4 Nivel 3;
- verificación automática de modularidad.

Los contextos delimitados definidos para CampusMarket son:

- **Gestión de Usuarios**;
- **Gestión de Publicaciones**;
- **Catálogo**;
- **Administración**.

La regla central de propiedad adoptada es:

> Cada dato de dominio tiene un único módulo responsable de escribirlo.

En el estado actual, la entidad persistida de dominio materializada es:

`publicaciones`

y su propietario es:

**Gestión de Publicaciones**

La escritura productiva se encuentra encapsulada en:

`backend/app/publicaciones/repository.py`

---

### 8.1 Mapa de contextos

El mapa de contextos y sus relaciones tipadas se encuentran documentados en:

[08-conceptos-transversales.md](./08-conceptos-transversales.md#83-mapa-de-contextos)

Las relaciones definidas incluyen:

- Gestión de Usuarios → Gestión de Publicaciones:
  **Customer/Supplier**;
- Gestión de Publicaciones → Catálogo:
  **Customer/Supplier**;
- Gestión de Publicaciones → Administración:
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

El Nivel 3 amplía el contenedor Backend API sin modificar la topología del C4
Nivel 2.

La descomposición actualmente verificable es:

```text
API de Publicaciones
        ↓
Servicio de Publicaciones
        ↓
Repositorio de Publicaciones
        ↓
SQLite
```

Los límites de Usuarios, Catálogo y Administración se mantienen documentados,
pero no se presentan como funcionalidades ya materializadas.

---

### 8.4 Verificación automática

Las reglas principales de modularidad se verifican adicionalmente mediante:

[`test_modularidad_s6.py`](../../backend/tests/test_modularidad_s6.py)

La prueba comprueba que:

- `publicaciones` tenga un único escritor productivo;
- otros contextos no accedan directamente a SQLite;
- otros contextos no dependan directamente del repositorio interno de
  Publicaciones;
- la dirección interna permanezca:

  `router → service → repository → SQLite`.

La prueba se ejecuta junto con el resto de `backend/tests` mediante GitHub
Actions.

---

### 8.5 Trazabilidad

La correspondencia entre aspectos, contextos, propiedad de datos, código,
auditoría y pruebas se mantiene en:

[docs/aspectos.md](../aspectos.md)

Para S6 la cadena de trazabilidad se amplía a:

```text
Aspecto
   ↓
Contexto delimitado
   ↓
Propietario del dato
   ↓
C4 Nivel 3
   ↓
Código
   ↓
Auditoría
   ↓
Prueba automática
```

---

### 8.6 Coherencia con ADR-0001

S6 mantiene los límites establecidos previamente por:

[ADR-0001 - Monolito modular](../adr/0001-usar-monolito-modular.md)

Los límites continúan siendo:

- `usuarios`;
- `publicaciones`;
- `catalogo`;
- `administracion`.

Durante S6 estos límites no fueron:

- fusionados;
- divididos;
- reemplazados;
- convertidos en microservicios.

La incorporación del C4 Nivel 3 hace explícita la estructura interna actual del
Backend API, pero no representa un reajuste de las fronteras arquitectónicas.

Por esta razón no se registra un nuevo ADR de reajuste para S6.

Un nuevo ADR será necesario únicamente si una evolución posterior modifica de
forma efectiva estos límites.

---

## 9. Decisiones arquitectónicas

Las decisiones arquitectónicas se encuentran documentadas mediante ADR.

Actualmente:

- [ADR-0001 - Monolito modular](../adr/0001-usar-monolito-modular.md)
- [ADR-0002 - Manejo de bloqueo temporal de SQLite](../adr/0002-manejo-bloqueo-sqlite.md)

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




