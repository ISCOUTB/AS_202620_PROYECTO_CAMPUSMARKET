# Ensayo aislado de la imagen GHCR con MySQL

## Objetivo, alcance e identidad

Preparar y ejecutar manualmente la imagen ya publicada en un runner efimero de
GitHub Actions del repositorio oficial. No se reconstruye el backend, no se
conecta a Dokploy y no se utilizan datos, credenciales ni volumenes productivos.
La promocion productiva sigue aplazada segun ADR-0024.

- Base de implementacion: `0971b2b0c229c25d4ebefd5c90bf1b8625656932`, merge del PR #72.
- Commit fuente de la imagen: `2154e7880e5111537256206a29f4f4c29a8c86c4`.
- Imagen: `ghcr.io/iscoutb/campusmarket-api@sha256:f9eaabdb166274225c9ad49dc44999f71f6b1f7c9c5902dc68ab98b07115ce8b`.
- Workflow nuevo: [ensayo-ghcr.yml](../../.github/workflows/ensayo-ghcr.yml).
- Verificador nuevo: [ensayar_imagen_ghcr.py](../../scripts/ensayar_imagen_ghcr.py).
- **Run real de este ensayo: pendiente. No existe una URL de ejecucion acreditada.**

`GITHUB_SHA` identifica el codigo del workflow, no el backend de la imagen.
El verificador contrasta OCI, `/app/REVISION` y el encabezado HTTP con el commit
fuente indicado arriba, independientemente del HEAD documental. El par SHA/digest
es el objetivo explicito de este ensayo; no es una variable productiva fija.

## Configuracion y comprobaciones implementadas

1. Solo `workflow_dispatch`, repositorio oficial y runner `ubuntu-24.04` alojado
   por GitHub; permisos `contents: read` y `packages: read`.
2. Autenticacion efimera de Actions por stdin. No PAT, secretos nuevos ni
   credenciales persistidas en el checkout. La configuracion Docker se guarda
   temporalmente en el runner y se elimina en cleanup.
3. Se utiliza **sin modificar** `deploy/compose.prod.yaml`. Antes de arrancar se
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

## Validacion estatica efectuada

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
- `git diff --check`. No se alteran Compose, backend ni configuraciones productivas.

Estas comprobaciones **no equivalen** a descargar GHCR o ejecutar MySQL/API.
El entorno de implementacion carece de Docker Engine. Las pruebas unitarias
simulan la infraestructura; sus identificadores temporales no son runs de Actions.

## Matriz previa a la ejecucion real

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

## Entrega y permiso de Pull Request

La rama `ci/ensayo-ghcr-20261030-0971b2b` se publico unicamente en el fork
`Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET`. GitHub confirmo un solo commit de
implementacion sobre `0971b2b...` y exactamente cuatro archivos nuevos. Esta
nota documental posterior registra el bloqueo de entrega; no cambia el ensayo.

La integracion rechazo crear el PR contra ISCOUTB/master con **403, Resource
not accessible by integration**. Se comprobo que no existe un PR abierto de
esta rama. No se reintenta con credenciales o permisos ampliados.

[Abrir la comparacion y preparar el PR oficial](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/compare/master...Nnigarp:ci/ensayo-ghcr-20261030-0971b2b?expand=1).
Ese enlace es un formulario de comparacion, **no una URL de PR creado**.

## Ejecucion pendiente y evidencia real

GitHub exige que un workflow manual exista en la **rama predeterminada** para
registrar `workflow_dispatch`. Crear este archivo en la rama del fork y abrir
el PR no lo hace ejecutable en el repositorio oficial. El job tambien rechaza
el contexto de un fork. No se usara un trigger privilegiado para eludirlo.

Pasos del responsable autorizado, despues de revisar el PR:

1. Coordinar la incorporacion del workflow a la rama predeterminada mediante
   el PR. **Fusionar a master tambien activa el autodeploy actual de Dokploy**;
   esa consecuencia requiere coordinacion independiente. Este trabajo no hace
   merge ni modifica ese autodeploy.
2. Con el workflow ya registrado y autorizacion de ejecucion, abrir Actions en
   `ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET`, seleccionar **Ensayo aislado de imagen
   GHCR** y **Run workflow** sobre la version revisada.
3. Si el paquete Internal devuelve 403, registrar el bloqueo. Un administrador
   del paquete debe confirmar el acceso del repositorio; no se anaden PAT ni se
   elevan permisos automaticamente.
4. Consultar el resumen y artefacto `ensayo-ghcr-<run_id>-<run_attempt>`:
   `resultado.json` y `matriz.md`. Incluyen SHA fuente, SHA del workflow, digest,
   Image IDs, MySQL efectivo, snapshots de montajes, checks y cleanup. Un fallo
   no se transforma en exito: el informe y el job quedan incompletos/fallidos.
5. Anadir la URL real y resultado a esta evidencia solo tras revisar el run.
   No se reutiliza como evidencia del ensayo el run anterior de publicacion.

## Riesgos y limites

- Acceso Internal, arranque, SQL, dependencia de health, persistencia y cleanup
  real siguen sin comprobarse para este workflow.
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
  [trazabilidad anterior](../evidencias/trazabilidad-ghcr-2026-10-30.md) y
  [registro IA de este ensayo](../evidencias/uso-ia-ensayo-ghcr-2026-10-30.md).
- [Guia UTB, secciones 1, 3.4, 3.6, bloques operativos y 5](https://github.com/ISCOUTB/iscoutb.dev/blob/0d121afd28a8472d75232b95ab6bb6b071a61e21/README.md)
  y [politicas](https://github.com/ISCOUTB/iscoutb.dev/blob/0d121afd28a8472d75232b95ab6bb6b071a61e21/docs/politicas-uso.md).
- [Requisito de registro del workflow manual](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow).
