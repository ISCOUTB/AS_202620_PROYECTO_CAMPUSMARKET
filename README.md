# CampusMarket

Marketplace universitario para la compra, venta y alquiler de productos.

## Integrantes

- Joshua Tenorio Alvarez
- Camilo Martinez Berrio
- Nilver Garcia Pimentel

## Estrategia arquitectónica

CampusMarket adopta un **monolito modular** de acuerdo con [ADR-0001](docs/adr/0001-usar-monolito-modular.md).

Fronteras principales del backend:

- `usuarios`
- `publicaciones`
- `catalogo`
- `administracion`

La Evidencia S4 materializa un corte vertical en `publicaciones`.

## Tecnologías actuales

- **Frontend:** Flutter / Dart.
- **Backend:** FastAPI / Python.
- **Persistencia del corte S4:** SQLite.
- **Persistencia prevista para evolución posterior:** MySQL.

> La documentación distingue lo que existe de lo previsto: S4 usa SQLite porque es la persistencia realmente implementada en el corte vertical.

## Requisitos previos

- Python 3.12.
- Flutter instalado y disponible en `PATH`.
- Google Chrome.
- Dependencias Python instaladas:

```bash
pip install -r backend/requirements.txt
```

## Arranque del corte vertical con un solo comando

### Windows PowerShell

Desde la raíz del repositorio:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_s4.ps1
```

El comando inicia:

- Backend FastAPI: `http://localhost:8000`
- Frontend Flutter Web: `http://localhost:3000`

### Linux/macOS

```bash
bash scripts/run_s4.sh
```

## Corte vertical S4: crear una publicación

Recorrido implementado:

1. El estudiante completa el formulario Flutter.
2. Flutter envía `POST /publicaciones`.
3. FastAPI valida la solicitud.
4. El módulo `publicaciones` ejecuta la lógica.
5. El repositorio guarda el dato en SQLite.
6. La API devuelve la publicación persistida.
7. Flutter confirma el resultado.

Rutas principales:

- UI: `frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart`
- Cliente API: `frontend/campusmarket/lib/publicaciones/publicaciones_api.dart`
- Interfaz backend: `backend/app/publicaciones/router.py`
- Lógica: `backend/app/publicaciones/service.py`
- Persistencia: `backend/app/publicaciones/repository.py`

## Pruebas automatizadas

```bash
python -m pytest backend/tests -q
```

Pruebas relevantes:

- `backend/tests/test_health.py`
- `backend/tests/test_publicaciones_vertical.py`

La prueba S4 crea una publicación mediante HTTP, verifica que SQLite persista el dato y vuelve a consultarlo.

## Documentación S4

- arc42 5: `docs/arc42/05-bloques-de-construccion.md`
- arc42 6: `docs/arc42/06-vista-ejecucion.md`
- arc42 9: `docs/arc42/09-decisiones.md`
- arc42 10: escenarios existentes de S2
- arc42 12: `docs/arc42/12-glosario.md`
- C4 Nivel 1: `docs/c4/01-contexto.puml`
- C4 Nivel 2: `docs/c4/02-contenedores.puml`
- Trazabilidad: `docs/aspectos.md`

## Alcance del corte S4

S4 demuestra una ruta funcional mínima. No implementa todavía pagos, envíos, logística, autenticación completa ni todas las capacidades del marketplace. Estas funciones no se documentan como existentes.
