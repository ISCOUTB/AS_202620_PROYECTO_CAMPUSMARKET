# ADR-0016 — Ajustar recursos a la cuota del laboratorio

- Estado: Aceptado
- Fecha: 2026-10-03
- Relación: extiende ADR-0001 y ADR-0012; reemplaza la concurrencia de dos
  decodificaciones de ADR-0015. No altera sus versiones aceptadas.

## Contexto

La guía oficial ISCOUTB/iscoutb.dev exige como máximo 512 MB por equipo,
0,5 CPU por contenedor, MySQL 8.4 y Flutter Web fuera del laboratorio.
scrypt N=2^17 usa aproximadamente 128 MiB. Dos hashes y dos imágenes
de 20 MP simultáneos pueden exceder el presupuesto antes de contar MySQL.

## Alternativas

1. Reducir scrypt: degrada protección de contraseñas para compensar la cuota.
2. Externalizar autenticación/imágenes: nuevos servicios y credenciales sin
   justificación funcional para este monolito.
3. Un proceso, trabajo intensivo serial y normalización de fotografías:
   menor throughput, manteniendo protección y archivos de cámaras habituales.

## Decisión

Elegir 3. Reservar 256 MiB para API y 256 MiB para MySQL. Uvicorn tiene un
worker y límite de concurrencia 6 (incluye conexiones). Una semáfora compartida
de infraestructura serializa scrypt y decodificación/reencodificación, sin
compartir datos de dominio ni permitir SQL entre contextos.

Mantener scrypt N=2^17, r=8, p=1. Admitir imágenes hasta 20 MP y 5 MiB,
normalizarlas a un lado máximo de 2048 px antes de convertir y copiar, aplicar
orientación EXIF antes de retirarla. El archivo normalizado debe seguir <=5 MiB.

Acotar cuerpos HTTP a 64 KiB para JSON y 6 MiB para multipart (una imagen por
solicitud), antes del parser, también sin Content-Length; responder 413.
El límite individual de archivo de 5 MiB permanece en Publicaciones.
No añadir paquetes: threading, Starlette y Pillow ya forman parte del stack.

## Trade-offs

- Los hashes se serializan; la cola HTTP queda acotada por Uvicorn.
- Saturación devuelve 503 y el cliente permite reintentar.
- La imagen pública pierde resolución por encima de 2048 px; resulta adecuada
  para tarjetas/detalle del MVP y reduce memoria/transferencia.
- Un worker impide escalado horizontal sin revisar el presupuesto y la guardia.
- Las transacciones de datos permanecen en sus repositories propietarios.

## Consecuencias y verificación

Docker Compose fija los límites y el comando; CI ejecutará registro concurrente,
subida de una imagen grande, reinicio con persistencia y lectura de memory.peak.
No se presenta una estimación como medición ni un build como despliegue público.

Fuentes: [políticas del laboratorio](https://github.com/ISCOUTB/iscoutb.dev/blob/main/docs/politicas-uso.md),
[plantilla MySQL](https://github.com/ISCOUTB/iscoutb.dev/blob/main/plantillas/compose.lab.mysql.yaml),
[Image.thumbnail](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.thumbnail),
[hashlib](https://docs.python.org/3.12/library/hashlib.html).
