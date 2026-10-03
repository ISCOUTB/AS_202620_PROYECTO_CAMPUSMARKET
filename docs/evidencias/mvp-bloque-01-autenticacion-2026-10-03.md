# Bloque 1 — Autenticación y propiedad real

> Registro histórico del bloque. Los pendientes y cifras de este registro
> corresponden a su hash/fecha; el estado acumulado de continuación se encuentra
> en [auditoría MVP](auditoria-mvp-continuacion-2026-10-03.md).

Base: `bfe3222`. Rama: `mvp-autenticacion-producto`. Fecha: 2026-10-03.

| Requisito | Implementación | Ejecución / prueba | Evidencia / estado |
|---|---|---|---|
| Registro y hash seguro | `usuarios/router.py`, `service.py`, `security.py`, `repository.py` | Registro y verificación de hash scrypt N=131072/r=8/p=1; correo único | `test_usuarios.py`; pasa sobre MySQL real |
| Login y usuario actual | Bearer aleatorio; hash SHA-256 en sesiones | Credenciales correctas/incorrectas y `/usuarios/me` | `test_usuarios.py`; pasa |
| Logout y expiración | Borrado de sesión y condición UTC en repository | Reutilizar token después de logout o expiración devuelve 401 | `test_usuarios.py`; pasa |
| Perfil | PATCH nombre, ID y privilegios fuera del body | Perfil propio; registro con privilegios/ID rechazado | `test_usuarios.py`; pasa |
| Propiedad auténtica | Router recibe UsuarioActual; SQL acota al propietario | Dos registros y logins reales | `test_ec02_autorizacion.py`; pasa |
| EC-02 | Autorización en PUT/DELETE y revisión posterior de datos | 10/10 intentos ajenos devuelven 404; datos intactos en cada intento | Ejecución explícita muestra `EC-02: 10/10` |
| Subida propia | Verificación antes de almacenamiento y bloqueo de fila al insertar | Ajeno y anónimo no pueden subir | `test_ec02_autorizacion.py`; pasa; validación de contenido completa queda para bloque 2 |
| Identidad heredada | Migración de DEFAULT 1 a NULL, sin borrado | Registro nuevo no obtiene fila antigua; reinicialización conserva nuevas | `test_migracion_identidad.py`: 2 passed |
| Contrato | `openapi-v2.json`; v1 conservado como histórico | Igualdad exacta proveedor/contrato, Bearer y ausencia de ID de entrada | 4 pruebas de contrato pasan |
| Límites | Conexión compartida sin tablas; cada repository posee su contexto | Modularidad y erosión | 8 pruebas pasan; auditoría se ampliará a administración en bloque 2 |
| Pruebas detectan defecto | `scripts/verificar_mutaciones_mvp.py` | Tres defectos controlados hacen fallar aserciones (exit 1) | 3/3 mutaciones detectadas |

## Resultado ejecutado

- Ruff: pasa, sin ignores nuevos.
- Suite antes de añadir migración: **50 passed**, 25.98 s.
- Migración + autorización: **6 passed**, 9.06 s.
- Contrato/modularidad/erosión: **12 passed**.
- Mutaciones: **3/3 detectadas**, script termina en 0.
- `git diff --check`: pasa.
- MySQL local real: **8.0.46**, instalado de paquetes oficiales Ubuntu en scratch.
  CI usa MySQL **8.4**; no confundir esta ejecución local con CI todavía pendiente.
- Pruebas destructivas de fixtures exigen una base que termine en `_test`.
- Avisos no bloqueantes: deprecación TestClient/httpx y nombre de HTTP 422.

## Riesgos y pendientes

- Flutter todavía usa la identidad anterior hasta el bloque del cliente; este
  commit no declara el MVP completo ni Web/Android cerrados.
- Sesión en memoria del cliente: reinicio requerirá login.
- Imágenes: falta validar decodificación completa y editar principal/eliminar.
- Administración: implementación pendiente; ADR-0014 corrige habilitación por correo.
- La ejecución local de Flutter fue bloqueada por revisión automática por acceso
  a metadatos de nube durante descarga; no se presenta como analyze/build realizado.
- No se ha desplegado ni mergeado esta rama a master.
