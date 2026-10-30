# Ensayo aislado de la imagen GHCR con MySQL

## Objetivo, alcance e identidad

Preparar y ejecutar manualmente la imagen ya publicada en un runner efimero de
GitHub Actions del repositorio oficial. No se reconstruye el backend, no se
conecta a Dokploy y no se utilizan datos, credenciales ni volumenes productivos.
La promocion productiva sigue aplazada segun ADR-0024.

- Base de implementacion: `0971b2b0c229c25d4ebefd5c90bf1b8625656932`, merge del PR #72.
- Commit fuente de la imagen: `2154e7880e5111537256206a29f4f4c29a8c86c4`.
- Imagen: `ghcr.io/iscoutb/campusmarket-api@sha256:f9eaabdb166274225e9ad490c44999f71f6b1f7c9c5902dc68ab98b07115ce8b`.
- Workflow nuevo: [ensayo-ghcr.yml](../../.github/workflows/ensayo-ghcr.yml).
- Verificador nuevo: [ensayar_imagen_ghcr.py](../../scripts/ensayar_imagen_ghcr.py).
- **Run definitivo:** [41051624793](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41051624793), intento 1, **success y 10/10 CUMPLE**, sobre `669368894d583406c7610e8c735f686c02931de3`. Se conservan abajo los dos intentos fallidos anteriores; esta consolidación documental no ejecuta otro ensayo.

`GITHUB_SHA` identifica el codigo del workflow, no el backend de la imagen.
El verificador contrasta OCI, `/app/REVISION` y el encabezado HTTP con el commit
fuente indicado arriba, independientemente del HEAD documental. El par SHA/digest
es el objetivo explicito de este ensayo; no es una variable productiva fija.

## Resultado real del run 41051624793

El run manual del 30/10/2026, de 06:56:04 a 06:58:52 (Colombia, UTC-5),
terminó satisfactoriamente. Se contrastaron la API de Actions, los diez PASS del
[job 124048828223](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41051624793/job/124048828223)
y los archivos `resultado.json` y `matriz.md` del
[artefacto ensayo-ghcr-41051624793-1](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41051624793/artifacts/12975600016).
El ZIP, ID `12975600016`, se descargó y verificó contra SHA-256
`5e45714e318b78f50d08b651aa149cc27fd198082996b65d748f2d3b3bd0daad`.
El JSON contiene `passed: true` y exactamente diez criterios `CUMPLE`.

Resultados observados, en el orden del verificador:

1. **compose — CUMPLE:** configuración validada sin build, dos servicios,
   red y volúmenes exclusivos del proyecto `campusmarket-ghcr-41051624793-1`.
2. **pull — CUMPLE:** digest GHCR corregido descargado con `packages: read`;
   RepoDigests y etiqueta comprobados. Esto acredita acceso desde este job de
   Actions, sin modificar la visibilidad Internal ni los permisos del paquete.
3. **identity — CUMPLE:** Image ID, Config.Image, etiqueta OCI,
   `/app/REVISION` y `X-CampusMarket-Revision` corresponden a la imagen fijada
   y al SHA fuente `2154e7880e5111537256206a29f4f4c29a8c86c4`.
   El SHA del workflow `6693688...` no se atribuye al backend construido.
4. **health — CUMPLE:** `/health` respondió HTTP 200, API y MySQL estuvieron
   healthy y la consulta SQL real acreditó MySQL **8.4.13** y la base
   `campusmarket_ghcr_41051624793_1_test`.
5. **functional — CUMPLE:** GET `/health`, `/openapi.json` y `/catalogo`
   respondieron HTTP 200; el catálogo inicial estaba vacío.
6. **synthetic — CUMPLE:** base nueva, un usuario `example.test`, una
   publicación y un PNG generados en el runner. No se accedió a datos reales.
7. **dependency — CUMPLE:** detener solo MySQL de prueba produjo HTTP 503 y
   healthcheck unhealthy de API. Al arrancar MySQL, ambos volvieron a healthy
   y se pudo recuperar la publicación y su archivo.
8. **persistence — CUMPLE:** cambiaron los IDs de ambos contenedores al
   recrearlos y conservaron los mismos montajes. El JSON acredita
   `sql_persisted: true` y `uploads_persisted: true`, comprobando el hash del PNG.
9. **no_build — CUMPLE:** ambos arranques usaron `--no-build --pull never`;
   la imagen ejecutada mantuvo el mismo Image ID descargado antes y después.
10. **cleanup — CUMPLE:** inventario final de contenedores, volúmenes y redes
    propios vacío; `temporary_credentials_removed: true`. Se eliminó también
    la autenticación temporal del runner.

Identidades y configuración efectivas conservadas en la evidencia:

- Image ID de API: `sha256:8e409313166b2c39cd0cc173cd9082e9e8ca7364746d4afb790bab652dc3962b`.
- MySQL descargado: `mysql@sha256:a0225d1ea6631c8bc2385dc4c2faba17bbf1834ecf369e1659a9a382bd8d5dd7`.
- Docker cliente/servidor: `28.0.4 / 28.0.4`; Docker Compose: `2.38.2`.
- SHA-256 del Compose usado: `1799970bbd7a9c2b8464a8c1f68bd717c52cd8e9f2344c01bfe17800aa108593`.
- Volumen SQL de prueba: `campusmarket-ghcr-41051624793-1_mysql_data`,
  destino `/var/lib/mysql`, RW `true`.
- Volumen de uploads de prueba: `campusmarket-ghcr-41051624793-1_publication_images`,
  destino `/app/backend/uploads`, RW `true`.
- Cada contenedor tuvo `268435456` bytes (256 MiB) de límite efectivo.
  Los snapshots completos y los IDs antes/después están en `resultado.json`.

La matriz de diez criterios generada por el propio run permanece en el
artefacto; no se crea otra copia documental. La relación con decisiones,
implementación y evidencias se actualiza en la
[matriz de trazabilidad existente](../evidencias/trazabilidad-ghcr-2026-10-30.md).
El artefacto está sujeto a la retención de 14 días del workflow; las identidades
y resultados contrastados quedan registrados aquí. Este éxito no acredita
migración, respaldo o rollback productivos ni acceso GHCR desde Dokploy.

## Incidente: digest transcrito incorrectamente

La investigacion compara el codigo de `1068764ba84095b93fe0d643cf401503131473ec`
con los logs del publicador exitoso. No consulta secretos, permisos del paquete
ni recursos productivos. Upstream/master y el master del fork coincidieron en
ese commit al crear `fix/diagnostico-pull-ghcr-20261030-1068764`.

| Referencia | Digest SHA-256 |
|---|---|
| Solicitado por Compose y verificador en los dos intentos fallidos | `f9eaabdb166274225c9ad49dc44999f71f6b1f7c9c5902dc68ab98b07115ce8b` |
| Publicado y descargado por el publicador exitoso | `f9eaabdb166274225e9ad490c44999f71f6b1f7c9c5902dc68ab98b07115ce8b` |

Hay dos diferencias en la parte hexadecimal (posiciones desde 1): **18: c/e** y
**24: d/0**. El nombre de paquete es el mismo. El workflow del ensayo no contiene
un digest: invoca el verificador, cuya constante IMAGE y el campo api.image de
Compose contenian el mismo valor incorrecto. Por eso `config` aprobaba una
configuracion internamente coherente, pero que apuntaba a otra referencia.

Evidencia verificable:

- [Publicacion, job 123965073846](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41026286264/job/123965073846), paso 6: a las 03:25:23 del 30/10/2026 (Colombia, UTC-5), el push imprime el digest correcto; despues `imagetools inspect`, `pull` y la verificacion remota terminan satisfactoriamente. `GHCR_VERIFICADO` repite esa referencia.
- El Image ID acreditado es `sha256:8e409313166b2c39cd0cc173cd9082e9e8ca7364746d4afb790bab652dc3962b`, diferente del digest del manifiesto. OCI y REVISION se verificaron contra `2154e7880e5111537256206a29f4f4c29a8c86c4`.
- [Ensayo, intento 1, job 124032891662](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41046842362/job/124032891662) y [reintento 2, job 124037350081](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41046842362/job/124037350081): Compose, login y cleanup exitosos; falla la descarga antes de descargar MySQL o iniciar los servicios.
- Los tres jobs muestran runner `2.338.0`, imagen `ubuntu-24.04`, version `20261025.353.1`. El publicador dispone de `packages: write`; el ensayo acredita `packages: read`. No hay evidencia de incompatibilidad del runner.
- El rol Admin en Manage Actions access y la visibilidad Internal son informacion comprobada por el usuario; no se han consultado ni cambiado desde esta investigacion. Login exitoso no prueba por si solo la autorizacion de una descarga concreta.

**Error histórico confirmado:** los dos intentos fallidos solicitaron un digest distinto del publicado.
El error de Docker concreto (404/manifest, autorizacion, red u otro) no puede
recuperarse de esos logs: `capture_output=True` capturo stderr y el verificador
lo descarto al elevar un mensaje generico. Los logs solo preservan el exit 1 de
Python, no el codigo de salida de Docker. No se afirma un fallo de permisos ni
se atribuye un mensaje MANIFEST_UNKNOWN que no se ha observado.

La correccion es literal: sustituir las dos referencias ejecutables y las cinco
referencias documentales; no se reconstruye ni publica otra imagen, no cambia
el SHA fuente y no se modifica el workflow. El Compose alternativo permanece
sin activar en Dokploy. Las evidencias antiguas pueden contrastarse en el
commit anterior; este apartado deja constancia expresa de la fe de erratas.

La corrección se incorporó mediante [PR #74](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/pull/74)
y se probó realmente en `41051624793`. El error de transcripción se conserva
como error detectado y corregido con apoyo de IA en el
[registro canónico](../ia.md#ghcr--publicación-ensayo-aislado-y-cierre-documental-2026-10-30).

## Diagnostico seguro y validacion de la correccion

Solo el `docker pull` de GHCR activa el diagnostico nuevo. Ante un exit distinto
de cero, el verificador registra `docker_pull_error` con **category** y
**exit_code**, y utiliza esos mismos datos en su mensaje de fallo. Un timeout
se registra como TIMEOUT y exit_code nulo. Nunca devuelve, imprime ni archiva
stderr/stdout, argumentos, credenciales o variables de entorno como diagnostico.

Las categorias orientativas distinguen referencia ausente, plataforma,
autenticacion, autorizacion, cuota, referencia invalida, daemon, red, TLS,
registro y almacenamiento. Lo no reconocido queda UNKNOWN. Son patrones de
errores Docker, no una comprobacion de permisos administrativos. Referencia de
codigos de registro: [Distribution HTTP API V2](https://distribution.github.io/distribution/spec/api/).

Validaciones locales de esta correccion, sin Engine ni acceso al paquete:

```text
python -m unittest scripts.test_ensayar_imagen_ghcr -v
python -m ruff check scripts/ensayar_imagen_ghcr.py scripts/test_ensayar_imagen_ghcr.py
docker compose --project-name <proyecto-de-prueba> --env-file <env-sintetico> -f deploy/compose.prod.yaml config --format json
git diff --check
```

Las cinco pruebas unitarias cubren 20 mensajes de clasificacion, supresion de
salidas sensibles, timeout, fallo ordinario y retorno satisfactorio. Se valida
Compose con credenciales sinteticas, se compara su imagen con el digest extraido
del log de publicacion y se exige que el digest anterior sea rechazado.
Gitleaks revisa los archivos del cambio. Ninguna de estas validaciones descarga
la imagen ni arranca servicios.

La tabla siguiente conserva el estado del incidente **antes** del run exitoso;
sus NO CUMPLE/BLOQUEADO no describen el estado actual del ensayo corregido.

| Criterio | Estado | Archivo/linea en el commit auditado | Commit | Run | Resultado |
|---|---|---|---|---|---|
| Publicacion y comprobacion de la identidad remota | CUMPLE | `.github/workflows/publicar-ghcr.yml:185` | `2154e7880e5111537256206a29f4f4c29a8c86c4` | `41026286264` | Digest correcto e Image ID acreditados |
| Referencia solicitada por el ensayo | NO CUMPLE | `scripts/ensayar_imagen_ghcr.py:20`; `deploy/compose.prod.yaml:3` | `1068764ba84095b93fe0d643cf401503131473ec` | `41046842362`, intentos 1 y 2 | Dos caracteres distintos al digest publicado |
| Login y permisos declarados del job | CUMPLE | `.github/workflows/ensayo-ghcr.yml:6`, `:28` | `1068764ba84095b93fe0d643cf401503131473ec` | Ambos intentos | Login exitoso y packages: read; no acredita acceso efectivo a un manifiesto |
| Causa Docker exacta de la descarga fallida | BLOQUEADO | `scripts/ensayar_imagen_ghcr.py:187` | `1068764ba84095b93fe0d643cf401503131473ec` | Ambos intentos | stderr y exit Docker no preservados; no se inventa 403/404 |
| Cleanup de los intentos fallidos | CUMPLE | `scripts/ensayar_imagen_ghcr.py:325` | `1068764ba84095b93fe0d643cf401503131473ec` | Ambos intentos | Cleanup exitoso; servicios no iniciados |
| API, SQL, salud y persistencia de la imagen corregida | BLOQUEADO | Verificador de esta rama | Rama de correccion | No ejecutado | No se repite el ensayo automaticamente |

## Configuracion y comprobaciones implementadas

1. Solo `workflow_dispatch`, repositorio oficial y runner `ubuntu-24.04` alojado
   por GitHub; permisos `contents: read` y `packages: read`.
2. Autenticacion efimera de Actions por stdin. No PAT, secretos nuevos ni
   credenciales persistidas en el checkout. La configuracion Docker se guarda
   temporalmente en el runner y se elimina en cleanup.
3. Se utiliza directamente `deploy/compose.prod.yaml`, corregido solo en su digest. Antes de arrancar se
   ejecuta `docker compose config --format json`, sin publicar el resultado
   completo. Se rechazan builds, puertos, bind mounts, redes/volumenes externos,
   referencias a otros proyectos y una base ajena al ensayo.
4. Proyecto `campusmarket-ghcr-<run_id>-<run_attempt>`, dos volumenes nuevos y
   base `<proyecto_con_guiones_bajos>_test`. Se comprueba que el namespace este
   vacio antes de utilizarlo. Las credenciales MySQL se generan al ejecutar,
   se enmascaran y se guardan en un archivo temporal 0600.
5. Descarga explicita del digest API y de MySQL 8.4. Ambos arranques emplean
   `--no-build --pull never`. Se comparan RepoDigests, Image ID, Config.Image,
   etiqueta OCI, REVISION, limites efectivos y montajes Name/Destination/RW.
6. Prueba de lectura: `/health`, `/openapi.json` y catalogo inicialmente vacio.
   Una consulta SQL comprueba el nombre real de la base y version MySQL 8.4.
7. Fixture separado: un usuario `example.test`, una publicacion y un PNG pequeno
   generados durante el run. La sesion permanece solo en memoria; los artefactos
   no incluyen passwords, sesiones, variables ni cuerpos HTTP.
8. Se detiene **solo la db sintetica** para comprobar HTTP 503 y healthcheck
   `unhealthy` de API; despues se recuperan ambos healthchecks.
9. Se recrean **los dos contenedores del ensayo**, conservando sus volumenes.
   Se exige que cambien ambos IDs, que los montajes permanezcan iguales y que
   persistan la publicacion y el hash del archivo servido por la API.
10. Cleanup con `always()` tras checkout: elimina exclusivamente contenedores,
    volumenes y red etiquetados con el proyecto del run y verifica inventario
    vacio. El `down --volumes` esta limitado al ensayo; nunca se aplica a Dokploy.
    Tambien se eliminan el archivo de entorno y la autenticacion temporal.

El host usa Python estandar y Docker/Compose disponibles en el runner. Pillow y
PyMySQL se utilizan dentro de la imagen, donde ya existen. No se incorporan
dependencias al producto ni se modifican workflows existentes.

## Historial: validacion estatica inicial

- Docker Compose standalone **5.6.1**: `config --format json` valido con valores
  sinteticos. Se verificaron digest, dos servicios, limites 256 MiB + 256 MiB,
  red propia y nombres de volumenes prefijados por el proyecto de prueba.
- Actionlint **1.7.12**, con ShellCheck no disponible: validacion del workflow.
- Ruff **0.16.9**: verificador nuevo sin hallazgos.
- Compilacion sintactica de Python y del probe ejecutado dentro de API.
- Sintaxis Bash de cada paso y permisos/triggers esperados del YAML.
- Gitleaks **8.30.1**: los cuatro archivos nuevos, sin hallazgos.
- 14 casos negativos: builds, otro digest, volumen externo/productivo, bind
  mount, host SQL externo, puerto publicado, red externa, servicio adicional,
  ausencia de healthcheck, contexto fork, Docker remoto, self-hosted e ID invalido.
- Cuatro pruebas unitarias de control sin daemon: cleanup acotado al namespace,
  eliminacion de credenciales incluso ante error de infraestructura, supresion
  de stdout/stderr sensibles e informe incompleto que falla.
- `git diff --check`. En esa preparacion inicial no se alteraron Compose, backend ni configuraciones productivas.

Estas comprobaciones **no equivalen** a descargar GHCR o ejecutar MySQL/API.
El entorno de implementacion carece de Docker Engine. Las pruebas unitarias
simulan la infraestructura; sus identificadores temporales no son runs de Actions.

## Historial: matriz anterior al run 41046842362

Esta matriz conserva el estado previo. El cierre vigente figura en
«Resultado real del run 41051624793» y la fe de erratas permanece en el incidente.

El workflow y verificador se publicaron en el commit `80152f17d175409f0d171ac39e5f96108d4ee4ff` del fork.
La matriz producida
por Actions registra automaticamente el SHA exacto del workflow, lineas y URL
real del run; no se inserta un hash autorreferencial en este documento.

| Criterio | Estado | Archivo/linea | Commit | Run | Resultado |
|---|---|---|---|---|---|
| Sintaxis del workflow y configuracion Compose | CUMPLE | `.github/workflows/ensayo-ghcr.yml:1`; `deploy/compose.prod.yaml:1` | `80152f17d175409f0d171ac39e5f96108d4ee4ff` | No aplica: validacion estatica local | Actionlint y Compose config ejecutados; no prueba runtime |
| Aislamiento y rechazo de configuracion insegura | PARCIAL | `scripts/ensayar_imagen_ghcr.py:133`, `:143` | `80152f17d175409f0d171ac39e5f96108d4ee4ff` | Pendiente | Casos negativos aprobados; falta inspeccion real de contenedores/volumenes |
| Acceso GHCR con permiso de lectura | BLOQUEADO | `.github/workflows/ensayo-ghcr.yml:28`; `scripts/ensayar_imagen_ghcr.py:285` | Pendiente ejecucion | Pendiente | El publicador anterior no acredita el contexto de este nuevo job |
| API ejecutada desde el digest, sin build | BLOQUEADO | `scripts/ensayar_imagen_ghcr.py:264`, `:285` | Pendiente ejecucion | Pendiente | Implementado; falta ejecucion real |
| OCI, REVISION, encabezado y SHA fuente | BLOQUEADO | `scripts/ensayar_imagen_ghcr.py:38`, `:264` | Fuente `2154e788...` | Pendiente | No se compara con HEAD documental |
| MySQL conectado y healthchecks positivos/negativos | BLOQUEADO | `scripts/ensayar_imagen_ghcr.py:38`, `:285` | Pendiente ejecucion | Pendiente | Falta probar 200, SQL, 503 y recuperacion |
| Prueba funcional y persistencia sintetica | BLOQUEADO | `scripts/ensayar_imagen_ghcr.py:38`, `:285` | Pendiente ejecucion | Pendiente | Falta recrear contenedores y verificar SQL/archivo |
| Cleanup real incluso ante fallo de tests | PARCIAL | `.github/workflows/ensayo-ghcr.yml:40`; `scripts/ensayar_imagen_ghcr.py:325` | `80152f17d175409f0d171ac39e5f96108d4ee4ff` | Pendiente | Pruebas unitarias de control aprobadas; falta Docker real |

## Historial: entrega inicial y permiso de Pull Request

La rama `ci/ensayo-ghcr-20261030-0971b2b` se publico unicamente en el fork
`Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET`. GitHub confirmo un solo commit de
implementacion sobre `0971b2b...` y exactamente cuatro archivos nuevos. Esta
nota documental posterior registra el bloqueo de entrega; no cambia el ensayo.

La integracion rechazo crear el PR contra ISCOUTB/master con **403, Resource
not accessible by integration**. Se comprobo que no existe un PR abierto de
esta rama. No se reintenta con credenciales o permisos ampliados.

[Comparación inicial, conservada como historial](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/compare/master...Nnigarp:ci/ensayo-ghcr-20261030-0971b2b?expand=1).
La incorporación posterior se acredita en [PR #73](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/pull/73),
merge `1068764...`; la corrección se incorporó en PR #74, merge `6693688...`.
El 403 inicial de la integración no se atribuye al registro GHCR.

## Siguiente ejecucion, solo con autorizacion

El workflow ya está registrado y el ensayo sobre `6693688...` finalizó con
éxito. No hay una repetición pendiente para acreditar este resultado. Los pasos
siguientes quedan como procedimiento para un ensayo futuro autorizado; esta
consolidación no dispara runs ni modifica jobs anteriores.

Pasos del responsable autorizado, despues de revisar el PR:

1. Coordinar cualquier cambio futuro del ensayo a la rama predeterminada mediante
   el PR. **Fusionar a master tambien activa el autodeploy actual de Dokploy**;
   esa consecuencia requiere coordinacion independiente. Este trabajo no hace
   merge ni modifica ese autodeploy.
2. Con el workflow ya registrado y autorizacion de ejecucion, abrir Actions en
   `ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET`, seleccionar **Ensayo aislado de imagen
   GHCR** y **Run workflow** sobre la version revisada.
3. Si falla la descarga, consultar la categoria y exit_code de `docker_pull_error`.
   No atribuir el fallo a permisos por conjetura, no anadir PAT ni elevar permisos
   automaticamente. UNKNOWN conserva el fallo sin publicar salidas sensibles.
4. Consultar el resumen y artefacto `ensayo-ghcr-<run_id>-<run_attempt>`:
   `resultado.json` y `matriz.md`. Incluyen SHA fuente, SHA del workflow, digest,
   Image IDs, MySQL efectivo, snapshots de montajes, checks y cleanup. Un fallo
   no se transforma en exito: el informe y el job quedan incompletos/fallidos.
5. Anadir la URL real y resultado a esta evidencia solo tras revisar el run.
   No se reutiliza como evidencia del ensayo el run anterior de publicacion.

## Riesgos y limites

- Descarga corregida, SQL, dependencia, persistencia y cleanup después de un
  stack funcional quedaron acreditados en `41051624793`; el alcance es el
  runner efímero. Los dos fallos previos se conservan como historial.
- MySQL usa el tag 8.4 requerido; se registra su digest e Image ID efectivos.
- No se prueban red publica, HTTPS, dominio, autodeploy ni recuperacion productiva.
- Una cancelacion forzada o perdida del runner puede impedir el ultimo paso;
  no se marca cleanup CUMPLE sin inventario vacio. Los recursos pertenecen al
  runner efimero, no al servidor compartido.
- Las imagenes descargadas quedan en la cache del runner hasta su destruccion;
  no se ejecuta un prune global. Los contenedores, volumenes, red y credenciales
  propios si se limpian y verifican durante el job.

## Referencias

- [Plan productivo](despliegue-ghcr.md), [cierre GHCR](evidencia-ghcr-cierre.md) y
  [decision operativa](decision-migracion-ghcr.md): no se da por realizada la migracion.
- [ADR-0024](../adr/0024-publicar-imagen-verificada-y-condicionar-promocion.md),
  [trazabilidad existente](../evidencias/trazabilidad-ghcr-2026-10-30.md) y
  [registro canónico de IA](../ia.md#ghcr--publicación-ensayo-aislado-y-cierre-documental-2026-10-30).
- [Guia UTB, secciones 1, 3.4, 3.6, bloques operativos y 5](https://github.com/ISCOUTB/iscoutb.dev/blob/0d121afd28a8472d75232b95ab6bb6b071a61e21/README.md)
  y [politicas](https://github.com/ISCOUTB/iscoutb.dev/blob/0d121afd28a8472d75232b95ab6bb6b071a61e21/docs/politicas-uso.md).
- [Requisito de registro del workflow manual](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow).
