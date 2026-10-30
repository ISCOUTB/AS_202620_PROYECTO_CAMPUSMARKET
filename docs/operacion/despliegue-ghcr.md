# CampusMarket - Plan de despliegue GHCR

## 1. Objetivo

Desplegar una imagen Docker previamente probada en CI,
sin reconstruirla en Dokploy y sin afectar la persistencia.

Estado del plan productivo: PREPARADO, NO EJECUTADO.

El [ensayo aislado en Actions](ensayo-ghcr.md) terminó con 10/10 criterios
aprobados en el [run 41051624793](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/41051624793).
No modifica el estado de este plan ni satisface por sí solo sus condiciones
de acceso, respaldo y recuperación del servidor Dokploy.

## 2. Evidencia de origen

Repositorio:
ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET

Commit validado:
2154e7880e5111537256206a29f4f4c29a8c86c4

Run de Compose:
41024201484

Run de publicacion GHCR:
41026286264

Imagen:
ghcr.io/iscoutb/campusmarket-api@sha256:f9eaabdb166274225e9ad490c44999f71f6b1f7c9c5902dc68ab98b07115ce8b

## 3. Infraestructura actual

Dokploy: campusmarket / production / sistema

Proyecto Compose:
campusmarket-sistema-2zvsxj

Compose activo:
deploy/compose.lab.yaml

Servicios:
- api
- db

Volumenes declarados:
- mysql_data
- publication_images

El servicio actual construye api desde GitHub.
El autodeploy desde master sigue activo.

## 4. Configuracion propuesta

Archivo:
deploy/compose.prod.yaml

Cambio funcional:
- api.build se sustituye por api.image con digest inmutable.

Sin cambios estructurales en:
- servicio db;
- variables funcionales de API;
- servicios y dependencias;
- volumenes declarados;
- healthchecks;
- limites de recursos.

La equivalencia declarativa no confirma montajes fisicos.

## 5. Condiciones obligatorias antes de desplegar

[ ] Confirmar acceso de Dokploy al paquete GHCR Internal.
[ ] Confirmar montajes efectivos de MySQL y uploads.
[ ] Confirmar los nombres fisicos de los volumenes.
[ ] Obtener y verificar un respaldo recuperable de datos.
[ ] Conservar una referencia recuperable de la imagen anterior.
[ ] Verificar compatibilidad de esquema para rollback.
[ ] Evitar conflictos con autodeploy desde master.
[ ] Confirmar ruta Compose y mecanismo de variables de Dokploy.
[ ] Obtener autorizacion explicita para intervenir produccion.

Si alguna condicion falla, NO DESPLEGAR.

## 6. Ensayo previo

1. Validar el YAML con Docker Compose config.
2. Verificar acceso al digest GHCR desde el servidor.
3. Revisar diferencias entre Compose actual y propuesto.
4. Comprobar que la imagen tiene el SHA esperado.
5. Registrar el estado y los identificadores anteriores.

No ejecutar docker compose down, down -v ni comandos
que eliminen volumenes.

## 7. Despliegue controlado (procedimiento propuesto)

Aplicar exclusivamente una actualizacion del servicio api
usando el mismo proyecto Compose existente.

El comando exacto y la integracion con Dokploy se
confirmaran cuando esten verificados los requisitos previos.

No cambiar el servicio db ni recrear sus volumenes.

## 8. Verificacion posterior

Comprobar:
- API running y healthy.
- MySQL running y healthy, sin recreacion.
- Identidad de imagen por digest.
- Revision OCI igual al commit aprobado.
- Archivo /app/REVISION igual al commit aprobado.
- Encabezado X-CampusMarket-Revision esperado.
- Persistencia de los montajes fisicos.
- Operaciones publicas no destructivas de la API.

Guardar fecha, SHA, digest, evidencia y resultado.

## 9. Rollback

Si la API falla:
1. Detener la promocion de nuevas versiones.
2. Restaurar la referencia de imagen anterior.
3. Actualizar solamente api mediante procedimiento autorizado.
4. Confirmar estado healthy y version restaurada.
5. Verificar MySQL y montajes sin alteraciones.

El rollback de imagen no revierte automaticamente
migraciones de datos ni cambios en archivos.

No declarar rollback probado hasta realizar un ensayo
controlado con una version compatible.

## 10. Riesgos pendientes

- Acceso GHCR desde Dokploy: no confirmado.
- Montajes fisicos: no confirmados.
- Backups recuperables: no confirmados.
- Autodeploy desde master: activo.
- Ensayo de rollback: no realizado.

La publicacion GHCR NO equivale a un despliegue
de produccion completado.
