# Evidencia EC-01 - Consulta de productos

**Proyecto:** CampusMarket
**Semana:** S9
**Fecha:** 2026-10-01
**Aspecto:** ASP-01 - Consulta y búsqueda de productos
**Escenario:** EC-01 - Consulta de productos
**ADR relacionado:** ADR-0009

---

## 1. Objetivo

Verificar el comportamiento de consulta del catálogo de CampusMarket frente al escenario EC-01.

El escenario establece:

- catálogo de hasta 1.000 publicaciones;
- 10 búsquedas consecutivas;
- al menos 9 de las 10 búsquedas deben responder en un máximo de 2 segundos.

---

## 2. Implementación evaluada

La capacidad evaluada corresponde al nuevo contexto funcional de Catálogo:

- `backend/app/catalogo/router.py`
- `backend/app/catalogo/service.py`

El módulo Catálogo consume la capacidad de lectura provista por Gestión de Publicaciones y no accede directamente al repositorio de persistencia.

La prueba utilizada es:

`backend/tests/test_ec01_catalogo.py`

---

## 3. Configuración de la medición

Para obtener una carga determinista se utilizaron:

- 1.000 publicaciones de prueba;
- petición HTTP a `GET /catalogo`;
- parámetro de búsqueda `q=producto`;
- `FastAPI TestClient`;
- medición mediante `time.perf_counter()`;
- 10 ejecuciones consecutivas.

Las 1.000 publicaciones fueron inyectadas mediante `monkeypatch` sobre la capacidad de lectura utilizada por Catálogo.

Por tanto, esta medición verifica:

- routing HTTP;
- validación de FastAPI;
- ejecución del servicio de Catálogo;
- búsqueda sobre 1.000 publicaciones;
- serialización de la respuesta HTTP.

Esta medición no incluye la latencia real de acceso a MySQL.

---

## 4. Resultados

| Ejecución | Tiempo |
|---|---:|
| 1 | 0.050431 s |
| 2 | 0.014077 s |
| 3 | 0.018896 s |
| 4 | 0.020142 s |
| 5 | 0.017189 s |
| 6 | 0.020874 s |
| 7 | 0.020386 s |
| 8 | 0.014462 s |
| 9 | 0.014051 s |
| 10 | 0.014317 s |

**Promedio:** 0.020482 s
**Máximo:** 0.050431 s
**Dentro del umbral:** 10/10

---

## 5. Evaluación

Criterio definido por EC-01:

> Al menos 9 de 10 búsquedas deben responder en un máximo de 2 segundos con un catálogo de hasta 1.000 publicaciones.

Resultado obtenido:

**10/10 ejecuciones <= 2 segundos.**

La medición controlada del comportamiento de búsqueda satisface el umbral de EC-01.

---

## 6. Alcance de la conclusión

La evidencia permite afirmar que la implementación de búsqueda y filtrado del módulo Catálogo satisface el umbral de EC-01 bajo una carga controlada de 1.000 publicaciones.

No se afirma todavía que el escenario completo haya sido validado extremo a extremo contra una instancia real de MySQL o contra el despliegue público.

La medición end-to-end podrá repetirse posteriormente sobre el entorno desplegado para incorporar la latencia real de persistencia y red.

---

## 7. Comando ejecutado

python -m pytest backend/tests/test_ec01_catalogo.py -q -s

Resultado:
EC01 ejecución 1: 0.050431 s
EC01 ejecución 2: 0.014077 s
EC01 ejecución 3: 0.018896 s
EC01 ejecución 4: 0.020142 s
EC01 ejecución 5: 0.017189 s
EC01 ejecución 6: 0.020874 s
EC01 ejecución 7: 0.020386 s
EC01 ejecución 8: 0.014462 s
EC01 ejecución 9: 0.014051 s
EC01 ejecución 10: 0.014317 s

EC01 resultado: 10/10 ejecuciones <= 2.0 s
EC01 promedio: 0.020482 s
EC01 máximo: 0.050431 s

1 passed

## 8. Trazabilidad
ASP-01
   ↓
EC-01
   ↓
ADR-0009
   ↓
backend/app/catalogo/
   ↓
backend/tests/test_catalogo.py
   ↓
backend/tests/test_ec01_catalogo.py
   ↓
10/10 <= 2 s

## 9. Estado
Medición controlada EC-01: SATISFECHA
Validación end-to-end con persistencia y entorno desplegado: pendiente.
