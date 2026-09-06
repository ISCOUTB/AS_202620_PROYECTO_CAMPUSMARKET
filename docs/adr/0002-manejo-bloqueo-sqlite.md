# ADR-0002 - Manejar de forma controlada el bloqueo temporal de SQLite

**Estado:** Aceptado  
**Fecha:** 2026-09-05  
**Decisión:** Aplicar espera acotada y degradación controlada ante bloqueo temporal de SQLite  
**Escenario principal:** EC-05 - Degradación ante bloqueo temporal de persistencia  
**Restricción principal:** R-07 - Persistencia sin nueva infraestructura durante el primer corte  
**Aspecto relacionado:** ASP-06 - Degradación controlada ante bloqueo de persistencia  

---

## 1. Contexto

CampusMarket implementa el corte vertical de creación de publicaciones mediante:

**Flutter Web → FastAPI → módulo `publicaciones` → SQLite**

Para la evaluación arquitectónica de S5, el equipo definió:

**R-07 - Persistencia sin nueva infraestructura durante el primer corte.**

R-07 exige mantener SQLite como mecanismo de persistencia y conservar el
backend como una única aplicación monolítica modular, sin dividirlo en nuevos
servicios desplegables. Como respuesta al reto no se incorporarán bases de
datos externas, colas ni cachés distribuidas.

La condición adversa seleccionada es un bloqueo temporal de escritura sobre
SQLite durante la creación de una publicación.

El escenario relacionado es:

**EC-05 - Degradación ante bloqueo temporal de persistencia.**

EC-05 establece que, mientras SQLite se encuentra bloqueada, CampusMarket debe:

- responder mediante HTTP `503`;
- finalizar la solicitud en un máximo de `2 s`;
- no producir escrituras parciales;
- informar la indisponibilidad temporal;
- recuperar la creación normal después de liberar SQLite.

### Línea base

Antes de aplicar cambios se obtuvo:

| Métrica | Línea base |
|---|---:|
| HTTP durante bloqueo | `500` |
| Tiempo durante bloqueo | `7.323 s` |
| Escritura parcial | `No` |
| HTTP después de liberar SQLite | `201` |
| Tiempo de recuperación | `0.007 s` |

Evidencia:

[Línea base de bloqueo SQLite](../evidencias/linea-base-bloqueo-sqlite-2026-09-05.md)

La línea base mostró que el sistema preservaba la integridad y se recuperaba
después de liberar SQLite, pero presentaba dos problemas:

1. trataba la indisponibilidad temporal como un error interno HTTP `500`;
2. mantenía la solicitud esperando `7.323 s`, superando el umbral de `2 s`.

Se requería, por tanto, mejorar el comportamiento observable sin violar R-07.

---

## 2. Fuerzas arquitectónicas

La decisión está condicionada por:

- **Disponibilidad / resiliencia:** degradar de forma controlada ante el bloqueo.
- **Tiempo de respuesta:** cumplir el umbral de `≤ 2 s` definido en EC-05.
- **Integridad:** evitar escrituras parciales.
- **Simplicidad operativa:** no incorporar nueva infraestructura.
- **Mantenibilidad:** conservar las fronteras del módulo `publicaciones`.
- **Trazabilidad:** permitir pruebas y mediciones reproducibles.
- **Reversibilidad:** no impedir una futura sustitución de SQLite.

---

## 3. Alternativas evaluadas

### 3.1 Alternativa A - Mantener el comportamiento existente

Mantener la configuración y manejo de errores existentes.

**Ventajas:**

- no requiere cambios;
- no introduce lógica adicional.

**Desventajas:**

- devuelve HTTP `500`;
- tarda `7.323 s` durante el bloqueo;
- no diferencia una indisponibilidad temporal;
- incumple el umbral de EC-05.

**Resultado:** descartada porque la línea base demuestra que no cumple EC-05.

---

### 3.2 Alternativa B - Espera acotada y degradación mediante HTTP 503

Mantener SQLite y configurar un tiempo de espera corto para adquirir el
bloqueo de persistencia.

Si SQLite continúa bloqueada, el sistema identifica específicamente la
condición y responde mediante HTTP `503 Service Unavailable`.

Para el primer corte se adopta un timeout SQLite de **`0.5 s`**.

No se incorporan reintentos automáticos.

**Ventajas:**

- permite cumplir el umbral de EC-05;
- diferencia una indisponibilidad temporal de un error interno;
- mantiene SQLite;
- conserva el backend como una única aplicación monolítica modular;
- no agrega infraestructura;
- conserva la integridad transaccional;
- mantiene las fronteras de `publicaciones`;
- permite verificación reproducible.

**Desventajas:**

- una solicitud puede ser rechazada aunque el bloqueo se libere poco después;
- el cliente deberá volver a intentar la operación;
- se agrega lógica específica para clasificar el bloqueo;
- el timeout deberá reconsiderarse si cambia la carga.

**Resultado:** aceptada.

---

### 3.3 Alternativa C - Migrar a PostgreSQL u otra base externa

Sustituir SQLite por un motor de persistencia con mayores capacidades de
concurrencia.

**Ventajas:**

- mayor capacidad para múltiples escritores;
- mejores mecanismos de concurrencia;
- mayor capacidad de evolución ante cargas superiores.

**Desventajas:**

- introduce nueva infraestructura;
- aumenta la complejidad de configuración y despliegue;
- requiere migración;
- incrementa el costo operativo;
- modifica más elementos de los necesarios;
- incumple R-07 durante el primer corte.

**Resultado:** descartada para S5.

Esta alternativa puede reconsiderarse posteriormente si existe evidencia que
justifique la migración.

---

## 4. Decisión

**CampusMarket adopta la Alternativa B: espera acotada y degradación
controlada mediante HTTP `503`.**

La implementación:

1. mantiene SQLite como persistencia;
2. conserva el backend como una única aplicación monolítica modular;
3. configura un timeout SQLite de `0.5 s`;
4. detecta específicamente `SQLITE_BUSY` y `SQLITE_LOCKED`;
5. diferencia el bloqueo temporal de otros errores de persistencia;
6. traduce la indisponibilidad temporal a HTTP `503 Service Unavailable`;
7. devuelve un mensaje explícito al cliente;
8. evita escrituras parciales;
9. permite la recuperación normal después de liberar SQLite;
10. verifica el comportamiento mediante prueba automatizada y medición reproducible.

No se implementan reintentos automáticos.

El cliente puede volver a intentar la operación cuando la persistencia se
encuentre nuevamente disponible.

---

## 5. Justificación

La alternativa seleccionada ofrece el mejor equilibrio entre disponibilidad,
simplicidad operativa, mantenibilidad y cumplimiento de R-07.

La línea base demostró que el problema principal no era la pérdida de
integridad, sino el tiempo de espera y la forma en que la indisponibilidad
temporal era comunicada.

El timeout de `0.5 s` deja margen frente al umbral máximo de `2 s` definido
por EC-05.

La medición posterior confirmó una respuesta HTTP `503` en `1.283 s`, sin
escrituras parciales y con recuperación posterior mediante HTTP `201`.

Además, la solución permanece dentro del módulo `publicaciones`, no modifica
la topología C4 y no introduce servicios distribuidos.

---

## 6. Tácticas arquitectónicas

### Espera acotada

Se limita el tiempo de espera por SQLite.

**Objetivo:** evitar tiempos prolongados como los `7.323 s` de la línea base.

### Detección explícita del bloqueo

Se identifican específicamente las condiciones `SQLITE_BUSY` y
`SQLITE_LOCKED`.

**Objetivo:** evitar convertir cualquier error de persistencia en HTTP `503`.

### Degradación controlada

La indisponibilidad temporal se traduce a HTTP `503`.

Mensaje utilizado:

`La persistencia está temporalmente no disponible. Intenta nuevamente.`

### Preservación de integridad

Una operación fallida no confirma escrituras parciales.

### Recuperación

Después de liberar SQLite, una nueva solicitud puede ejecutarse normalmente.

---

## 7. Consecuencias

### Positivas

- la solicitud bloqueada responde dentro del umbral;
- el cliente distingue una indisponibilidad temporal;
- se conserva SQLite;
- no se incorpora infraestructura adicional;
- se conserva el backend monolítico modular;
- se mantienen las fronteras de `publicaciones`;
- el escenario puede verificarse automáticamente;
- se conserva la posibilidad de sustituir SQLite posteriormente;
- las conexiones SQLite se cierran explícitamente después de cada operación.

### Negativas

- una operación puede ser rechazada temporalmente;
- el usuario puede necesitar volver a intentar;
- se incorpora lógica adicional de manejo de errores;
- el timeout se convierte en una política que deberá revisarse si cambia la carga.

### Riesgo aceptado

El equipo acepta rechazar temporalmente una operación en lugar de mantenerla
bloqueada durante varios segundos.

---

## 8. Criterio de reconsideración

ADR-0002 deberá reconsiderarse si aparece evidencia de que SQLite deja de ser
suficiente.

Se revisará la decisión si ocurre alguna de estas condiciones:

- más del **5 % de 100 intentos de creación** bajo una carga representativa
  termina en indisponibilidad por contención de escritura;
- CampusMarket requiere múltiples instancias del backend escribiendo
  concurrentemente sobre la misma persistencia;
- los requisitos futuros demandan una concurrencia incompatible con EC-05;
- una nueva restricción elimina la obligación de mantener SQLite.

En ese caso se volverán a evaluar alternativas como PostgreSQL.

---

## 9. Costo de reversión

El costo de reversión se considera **moderado**.

La lógica específica de SQLite se encuentra localizada dentro del módulo
`publicaciones` y no modifica las fronteras generales establecidas por
ADR-0001.

Una futura sustitución de SQLite requeriría principalmente:

- reemplazar o adaptar el mecanismo de persistencia;
- retirar la detección específica de bloqueo SQLite;
- conservar o redefinir la excepción de indisponibilidad;
- ejecutar nuevamente las pruebas del corte vertical;
- volver a medir EC-05 con la nueva tecnología.

El equipo acepta este costo porque evita introducir infraestructura adicional
antes de contar con evidencia que la justifique.

---

## 10. Impacto sobre la implementación

Los cambios principales se localizaron en:

```text
backend/app/publicaciones/repository.py
backend/app/publicaciones/service.py
backend/app/publicaciones/router.py
frontend/campusmarket/lib/publicaciones/publicaciones_api.dart
frontend/campusmarket/lib/publicaciones/publicacion_form_page.dart
backend/tests/test_publicaciones_vertical.py
scripts/medir_bloqueo_sqlite.py
```

Responsabilidades:

- `repository.py`: configura el timeout de `0.5 s`, identifica
  `SQLITE_BUSY` y `SQLITE_LOCKED` y traduce el bloqueo a indisponibilidad
  temporal.
- `service.py`: mantiene la traducción dentro de la frontera funcional de
  `publicaciones`.
- `router.py`: responde mediante HTTP `503 Service Unavailable`.
- `publicaciones_api.dart`: identifica específicamente HTTP `503`.
- `publicacion_form_page.dart`: informa al usuario sobre la indisponibilidad
  temporal.
- `test_publicaciones_vertical.py`: verifica respuesta, tiempo, integridad y
  recuperación.
- `medir_bloqueo_sqlite.py`: reproduce y mide el escenario adverso.

La implementación conserva:

**Flutter Web → FastAPI → módulo `publicaciones` → SQLite**

El cambio modifica el comportamiento ante la condición adversa, pero no
cambia la topología de contenedores ni divide el backend en nuevos servicios
desplegables.

---

## 11. Verificación y resultados

La comparación reproducible es:

| Métrica | Línea base | Después de ADR-0002 | Umbral EC-05 | Resultado |
|---|---:|---:|---:|---|
| HTTP durante bloqueo | `500` | `503` | `503` | Cumple |
| Tiempo durante bloqueo | `7.323 s` | `1.283 s` | `≤ 2 s` | Cumple |
| Escritura parcial | `No` | `No` | `No` | Cumple |
| HTTP después de liberar SQLite | `201` | `201` | `201` | Cumple |
| Tiempo de recuperación | `0.007 s` | `0.006 s` | Informativo | Correcto |

Una ejecución posterior confirmó nuevamente:

- HTTP `503`;
- `1.138 s` durante el bloqueo;
- ninguna escritura parcial;
- recuperación HTTP `201`.

La medición formal utilizada como evidencia es la ejecución de **`1.283 s`**.

Evidencias:

- [Línea base](../evidencias/linea-base-bloqueo-sqlite-2026-09-05.md)
- [Medición posterior](../evidencias/medicion-bloqueo-sqlite-2026-09-06.md)
- [Prueba automatizada](../../backend/tests/test_publicaciones_vertical.py)
- [Script de medición](../../scripts/medir_bloqueo_sqlite.py)

---

## 12. Trazabilidad de implementación

La respuesta arquitectónica de S5 fue consolidada mediante:

- Pull Request:
  [#28 - Completar reto arquitectónico S5 del primer corte](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/pull/28)
- Commit de integración:
  [`ff68cf2`](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/commit/ff68cf255b90340634e0760f056870f9a19e9abd)

La cadena principal es:

**ASP-06 → R-07 / EC-05 → C4 Nivel 2 → ADR-0002 → código → prueba → medición → evidencia**

Elementos relacionados:

- [R-07](../arc42/02-restricciones.md#r-07-persistencia-sin-nueva-infraestructura-durante-el-primer-corte)
- [EC-05](../arc42/10-escenarios-de-calidad.md#ec-05---degradación-ante-bloqueo-temporal-de-persistencia)
- [C4 Nivel 2](../c4/02-contenedores.md)
- [ASP-06](../aspectos.md)
- [Registro de IA](../ia.md)

ADR-0002 queda así asociado explícitamente con:

**restricción → escenario de calidad → decisión → implementación → prueba → medición → evidencia**
