# ADR-0001 - Adoptar un monolito modular para CampusMarket

**Estado:** Aceptado  
**Fecha:** 2026-08-23  
**Decisión:** Estilo arquitectónico inicial de CampusMarket  
**Escenario principal:** EC-03 - Modificación del sistema  
**Aspecto relacionado:** ASP-03 - Evolución de la gestión de productos  

---

## 1. Contexto

CampusMarket es una plataforma web orientada a estudiantes universitarios que busca facilitar la publicación, búsqueda, venta y alquiler de productos nuevos o usados dentro de la comunidad estudiantil.

El proyecto debe construir un prototipo funcional durante el semestre académico y será desarrollado por un equipo de tres integrantes. Por esta razón, se necesita una arquitectura que permita organizar el sistema de forma mantenible sin introducir una complejidad técnica u operativa mayor que la necesaria para el alcance actual.

La decisión se toma considerando los escenarios de calidad priorizados en el árbol de utilidad:

| Escenario | Atributo de calidad | Prioridad |
|---|---|---|
| EC-01 - Consulta de productos | Rendimiento | Alta |
| EC-02 - Protección de publicaciones | Seguridad | Alta |
| EC-03 - Modificación del sistema | Mantenibilidad | Alta |
| EC-04 - Recuperación del prototipo | Disponibilidad y recuperación | Media |

El escenario que principalmente motiva esta decisión es **EC-03 - Modificación del sistema**.

En este escenario se solicita agregar un nuevo estado para los productos, por ejemplo, `reacondicionado`. La medida establecida indica que el cambio deberá realizarse modificando **como máximo dos módulos principales y sin requerir cambios en las funciones de autenticación o búsqueda**.

La arquitectura seleccionada debe, por tanto, favorecer la separación de responsabilidades, el bajo acoplamiento y la evolución del sistema, manteniendo al mismo tiempo una complejidad adecuada para el equipo.

También condicionan esta decisión las siguientes restricciones:

- **R-01 - Tiempo de desarrollo:** el prototipo debe completarse dentro del semestre académico.
- **R-02 - Tamaño del equipo:** CampusMarket será desarrollado por tres integrantes.
- **R-05 - Alcance funcional:** el prototipo inicial no incluirá pagos electrónicos, procesamiento bancario, servicios de envío ni logística de entrega.
- **R-06 - Plataforma web:** CampusMarket será desarrollado inicialmente como una aplicación web.

---

## 2. Alternativas evaluadas

Se evaluaron tres estilos arquitectónicos:

1. Arquitectura en capas.
2. Arquitectura hexagonal.
3. Monolito modular.

La comparación detallada contra los escenarios de calidad se encuentra en la [sección 4 de arc42](../arc42/04-estrategia-de-solucion.md).

### 2.1 Arquitectura en capas

La arquitectura en capas organiza el sistema principalmente alrededor de áreas técnicas como presentación, lógica de negocio y persistencia.

**Ventajas:**

- estructura sencilla y conocida;
- bajo costo de implementación inicial;
- facilita comenzar rápidamente el prototipo;
- puede mantenerse como una sola unidad de despliegue.

**Desventajas:**

- un cambio funcional puede atravesar varias capas;
- una misma capacidad del negocio puede quedar distribuida entre diferentes áreas técnicas;
- puede aumentar el acoplamiento a medida que crece el sistema;
- responde con menor claridad a EC-03.

**Motivo de descarte:**

Se descarta como estrategia principal porque la organización horizontal puede hacer que cambios relacionados con una funcionalidad requieran modificar presentación, lógica y persistencia.

Aunque resulta sencilla al inicio, ofrece menor aislamiento funcional que el monolito modular para el escenario de mantenibilidad priorizado.

---

### 2.2 Arquitectura hexagonal

La arquitectura hexagonal organiza el sistema separando el dominio de los mecanismos externos mediante puertos y adaptadores.

**Ventajas:**

- fuerte aislamiento entre dominio e infraestructura;
- alta testabilidad;
- facilita sustituir mecanismos externos;
- favorece la mantenibilidad y la inversión de dependencias.

**Desventajas:**

- requiere mayor cantidad de interfaces, puertos y adaptadores;
- introduce mayor indirección;
- aumenta el código de andamiaje;
- exige mayor esfuerzo inicial para un equipo pequeño.

**Motivo de descarte:**

Se descarta para la etapa actual porque su costo de implementación y abstracción resulta mayor que el beneficio adicional que aporta para el alcance actual de CampusMarket.

La arquitectura hexagonal responde muy bien a EC-03, pero el monolito modular permite obtener un nivel suficiente de aislamiento y mantenibilidad con menor complejidad estructural.

Podría reconsiderarse posteriormente si CampusMarket necesita integrar múltiples mecanismos externos o sustituir infraestructura con frecuencia.

---

### 2.3 Monolito modular

El monolito modular mantiene una sola aplicación y una sola unidad de despliegue, pero organiza internamente el sistema mediante módulos asociados con capacidades del negocio.

Para CampusMarket se plantean inicialmente los siguientes módulos:

- `usuarios`
- `publicaciones`
- `catalogo`
- `administracion`

Cada módulo tendrá responsabilidades explícitas y deberá evitar depender directamente de los detalles internos de otros módulos.

**Ventajas:**

- mantiene una única aplicación para desarrollar y desplegar;
- reduce la complejidad operativa;
- organiza el código según capacidades del negocio;
- permite establecer fronteras explícitas;
- favorece la mantenibilidad;
- evita comunicación distribuida innecesaria;
- permite evolucionar progresivamente el sistema.

**Costo y riesgos:**

- requiere disciplina para respetar las fronteras;
- todos los módulos comparten la misma unidad de despliegue;
- no permite escalar cada módulo de forma independiente;
- existe riesgo de aumentar el acoplamiento si no se controlan las dependencias.

---

## 3. Decisión

**CampusMarket adopta un monolito modular como estilo arquitectónico inicial.**

El sistema se implementará como una sola aplicación y una sola unidad de despliegue, organizada internamente mediante módulos con responsabilidades y fronteras explícitas.

La organización inicial será:

| Módulo | Responsabilidad principal |
|---|---|
| `usuarios` | Registro, autenticación y gestión básica del usuario |
| `publicaciones` | Creación, modificación, eliminación y validación de propiedad de publicaciones |
| `catalogo` | Consulta, búsqueda y filtrado de productos |
| `administracion` | Supervisión y gestión básica del contenido |

La comunicación entre módulos deberá realizarse mediante contratos, interfaces o servicios explícitos.

Un módulo no deberá acceder arbitrariamente a los componentes internos de otro módulo.

Durante esta etapa, los módulos **no se desplegarán como servicios independientes**.

---

## 4. Justificación

El monolito modular ofrece el mejor equilibrio entre las necesidades de mantenibilidad y las restricciones actuales de CampusMarket.

La decisión responde principalmente a **EC-03 - Modificación del sistema**, porque organizar el código por capacidades del negocio permite limitar el impacto de los cambios.

Por ejemplo, agregar un nuevo estado para un producto deberá concentrarse principalmente en `publicaciones` y, cuando corresponda, en `catalogo`, sin requerir modificaciones en `usuarios`.

Esto permite orientar la implementación hacia la medida definida en EC-03:

> El cambio deberá realizarse modificando como máximo dos módulos principales y sin requerir cambios en las funciones de autenticación o búsqueda.

Además, una sola unidad de despliegue reduce el esfuerzo necesario para construir, ejecutar, probar y recuperar el prototipo durante el semestre.

Frente a las alternativas evaluadas:

- **Capas** ofrece mayor simplicidad inicial, pero menor aislamiento funcional.
- **Hexagonal** ofrece mayor aislamiento y testabilidad, pero introduce un sobrecosto de abstracciones para el alcance actual.
- **Monolito modular** mantiene la simplicidad operativa de una sola aplicación y agrega fronteras funcionales acordes con EC-03.

---

## 5. Tácticas arquitectónicas y costos asumidos

| Escenario | Tácticas asociadas | Costo asumido |
|---|---|---|
| **EC-01 - Rendimiento** | Ejecutar las consultas dentro del mismo proceso; evitar comunicación remota; concentrar búsqueda y filtrado en `catalogo`; utilizar paginación e índices cuando se implemente persistencia. | Los índices y la paginación requieren configuración, mantenimiento y pruebas adicionales. |
| **EC-02 - Seguridad** | Autenticación antes de operaciones protegidas; validación de propiedad; control de acceso; rechazo por defecto ante operaciones no autorizadas. | Añade validaciones, código adicional y cierto costo de procesamiento. |
| **EC-03 - Mantenibilidad** | Modularización por capacidades; SRP; DIP cuando sea necesario; alta cohesión; bajo acoplamiento; contratos explícitos; variaciones protegidas. | Requiere disciplina sobre dependencias y puede introducir interfaces e indirección adicional. |
| **EC-04 - Recuperación** | Una única unidad de despliegue; configuración reproducible; un procedimiento único de inicio y prueba. | Una falla de la aplicación puede afectar simultáneamente a todos los módulos. |

El equipo acepta estos costos porque son compatibles con las prioridades y restricciones actuales del proyecto.

---

## 6. Consecuencias

### Consecuencias positivas

- el código queda organizado según capacidades del negocio;
- se reduce el impacto esperado de los cambios funcionales;
- se mantiene una única aplicación para construir y desplegar;
- se evita la complejidad operativa de una solución distribuida;
- las responsabilidades entre módulos quedan explícitas;
- se facilita incorporar pruebas por módulo;
- la arquitectura puede evolucionar posteriormente si cambian las necesidades.

### Consecuencias negativas y riesgos asumidos

- las fronteras entre módulos deberán mantenerse activamente;
- será necesario controlar las dependencias entre módulos;
- todos los módulos compartirán el mismo ciclo de despliegue;
- una falla global puede afectar toda la aplicación;
- no será posible escalar cada módulo independientemente;
- el sistema podría degradarse hacia un monolito fuertemente acoplado si no se respeta la modularidad.

Estas consecuencias se consideran aceptables frente al tiempo disponible, el tamaño del equipo y el alcance del prototipo.

---

## 7. Impacto sobre la implementación

El esqueleto ejecutable de CampusMarket deberá reflejar esta decisión mediante una estructura que haga visibles las fronteras iniciales:

```text
usuarios/
publicaciones/
catalogo/
administracion/
