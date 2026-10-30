# ADR-0024 — Publicar imagen verificada y condicionar su promoción

- **Estado:** Aceptada para la publicación de artefactos; promoción a producción **aplazada**.
- **Fecha:** 2026-10-30.
- **Ámbito:** CI/CD y operación de CampusMarket. No sustituye el ADR-0001 ni los ADR funcionales existentes.

## Contexto y problema

Durante la auditoría del Compose de Dokploy se detectó que la variable `CAMPUSMARKET_REVISION` conservaba el SHA `7856416795bb4accdf9d05e01adb470654875e56` pese a existir merges posteriores. No fue posible corroborar el encabezado `X-CampusMarket-Revision` por un 403 en el cliente utilizado. Por tanto, no debe afirmarse que el encabezado HTTP público se comprobó incorrecto: se detectó una **brecha de trazabilidad verificable**.

El despliegue activo reconstruye `api` desde GitHub. Queremos evitar que la imagen probada por CI y la imagen desplegada sean construcciones distintas, preservando MySQL y los archivos persistentes.

## Alternativas

| Alternativa | Ventajas | Costos y riesgos |
|---|---|---|
| Mantener builds independientes en CI y Dokploy | Menor cambio operativo inmediato | No acredita identidad entre artefacto probado y artefacto desplegado |
| Construir y probar una vez; publicar en GHCR por digest | Procedencia verificable, artefacto reutilizable e identidad inmutable | Requiere permisos de registro, verificación de digest y estrategia de promoción |
| Migrar inmediatamente la API a GHCR | Materializa pronto la ruta objetivo | Sin respaldo ni rollback acreditados, expone a interrupciones o pérdida de recuperabilidad |

## Decisión

**Aceptar** construir una imagen una sola vez, probarla en CI, exportar ese artefacto, verificar SHA/etiqueta OCI/`/app/REVISION`, publicarlo manualmente en GHCR y fijarlo por digest en un Compose alternativo.

**No activar aún** el Compose de producción en Dokploy. La promoción requiere verificar el acceso al paquete Internal, montajes efectivos, respaldos recuperables, imagen anterior y gestión de autodeploy. No se autoriza cambiar el Compose activo ni iniciar/recrear MySQL como consecuencia de este ADR.

## Consecuencias y atributos de calidad

- **Trazabilidad y auditabilidad:** secuencia commit → CI → `api.tar` → GHCR/digest documentada.
- **Reproducibilidad:** la imagen de GHCR es la misma imagen exportada por CI, no una reconstrucción posterior.
- **Desplegabilidad:** `deploy/compose.prod.yaml` representa la configuración objetivo, todavía no utilizada en producción.
- **Disponibilidad y recuperabilidad:** se preserva el servicio activo mientras no existan respaldos y rollback acreditados.
- **Seguridad:** las credenciales GHCR se manejarán fuera del repositorio, por mecanismos autorizados; no se publican secretos.
- **Costo:** se aprovecha GitHub Actions y GHCR ya disponibles; no se incorpora infraestructura adicional al servicio.

## Evidencias y límites

- Commit probado: `2154e7880e5111537256206a29f4f4c29a8c86c4`.
- CI Compose: [run 41024201484](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41024201484).
- Verificación sin publicar: [run 41025785578](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41025785578).
- Publicación verificada: [run 41026286264](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41026286264).
- Imagen: `ghcr.io/iscoutb/campusmarket-api@sha256:f9eaabdb166274225e9ad490c44999f71f6b1f7c9c5902dc68ab98b07115ce8b`.
- Compose alternativo: [`deploy/compose.prod.yaml`](../../deploy/compose.prod.yaml).
- Evidencia completa: [`evidencia-ghcr-cierre.md`](../operacion/evidencia-ghcr-cierre.md).

La publicación **no** acredita acceso desde Dokploy, actualización de API, persistencia en ejecución ni rollback ensayado.

## Revisión de esta decisión

Revisar cuando un operador autorizado acredite la imagen y los montajes reales, respaldos consistentes y recuperación probada, autenticación GHCR desde el servidor, control del autodeploy y procedimiento de actualización únicamente de `api`.
