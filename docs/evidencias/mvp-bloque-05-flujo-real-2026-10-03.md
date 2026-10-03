# Bloque 05 — ejecución real en Web y Android

Base: d94cc62c783184c492cbfd70e058ff58c7d6a7e2.
Estado: prueba implementada y pendiente de ejecutar.

Se ejecuta el mismo flujo en Chrome 1440×1000, Chrome 390×844 y Android API 35.
Cada runner contiene MySQL 8.4, backend de este hash y cuentas sintéticas propias.
No se usan cuentas ni datos de producción.

## Requisito → implementación → prueba → evidencia

- Registro/login/logout/perfil: widgets y usuarios API; registro A/B/moderador,
  inicio de sesión y rechazo del token anterior tras logout; resultado.json.
- Publicar con identidad real: formulario con precio con coma y archivo elegido
  en el selector; API y MySQL devuelven propietario A y precio normalizado.
- Galería: tres archivos elegidos y subidos, rechazo de cuarto en servidor,
  cambio de principal y eliminación con URL retirada; capturas y aserciones.
- Catálogo/detalle: portada real, tarjetas y detalle actual; disponibilidad y
  galería visible; capturas PNG.
- EC-02: B intenta editar, cambiar estado, eliminar y modificar imágenes de A,
  además de suplantar propietario por query; HTTP 404 y datos intactos tras
  cada intento, Mis publicaciones B vacías y moderación 403.
- Administración: B registra un reporte, moderador habilitado en el entorno de
  prueba revisa motivo y oculta con nota; catálogo 404, propietario conserva gestión.
- Cierre: A elimina la publicación oculta y sus archivos, luego logout revocado.

La cuenta de moderación usa ID 3 únicamente porque el entorno de prueba vacío
crea A, B y la cuenta controlada en ese orden; su ID y flag retornado se validan.
Esto no es una configuración ni una identidad recomendada para producción.
Producción mantiene la capacidad deshabilitada hasta seleccionar una cuenta
existente y verificada fuera del registro público (ADR-0014).

Artefactos por hash: resultado.json, PNG por etapa, índice visual, hash.txt,
flutter-version.txt, versión ChromeDriver, logs backend sin credenciales y
registro del selector. No se escriben tokens/contraseñas en resultado ni logs.

Se añade integration_test exclusivamente desde SDK (desarrollo), justificado en
docs/dependencias-mvp.md. Sin cambios de decisiones arquitectónicas ni despliegue.
