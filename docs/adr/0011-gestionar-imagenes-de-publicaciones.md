# ADR-0011 - Gestionar hasta tres imágenes por publicación sin romper la propiedad de datos

**Estado:** Aceptado  
**Fecha:** 2026-10-02  
**Aspectos relacionados:** ASP-01 - Consulta y búsqueda de productos; experiencia de publicación  
**ADR relacionados:** ADR-0001, ADR-0004, ADR-0005, ADR-0009

---

## 1. Contexto

CampusMarket evolucionó de un corte vertical centrado en datos textuales a una experiencia de marketplace en la que una publicación necesita evidencia visual del producto.

La arquitectura vigente mantiene un monolito modular. El contexto `publicaciones` es propietario de la escritura de publicaciones y su persistencia; `catalogo` compone la experiencia de consulta mediante capacidades explícitas del módulo `publicaciones`, según ADR-0009.

La solución debe permitir:

- asociar hasta tres imágenes a una publicación;
- identificar una imagen principal;
- mantener orden determinista;
- mostrar la imagen principal en el catálogo;
- mostrar la colección completa en el detalle;
- evitar almacenar binarios o Base64 dentro de la tabla `publicaciones`;
- conservar la trazabilidad entre contrato, implementación, prueba y evidencia.

La solución local de desarrollo no debe confundirse con la estrategia de almacenamiento productivo. El despliegue en Azure documentado en S8 requiere que, antes de llevar esta capacidad a producción, el almacenamiento de archivos se ubique en un medio persistente apropiado para ese entorno.

---

## 2. Problema

Guardar tres columnas (`imagen1_url`, `imagen2_url`, `imagen3_url`) en `publicaciones` resolvería el caso inmediato, pero introduciría rigidez, campos repetidos y una evolución costosa si cambia el límite o aparecen metadatos adicionales.

Guardar el archivo binario directamente en MySQL aumentaría el tamaño y acoplamiento de la persistencia relacional a un recurso que tiene un ciclo de vida distinto.

También existe un riesgo de consistencia: si primero se escribe el archivo y luego falla el registro de metadatos en MySQL, puede quedar un archivo huérfano.

---

## 3. Alternativas consideradas

### 3.1 Tres columnas de URL en `publicaciones`

**Ventajas**

- implementación directa;
- una sola tabla.

**Desventajas**

- estructura rígida;
- campos repetidos;
- dificulta ordenar, marcar principal y evolucionar metadatos;
- mezcla la entidad publicación con la colección de recursos visuales.

**Decisión:** descartada.

### 3.2 Guardar BLOB/Base64 en MySQL

**Ventajas**

- transacción concentrada en una base de datos;
- no requiere un almacenamiento de archivos separado.

**Desventajas**

- crecimiento innecesario de la base relacional;
- mayor costo de transferencia y respaldo;
- acoplamiento entre persistencia transaccional y contenido binario;
- no es la estrategia objetivo para despliegue productivo.

**Decisión:** descartada.

### 3.3 Tabla de metadatos + almacenamiento externo al esquema relacional

Se crea `publicacion_imagenes` con una fila por imagen. MySQL conserva metadatos y referencia; el archivo se guarda fuera de la tabla.

**Ventajas**

- modelo normalizado;
- permite ordenar y marcar la imagen principal;
- mantiene separado el binario de los datos relacionales;
- facilita sustituir almacenamiento local por Azure Blob Storage sin modificar el contrato de dominio;
- soporta borrado en cascada de metadatos.

**Costos y riesgos**

- requiere coordinar dos recursos;
- puede existir inconsistencia parcial si una operación falla;
- el almacenamiento local no es suficiente como solución productiva en una instancia efímera.

**Decisión:** seleccionada.

---

## 4. Decisión

CampusMarket representará las imágenes mediante la tabla `publicacion_imagenes`:

```text
publicacion_imagenes
- id
- publicacion_id  -> publicaciones.id
- imagen_url
- orden           -> 1..3
- es_principal
```

Se establecen las siguientes reglas:

1. Una publicación puede tener como máximo tres imágenes.
2. La primera imagen registrada es la principal.
3. El orden se conserva mediante `orden` y una restricción única por publicación.
4. Los formatos aceptados son JPG, JPEG, PNG y WEBP.
5. El tamaño máximo es 5 MiB por imagen.
6. Los archivos no se versionan en Git; `backend/uploads/` permanece ignorado.
7. En desarrollo local, los archivos se sirven mediante `/uploads` desde FastAPI.
8. Si el archivo se escribe y luego falla el registro de metadatos, se ejecuta una compensación para eliminar el archivo ya creado.
9. `catalogo` no accede directamente a `publicacion_imagenes`; obtiene las imágenes mediante una capacidad de lectura expuesta por `publicaciones`.
10. El contrato HTTP expone la carga mediante `POST /publicaciones/{publication_id}/imagenes` y la consulta del catálogo incorpora la colección `imagenes`.

---

## 5. Flujo resultante

```text
Flutter - Publicar
   ↓ POST /publicaciones
FastAPI - Publicaciones
   ↓
MySQL - publicaciones
   ↓ id
Flutter
   ↓ multipart (máx. 3)
POST /publicaciones/{id}/imagenes
   ↓
almacenamiento de archivo + metadatos MySQL

Flutter - Catálogo
   ↓ GET /catalogo
Catálogo
   ↓ capacidad de lectura
Publicaciones
   ↓
MySQL (publicaciones + metadatos de imágenes)
   ↓
imagen principal en tarjeta / galería en detalle
```

---

## 6. Consecuencias

### Positivas

- la publicación conserva un modelo relacional limpio;
- la UI puede mostrar contenido visual real;
- `catalogo` mantiene la frontera definida por ADR-0009;
- la estrategia permite migrar el archivo físico sin cambiar la entidad publicación;
- las restricciones de cantidad y orden quedan verificables.

### Negativas

- existe coordinación entre almacenamiento de archivo y MySQL;
- el almacenamiento local requiere una posterior sustitución para producción;
- consultar las imágenes agrega lecturas adicionales mientras no exista una consulta agregada optimizada.

---

## 7. Verificación y evidencia

La decisión se considera implementada únicamente cuando exista evidencia verificable de:

- creación de una publicación;
- carga real de una, dos y tres imágenes;
- rechazo de una cuarta imagen;
- rechazo de formato o tamaño inválido;
- consulta de `GET /catalogo` con metadatos de imágenes;
- renderizado de la imagen principal en la tarjeta;
- visualización de la colección en el detalle;
- prueba automatizada de la respuesta de catálogo con imágenes;
- contrato OpenAPI regenerado y prueba de contrato en verde;
- `flutter analyze` sin errores;
- suite backend en verde para el mismo hash que se entregue.

El 2 de octubre de 2026 se verificó localmente el flujo de creación de la publicación `#49` con tres imágenes antes de integrar su lectura en Catálogo. Esa ejecución sirve como evidencia intermedia; no sustituye la verificación final del hash entregado.

---

## 8. Criterio de reconsideración

Esta decisión debe revisarse si ocurre cualquiera de estas condiciones:

- el backend se despliega en una infraestructura donde el filesystem local no ofrece persistencia garantizada;
- se requiere CDN, transformación o versionado de imágenes;
- aumenta de forma relevante el volumen o tamaño de archivos;
- se necesita eliminación/reordenamiento independiente de imágenes;
- aparecen métricas que demuestren que la composición actual del catálogo incumple EC-01.

En producción, la alternativa preferente a evaluar es un almacenamiento de objetos persistente (por ejemplo, Azure Blob Storage) detrás de una abstracción de almacenamiento, manteniendo en MySQL únicamente metadatos y referencias.
