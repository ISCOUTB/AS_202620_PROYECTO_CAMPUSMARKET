# ADR-0006 - Publicar Flutter Web mediante GitHub Pages

## Estado

Aceptado

## Fecha

2026-09-27

## Pieza decidida

**Frontend Web de CampusMarket**

Esta decisión corresponde exclusivamente a la pieza Flutter Web.

No decide el despliegue del Backend API ni de la base de datos.

---

## Contexto

CampusMarket utiliza Flutter Web como frontend del corte vertical.

Una vez ejecutado:

```text
flutter build web
```

el resultado es un conjunto de archivos estáticos que pueden servirse
independientemente del proceso FastAPI.

Durante S8 el frontend necesita:

- una URL pública accesible desde fuera de la universidad;
- comunicación HTTPS con el Backend API;
- despliegue reproducible;
- posibilidad de rollback;
- no depender de una tarjeta bancaria personal;
- mantener bajo el costo del prototipo académico;
- permitir que frontend y backend evolucionen independientemente.

La arquitectura lógica que debe preservarse es:

```text
Usuario
   ↓ HTTPS
Flutter Web
   ↓ HTTPS / JSON
FastAPI
```

Restricciones relacionadas:

- R-08 - despliegue público, reproducible y verificable;
- R-11 - límite de costo operativo;
- R-12 - no dependencia de tarjeta bancaria personal.

---

## Alternativas consideradas

### Alternativa A - GitHub Pages

Publicar el contenido generado en:

```text
frontend/campusmarket/build/web
```

mediante una rama:

```text
gh-pages
```

Ventajas:

- adecuado para contenido web estático;
- permite una URL pública independiente del backend;
- integra el despliegue con el repositorio GitHub existente;
- el frontend puede publicarse sin redesplegar FastAPI;
- durante S8 no produjo costo adicional observado para el equipo;
- el despliegue utilizado no requirió registrar una tarjeta bancaria personal;
- rollback mediante republicación de un build correspondiente a un commit
  previamente validado.

Desventajas:

- no ejecuta lógica de servidor;
- requiere configurar correctamente `base-href`;
- requiere que CORS del backend autorice el origen público;
- la URL del backend debe proporcionarse durante el build.

---

### Alternativa B - Servir Flutter Web desde el mismo Azure App Service de FastAPI

El build estático de Flutter podría incorporarse al mismo artefacto o entorno
que ejecuta FastAPI.

Ventajas:

- una sola plataforma de despliegue;
- podría simplificar el número de destinos operativos;
- permitiría concentrar frontend y API bajo infraestructura Azure.

Desventajas:

- acopla el ciclo de publicación del frontend con el Backend API;
- un cambio únicamente visual puede requerir redesplegar el backend;
- consume recursos del entorno destinado a ejecutar FastAPI;
- dificulta revertir frontend y backend de forma independiente;
- mezcla dos piezas con características operativas distintas.

---

## Decisión

Se selecciona:

**GitHub Pages**

para publicar el frontend Flutter Web de CampusMarket.

URL pública:

`https://nnigarp.github.io/AS_202620_PROYECTO_CAMPUSMARKET/`

La decisión mantiene el frontend como una pieza de despliegue independiente.

La comunicación queda:

```text
GitHub Pages
Flutter Web
    ↓ HTTPS / JSON
Azure App Service
FastAPI
```

---

## Configuración reproducible

El frontend se verifica primero mediante:

```bash
cd frontend/campusmarket
flutter analyze
```

Build utilizado para el entorno público:

```bash
flutter build web \
  --release \
  --dart-define=CAMPUSMARKET_API_BASE_URL=https://campusmarket-s8-api-nilver.azurewebsites.net \
  --base-href "/AS_202620_PROYECTO_CAMPUSMARKET/"
```

Artefacto:

```text
frontend/campusmarket/build/web
```

El contenido generado se publica mediante:

```text
gh-pages
```

---

## Capa gratuita y condición de tarjeta

Durante S8 GitHub Pages se utilizó para el repositorio público del proyecto sin
costo adicional observado para el equipo.

La publicación utilizada para la evidencia no requirió registrar una tarjeta
bancaria personal.

Por tanto, para el volumen y condiciones del prototipo S8:

```text
Costo observado del frontend: USD 0 adicionales
Tarjeta personal requerida: No
```

No se afirma que cualquier uso futuro de GitHub tenga costo cero
indefinidamente.

---

## Punto de ruptura

La decisión debe reevaluarse si ocurre alguna de las siguientes condiciones:

- el frontend deja de poder tratarse como contenido web estático;
- se requiere procesamiento server-side dentro de la propia pieza frontend;
- las necesidades del proyecto exceden las condiciones o límites aplicables a
  GitHub Pages;
- se requiere una característica operativa que GitHub Pages no proporcione;
- las condiciones comerciales del servicio cambian.

En cualquiera de esos casos deberá compararse nuevamente un servicio de hosting
web apropiado.

---

## Seguridad

GitHub Pages no almacena credenciales de MySQL.

El frontend solamente conoce la URL pública del Backend API.

La variable utilizada durante el build es:

```text
CAMPUSMARKET_API_BASE_URL
```

Las credenciales de persistencia permanecen exclusivamente del lado del
backend.

La comunicación con la API utiliza HTTPS.

---

## Verificación realizada

Durante S8 se verificó:

- build Flutter Web exitoso;
- `flutter analyze` sin errores;
- publicación mediante `gh-pages`;
- workflow de GitHub Pages exitoso;
- acceso desde navegador a la URL pública;
- CORS con el Backend API;
- creación real de una publicación desde la interfaz pública;
- persistencia posterior mediante FastAPI y MySQL.

La interfaz pública mostró:

```text
CampusMarket S8: Flutter Web → FastAPI → MySQL en Azure.
```

---

## Rollback

El rollback del frontend consiste en seleccionar un commit previamente
validado, reconstruir su artefacto y republicarlo.

Procedimiento:

```text
1. seleccionar KNOWN_GOOD_SHA;
2. hacer checkout del commit;
3. ejecutar flutter analyze;
4. reconstruir build/web con CAMPUSMARKET_API_BASE_URL;
5. publicar nuevamente el artefacto en gh-pages;
6. comprobar la URL pública;
7. realizar una prueba del corte vertical.
```

Después del rollback deben verificarse:

- carga del frontend;
- comunicación CORS;
- `GET /publicaciones`;
- creación de publicación.

---

## Consecuencias positivas

- frontend públicamente accesible;
- despliegue independiente de FastAPI;
- rollback independiente;
- costo adicional observado igual a cero para S8;
- no dependencia de tarjeta personal;
- menor acoplamiento operativo;
- integración natural con el repositorio GitHub.

---

## Consecuencias negativas

- deben mantenerse dos destinos de despliegue;
- CORS debe configurarse explícitamente;
- `base-href` debe corresponder con la ruta de GitHub Pages;
- la URL del backend debe inyectarse durante el build de producción.

---

## Relación con decisiones anteriores

ADR-0001 continúa vigente: el despliegue del frontend no modifica el monolito
modular del backend.

ADR-0003 continúa vigente: Flutter y FastAPI mantienen comunicación síncrona
HTTP/JSON, utilizando HTTPS en producción.

ADR-0005 queda refinado por este ADR para la decisión específica del frontend.

---

## Evidencia relacionada

- `README.md`
- `frontend/campusmarket/`
- `docs/arc42/07-vista-despliegue.md`
- `docs/arc42/02-restricciones.md`
- `docs/evidencias/evidencia-s8-2026-09-27.md`
- rama `gh-pages`
