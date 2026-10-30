# Evidencia complementaria â€” Trazabilidad GHCR (30/10/2026)

**Alcance:** mejora tÃ©cnica posterior a las entregas semanales; no se presenta como un criterio de rÃºbrica expresamente exigido. No cambia la arquitectura funcional del monolito modular ni declara migraciÃ³n productiva.

## MotivaciÃ³n

La auditorÃ­a de Dokploy mostrÃ³ una variable `CAMPUSMARKET_REVISION` antigua y builds independientes en el servicio. El valor del encabezado HTTP pÃºblico no fue comprobable por 403. El objetivo fue vincular fuente, pruebas e imagen entregable sin inventar evidencias del entorno de producciÃ³n.

## Matriz de trazabilidad

| Aspecto / atributo de calidad | DecisiÃ³n | ImplementaciÃ³n | VerificaciÃ³n | Evidencia / estado |
|---|---|---|---|---|
| Identidad de versiÃ³n / auditabilidad | [ADR-0024](../adr/0024-publicar-imagen-verificada-y-condicionar-promocion.md) | Etiqueta OCI `org.opencontainers.image.revision` y `/app/REVISION` en `backend/Dockerfile` | InspecciÃ³n de imagen Docker recuperada | [Publicador GHCR](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41026286264) â€” **aprobado** |
| Prueba del artefacto / confianza | ADR-0024 | `.github/workflows/compose-mvp.yml`, exportaciÃ³n de `api.tar` | Compose y persistencia sobre imagen construida | [Run 41024201484](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41024201484) â€” **aprobado** |
| Procedencia / control de promociÃ³n | ADR-0024 | `.github/workflows/publicar-ghcr.yml` | Procedencia de run, checks, origen de checks, SHA y etiqueta | [Ensayo sin publicar](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41025785578) â€” **aprobado** |
| Artefacto remoto / despliegue reproducible | ADR-0024 | PublicaciÃ³n GHCR manual, digest remoto | VerificaciÃ³n de identidad y etiqueta de imagen extraÃ­da del registro | [Run 41026286264](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41026286264) â€” **aprobado** |
| Desplegabilidad sin reconstrucciÃ³n | ADR-0024 | `deploy/compose.prod.yaml`, solo `api.build` â†’ `api.image` | Equivalencia YAML, `docker compose config --quiet` local | [Compose alternativo](../../deploy/compose.prod.yaml) â€” **validado, no desplegado** |
| Persistencia / recuperaciÃ³n | ADR-0024 | `docs/operacion/despliegue-ghcr.md`; mantiene definiciones de volÃºmenes | AuditorÃ­a de Work en Dokploy; no se acreditaron montajes efectivos ni respaldos | [Plan operativo](../operacion/despliegue-ghcr.md) â€” **bloqueado** |

## Cadena de identidad concreta

- Repositorio: `ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET`.
- SHA del cÃ³digo **construido y probado**: `2154e7880e5111537256206a29f4f4c29a8c86c4`.
- Run de Compose: `41024201484`.
- Ensayo manual de verificaciÃ³n: `41025785578` (`publicar: false`).
- Run de publicaciÃ³n: `41026286264` (`publicar: true`).
- Digest: `sha256:f9eaabdb166274225e9ad490c44999f71f6b1f7c9c5902dc68ab98b07115ce8b`.
- Merge posterior de preparaciÃ³n de Compose: `321548f0e1068e2bea7e59d77f09c8717db5f19a`. **Este SHA no se atribuye a la imagen publicada**.

## Incidencia real y resultado

En el CI del merge posterior se observÃ³ `device offline` en Android y, a continuaciÃ³n, un archivo PNG invÃ¡lido al generar evidencia visual. Se ejecutÃ³ nuevamente el job fallido y finalizÃ³ con Ã©xito. Esto se documenta como incidencia transitoria observada, **no** como defecto de `compose.prod.yaml` ni como prueba de despliegue GHCR: [workflow 41029797678](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41029797678).

## Comprobaciones de Dokploy

- Servicio: `campusmarket â†’ production â†’ sistema`; proyecto `campusmarket-sistema-2zvsxj`.
- Ruta actual: `./deploy/compose.lab.yaml` y autodeploy por push a `master`.
- API y MySQL reportados como `running / healthy` por auditorÃ­a de solo lectura.
- VolÃºmenes fÃ­sicos identificados por Work: `campusmarket-sistema-2zvsxj_mysql_data` y `campusmarket-sistema-2zvsxj_publication_images`.
- Sin respaldo/ensayo de restauraciÃ³n acreditado, imagen anterior efectiva ni acceso al paquete Internal desde el servidor confirmados.
- **No se realizÃ³ promociÃ³n de GHCR a Dokploy, ni rollback.**

## Criterio de cierre

Se considera **completada la publicaciÃ³n trazable** hasta GHCR, con evidencia por run y digest. La **promociÃ³n a producciÃ³n sigue pendiente** por controles de recuperaciÃ³n. VÃ©ase [decisiÃ³n operativa](../operacion/decision-migracion-ghcr.md).
