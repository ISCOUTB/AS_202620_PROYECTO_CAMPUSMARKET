# Evidencia S7 - Contrato de API y prueba de contrato

**Periodo:** 14-20/09/2026  
**Última actualización:** 16/09/2026  
**Proyecto:** CampusMarket

**Estado:** Evidencia S7 integrada y verificada en `master`.

La implementación principal del contrato se incorporó mediante los PR #37 y #38.
Durante el cierre de S7 se realizaron además los ajustes de persistencia MySQL,
trazabilidad arquitectónica y documentación mediante los PR #40 y #41, junto
con el ajuste final del C4 Nivel 2.

---

## Resultado

CampusMarket formaliza como API principal la integración síncrona entre el
Frontend Flutter Web y el Backend FastAPI.

El contrato OpenAPI `1.0.0` describe las operaciones actualmente implementadas,
sus cuerpos, respuestas y esquemas de datos.

La prueba automatizada compara el contrato versionado con la superficie OpenAPI
generada por FastAPI y se ejecuta mediante un paso explícito del pipeline.

Además, se verificó experimentalmente que la prueba falla cuando el proveedor
introduce un cambio incompatible y vuelve a verde después de restaurar el
contrato esperado.

---

## Matriz de cumplimiento S7

| Criterio | Estado | Evidencia |
|---|---|---|
| Contrato ejecutable versionado | Cumple | `contracts/openapi-v1.json`: OpenAPI `3.1.0`, API `1.0.0` |
| Rutas y esquemas de datos | Cumple | `GET /health`, `GET /publicaciones`, `POST /publicaciones`; esquemas `HealthResponse`, `PublicacionCreate`, `Publicacion` y `ErrorResponse` |
| Correspondencia contrato-API | Cumple | `backend/app/main.py`, `backend/app/publicaciones/router.py` y comparación exacta en `backend/tests/test_contrato_openapi.py` |
| Versión declarada e historial | Cumple | `info.version: 1.0.0`; contrato incorporado mediante el PR #37 y versionado en Git |
| Prueba de contrato presente | Cumple | `backend/tests/test_contrato_openapi.py` |
| Pipeline ejecuta la prueba | Cumple | Paso `Ejecutar prueba de contrato OpenAPI` en `.github/workflows/backend-tests.yml`; Run #91 sobre `master` |
| Falla ante cambio incompatible | Cumple | Ejecución roja ante `crearPublicacion` → `registrarPublicacion` y comprobación local complementaria `titulo` → `nombre` |
| ADR ligado a un escenario | Cumple | `docs/adr/0003-usar-integracion-sincrona-http-json.md`, ligado principalmente a EC-06, con alternativa asíncrona descartada y consecuencias documentadas |
| arc42 sección 6 | Cumple | Flujos de creación, consulta, persistencia e indisponibilidad en `docs/arc42/06-vista-ejecucion.md` |
| C4 Nivel 2 etiquetado | Cumple | `docs/c4/02-contenedores.puml` y `docs/c4/02-contenedores.md`; relaciones con propósito y protocolo/formato o tecnología explícitos |

**Recuento:** 10 de 10 criterios cumplidos.

---

## Operaciones contratadas

| Método | Ruta | Operación | Respuestas |
|---|---|---|---|
| `GET` | `/health` | `consultarSalud` | `200 HealthResponse` |
| `GET` | `/publicaciones` | `listarPublicaciones` | `200 Publicacion[]` |
| `POST` | `/publicaciones` | `crearPublicacion` | `201 Publicacion`, `422 HTTPValidationError`, `503 ErrorResponse` |

---

## Verificaciones ejecutadas

### Estado compatible inicial

Durante la implementación inicial del contrato se obtuvo:

```text
11 passed, 2 warnings
exit code: 0
````

Ejecución verde del fork con las pruebas separadas:

[https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/34935043273](https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/34935043273)

Ejecución oficial correspondiente al PR #38:

[https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/34935516952](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/34935516952)

---

## Evidencia de fallo ante cambio incompatible

### Mutación controlada en GitHub Actions

Se cambió temporalmente:

```diff
- operation_id="crearPublicacion",
+ operation_id="registrarPublicacion",
```

Ejecución roja:

[https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/34934077733](https://github.com/Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/34934077733)

Resultado:

```text
FAILED test_proveedor_fastapi_cumple_el_contrato_versionado

Contrato: operationId = crearPublicacion
Proveedor: operationId = registrarPublicacion

1 failed, 10 passed, 2 warnings
Process completed with exit code 1.
```

La ejecución demuestra que la prueba de contrato no pasa de forma incondicional:
un cambio incompatible en el proveedor rompe el pipeline.

---

### Mutación local complementaria

También se cambió temporalmente el esquema:

```diff
- titulo: str = Field(min_length=3, max_length=100)
+ nombre: str = Field(min_length=3, max_length=100)
```

Resultado:

```text
FAILED test_proveedor_fastapi_cumple_el_contrato_versionado

1 failed, 2 passed
exit code: 1
```

Las dos mutaciones fueron restauradas y no permanecen en el código vigente.

La demostración completa se encuentra en:

[`fallo-contrato-s7-2026-09-15.md`](./fallo-contrato-s7-2026-09-15.md)

---

## Verificación final en `master`

Después de la integración del contrato, la migración de persistencia a MySQL y
el cierre documental de S7, se realizó una verificación final sobre la rama
principal.

Estado revisado:

```text
commit: 208ada3d6e6d378f474a8e01afabb8e5385b3ef2
rama: master
GitHub Actions: Run #91
resultado: success
```

Run:

[https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/35114137881](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/35114137881)

El pipeline verificó primero la disponibilidad del servicio MySQL utilizado
durante las pruebas.

Resultado de las pruebas funcionales y arquitectónicas:

```text
9 passed, 2 warnings
```

Resultado de la prueba de contrato ejecutada de manera independiente:

```text
3 passed
```

Resultado global del pipeline:

```text
12 pruebas aprobadas
GitHub Actions: success
```

La separación de las pruebas permite identificar explícitamente que la prueba
de contrato forma parte de la integración continua y no está oculta dentro del
conjunto general de pruebas.

---

## C4 Nivel 2

Durante el cierre del 16/09/2026 se revisó el C4 Nivel 2 para hacer explícita la
tecnología o protocolo utilizado en cada relación.

Las relaciones vigentes son:

```text
Estudiante
    ↓
[HTTPS / Flutter Web]
    ↓
Frontend Web
```

```text
Administrador
    ↓
[HTTPS / Flutter Web]
    ↓
Frontend Web
```

```text
Frontend Web
    ↓
[HTTP / JSON síncrono]
    ↓
Backend API
```

```text
Backend API
    ↓
[PyMySQL / SQL]
    ↓
MySQL
```

El ajuste quedó registrado en:

```text
208ada3 - Ajustar C4 Nivel 2 con protocolos en todas las relaciones
```

Fuentes:

* [`docs/c4/02-contenedores.puml`](../c4/02-contenedores.puml)
* [`docs/c4/02-contenedores.md`](../c4/02-contenedores.md)

---

## Cliente generado

OpenAPI Generator `7.25.0` generó de forma reproducible un cliente Dart con:

* `crearPublicacion`;
* `listarPublicaciones`;
* `consultarSalud`.

El procedimiento se documenta en:

[`contracts/README.md`](../../contracts/README.md)

El cliente generado se utilizó únicamente como comprobación reproducible del
contrato.

No se incorporó como segundo cliente productivo porque
`publicaciones_api.dart` ya representa el cliente actual del corte vertical y
mantener ambos introduciría responsabilidades duplicadas.

---

## Decisión y trade-off

Se mantiene la integración síncrona porque crear y consultar publicaciones
requiere una respuesta inmediata para el consumidor Flutter.

Se acepta como consecuencia el acoplamiento temporal entre Frontend y Backend.

Los modos de fallo se expresan mediante:

* HTTP `422`;
* HTTP `503`;
* errores de comunicación HTTP.

La alternativa asíncrona fue evaluada y descartada para el alcance actual porque
requeriría:

* estados pendientes;
* reintentos;
* idempotencia;
* tratamiento de duplicados;
* consistencia eventual;
* infraestructura adicional de mensajería.

No existe actualmente una necesidad arquitectónica que justifique introducir
esa complejidad.

La decisión está registrada en:

[`ADR-0003`](../adr/0003-usar-integracion-sincrona-http-json.md)

---

## Persistencia vigente

Durante el cierre de S7 la persistencia vigente de CampusMarket fue migrada de
SQLite a MySQL.

El acceso productivo se realiza mediante:

```text
FastAPI
   ↓
service.py
   ↓
repository.py
   ↓
PyMySQL / SQL
   ↓
MySQL
```

SQLite se conserva únicamente como evidencia histórica del primer corte y de
las mediciones realizadas durante S5.

La decisión de migración se encuentra registrada en:

[`ADR-0004`](../adr/0004-migrar-persistencia-a-mysql.md)

---

## Calidad y análisis estático

CampusMarket utiliza el proyecto oficial de SonarQube Cloud:

```text
ISCOUTB_AS_202620_PROYECTO_CAMPUSMARKET
```

La configuración complementaria permanece versionada en:

```text
.sonarcloud.properties
```

Durante el cierre de S7, el análisis correspondiente al PR #41 reportó:

* Quality Gate: **Passed**;
* problemas nuevos: **0**;
* problemas aceptados nuevos: **0**;
* Security Hotspots nuevos: **0**;
* duplicación en código nuevo: **0.0 %**.

PR:

[https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/pull/41](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/pull/41)

El análisis pertenece al proyecto oficial de SonarQube Cloud configurado para
el repositorio de ISCOUTB.

---

## Cadena de trazabilidad

La trazabilidad principal de S7 es:

```text
ASP-07
   ↓
EC-06
   ↓
C4 Nivel 2
   ↓
ADR-0003
   ↓
OpenAPI 1.0.0
   ↓
FastAPI / Flutter Web
   ↓
test_contrato_openapi.py
   ↓
GitHub Actions
   ↓
fallo ante cambio incompatible
   ↓
restauración
   ↓
Run #91 en verde
```

Esta cadena conecta:

* aspecto arquitectónico;
* escenario de calidad;
* representación C4;
* decisión arquitectónica;
* contrato ejecutable;
* implementación;
* prueba automática;
* pipeline;
* evidencia experimental de fallo;
* estado final compatible.

---

## Estado final S7

Al 16/09/2026, CampusMarket cuenta con:

* contrato OpenAPI ejecutable y versionado;
* API `1.0.0`;
* rutas y esquemas de datos explícitos;
* correspondencia automática contrato ↔ FastAPI;
* prueba de contrato dentro de GitHub Actions;
* evidencia real de fallo ante cambio incompatible;
* ADR de integración síncrona;
* arc42 sección 6 actualizada;
* C4 Nivel 2 con comunicaciones etiquetadas;
* persistencia vigente MySQL;
* pipeline final en verde;
* proyecto oficial de SonarQube Cloud con Quality Gate aprobado.
