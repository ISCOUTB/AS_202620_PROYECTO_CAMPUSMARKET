# Bloque 04 — producto, fotografías y reportes

Base: 1aefd4526ee5221e92f520969d34c86cb2c64a24.
Estado: validaciones de código y builds aprobadas; flujo real en bloque 05.
Hash: d94cc62c783184c492cbfd70e058ff58c7d6a7e2.
Backend: https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37131600619
Flutter: https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37131600565

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

## Resultado comprobado

68 pruebas backend aprobadas (64 funcionales/arquitectónicas y 4 de contrato).
Cinco mutaciones backend detectadas. Flutter analyze sin observaciones, seis
pruebas aprobadas, dos mutaciones detectadas y builds Web/Android aprobados.
git diff --check aprobado. FastAPI excluye default null en el esquema publicado;
se corrigió el snapshot conservando el tipo nullable, sin cambiar la API.
La revisión visual completa continúa con las capturas del flujo real.
