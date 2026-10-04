# Evidencia S9 - Generación verificada y trazable

**Proyecto:** CampusMarket
**Semana:** 9
**Fecha:** 2026-10-01
**Corte:** Segundo corte

---

## 1. Porción real trabajada

Durante S9 se materializó una porción real del contexto **Catálogo** de CampusMarket.

La capacidad incorporada permite:

- consultar publicaciones;
- buscar por texto;
- filtrar por modalidad;
- filtrar por estado;
- filtrar por rango de precio;
- consultar el detalle de una publicación.

Archivos principales:

- `backend/app/catalogo/router.py`
- `backend/app/catalogo/service.py`
- `backend/app/main.py`

El módulo Catálogo consume la capacidad de lectura expuesta por Gestión de Publicaciones y no accede directamente al repositorio de persistencia.

---

## 2. Cadena de trazabilidad

La porción implementada sigue la cadena:

ASP-01
   ↓
EC-01
   ↓
C4
   ↓
ADR-0009
   ↓
backend/app/catalogo/
   ↓
tests
   ↓
mutación controlada
   ↓
medición EC-01
   ↓
evidencia

Referencias:
- Aspectos: docs/aspectos.md
- Escenario: docs/arc42/10-escenarios-de-calidad.md
- Decisión: docs/adr/0009-materializar-catalogo-sin-romper-fronteras.md
- Evidencia EC-01: docs/evidencias/evidencia-ec01-catalogo-s9-2026-10-01.md

## 3. Decisión arquitectónica

ADR-0009 establece que Catálogo consume una capacidad explícita de lectura de Publicaciones.
Se descartó:
- acceso directo de Catálogo a MySQL;
- importación directa de publicaciones.repository;
- creación de un microservicio independiente de Catálogo.
La propiedad de escritura de la entidad publicaciones continúa perteneciendo a Gestión de Publicaciones.

## 4. Pruebas funcionales

Archivo:
backend/tests/test_catalogo.py
Se verificó:
- listado;
- búsqueda textual;
- filtro por modalidad;
- filtro por estado;
- filtro por precio;
- validación de rango de precios;
- consulta de detalle;
- detalle inexistente.
Resultado:
8 passed

## 5. Auditoría de erosión arquitectónica

Archivo:
backend/tests/test_erosion_s9.py
Las reglas verifican que Catálogo:
- no importe directamente el repositorio de Publicaciones;
- no utilice PyMySQL;
- no ejecute escrituras SQL directas sobre publicaciones.
Resultado normal:
3 passed

## 6. Prueba que falla ante el defecto

Se introdujo temporalmente la siguiente mutación:
from backend.app.publicaciones import repository  # MUTACION_S9


La ejecución produjo:
FAILED test_catalogo_no_importa_repository_de_publicaciones
1 failed, 2 passed

La mutación fue retirada inmediatamente.
Al restaurar la implementación correcta:
3 passed

La mutación no forma parte del estado final del código.

## 7. Contrato OpenAPI

La incorporación de /catalogo modificó correctamente el esquema OpenAPI del proveedor.
La prueba de contrato detectó inicialmente la divergencia entre FastAPI y:
contracts/openapi-v1.json
El contrato fue regenerado desde app.openapi() y posteriormente se obtuvo:
3 passed

en:
backend/tests/test_contrato_openapi.py
No se debilitó la prueba para hacerla pasar.

## 8. Medición EC-01

Se ejecutó:
python -m pytest backend/tests/test_ec01_catalogo.py -q -s

Configuración:
- 1.000 publicaciones controladas;
- 10 búsquedas consecutivas;
- petición GET /catalogo?q=producto;
- medición con perf_counter().
Resultado:
10/10 ejecuciones <= 2.0 s
Promedio: 0.020482 s
Máximo: 0.050431 s
1 passed

La medición verifica routing HTTP, lógica de búsqueda y serialización con una carga controlada.
No incluye todavía latencia real de MySQL ni red de producción.
Detalle:
docs/evidencias/evidencia-ec01-catalogo-s9-2026-10-01.md

## 9. Uso de IA

El uso de IA y la revisión del equipo están documentados en:
docs/ia.md
Durante S9 se registraron explícitamente:
- propuestas aceptadas;
- propuestas corregidas;
- propuestas rechazadas;
- razones técnicas de rechazo;
- mutación y restauración;
- medición.
Entre las propuestas rechazadas se encuentra permitir que Catálogo acceda directamente al repositorio de Publicaciones, porque rompe la propiedad de datos definida en S6.

## 10. Dependencias

Durante esta porción S9 no se incorporaron nuevas dependencias de producción.
Se revisaron:
- requirements.txt
- frontend/campusmarket/pubspec.yaml
No se agregó una biblioteca nueva como consecuencia de una sugerencia de IA.

## 11. Secretos

Se ejecutó una búsqueda de patrones de alto riesgo:
git grep -n -I -E "AKIA|AIza|sk-[A-Za-z0-9]|ghp_|github_pat_|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY"

Resultado:
Sin coincidencias

Las referencias a PASSWORD, TOKEN y variables relacionadas fueron revisadas.
Los valores root_ci y campusmarket_ci pertenecen al servicio MySQL efímero de GitHub Actions y no corresponden a credenciales productivas.
Detalle:
docs/evidencias/auditoria-s9-dependencias-secretos-2026-10-01.md

## 12. Componente generativo

CampusMarket no incorpora actualmente un componente generativo dentro del producto.
La decisión está documentada en:
docs/adr/0010-no-incorporar-componente-generativo-en-campusmarket.md
La decisión se basa en:
- ausencia de una necesidad funcional demostrada;
- costo adicional;
- latencia;
- dependencia externa;
- privacidad;
- necesidad adicional de evaluación;
- riesgo de generación incorrecta.
El uso de IA como apoyo al desarrollo continúa permitido bajo revisión y verificación del equipo.

## 13. Pruebas verificadas antes del cierre

Resultados obtenidos:
backend/tests/test_catalogo.py
8 passed

backend/tests/test_erosion_s9.py
3 passed

backend/tests/test_contrato_openapi.py
3 passed

backend/tests/test_modularidad_s6.py
5 passed

backend/tests/test_ec01_catalogo.py
1 passed

## 14. Estado actual
La porción S9 cuenta con:
- implementación real;
- ADR;
- trazabilidad;
- pruebas funcionales;
- prueba de erosión;
- evidencia de prueba roja;
- restauración a verde;
- medición EC-01;
- registro de IA;
- auditoría de dependencias;
- auditoría de secretos;
- decisión sobre componente generativo.
Pendiente antes del cierre definitivo:
- commit/hash final;
- ejecución completa en CI sobre ese mismo hash;
- URL del run de GitHub Actions;
- actualización final de esta evidencia con hash y run.

## 15. Commit y CI verificados

**Commit verificado:**

`199defc5887162bcc703bed6d730f0e1eeca4efb`

**Pull Request:**

`#45 - S9 - Materializar catálogo con trazabilidad y verificación arquitectónica`

**GitHub Actions:**

- workflow: `Pruebas del backend`
- run: `#105`
- resultado: `success`

La evidencia S9 queda asociada al mismo estado de código que pasó la verificación automática del backend.


## 16. Lectura de cierre S9 — trazabilidad vigente al 3 de octubre de 2026

Esta sección complementa los resultados históricos anteriores. La entrega S9
se centra en **Catálogo construido con apoyo de IA** y en la capacidad del equipo
para decidir y verificar. El despliegue público es evidencia adicional de operación;
no sustituye la auditoría de erosión, la mutación ni el registro de criterio.

### Estado, periodo y cierre

- Base S8: `784d788`; código contrastado: `7856416795bb4accdf9d05e01adb470654875e56`,
  integrado en `master` mediante PR #51.
- Periodo comparado: [S8 → estado contrastado](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/compare/784d788...7856416795bb4accdf9d05e01adb470654875e56).
- Implementación inicial: [1febc85](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/commit/1febc859a4466e73af706fd364d633bfa5276747), integrada por PR #45.
- Corrección de consultas repetidas: [fda3897](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/commit/fda38976882fd5abcca8486b4b114efd28ca2b1c), integrada dentro de PR #49.
- Moodle indica cierre el **domingo 4 de octubre de 2026, 23:55 America/Bogota**
  (`2026-10-05T04:55:00Z`). Prevalece el aula frente a la hora de la pasada preliminar.
- Este documento prepara el cierre: el estado calificado será el último commit
  de la rama oficial anterior o igual al cierre. Un cambio documental en un fork
  no cuenta hasta integrarse. Los runs siguientes acreditan el SHA indicado,
  no acreditan automáticamente el futuro commit de merge.

### Cadena que debe recorrer el revisor

[ASP-01](../aspectos.md#matriz-general-de-trazabilidad) →
[EC-01](../arc42/10-escenarios-de-calidad.md#ec-01---consulta-de-productos) →
[C4 L3: Catálogo/Publicaciones](../c4/03-componentes-backend.md) →
[ADR-0009](../adr/0009-materializar-catalogo-sin-romper-fronteras.md) y
[ADR-0019](../adr/0019-consultar-imagenes-en-lote-a-traves-de-publicaciones.md) →
[servicio Catálogo](../../backend/app/catalogo/service.py) →
[pruebas funcionales](../../backend/tests/test_catalogo.py),
[erosión](../../backend/tests/test_erosion_s9.py) y
[propiedad de datos](../../backend/tests/test_propiedad_datos.py) →
[mutaciones](../../scripts/verificar_mutaciones_mvp.py) →
[medición HTTP/MySQL](../../scripts/verificar_compose_mvp.py) →
[CI backend](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37173110650) y
[CI Compose](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37173110759).

Catálogo busca, filtra y compone respuestas. Publicaciones conserva la propiedad
de publicaciones y metadatos de imágenes. Catálogo importa capacidades de su
**service**, sin conexión SQL ni repository ajeno. La lectura en lote elimina
viajes repetidos a MySQL y conserva esa frontera. Elegirla evita duplicar SQL,
crear un microservicio sin necesidad o aumentar la cuota para ocultar el defecto.
La decisión se argumenta en ADR-0009/0019; su explicación agrupada está en
[arc42 §9](../arc42/09-decisiones.md#lectura-agrupada-de-las-decisiones-vigentes).

### IA: aceptado, corregido y rechazado

Extracto sintetizado del [registro original y complemento S9](../ia.md#s9--criterio-y-verificacion-del-catalogo):

| Salida o propuesta de IA | Decisión del equipo registrada | Motivo técnico / verificación |
|---|---|---|
| Materializar búsquedas/filtros mediante servicio Catálogo | Aceptada | Porción real ASP-01; mantiene una aplicación y propiedad de Publicaciones |
| Consulta de imágenes por cada publicación | Corregida a lectura en lote | La primera búsqueda de 1000 filas superó 60 s bajo cuota; ADR-0019 y prueba de conexiones constantes |
| Importar el repository de Publicaciones desde Catálogo | Rechazada | Cruza el límite de contexto; la mutación hace fallar la regla de erosión |
| Aumentar recursos o retirar el umbral de dos segundos | Rechazada | Contradice la cuota y el escenario; la corrección debe reducir viajes a persistencia |
| Declarar EC-01 público con una prueba controlada o solo latencia interna | Rechazada | La medición debe indicar qué incluye y compararse con el umbral; no equivale al tiempo visible en el navegador |
| Introducir un modelo generativo por estar en la semana de IA | Rechazada | No existe necesidad funcional demostrada; ADR-0010 evalúa costo, latencia, dependencia y riesgo |

La IA asistió implementación, pruebas y documentación. Este registro atribuye
las decisiones al proceso de revisión documentado del equipo; no demuestra por
sí solo que todos los integrantes puedan explicarlas. Eso se valida en sustentación.

### Auditoría de erosión y defecto controlado

| Hallazgo/regla | Ubicación y corrección | Prueba que detecta una regresión |
|---|---|---|
| Riesgo de importar persistencia ajena | Catálogo llama al servicio propietario; no incorpora SQL | `test_catalogo_no_importa_repository_de_publicaciones` |
| Lecturas N+1 de imágenes observadas bajo cuota | `buscar_publicaciones` obtiene IDs y llama una vez a `listar_imagenes_publicaciones` | `test_catalogo_real_no_repite_conexiones_por_publicacion`: 52 filas, dos galerías, <=4 conexiones, sin mezcla |
| Escritura fuera del propietario | Cada una de las seis tablas tiene repository escritor único; Catálogo no posee tablas | `test_cada_tabla_solo_tiene_escritor_en_su_repository` |
| Import mediante alias o SQL en router/service | Auditoría AST de cuatro contextos y capas | `test_ningun_contexto_importa_repository_ajeno_incluso_por_alias` y `test_routers_y_services_no_acceden_a_conexion_sql` |

Fuentes: [service](../../backend/app/catalogo/service.py),
[pruebas Catálogo](../../backend/tests/test_catalogo.py),
[AST de propiedad](../../backend/tests/test_propiedad_datos.py).

Procedimiento reproducible, con Python 3.12, dependencias de desarrollo instaladas
y MySQL 8.4 de pruebas configurado como en el workflow:

```bash
python -m pytest backend/tests/test_catalogo.py backend/tests/test_erosion_s9.py backend/tests/test_propiedad_datos.py -q
python scripts/verificar_mutaciones_mvp.py
```

El script crea copias temporales de backend/contracts. En una inserta el import
ajeno; en otra sustituye la consulta en lote por una consulta por ID. Ejecuta la
prueba específica y exige **exit code 1 y una aserción fallida**; un error de
colección/importación no se acepta como detección. Al terminar elimina la copia.
El checkout original queda intacto. El
[workflow backend](../../.github/workflows/backend-tests.yml) ejecuta ese script
y comprueba checkout limpio. Los pasos «Verificar que las pruebas detectan
defectos de seguridad y erosión» y «Verificar checkout limpio tras pruebas y
mutaciones» concluyeron success en el
[job del SHA contrastado](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37173110650/job/111349967672).

No se afirma que hubo una importación productiva cruzada si solo se introdujo
como mutación. La consulta N+1 sí fue un defecto medido y corregido; el import
ajeno es un defecto artificial para comprobar que la regla lo detectaría.

### Medición y contraste con EC-01

EC-01 exige al menos 9 de 10 búsquedas de hasta 1000 publicaciones en <=2 s.
Se conservan tres alcances distintos:

| Ejecución | Datos y resultado | Qué acredita |
|---|---|---|
| Primera medición S9, sección 8 y [detalle](./evidencia-ec01-catalogo-s9-2026-10-01.md) | 1000 publicaciones controladas; 10/10; promedio 0,020482 s, máximo 0,050431 s | Routing/lógica/serialización en un entorno controlado; no latencia pública |
| [Checkpoint fda3897](./auditoria-mvp-continuacion-2026-10-03.md) | MySQL real, HTTP loopback, cuota 512 MiB; diez muestras, 10/10; rango 152,70–198,04 ms | Resultado numérico histórico para ese SHA; no atribuir sus valores al SHA actual |
| [Compose del SHA contrastado](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/actions/runs/37173110759) | Paso de medición success; verificador exige 1000 filas reales, diez muestras y >=9/10 en <=2000 ms | Medición repetida bajo cuota. Valores individuales en artefacto `compose-verificado-7856416795bb4accdf9d05e01adb470654875e56`, campo `ec01.samples_ms` |

El [verificador](../../scripts/verificar_compose_mvp.py) usa `perf_counter`,
GET /catalogo con q/modalidad/estado/precios, exige HTTP 200 y 1000 resultados,
y falla si no alcanza el umbral. La infraestructura CI es un medio de medición
de S9, no un sustituto de una prueba extremo a extremo pública.

La [verificación pública adicional](./despliegue-publico-mvp-2026-10-04.md)
conserva el contraste: diez muestras internas estuvieron bajo dos segundos,
mientras el cliente remoto midió 3,273–4,709 s con un catálogo de una publicación.
Por tanto, **EC-01 completo, desde el navegador público y con 1000 filas, no se
declara cerrado**. El criterio S9 de realizar/contrastar una medición tiene evidencia;
el objetivo público necesita otra ejecución y, si incumple, corrección.

### Dependencias y secretos del periodo

La frase histórica «no se incorporaron dependencias» aplica solo a la primera
porción Catálogo. El periodo completo S8→SHA contrastado sí añadió
python-multipart, Pillow, file_picker e integration_test del SDK.
La [auditoría ampliada](./auditoria-s9-dependencias-secretos-2026-10-01.md#ampliacion-al-periodo-s9-completo)
registra necesidad, versión, registro oficial, origen y verificación.

El [workflow backend](../../.github/workflows/backend-tests.yml) ejecuta Ruff,
Gitleaks sobre checkout completo (incluidos docs/ejemplos) y sobre el historial
desde `bfe3222c1e29dddc404560cdd9d61095d4bdb3fe`. Los pasos concluyeron success
para el SHA contrastado; conserva informes redactados en `secretos-7856416795bb4accdf9d05e01adb470654875e56`.
Ese intervalo de Gitleaks no equivale a todo el historial del semestre.
La auditoría histórica aporta el barrido anterior; la revisión final puede
repetir el barrido del CONTRATO sobre el historial completo. No se publican secretos.

### Matriz de la ficha S9

Evaluación técnica de la documentación/código contrastados, no nota del docente.
Las filas Cumple describen el alcance que efectivamente acredita la evidencia.
La integración de este cierre y CI del merge posterior todavía son condiciones
de entrega; no basta con que esta rama del fork exista.

| Criterio literal S9 | Estado | Evidencia y límite |
|---|---|---|
| Porción real construida con IA | Cumple | Catálogo; commits 1febc85/fda3897; registro IA y código enlazados |
| Cadena navegable | Cumple en esta propuesta | ASP-01, EC-01, C4 L3, ADR-0009/0019, service, tests, mutación y medición enlazados |
| ADR argumentado por el equipo | Cumple | ADR-0009/0019 comparan alternativas con propiedad de datos, monolito y cuota |
| Prueba que falla ante el defecto | Cumple | Script de mutaciones y paso CI exitoso; fallo de aserción obligatorio |
| Medición del escenario y contraste | Cumple para alcance medido | HTTP/MySQL/1000 filas/cuota; EC-01 público completo permanece no verificado |
| IA: aceptado/corregido/rechazado con motivo | Cumple | Extracto anterior y docs/ia.md; sustentación confirma comprensión |
| Auditoría de erosión | Cumple | Regla de frontera, AST de escritores/imports, N+1 corregido y mutación |
| Dependencias legítimas verificadas | Cumple | Auditoría ampliada; registros oficiales y resolución/instalación en CI |
| Sin credenciales en código/ejemplos generados | Cumple en checkout contrastado | Gitleaks dir sin hallazgos; no extender al historial completo sin barrerlo |
| Componente generativo evaluado o ADR de no incorporación | Cumple | ADR-0010; el producto no llama a un modelo y no requiere contenedor generativo |

**10 filas con evidencia dentro de los alcances declarados**; no se convierte
este recuento en promesa de nota ni en cierre transversal. El aula califica la
correspondencia, no la extensión del documento. La evaluación final depende
del master vigente al cierre y de que el equipo explique su trabajo.

### Matriz transversal del CONTRATO y pendientes

| Control transversal | Estado al preparar este cierre | Evidencia/acción |
|---|---|---|
| Repositorio oficial público/nombre | Cumple | URL oficial y lectura pública del árbol; `master` |
| Estructura mínima | Cumple | docs/arc42, adr, c4, aspectos, ia y README; §11 de arc42 centraliza riesgos |
| Estado al cierre identificable | No verificado todavía | Cierre aún futuro; guardar hash/fecha del master <=2026-10-05T04:55:00Z |
| Nombres ADR | Cumple | ADR 0001–0019 siguen cuatro dígitos y título en kebab-case |
| ADR aceptados no reescritos | No cumple histórico | Revisor señaló 0002/0003/0005; este cierre no los toca ni borra el hallazgo |
| IA al día | Cumple en esta propuesta | Extracto S9 con criterio y límites; requiere integración |
| CI + scanner Sonar + Quality Gate auditable | No cumple | Backend y Compose verdes; ningún scanner en workflows. Gate automático no satisface CONTRATO §8 |
| Secretos también en historial completo | No verificado por este cierre | CI cubre checkout y un intervalo; repetir barrido completo para declaración global |
| Contribución de tres integrantes | Evidencia histórica; no recontada aquí | Revisión preliminar consolida Nilver/Camilo/Joshua; mantener su fuente, no inventar nueva participación |

[Revisión preliminar del docente](https://github.com/ISCOUTB/AS_202620_feedback/blob/master/revisiones/2026-2/AS_202620_PROYECTO_CAMPUSMARKET/semana-09-evidencia-s9.md)
evaluó `784d788`, con periodo S9 vacío; no es una evaluación de `7856416795bb4accdf9d05e01adb470654875e56`.
La entrega nueva incorpora commits y evidencia del periodo, pero no autoriza
a cambiar retroactivamente aquel informe.

### Guion de explicación del equipo

1. Catálogo consulta datos cuyo propietario es Publicaciones; enseñar ASP-01 y C4 L3.
2. Justificar el service propietario frente a SQL ajeno/microservicio, con ADR-0009.
3. Mostrar el defecto N+1 medido, la consulta en lote y su costo, con ADR-0019.
4. Enseñar la mutación y por qué solo un fallo de aserción cuenta como detección.
5. Contrastar las diez muestras con dos segundos, indicando loopback/MySQL/cuota.
6. Mostrar una propuesta de IA rechazada y explicar el motivo técnico.
7. Declarar límites: medición pública, scanner y hallazgos históricos permanecen visibles.
