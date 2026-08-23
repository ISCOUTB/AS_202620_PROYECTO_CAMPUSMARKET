# Escenarios de calidad - CampusMarket

Los siguientes escenarios permiten convertir los atributos de calidad del proyecto en condiciones observables y verificables.

Los valores utilizados como medidas fueron definidos inicialmente por el equipo y podrán ser ajustados posteriormente mediante pruebas y evidencia del prototipo.

---

## EC-01 - Consulta de productos

**Atributo de calidad:** Rendimiento.

**Fuente:** Estudiante.

**Estímulo:** El estudiante realiza una búsqueda o aplica un filtro sobre el catálogo.

**Artefacto:** Funcionalidad de consulta de productos de CampusMarket.

**Entorno:** Operación normal con un catálogo de hasta 1.000 publicaciones.

**Respuesta:** El sistema procesa la consulta y muestra los productos que coinciden con los criterios seleccionados.

**Medida verificable:** En una prueba de 10 búsquedas consecutivas, por lo menos 9 deben mostrar los resultados en un tiempo máximo de 2 segundos.

**Prioridad:** Alta.

---

## EC-02 - Protección de publicaciones

**Atributo de calidad:** Seguridad.

**Fuente:** Usuario autenticado.

**Estímulo:** El usuario intenta editar o eliminar una publicación que pertenece a otro estudiante.

**Artefacto:** Funcionalidad de gestión de publicaciones.

**Entorno:** Operación normal con dos usuarios registrados diferentes.

**Respuesta:** CampusMarket rechaza la operación y mantiene la publicación sin modificaciones.

**Medida verificable:** En 10 intentos realizados por un usuario que no sea propietario de la publicación, los 10 intentos deben ser rechazados.

**Prioridad:** Alta.

---

## EC-03 - Modificación del sistema

**Atributo de calidad:** Mantenibilidad.

**Fuente:** Equipo de desarrollo.

**Estímulo:** Se solicita agregar un nuevo estado para los productos, por ejemplo, "reacondicionado".

**Artefacto:** Funcionalidad encargada de gestionar los productos.

**Entorno:** Desarrollo normal del sistema.

**Respuesta:** El equipo incorpora la nueva opción sin modificar funcionalidades no relacionadas con los productos.

**Medida verificable:** El cambio deberá realizarse modificando como máximo dos módulos principales y sin requerir cambios en las funciones de autenticación o búsqueda.

**Prioridad:** Alta.

---

## EC-04 - Recuperación del prototipo

**Atributo de calidad:** Disponibilidad y recuperación.

**Fuente:** Administrador o equipo de desarrollo.

**Estímulo:** La aplicación deja de responder durante una prueba o demostración.

**Artefacto:** Aplicación CampusMarket.

**Entorno:** Ejecución del prototipo.

**Respuesta:** El equipo reinicia o recupera el servicio y vuelve a permitir el acceso a CampusMarket sin perder la información almacenada correctamente antes de la falla.

**Medida verificable:** El prototipo deberá volver a estar disponible en un tiempo máximo de 10 minutos después de detectar la falla.

**Prioridad:** Media.
