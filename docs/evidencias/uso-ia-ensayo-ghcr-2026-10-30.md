# Registro IA del ensayo aislado GHCR (30/10/2026)

Anexo nuevo; conserva los registros y decisiones anteriores. La IA implementa
la infraestructura de prueba y propone verificaciones; el equipo revisa el PR,
autoriza las operaciones pendientes y contrasta los resultados reales.

| Propuesta o trabajo | Decision | Verificacion y limite |
|---|---|---|
| Crear rama del fork desde upstream actualizado | Aceptada | Ambos master coinciden en `0971b2b0c229c25d4ebefd5c90bf1b8625656932`; se usa ese commit, no una base personal divergente |
| Workflow manual y verificador separado, sin cambiar workflows anteriores | Aceptada | Permisos contents/packages de lectura; dependencias existentes de la imagen y Python estandar en el runner |
| Usar digest publicado y SHA fuente independiente de GITHUB_SHA | Aceptada | Preflight rechaza otro digest; OCI, archivo, encabezado e Image ID se comprobaran en el run real |
| Crear MySQL y uploads sinteticos; probar fallo de DB y recreacion | Aceptada para el ensayo | Solo proyecto unico del runner alojado, sin conexiones Docker remotas ni endpoints publicos; ejecucion real pendiente |
| Definir runner.temp en env del job | Corregida | Actionlint lo rechazo por contexto no permitido. Se genera DOCKER_CONFIG mediante GITHUB_ENV en un paso del runner |
| Capturar cualquier Exception para ocultar stderr | Corregida | Ruff rechazo la captura ciega; se enumeran errores esperados y solo se publican mensajes propios/tipos, nunca stdout/stderr completos |
| Dar CUMPLE a persistencia o cleanup por tener codigo | Rechazada | Las pruebas unitarias de control no se presentan como Docker real. Matriz previa PARCIAL/BLOQUEADO; matriz del run se genera con hechos medidos |
| Ejecutar el nuevo workflow desde la rama del fork como si estuviera registrado | Rechazada | workflow_dispatch requiere presencia en rama predeterminada; el job requiere contexto oficial. No se altera master ni se hace merge para sortearlo |
| Usar pull_request_target, PAT o ampliar permisos para forzar una prueba | Rechazada | No son necesarios ni estan autorizados; un 403 se documenta como bloqueo |
| Copiar produccion a development o tocar recursos del laboratorio | Rechazada | El ensayo se prepara en Actions. No modifica Dokploy ni consume la cuota compartida del equipo |

## Evidencia y resultados reales

Se ejecutaron validacion Compose standalone 5.6.1, Actionlint 1.7.12, Ruff
0.16.9, Gitleaks 8.30.1, sintaxis Bash y Python, 14 casos negativos y cuatro pruebas unitarias
de control sin daemon. No se ejecuto la imagen GHCR, MySQL ni el cleanup real
en el entorno de implementacion, que no dispone de Docker Engine.

La prueba operativa sigue bloqueada hasta que el workflow sea accesible en
Actions en el contexto oficial y exista autorizacion. **No hay una URL de run
de este ensayo acreditada.** La publicacion anterior no se reutiliza como
prueba de arranque, persistencia o limpieza del nuevo job.

La rama del fork se publico con el commit de implementacion
`80152f17d175409f0d171ac39e5f96108d4ee4ff`. La creacion del PR oficial fallo con
403, `Resource not accessible by integration`; se verifico que no hay un PR
abierto de esa rama. Se entrega el enlace de comparacion para apertura manual,
sin ampliar permisos ni simular la existencia del PR o del run.

[Configuracion, matriz y procedimiento](../operacion/ensayo-ghcr.md).
