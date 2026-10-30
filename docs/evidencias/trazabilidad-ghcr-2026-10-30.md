# Evidencia complementaria — Trazabilidad GHCR (30/10/2026)

**Alcance:** mejora técnica posterior a las entregas semanales; no se presenta como un criterio de rúbrica expresamente exigido. No cambia la arquitectura funcional del monolito modular ni declara migración productiva.

## Motivación

La auditoría de Dokploy mostró una variable `CAMPUSMARKET_REVISION` antigua y builds independientes en el servicio. El valor del encabezado HTTP público no fue comprobable por 403. El objetivo fue vincular fuente, pruebas e imagen entregable sin inventar evidencias del entorno de producción.

## Matriz de trazabilidad

| Aspecto / atributo de calidad | Decisión | Implementación | Verificación | Evidencia / estado |
|---|---|---|---|---|
| Identidad de versión / auditabilidad | [ADR-0024](../adr/0024-publicar-imagen-verificada-y-condicionar-promocion.md) | Etiqueta OCI `org.opencontainers.image.revision`, `/app/REVISION` y encabezado HTTP; `scripts/ensayar_imagen_ghcr.py` | Inspección de imagen recuperada y de la descargada; OCI, archivo y cabecera iguales al SHA fuente `2154e788...`, Image ID conservado | [Publicador GHCR](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41026286264) y [ensayo real 41051624793](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41051624793) — **CUMPLE en Actions** |
| Prueba del artefacto / confianza | ADR-0024 | `.github/workflows/compose-mvp.yml`, exportación de `api.tar`; `.github/workflows/ensayo-ghcr.yml` | Compose y persistencia sobre imagen construida; después, imagen GHCR sin reconstruir con MySQL real 8.4.13, datos sintéticos y diez criterios CUMPLE | [Run 41024201484](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41024201484) y [run 41051624793](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41051624793) — **aprobados** |
| Procedencia / control de promoción | ADR-0024 | `.github/workflows/publicar-ghcr.yml` | Procedencia de run, checks, origen de checks, SHA y etiqueta | [Ensayo sin publicar](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41025785578) — **aprobado** |
| Artefacto remoto / despliegue reproducible | ADR-0024 | Publicación GHCR manual, digest remoto; pull con token efímero de lectura | Identidad remota y descarga efectiva del digest corregido desde el contexto del repositorio oficial | [Run 41026286264](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41026286264) y [run 41051624793](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41051624793) — **CUMPLE en Actions; no acredita acceso desde Dokploy** |
| Desplegabilidad sin reconstrucción | ADR-0024 | `deploy/compose.prod.yaml`, solo `api.build` → `api.image` | Equivalencia YAML y config local; ambos arranques reales con `--no-build --pull never`, mismo Image ID | [Compose alternativo](../../deploy/compose.prod.yaml) y [ensayo](../operacion/ensayo-ghcr.md) — **validado y ejecutado en runner; no promovido a producción** |
| Persistencia / recuperación | ADR-0024 | `scripts/ensayar_imagen_ghcr.py`; volúmenes nuevos del runner; [plan productivo](../operacion/despliegue-ghcr.md) | En CI, caída real de MySQL, HTTP 503/unhealthy y recuperación; SQL y PNG sobreviven a recrear ambos contenedores; cleanup vacío. La auditoría previa de Dokploy no acreditó todos los montajes efectivos ni respaldos recuperables | [Run 41051624793](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41051624793) — **CUMPLE en CI; promoción, respaldo y rollback productivos siguen bloqueados** |

## Cadena de identidad concreta

- Repositorio: `ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET`.
- SHA del código **construido y probado**: `2154e7880e5111537256206a29f4f4c29a8c86c4`.
- Run de Compose: `41024201484`.
- Ensayo manual de verificación: `41025785578` (`publicar: false`).
- Run de publicación: `41026286264` (`publicar: true`).
- Ensayo real de la imagen publicada: [run 41051624793](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41051624793), intento 1, `passed: true`, **10/10 CUMPLE**.
- Commit del workflow/verificador del ensayo: `669368894d583406c7610e8c735f686c02931de3`; no es el SHA fuente construido.
- Digest: `sha256:f9eaabdb166274225e9ad490c44999f71f6b1f7c9c5902dc68ab98b07115ce8b`.
- Image ID de API: `sha256:8e409313166b2c39cd0cc173cd9082e9e8ca7364746d4afb790bab652dc3962b`.
- Artefacto del ensayo: `ensayo-ghcr-41051624793-1`, ID `12975600016`; ZIP SHA-256 `5e45714e318b78f50d08b651aa149cc27fd198082996b65d748f2d3b3bd0daad`, descargado y contrastado con los logs. [Resultados y configuración](../operacion/ensayo-ghcr.md).
- Merge posterior de preparación de Compose: `321548f0e1068e2bea7e59d77f09c8717db5f19a`. **Este SHA no se atribuye a la imagen publicada**.

## Incidencia real y resultado

En el CI del merge posterior se observó `device offline` en Android y, a continuación, un archivo PNG inválido al generar evidencia visual. Se ejecutó nuevamente el job fallido y finalizó con éxito. Esto se documenta como incidencia transitoria observada, **no** como defecto de `compose.prod.yaml` ni como prueba de despliegue GHCR: [workflow 41029797678](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41029797678).

El [run 41046842362](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41046842362), intentos 1 y 2 sobre `1068764...`, falló antes de iniciar API/MySQL. Compose y verificador copiaron un digest con dos caracteres incorrectos (hex 18: `c → e`, 24: `d → 0`). La corrección de [PR #74](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/pull/74) se acreditó después en `41051624793`; no se oculta el fallo previo ni se atribuye un 403/404 que el verificador antiguo no conservó. El [registro canónico de IA](../ia.md#ghcr--publicación-ensayo-aislado-y-cierre-documental-2026-10-30) conserva la intervención, las correcciones y las alternativas rechazadas.

## Comprobaciones de Dokploy

Antecedente de la auditoría de lectura, no repetida en el ensayo ni en esta consolidación:

- Servicio: `campusmarket → production → sistema`; proyecto `campusmarket-sistema-2zvsxj`.
- Ruta actual: `./deploy/compose.lab.yaml` y autodeploy por push a `master`.
- API y MySQL reportados como `running / healthy` por auditoría de solo lectura.
- Volúmenes físicos identificados por Work: `campusmarket-sistema-2zvsxj_mysql_data` y `campusmarket-sistema-2zvsxj_publication_images`.
- Sin respaldo/ensayo de restauración acreditado, imagen anterior efectiva ni acceso al paquete Internal desde el servidor confirmados.
- **No se realizó promoción de GHCR a Dokploy, ni rollback.**

## Criterio de cierre

Se consideran **completadas la publicación trazable y la ejecución aislada de esa imagen con MySQL**, con evidencia por run, digest y artefacto. La matriz anterior es la matriz GHCR existente actualizada; el detalle de diez criterios pertenece al artefacto del ensayo. La **promoción a producción sigue pendiente** por controles de recuperación. Véase [decisión operativa](../operacion/decision-migracion-ghcr.md).
