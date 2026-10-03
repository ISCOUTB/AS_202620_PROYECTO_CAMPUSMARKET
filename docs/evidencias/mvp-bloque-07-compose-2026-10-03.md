# Bloque 07 — Compose reproducible y persistencia

Estado: ejecutado y aprobado en fda38976882fd5abcca8486b4b114efd28ca2b1c.
[Run 37141901649](https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37141901649).
Artefacto `compose-verificado-fda38976882fd5abcca8486b4b114efd28ca2b1c`, resultado.json.
Ocho comprobaciones aprobadas, EC-02 10/10 con datos intactos; sesión/publicación/foto
sobreviven a recreación (12.510,98 ms). Sin OOM ni reinicios inesperados.
Peak API 195.084.288 bytes, DB 190.177.280 bytes: ambos bajo 268.435.456 bytes.
Diez búsquedas HTTP de 1000 filas: 192,56; 152,70; 194,67; 196,23; 194,42;
198,04; 193,84; 194,41; 195,28; 196,04 ms. 10/10 bajo 2 s; no acredita red pública.
La continuación y sus nuevas ejecuciones se registran en
[auditoría MVP](auditoria-mvp-continuacion-2026-10-03.md).

| Requisito | Implementación | Prueba real | Evidencia |
|---|---|---|---|
| Misma revisión | REVISION, OCI y header de health | comparar tres valores con GITHUB_SHA | resultado.json con SHA |
| Monolito y MySQL | Dockerfile no root, Compose de dos servicios | health y cuatro contextos por HTTP | checks del runner |
| Cuota oficial | 256 MiB y 0,5 CPU por contenedor | inspect selectivo y cgroup memory.peak | snapshots sin Environment |
| Carga intensiva acotada | guardia común y worker único | dos cuentas concurrentes y PNG 12 MP | normalización, peak y OOM=false |
| EC-02 | SQL propietario + identidad del token | diez ataques B, datos A intactos | attempts/rejected y checks |
| Rendimiento | backend publicado y 1000 filas MySQL | diez búsquedas HTTP bajo cuota | muestras reales; 9/10 <=2 s |
| Persistencia | volúmenes MySQL y fotos | recrear ambos, mismo token/datos/archivo | hash del archivo y duración |
| Secretos fuera de Git | Environment obligatorio y env efímero | archivo del runner 0600; no defaults reales | workflow y env.example vacío |

La prueba usa solo proyecto campusmarket-ci-<run_id> y base _test. El cleanup
borra exclusivamente esos fixtures. No ejecuta despliegues ni cambios remotos.
La medición loopback no acredita el rendimiento de una red pública.
