# ADR-0022 — Mantener MySQL como fuente de verdad y evitar proyecciones asíncronas en S12

- Estado: **Aceptado para el alcance S12**, sujeto a verificación de la evidencia final y revisión del equipo.
- Fecha: 2026-10-25 (America/Bogota).
- Base de análisis: `master` `a237dd2f22b02bb547f87a07d15b6d31ea0dc758`.
- Relacionados: [ADR-0001](0001-usar-monolito-modular.md), [ADR-0004](0004-migrar-persistencia-a-mysql.md), [ADR-0021](0021-mantener-catalogo-en-el-monolito-modular.md). **No modifica** ninguno de ellos.

## Contexto y decisión difícil de revertir

La aplicación implementada emplea MySQL como persistencia del dominio, con propiedad de escritura por contexto (Usuarios, Publicaciones y Administración). Catálogo consulta mediante el servicio de Publicaciones y no mantiene una proyección propia. El código de creación y modificación de publicaciones realiza escrituras SQL; la revisión de reportes utiliza una transacción con `FOR UPDATE`. Las imágenes se almacenan aparte y se vinculan por metadatos SQL.

La decisión evaluada no es únicamente escoger una marca de base de datos: **dónde está la fuente de verdad y qué contextos pueden escribir cada dato**. Revertir una persistencia consolidada o repartir su autoridad exigiría migrar registros, claves foráneas, lecturas, escrituras, despliegue, contratos, copias y procedimientos de recuperación. Por eso su costo de reversión es mayor que ajustar un TTL o una consulta. No se afirma una cuantificación económica no medida.

## Alternativas

| Alternativa | Ventajas | Costo y riesgo |
|---|---|---|
| A. Mantener MySQL como fuente de verdad y lectura sin proyección asíncrona | Consistencia de escrituras locales, menos componentes, respeta el MVP y los ADR anteriores | Catálogo sigue acoplado a disponibilidad de Publicaciones/MySQL; escala conjuntamente |
| B. Proyección separada de Catálogo alimentada por eventos | Lecturas aislables, posible escalado independiente | Doble escritura/outbox, deduplicación, versiones, lag, reconciliación, broker y migración de lecturas |
| C. Nuevo almacén NoSQL como autoridad del dominio | Modelo de consultas flexible en casos específicos | Migración de esquema/identificadores, nuevas garantías, validación de integridad, operaciones y rollback complejos |

## Decisión

Elegir **A** para S12. MySQL continúa como única fuente de verdad; respetar el propietario único por tabla y las transacciones locales. **No agregar Redis, broker, proyección distribuida ni una caché compartida sin un escenario medido que lo exija**. El flujo por eventos, si se ensaya en el taller, será un prototipo aislado, no parte del C4 productivo.

## Consecuencias y garantías

- Escrituras confirmadas en MySQL son la referencia; no inferir consistencia global en filesystem o entre transacciones independientes.
- Las lecturas de Catálogo llegan a los servicios propietarios sin réplica asíncrona de Catálogo; no prometer consistencia fuerte universal en todas las rutas.
- Evitar caché de datos mutables en el servidor para S12: tras una escritura confirmada, otra consulta debe consultar la fuente en lugar de devolver una entrada caducada. La política de invalidación es **no generar entradas persistentes para lecturas del dominio**. El diseño futuro, condicionado a medición, sería cache-aside con invalidación de claves afectadas al confirmar escrituras, además de TTL de respaldo; no se declara implementado.
- La creación de publicación aún puede duplicarse ante un segundo POST después de un timeout, según [evidencia S11](../evidencias/evidencia-s11-2026-10-18.md). La consistencia transaccional no implica idempotencia de solicitudes.
- Los archivos de imágenes no comparten una transacción atómica con MySQL y necesitan compensación/reconciliación.

## Costo de reversión y plan futuro

Si se decide incorporar proyección/eventos, deben diseñarse contrato versionado, transactional outbox, claves idempotentes, estado de reprocesamiento, DLQ, lag máximo aceptado, reconstrucción/backfill, medición y retorno seguro antes de hacer el corte de lecturas. La migración puede afectar cada publicación e imagen, consumidores y despliegues. El costo concreto depende de volumen y operaciones que aún no se han medido. Este ADR no reemplaza ni reescribe decisiones previas.

## Trazabilidad

- Alcance: [Evidencia S12](../evidencias/evidencia-s12-2026-10-25.md) y [EC-01/EC-03](../arc42/10-escenarios-de-calidad.md).
- Modelos: [C4 nivel 2](../c4/02-contenedores.md), [arc42 sección 8](../arc42/08-conceptos-transversales.md).
- Código: [Publicaciones](../../backend/app/publicaciones/repository.py), [Catálogo](../../backend/app/catalogo/service.py), [Administración](../../backend/app/administracion/repository.py).
- Pruebas de base, **sin afirmar un run nuevo**: [test_catalogo.py](../../backend/tests/test_catalogo.py), [test_gestion_publicaciones.py](../../backend/tests/test_gestion_publicaciones.py), [test_propiedad_datos.py](../../backend/tests/test_propiedad_datos.py).
- Implementación: este ADR mantiene la topología existente; no introduce código nuevo. Hash y CI de cierre se registrarán en la evidencia cuando puedan verificarse.
