# CampusMarket — Evidencia de trazabilidad y publicación GHCR

## 1. Problema identificado

Durante la auditoría del servicio CampusMarket en Dokploy se
observó una discrepancia entre la revisión configurada en el
despliegue y commits posteriores del repositorio.

La variable CAMPUSMARKET_REVISION conservaba la revisión
7856416795bb4accdf9d05e01adb470654875e56.

La cabecera HTTP X-CampusMarket-Revision no pudo comprobarse
directamente durante esa auditoría debido a una respuesta 403.

Por ello, no se declaró que la cabecera pública fuera incorrecta:
se identificó una falta de trazabilidad verificable entre
código, construcción, pruebas y despliegue.

## 2. Objetivo

Producir una imagen Docker de CampusMarket que pueda
identificarse inequívocamente con el commit probado y
recuperarse por un digest inmutable.

## 3. Solución implementada

- Identidad del commit en la etiqueta OCI.
- Registro del commit en /app/REVISION.
- Pruebas de la imagen mediante Docker Compose.
- Exportación del artefacto Docker probado.
- Verificación de procedencia, SHA y comprobaciones CI.
- Publicación manual en GitHub Container Registry.
- Comprobación de identidad de la imagen remota.
- Preparación de un Compose alternativo por digest.
- Documentación del procedimiento de despliegue y rollback.

## 4. Evidencias verificables

Repositorio oficial:
https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET

Commit fuente de la imagen:
2154e7880e5111537256206a29f4f4c29a8c86c4

Run de Compose:
https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41024201484

Verificación manual sin publicar:
https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41025785578

Publicación GHCR verificada:
https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41026286264

Imagen inmutable:
ghcr.io/iscoutb/campusmarket-api@sha256:f9eaabdb166274225e9ad490c44999f71f6b1f7c9c5902dc68ab98b07115ce8b

Compose alternativo:
deploy/compose.prod.yaml

Plan operativo:
docs/operacion/despliegue-ghcr.md

## 5. Resultados

CONFIRMADO:
- Imagen construida y probada en CI.
- Artefacto de la imagen recuperado.
- Commit contrastado con la etiqueta OCI y /app/REVISION.
- Publicación GHCR completada correctamente.
- Imagen remota contrastada con la imagen recuperada.
- Compose alternativo validado estructuralmente.
- docker compose config --quiet aprobado localmente.

NO CONFIRMADO:
- Uso efectivo de la imagen GHCR en Dokploy.
- Autenticación GHCR desde el servidor Dokploy.
- Destinos y permisos efectivos de todos los montajes.
- Respaldo recuperable de la base de datos y uploads.
- Imagen anterior conservada y recuperable.
- Ensayo completo de rollback.

## 6. Estado de producción

La auditoría indicó que Dokploy continúa utilizando:

deploy/compose.lab.yaml

Proyecto Compose:
campusmarket-sistema-2zvsxj

Los servicios API y MySQL estaban healthy en la última
auditoría disponible.

No se realizó una migración a GHCR.

## 7. Conclusión

Se completó la cadena de trazabilidad y publicación de la
imagen probada hasta GHCR.

La promoción a producción quedó deliberadamente aplazada
porque no se acreditaron todas las condiciones de
recuperabilidad, persistencia y acceso al registro.

No se presenta el despliegue GHCR ni el rollback como
resultados ejecutados o verificados.
