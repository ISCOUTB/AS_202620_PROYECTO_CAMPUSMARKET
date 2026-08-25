# C4 Nivel 2 - Contenedores de CampusMarket

El diagrama versionado se encuentra en [`02-contenedores.puml`](./02-contenedores.puml).

## Correspondencia con el código

| Contenedor | Tecnología | Evidencia en el repositorio |
|---|---|---|
| Frontend Web | Flutter / Dart | `frontend/campusmarket/lib/` |
| Backend API | FastAPI / Python | `backend/app/` |
| Persistencia del corte S4 | SQLite | `backend/app/publicaciones/repository.py` y `backend/data/` en ejecución |

El nivel 2 mantiene los mismos actores del nivel 1: **Estudiante** y **Administrador**.
No se incluye C4 nivel 3 porque la Evidencia S4 lo pospone a la semana 6.
