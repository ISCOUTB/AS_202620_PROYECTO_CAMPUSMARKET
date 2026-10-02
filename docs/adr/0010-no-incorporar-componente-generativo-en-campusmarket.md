# ADR-0010 - No incorporar un componente generativo en CampusMarket por ahora

**Estado:** Aceptado
**Fecha:** 2026-10-01
**Relacionado con:** Evidencia S9 - Generación verificada y trazable

---

## 1. Contexto

CampusMarket utiliza herramientas de IA generativa como apoyo durante el desarrollo del proyecto.

Ese uso se registra en `docs/ia.md` y está sujeto a revisión humana, pruebas y verificación técnica.

Sin embargo, una decisión distinta es incorporar una capacidad generativa dentro del producto en tiempo de ejecución.

Actualmente CampusMarket tiene como capacidades principales:

- gestión de publicaciones;
- consulta de catálogo;
- búsqueda y filtrado;
- detalle de publicaciones;
- persistencia;
- observabilidad;
- operación y despliegue.

Los escenarios de calidad vigentes no requieren que el sistema genere texto, imágenes, recomendaciones generativas ni contenido mediante un modelo de IA.

---

## 2. Problema

La Evidencia S9 exige que el equipo evalúe el uso de un componente generativo si el sistema lo incorpora o planea incorporarlo.

Si el equipo decide no incorporarlo, la decisión debe quedar justificada mediante ADR.

Por tanto, el equipo debe decidir si CampusMarket debe incluir actualmente una capacidad generativa en el producto.

---

## 3. Alternativas consideradas

### 3.1 Incorporar generación automática de descripciones

El sistema podría utilizar un modelo generativo para redactar descripciones de productos.

#### Ventajas

- menor esfuerzo de escritura para el usuario;
- posible mejora de consistencia textual;
- experiencia diferenciada.

#### Desventajas

- dependencia de un proveedor externo;
- costo por uso;
- latencia adicional;
- necesidad de gestionar errores y disponibilidad del proveedor;
- riesgo de generar información incorrecta sobre un producto;
- necesidad de evaluación específica de calidad de las respuestas.

**Decisión:** descartada por ahora.

---

### 3.2 Incorporar recomendaciones generativas

El sistema podría utilizar IA para generar recomendaciones personalizadas.

#### Ventajas

- posible mejora de descubrimiento de productos;
- experiencia personalizada.

#### Desventajas

- requiere datos suficientes de comportamiento de usuarios;
- introduce decisiones adicionales sobre privacidad;
- necesita métricas de calidad específicas;
- aumenta complejidad y costo;
- no existe actualmente una necesidad funcional demostrada.

**Decisión:** descartada por ahora.

---

### 3.3 No incorporar un componente generativo en tiempo de ejecución

CampusMarket mantiene sus capacidades actuales sin depender de un modelo generativo en producción.

La IA puede seguir utilizándose como herramienta de apoyo al desarrollo, pero sus resultados deben ser revisados y verificados por el equipo.

#### Ventajas

- menor complejidad operativa;
- evita dependencia externa adicional;
- no introduce costo por inferencia;
- no añade latencia al flujo de usuario;
- evita riesgos de generación incorrecta de contenido;
- mantiene el alcance concentrado en los escenarios actuales.

#### Desventajas

- se renuncia temporalmente a posibles funcionalidades de asistencia inteligente;
- futuras capacidades de recomendación o generación requerirán una nueva decisión.

**Decisión:** seleccionada.

---

## 4. Decisión

CampusMarket **no incorporará actualmente un componente generativo dentro del producto en tiempo de ejecución**.

Esta decisión no implica prohibir el uso de herramientas de IA durante el desarrollo.

Se mantiene la siguiente distinción:

IA como apoyo al desarrollo
        ↓
permitida con revisión y verificación

IA generativa dentro del producto
        ↓
no incorporada actualmente

Las capacidades actuales de CampusMarket pueden satisfacerse mediante lógica determinista, contratos HTTP, persistencia, pruebas y reglas de dominio existentes.

## 5. Razones de la decisión

La decisión se basa en:
- ausencia de un requisito funcional que necesite generación;
- ausencia de un escenario de calidad que dependa de IA generativa;
- riesgo de dependencia con proveedores externos;
- costo por inferencia;
- latencia adicional;
- necesidad de evaluación de calidad de respuestas;
- posibilidad de producir contenido incorrecto;
- impacto potencial sobre privacidad;
- incremento de complejidad operativa;
- necesidad de mantener el alcance del proyecto controlado.

## 6. Impacto sobre arquitectura

No se agregan:
- nuevos servicios de IA;
- nuevas APIs externas;
- nuevas credenciales;
- nuevos modelos;
- nueva infraestructura;
- nuevos almacenes de datos;
- nuevas dependencias de ejecución.
La arquitectura continúa como monolito modular.

## 7. Impacto económico

La decisión evita actualmente costos asociados a:
- consumo de APIs de modelos generativos;
- almacenamiento adicional de conversaciones o prompts;
- monitoreo de respuestas generativas;
- evaluación continua del modelo;
- posibles mecanismos de moderación.
Mientras no exista una necesidad funcional demostrada, estos costos no aportan valor suficiente al sistema.

## 8. Impacto sobre latencia

Una llamada a un proveedor generativo introduciría una operación externa adicional en el recorrido del usuario.
Eso:
- aumentaría el tiempo de respuesta;
- agregaría variabilidad;
- incorporaría dependencia de disponibilidad externa.
Las capacidades actuales de búsqueda, filtrado y publicación no requieren esa dependencia.

## 9. Riesgos evitados

La decisión evita actualmente:
- alucinaciones;
- generación de descripciones incorrectas;
- dependencia de proveedor;
- exposición accidental de información a servicios externos;
- costos no controlados;
- degradación por indisponibilidad del proveedor;
- dificultad adicional para reproducir pruebas.
## 10. Uso de IA durante el desarrollo

El equipo continuará registrando en docs/ia.md:
- propuestas aceptadas;
- propuestas corregidas;
- propuestas rechazadas;
- razones técnicas;
- verificación realizada.
La IA no sustituye las decisiones arquitectónicas del equipo.
## 11. Criterios de reconsideración

Esta decisión deberá revisarse mediante un nuevo ADR si aparece una necesidad concreta como:
- asistencia para redactar publicaciones;
- clasificación automática con modelos generativos;
- recomendación inteligente basada en contexto;
- búsqueda semántica avanzada;
- soporte conversacional;
- moderación asistida.
La reconsideración deberá incluir:
- necesidad funcional;
- escenario de calidad;
- proveedor;
- costo;
- latencia;
- privacidad;
- disponibilidad;
- evaluación de calidad;
- pruebas;
- estrategia de fallback.

## 12. Estado
Al momento de crear este ADR:
- no existe un componente generativo en producción;
- no existe dependencia de un proveedor generativo;
- no existe requisito que lo exija;
- no existe escenario de calidad que dependa de generación.
Por estas razones, el estado inicial es:
Propuesto
Pasará a:
Aceptado
cuando el equipo cierre la Evidencia S9 y confirme esta decisión.
