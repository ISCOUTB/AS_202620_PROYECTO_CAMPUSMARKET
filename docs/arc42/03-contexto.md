# 3. Contexto y alcance

Esta sección describe el contexto actual de CampusMarket, los actores externos, el alcance funcional y las interfaces que delimitan el sistema.

## 3.1 Contexto del sistema

CampusMarket es un marketplace universitario orientado a centralizar la publicación, consulta y búsqueda de productos dentro de la comunidad universitaria.

Los actores externos principales son:

- **Estudiante:** utiliza CampusMarket para publicar y consultar productos.
- **Administrador:** participa en la supervisión de publicaciones y contenido.

El contexto del sistema está representado en el C4 Nivel 1:

[C4 Nivel 1 - Contexto](../c4/01-contexto.md)

Fuente versionada del diagrama:

[`01-contexto.puml`](../c4/01-contexto.puml)

## 3.2 Alcance funcional

CampusMarket contempla como capacidades del sistema:

- gestión de publicaciones de productos;
- consulta y búsqueda de productos;
- modalidades de venta y alquiler;
- gestión básica de usuarios;
- supervisión de publicaciones.

Para la Evidencia S4, el corte vertical implementado y verificable se concentra en la **creación y consulta de publicaciones**.

Actualmente no forman parte del alcance:

- pagos electrónicos;
- procesamiento bancario;
- servicios de envío;
- logística de entrega;
- integraciones con empresas de transporte.

Estas exclusiones permiten mantener el alcance del prototipo compatible con las restricciones del proyecto.

## 3.3 Interfaces externas

Durante la ejecución local de la Evidencia S4:

- el frontend se ejecuta mediante **Flutter Web**;
- el frontend se comunica con el backend mediante **HTTP/JSON REST**;
- el backend utiliza **FastAPI / Python**;
- la persistencia utilizada por el corte vertical es **SQLite**.

El frontend no accede directamente a la persistencia.

El recorrido implementado es:

**Flutter Web → Backend API FastAPI → lógica de publicaciones → SQLite**

En desarrollo local:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`

La comunicación mediante HTTPS corresponde a un despliegue externo futuro y no se documenta como si ya estuviera implementada en el entorno local.

Actualmente no existen integraciones implementadas con sistemas externos de pagos, banca, transporte o logística.

## 3.4 Relación con los diagramas C4

El **C4 Nivel 1** representa CampusMarket como un único sistema e identifica a sus actores externos.

El **C4 Nivel 2** muestra los contenedores actuales de CampusMarket:

- **Frontend Web:** Flutter / Dart;
- **Backend API:** FastAPI / Python;
- **Persistencia local:** SQLite.

Los actores externos definidos en el Nivel 1 se mantienen conectados en el Nivel 2.

Documentación:

- [C4 Nivel 1 - Contexto](../c4/01-contexto.md)
- [C4 Nivel 2 - Contenedores](../c4/02-contenedores.md)

Fuentes versionadas:

- [`01-contexto.puml`](../c4/01-contexto.puml)
- [`02-contenedores.puml`](../c4/02-contenedores.puml)
