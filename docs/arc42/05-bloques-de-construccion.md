# 5. Bloques de construcción

CampusMarket se materializa en tres bloques ejecutables para el corte vertical de la Semana 4.

| Bloque | Responsabilidad | Tecnología | Ubicación |
|---|---|---|---|
| Frontend Web | Capturar la información de una publicación y comunicarla al backend. | Flutter / Dart | `frontend/campusmarket/lib/` |
| Backend API | Validar la solicitud y coordinar la creación y consulta de publicaciones. | FastAPI / Python | `backend/app/` |
| Persistencia local | Guardar y recuperar publicaciones del corte vertical. | SQLite / `sqlite3` | `backend/app/publicaciones/repository.py` |

## 5.1 Backend modular

La decisión ADR-0001 organiza el backend por capacidades del negocio:

- `usuarios`: registro, autenticación y gestión básica de usuarios;
- `publicaciones`: creación y gestión de publicaciones;
- `catalogo`: consulta, búsqueda y filtrado;
- `administracion`: supervisión del contenido.

En S4 el recorrido funcional implementado se concentra en `publicaciones`. Los demás módulos mantienen sus fronteras sin incorporar lógica no exigida por la evidencia.

## 5.2 Interfaces relevantes

- **Flutter → FastAPI:** REST sobre HTTP/JSON.
- **FastAPI → SQLite:** operaciones SQL mediante la biblioteca estándar `sqlite3`.
- **Endpoint de creación:** `POST /publicaciones`.
- **Endpoint de consulta:** `GET /publicaciones`.

La estructura corresponde al C4 Nivel 2 documentado en `docs/c4/02-contenedores.puml`.
