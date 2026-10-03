# Bloque 2 — Imágenes verificadas y administración mínima

Fecha: 2026-10-03. Rama: `mvp-autenticacion-producto`.

| Requisito | Implementación | Prueba | Evidencia |
|---|---|---|---|
| Hasta tres imágenes | Lock de publicación antes de insertar metadata | Cuatro subidas concurrentes | 3×201 y 1×400, tres órdenes únicos y un principal |
| Archivo real | Pillow decodifica, comprueba formato y reencodifica | Texto/falso/vacío/formato cruzado/5 MiB | Rechazados sin metadata ni archivo persistido |
| Principal y eliminación | Servicio de publicaciones con owner de sesión | Seleccionar, eliminar principal y reponer | Un único principal y galería descargable |
| Privacidad de fotos | Reencodificación sin metadata de origen | PNG con texto privado | Descarga no contiene el metadata original |
| No modificar imágenes ajenas | Lock + propietario real | Eliminar y elegir principal con usuario B | 404 y galería conservada |
| Administración útil | Reporte autenticado y cola de revisión | Reportar, duplicado, reporte propio | 201 / 409 / 400 |
| Moderación protegida | IDs verificados configurados fuera del repo | Anónimo y usuario normal | 401 / 403; registro y perfil no permiten es_admin |
| Ocultar y descartar | Administración consume servicio de publicaciones | Revisión real | Ocultar retira catálogo, preserva acceso propio; descartar conserva catálogo |
| Límites de contexto | Repositories poseen tablas | Pruebas AST e invariantes S6/S9 | Único escritor por tabla; ningún repository ajeno importado |
| Dependencias | Pillow==12.3.0 | Metadata PyPI y ejecución en Python 3.12.14/Linux | Python >=3.10; wheels Linux/Windows CPython 3.12; MIT-CMU |

## Ejecución

`python -m ruff check backend/app backend/tests`: pasa.
`python -m pytest backend/tests -q`: **66 passed**, 45.76 s, sobre
MySQL real 8.0.46 aislado, con dos avisos no bloqueantes ya documentados.
Contrato v2 regenerado desde el proveedor; v1 histórico conservado.

CI del bloque 1, hash `d5eeec7`: [run 37127354328](https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37127354328),
success sobre MySQL 8.4. No es evidencia de este bloque 2 hasta el nuevo run.

Dependencia verificada en [JSON oficial](https://pypi.org/pypi/Pillow/12.3.0/json),
con [fuente mantenida](https://github.com/python-pillow/Pillow).
No se añade pytest-cov ni dependencia de autenticación.

## Riesgos y siguiente bloque

- Ocultar SQL y resolver reporte tienen transacciones diferentes: lock de reporte
  impide decisiones concurrentes; ocultado es idempotente y un fallo es reintentable.
- Crash entre escritura de archivo y metadata puede dejar huérfanos; compensación
  atiende fallos normales, volumen persistente y reconciliación se documentan para operación.
- Perfil/IDs de moderadores deben comprobarse por el operador en cada base.
- El cliente Flutter aún requiere integración y validación real. No se declara
  UX, Web, Android ni MVP global cerrados en este bloque.
- PR oficial: conector devuelve 403 Resource not accessible by integration.
  No se desplegó ni se mergeó; el fork contiene el avance revisable.
