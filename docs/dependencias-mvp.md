# Dependencias incorporadas para el MVP

Las incorporaciones se contrastan con CONTRATO (pruebas, trazabilidad, ADR y
evidencia) y las fuentes de curso disponibles. No se presenta la guía de bienvenida
como si contuviera los once capítulos del curso.

## Producto: Pillow 12.3.0

Necesidad: decodificar contenido real, verificar formato, limitar píxeles y
reencodificar las imágenes eliminando metadatos. Ver ADR-0015 y evidencia bloque 02.
No basta con extensión o firma del archivo y no existe equivalente en la
biblioteca estándar que verifique estos formatos completos.
Verificado Python >=3.10, CPython 3.12 y wheels Linux/Windows; mantenedor
python-pillow/Pillow, licencia MIT-CMU.
Fuente: https://pypi.org/pypi/Pillow/12.3.0/json
Repositorio: https://github.com/python-pillow/Pillow
Sin cambios de decisión en ADR aceptados.

## Desarrollo: integration_test del SDK Flutter 3.47.3

Necesidad: ejecutar el flujo sobre Chrome real y Android real emulado con el
backend/MySQL, seleccionar archivos y capturar las pantallas. flutter_test ya
existente valida widgets, pero no sustituye ejecución de la aplicación en un
dispositivo. Pruebas HTTP aisladas no prueban navegación, renderizado ni integración
del selector del sistema.
Mantenedor: equipo Flutter, paquete incluido en el SDK, versión alineada a 3.47.3,
solo dev_dependencies. No participa en el bundle Web/APK de producción.
Fuente: https://docs.flutter.dev/testing/integration-tests
Fuente: https://github.com/flutter/flutter/tree/3.47.3/packages/integration_test
Sus dependencias de prueba transitivas son resueltas por el SDK y se registran en
pubspec.lock; no se añaden paquetes externos para sesiones, estado ni automatización.

## Herramientas de CI

- flutter-action, subosito: prepara SDK oficial, hash v2 verificado y fijado.
- android-emulator-runner, ReactiveCircus: ejecuta Android API 35, x86_64, KVM,
  hash v2 verificado y fijado. Es una herramienta de ejecución, no un paquete del app.
- checkout v5, setup-python v6 y setup-java v5: acciones oficiales de GitHub,
  referencias verificadas y fijadas; evitan versiones de Node retiradas.
- ChromeDriver: descarga oficial de Google cuyo build coincide con Chrome del
  runner; versiones quedan en artefacto. Usa Python urllib/zipfile, sin otro paquete.
- El puente del selector usa ChromeDriver/W3C y adb/uiautomator del SDK Android.
  En Web entrega un archivo real al input HTML del plugin; en Android opera
  DocumentsUI. No reemplaza el plugin por un mock.

No se incorpora pytest-cov. No se incorporan Pillow para estética, proveedores
OAuth, JWT, almacenamiento de token en navegador, una biblioteca adicional de
estado, Patrol, Selenium Python ni Playwright.
