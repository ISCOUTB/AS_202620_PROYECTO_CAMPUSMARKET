# Evidencia S6 — Auditoría de modularidad y propiedad de datos

## 1. Objetivo

Esta auditoría verifica si la implementación actual de CampusMarket respeta los
límites definidos para el monolito modular y, específicamente, la regla
arquitectónica de que cada dato de dominio tenga un único módulo responsable de
su escritura.

La revisión se realizó sobre el estado del repositorio correspondiente a la
línea base posterior al primer corte.

---

## 2. Contextos revisados

Los límites definidos para CampusMarket son:

- `usuarios`
- `publicaciones`
- `catalogo`
- `administracion`

Rutas revisadas:

- `backend/app/usuarios/`
- `backend/app/publicaciones/`
- `backend/app/catalogo/`
- `backend/app/administracion/`
- `backend/tests/`
- `scripts/`

---

## 3. Método de auditoría

La revisión buscó identificar:

1. tablas y entidades persistidas;
2. operaciones de creación o modificación de datos;
3. módulos que ejecutan dichas operaciones;
4. accesos directos a SQLite fuera del módulo propietario;
5. posibles escrituras compartidas entre módulos.

Se revisaron específicamente patrones relacionados con:

- `INSERT`
- `UPDATE`
- `DELETE`
- `sqlite3.connect`
- operaciones sobre la tabla `publicaciones`
- repositorios y servicios del backend

La auditoría distingue entre:

- código productivo del backend;
- pruebas automatizadas;
- scripts experimentales o de medición.

---

## 4. Entidades persistidas encontradas

En el estado actual del prototipo se identificó una entidad persistida de
dominio:

### `publicaciones`

Definida en:

`backend/app/publicaciones/repository.py`

Campos actuales:

| Campo | Tipo lógico | Descripción |
|---|---|---|
| `id` | entero | Identificador de la publicación |
| `titulo` | texto | Título del producto publicado |
| `descripcion` | texto | Descripción del producto |
| `precio` | real | Precio declarado |
| `modalidad` | texto | `venta` o `alquiler` |
| `estado` | texto | `nuevo`, `usado` o `reacondicionado` |

No se encontraron actualmente tablas persistidas correspondientes a
`usuarios`, `catalogo` o `administracion`.

---

## 5. Tabla módulo → datos → propietario

| Módulo | Dato / entidad | Escritura actual | Propietario |
|---|---|---|---|
| `publicaciones` | `publicaciones` | Sí | `publicaciones` |
| `usuarios` | identidad de usuarios | No materializada | `usuarios` cuando se implemente |
| `catalogo` | consultas/vistas de publicaciones | No posee persistencia propia | `catalogo` solo será propietario de datos propios |
| `administracion` | información administrativa | No materializada | `administracion` cuando se implemente |

La entidad `publicaciones` tiene actualmente un único escritor productivo:
Gestión de Publicaciones.

---

## 6. Operaciones de escritura encontradas

### 6.1 Creación de publicaciones

Ruta:

`backend/app/publicaciones/repository.py`

Operación identificada:

```sql
INSERT INTO publicaciones (
    titulo,
    descripcion,
    precio,
    modalidad,
    estado
)
VALUES (?, ?, ?, ?, ?)
