# ADR-0019 — Consultar imágenes en lote a través de Publicaciones

- Estado: Aceptado
- Fecha: 2026-10-03
- Relación: extiende ADR-0009 y ADR-0016; conserva el límite de contexto del
  catálogo y no reescribe decisiones aceptadas.

## Contexto

El catálogo filtraba publicaciones y luego llamaba a listar_imagenes_publicacion
por cada fila. Cada llamada inicializa y abre conexiones MySQL. Con 1000 filas
y 0,5 CPU por contenedor, la primera búsqueda superó el timeout HTTP de 60 s
en [Compose d473b1f](https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37141453184).
La cuota sí sostuvo hashes e imagen de 12 MP sin OOM. El problema es la
cantidad de viajes a la persistencia, no una razón para debilitar autenticación.

## Alternativas

1. Catálogo importa el repository de Publicaciones: viola propiedad de datos.
2. Copiar SQL a un shared kernel o usar otro servicio: introduce acoplamiento
   o distribución para una proyección local.
3. Interfaz de lectura en lote del servicio propietario: mantiene el monolito
   y elimina N llamadas por búsqueda sin cambiar el contrato HTTP.

## Decisión

Elegir 3. Catálogo filtra las publicaciones recibidas del servicio, pasa sus
IDs a listar_imagenes_publicaciones y compone la respuesta con la colección
agrupada. Publicaciones ejecuta una consulta parametrizada IN, conserva el
orden de las imágenes y devuelve listas vacías para publicaciones sin fotos.

Catálogo no accede a SQL ni a repository ajeno. Los parámetros son valores
y los placeholders se generan por cantidad; nunca interpolar IDs en SQL.
El contrato OpenAPI y el detalle conservan su forma.

## Trade-offs y consecuencias

- Se mantienen filtros en memoria y listado completo del MVP; paginación
  sería una decisión futura si el volumen excede la escala comprobada.
- La consulta retorna como máximo tres imágenes por publicación según la
  restricción ya existente; no agrega cachés ni réplicas.
- Catálogo depende del contrato interno de Publicaciones y una prueba de
  modularidad impide erosionarlo.
- No se promete latencia pública a partir de una medición loopback.

## Prueba y evidencia

MySQL real con 52 publicaciones visibles, dos propietarios, galerías distintas,
filas ocultas/heredadas y 50 listas vacías. La cantidad de conexiones queda
constante (<=4) y la mutación que consulta una por una debe fallar.
Compose repite diez búsquedas de 1000 filas bajo cuota y exige 9/10 <=2 s.
