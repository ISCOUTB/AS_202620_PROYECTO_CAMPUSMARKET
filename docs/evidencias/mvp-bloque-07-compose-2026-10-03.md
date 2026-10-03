# Bloque 07 — Compose reproducible y persistencia

Estado: preparado; ejecución y mediciones pendientes.

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
