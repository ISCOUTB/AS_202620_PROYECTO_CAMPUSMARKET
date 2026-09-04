# CampusMarket

Marketplace universitario para la publicación, consulta, venta y alquiler de productos dentro de la comunidad universitaria.

## Integrantes

- Joshua Tenorio Alvarez
- Camilo Martinez Berrio
- Nilver Garcia Pimentel

## Arquitectura

CampusMarket adopta un **monolito modular** de acuerdo con:

[ADR-0001 - Monolito modular](docs/adr/0001-usar-monolito-modular.md)

Para la Evidencia S4, el corte vertical implementado corresponde principalmente a la capacidad de `publicaciones`.

## Tecnologías actuales

- Frontend: Flutter / Dart
- Backend: FastAPI / Python
- Persistencia S4: SQLite
- Persistencia prevista posteriormente: MySQL

En S4, SQLite es la persistencia realmente implementada.

## Requisitos previos

- Python 3.12
- Flutter disponible en `PATH`
- Google Chrome
- Dependencias Python:

```bash
pip install -r backend/requirements.txt
```

## Arranque con un solo comando

### Windows

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_s4.ps1
```

### Linux/macOS

```bash
bash scripts/run_s4.sh
```

El comando inicia:

- Backend FastAPI: `http://localhost:8000`
- Frontend Flutter Web: `http://localhost:3000`

## Corte vertical S4

El corte vertical implementado recorre:

**Flutter Web → FastAPI → lógica de publicaciones → SQLite**

La Evidencia S4 se concentra en la creación y consulta de publicaciones.

### Correspondencia con el código

- Interfaz: [`publicacion_form_page.dart`](frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart)
- Cliente API: [`publicaciones_api.dart`](frontend/campusmarket/lib/publicaciones/publicaciones_api.dart)
- Entrada Backend: [`router.py`](backend/app/publicaciones/router.py)
- Lógica: [`service.py`](backend/app/publicaciones/service.py)
- Persistencia SQLite: [`repository.py`](backend/app/publicaciones/repository.py)

## Pruebas automatizadas

Desde la raíz del repositorio:

```bash
python -m pytest backend/tests -q
```

La prueba principal del corte vertical es:

[`backend/tests/test_publicaciones_vertical.py`](backend/tests/test_publicaciones_vertical.py)

La prueba crea una publicación mediante HTTP, verifica su persistencia en SQLite y posteriormente consulta el registro almacenado.

## Integración continua y análisis estático

Las pruebas automatizadas del backend y el análisis estático se ejecutan mediante GitHub Actions con:

[`.github/workflows/backend-tests.yml`](.github/workflows/backend-tests.yml)

La configuración de SonarQube Cloud se encuentra en:

[`sonar-project.properties`](sonar-project.properties)

El pipeline realiza:

1. Obtención del repositorio.
2. Configuración de Python 3.12.
3. Instalación de dependencias.
4. Ejecución de pruebas automatizadas con `pytest`.
5. Análisis estático con SonarQube Cloud en los `push` a `master`.

### Evidencia de ejecución exitosa

- Workflow: **Pruebas del backend**
- Run: **#29**
- Rama: `master`
- Resultado general: **success**
- Pruebas automatizadas: **success**
- Análisis de SonarQube Cloud: **success**
- [GitHub Actions - Run #29](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/33847799874)

## Documentación arc42

- Secciones 1 a 4: [`ARC42.md`](docs/arc42/ARC42.md)
- Sección 2: [`02-restricciones.md`](docs/arc42/02-restricciones.md)
- Sección 3: [`03-contexto.md`](docs/arc42/03-contexto.md)
- Sección 4: [`04-estrategia-de-solucion.md`](docs/arc42/04-estrategia-de-solucion.md)
- Sección 5: [`05-bloques-de-construccion.md`](docs/arc42/05-bloques-de-construccion.md)
- Sección 6: [`06-vista-ejecucion.md`](docs/arc42/06-vista-ejecucion.md)
- Sección 9: [`09-decisiones.md`](docs/arc42/09-decisiones.md)
- Sección 10: [`10-escenarios-de-calidad.md`](docs/arc42/10-escenarios-de-calidad.md)
- Sección 12: [`12-glosario.md`](docs/arc42/12-glosario.md)

## Diagramas C4

### Nivel 1 - Contexto

- [Documentación](docs/c4/01-contexto.md)
- [Fuente PlantUML](docs/c4/01-contexto.puml)

### Nivel 2 - Contenedores

- [Documentación](docs/c4/02-contenedores.md)
- [Fuente PlantUML](docs/c4/02-contenedores.puml)

Para la Evidencia S4 se documentan C4 Nivel 1 y Nivel 2. No se requiere C4 Nivel 3.

## Trazabilidad

La trazabilidad del proyecto está documentada en:

[`docs/aspectos.md`](docs/aspectos.md)

Para la Evidencia S4, la fila **ASP-05 - Creación de publicaciones** está completa hasta la columna **Pruebas** y relaciona:

**Aspecto → Requisito → C4 → ADR → Código → Pruebas → Evidencia**

## Alcance de la Evidencia S4

El corte vertical verificable de S4 corresponde principalmente a la creación y consulta de publicaciones.

Actualmente no se documentan como implementados:

- pagos electrónicos;
- procesamiento bancario;
- envíos y logística;
- integraciones con empresas de transporte.

## Evidencia explícita para revisión S4

### Glosario de dominio

El glosario completo de CampusMarket se encuentra en:

[`docs/arc42/12-glosario.md`](docs/arc42/12-glosario.md)

Incluye términos propios del dominio del sistema:

- **Publicación:** registro mediante el cual un estudiante ofrece un producto.
- **Producto:** artículo que un estudiante desea vender o alquilar.
- **Modalidad:** forma en que se ofrece un producto: venta o alquiler.
- **Estado del producto:** condición del artículo: nuevo, usado o reacondicionado.
- **Estudiante:** usuario principal que publica o consulta productos.
- **Administrador:** usuario que supervisa publicaciones y contenido.
- **Catálogo:** conjunto consultable de publicaciones de CampusMarket.

### Trazabilidad verificable ASP-05

La fila completa utilizada como evidencia S4 es:

| ID | Aspecto | Requisito | C4 | ADR | Código | Pruebas | Evidencia |
|---|---|---|---|---|---|---|---|
| ASP-05 | Creación de publicaciones | [Alcance funcional - Gestión de publicaciones](docs/arc42/ARC42.md#32-alcance-funcional) | [C4 Nivel 2](docs/c4/02-contenedores.md) | [ADR-0001 - Monolito modular](docs/adr/0001-usar-monolito-modular.md) | [`publicacion_form_page.dart`](frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart), [`publicaciones_api.dart`](frontend/campusmarket/lib/publicaciones/publicaciones_api.dart), [`router.py`](backend/app/publicaciones/router.py), [`service.py`](backend/app/publicaciones/service.py), [`repository.py`](backend/app/publicaciones/repository.py) | [`test_publicaciones_vertical.py`](backend/tests/test_publicaciones_vertical.py) | Evidencia S4 |

La tabla completa de trazabilidad está disponible en:

[`docs/aspectos.md`](docs/aspectos.md)

### Registro de uso de IA

El registro actualizado de herramientas de IA se encuentra en:

[`docs/ia.md`](docs/ia.md)

El registro documenta para cada uso:

- fecha;
- herramienta utilizada;
- uso realizado;
- verificación del equipo;
- qué se rechazó y la justificación técnica.
