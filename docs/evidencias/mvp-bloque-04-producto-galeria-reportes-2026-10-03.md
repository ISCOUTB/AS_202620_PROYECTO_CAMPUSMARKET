# Bloque 04 — producto, fotografías y reportes

Base: 1aefd4526ee5221e92f520969d34c86cb2c64a24.
Estado: implementación pendiente de ejecutar en CI y flujo real.

| Requisito | Implementación | Prueba prevista | Evidencia |
| --- | --- | --- | --- |
| Hasta tres fotos y principal | ImagenesPage, APIs de galería con sesión | Backend validado en bloque 02; flujo real y compilación Flutter | CI y capturas pendientes |
| Propiedad y disponibilidad en catálogo | DTO y modelo extienden contrato v2 | MySQL real verifica propietario A y estado reservado vistos por B | test_catalogo.py |
| Detalle actual | Consulta GET de detalle con loading/error/reintento | Integración con edición, ocultamiento y eliminación | Pendiente |
| Administración mínima | Reporte desde detalle, revisión con nota por moderador | Backend probado; UI consume los endpoints reales | ModeracionPage y futuras pruebas |
| Identidad visual | Portada usa imagen de una publicación existente; precios COP consistentes | Revisión de captura en ambos formatos | Pendiente |
| IA y pruebas sensibles a defecto | Dos mutaciones Flutter y cinco backend | Ejecución automatizada | scripts/verificar_mutaciones_flutter.py |

Se aplican ADR-0012, 0013, 0014 y 0015, sin cambiarlos. Extender DTO y vistas para
capacidades ya decididas no introduce un mecanismo arquitectónico nuevo.
Sin dependencias de producto nuevas en este bloque.
