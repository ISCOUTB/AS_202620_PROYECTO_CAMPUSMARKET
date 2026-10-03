# ADR-0015 — Validar y reencodificar imágenes con Pillow

- Estado: Aceptado
- Fecha: 2026-10-03
- Relación: extiende ADR-0011 sin reescribirlo. Mantiene archivos locales en
  desarrollo y volumen persistente para el entorno Compose futuro.

## Contexto

ADR-0011 admite hasta tres imágenes y 5 MiB por imagen. El código comprobaba
solo la extensión: texto o contenido corrupto con nombre JPG se aceptaba.
Necesitamos verificar decodificación, acotar memoria y retirar EXIF/metadatos.

## Alternativas

1. Extensión y firma manual con biblioteca estándar: no verifica el contenido
   completo ni permite retirar metadatos de forma fiable.
2. Servicio externo de imágenes: añade costo, credenciales y red fuera del MVP.
3. Pillow: decodifica formatos existentes y permite reencodificar sin metadatos.

## Decisión

Incorporar únicamente `Pillow==12.3.0` al backend. Proyecto mantenido en la
organización `python-pillow`; versión existente comprobada en PyPI mediante
JSON oficial, Python >=3.10, wheels CPython 3.12 para Linux y Windows. Licencia
verificada en el registro; no contradice la política de dependencias del curso:
se declara necesidad, fuente, versión y verificación ejecutable.

Validar JPG/PNG/WEBP con formato concordante, decodificar completamente y
reencodificar en un archivo con UUID. Rechazar imágenes vacías, corruptas,
mayores de 5 MiB o 20 megapíxeles. Limitar decodificación concurrente a dos
operaciones; ejecutarlas fuera del event loop. No copiar EXIF ni comentarios.

Propiedad se verifica antes de almacenar y dentro de la transacción de metadata.
Serializar inserciones de imágenes mediante bloqueo de la publicación;
garantizar máximo tres en concurrencia. Elegir principal y eliminar foto solo
para el propietario, con sustitución de principal cuando corresponde.

## Trade-offs y consecuencias

- Añade un paquete mantenido con ruedas nativas y requiere actualizaciones.
- Reencodificar tiene costo CPU y puede cambiar compresión; evita publicar
  contenido sin decodificar y metadatos privados.
- Transacción SQL y escritura de archivo son diferentes: compensar inserciones
  fallidas, y documentar que un crash puede dejar un archivo huérfano.
- Directorio de uploads configurable, fuera de Git y persistido por volumen.
- No se incorpora pytest-cov: medir cobertura no es necesario para validar
  este comportamiento y la mutación ya demuestra detección del defecto.

## Fuentes y trazabilidad

- [Registro oficial versión](https://pypi.org/pypi/Pillow/12.3.0/json)
- [Mantenedor/código](https://github.com/python-pillow/Pillow)
- [Documentación](https://pillow.readthedocs.io/en/stable/reference/Image.html)
- CONTRATO §9 y ficha S9: dependencias propuestas verificadas y sin secretos.
- Código: `publicaciones/image_storage.py`, `repository.py`, `service.py`.
- Prueba: `test_imagenes_seguras.py`; evidencia en bloque 2 del MVP.
