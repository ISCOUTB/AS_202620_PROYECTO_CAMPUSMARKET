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

```

La escritura está encapsulada dentro del repositorio perteneciente al mismo
contexto dueño de la entidad.

**Resultado:** conforme.

---

### 6.2 Actualizaciones

No se identificaron operaciones productivas:

```sql
UPDATE publicaciones
```

en el estado actual revisado.

**Resultado:** no aplica en el corte actual.

---

### 6.3 Eliminaciones

No se identificaron operaciones productivas:

```sql
DELETE FROM publicaciones
```

en el estado actual revisado.

**Resultado:** no aplica en el corte actual.

---

## 7. Accesos directos a SQLite

Además del repositorio de Publicaciones, se encontraron conexiones directas a
SQLite en código de soporte.

### `backend/tests/test_publicaciones_vertical.py`

El acceso se utiliza durante pruebas automatizadas para preparar o verificar el
estado de la persistencia.

Este archivo no pertenece a otro contexto de dominio y no representa un segundo
módulo productivo propietario de `publicaciones`.

### `scripts/medir_bloqueo_sqlite.py`

El script abre directamente SQLite con el propósito de producir de forma
controlada un bloqueo exclusivo y medir la respuesta del sistema.

La creación de una publicación durante el experimento se realiza mediante el
endpoint HTTP del sistema y no mediante un `INSERT` alternativo implementado por
otro módulo de negocio.

Por tanto, este acceso se clasifica como **instrumentación experimental** y no
como escritura compartida entre contextos.

---

## 8. Escrituras compartidas

### Resultado

**No se detectaron escrituras compartidas entre módulos de dominio en el estado
actual del repositorio.**

El único escritor productivo identificado para la entidad `publicaciones` se
encuentra en:

`backend/app/publicaciones/repository.py`

No se encontraron implementaciones en:

- `backend/app/usuarios/`
- `backend/app/catalogo/`
- `backend/app/administracion/`

que ejecuten escrituras directas sobre `publicaciones`.

Esta conclusión no se obtiene de una lista vacía asumida: resulta del recorrido
de las rutas del backend y de la búsqueda de operaciones de persistencia
descritas anteriormente.

---

## 9. No conformidades y riesgos detectados

Aunque actualmente no existe una escritura compartida entre contextos, se
identificaron riesgos de evolución.

| ID | Hallazgo / riesgo | Estado | Plan |
|---|---|---|---|
| MOD-01 | Catálogo podría terminar consultando o escribiendo directamente SQLite cuando se implemente. | Riesgo futuro | Consumir Publicaciones mediante contratos explícitos y prohibir repositorios de Catálogo sobre la tabla `publicaciones`. |
| MOD-02 | Administración podría modificar directamente `publicaciones` al implementar moderación. | Riesgo futuro | Exponer una operación de moderación desde Publicaciones y utilizar una capa anticorrupción desde Administración. |
| MOD-03 | La relación entre propietario y publicación todavía no está materializada. | Brecha actual | Incorporar la identidad del propietario cuando Gestión de Usuarios sea implementada, manteniendo Usuarios como dueño de identidad. |
| MOD-04 | Scripts y pruebas acceden directamente a SQLite para verificación experimental. | Aceptado para pruebas | Mantener estos accesos fuera del código productivo y documentar su propósito. |

---

## 10. Plan de corrección y prevención

### MOD-01 — Catálogo

Cuando se implemente el contexto Catálogo:

- no crear operaciones `INSERT`, `UPDATE` o `DELETE` sobre `publicaciones`;
- consumir operaciones públicas del contexto Publicaciones;
- mantener Catálogo orientado a consulta, búsqueda y filtrado.

### MOD-02 — Administración

Cuando se implemente moderación:

- Administración no debe acceder directamente al repositorio de Publicaciones;
- Gestión de Publicaciones deberá ofrecer una operación explícita de moderación;
- Administración utilizará una capa anticorrupción para adaptar sus necesidades
  al contrato de Publicaciones.

### MOD-03 — Propietario de publicación

Cuando Usuarios sea materializado:

- la identidad seguirá siendo propiedad de Gestión de Usuarios;
- Publicaciones almacenará únicamente la referencia necesaria para asociar al
  propietario;
- Publicaciones no modificará los datos internos del usuario.

### MOD-04 — Código de prueba

Los accesos directos a SQLite utilizados por pruebas y scripts deberán
mantenerse separados del código productivo.

Su finalidad deberá permanecer explícitamente documentada como instrumentación
de prueba o medición.

---

## 11. Conclusión

La implementación actual de CampusMarket cumple, para las entidades
materializadas en este corte, con la regla de propiedad única de datos.

La entidad `publicaciones` posee un único escritor productivo dentro del módulo
Gestión de Publicaciones.

No se detectaron dos contextos escribiendo actualmente la misma entidad.

Los principales riesgos identificados corresponden a la evolución futura de
Catálogo, Administración y Usuarios. Por ello se documentan desde S6 reglas de
comunicación y propiedad que deberán preservarse cuando estos módulos incorporen
funcionalidad.

La auditoría confirma que el monolito modular actual constituye una base válida
para continuar creciendo sin introducir escrituras compartidas entre contextos.
