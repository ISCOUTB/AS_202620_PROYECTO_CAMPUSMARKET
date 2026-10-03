# ADR-0018 — Ejecutar el monolito en Dokploy con volúmenes

- Estado: Aceptado para preparación; despliegue pendiente del cierre del MVP.
- Fecha: 2026-10-03
- Relación: extiende ADR-0001, ADR-0004 y ADR-0016. Sustituye la elección de
  Azure como backend principal de ADR-0005/0007/0008 para la próxima fase;
  Azure se conserva como segundo entorno de portabilidad. Extiende ADR-0011
  con almacenamiento durable Compose sin reescribir ninguno de esos ADR.

## Contexto

El usuario establece GitHub Pages para Flutter Web, Dokploy/iscoutb.dev para
el backend principal y Azure como segundo entorno. La guía del curso fija
límites sumados <=512 MB, red aislada, dominio propio, HTTPS en Traefik y
volúmenes con nombre. Las imágenes no pueden persistirse solo en el
filesystem efímero del contenedor.

## Alternativas

1. Continuar únicamente Azure: no satisface la prioridad operativa actual.
2. Servicio de objetos externo: portabilidad y escala, a costo de nueva
   dependencia, servicio y secretos fuera de la necesidad del MVP.
3. API única + MySQL en Compose, volúmenes para datos e imágenes y frontend
   en Pages: encaja con la cuota y mantiene las fronteras del monolito.

## Decisión

Elegir 3. deploy/compose.lab.yaml contiene API y MySQL 8.4, 256 MiB y 0,5 CPU
por contenedor; sin ports, bind mounts, container_name ni privilegios.
Solo el override local publica API en 127.0.0.1:8000. Flutter no se compila
ni se sirve en el laboratorio. Dokploy conserva Isolated Deployment.

La imagen API usa Python oficial 3.12.15-slim-bookworm, proceso no root,
un worker y límite de concurrencia 6. MySQL sigue la configuración oficial
de memoria del laboratorio. Volúmenes nombrados conservan MySQL y uploads
entre reinicios/recreaciones. Las variables sensibles son obligatorias en
Environment; no hay passwords por defecto ni valores en .env.example.

HTTPS público termina en el proxy del laboratorio, servicio api:8000 con
dominio campusmarket.iscoutb.dev. CORS admite el origen Pages autorizado.
El build recibe un SHA público, lo conserva en REVISION y en etiqueta OCI;
la verificación compara /health, etiqueta del contenedor y hash aprobado.

En Azure, mantener TLS a MySQL y almacenar imágenes en /home persistente,
o montar almacenamiento durable equivalente antes de habilitar publicaciones.
No multiplicar instancias con filesystem local sin almacenamiento compartido.
No efectuar despliegue, aprovisionamiento ni gasto al preparar este ADR.

## Trade-offs y consecuencias

- Una API y dos volúmenes simplifican la operación; no ofrecen alta disponibilidad.
- SQL y filesystem no comparten transacción; permanecen compensación y riesgo
  de huérfanos tras crash documentados en ADR-0015.
- Reinicio de contenedores conserva datos; down -v o cierre del semestre los
  elimina. La guía no garantiza backups: exigir exportación verificable antes
  de tocar volúmenes con datos reales.
- Los tags oficiales se registran con sus IDs/digests en evidencia del build;
  la imagen aprobada debe desplegarse por su digest al cerrar el MVP.
- Rollback de código no revierte migraciones de datos; usar solo versiones
  compatibles con la migración de identidad del ADR-0017.

## Fuentes y verificación

[Guía oficial](https://github.com/ISCOUTB/iscoutb.dev/blob/main/README.md),
[políticas](https://github.com/ISCOUTB/iscoutb.dev/blob/main/docs/politicas-uso.md),
[imagen Python oficial](https://github.com/docker-library/official-images/blob/master/library/python).

CI valida Compose, límites efectivos, cuatro contextos con HTTP/MySQL, sesión
e imágenes después del reinicio, ausencia de OOM y hash de la imagen.
La evidencia de CI prepara despliegue; no demuestra una URL pública desplegada.
