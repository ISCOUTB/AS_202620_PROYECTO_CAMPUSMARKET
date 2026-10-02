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
