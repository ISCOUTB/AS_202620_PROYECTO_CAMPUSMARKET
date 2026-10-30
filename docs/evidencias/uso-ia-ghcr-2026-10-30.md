# Registro de uso responsable de IA â€” Mejora GHCR (30/10/2026)

Este anexo complementa `docs/ia.md` **sin modificarlo**. Registra uso, verificaciÃ³n y propuestas rechazadas, siguiendo la prÃ¡ctica documental de CampusMarket. La responsabilidad de las decisiones y de ejecutar operaciones corresponde al equipo.

| Fecha | Herramienta | Uso realizado | VerificaciÃ³n del equipo / evidencia | QuÃ© se rechazÃ³ o no se asumiÃ³ y por quÃ© |
|---|---|---|---|---|
| 29â€“30/10/2026 | ChatGPT | DiagnÃ³stico de discrepancia entre versiÃ³n configurada y commits; propuesta de cadena commit â†’ imagen probada â†’ GHCR | Se compararon commits, Dockerfile, Compose y resultados visibles de GitHub Actions | No se afirmÃ³ que el encabezado pÃºblico fuera incorrecto: el cliente de auditorÃ­a obtuvo 403 y no pudo comprobarlo |
| 30/10/2026 | ChatGPT | Propuesta e iteraciones de workflows de exportaciÃ³n y publicaciÃ³n con comprobaciones de SHA, checks y origen | Se comprobaron YAML, nombres reales de checks de GitHub y se ejecutÃ³ ensayo `publicar: false` en [run 41025785578](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41025785578) | Se descartÃ³ publicar sin comprobar identidad, usar nombres supuestos de checks y confundir el SHA del merge con el del artefacto |
| 30/10/2026 | ChatGPT | Propuesta de publicaciÃ³n manual y verificaciÃ³n de digest remoto | [Run 41026286264](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41026286264), con verificaciÃ³n de identidad de imagen y revisiÃ³n | No se dio por desplegada la imagen por el simple hecho de publicar en GHCR |
| 30/10/2026 | ChatGPT | Propuesta de Compose alternativo y plan de despliegue/rollback | Se comparÃ³ la estructura con Compose de laboratorio y se validÃ³ localmente con `docker compose config --quiet` | No se sustituyÃ³ el Compose activo ni se realizaron cambios sobre MySQL o sus volÃºmenes |
| 30/10/2026 | ChatGPT Work | AuditorÃ­a exclusivamente de lectura del servicio Dokploy, autodeploy, contenedores, nombres de volÃºmenes y limitaciones de acceso | Informes de Work y consulta visual del panel; API y DB reportados saludables | No se inventaron montajes RW, credenciales GHCR, respaldos recuperables ni una imagen anterior efectiva ante inspectores inaccesibles |
| 30/10/2026 | ChatGPT / equipo | EvaluaciÃ³n de alternativas: migrar de inmediato o preservar producciÃ³n y documentar bloqueantes | [ADR-0024](../adr/0024-publicar-imagen-verificada-y-condicionar-promocion.md), [decisiÃ³n operativa](../operacion/decision-migracion-ghcr.md) | Se rechazÃ³ la migraciÃ³n inmediata sin autenticaciÃ³n, respaldo, imagen para rollback ni verificaciÃ³n de montajes |

## LÃ­mites y revisiÃ³n humana

- La IA propuso comandos y contenido; **los resultados verificados** fueron los reportados por GitHub Actions, Docker Compose local y las auditorÃ­as de solo lectura.
- Un anÃ¡lisis sintÃ¡ctico de YAML no equivale a pruebas del pipeline; la publicaciÃ³n se acreditÃ³ con el run exitoso.
- El error `device offline` de CI Android fue diagnosticado mediante logs y el rerun exitoso no se confunde con una reparaciÃ³n de cÃ³digo.
- La autenticaciÃ³n al paquete GHCR de visibilidad Internal desde Dokploy **no** fue probada.
- No se compartieron contraseÃ±as de MySQL, PAT ni secretos en la documentaciÃ³n.
- La migraciÃ³n, el respaldo restaurable y el rollback **siguen pendientes**; no se presentan como logros.

## Referencias cruzadas

- Registro histÃ³rico: [`docs/ia.md`](../ia.md).
- Evidencia tÃ©cnica: [`trazabilidad-ghcr-2026-10-30.md`](trazabilidad-ghcr-2026-10-30.md).
- Evidencia de cierre: [`evidencia-ghcr-cierre.md`](../operacion/evidencia-ghcr-cierre.md).
