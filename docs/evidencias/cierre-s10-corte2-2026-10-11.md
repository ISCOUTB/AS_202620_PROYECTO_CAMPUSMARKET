# Complemento de cierre S10 - CampusMarket

Entrada: [evidencia del experimento](evidencia-s10-corte2-2026-10-11.md). Este archivo registra validaciones y el estado de integración sin reescribir un ADR aceptado.

## Verificación anterior a publicar

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Experimento público nuevo | 58 respuestas; 15/15 200 en baseline, 15/15 422 incompatibles, 15/15 200 adaptadas; 9/9 salud ok; todos los UUID correlacionados | [Resumen](s10/ejecucion-20261012T0419Z/resumen.json) y [muestras](s10/ejecucion-20261012T0419Z/observaciones.jsonl) |
| Frontera, contrato y logs | 8 passed, un aviso de deprecación de TestClient | [Validación local](s10/verificacion-local.json) |
| Ruff y git diff --check | Códigos 0 | Mismo reporte de validación |
| ADR anteriores | Los 19 conservan exactamente sus bytes | Reporte local y diff del PR |
| Documentación anterior | Solo docs/ia.md recibe adición al final; su contenido previo se conserva byte por byte | Reporte local y diff del PR |
| Código del proveedor y contrato | Diff vacío entre API observada y base de master | Comando de equivalencia en evidencia principal |
| Frontend y flujo de consulta | Pages 200; marcador fuente c38e0cf; detalle /catalogo/1 200; hora y duración registradas | [Comprobaciones públicas adicionales](s10/comprobaciones-publicas.json) |
| PDF | Excluido, según informe docente de CampusMarket; el equipo indica que no estaba habilitada su entrega | Fuente y explicación en evidencia principal |

## Barrido de secretos

[Resumen del barrido](s10/barrido-secretos-resumen.json), [checkout](s10/barrido-secretos-checkout.json) e [historial redactado](s10/barrido-secretos-historial-redactado.json).

Gitleaks 8.30.1, binario con SHA256 verificado, ejecutó:

```bash
gitleaks dir . --redact --config .gitleaks.toml
gitleaks git . --redact --config .gitleaks.toml
```

El checkout del trabajo S10 terminó con código 0 y cero hallazgos. El historial completo de la base contiene 365 commits; el scanner informó 295 commits con diff y terminó con código 1 por cinco coincidencias. Se conservaron esas coincidencias: cuatro valores del identificador público de Sonar en README histórico y una propiedad `sonar.projectKey` de configuración antigua. Se clasificaron como identificadores públicos, no credenciales; no se amplió la allowlist ni se cambió el código de salida a cero. No quedaron coincidencias sin clasificar. Este barrido no equivale a una auditoría completa de seguridad.

## Matriz transversal del contrato

| Comprobación | Estado y límite |
|---|---|
| Organización/nombre/visibilidad | Repositorio oficial ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET, público |
| Estructura mínima | Se conserva; los complementos S10 están enlazados desde S10-CORTE-2.md y la evidencia principal |
| Estado calificado en master | Integración y hash exacto se registran abajo; una rama de trabajo por sí sola no cierra esta fila |
| Nombres ADR | Nuevo 0020 con la convención NNNN-kebab-case; los anteriores intactos |
| ADR aceptados no reescritos | Cumple para el delta S10; persiste hallazgo histórico de ADR-0002/0003/0005, no se declara reparado |
| Registro IA | S10 añadido al final de docs/ia.md; motivos de aceptación/rechazo y vínculos al experimento |
| Pipeline/Sonar/Quality Gate | Estado final de CI abajo; Sonar scanner en CI sigue No cumple, según revisión previa y workflow vigente |
| Secretos | Checkout sin hallazgos; barrido histórico completo con cinco identificadores públicos clasificados, reporte preservado |
| Contribución del equipo | S10 no inventa correspondencia de cuentas ni contribuciones. La autoría agregada y su validación docente conservan el alcance previo |

## Estado de integración y límites de evaluación

Al preparar este complemento, las pruebas locales y la corrida pública están verificadas; la publicación por PR y sus nuevos runs de CI se comprueban a continuación. El hash final de master debe ser anterior a 2026-10-12T05:00:00Z. La regla activa exige PR y check `test`, sin bypass.

La sustentación, ejecución del pipeline en vivo y aceptación docente del escenario no se puntúan desde este documento. No se presenta una estimación de nota ni se dan por corregidos Sonar o los hallazgos históricos de ADR.
