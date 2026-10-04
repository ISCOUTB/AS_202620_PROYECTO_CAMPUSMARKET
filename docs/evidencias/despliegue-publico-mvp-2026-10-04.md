# CampusMarket — prueba funcional de producción S9

Ejecución UTC: 20261004T021640Z
Destino: https://campusmarket.iscoutb.dev

## Alcance y criterios
Pruebas HTTP reales contra producción. Se verifican códigos HTTP, identidad, propiedad, valores editados, imagen pública y revocación de sesión. Esto valida el flujo probado; no constituye una auditoría completa de seguridad ni el cierre de toda S9.
Fuentes consultadas: bienvenida del curso, CONTRATO (1)(1).md, S08-despliegue-y-operacion.pdf, guía oficial https://github.com/ISCOUTB/iscoutb.dev/blob/main/README.md y políticas https://github.com/ISCOUTB/iscoutb.dev/blob/main/docs/politicas-uso.md. Las normas oficiales del laboratorio se contrastaron con el Compose del repositorio, no solo con la vista que Dokploy genera.

## Resultados
| Prueba | HTTP esperado | HTTP real | Resultado |
|---|---:|---:|---|
| Salud | 200 | 200 | PASS |
| Contrato OpenAPI | 200 | 200 | PASS |
| Registro a | 201 | 201 | PASS |
| Login a | 200 | 200 | PASS |
| Identidad a | 200 | 200 | PASS |
| Registro b | 201 | 201 | PASS |
| Login b | 200 | 200 | PASS |
| Identidad b | 200 | 200 | PASS |
| Autenticacion requerida | 401 | 401 | PASS |
| Catalogo publico | 200 | 200 | PASS |
| Crear publicacion A | 201 | 201 | PASS |
| Publicaciones propias A | 200 | 200 | PASS |
| Aislamiento listado B | 200 | 200 | PASS |
| Detalle publico | 200 | 200 | PASS |
| Subir imagen A | 201 | 201 | PASS |
| Imagen accesible | 200 | 200 | PASS |
| Editar publicacion A | 200 | 200 | PASS |
| Aislamiento editar B | 404 | 404 | PASS |
| Aislamiento eliminar B | 404 | 404 | PASS |
| Verificar integridad tras B | 200 | 200 | PASS |
| Reservar publicacion prueba | 200 | 200 | PASS |
| Cerrar sesion B | 204 | 204 | PASS |
| Sesion B revocada | 401 | 401 | PASS |

## Datos para persistencia
Publicación de prueba: **1**.
Detalle: https://campusmarket.iscoutb.dev/catalogo/1
Título esperado: PRUEBA S9 EDITADA 20261004T021640Z
Precio esperado: 16000. Estado: reservado. Una imagen asociada.
Imagen: /uploads/publicaciones/1/9dc8079ae3aa4b14aa2df5c9c3062792.png
Se conservaron dos cuentas de prueba con correo example.com y esta publicación para comprobar persistencia. La publicación está marcada como prueba y reservada. No se alteraron publicaciones ajenas. No se hizo reinicio ni redeploy.

## Pendientes y hallazgos
1. Persistencia después de restart/redeploy: BLOQUEADA/PENDIENTE. Intento de Restart de API rechazado por Dokploy: unauthorized to access resource docker (captura image(20261004-022754).png). No hubo reinicio. Después del intento fallido /health y /catalogo/1 devolvieron 200; eso no demuestra persistencia tras reiniciar.
2. Evidencia de commit del despliegue: captura image(20261004-022958).png muestra Done y commit c38e0cf36a30dddec39f169b7618b7c6127e0a71. Log adjunto Markdown pegado(2).md incluye escritura de ese hash a REVISION, construcción de la imagen y Docker Compose Deployed. Esto vincula el registro del despliegue al commit; no sustituye una lectura de REVISION en runtime.
3. OpenAPI anuncia http://localhost:8000 como servidor. Las pruebas usaron el dominio real explícitamente. Falta verificar Try it out en producción antes de concluir su impacto.
4. Prueba de frontend/UI: PENDIENTE. Este reporte cubre API.
5. Normas oficiales de laboratorio revisadas; ver comprobaciones siguientes. Rúbrica actual completa de la actividad Moodle no disponible.

## Procedimiento pendiente
En Dokploy identificar los contenedores de sistema y revisar volumen de base de datos e imágenes y commit desplegado. Registrar estado previo; realizar restart del servicio correcto sin eliminar volúmenes; esperar salud OK; volver a consultar la publicación y descargar imagen; comparar identificador, título, precio, estado e imagen. Reinicio y redeploy no son pruebas equivalentes: documentar cuál se ejecutó.

## Respuestas verificables (sin contraseñas ni tokens)

### Salud
GET /health — HTTP 200
```json
{
  "status": "ok",
  "service": "campusmarket-api"
}
```

### Contrato OpenAPI
GET /openapi.json — HTTP 200
```json
{
  "title": "CampusMarket API",
  "version": "2.0.0",
  "servers": [
    {
      "url": "http://localhost:8000",
      "description": "Entorno local"
    }
  ]
}
```

### Registro a
POST /usuarios/registro — HTTP 201
```json
{
  "id": 1,
  "nombre": "Prueba S9 A",
  "correo": "smoke.s9.20261004t021640z.a@example.com",
  "es_admin": false
}
```

### Login a
POST /usuarios/login — HTTP 200
```json
{
  "access_token": "[REDACTADO]",
  "token_type": "bearer",
  "expira_en": "2026-10-04T14:17:00.365972Z",
  "usuario": {
    "id": 1,
    "nombre": "Prueba S9 A",
    "correo": "smoke.s9.20261004t021640z.a@example.com",
    "es_admin": false
  }
}
```

### Identidad a
GET /usuarios/me — HTTP 200
```json
{
  "id": 1,
  "nombre": "Prueba S9 A",
  "correo": "smoke.s9.20261004t021640z.a@example.com",
  "es_admin": false
}
```

### Registro b
POST /usuarios/registro — HTTP 201
```json
{
  "id": 2,
  "nombre": "Prueba S9 B",
  "correo": "smoke.s9.20261004t021640z.b@example.com",
  "es_admin": false
}
```

### Login b
POST /usuarios/login — HTTP 200
```json
{
  "access_token": "[REDACTADO]",
  "token_type": "bearer",
  "expira_en": "2026-10-04T14:17:17.550194Z",
  "usuario": {
    "id": 2,
    "nombre": "Prueba S9 B",
    "correo": "smoke.s9.20261004t021640z.b@example.com",
    "es_admin": false
  }
}
```

### Identidad b
GET /usuarios/me — HTTP 200
```json
{
  "id": 2,
  "nombre": "Prueba S9 B",
  "correo": "smoke.s9.20261004t021640z.b@example.com",
  "es_admin": false
}
```

### Autenticacion requerida
GET /usuarios/me — HTTP 401
```json
{
  "detail": "Inicia sesión para continuar."
}
```

### Catalogo publico
GET /catalogo — HTTP 200
```json
[]
```

### Crear publicacion A
POST /publicaciones — HTTP 201
```json
{
  "titulo": "PRUEBA S9 20261004T021640Z",
  "descripcion": "Publicacion de prueba automatica S9. No corresponde a una oferta real. Reservada para verificar persistencia.",
  "precio": 15000.0,
  "modalidad": "venta",
  "estado": "usado",
  "estado_publicacion": "disponible",
  "id": 1,
  "propietario_id": 1,
  "visible": true
}
```

### Publicaciones propias A
GET /publicaciones/mias — HTTP 200
```json
[
  {
    "titulo": "PRUEBA S9 20261004T021640Z",
    "descripcion": "Publicacion de prueba automatica S9. No corresponde a una oferta real. Reservada para verificar persistencia.",
    "precio": 15000.0,
    "modalidad": "venta",
    "estado": "usado",
    "estado_publicacion": "disponible",
    "id": 1,
    "propietario_id": 1,
    "visible": true,
    "imagenes": []
  }
]
```

### Aislamiento listado B
GET /publicaciones/mias — HTTP 200
```json
[]
```

### Detalle publico
GET /catalogo/1 — HTTP 200
```json
{
  "id": 1,
  "titulo": "PRUEBA S9 20261004T021640Z",
  "descripcion": "Publicacion de prueba automatica S9. No corresponde a una oferta real. Reservada para verificar persistencia.",
  "precio": 15000.0,
  "modalidad": "venta",
  "estado": "usado",
  "propietario_id": 1,
  "estado_publicacion": "disponible",
  "imagenes": []
}
```

### Subir imagen A
POST /publicaciones/1/imagenes — HTTP 201
```json
{
  "id": 1,
  "publicacion_id": 1,
  "imagen_url": "/uploads/publicaciones/1/9dc8079ae3aa4b14aa2df5c9c3062792.png",
  "orden": 1,
  "es_principal": true
}
```

### Imagen accesible
GET https://campusmarket.iscoutb.dev/uploads/publicaciones/1/9dc8079ae3aa4b14aa2df5c9c3062792.png — HTTP 200
```json
{
  "content_type": "image/png",
  "bytes": 70
}
```

### Editar publicacion A
PUT /publicaciones/1 — HTTP 200
```json
{
  "titulo": "PRUEBA S9 EDITADA 20261004T021640Z",
  "descripcion": "Publicacion de prueba automatica S9. No corresponde a una oferta real. Reservada para verificar persistencia.",
  "precio": 16000.0,
  "modalidad": "venta",
  "estado": "usado",
  "estado_publicacion": "disponible",
  "id": 1,
  "propietario_id": 1,
  "visible": true
}
```

### Aislamiento editar B
PUT /publicaciones/1 — HTTP 404
```json
{
  "detail": "La publicación no existe o no pertenece al propietario."
}
```

### Aislamiento eliminar B
DELETE /publicaciones/1 — HTTP 404
```json
{
  "detail": "La publicación no existe o no pertenece al propietario."
}
```

### Verificar integridad tras B
GET /catalogo/1 — HTTP 200
```json
{
  "id": 1,
  "titulo": "PRUEBA S9 EDITADA 20261004T021640Z",
  "descripcion": "Publicacion de prueba automatica S9. No corresponde a una oferta real. Reservada para verificar persistencia.",
  "precio": 16000.0,
  "modalidad": "venta",
  "estado": "usado",
  "propietario_id": 1,
  "estado_publicacion": "disponible",
  "imagenes": [
    {
      "id": 1,
      "publicacion_id": 1,
      "imagen_url": "/uploads/publicaciones/1/9dc8079ae3aa4b14aa2df5c9c3062792.png",
      "orden": 1,
      "es_principal": true
    }
  ]
}
```

### Reservar publicacion prueba
PATCH /publicaciones/1/estado — HTTP 200
```json
{
  "titulo": "PRUEBA S9 EDITADA 20261004T021640Z",
  "descripcion": "Publicacion de prueba automatica S9. No corresponde a una oferta real. Reservada para verificar persistencia.",
  "precio": 16000.0,
  "modalidad": "venta",
  "estado": "usado",
  "estado_publicacion": "reservado",
  "id": 1,
  "propietario_id": 1,
  "visible": true
}
```

### Cerrar sesion B
POST /usuarios/logout — HTTP 204
```json
""
```

### Sesion B revocada
GET /usuarios/me — HTTP 401
```json
{
  "detail": "Sesión inválida o expirada."
}
```

## Evidencia de volúmenes del despliegue inicial
El log adjunto registra creación de los volúmenes campusmarket-sistema-2zvsxj_mysql_data y campusmarket-sistema-2zvsxj_publication_images, DB Healthy y API Started. La existencia de volúmenes no prueba por sí sola persistencia después de recreación. No se verificaron aún sus puntos de montaje.


## Redeploy del mismo commit — resultado y límite
Fuentes: capturas image(20261004-023458).png e image(20261004-023526).png y log Markdown pegado(3).md.
El registro más reciente terminó Done con c38e0cf36a30dddec39f169b7618b7c6127e0a71. El log muestra construcción usando caché, API Running, DB Running, DB Healthy y Docker Compose Deployed. No muestra recreación ni reinicio de los contenedores.
Después de ese redeploy se ejecutaron consultas reales: /health 200 con status ok; /catalogo/1 200 conserva título PRUEBA S9 EDITADA 20261004T021640Z, precio 16000, estado reservado, propietario 1 e imagen 1. La imagen devolvió 200, 70 bytes y SHA-256 d5a51b6aed15684ec8c123e30fe5703155359d6543b6d7b47cb5766ef44939de, idéntico al contenido previo.
Conclusión: redeploy sin pérdida observado, pero persistencia tras reinicio o recreación sigue SIN DEMOSTRAR. No se considera cerrado ese criterio. El restart directo fue rechazado por permisos y requiere intervención autorizada del administrador.
Compose suministrado por el usuario declara mysql_data:/var/lib/mysql y publication_images:/app/backend/uploads. Son montajes configurados; no sustituyen la prueba de ciclo de vida.


## Contraste con guía oficial del laboratorio — 2026-10-04

Fuente versionada: guía README blob b1b220cc58d5a51118700864b8e06b59b6513350 y políticas blob 9d671f7ef1e6b64b4c9d99a8b025099605b83239.

| Regla | Evidencia observada | Estado |
|---|---|---|
| Máximo 4 contenedores, 512 MB total, 0,5 CPU cada uno | Compose versionado: API y DB, 256M y 0.50 CPU cada uno | Configuración cumple; consumo runtime no medido |
| Sin puertos publicados, bind mounts, privilegios o Docker socket | deploy/compose.lab.yaml blob 14903e37655005335a35ba4bda65b64a6ac53124 | Cumple en archivo versionado |
| Sin redes externas añadidas por el equipo | El Compose versionado no declara networks ni labels; Dokploy añade red del servicio y labels al renderizar | Cumple en archivo; verificar Isolated Deployment en panel |
| Volúmenes nombrados para DB y archivos | mysql_data y publication_images configurados; log registra creación | Cumple configuración; ciclo de vida público pendiente |
| Secretos fuera del repo | Compose usa sustitución obligatoria MYSQL_PASSWORD y MYSQL_ROOT_PASSWORD; Environment mantiene valores | Cumple Compose; auditoría histórica basada en CI, no nueva inspección completa local |
| Flutter fuera del laboratorio | API + MySQL únicamente en Compose; frontend GitHub Pages | Cumple ubicación |
| Dominio del equipo y HTTPS | campusmarket.iscoutb.dev, pruebas urllib con validación TLS | Cumple prueba HTTP externa |
| CI del hash publicado | Cuatro runs terminados success para c38e0cf36a30dddec39f169b7618b7c6127e0a71 | Cumple los runs citados |
| CORS para frontend Pages | GET /publicaciones con Origin https://nnigarp.github.io devuelve 200 y Access-Control-Allow-Origin igual | Cumple prueba de respuesta |
| Health con DB no disponible | /health 200 con DB activa; no se detuvo DB en producción | Pendiente de ejecución pública; existe prueba previa/CI |
| Logs JSON | Implementación y evidencia CI disponibles; captura de Logs de producción aún no recogida | Pendiente evidencia runtime |
| Métrica consultable | /ops/metrics/ec01 devuelve 200; muestra inicial vacía (evaluation_available false) | URL cumple; no prueba rendimiento por sí sola |
| Publicar 24h antes del cierre | Deploy inicial 2026-10-04 UTC; fecha/hora oficial de Moodle por confirmar | No verificado contra actividad actual |

Runs actuales:
- Compose y persistencia: https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37156541579
- Backend: https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37156541480
- Flutter: https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37156541605
- Web y Android: https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37156541600

### Frontend publicado
La URL histórica https://nnigarp.github.io/AS_202620_PROYECTO_CAMPUSMARKET/ y main.dart.js responden 200. El bundle consultado todavía incluye campusmarket-s8-api-nilver.azurewebsites.net y no campusmarket.iscoutb.dev. Se inició publicación reproducible del mismo hash aprobado con API Dokploy:
https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37172016525
Estado al redactar este apartado: en curso. No se considera frontend MVP verificado hasta terminar publicación y comprobar flujo en navegador.

### Contrato transversal y Sonar
El contrato del curso exige configuración, invocación del scanner en workflow, run exitoso y Quality Gate público. El árbol actual tiene cuatro workflows y backend-tests.yml no invoca scanner. Los cuatro pipelines en verde no demuestran esa exigencia; un análisis automático de Sonar no sustituye la invocación pedida. Falta corregir/verificar esta evidencia antes de afirmar cumplimiento integral. No se editó ningún ADR aceptado durante este trabajo.


## Resultado posterior de frontend y medición pública

Publicación del frontend: run 37172016525 terminado success. Ejecutó flutter analyze, flutter test y build web release con Flutter 3.47.3, base href /AS_202620_PROYECTO_CAMPUSMARKET/ y CAMPUSMARKET_API_BASE_URL=https://campusmarket.iscoutb.dev. Fuente exacta c38e0cf36a30dddec39f169b7618b7c6127e0a71. Commit de artefactos gh-pages 4626e11 (no es el hash del código fuente).

Comprobación HTTP posterior: source-revision.txt 200 contiene el SHA fuente; main.dart.js 200 contiene campusmarket.iscoutb.dev y no contiene la URL antigua de Azure. Navegador real: Inicio muestra la publicación 1; Ver detalles abre título esperado, COP $16.000, Reservado, Usado, Venta y Fotografías 1. La imagen de prueba es un PNG de un píxel, por lo que la superficie visual resulta blanca; no se usó como prueba de calidad fotográfica. Captura local campusmarket-detalle-1791082096671.jpg. La sesión y formularios autenticados del navegador público permanecen pendientes; no se confunden con los tests HTTP ni con los tests de Web/Android en CI.

Se enviaron diez GET /publicaciones secuenciales, todos 200. Métrica del servidor: diez muestras, diez dentro de 2000 ms, duración interna entre 57.15 y 97.58 ms, meets_backend_target true, ec01_fully_verified false. Los tiempos observados desde este cliente remoto fueron 3273.10–4709.98 ms, incluyendo red/TLS: esta muestra externa supera 2 s y no demuestra cumplimiento extremo a extremo. No se sembraron 1000 publicaciones en producción; la prueba con ese volumen pertenece a CI.

Respuesta de la métrica:
```json
{
  "scenario_id": "EC-01",
  "quality_attribute": "rendimiento",
  "measurement_scope": "backend GET /publicaciones",
  "window_size": 10,
  "threshold_ms": 2000.0,
  "required_within_threshold": 9,
  "observed_requests": 10,
  "within_threshold": 10,
  "evaluation_available": true,
  "meets_backend_target": true,
  "ec01_fully_verified": false,
  "samples": [
    {
      "status_code": 200,
      "duration_ms": 59.71
    },
    {
      "status_code": 200,
      "duration_ms": 58.09
    },
    {
      "status_code": 200,
      "duration_ms": 57.98
    },
    {
      "status_code": 200,
      "duration_ms": 84.41
    },
    {
      "status_code": 200,
      "duration_ms": 92.74
    },
    {
      "status_code": 200,
      "duration_ms": 58.38
    },
    {
      "status_code": 200,
      "duration_ms": 57.52
    },
    {
      "status_code": 200,
      "duration_ms": 57.15
    },
    {
      "status_code": 200,
      "duration_ms": 57.85
    },
    {
      "status_code": 200,
      "duration_ms": 97.58
    }
  ]
}
```
