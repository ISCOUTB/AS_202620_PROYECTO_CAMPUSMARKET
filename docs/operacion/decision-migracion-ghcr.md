# CampusMarket — Decisión operativa sobre migración a GHCR

## Contexto

CampusMarket funciona actualmente en Dokploy mediante un
servicio Docker Compose que construye la API desde GitHub.

Se dispone de una imagen Docker probada, publicada en GHCR
y referenciada por digest inmutable.

El despliegue de esa imagen todavía requiere comprobar
aspectos de seguridad operativa y recuperación.

## Decisión

Mantener temporalmente la configuración activa de Dokploy
y conservar deploy/compose.prod.yaml como configuración
alternativa preparada, pero no activada.

No ejecutar la migración mientras existan bloqueantes
relacionados con respaldo, montajes, acceso GHCR o rollback.

Esta es una decisión operativa documentada, no una
sustitución de los ADR existentes.

## Alternativas consideradas

### A. Migración inmediata

Ventaja:
- Incorporación rápida de la imagen inmutable.

Riesgo:
- Posible interrupción sin recuperación acreditada.

Resultado: descartada por ahora.

### B. Conservar el despliegue y preparar la migración

Ventajas:
- Mantener el sistema operativo.
- Conservar la evidencia técnica obtenida.
- Evitar intervenir datos y servicios sin garantías.

Limitación:
- La producción aún no utiliza el digest publicado.

Resultado: alternativa seleccionada.

## Atributos de calidad

Trazabilidad:
- Identidad del commit, pruebas e imagen publicada.

Desplegabilidad:
- Imagen preconstruida e identificada por digest.

Recuperabilidad:
- Exige imagen anterior disponible y respaldos probados.

Disponibilidad:
- Se evita una intervención prematura en producción.

Seguridad operativa:
- No se exponen credenciales ni se modifican permisos.

## Condiciones para reconsiderar la decisión

- Acceso GHCR comprobado desde el servidor.
- Montajes reales y permisos verificados.
- Respaldos consistentes y recuperación ensayada.
- Imagen anterior identificada y conservada.
- Procedimiento de actualización exclusiva de API validado.
- Control de autodeploy durante la intervención.
- Autorización expresa para modificar producción.

## Consecuencias

La publicación GHCR queda implementada y demostrada.

La migración y el rollback continúan pendientes.

El trabajo no se presenta como una migración de
producción completada.

## Referencias

- docs/operacion/evidencia-ghcr-cierre.md
- docs/operacion/despliegue-ghcr.md
- deploy/compose.prod.yaml
