\# Aspectos del proyecto - CampusMarket



Este documento mantiene la trazabilidad de los aspectos de CampusMarket desde los requisitos y decisiones arquitectónicas hasta su implementación y evidencia verificable.



La cadena de trazabilidad utilizada es:



\*\*Aspecto → Requisito → C4 → ADR → Código → Pruebas → Evidencia\*\*



| ID | Aspecto | Requisito | C4 | ADR | Código | Pruebas | Evidencia |

|---|---|---|---|---|---|---|---|

| ASP-01 | Consulta y búsqueda de productos | \[EC-01 - Consulta de productos](./arc42/10-escenarios-de-calidad.md#ec-01---consulta-de-productos) | \[C4 Nivel 2](./c4/02-contenedores.md) | — | — | — | — |

| ASP-02 | Gestión segura de publicaciones | \[EC-02 - Protección de publicaciones](./arc42/10-escenarios-de-calidad.md#ec-02---protección-de-publicaciones) | \[C4 Nivel 1](./c4/01-contexto.md) | — | — | — | — |

| ASP-03 | Evolución de la gestión de productos | \[EC-03 - Modificación del sistema](./arc42/10-escenarios-de-calidad.md#ec-03---modificación-del-sistema) | \[C4 Nivel 2](./c4/02-contenedores.md) | \[ADR-0001 - Monolito modular](./adr/0001-usar-monolito-modular.md) | \[`backend/app/publicaciones/`](../backend/app/publicaciones/) | — | Evidencia S3/S4 |

| ASP-04 | Recuperación del prototipo | \[EC-04 - Recuperación del prototipo](./arc42/10-escenarios-de-calidad.md#ec-04---recuperación-del-prototipo) | \[C4 Nivel 1](./c4/01-contexto.md) | \[ADR-0001 - Monolito modular](./adr/0001-usar-monolito-modular.md) | \[`scripts/run\_s4.ps1`](../scripts/run\_s4.ps1) | \[`test\_health.py`](../backend/tests/test\_health.py) | Evidencia S3/S4 |

| ASP-05 | Creación de publicaciones | \[Alcance funcional - Gestión de publicaciones](./arc42/ARC42.md#32-alcance-funcional) | \[C4 Nivel 2](./c4/02-contenedores.md) | \[ADR-0001 - Monolito modular](./adr/0001-usar-monolito-modular.md) | \[`publicacion\_form\_page.dart`](../frontend/campusmarket/lib/publicaciones/publicacion\_form\_page.dart), \[`publicaciones\_api.dart`](../frontend/campusmarket/lib/publicaciones/publicaciones\_api.dart), \[`router.py`](../backend/app/publicaciones/router.py), \[`service.py`](../backend/app/publicaciones/service.py), \[`repository.py`](../backend/app/publicaciones/repository.py) | \[`test\_publicaciones\_vertical.py`](../backend/tests/test\_publicaciones\_vertical.py) | Evidencia S4 |



\## Estado de trazabilidad S4



La fila \*\*ASP-05 - Creación de publicaciones\*\* queda completa hasta la columna \*\*Pruebas\*\*, cumpliendo el mínimo solicitado para la Evidencia S4.



La trazabilidad corresponde al corte vertical ejecutado:



\*\*Interfaz Flutter → API FastAPI → lógica del módulo `publicaciones` → persistencia SQLite.\*\*



Durante la verificación local se creó una publicación desde la interfaz Flutter y se comprobó posteriormente su almacenamiento en SQLite, por lo que las rutas indicadas corresponden al comportamiento real del prototipo.
