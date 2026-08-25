# Aspectos del proyecto - CampusMarket

Este documento mantiene la trazabilidad de los aspectos de CampusMarket desde los requisitos y decisiones arquitectónicas hasta su implementación y evidencia verificable.

La cadena de trazabilidad utilizada es:

**Aspecto → Requisito → C4 → ADR → Código → Pruebas → Evidencia**

| ID | Aspecto | Requisito | C4 | ADR | Código | Pruebas | Evidencia |
|---|---|---|---|---|---|---|---|
| ASP-01 | Consulta y búsqueda de productos | [EC-01 - Consulta de productos](./arc42/10-escenarios-de-calidad.md#ec-01---consulta-de-productos) | [C4 Nivel 2](./c4/02-contenedores.md) | — | — | — | — |
| ASP-02 | Gestión segura de publicaciones | [EC-02 - Protección de publicaciones](./arc42/10-escenarios-de-calidad.md#ec-02---protección-de-publicaciones) | [C4 Nivel 1](./c4/01-contexto.md) | — | — | — | — |
| ASP-03 | Evolución de la gestión de productos | [EC-03 - Modificación del sistema](./arc42/10-escenarios-de-calidad.md#ec-03---modificación-del-sistema) | [C4 Nivel 2](./c4/02-contenedores.md) | [ADR-0001 - Monolito modular](./adr/0001-usar-monolito-modular.md) | [`backend/app/publicaciones/`](../backend/app/publicaciones/), [`publicacion_form_page.dart`](../frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart) | [`test_publicaciones_vertical.py`](../backend/tests/test_publicaciones_vertical.py) | Evidencia S3/S4 |
| ASP-04 | Recuperación del prototipo | [EC-04 - Recuperación del prototipo](./arc42/10-escenarios-de-calidad.md#ec-04---recuperación-del-prototipo) | [C4 Nivel 1](./c4/01-contexto.md) | [ADR-0001 - Monolito modular](./adr/0001-usar-monolito-modular.md) | [`scripts/run_s4.ps1`](../scripts/run_s4.ps1) | [`test_health.py`](../backend/tests/test_health.py) | Evidencia S3/S4 |
| ASP-05 | Creación de publicaciones | [Alcance funcional - Gestión de publicaciones](./arc42/ARC42.md#32-alcance-funcional) | [C4 Nivel 2](./c4/02-contenedores.md) | [ADR-0001 - Monolito modular](./adr/0001-usar-monolito-modular.md) | [`publicacion_form_page.dart`](../frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart), [`publicaciones_api.dart`](../frontend/campusmarket/lib/publicaciones/publicaciones_api.dart), [`router.py`](../backend/app/publicaciones/router.py), [`service.py`](../backend/app/publicaciones/service.py), [`repository.py`](../backend/app/publicaciones/repository.py) | [`test_publicaciones_vertical.py`](../backend/tests/test_publicaciones_vertical.py) | Evidencia S4 |

## Estado de trazabilidad S4

La fila **ASP-05 - Creación de publicaciones** queda completa hasta la columna **Pruebas**, cumpliendo el mínimo solicitado para la Evidencia S4.

La trazabilidad del corte vertical corresponde al recorrido:

**Interfaz Flutter → API FastAPI → lógica del módulo `publicaciones` → persistencia SQLite.**

Durante la verificación local se creó una publicación desde la interfaz Flutter y se comprobó posteriormente su almacenamiento en SQLite, por lo que las rutas indicadas corresponden al comportamiento real del prototipo.

## Verificación de EC-03 en S4

Durante el ajuste final de la Evidencia S4 se incorporó el estado de producto `reacondicionado`, utilizado como caso concreto para verificar el escenario **EC-03 - Modificación del sistema**.

El cambio se mantuvo dentro de la capacidad funcional de `publicaciones` y requirió ajustes únicamente en los elementos directamente relacionados con la creación, validación y persistencia de publicaciones.

No fue necesario modificar los módulos de autenticación ni búsqueda, manteniendo las fronteras definidas por el **ADR-0001 - Monolito modular**.

La prueba automatizada [`test_publicaciones_vertical.py`](../backend/tests/test_publicaciones_vertical.py) crea una publicación con estado `reacondicionado`, verifica su persistencia en SQLite y posteriormente recupera el registro para comprobar que el nuevo estado se conserva correctamente.

De esta forma queda trazada la relación:

**EC-03 → ADR-0001 → módulo `publicaciones` → código → prueba automatizada.**
