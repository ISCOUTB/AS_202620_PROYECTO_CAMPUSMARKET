# Bloque 03 — integración de sesión en Flutter

Base: ecab64bd5bea13a9c074229789e73b29f3eac821.
Estado: implementación preparada; validación Flutter pendiente de CI.

| Requisito | Implementación | Prueba | Evidencia requerida |
| --- | --- | --- | --- |
| Registro y login | AuthPage y SessionController, API usuarios | Flujo real Web/Android pendiente; validación responsive de formulario | Runner y artefactos del hash |
| Sesión y logout | Bearer en memoria, expiración y revocación remota | Logout fallido conserva sesión; 401 elimina la identidad que originó la petición | session_authorization_test.dart |
| Propiedad real | PublicacionesApi omite propietario y transmite sesión | Crear y listar mías verifican body, query y Authorization | session_authorization_test.dart |
| Aislamiento de dos cuentas | Recreación de vistas privadas por identidad | Respuesta antigua de A no invalida sesión B; prueba UI completa pendiente | session_authorization_test.dart y futura integración |
| Formularios | Precio normalizado y reintento de imágenes sobre el mismo id | Revisión de implementación; integración pendiente | publicacion_form_page.dart |
| Web y Android | CI SDK 3.47.3; INTERNET en manifest principal; HTTP solo en debug | analyze, pruebas y builds | flutter-mvp.yml |

No se agregan dependencias de ejecución. flutter_test y http/testing ya pertenecen
al stack. La infraestructura CI usa versiones verificadas de acciones mantenidas.
Los builds con backend local son artefactos de validación, no despliegues.

La terminal perdió conexión después de publicar el bloque 02. Los cambios de este
bloque se preservan en GitHub. No se declara working tree local sincronizado hasta
recuperar acceso y comprobarlo. No se declara cerrado el MVP por compilar.

Riesgos pendientes: verificar subida nativa desde selector, galería editable,
reportes desde detalle, cola de moderación, responsive completo y flujo real con
dos usuarios en ambas plataformas. Una respuesta de red perdida tras un POST
puede dejar un resultado incierto; el reintento de imágenes conserva el id conocido
y no pretende proporcionar idempotencia global del protocolo.
