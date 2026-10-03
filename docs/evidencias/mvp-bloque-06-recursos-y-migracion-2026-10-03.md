# Bloque 06 — recursos, fotografías de cámara y migración segura

Estado: pruebas de código aprobadas en 0eba3f423775a5fce716119bf336231441ba2729.
Ruff y 76 pruebas (72 funcionales/arquitectura + 4 contrato), nueve mutaciones
detectadas: [backend](https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37140687982).
Flutter analyze, seis pruebas, dos mutaciones, build Web y APK:
[Flutter](https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37140687986).
Flujos reales desktop/móvil/Android con concurrencia 6 y 19 capturas cada uno:
[flujo](https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37140687994).
Medición del Compose bajo 512 MiB pendiente del bloque 07.

## Requisito → implementación → prueba → evidencia

| Requisito | Implementación | Prueba | Evidencia prevista |
|---|---|---|---|
| Cuota oficial de 512 MB | ADR-0016, trabajo intensivo serial y un worker | Compose con memoria acotada, registros concurrentes e imagen de 12 MP | límites y memory.peak del contenedor |
| Fotografías de cámara | thumbnail 2048 y orientación EXIF antes de retirar metadata | PNG 4000×3000 → 2048×1536; JPEG orientación 6 → 60×100 sin EXIF | pytest y dos mutaciones |
| Solicitudes acotadas | Middleware antes del parser, 64 KiB JSON / 6 MiB multipart | Content-Length y transferencia sin ese header, HTTP 413 | pytest, mutación del contador y OpenAPI v2 |
| Privacidad de sesión/logs | no-store y UUID de correlación | dos cuentas sin caché; texto arbitrario no llega a logs | pytest |
| Retirar identidad temporal en concurrencia | ADR-0017, GET_LOCK durante DDL/migración | segundo inicializador espera; conserva fila heredada sin dueño y nueva fila autenticada | MySQL real y mutación SELECT 1 |

Los ADR aceptados 0012 y 0015 permanecen intactos. El límite de 20 MP y 5 MiB
se conserva; la imagen pública se normaliza para el catálogo.
No se incorporan paquetes, servicios independientes ni secretos.
