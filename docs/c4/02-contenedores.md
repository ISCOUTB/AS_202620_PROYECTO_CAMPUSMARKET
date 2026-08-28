# C4 Nivel 2 - Contenedores de CampusMarket

El diagrama de contenedores vigente de CampusMarket se mantiene como **diagrama como código** en:

[`02-contenedores.puml`](./02-contenedores.puml)

## Propósito

Este nivel muestra los contenedores principales que forman CampusMarket, su responsabilidad general, la tecnología utilizada y la comunicación entre ellos.

Los actores externos se mantienen coherentes con el C4 Nivel 1:

- **Estudiante:** utiliza CampusMarket para publicar, consultar y buscar productos.
- **Administrador:** accede al sistema para funciones de supervisión.

## Contenedores

| Contenedor | Tecnología | Responsabilidad |
|---|---|---|
| Frontend Web | Flutter / Dart | Proporcionar la interfaz web mediante la cual los usuarios interactúan con CampusMarket. |
| Backend API | FastAPI / Python | Recibir solicitudes HTTP, validar datos y coordinar la lógica de aplicación. |
| Persistencia local | SQLite | Almacenar y recuperar los datos utilizados por el corte vertical actual. |

## Correspondencia con el código

| Contenedor C4 | Evidencia en el repositorio |
|---|---|
| Frontend Web | `frontend/campusmarket/lib/` |
| Backend API | `backend/app/` |
| Persistencia local | `backend/app/publicaciones/repository.py`, que utiliza `sqlite3` para almacenar y recuperar publicaciones. |

La base SQLite utilizada durante la ejecución se genera dinámicamente. Por esta razón, la evidencia versionada de la persistencia se encuentra en el código que implementa el acceso a SQLite y no en un archivo de base de datos almacenado en Git.

## Relaciones entre contenedores

- **Estudiante → Frontend Web:** interacción mediante navegador web.
- **Administrador → Frontend Web:** acceso mediante navegador web.
- **Frontend Web → Backend API:** comunicación mediante **HTTP/JSON REST**.
- **Backend API → Persistencia local:** acceso mediante **SQL utilizando `sqlite3`**.

## Alcance del Nivel 2

Este diagrama representa únicamente los contenedores principales del sistema.

No describe:

- módulos internos;
- componentes;
- clases;
- routers;
- servicios;
- repositorios internos.

Ese nivel de detalle corresponde al **C4 Nivel 3**, que no forma parte de la Evidencia S4.

## Fuente canónica

El archivo [`02-contenedores.puml`](./02-contenedores.puml) es la fuente versionada y vigente del C4 Nivel 2.

Las modificaciones del diagrama deben realizarse sobre ese archivo para mantener la documentación sincronizada con el repositorio.
