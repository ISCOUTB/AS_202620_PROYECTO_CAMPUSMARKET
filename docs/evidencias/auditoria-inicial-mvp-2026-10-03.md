# Auditoría inicial del MVP funcional

Fecha: 2026-10-03. Base: `bfe3222c1e29dddc404560cdd9d61095d4bdb3fe`
en `ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET:master`.
PR #47 y #48 integrados. Fork sincronizado mediante fast-forward, sin force.
Rama de trabajo: `mvp-autenticacion-producto`. Clon Linux independiente;
no hay acceso al clon Windows del usuario.

| Criterio | Estado actual | Cambio necesario | Prueba | Evidencia |
|---|---|---|---|---|
| Usuarios | No cumple | Registro, login, logout, sesión revocable, perfil | Credenciales, expiración, revocación | `backend/app/usuarios/__init__.py` es el único archivo |
| Propiedad | No cumple | Identidad obtenida del servidor | Dos usuarios, suplantación | `publicaciones/router.py`, `service.py`, `publicaciones_api.dart` aceptan propietario temporal |
| EC-02 | Parcial | 10/10 intentos ajenos rechazados conservando datos | MySQL real | `docs/arc42/10-escenarios-de-calidad.md` reconoce ausencia de autenticación |
| Imágenes | Parcial | Autorizar, validar contenido, controlar carreras | Subida ajena, máximo tres, archivo inválido | `subir_imagen` no exige identidad; storage solo comprueba extensión |
| Catálogo | Implementación existente | Conservar integración por servicio y revisar UX | Búsqueda, filtros, detalle, imágenes | `catalogo/service.py` no importa repository ajeno |
| Administración | No cumple | Reportes y moderación mínima | Reportar, revisar, ocultar, denegar a no moderador | Solo `__init__.py` |
| UX | Parcial | Autenticación, perfil, navegación y actualización de datos | Recorridos responsive | Detalle contiene botón de contacto deshabilitado |
| Arquitectura/OpenAPI | Cumple sobre base | Evolucionar decisiones y contrato | 11 pruebas | Ruff y `pytest` contrato/modularidad/erosión: 11 passed |
| Web/Android | No verificado en este entorno | Preparar SDK, compilar y ejecutar | Analyze, builds, recorrido | SDK no estaba instalado |
| CI | Cumple sobre base | Verificar nueva rama/hash | Run de Actions | [37123324994](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37123324994) success |
| SonarCloud | Gate verde sobre base; cadena del scanner pendiente | Verificar nueva revisión y cadena del CONTRATO §8 | Check y run scanner | Check SonarCloud de `bfe3222`: success; workflow no invoca scanner |
| Secretos | Sin hallazgos reales en barrido inicial | Repetir antes de entregar | Árbol e historial, salida redactada | Sin tokens/keys ni `.env` versionado. `1febc85` coincide por comandos de barrido documentados |
| Despliegue | Parcial | Docker, Compose, persistencia y configuración | Validación reproducible | Bicep presente; Compose ausente |

## Fuentes y límites

- Guía adjunta: bienvenida; explica 17 semanas y revisión de IA, pero no contiene
  los once capítulos completos. No se le atribuyen rúbricas ausentes.
- Plantilla arc42 adjunta: versión 9.0-EN, julio de 2025.
- CONTRATO vigente obtenido de `ISCOUTB/AS_202620_feedback/CONTRATO.md`.
- Feedback S9 publicado evalúa `784d788`, **no** esta base nueva; se conservan
  sus pendientes transversales, sin tratarlo como revisión de `bfe3222`.
- `git diff --check`: pasa sobre base limpia.
- Los valores de MySQL del workflow son fixtures efímeros de CI, no secretos
  productivos. No se publican valores de credenciales reales.

## Bloques autorizados

1. Autenticación y propiedad, cuarentena de publicaciones heredadas, EC-02.
2. Administración mínima e imágenes seguras; contrato y límites.
3. Flutter: sesión en memoria, acceso protegido, perfil, moderación, UX e imágenes.
4. Evidencias reproducibles, CI, SonarCloud y documentación coincidente.

No se despliega mientras queden criterios de cierre sin evidencia.
