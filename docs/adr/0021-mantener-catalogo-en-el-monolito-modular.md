# ADR-0021 — Mantener Catálogo en el monolito modular

- Estado: **Decidido para S11 — no extraer Catálogo**. Se conserva el monolito modular vigente; esta decisión no implica haber implementado idempotencia ni haber extraído un servicio.
- Fecha: 2026-10-18 (America/Bogota).
- Base: `master` `1582c1ff609202fa2cc4a06fa14d18b9b61bed74`.
- Relación: respeta [ADR-0001](0001-usar-monolito-modular.md), [ADR-0003](0003-usar-integracion-sincrona-http-json.md), [ADR-0009](0009-materializar-catalogo-sin-romper-fronteras.md) y [ADR-0018](0018-ejecutar-el-monolito-en-dokploy-con-volumenes.md). No sustituye ni reescribe ADR aceptados anteriores.

## 1. Contexto y problema

CampusMarket integra Flutter Web/Android con una API FastAPI y MySQL. El backend tiene contextos Usuarios, Publicaciones, Catálogo y Administración **dentro de un mismo proceso FastAPI**. Actualmente `backend/app/catalogo/service.py` consume `listar_publicaciones` y `listar_imagenes_publicaciones` de `backend/app/publicaciones/service.py`; no utiliza HTTP interno ni escribe directamente tablas ajenas. Catálogo tiene dependencia funcional de datos propiedad de Publicaciones. El despliegue usa cuotas limitadas de CPU/memoria en Dokploy, según `deploy/compose.lab.yaml` y la vista de despliegue.

**Decisión a tomar:** ¿conviene extraer Catálogo a un servicio independiente durante S11 para incrementar autonomía y resiliencia? Separarlo añade una frontera de red, fallo parcial, observabilidad, seguridad entre servicios y estrategia de coherencia de datos. No se ha acreditado carga o necesidad de escalamiento independiente que compense ese costo.

## 2. Opciones evaluadas y criterios

| Criterio | A. **No extraer:** mantener módulo Catálogo dentro de FastAPI | B. Extraer Catálogo con API propia y consultas síncronas a Publicaciones | C. Extraer Catálogo con proyección propia y eventos |
|---|---|---|---|
| Desarrollo/despliegue | Una unidad operable y suites existentes; conserva separación por módulos | Añade build, servicio, ruteo, secretos y dos unidades desplegables | Añade B + bus, proyección, consumidores y recuperación |
| Fallos parciales | Sin nueva llamada de red entre Catálogo y Publicaciones | Timeout/503/latencia de dependencia entre servicios | Mensajes repetidos/reordenados; consistencia eventual |
| Consistencia de datos | Publicaciones sigue como propietario; llamadas locales de lectura | Publicaciones sigue propietario; lectura remota | Proyección con lag; requiere outbox, idempotencia y reconciliación |
| Escalado independiente | No | Sí, con costo adicional | Sí, con complejidad mayor |
| Restricción de recursos del laboratorio | Se ajusta a la topología existente | Nuevos recursos y vigilancia de consumo | Operación y recursos superiores |
| Evidencia de necesidad actual | No se ha mostrado cuello de botella que exija extracción | Beneficio hipotético; falta prueba de carga aislada | Fuera del alcance y necesidad actual de S11 |

## 3. Decisión

**Elegir A: no extraer Catálogo ahora.** Mantener la frontera lógica Catálogo/Publicaciones, su API externa HTTP/JSON y el propietario único por tabla. Es una **opción evaluada y preferida** por simplicidad operativa, menor superficie de fallos distribuidos, recursos del laboratorio y falta de un beneficio medido de extraer. No se usa «falta de tiempo» como criterio. La integración distribuida real a endurecer primero es Flutter→FastAPI, en especial repetición de `POST /publicaciones`.

## 4. Consecuencias y condiciones de revisión

**A favor:** sin salto remoto nuevo en lectura de catálogo; conserva pruebas y restricciones de propiedad de datos; no aumenta servicios ni dependencias de producción. **En contra:** no se escala Catálogo de forma independiente; una caída del proceso FastAPI afecta también Catálogo; despliegue y versiones permanecen vinculados.

**Reabrir mediante un nuevo ADR** si pruebas reproducibles muestran saturación aislable de Catálogo, crecimiento relevante de tráfico/costo, necesidad real de despliegues independientes, límites de propiedad suficientes y presupuesto para health/alertas, autenticación entre servicios, contratos, fallos parciales y consistencia. Si se decide separar después, considerar migración gradual tipo *Strangler*, con canary, pruebas contractuales y retorno seguro; no ejecutar una extracción de una sola vez.

## 5. Trazabilidad y validación

- Requisitos: Evidencia S11 (decisión explícita y alternativa no extraer); EC-01 consulta y EC-03 modificabilidad.
- Arquitectura: [C4 L2](../c4/02-contenedores.md), [C4 L3](../c4/03-componentes-backend.md), [arc42 08](../arc42/08-conceptos-transversales.md), [arc42 11](../arc42/11-riesgos-y-deuda-tecnica.md).
- Código: [`catalogo/service.py`](../../backend/app/catalogo/service.py), [`publicaciones/service.py`](../../backend/app/publicaciones/service.py), [`publicaciones/repository.py`](../../backend/app/publicaciones/repository.py).
- Pruebas ya existentes (sin afirmar ejecución nueva): [`test_modularidad_s6.py`](../../backend/tests/test_modularidad_s6.py), [`test_propiedad_datos.py`](../../backend/tests/test_propiedad_datos.py), [`test_erosion_s9.py`](../../backend/tests/test_erosion_s9.py), [`test_catalogo.py`](../../backend/tests/test_catalogo.py).
- Evidencia S11: [modos de fallo, diseño, límites y CI por revisión](../evidencias/evidencia-s11-2026-10-18.md). Integración: [PR #56](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/pull/56); cierre: [PR #58](https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET/pull/58). Las mitigaciones no implementadas conservan ese estado.
