# ADR-0024 â€” Publicar imagen verificada y condicionar su promociÃ³n

- **Estado:** Aceptada para la publicaciÃ³n de artefactos; promociÃ³n a producciÃ³n **aplazada**.
- **Fecha:** 2026-10-30.
- **Ãmbito:** CI/CD y operaciÃ³n de CampusMarket. No sustituye el ADR-0001 ni los ADR funcionales existentes.

## Contexto y problema

Durante la auditorÃ­a del Compose de Dokploy se detectÃ³ que la variable `CAMPUSMARKET_REVISION` conservaba el SHA `7856416795bb4accdf9d05e01adb470654875e56` pese a existir merges posteriores. No fue posible corroborar el encabezado `X-CampusMarket-Revision` por un 403 en el cliente utilizado. Por tanto, no debe afirmarse que el encabezado HTTP pÃºblico se comprobÃ³ incorrecto: se detectÃ³ una **brecha de trazabilidad verificable**.

El despliegue activo reconstruye `api` desde GitHub. Queremos evitar que la imagen probada por CI y la imagen desplegada sean construcciones distintas, preservando MySQL y los archivos persistentes.

## Alternativas

| Alternativa | Ventajas | Costos y riesgos |
|---|---|---|
| Mantener builds independientes en CI y Dokploy | Menor cambio operativo inmediato | No acredita identidad entre artefacto probado y artefacto desplegado |
| Construir y probar una vez; publicar en GHCR por digest | Procedencia verificable, artefacto reutilizable e identidad inmutable | Requiere permisos de registro, verificaciÃ³n de digest y estrategia de promociÃ³n |
| Migrar inmediatamente la API a GHCR | Materializa pronto la ruta objetivo | Sin respaldo ni rollback acreditados, expone a interrupciones o pÃ©rdida de recuperabilidad |

## DecisiÃ³n

**Aceptar** construir una imagen una sola vez, probarla en CI, exportar ese artefacto, verificar SHA/etiqueta OCI/`/app/REVISION`, publicarlo manualmente en GHCR y fijarlo por digest en un Compose alternativo.

**No activar aÃºn** el Compose de producciÃ³n en Dokploy. La promociÃ³n requiere verificar el acceso al paquete Internal, montajes efectivos, respaldos recuperables, imagen anterior y gestiÃ³n de autodeploy. No se autoriza cambiar el Compose activo ni iniciar/recrear MySQL como consecuencia de este ADR.

## Consecuencias y atributos de calidad

- **Trazabilidad y auditabilidad:** secuencia commit â†’ CI â†’ `api.tar` â†’ GHCR/digest documentada.
- **Reproducibilidad:** la imagen de GHCR es la misma imagen exportada por CI, no una reconstrucciÃ³n posterior.
- **Desplegabilidad:** `deploy/compose.prod.yaml` representa la configuraciÃ³n objetivo, todavÃ­a no utilizada en producciÃ³n.
- **Disponibilidad y recuperabilidad:** se preserva el servicio activo mientras no existan respaldos y rollback acreditados.
- **Seguridad:** las credenciales GHCR se manejarÃ¡n fuera del repositorio, por mecanismos autorizados; no se publican secretos.
- **Costo:** se aprovecha GitHub Actions y GHCR ya disponibles; no se incorpora infraestructura adicional al servicio.

## Evidencias y lÃ­mites

- Commit probado: `2154e7880e5111537256206a29f4f4c29a8c86c4`.
- CI Compose: [run 41024201484](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41024201484).
- VerificaciÃ³n sin publicar: [run 41025785578](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41025785578).
- PublicaciÃ³n verificada: [run 41026286264](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41026286264).
- Imagen: `ghcr.io/iscoutb/campusmarket-api@sha256:f9eaabdb166274225e9ad490c44999f71f6b1f7c9c5902dc68ab98b07115ce8b`.
- Compose alternativo: [`deploy/compose.prod.yaml`](../../deploy/compose.prod.yaml).
- Evidencia completa: [`evidencia-ghcr-cierre.md`](../operacion/evidencia-ghcr-cierre.md).

La publicaciÃ³n **no** acredita acceso desde Dokploy, actualizaciÃ³n de API, persistencia en ejecuciÃ³n ni rollback ensayado.

## RevisiÃ³n de esta decisiÃ³n

Revisar cuando un operador autorizado acredite la imagen y los montajes reales, respaldos consistentes y recuperaciÃ³n probada, autenticaciÃ³n GHCR desde el servidor, control del autodeploy y procedimiento de actualizaciÃ³n Ãºnicamente de `api`.
